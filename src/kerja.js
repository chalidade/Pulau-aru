// Interactions with buildings (ep 13, Chalid): sit at Warung Fahmi and order food, take a shift at the Kantor Pulau to earn
// coins. Coins are the same island coins as Kebunku (src/kebun.js), saved on the visitor's own device only.
// More interactions (slide, swing...) are meant to be added here one by one.
import * as THREE from 'three';
import { store } from './data.js';
import { BT, G, mat } from './models.js';
import { h, sheet, closeSheet, toast, fmt, panels } from './ui.js';
import * as kebun from './kebun.js';

export const MENU = {
  nasgor: { n: 'Nasi goreng', harga: 4, col: '#e0a84a', isi: 'Nasi goreng telur, kerupuknya bonus.' },
  mieayam: { n: 'Mie ayam', harga: 4, col: '#f2d48a', isi: 'Mie ayam pakai pangsit.' },
  gorengan: { n: 'Gorengan', harga: 1, col: '#d99a3e', isi: 'Bakwan dan tempe, masih panas.' },
  esteh: { n: 'Es teh manis', harga: 1, col: '#c0702a', drink: true, isi: 'Es teh manis, gelas besar.' },
  kopi: { n: 'Kopi tubruk', harga: 2, col: '#3a2618', drink: true, isi: 'Kopi tubruk, ampasnya jangan diminum.' },
};
export const JOBS = {
  surat: { n: 'Sortir surat warga', detik: 20, upah: 3, cd: 10 },
  kas: { n: 'Hitung kas Kantin Kejujuran', detik: 40, upah: 6, cd: 30 },
  arsip: { n: 'Rapikan arsip episode', detik: 60, upah: 9, cd: 60 },
};
const KEY = 'pulau-aru-kerja';
let app = null, seat = null, plate = null, job = null, eatT = 0;
const cd = (() => { try { return JSON.parse(store.get(KEY) || '{}') || {}; } catch (e) { return {}; } })();
const saveCd = () => store.set(KEY, JSON.stringify(cd));

export function init(a) { app = a; panels.warung = openWarung; panels.kantor = openKantor; }

// ---------- seats ----------
function seatsOf(o) {
  const d = o.userData.def, s = d.scale || 1; o.updateMatrixWorld(true);
  return d.seats.map(([x, y, z, f], i) => { const p = o.localToWorld(new THREE.Vector3(x * s, y * s, z * s)); return { i, o, x: p.x, y: p.y, z: p.z, ry: f + o.rotation.y, lx: x, lz: z, lf: f }; });
}
function nearestBuilding(type) { const P = app.player; let best = null, bd = Infinity; for (const o of app.objs()) if (o.userData.b.type === type) { const d = Math.hypot(o.position.x - P.x, o.position.z - P.z); if (d < bd) { bd = d; best = o; } } return best; }
function sitAt(o, pick) {
  const P = app.player, list = seatsOf(o).filter(s => !app.npcSeat || !app.npcSeat(s));
  const s = pick != null ? list[pick] : list.sort((a, b) => Math.hypot(a.x - P.x, a.z - P.z) - Math.hypot(b.x - P.x, b.z - P.z))[0];
  if (!s) return null;
  seat = s; P.sit = s; P.tx = null; P.x = s.x; P.z = s.z; return s;
}
// standing up puts the player on the nearest free ground outside the building (the seats are inside its solid
// footprint, so stepping straight forward used to leave the character stuck in place, unable to walk away)
function standSpot(s) {
  const free = app.free || (() => true);
  for (let d = .6; d <= 5; d += .3) for (let k = 0; k < 12; k++) {
    const a = s.ry + (k % 2 ? 1 : -1) * Math.ceil(k / 2) * Math.PI / 6, x = s.x + Math.sin(a) * d, z = s.z + Math.cos(a) * d;
    if (free(x, z) && free(x + .25, z) && free(x - .25, z) && free(x, z + .25) && free(x, z - .25)) return [x, z];
  }
  return [s.x + Math.sin(s.ry) * .55, s.z + Math.cos(s.ry) * .55];
}
export function stand() { const P = app && app.player; if (!P || !P.sit) return; const s = P.sit; P.sit = null; [P.x, P.z] = standSpot(s); P.tx = null; P.vy = 0; P.grounded = false; seat = null; clearPlate(); if (job) { toast('Shift dibatalkan. Upah dibayar kalau shift selesai.'); job = null; } }
export const sitting = () => !!(app && app.player.sit);

// a seated character: legs forward, arms do whatever the current activity is
export function pose(ch, T) {
  const P = app.player, s = P.sit, u = ch.userData, sc = ch.scale.y || 1;
  ch.position.set(s.x, s.y - .5 * sc + .03, s.z); ch.rotation.y = s.ry;
  u.legL.rotation.x = u.legR.rotation.x = -1.45; u.body.position.y = 0;
  if (job) { u.armR.rotation.x = -1.2 + Math.sin(T * 14) * .12; u.armL.rotation.x = -1.2 - Math.sin(T * 13) * .12; }   // typing
  else if (eatT > 0) { u.armR.rotation.x = -1.3 + Math.sin(T * 8) * .45; u.armL.rotation.x = -.8; }
  else { u.armR.rotation.x = u.armL.rotation.x = -.55; }
}

