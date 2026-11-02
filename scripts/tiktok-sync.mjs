// Fetch the creator's TikTok follower count and write it into data/island.json.
// Runs inside GitHub Actions. Tokens are masked and never printed.
//   MODE=connect  exchange a one-time authorization code for tokens
//   MODE=sync     refresh the access token and update the follower count
import fs from 'node:fs';
import path from 'node:path';

const env = process.env;
const KEY = env.TIKTOK_CLIENT_KEY, SECRET = env.TIKTOK_CLIENT_SECRET;
const REDIRECT = env.TIKTOK_REDIRECT_URI || 'https://pulau-aru.web.id/tiktok/callback.html';
const OUT = path.join(env.RUNNER_TEMP || '.', 'tiktok_refresh_token');
const DATA = 'data/island.json';

const mask = v => { if (v) console.log(`::add-mask::${v}`); };
const fail = msg => { console.log(`::error::${msg}`); process.exit(1); };
mask(SECRET); mask(env.TIKTOK_REFRESH_TOKEN); mask(env.CODE);
if (!KEY || !SECRET) fail('Secret TIKTOK_CLIENT_KEY atau TIKTOK_CLIENT_SECRET belum diisi di Settings → Secrets and variables → Actions.');

async function token(params) {
  const r = await fetch('https://open.tiktokapis.com/v2/oauth/token/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded', 'Cache-Control': 'no-cache' },
    body: new URLSearchParams({ client_key: KEY, client_secret: SECRET, ...params }),
  });
  const j = await r.json().catch(() => ({}));
  if (!j.access_token) fail(`TikTok menolak permintaan token (${j.error || r.status}): ${j.error_description || 'tanpa keterangan'}`);
  mask(j.access_token); mask(j.refresh_token);
  return j;
}

async function userInfo(accessToken) {
  const r = await fetch('https://open.tiktokapis.com/v2/user/info/?fields=display_name,follower_count', { headers: { Authorization: `Bearer ${accessToken}` } });
  const j = await r.json().catch(() => ({}));
  if (!r.ok || (j.error && j.error.code && j.error.code !== 'ok')) fail(`Gagal membaca profil TikTok (${(j.error && j.error.code) || r.status}). Pastikan scope user.info.stats disetujui.`);
  return j.data.user;
}

let tok;
if (env.MODE === 'connect') {
  const code = decodeURIComponent((env.CODE || '').trim());
  if (!code) fail('Kode otorisasi kosong.');
  tok = await token({ code, grant_type: 'authorization_code', redirect_uri: REDIRECT });
} else {
  if (!env.TIKTOK_REFRESH_TOKEN) fail('Belum terhubung ke TikTok. Jalankan workflow "TikTok: hubungkan akun" dulu.');
  tok = await token({ grant_type: 'refresh_token', refresh_token: env.TIKTOK_REFRESH_TOKEN });
}
// hand the (possibly rotated) refresh token to the next step through a temp file, never stdout
if (tok.refresh_token && tok.refresh_token !== env.TIKTOK_REFRESH_TOKEN) fs.writeFileSync(OUT, tok.refresh_token);

const user = await userInfo(tok.access_token);
const count = Number(user.follower_count) || 0;
console.log(`Akun: ${user.display_name} · follower: ${count}`);

const s = JSON.parse(fs.readFileSync(DATA, 'utf8'));
const residents = Array.isArray(s.residents) ? s.residents.length : 0;
const next = Math.max(count, residents);
const changed = s.followers !== next || !s.tiktok || s.tiktok.followers !== count;
if (changed) {
  s.followers = next;
  s.tiktok = { followers: count, updatedAt: new Date().toISOString() };
  fs.writeFileSync(DATA, JSON.stringify(s, null, 1) + '\n');
}
console.log(changed ? `Penduduk diperbarui → ${next}` : 'Tidak ada perubahan follower.');
if (env.GITHUB_OUTPUT) fs.appendFileSync(env.GITHUB_OUTPUT, `changed=${changed}\nfollowers=${count}\n`);
