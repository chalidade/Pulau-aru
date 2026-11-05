// Kebun warga: every visitor buys seeds with island coins, plants them in the six beds of the Ladang Buah and harvests
// them later. Everything is saved on the visitor's own device (localStorage); nothing is sent anywhere. (ep 11, Chalid)
import * as THREE from 'three';
import { store } from './data.js';
import { mat, G, BT } from './models.js';
import { h, sheet, toast, fmt, $, panels } from './ui.js';

const KEY = 'pulau-aru-kebun';
// harga = seed price, jual = coins at harvest, menit = minutes to grow (real time, keeps growing while the page is closed)
export const SEEDS = {
  cabai: { n: 'Cabai', harga: 2, jual: 5, menit: 10, buah: '#d0483a', daun: '#4f9b45', tinggi: .35 },
  jagung: { n: 'Jagung', harga: 3, jual: 8, menit: 30, buah: '#f2c94c', daun: '#7cbf4a', tinggi: .6 },
  semangka: { n: 'Semangka', harga: 5, jual: 14, menit: 120, buah: '#2f7a32', daun: '#57b04a', tinggi: .2 },
  pisang: { n: 'Pisang', harga: 8, jual: 22, menit: 240, buah: '#ffd84a', daun: '#4fa040', tinggi: .75 },
  mangga: { n: 'Mangga', harga: 12, jual: 35, menit: 480, buah: '#f0a030', daun: '#3f8a3a', tinggi: .8 },
};
const START = 15, FISH = 2, DAILY = 5, NPLOT = 6;
const today = () => new Date().toISOString().slice(0, 10);

let st = load(), host = null, group = null, lastSig = '', readyNotified = new Set(), now = () => Date.now();
function load() {
  let s = null; try { s = JSON.parse(store.get(KEY) || 'null'); } catch (e) { }
  if (!s || typeof s !== 'object') s = { v: 1, koin: START, plots: [], panen: 0, day: '' };
  s.koin = Math.max(0, s.koin | 0); s.panen = s.panen | 0;
  s.plots = Array.from({ length: NPLOT }, (_, i) => { const p = (s.plots || [])[i]; return p && SEEDS[p.s] && +p.t ? { s: p.s, t: +p.t } : null; });
  return s;
}
const save = () => store.set(KEY, JSON.stringify(st));
const progress = p => p ? Math.min(1, (now() - p.t) / (SEEDS[p.s].menit * 60000)) : 0;
const left = p => Math.max(0, p.t + SEEDS[p.s].menit * 60000 - now());
const dur = ms => { const m = Math.ceil(ms / 60000); return m >= 60 ? `${Math.floor(m / 60)} jam${m % 60 ? ' ' + (m % 60) + ' mnt' : ''}` : `${m} mnt`; };
export const readyCount = () => st.plots.filter(p => p && progress(p) >= 1).length;

export function init() {
  panels.kebun = () => open();
  // daily delivery from the vice president's farm, and coins for every fish caught with the spear
  if (st.day !== today()) { const first = !st.day; st.day = today(); if (!first) { st.koin += DAILY; setTimeout(() => toast(`Kiriman harian dari Ladang Buah: +${DAILY} koin`), 1800); } save(); }
  window.addEventListener('pulau-fish', () => { st.koin += FISH; save(); toast(`+${FISH} koin untuk kebunmu`); });
  const n = readyCount(); if (n) setTimeout(() => toast(`${n} tanaman siap dipanen di Ladang Buah!`), 2600);
  st.plots.forEach((p, i) => { if (p && progress(p) >= 1) readyNotified.add(i); });
  dot();
}
function dot() { const d = $('kebun-dot'); if (d) d.hidden = !readyCount(); }

