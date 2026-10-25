#!/usr/bin/env python
"""
generate_odmap_data.py
──────────────────────
Build ODMAP's ALL_INTERACTIONS_RAW from REAL FDA data, structured by Gemini.

Pipeline (Option 2):
  1. Read the drug roster (brand -> ingredient) straight out of odmap_v6.html.
  2. For each drug, pull openFDA's real `drug_interactions` label text (free API).
  3. Hand the real FDA text + the roster to Gemini and ask it ONLY to STRUCTURE
     that text into pairwise records — not to invent interactions.
  4. Write odmap_interactions.json and splice the records into the HTML's
     ALL_INTERACTIONS_RAW array, keeping ODMAP a static, offline file.

Keys are read from .env (GEMINI_API_KEY, optional OPENFDA_API_KEY).
Run:  .venv\\Scripts\\python.exe generate_odmap_data.py
"""

import json
import os
import re
import sys
import time

import requests
from dotenv import load_dotenv

try:
    from google import genai
    from google.genai import types
except ImportError:
    sys.exit("google-genai not installed. Run: .venv\\Scripts\\python.exe -m pip install google-genai")

load_dotenv()

HERE = os.path.dirname(os.path.abspath(__file__))
HTML_PATH = os.path.join(HERE, "odmap_v6.html")
JSON_OUT = os.path.join(HERE, "odmap_interactions.json")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash").strip() or "gemini-2.5-flash"
OPENFDA_API_KEY = os.getenv("OPENFDA_API_KEY", "").strip()
OPENFDA_LABEL = "https://api.fda.gov/drug/label.json"

VALID_SEVERITY = {"severe", "moderate", "mild"}
VALID_TYPE = {"Hematologic", "Metabolic", "Cardiovascular", "Neurological", "Other"}


# ── 1. Parse the roster from the HTML ──────────────────────────────────────────
def parse_roster(html: str) -> dict[str, str]:
    """Return {brandName: ingredient} from the ALL_DRUGS block."""
    m = re.search(r"const ALL_DRUGS\s*=\s*\{(.*?)\n\};", html, re.DOTALL)
    if not m:
        sys.exit("Could not find ALL_DRUGS block in odmap_v6.html")
    block = m.group(1)
    roster: dict[str, str] = {}
    for line in block.splitlines():
        brand_m = re.search(r'"([^"]+)"\s*:\s*\{', line)
        ing_m = re.search(r'ingredient\s*:\s*"([^"]+)"', line)
        if brand_m and ing_m:
            roster[brand_m.group(1)] = ing_m.group(1)
    return roster


# ── 2. openFDA real interaction text ───────────────────────────────────────────
def fetch_fda_interactions(ingredient: str) -> tuple[str, str]:
    """Return (interaction_text, source_url) from the FDA label; ('','') if none."""
    query = f'openfda.generic_name:"{ingredient}"'
    params = {"search": query, "limit": 1}
    if OPENFDA_API_KEY:
        params["api_key"] = OPENFDA_API_KEY
    try:
        r = requests.get(OPENFDA_LABEL, params=params, timeout=20)
        if r.status_code == 404:
            return "", ""
        r.raise_for_status()
        results = r.json().get("results", [])
        if not results:
            return "", ""
        res = results[0]
        texts = res.get("drug_interactions") or res.get("drug_interactions_table") or []
        text = " ".join(texts) if isinstance(texts, list) else str(texts)
        set_id = res.get("set_id", "")
        url = f"https://labels.fda.gov/{set_id}" if set_id else "https://open.fda.gov/apis/drug/label/"
        return text.strip()[:8000], url
    except requests.RequestException as e:
        print(f"    openFDA error for {ingredient}: {e}")
        return "", ""


# ── 3. Gemini structures the real text into pairs ──────────────────────────────
INTERACTION_SCHEMA = {
    "type": "OBJECT",
    "properties": {
        "interactions": {
            "type": "ARRAY",
            "items": {
                "type": "OBJECT",
                "properties": {
                    "drug_a": {"type": "STRING"},
                    "drug_b": {"type": "STRING"},
                    "severity": {"type": "STRING", "enum": ["severe", "moderate", "mild"]},
                    "type": {
                        "type": "STRING",
                        "enum": ["Hematologic", "Metabolic", "Cardiovascular", "Neurological", "Other"],
                    },
                    "desc": {"type": "STRING"},
                },
                "required": ["drug_a", "drug_b", "severity", "type", "desc"],
            },
        }
    },
    "required": ["interactions"],
}


