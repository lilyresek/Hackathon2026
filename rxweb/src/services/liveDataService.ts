// Orchestrates the free APIs into the app's Drug[] / DrugInteraction[] shape.
//   RxNorm  -> normalize each drug name + therapeutic class
//   openFDA -> label description, side effects, boxed warnings (per drug node)
//   Gemini  -> clinically significant pairwise interaction edges
//
// Nodes come from real government data; edges come from the LLM, because no
// free government pairwise-interaction API currently exists.

import {
  Drug,
  DrugInteraction,
  calculateHubMetrics,
} from '../data/drugData';
import { resolveDrug, getDrugClass } from './rxnorm';
import { fetchLabel } from './openfda';
import { generateInteractions } from './gemini';
import { hasGeminiKey } from './env';

export interface LiveFetchProgress {
  step: string;
  current: number;
  total: number;
}

export interface LiveFetchResult {
  drugs: Drug[];
  interactions: DrugInteraction[];
  notes: string[];
}

// Map an RxNorm/ATC class string onto the app's fixed classKey palette.
function inferClassKey(classLabel: string, category: string): Drug['classKey'] {
  const hay = `${classLabel} ${category}`.toLowerCase();
  if (/anti-?inflammat|nsaid/.test(hay)) return 'nsaid';
  if (/anticoagul|antithrombo|antiplatelet|heparin|warfarin/.test(hay)) return 'anticoagulant';
  if (/cardi|antihyperten|vascul|statin|lipid|blood pressure/.test(hay)) return 'cardiovascular';
  if (/antidepress|ssri|psychi|serotonin/.test(hay)) return 'psychiatric';
  if (/stimulant|amphetamine|adhd/.test(hay)) return 'stimulant';
  if (/sedat|hypnotic|benzodiazep|anxiolytic|sleep/.test(hay)) return 'sedative';
  if (/analgesic|opioid|pain/.test(hay)) return 'analgesic';
  if (/antibiotic|antimicrob|antifung|antibacter/.test(hay)) return 'antimicrobial';
  if (/diabet|thyroid|metabol|endocrin|insulin/.test(hay)) return 'metabolic';
  if (/herbal|supplement|vitamin|botanical/.test(hay)) return 'supplement';
  return 'analgesic';
}

function toId(name: string): string {
  return name.trim().toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-+|-+$/g, '');
}

/**
 * Build a live dataset from a list of free-text drug names.
 * Degrades gracefully: a drug missing from openFDA still becomes a node;
 * if Gemini has no key, nodes are returned with zero edges.
 */
export async function fetchLiveDataset(
  drugNames: string[],
  onProgress?: (p: LiveFetchProgress) => void
): Promise<LiveFetchResult> {
  const notes: string[] = [];
  const names = Array.from(
    new Set(drugNames.map((n) => n.trim()).filter((n) => n.length > 0))
  );

  if (names.length === 0) {
    throw new Error('Enter at least one drug name.');
  }

  const drugs: Drug[] = [];
  const total = names.length;

  for (let i = 0; i < names.length; i++) {
    const name = names[i];
    onProgress?.({ step: `Resolving ${name}`, current: i + 1, total });

    // 1. RxNorm normalization (non-fatal if it misses).
    let normalizedName = name;
    let classLabel = '';
    try {
      const rx = await resolveDrug(name);
      if (rx) {
        normalizedName = rx.name;
        classLabel = await getDrugClass(rx.rxcui);
      } else {
        notes.push(`RxNorm had no match for "${name}" — using the name as entered.`);
      }
    } catch {
      notes.push(`RxNorm lookup failed for "${name}" — continuing.`);
    }

    // 2. openFDA label enrichment (non-fatal if it misses).
    let label = null;
    try {
      label = await fetchLabel(name);
      if (!label) notes.push(`No FDA label found for "${name}" — node added with basic info.`);
    } catch {
      notes.push(`openFDA lookup failed for "${name}" — node added with basic info.`);
    }

    const category = classLabel || 'Medication';
    const brandName = name.charAt(0).toUpperCase() + name.slice(1);

    drugs.push({
      id: toId(name),
      brandName,
      genericName: normalizedName,
      category,
      classKey: inferClassKey(classLabel, category),
      description: label?.description || `Live record for ${brandName}. No FDA description available.`,
      commonSideEffects: label?.sideEffects?.length ? label.sideEffects : ['Refer to the product label'],
      patientAdvice: label?.patientAdvice || 'Follow the label and consult your pharmacist.',
      fdaBoxedWarning: !!label?.boxedWarning,
      boxedWarningSummary: label?.boxedWarning,
    });
  }

  // 3. Gemini interaction edges.
  let interactions: DrugInteraction[] = [];
  if (hasGeminiKey()) {
    onProgress?.({ step: 'Analyzing interactions with Gemini', current: total, total });
    try {
      interactions = await generateInteractions(
        drugs.map((d) => ({ id: d.id, label: d.genericName || d.brandName }))
      );
      notes.push(`Gemini identified ${interactions.length} interaction${interactions.length === 1 ? '' : 's'}.`);
    } catch (err: any) {
      notes.push(`Gemini interaction step failed: ${err.message}. Nodes loaded without edges.`);
    }
  } else {
    notes.push('No Gemini key set — drugs loaded without interaction edges. Add VITE_GEMINI_API_KEY to .env.local to enable.');
  }

  return {
    drugs: calculateHubMetrics(drugs, interactions),
    interactions,
    notes,
  };
}