// ---------- 3D plants on the beds of the Ladang Buah ----------
export function attach(o) { host = o || null; if (group && group.parent) group.parent.remove(group); group = null; lastSig = ''; refresh3d(); }
function stage(p) { const k = progress(p); return k >= 1 ? 4 : k >= .6 ? 3 : k >= .25 ? 2 : 1; }
function plant(def, sg) {
  const g = new THREE.Group(), leaf = mat(def.daun), add = (geo, m, sx, sy, sz, x, y, z) => { const o = new THREE.Mesh(geo, typeof m === 'string' ? mat(m) : m); o.scale.set(sx, sy, sz); o.position.set(x, y, z); o.castShadow = true; g.add(o); return o; };
  if (sg === 1) { add(G.sph, '#7a5634', .14, .06, .14, 0, .02, 0); add(G.cone4, leaf, .03, .06, .03, 0, .08, 0); return g; }
  const k = sg === 2 ? .45 : 1, H = def.tinggi * k;
  add(G.cyl6, '#5f8a3a', .025 + .02 * k, H, .025 + .02 * k, 0, H / 2, 0);
  for (let i = 0; i < 4; i++) { const l = add(G.box, leaf, .28 * k + .06, .025, .1 * k + .04, Math.cos(i * 1.57 + .4) * .1 * k, H * (.45 + i * .14), Math.sin(i * 1.57 + .4) * .1 * k); l.rotation.y = -(i * 1.57 + .4); l.rotation.z = .3; }
  if (def === SEEDS.mangga || def === SEEDS.pisang) add(G.dode, leaf, .22 * k + .05, .18 * k + .04, .22 * k + .05, 0, H + .05, 0);
  if (sg === 4) {
    const fm = mat(def.buah);
    if (def === SEEDS.semangka) { add(G.sph, fm, .16, .13, .2, .12, .12, .05); add(G.sph, fm, .13, .11, .16, -.15, .1, -.08); }
    else if (def === SEEDS.jagung) for (const s of [-1, 1]) { const c = add(G.cyl6, fm, .045, .2, .045, s * .07, H * .6, 0); c.rotation.z = s * .4; }
    else if (def === SEEDS.pisang) for (let i = 0; i < 4; i++) add(G.cyl6, fm, .03, .14, .03, .1 + (i % 2) * .05, H * .7 - Math.floor(i / 2) * .08, .08);
    else for (let i = 0; i < 5; i++) add(G.sph, fm, .045, .06, .045, Math.cos(i * 1.3) * (.1 + H * .12), H * (.55 + (i % 3) * .15), Math.sin(i * 1.3) * (.1 + H * .12));
    const glow = new THREE.Mesh(G.sph, new THREE.MeshBasicMaterial({ color: '#fff3a0', transparent: true, opacity: .35, depthWrite: false })); glow.scale.setScalar(.06); glow.position.y = H + .35; glow.userData.spark = true; g.add(glow);
  }
  return g;
}
function refresh3d() {
  if (!host) return;
  const sig = st.plots.map(p => p ? p.s + stage(p) : '-').join(',');
  if (sig === lastSig && group) return; lastSig = sig;
  if (group) host.remove(group);
  group = new THREE.Group(); host.add(group);
  const plots = BT.ladang.plots;
  st.plots.forEach((p, i) => { if (!p) return; const def = SEEDS[p.s], sg = stage(p);
    for (const [dx, dz] of [[-.17, -.17], [.17, -.17], [-.17, .17], [.17, .17]]) { const o = plant(def, sg); o.position.set(plots[i][0] + dx, .2, plots[i][1] + dz); o.rotation.y = (i * 4 + dx * 9 + dz * 5); o.scale.setScalar(def.tinggi > .7 ? .8 : 1); group.add(o); } });
}
let acc = 0;
export function update(dt, T) {
  if (group) group.traverse(o => { if (o.userData.spark) { o.position.y += Math.sin(T * 3 + o.id) * .002; o.material.opacity = .25 + .2 * Math.sin(T * 4 + o.id); } });
  acc += dt; if (acc < 2) return; acc = 0;
  refresh3d();
  st.plots.forEach((p, i) => { if (p && progress(p) >= 1 && !readyNotified.has(i)) { readyNotified.add(i); toast(`${SEEDS[p.s].n} di petak ${i + 1} siap dipanen!`); } });
  dot();
}

