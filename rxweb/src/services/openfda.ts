// openFDA — FDA drug label data. Free; API key optional (raises rate limit).
// Docs: https://open.fda.gov/apis/drug/label/

import { withOpenFdaKey } from './env';

const OPENFDA_LABEL = 'https://api.fda.gov/drug/label.json';

export interface OpenFdaLabel {
  description: string;
  sideEffects: string[];
  boxedWarning?: string;
  patientAdvice: string;
}

function firstText(arr: unknown): string {
  if (Array.isArray(arr) && typeof arr[0] === 'string') return arr[0].trim();
  return '';
}

// Turn a long label paragraph into a few short bullet-style side effects.
function extractSideEffects(raw: string): string[] {
  if (!raw) return [];
  const cleaned = raw.replace(/\s+/g, ' ').trim();
  // Split on common separators, keep short, meaningful fragments.
  const parts = cleaned
    .split(/[;,.]/)
    .map((p) => p.trim())
    .filter((p) => p.length > 3 && p.length < 60);
  return parts.slice(0, 6);
}

/**
 * Fetch FDA label info for a drug name. Returns null if the drug is not in
 * the openFDA label corpus (common for supplements). Never throws on 404.
 */
export async function fetchLabel(drugName: string): Promise<OpenFdaLabel | null> {
  const q = drugName.trim();
  if (!q) return null;

  // Space between the two field queries acts as an OR in openFDA's syntax.
  const query = `openfda.brand_name:"${q}" openfda.generic_name:"${q}"`;
  const url = withOpenFdaKey(`${OPENFDA_LABEL}?search=${encodeURIComponent(query)}&limit=1`);

  const res = await fetch(url);
  // openFDA returns 404 when no records match — treat as "no data", not an error.
  if (res.status === 404) return null;
  if (!res.ok) throw new Error(`openFDA label lookup failed (${res.status}) for "${q}"`);

  const data = await res.json();
  const result = data?.results?.[0];
  if (!result) return null;

  const boxed = firstText(result.boxed_warning);
  const description =
    firstText(result.description) ||
    firstText(result.indications_and_usage) ||
    firstText(result.purpose) ||
    'No structured FDA description available for this product.';

  const adverse = firstText(result.adverse_reactions) || firstText(result.warnings);
  const patientAdvice =
    firstText(result.patient_information) ||
    firstText(result.dosage_and_administration) ||
    'Follow the directions on the label and consult your pharmacist.';

  return {
    description: description.slice(0, 400),
    sideEffects: extractSideEffects(adverse),
    boxedWarning: boxed ? boxed.slice(0, 300) : undefined,
    patientAdvice: patientAdvice.slice(0, 300),
  };
}