// ---------- food on the table ----------
function clearPlate() { if (plate && plate.parent) plate.parent.remove(plate); plate = null; eatT = 0; }
function serve(id) {
  clearPlate(); const m = MENU[id], s = seat, d = s.o.userData.def, sc = d.scale || 1, [ty, off] = d.table;
  const g = new THREE.Group(), add = (geo, c, sx, sy, sz, x, y, z) => { const o = new THREE.Mesh(geo, mat(c)); o.scale.set(sx, sy, sz); o.position.set(x, y, z); g.add(o); return o; };
  if (m.drink) { add(G.cyl8, '#e8e2d4', .045, .12, .045, 0, .06, 0); add(G.cyl8, m.col, .04, .01, .04, 0, .115, 0); }
  else { add(G.cyl8, '#f4eee0', .13, .02, .13, 0, .01, 0); add(G.sph, m.col, .09, .045, .09, 0, .04, 0); if (id === 'gorengan') for (let i = 0; i < 3; i++) add(G.ico, '#c98a3a', .04, .025, .06, -.05 + i * .05, .06, 0); }
  g.scale.setScalar(1 / sc);
  g.position.set(s.lx, ty, s.lz + Math.cos(s.lf) * off);
  (s.o.children[0] && d.scale ? s.o.children[0] : s.o).add(g); plate = g; eatT = 6;
}
export function update(dt) {
  if (eatT > 0) { eatT -= dt; if (eatT <= 0) { if (plate) plate.visible = false; toast('Kenyang! Terima kasih sudah makan di Warung Fahmi.'); } }
  if (job) { job.t += dt; const J = JOBS[job.id];
    if (Math.floor(job.t / 5) !== Math.floor((job.t - dt) / 5) && job.t < J.detik) toast(`${J.n}: ${Math.round(job.t / J.detik * 100)}%`);
    if (job.t >= J.detik) { kebun.addKoin(J.upah); cd[job.id] = Date.now(); saveCd(); toast(`Shift selesai! +${J.upah} koin (sekarang ${fmt(kebun.koin())})`); job = null; } }
}

// ---------- sheets ----------
function openWarung() {
  const o = nearestBuilding('warungfahmi'); if (!o) return;
  const rows = Object.entries(MENU).map(([id, m]) => h('div', { class: 'li kebun' },
    h('div', null, h('b', null, m.n), h('div', { class: 'umkm-k' }, `${m.harga} koin · ${m.isi}`)),
    h('button', { class: 'mini', disabled: kebun.koin() < m.harga, onclick: () => order(o, id) }, kebun.koin() < m.harga ? 'Koin kurang' : 'Pesan')));
  sheet('Warung Fahmi',
    h('div', { class: 'eyebrow' }, 'koin pulau'), h('div', { class: 'big' }, fmt(kebun.koin())),
    h('p', { class: 'lede', style: 'margin-top:8px' }, 'Duduk di bangku panjang, pesan, lalu makan di meja. Usulan @FAHMI di TikTok. Gerakkan karakter untuk berdiri lagi.'),
    h('div', { class: 'list kebun-list' }, rows),
    h('div', { style: 'display:flex;gap:8px;margin-top:12px' }, h('button', { class: 'mini', onclick: () => { if (!sitting()) sitAt(o); closeSheet(); toast('Kamu duduk di Warung Fahmi.'); } }, 'Duduk saja')),
    h('p', { class: 'lede', style: 'margin-top:12px;font-size:13px' }, 'Koin kurang? Kerja satu shift di Kantor Pulau, berkebun di Kebunku, atau tangkap ikan.'));
}
function order(o, id) {
  const m = MENU[id]; if (kebun.koin() < m.harga) return;
  if (!sitting() || seat.o !== o) { if (sitting()) stand(); if (!sitAt(o)) { toast('Bangkunya penuh.'); return; } }
  kebun.addKoin(-m.harga); serve(id); closeSheet(); toast(`${m.n} datang! -${m.harga} koin`);
}
function openKantor() {
  const o = nearestBuilding('kantor'); if (!o) return;
  const rows = Object.entries(JOBS).map(([id, J]) => { const wait = (cd[id] || 0) + J.cd * 60000 - Date.now();
    return h('div', { class: 'li kebun' },
      h('div', null, h('b', null, J.n), h('div', { class: 'umkm-k' }, `${J.detik} detik · upah +${J.upah} koin${wait > 0 ? ` · bisa lagi ${Math.ceil(wait / 60000)} mnt` : ''}`)),
      h('button', { class: 'mini', disabled: wait > 0 || !!job, onclick: () => startJob(o, id) }, job && job.id === id ? 'Sedang kerja' : wait > 0 ? 'Istirahat' : 'Mulai shift')); });
  sheet('Kantor Pulau',
    h('div', { class: 'eyebrow' }, 'koin pulau'), h('div', { class: 'big' }, fmt(kebun.koin())),
    h('p', { class: 'lede', style: 'margin-top:8px' }, 'Kerja jujur, dapat koin. Duduk di meja kerja sampai shift selesai; kalau berdiri, shift batal. Usulan wapres @EGA_91.'),
    h('div', { class: 'list kebun-list' }, rows),
    h('p', { class: 'lede', style: 'margin-top:12px;font-size:13px' }, 'Koinnya bisa dipakai makan di Warung Fahmi dan beli bibit di Kebunku. Disimpan di perangkat ini saja.'));
}
function startJob(o, id) {
  if (job) return; if (sitting()) stand(); if (!sitAt(o)) { toast('Meja kerjanya penuh.'); return; }
  job = { id, t: 0 }; closeSheet(); toast(`Mulai: ${JOBS[id].n}. Tetap duduk ${JOBS[id].detik} detik.`);
}
// for the studio capture
export const __sit = (type, i, food) => { const o = nearestBuilding(type) || app.objs().find(b => b.userData.b.type === type); if (sitting()) stand(); sitAt(o, i); if (food) serve(food); };
export const __job = id => { job = { id, t: 0 }; };