// ---------- the Kebunku sheet ----------
export function open(pick = null) {
  const rows = st.plots.map((p, i) => {
    if (!p) return h('div', { class: 'li kebun' }, h('div', null, h('b', null, `Petak ${i + 1}`), h('div', { class: 'umkm-k' }, 'Kosong')), h('button', { class: 'mini', onclick: () => open(i) }, pick === i ? 'Pilih bibit ↓' : 'Tanam'));
    const def = SEEDS[p.s], k = progress(p);
    return h('div', { class: 'li kebun' },
      h('div', { style: 'flex:1;min-width:0' }, h('b', null, `Petak ${i + 1} · ${def.n}`), h('div', { class: 'umkm-k' }, k >= 1 ? `Siap panen · +${def.jual} koin` : `${dur(left(p))} lagi`),
        h('div', { class: 'ms-bar', style: 'margin-top:4px' }, h('i', { style: `width:${Math.round(k * 100)}%` }))),
      k >= 1 ? h('button', { class: 'mini ready', onclick: () => harvest(i) }, 'Panen') : null);
  });
  const shop = pick == null ? null : h('div', null,
    h('div', { class: 'eyebrow', style: 'margin:14px 0 8px' }, `Kios Bibit · tanam di petak ${pick + 1}`),
    h('div', { class: 'list' }, Object.entries(SEEDS).map(([id, d]) => h('div', { class: 'li kebun' },
      h('div', null, h('b', null, d.n), h('div', { class: 'umkm-k' }, `${d.harga} koin · tumbuh ${dur(d.menit * 60000)} · panen +${d.jual}`)),
      h('button', { class: 'mini', disabled: st.koin < d.harga, onclick: () => buy(pick, id) }, st.koin < d.harga ? 'Koin kurang' : 'Beli & tanam')))));
  sheet('Kebunku',
    h('div', { class: 'eyebrow' }, 'koin pulau'), h('div', { class: 'big' }, fmt(st.koin)),
    h('p', { class: 'lede', style: 'margin-top:8px' }, `Kebunmu ada di Ladang Buah, timur waterpark. Beli bibit, tanam, lalu kembali saat tanamannya matang; ia tetap tumbuh walau situs ditutup. Sudah panen ${fmt(st.panen)} kali.`),
    h('div', { class: 'list kebun-list' }, rows), ...(shop ? [shop] : []),
    h('p', { class: 'lede', style: 'margin-top:12px;font-size:13px' }, `Cari koin: panen, tangkap ikan dengan tombak (+${FISH}), dan kiriman harian Ladang Buah (+${DAILY}). Data kebun disimpan di perangkat ini saja, jadi kebun di HP dan di laptop berbeda.`));
}
function buy(i, id) {
  const d = SEEDS[id]; if (st.plots[i] || st.koin < d.harga) return;
  st.koin -= d.harga; st.plots[i] = { s: id, t: now() }; readyNotified.delete(i); save(); refresh3d();
  toast(`${d.n} ditanam di petak ${i + 1}. Panen dalam ${dur(d.menit * 60000)}.`); open();
}
function harvest(i) {
  const p = st.plots[i]; if (!p || progress(p) < 1) return; const d = SEEDS[p.s];
  st.plots[i] = null; st.koin += d.jual; st.panen++; readyNotified.delete(i); save(); refresh3d(); dot();
  toast(`Panen ${d.n}! +${d.jual} koin`); open();
}
// for the studio capture: show a prepared garden without touching anyone's real data
export const __demo = (plots, koin) => { st = { ...st, koin: koin ?? st.koin, plots: plots.map(p => p ? { s: p[0], t: now() - p[1] * SEEDS[p[0]].menit * 60000 } : null) }; lastSig = ''; refresh3d(); };
