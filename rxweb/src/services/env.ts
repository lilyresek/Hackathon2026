// Centralized, typed access to Vite environment variables.
// Only VITE_-prefixed vars are exposed to the browser bundle.

const env = import.meta.env as Record<string, string | undefined>;

export const GEMINI_API_KEY = env.VITE_GEMINI_API_KEY ?? '';
export const GEMINI_MODEL = env.VITE_GEMINI_MODEL ?? 'gemini-2.5-flash';
export const OPENFDA_API_KEY = env.VITE_OPENFDA_API_KEY ?? '';

export const hasGeminiKey = (): boolean => GEMINI_API_KEY.trim().length > 0;

// openFDA works without a key; this just appends one when present to raise limits.
export function withOpenFdaKey(url: string): string {
  if (!OPENFDA_API_KEY.trim()) return url;
  const sep = url.includes('?') ? '&' : '?';
  return `${url}${sep}api_key=${encodeURIComponent(OPENFDA_API_KEY.trim())}`;
}
