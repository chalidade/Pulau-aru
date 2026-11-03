// Anonymous visit counters (no cookies, nothing personal): each page load bumps a few public counts on
// Abacus (abacus.jasoncameron.dev). "Visitor" = a browser counted once per day, remembered in localStorage.
const API = 'https://abacus.jasoncameron.dev', NS = 'pulau-aru-web-id';
const day = (d = new Date()) => new Date(d.getTime() + 7 * 3600e3).toISOString().slice(0, 10).replace(/-/g, ''); // WIB date
const ls = { get: k => { try { return localStorage.getItem(k); } catch { return null; } }, set: (k, v) => { try { localStorage.setItem(k, v); } catch {} } };
const hit = key => fetch(`${API}/hit/${NS}/${key}`, { mode: 'cors', keepalive: true }).catch(() => {});
const skip = () => navigator.webdriver || /^(localhost|127\.|192\.168\.)/.test(location.hostname) || ls.get('pulau-aru-nostat') === '1';

export const SOURCES = [['tiktok', 'TikTok'], ['instagram', 'Instagram'], ['whatsapp', 'WhatsApp'], ['search', 'Google'], ['other', 'Situs lain'], ['direct', 'Langsung']];
function source() {
  const ua = navigator.userAgent, ref = document.referrer, q = new URLSearchParams(location.search);
  const u = (q.get('utm_source') || q.get('src') || '').toLowerCase();
  if (u) return SOURCES.some(([k]) => k === u) ? u : 'other';
  if (/musical_ly|bytedance|tiktok|trill_/i.test(ua) || /tiktok\./i.test(ref)) return 'tiktok';
  if (/instagram/i.test(ua) || /instagram\./i.test(ref)) return 'instagram';
  if (/whatsapp/i.test(ua) || /whatsapp\./i.test(ref)) return 'whatsapp';
  if (/google\.|bing\.|duckduckgo\.|yahoo\./i.test(ref)) return 'search';
  if (ref && !ref.includes(location.hostname)) return 'other';
  return 'direct';
}

export function trackVisit() {
  if (skip()) return;
  const d = day();
  hit('visits'); hit('visits-' + d);
  if (!ls.get('pulau-aru-seen')) { ls.set('pulau-aru-seen', d); hit('visitors'); }
  if (ls.get('pulau-aru-day') !== d) { ls.set('pulau-aru-day', d); hit('daily-' + d); hit('src-' + source()); }
}
let played = false;
export function trackPlay() { if (played || skip()) return; played = true; hit('plays'); hit('plays-' + day()); }

// ---- reading, for the admin panel ----
const get = key => fetch(`${API}/get/${NS}/${key}`, { cache: 'no-store' }).then(r => r.ok ? r.json() : { value: 0 }).then(j => j.value | 0).catch(() => 0);
// the service allows 30 requests per 10 s per IP, so one load reads 9 totals + 7 days x 2 = 23 counters
export async function loadStats(days = 7) {
  const ds = []; for (let i = days - 1; i >= 0; i--) ds.push(day(new Date(Date.now() - i * 864e5)));
  const [visits, visitors, plays] = await Promise.all(['visits', 'visitors', 'plays'].map(get));
  const src = await Promise.all(SOURCES.map(([k]) => get('src-' + k)));
  const daily = [];
  for (const d of ds) { const [v, u] = await Promise.all([get('visits-' + d), get('daily-' + d)]); daily.push({ d, visits: v, visitors: u }); }
  return { visits, visitors, plays, src: SOURCES.map(([k, l], i) => ({ k, l, n: src[i] })), daily };
}
export const ignoreMe = on => ls.set('pulau-aru-nostat', on ? '1' : '0');
export const ignored = () => ls.get('pulau-aru-nostat') === '1';
