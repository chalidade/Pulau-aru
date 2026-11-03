// Island state: read from data/island.json (served by GitHub Pages), written back through the GitHub Contents API.
export const REPO = { owner: 'chalidade', repo: 'Pulau-aru', branch: 'main', path: 'data/island.json' };

export const DEFAULT_STATE = {
  v: 1, islandName: 'Pulau Tanpa Nama', followers: 0, residents: [], buildings: [],
  episodes: [], letters: [], clues: [], clueTotal: 10,
};

export const store = {
  get(k) { try { return localStorage.getItem(k); } catch (e) { return null; } },
  set(k, v) { try { localStorage.setItem(k, v); } catch (e) { } },
  del(k) { try { localStorage.removeItem(k); } catch (e) { } },
};

export function normalize(d) {
  const s = Object.assign(JSON.parse(JSON.stringify(DEFAULT_STATE)), d || {});
  for (const k of ['residents', 'buildings', 'episodes', 'letters', 'clues']) if (!Array.isArray(s[k])) s[k] = [];
  s.followers = Math.max(0, s.followers | 0);
  s.expand = Math.max(0, Math.min(3, s.expand | 0));
  for (const b of s.buildings) if (b.type === 'piramida' && !b.big) { b.x -= 5; b.y -= 5; b.big = true; }
  return s;
}

export async function loadState() {
  try {
    const r = await fetch(REPO.path + '?t=' + Date.now(), { cache: 'no-store' });
    if (!r.ok) throw new Error(r.status);
    return normalize(await r.json());
  } catch (e) {
    console.warn('island.json tidak bisa dimuat, memakai data awal', e);
    return normalize(null);
  }
}

const b64 = s => btoa(unescape(encodeURIComponent(s)));
export const tokenKey = 'pulau-aru-gh-token';

export async function publishState(state, message, base) {
  const token = store.get(tokenKey);
  if (!token) throw Object.assign(new Error('no_token'), { code: 'no_token' });
  const api = `https://api.github.com/repos/${REPO.owner}/${REPO.repo}/contents/${REPO.path}`;
  const headers = { Authorization: 'Bearer ' + token, Accept: 'application/vnd.github+json', 'X-GitHub-Api-Version': '2022-11-28' };
  let sha;
  const cur = await fetch(api + '?ref=' + REPO.branch + '&t=' + Date.now(), { headers, cache: 'no-store' });
  if (cur.status === 401) throw Object.assign(new Error('bad_token'), { code: 'bad_token' });
  if (cur.ok) {
    const j = await cur.json(); sha = j.sha;
    // the TikTok sync owns the follower count: keep the newest synced value instead of the draft's
    try {
      const remote = JSON.parse(decodeURIComponent(escape(atob((j.content || '').replace(/\n/g, '')))));
      // residents added remotely since this draft was loaded are kept; ones removed in the draft stay removed
      if (base && Array.isArray(remote.residents)) {
        const k = r => String(r.n).toLowerCase(), inBase = new Set((base.residents || []).map(k)), inDraft = new Set(state.residents.map(k));
        for (const r of remote.residents) if (!inBase.has(k(r)) && !inDraft.has(k(r))) { state.residents.push(r); inDraft.add(k(r)); }
      }
      if (remote.tiktok && (!state.tiktok || remote.tiktok.updatedAt >= state.tiktok.updatedAt)) { state.tiktok = remote.tiktok; state.followers = Math.max(remote.tiktok.followers, state.residents.length); }
    } catch (e) { }
  }
  const body = { message, content: b64(JSON.stringify(state, null, 1) + '\n'), branch: REPO.branch };
  if (sha) body.sha = sha;
  const r = await fetch(api, { method: 'PUT', headers, body: JSON.stringify(body) });
  if (r.status === 401) throw Object.assign(new Error('bad_token'), { code: 'bad_token' });
  if (r.status === 403 || r.status === 404) throw Object.assign(new Error('forbidden'), { code: 'forbidden' });
  if (r.status === 409) throw Object.assign(new Error('conflict'), { code: 'conflict' });
  if (!r.ok) throw Object.assign(new Error('failed ' + r.status), { code: 'failed' });
  return true;
}

export function downloadState(state) {
  const blob = new Blob([JSON.stringify(state, null, 1) + '\n'], { type: 'application/json' });
  const a = document.createElement('a'); a.href = URL.createObjectURL(blob); a.download = 'island.json';
  document.body.appendChild(a); a.click(); setTimeout(() => { URL.revokeObjectURL(a.href); a.remove(); }, 500);
}
