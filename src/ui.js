// HUD, panels and the creator's admin tools.
import { BT } from './models.js';
import { ROLE_LINES } from './activities.js';
import { store, tokenKey, publishState, downloadState, normalize, REPO } from './data.js';

export const $ = id => document.getElementById(id);
export function h(tag, attrs, ...kids) {
  const e = document.createElement(tag);
  if (attrs) for (const k in attrs) { const v = attrs[k]; if (v == null || v === false) continue; if (k === 'class') e.className = v; else if (k.startsWith('on')) e.addEventListener(k.slice(2), v); else e.setAttribute(k, v === true ? '' : v); }
  for (const k of kids.flat()) { if (k == null || k === false) continue; e.append(k instanceof Node ? k : document.createTextNode(String(k))); }
  return e;
}
export const fmt = n => Number(n).toLocaleString('id-ID');
export const clean = s => String(s || '').trim().replace(/^@+/, '').replace(/\s+/g, '').slice(0, 40);
const today = () => new Date().toLocaleDateString('id-ID', { day: 'numeric', month: 'short', year: 'numeric', timeZone: 'Asia/Jakarta' });
const MS = [100, 1000, 10000];

let app;
export function initUI(a) {
  app = a;
  $('sheet-x').onclick = closeSheet;
  $('sheet').addEventListener('pointerdown', e => { if (e.target.id === 'sheet') closeSheet(); });
  $('dialog').addEventListener('click', closeDialog);
  $('b-journal').onclick = openJournal; $('b-letters').onclick = openLetters; $('b-names').onclick = openNames; $('b-map').onclick = openMap;
  $('b-admin').onclick = () => openAdmin();
  const menu = $('menu'), mb = $('b-menu');
  const setMenu = on => { menu.hidden = !on; mb.setAttribute('aria-expanded', String(on)); };
  mb.onclick = e => { e.stopPropagation(); setMenu(menu.hidden); };
  menu.addEventListener('click', e => { if (e.target.closest('.mi') && e.target.closest('.mi').id !== 'b-time') setMenu(false); });
  document.addEventListener('pointerdown', e => { if (!menu.hidden && !e.target.closest('#hud-r')) setMenu(false); });
  const pill = $('hud-pill'), more = $('hud-more');
  pill.onclick = () => { more.hidden = !more.hidden; pill.setAttribute('aria-expanded', String(!more.hidden)); };
  $('banner-x').onclick = () => { app.endPlace(); openAdmin('bangun'); };
}

// ---------- primitives ----------
let toastT;
export function toast(t) { const e = $('toast'); e.textContent = t; e.hidden = false; clearTimeout(toastT); toastT = setTimeout(() => e.hidden = true, 3000); }
export function dialog(name, text) { $('dlg-name').textContent = name; $('dlg-text').textContent = text; $('dialog').hidden = false; }
export function closeDialog() { $('dialog').hidden = true; }
export function sheet(title, ...body) { $('sheet-title').textContent = title; $('sheet-body').replaceChildren(...body); $('sheet').hidden = false; $('sheet-body').scrollTop = 0; }
export function closeSheet() { $('sheet').hidden = true; }
const fld = (label, el) => h('div', { class: 'field' }, h('label', { for: el.id }, label), el);

export function refreshHud() {
  const S = app.S;
  $('isl-name').textContent = S.islandName || 'Pulau Tanpa Nama';
  const ep = app.curEp();
  $('isl-sub').textContent = `Hari ke-${ep} · ${S.buildings.length} bangunan` + (S.tiktok ? ' · live dari TikTok' : '');
  $('pop-n').textContent = fmt(app.pop());
  const p = app.pop(), next = MS.find(m => p < m);
  if (next) { const prev = MS[MS.indexOf(next) - 1] || 0; $('ms-fill').style.width = Math.max(2, (p - prev) / (next - prev) * 100) + '%'; $('ms-txt').textContent = `Menuju ${fmt(next)} penduduk: ${next === 100 ? 'festival pertama' : next === 1000 ? 'kapal pertama datang' : 'pulau muncul di peta'}`; }
  else { $('ms-fill').style.width = '100%'; $('ms-txt').textContent = 'Pulau ini sudah tercatat di peta dunia'; }
  $('st-name').textContent = S.islandName; $('st-pop').textContent = fmt(p); $('st-bld').textContent = S.buildings.length; $('st-ep').textContent = ep;
  $('dirty-dot').hidden = !app.dirty;
  let bar = $('unpub');
  if (!bar) { bar = h('div', { id: 'unpub', hidden: true }, h('span', null, 'Perubahan belum terbit. Pengunjung belum melihatnya.'), h('button', { onclick: publishNow }, 'Terbitkan')); document.body.appendChild(bar); }
  bar.hidden = !app.dirty;
  $('letter-dot').hidden = !S.letters.length || (store.get('pulau-aru-seen-letters') | 0) >= S.letters.length;
  $('menu-dot').hidden = $('letter-dot').hidden && !app.dirty;
  $('pill-ep').textContent = 'Ep ' + ep;
  document.title = (S.islandName && S.islandName !== 'Pulau Tanpa Nama' ? S.islandName : 'Pulau Aru') + ' · ' + fmt(p) + ' penduduk';
}

