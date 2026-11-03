// Trakteer → Pulau Aru: reads the latest supports (Rp5.000 = 1 request) with the creator's API key and
//  - totals every supporter into data/island.json → supporters [{n, count, total}] (Papan & Monumen Dermawan)
//  - queues new support messages as requests in studio/traktir.json, for the next episode (no draw)
// Needs the repo secret TRAKTEER_API_KEY (Trakteer → Pengaturan → Integrasi/API → API Key). Without it, does nothing.
import fs from 'node:fs';
const key = process.env.TRAKTEER_API_KEY;
const out = (k, v) => process.env.GITHUB_OUTPUT && fs.appendFileSync(process.env.GITHUB_OUTPUT, `${k}=${v}\n`);
if (!key) { console.log('::notice::TRAKTEER_API_KEY belum diisi, lewati.'); out('changed', 'false'); process.exit(0); }
const all = [];
for (let page = 1; page <= 20; page++) {
  const r = await fetch(`https://api.trakteer.id/v1/public/supports?limit=50&page=${page}`, { headers: { key, Accept: 'application/json', 'X-Requested-With': 'XMLHttpRequest' } });
  if (!r.ok) { console.log(`::error::Trakteer ${r.status}: ${(await r.text()).slice(0, 200)}`); process.exit(1); }
  const j = await r.json(), data = j?.result?.data || j?.data || [];
  all.push(...data);
  if (data.length < 50) break;
}
console.log(`[trakteer] ${all.length} dukungan`);
const clean = s => String(s || '').replace(/^@/, '').replace(/[^\p{L}\p{N}._\- ]/gu, '').trim().slice(0, 40) || 'Seseorang';
const sup = new Map();
for (const s of all) {
  const n = clean(s.supporter_name), q = Math.max(1, s.quantity | 0), amt = s.amount | 0;
  const cur = sup.get(n.toLowerCase()) || { n, count: 0, total: 0 };
  cur.count += q; cur.total += amt; sup.set(n.toLowerCase(), cur);
}
const island = JSON.parse(fs.readFileSync('data/island.json', 'utf8'));
const next = [...sup.values()].sort((a, b) => b.count - a.count || b.total - a.total);
const changedSup = JSON.stringify(island.supporters || []) !== JSON.stringify(next);
if (changedSup) { island.supporters = next; fs.writeFileSync('data/island.json', JSON.stringify(island, null, 1) + '\n'); }
// request queue
const qPath = 'studio/traktir.json';
const q = fs.existsSync(qPath) ? JSON.parse(fs.readFileSync(qPath, 'utf8')) : { requests: [] };
const seen = new Set(q.requests.map(r => r.id));
let added = 0;
for (const s of all) {
  const id = String(s.order_id || s.id || `${s.supporter_name}|${s.updated_at}|${s.amount}`);
  if (seen.has(id)) continue;
  q.requests.push({ id, n: clean(s.supporter_name), qty: Math.max(1, s.quantity | 0), message: String(s.support_message || '').slice(0, 400), at: s.updated_at || '', done: false });
  added++;
}
if (added) fs.writeFileSync(qPath, JSON.stringify(q, null, 1) + '\n');
console.log(`[trakteer] ${next.length} dermawan, ${added} request baru`);
out('changed', changedSup || added ? 'true' : 'false');
