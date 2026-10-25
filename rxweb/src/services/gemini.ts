// Gemini — generates pairwise drug interaction edges as structured JSON.
// Free tier; get a key at https://aistudio.google.com/apikey
//
// SECURITY NOTE: this runs client-side, so VITE_GEMINI_API_KEY ends up in the
// browser bundle. That's fine for a local hackathon demo. For production, move
// this call behind a small server route so the key never reaches the client.

import { GoogleGenAI, Type } from '@google/genai';
import { GEMINI_API_KEY, GEMINI_MODEL, hasGeminiKey } from './env';
import type { DrugInteraction } from '../data/drugData';

export interface GeminiInteractionRaw {
  drug1: string; // must match an id we passed in
  drug2: string;
  severity: 'severe' | 'moderate' | 'minor';
  mechanismType: 'synergistic' | 'metabolic' | 'clearance';
  title: string;
  description: string;
  clinicalRationale: string;
  patientActionableAdvice: string;
}

const interactionSchema = {
  type: Type.OBJECT,
  properties: {
    interactions: {
      type: Type.ARRAY,
      items: {
        type: Type.OBJECT,
        properties: {
          drug1: { type: Type.STRING },
          drug2: { type: Type.STRING },
          severity: { type: Type.STRING, enum: ['severe', 'moderate', 'minor'] },
          mechanismType: { type: Type.STRING, enum: ['synergistic', 'metabolic', 'clearance'] },
          title: { type: Type.STRING },
          description: { type: Type.STRING },
          clinicalRationale: { type: Type.STRING },
          patientActionableAdvice: { type: Type.STRING },
        },
        required: [
          'drug1', 'drug2', 'severity', 'mechanismType',
          'title', 'description', 'clinicalRationale', 'patientActionableAdvice',
        ],
      },
    },
  },
  required: ['interactions'],
};

/**
 * Ask Gemini for clinically-grounded interactions among the given drugs.
 * `drugs` is a list of { id, label } so the model returns ids we can match.
 * Returns only pairs the model flagged as interacting.
 */
export async function generateInteractions(
  drugs: { id: string; label: string }[]
): Promise<DrugInteraction[]> {
  if (!hasGeminiKey()) {
    throw new Error('No Gemini API key set. Add VITE_GEMINI_API_KEY to .env.local.');
  }
  if (drugs.length < 2) return [];

  const ai = new GoogleGenAI({ apiKey: GEMINI_API_KEY });

  const roster = drugs.map((d) => `- id="${d.id}" name="${d.label}"`).join('\n');

  const prompt = [
    'You are a clinical pharmacology assistant. Analyze the drug list below and',
    'identify clinically significant pairwise drug-drug interactions.',
    '',
    'Rules:',
    '- Only report pairs that genuinely interact. Omit pairs with no meaningful interaction.',
    '- Use the exact "id" values provided for drug1 and drug2.',
    '- severity: severe | moderate | minor.',
    '- mechanismType: synergistic | metabolic | clearance.',
    '- Keep descriptions patient-friendly; put the pharmacology in clinicalRationale.',
    '- Base this on established clinical knowledge. This is for educational use, not medical advice.',
    '',
    'Drugs:',
    roster,
  ].join('\n');

  const response = await ai.models.generateContent({
    model: GEMINI_MODEL,
    contents: prompt,
    config: {
      responseMimeType: 'application/json',
      responseSchema: interactionSchema as unknown as object,
    },
  });

  const text = response.text;
  if (!text) return [];

  let parsed: { interactions?: GeminiInteractionRaw[] };
  try {
    parsed = JSON.parse(text);
  } catch {
    throw new Error('Gemini returned a response that was not valid JSON.');
  }

  const validIds = new Set(drugs.map((d) => d.id));
  const raw = parsed.interactions ?? [];

  return raw
    .filter((i) => validIds.has(i.drug1) && validIds.has(i.drug2) && i.drug1 !== i.drug2)
    .map((i, idx) => ({
      id: `gemini-${i.drug1}-${i.drug2}-${idx}`,
      drug1: i.drug1,
      drug2: i.drug2,
      severity: i.severity,
      mechanismType: i.mechanismType,
      title: i.title,
      description: i.description,
      clinicalRationale: i.clinicalRationale,
      patientActionableAdvice: i.patientActionableAdvice,
    }));
}