// ---------- visitor panels ----------
export function openNames() {
  const S = app.S;
  const q = h('input', { class: 'inp', id: 'name-q', placeholder: 'Cari username…', autocomplete: 'off', autocapitalize: 'off' });
  const grid = h('div', { class: 'names' });
  const me = app.role.kind === 'warga' ? app.role.name.toLowerCase() : null;
  const draw = () => {
    const s = clean(q.value).toLowerCase();
    const list = S.residents.map((r, i) => ({ ...r, i: i + 1 })).filter(r => !s || r.n.toLowerCase().includes(s));
    grid.replaceChildren(...(list.length ? list.slice(0, 800).map(r => h('div', { class: 'nm' + (r.n.toLowerCase() === me ? ' me' : '') }, h('span', null, '@' + r.n), h('b', null, '#' + r.i)))
      : [h('div', { class: 'empty', style: 'grid-column:1/-1' }, S.residents.length ? 'Nama itu belum terukir di batu.' : 'Batu ini masih kosong. Nama warga pertama akan terukir di sini.')]));
  };
  q.addEventListener('input', draw); draw();
  sheet('Batu Nama', h('p', { class: 'lede' }, `${fmt(S.residents.length)} nama sudah diukir di batu dekat pantai. Ingin namamu dihapus? Kirim pesan ke kreator.`), q, grid);
}
export function openLight() {
  const S = app.S, L = app.lamps(), recent = S.residents.slice(-12).reverse();
  sheet('Mercusuar', h('div', { class: 'eyebrow' }, 'lampu menyala'), h('div', { class: 'big' }, fmt(L)),
    h('p', { class: 'lede', style: 'margin-top:8px' }, L ? 'Setiap warga baru, Aru menyalakan satu lampu kecil. Datanglah malam hari untuk melihat cahayanya.' : 'Mercusuar masih gelap. Lampu pertama menyala saat warga pertama datang.'),
    recent.length ? h('div', null, h('div', { class: 'eyebrow', style: 'margin-bottom:6px' }, 'Lampu terbaru dinyalakan untuk'), h('div', { class: 'chips' }, recent.map(r => h('span', { class: 'chip' }, '@' + r.n)))) : null);
}
export function openLetters() {
  const S = app.S; store.set('pulau-aru-seen-letters', String(S.letters.length)); refreshHud();
  const nextEp = (Math.floor(app.curEp() / 10) + 1) * 10;
  const L = [...S.letters].reverse();
  sheet('Surat Aru', h('p', { class: 'lede' }, `Setiap 10 episode Aru menulis surat untuk warganya. Surat berikutnya di episode ${nextEp}.`),
    L.length ? h('div', { class: 'feed' }, L.map(l => h('article', { class: 'letter' }, h('h3', null, l.title || 'Untuk warga pulau'), h('div', { style: 'font-size:14px;opacity:.7;margin:-4px 0 8px' }, `Episode ${l.ep} · ${l.date}`), l.body, h('div', { class: 'sign' }, 'Aru'))))
      : h('div', { class: 'empty' }, 'Kotak surat masih kosong. Surat pertama datang di episode 10.'));
}
export function openRules() {
  sheet('Papan Aturan Pulau', h('p', { class: 'lede' }, 'Aturan ini dipasang Aru sejak hari pertama supaya pulau tetap hangat.'),
    h('ol', { class: 'rules' },
      h('li', null, 'Setiap hari dua komentar dipilih acak untuk mengatur jalan cerita: membangun, berkegiatan, atau apa pun.'),
      h('li', null, 'Usulan yang menyakiti atau tidak pantas dilewati, lalu komentar diundi ulang.'),
      h('li', null, 'Undian benar-benar acak dan ditampilkan di video. Tidak ada hadiah.'),
      h('li', null, 'Hanya username yang disebut. Minta namamu dihapus kapan saja.'),
      h('li', null, 'Setiap follower adalah warga. Jumlah follower adalah jumlah penduduk.')));
}
export function openMystery() {
  const S = app.S, tot = Math.max(S.clueTotal | 0, S.clues.length), items = [];
  for (let i = 0; i < tot; i++) { const c = S.clues[i]; items.push(c ? h('div', { class: 'clue' }, h('div', { class: 'eyebrow', style: 'margin-bottom:4px' }, `Petunjuk ${i + 1} · episode ${c.ep}`), c.text) : h('div', { class: 'clue locked' }, `Petunjuk ${i + 1} belum terbuka`)); }
  sheet('Bagaimana Aru sampai ke pulau ini?', h('p', { class: 'lede' }, `Perahu rusak ini menyimpan cerita. ${S.clues.length} dari ${tot} petunjuk sudah terbuka.`), h('div', { class: 'feed' }, items));
}
export function openJournal() {
  const E = [...app.S.episodes].sort((a, b) => b.ep - a.ep);
  sheet('Catatan Pulau', h('p', { class: 'lede' }, 'Semua yang terjadi di pulau, dicatat Aru di dekat api unggun.'),
    E.length ? h('div', { class: 'feed' }, E.map(e => h('div', { class: 'entry' }, h('h3', null, `Episode ${e.ep}`), h('div', { class: 'meta' }, e.date), h('p', null, e.text),
      e.picks && e.picks.filter(Boolean).length ? h('div', { class: 'chips' }, e.picks.filter(Boolean).map(p => h('span', { class: 'chip' }, 'diusulkan @' + clean(p)))) : null)))
      : h('div', { class: 'empty' }, 'Belum ada catatan.'));
}
export function openMap() {
  const c = app.mapCanvas();
  const p = app.pop(), onMap = p >= 10000;
  sheet('Peta ' + (app.S.islandName || 'pulau'), h('p', { class: 'lede' }, onMap ? 'Pulau ini sudah muncul di peta dunia.' : `Pulau ini belum ada di peta dunia. Ia akan muncul saat penduduk mencapai 10.000 (sekarang ${fmt(p)}).`),
    h('div', { class: 'mapwrap' }, c),
    h('div', { class: 'legend' }, ...[['#ffffff', 'Kamu'], ['#ff8a72', 'Kemah Aru'], ['#ffc94a', 'Mercusuar'], ['#cfd3cc', 'Batu Nama'], ['#8a5a34', 'Perahu rusak'], ['#e3c49a', 'Bangunan warga']].map(([c, l]) => h('span', null, h('i', { style: 'background:' + c }), l))));
}
export function bldDialog(b) {
  const d = BT[b.type], parts = [];
  if (b.label) parts.push(`"${b.label}"`); if (b.by) parts.push(`Usulan @${clean(b.by)}`); if (b.ep != null && b.ep !== '' && !isNaN(b.ep)) parts.push(`dibangun di episode ${b.ep}`);
  dialog(d.n, parts.length ? parts.join(' · ') : 'Dibangun oleh warga pulau.');
}
export function talk(n) {
  const S = app.S;
  if (n.aru) {
    const e = [...S.episodes].sort((a, b) => b.ep - a.ep)[0];
    const lines = [`Selamat datang. Kita sekarang ${fmt(app.pop())} orang di pulau ini.`, e ? `Catatan terakhir, episode ${e.ep}: ${e.text}` : 'Aku masih menunggu warga pertama.', `Mercusuar sudah punya ${fmt(app.lamps())} lampu menyala.`, 'Kadang aku masih ingat ombak malam itu. Belum semuanya bisa kuceritakan.'];
    dialog('Aru', lines[(Math.random() * lines.length) | 0]); return;
  }
  if (n.role && ROLE_LINES[n.role] && (n.pres || n.vp || Math.random() < .65)) { const L = ROLE_LINES[n.role]; dialog(n.pres ? 'Presiden ' + n.name : n.vp ? 'Wakil Presiden ' + n.name : n.name, L[(Math.random() * L.length) | 0]); return; }
  const b = S.buildings[S.buildings.length - 1];
  const pool = [n.num ? `Aku warga ke-${n.num}. Namaku terukir di batu dekat pantai.` : 'Aku baru datang. Namaku belum sempat diukir.', b ? `Sudah lihat ${BT[b.type].n.toLowerCase()} yang baru dibangun? Aku suka.` : 'Pulau ini masih sepi. Kira-kira besok kita bangun apa ya?', `Kata Aru, mercusuar sudah punya ${fmt(app.lamps())} lampu.`, 'Kalau malam, coba lihat ke arah mercusuar.', S.clues.length > 1 ? 'Aku dengar di perahu rusak ada petunjuk baru.' : 'Menurutmu, bagaimana Aru bisa sampai ke sini?'];
  dialog(n.name, pool[(Math.random() * pool.length) | 0]);
}

