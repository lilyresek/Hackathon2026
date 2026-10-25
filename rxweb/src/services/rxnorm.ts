// RxNorm / RxClass — U.S. National Library of Medicine.
// Free, public, no API key required.
// Docs: https://lhncbc.nlm.nih.gov/RxNav/APIs/

const RXNORM_BASE = 'https://rxnav.nlm.nih.gov/REST';

export interface RxNormDrug {
  rxcui: string;
  name: string; // normalized concept name
  query: string; // what the user typed
}

/**
 * Resolve a free-text drug name to its best-matching RxNorm concept.
 * Returns null if nothing matches.
 */
export async function resolveDrug(name: string): Promise<RxNormDrug | null> {
  const q = name.trim();
  if (!q) return null;

  // approximateTerm tolerates brand/generic/misspelled input.
  const url = `${RXNORM_BASE}/approximateTerm.json?term=${encodeURIComponent(q)}&maxEntries=1`;
  const res = await fetch(url);
  if (!res.ok) throw new Error(`RxNorm lookup failed (${res.status}) for "${q}"`);

  const data = await res.json();
  const candidate = data?.approximateGroup?.candidate?.[0];
  if (!candidate?.rxcui) return null;

  // Fetch the canonical concept name for a clean label.
  let conceptName = q;
  try {
    const propRes = await fetch(`${RXNORM_BASE}/rxcui/${candidate.rxcui}/property.json?propName=RxNorm%20Name`);
    if (propRes.ok) {
      const propData = await propRes.json();
      conceptName = propData?.propConceptGroup?.propConcept?.[0]?.propValue ?? q;
    }
  } catch {
    // Non-fatal — fall back to the user's input.
  }

  return { rxcui: String(candidate.rxcui), name: conceptName, query: q };
}

/**
 * Get the therapeutic/ATC class label for a drug, used to color-code the graph.
 * Falls back to an empty string when unavailable.
 */
export async function getDrugClass(rxcui: string): Promise<string> {
  try {
    const url = `${RXNORM_BASE}/rxclass/class/byRxcui.json?rxcui=${encodeURIComponent(rxcui)}&relaSource=ATC`;
    const res = await fetch(url);
    if (!res.ok) return '';
    const data = await res.json();
    const info = data?.rxclassDrugInfoList?.rxclassDrugInfo?.[0];
    return info?.rxclassMinConceptItem?.className ?? '';
  } catch {
    return '';
  }
}