def structure_with_gemini(client, roster: dict[str, str], fda_blurbs: dict[str, tuple[str, str]]):
    brands = list(roster.keys())
    roster_lines = "\n".join(f'- "{b}" (active ingredient: {roster[b]})' for b in brands)
    evidence = "\n\n".join(
        f'### {b} — FDA label drug interactions:\n{fda_blurbs[b][0]}'
        for b in brands
        if fda_blurbs[b][0]
    )

    prompt = f"""You are a clinical pharmacology data extractor.

Below is the official FDA drug-interaction label text for a set of drugs, plus a
roster of drugs we track. STRUCTURE the FDA text into pairwise interactions.

STRICT RULES:
- Only output a pair if BOTH drugs are in the roster (use the exact brand name as drug_a/drug_b).
- Base every interaction on the FDA label text provided. Do NOT invent interactions
  that the FDA text does not support. If a drug or drug class is named generically
  in the text (e.g. "NSAIDs", "SSRIs"), you may map it to a roster drug of that class.
- severity: severe | moderate | mild. type: Hematologic | Metabolic | Cardiovascular | Neurological | Other.
- desc: one patient-friendly sentence explaining the interaction and its mechanism.
- Do not duplicate a pair (A,B) and (B,A).

ROSTER:
{roster_lines}

FDA EVIDENCE:
{evidence}
"""

    resp = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=INTERACTION_SCHEMA,
        ),
    )
    data = json.loads(resp.text or "{}")
    return data.get("interactions", [])


# ── 4. Validate + dedupe + attach FDA citation ─────────────────────────────────
def finalize(raw, roster, fda_blurbs):
    brands_lower = {b.lower(): b for b in roster}
    seen = set()
    out = []
    for item in raw:
        a = brands_lower.get(str(item.get("drug_a", "")).lower())
        b = brands_lower.get(str(item.get("drug_b", "")).lower())
        if not a or not b or a == b:
            continue
        key = tuple(sorted((a, b)))
        if key in seen:
            continue
        seen.add(key)
        severity = item.get("severity", "moderate")
        if severity not in VALID_SEVERITY:
            severity = "moderate"
        itype = item.get("type", "Other")
        if itype not in VALID_TYPE:
            itype = "Other"
        # Cite the FDA label of drug_a (fall back to drug_b).
        citation = fda_blurbs.get(a, ("", ""))[1] or fda_blurbs.get(b, ("", ""))[1] \
            or "https://open.fda.gov/apis/drug/label/"
        out.append({
            "drug_a": a,
            "drug_b": b,
            "severity": severity,
            "type": itype,
            "citation": citation,
            "desc": item.get("desc", "").strip() or f"Interaction between {a} and {b} per FDA labeling.",
        })
    return out


# ── 5. Emit JS array + splice into HTML ────────────────────────────────────────
def to_js_array(records) -> str:
    lines = ["const ALL_INTERACTIONS_RAW = ["]
    for r in records:
        lines.append(
            "  {"
            f'drug_a:{json.dumps(r["drug_a"])},  '
            f'drug_b:{json.dumps(r["drug_b"])},  '
            f'severity:{json.dumps(r["severity"])},  '
            f'type:{json.dumps(r["type"])},  '
            f'citation:{json.dumps(r["citation"])},  '
            f'desc:{json.dumps(r["desc"])}'
            "},"
        )
    lines.append("];")
    return "\n".join(lines)


def splice_html(html: str, js_array: str) -> str:
    pattern = re.compile(r"const ALL_INTERACTIONS_RAW\s*=\s*\[.*?\];", re.DOTALL)
    if not pattern.search(html):
        sys.exit("Could not find ALL_INTERACTIONS_RAW block to replace in HTML.")
    return pattern.sub(js_array, html, count=1)


def main():
    if not GEMINI_API_KEY:
        sys.exit("GEMINI_API_KEY is not set in .env. Add it, then re-run.")

    with open(HTML_PATH, encoding="utf-8") as f:
        html = f.read()

    roster = parse_roster(html)
    print(f"Roster: {len(roster)} drugs -> {', '.join(roster)}")

    print("Fetching real FDA interaction text from openFDA...")
    fda_blurbs: dict[str, tuple[str, str]] = {}
    for brand, ingredient in roster.items():
        text, url = fetch_fda_interactions(ingredient)
        fda_blurbs[brand] = (text, url)
        status = f"{len(text)} chars" if text else "no label data"
        print(f"  {brand:12s} ({ingredient}): {status}")
        time.sleep(0.3)  # be polite to the free API

    have = sum(1 for t, _ in fda_blurbs.values() if t)
    print(f"openFDA returned interaction text for {have}/{len(roster)} drugs.")

    print(f"Structuring with Gemini ({GEMINI_MODEL})...")
    client = genai.Client(api_key=GEMINI_API_KEY)
    raw = structure_with_gemini(client, roster, fda_blurbs)
    records = finalize(raw, roster, fda_blurbs)
    print(f"Gemini produced {len(raw)} raw -> {len(records)} valid, deduped interactions.")

    with open(JSON_OUT, "w", encoding="utf-8") as f:
        json.dump(records, f, indent=2)
    print(f"Wrote {JSON_OUT}")

    new_html = splice_html(html, to_js_array(records))
    with open(HTML_PATH, "w", encoding="utf-8") as f:
        f.write(new_html)
    print(f"Updated {HTML_PATH} with {len(records)} FDA-sourced interactions.")


if __name__ == "__main__":
    main()