// ---------- admin ----------
let adminTab = 'warga';
const adState = { sel: 'rumah', comments: '', skip: [], pre: null };
export function openAdmin(tab) {
  if (tab) adminTab = tab;
  const tabs = [['warga', 'Warga'], ['bangun', 'Bangun'], ['undian', 'Undian'], ['episode', 'Episode'], ['surat', 'Surat'], ['misteri', 'Misteri'], ['pulau', 'Pulau & GitHub']];
  const body = h('div');
  body.append(h('div', { class: 'tabs', role: 'tablist' }, tabs.map(([k, l]) => h('button', { class: 'tab', role: 'tab', 'aria-selected': String(k === adminTab), onclick: () => openAdmin(k) }, l))));
  body.append(({ warga: adWarga, bangun: adBangun, undian: adUndian, episode: adEpisode, surat: adSurat, misteri: adMisteri, pulau: adPulau })[adminTab]());
  const hasToken = !!store.get(tokenKey);
  body.append(h('div', { class: 'savebar' },
    h('span', null, app.dirty ? (hasToken ? 'Ada perubahan yang belum diterbitkan.' : 'Ada perubahan. Hubungkan GitHub di tab "Pulau & GitHub" untuk menerbitkan.') : 'Semua perubahan sudah terbit.'),
    app.dirty ? h('button', { class: 'btn ghost', onclick: () => { app.revert(); openAdmin(); } }, 'Batalkan') : null,
    h('button', { class: 'btn', disabled: !app.dirty, onclick: publishNow }, 'Terbitkan')));
  sheet('Kelola pulau', body);
}
async function publishNow() {
  const S = app.S;
  if (!store.get(tokenKey)) { openAdmin('pulau'); toast('Hubungkan GitHub dulu, atau unduh island.json.'); return; }
  try {
    toast('Menerbitkan ke GitHub…');
    await publishState(S, `Episode ${app.curEp()}: ${fmt(app.pop())} penduduk, ${S.buildings.length} bangunan`, app.base);
    app.markPublished(); toast('Terbit. Pengunjung melihatnya dalam 1–2 menit.'); if (!$('sheet').hidden) openAdmin();
  } catch (e) {
    const c = e.code;
    toast(c === 'bad_token' ? 'Token GitHub tidak valid atau kedaluwarsa.' : c === 'forbidden' ? 'Token tidak punya izin menulis ke repo ini.' : c === 'conflict' ? 'File berubah di GitHub. Coba terbitkan lagi.' : 'Gagal menerbitkan. Periksa koneksi lalu coba lagi.');
  }
}
function adWarga() {
  const S = app.S;
  const f = h('input', { id: 'ad-fol', type: 'number', min: '0', value: String(S.followers | 0) });
  const ta = h('textarea', { id: 'ad-names', placeholder: '@username1\n@username2\natau pisahkan dengan koma' });
  const list = h('div', { class: 'list' });
  const drawList = () => list.replaceChildren(...[...S.residents].map((r, i) => ({ r, i })).reverse().slice(0, 300).map(({ r, i }) => h('div', { class: 'li' }, h('span', null, `#${i + 1} @${r.n}`), h('button', { class: 'mini', onclick: () => { S.residents.splice(i, 1); app.markDirty(); drawList(); } }, 'Hapus'))));
  drawList();
  return h('div', null,
    h('p', { class: 'lede' }, 'Penduduk = jumlah follower + Aru. Setiap follower menyalakan satu lampu mercusuar.'),
    S.tiktok ? h('p', { class: 'lede' }, `Jumlah follower diisi otomatis dari TikTok (terakhir berubah ${new Date(S.tiktok.updatedAt).toLocaleString('id-ID', { timeZone: 'Asia/Jakarta' })}). Angka manual akan ditimpa sinkron berikutnya.`) : null,
    h('div', { class: 'row' }, fld('Jumlah follower', f), h('button', { class: 'btn ghost', onclick: () => { S.followers = Math.max(S.residents.length, parseInt(f.value) || 0); app.markDirty(); openAdmin(); } }, 'Pakai')),
    fld('Ukir nama warga baru di Batu Nama', ta),
    h('button', { class: 'btn ghost', onclick: () => { const have = new Set(S.residents.map(r => r.n.toLowerCase())); let added = 0; for (const raw of ta.value.split(/[\n,]+/)) { const n = clean(raw); if (!n || have.has(n.toLowerCase())) continue; have.add(n.toLowerCase()); S.residents.push({ n, ep: app.curEp() }); added++; } if (S.followers < S.residents.length) S.followers = S.residents.length; app.markDirty(); toast(added + ' nama diukir'); openAdmin(); } }, 'Ukir nama'),
    h('div', { class: 'eyebrow', style: 'margin-top:18px;margin-bottom:6px' }, 'Presiden pulau'),
    h('div', { class: 'row' }, fld('Username presiden', h('input', { id: 'ad-pres', value: (S.president && S.president.n) || '', placeholder: '@username' })),
      h('button', { class: 'btn ghost', onclick: () => { const v = clean($('ad-pres').value); S.president = v ? { n: v, ep: app.curEp() } : null; if (v && !S.residents.some(r => r.n.toLowerCase() === v.toLowerCase())) S.residents.push({ n: v, ep: app.curEp() }); app.markDirty(); toast(v ? 'Presiden dilantik: @' + v : 'Jabatan presiden dikosongkan'); openAdmin('warga'); } }, 'Lantik')),
    h('div', { class: 'row' }, fld('Username wakil presiden', h('input', { id: 'ad-vp', value: (S.vicePresident && S.vicePresident.n) || '', placeholder: '@username' })),
      h('button', { class: 'btn ghost', onclick: () => { const v = clean($('ad-vp').value); S.vicePresident = v ? { n: v, ep: app.curEp() } : null; if (v && !S.residents.some(r => r.n.toLowerCase() === v.toLowerCase())) S.residents.push({ n: v, ep: app.curEp() }); app.markDirty(); toast(v ? 'Wakil presiden dilantik: @' + v : 'Jabatan wakil presiden dikosongkan'); openAdmin('warga'); } }, 'Lantik')),
    h('div', { class: 'eyebrow', style: 'margin-top:18px;margin-bottom:6px' }, 'Impor dari data TikTok'),
    h('p', { class: 'lede' }, 'Pilih file user_data_tiktok.json (atau Follower.txt) dari unduhan data akun TikTok-mu. Nama follower baru langsung diukir, urut dari yang paling lama follow.'),
    h('input', { id: 'ad-ttfile', type: 'file', accept: '.json,.txt,application/json,text/plain', class: 'inp', onchange: e => importFollowers(e.target.files[0]) }),
    h('div', { class: 'eyebrow', style: 'margin-top:16px' }, `${S.residents.length} nama di batu`), list);
}
// Parse TikTok's "Download your data" export. The layout differs between versions, so search
// for any list of objects carrying a username under a key that mentions fans/followers.
export function parseFollowerExport(text) {
  const out = [];
  const t = text.trim();
  if (t.startsWith('{') || t.startsWith('[')) {
    const data = JSON.parse(t);
    // Apify tiktok-followers-scraper: [{ authorMeta: { name } }], newest follower first
    if (Array.isArray(data) && data[0]?.authorMeta) return data.map(it => ({ n: String(it.authorMeta?.name || ''), d: '' })).filter(it => it.n).reverse();
    const walk = (node, inFans) => {
      if (Array.isArray(node)) { for (const it of node) { if (inFans && it && typeof it === 'object') { const u = it.UserName || it.username || it.userName || it.Username || it.uniqueId; if (u) out.push({ n: String(u), d: it.Date || it.date || '' }); } walk(it, inFans); } return; }
      if (node && typeof node === 'object') for (const k in node) walk(node[k], inFans || /fans|follower/i.test(k) && !/following/i.test(k));
    };
    walk(data, false);
  } else {
    // TXT export: blocks of "Date: …" followed by "Username: …"
    let d = '';
    for (const line of t.split(/\r?\n/)) { const md = line.match(/^\s*Date:\s*(.+)$/i); if (md) d = md[1]; const mu = line.match(/^\s*User ?name:\s*(\S+)/i); if (mu) out.push({ n: mu[1], d }); }
  }
  out.sort((a, b) => String(a.d).localeCompare(String(b.d)));
  return out;
}
async function importFollowers(file) {
  if (!file) return;
  const S = app.S;
  let list;
  try { list = parseFollowerExport(await file.text()); } catch (e) { toast('File tidak bisa dibaca. Pilih user_data_tiktok.json dari folder hasil unduhan.'); return; }
  if (!list.length) { toast('Daftar follower tidak ditemukan di file ini.'); return; }
  const have = new Set(S.residents.map(r => r.n.toLowerCase())); let added = 0;
  for (const it of list) { const n = clean(it.n); if (!n || have.has(n.toLowerCase())) continue; have.add(n.toLowerCase()); S.residents.push({ n, ep: app.curEp() }); added++; }
  if (S.followers < S.residents.length) S.followers = S.residents.length;
  app.markDirty(); toast(`${list.length} follower ditemukan, ${added} nama baru diukir. Jangan lupa terbitkan.`); openAdmin('warga');
}
function adBangun() {
  const pal = h('div', { class: 'palette' });
  const label = h('input', { id: 'ad-blabel', placeholder: 'Tulisan di papan, atau nama bangunan', maxlength: '40' });
  const by = h('input', { id: 'ad-bby', placeholder: '@username pengusul' });
  const ep = h('input', { id: 'ad-bep', type: 'number', value: String(app.curEp()) });
  for (const k in BT) {
    const b = h('button', { class: 'pal', 'aria-pressed': String(k === adState.sel), onclick: () => { adState.sel = k; [...pal.children].forEach(x => x.setAttribute('aria-pressed', String(x === b))); } }, app.thumb(k), BT[k].n);
    pal.append(b);
  }
  return h('div', null, h('p', { class: 'lede' }, 'Pilih bangunan, lalu taruh di peta. Jalan dulu ke lokasi yang diinginkan. Tombol R memutar bangunan. Tahan Shift untuk menaruh beberapa sekaligus.'), pal,
    h('div', { class: 'row', style: 'margin-top:12px' }, fld('Pengusul', by), fld('Episode', ep)), fld('Keterangan (opsional)', label),
    h('div', { class: 'row' }, h('button', { class: 'btn', onclick: () => app.startPlace(adState.sel, { label: label.value.trim().slice(0, 40), by: clean(by.value), ep: parseInt(ep.value) }) }, 'Taruh di peta'), h('button', { class: 'btn ghost', onclick: app.startErase }, 'Hapus bangunan')));
}
const secureRand = n => { const a = new Uint32Array(1); crypto.getRandomValues(a); return a[0] % n; };
function adUndian() {
  const ta = h('textarea', { id: 'ad-comments', placeholder: 'Tempel komentar, satu per baris:\n@budi: bangun sumur\n@sari: Aru belajar memancing', style: 'min-height:120px' });
  ta.value = adState.comments; ta.addEventListener('input', () => adState.comments = ta.value);
  const stage = h('div', { class: 'draw-stage' }, h('div', { class: 'eyebrow' }, 'Siap mengundi'), h('div', { class: 'draw-name' }, '2 komentar'));
  const out = h('div');
  const parse = () => ta.value.split('\n').map(l => l.trim()).filter(Boolean).map(l => { const m = l.match(/^@?([\w.\-]+)\s*[:\-–]?\s*(.*)$/); return m ? { u: m[1], t: m[2] || '' } : { u: '', t: l }; });
  let picks = [], pool = [];
  const run = (slot) => {
    pool = parse(); if (pool.length < 2) { toast('Butuh minimal 2 komentar.'); return; }
    let ticks = 0;
    const iv = setInterval(() => { const r = pool[(Math.random() * pool.length) | 0]; stage.replaceChildren(h('div', { class: 'eyebrow' }, 'Mengundi dari ' + pool.length + ' komentar…'), h('div', { class: 'draw-name' }, '@' + r.u), h('div', { class: 'draw-text' }, r.t)); if (++ticks > 18) { clearInterval(iv); finish(slot); } }, 70);
  };
  const finish = (slot) => {
    const used = new Set(picks.filter((_, i) => i !== slot).map(p => p.idx)), skipped = new Set(adState.skip);
    const cand = pool.map((_, i) => i).filter(i => !used.has(i) && !skipped.has(i));
    if (!cand.length) { toast('Komentar habis.'); return; }
    if (slot == null) { const a = cand.splice(secureRand(cand.length), 1)[0]; picks = [{ idx: a, ...pool[a] }]; if (cand.length) { const b = cand[secureRand(cand.length)]; picks.push({ idx: b, ...pool[b] }); } }
    else { const k = cand[secureRand(cand.length)]; picks[slot] = { idx: k, ...pool[k] }; }
    const time = new Date().toLocaleTimeString('id-ID', { timeZone: 'Asia/Jakarta' });
    stage.replaceChildren(h('div', { class: 'eyebrow' }, `Terpilih dari ${pool.length} komentar · ${time} WIB`), ...picks.map((p, i) => h('div', { class: 'pick' }, h('div', { class: 'draw-name' }, '@' + p.u), h('div', { class: 'draw-text' }, p.t), h('div', { class: 'row', style: 'margin-top:8px' }, h('button', { class: 'mini', onclick: () => { adState.skip.push(p.idx); run(i); } }, 'Lewati (tidak pantas) & undi ulang')))));
    out.replaceChildren(h('button', { class: 'btn', style: 'margin-top:10px', onclick: () => { adState.pre = { picks: picks.map(p => p.u), text: picks.map(p => '@' + p.u + ': ' + p.t).join('\n') }; openAdmin('episode'); } }, 'Pakai untuk episode baru'));
  };
  return h('div', null, h('p', { class: 'lede' }, 'Undian memakai pengacak kriptografis peramban. Tampilkan layar ini di video supaya terlihat adil. Tidak ada hadiah.'), fld('Komentar', ta), h('button', { class: 'btn', onclick: () => { adState.skip = []; picks = []; run(null); } }, 'Undi 2 komentar'), stage, out);
}
function adEpisode() {
  const S = app.S, pre = adState.pre || {}; adState.pre = null;
  const ep = h('input', { id: 'ad-ep', type: 'number', value: String(app.curEp() + 1) });
  const p1 = h('input', { id: 'ad-p1', placeholder: '@pengusul 1', value: pre.picks ? pre.picks[0] || '' : '' });
  const p2 = h('input', { id: 'ad-p2', placeholder: '@pengusul 2', value: pre.picks ? pre.picks[1] || '' : '' });
  const tx = h('textarea', { id: 'ad-eptext', placeholder: 'Apa yang terjadi hari ini? Contoh: Warga membangun sumur pertama dan Aru belajar memancing.' }); tx.value = pre.text || '';
  const list = h('div', { class: 'list' }, [...S.episodes].map((e, i) => ({ e, i })).sort((a, b) => b.e.ep - a.e.ep).map(({ e, i }) => h('div', { class: 'li' }, h('span', null, `Ep ${e.ep}: ${e.text}`), h('button', { class: 'mini', onclick: () => { S.episodes.splice(i, 1); app.markDirty(); openAdmin(); } }, 'Hapus'))));
  return h('div', null, h('div', { class: 'row' }, fld('Episode', ep), fld('Usulan 1', p1), fld('Usulan 2', p2)), fld('Cerita hari ini', tx),
    h('button', { class: 'btn', onclick: () => { if (!tx.value.trim()) { toast('Tulis ceritanya dulu.'); return; } S.episodes.push({ ep: parseInt(ep.value) || 0, date: today(), picks: [clean(p1.value), clean(p2.value)].filter(Boolean), text: tx.value.trim().slice(0, 1200) }); app.markDirty(); toast('Episode dicatat'); openAdmin(); } }, 'Catat episode'),
    h('div', { class: 'eyebrow', style: 'margin-top:16px' }, 'Riwayat'), list);
}
function adSurat() {
  const S = app.S;
  const ep = h('input', { id: 'ad-lep', type: 'number', value: String(app.curEp()) });
  const ti = h('input', { id: 'ad-ltitle', placeholder: 'Untuk warga pulau' });
  const bd = h('textarea', { id: 'ad-lbody', style: 'min-height:180px;font-family:var(--f-hand);font-size:17px', placeholder: 'Warga yang baik,\n\nHari ini…' });
  const list = h('div', { class: 'list' }, S.letters.map((l, i) => h('div', { class: 'li' }, h('span', null, `Ep ${l.ep}: ${l.title || 'Untuk warga pulau'}`), h('button', { class: 'mini', onclick: () => { S.letters.splice(i, 1); app.markDirty(); openAdmin(); } }, 'Hapus'))));
  return h('div', null, h('p', { class: 'lede' }, `Surat ditulis setiap 10 episode. Episode sekarang: ${app.curEp()}.`), h('div', { class: 'row' }, fld('Episode', ep), fld('Judul', ti)), fld('Isi surat', bd),
    h('button', { class: 'btn', onclick: () => { if (!bd.value.trim()) return toast('Isi suratnya dulu.'); S.letters.push({ ep: parseInt(ep.value) || 0, date: today(), title: ti.value.trim().slice(0, 80), body: bd.value.trim().slice(0, 4000) }); app.markDirty(); toast('Surat masuk kotak surat'); openAdmin(); } }, 'Kirim ke kotak surat'), list);
}
function adMisteri() {
  const S = app.S;
  const tot = h('input', { id: 'ad-ctot', type: 'number', min: '1', value: String(S.clueTotal | 0) });
  const tx = h('textarea', { id: 'ad-clue', placeholder: 'Petunjuk baru tentang bagaimana Aru sampai ke pulau…' });
  const list = h('div', { class: 'list' }, S.clues.map((c, i) => h('div', { class: 'li' }, h('span', null, `${i + 1}. ${c.text}`), h('button', { class: 'mini', onclick: () => { S.clues.splice(i, 1); app.markDirty(); openAdmin(); } }, 'Hapus'))));
  return h('div', null, h('p', { class: 'lede' }, 'Buka misteri sedikit demi sedikit. Petunjuk bisa dibaca di perahu rusak.'),
    h('div', { class: 'row' }, fld('Total petunjuk direncanakan', tot), h('button', { class: 'btn ghost', onclick: () => { S.clueTotal = Math.max(1, parseInt(tot.value) || 1); app.markDirty(); openAdmin(); } }, 'Pakai')),
    fld('Petunjuk baru', tx), h('button', { class: 'btn', onclick: () => { if (!tx.value.trim()) return; S.clues.push({ text: tx.value.trim().slice(0, 600), ep: app.curEp() }); app.markDirty(); openAdmin(); } }, 'Buka petunjuk'), list);
}
function adPulau() {
  const S = app.S;
  const nm = h('input', { id: 'ad-iname', value: S.islandName, maxlength: '40' });
  const tok = h('input', { id: 'ad-token', type: 'password', placeholder: store.get(tokenKey) ? 'Token tersimpan di perangkat ini' : 'github_pat_…', autocomplete: 'off' });
  const io = h('textarea', { id: 'ad-json', placeholder: 'Tempel isi island.json untuk memulihkan' });
  const connected = !!store.get(tokenKey);
  return h('div', null,
    fld('Nama pulau (biar warga yang memilih)', nm), h('button', { class: 'btn ghost', onclick: () => { S.islandName = nm.value.trim() || 'Pulau Tanpa Nama'; app.markDirty(); openAdmin(); } }, 'Ganti nama'),
    h('div', { class: 'eyebrow', style: 'margin-top:18px;margin-bottom:6px' }, `Luas pulau: tahap ${S.expand | 0} dari 3`),
    h('p', { class: 'lede' }, 'Setiap tahap memunculkan daratan baru yang naik dari laut, tanpa pohon, siap untuk rumah warga.'),
    h('div', { class: 'row' }, h('button', { class: 'btn ghost', disabled: (S.expand | 0) >= 3, onclick: () => { S.expand = (S.expand | 0) + 1; closeSheet(); app.markDirty(); toast('Daratan baru muncul. Jangan lupa terbitkan.'); } }, 'Perluas pulau'),
      (S.expand | 0) > 0 ? h('button', { class: 'btn ghost', onclick: () => { S.expand = (S.expand | 0) - 1; app.markDirty(); openAdmin('pulau'); } }, 'Kembalikan satu tahap') : null),
    h('div', { class: 'eyebrow', style: 'margin-top:18px;margin-bottom:6px' }, connected ? 'GitHub terhubung' : 'Hubungkan GitHub'),
    fld('Token GitHub (disimpan hanya di peramban ini)', tok),
    h('div', { class: 'row' },
      h('button', { class: 'btn ghost', onclick: () => { const v = tok.value.trim(); if (!v) return toast('Tempel tokennya dulu.'); store.set(tokenKey, v); toast('GitHub terhubung'); openAdmin('pulau'); } }, 'Simpan token'),
      connected ? h('button', { class: 'btn ghost', onclick: () => { store.del(tokenKey); toast('Token dihapus dari perangkat ini'); openAdmin('pulau'); } }, 'Putuskan') : null),
    h('div', { class: 'tokenbox' }, 'Cara membuat token (sekali saja):', h('ol', null,
      h('li', null, 'Buka ', h('a', { href: 'https://github.com/settings/personal-access-tokens/new', target: '_blank', rel: 'noopener' }, 'github.com/settings/personal-access-tokens/new')),
      h('li', null, `Repository access: Only select repositories → ${REPO.repo}`),
      h('li', null, 'Permissions → Contents: Read and write'),
      h('li', null, 'Generate, salin, tempel di atas. Jangan bagikan token ini.'))),
    h('div', { class: 'eyebrow', style: 'margin-top:18px;margin-bottom:6px' }, 'Cadangan data'),
    h('div', { class: 'row' },
      h('button', { class: 'btn ghost', onclick: () => downloadState(S) }, 'Unduh island.json'),
      h('button', { class: 'btn ghost', onclick: () => { try { const d = JSON.parse(io.value); if (!d || !Array.isArray(d.buildings)) throw 0; app.replace(normalize(d)); toast('Data dipulihkan. Terbitkan untuk menyimpan.'); openAdmin(); } catch (e) { toast('JSON tidak valid.'); } } }, 'Pulihkan dari JSON')),
    fld('Data', io));
}
