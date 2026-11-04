// Low-poly models built from primitives. Everything shares cached materials.
import * as THREE from 'three';

const matCache = new Map();
export function mat(color, o = {}) {
  const key = color + JSON.stringify(o);
  if (!matCache.has(key)) matCache.set(key, new THREE.MeshStandardMaterial({ color, flatShading: true, roughness: .85, metalness: 0, ...o }));
  return matCache.get(key);
}
// window glass glows at night (emissiveIntensity driven by main loop)
export const windowMat = new THREE.MeshStandardMaterial({ color: '#2f4a5a', emissive: '#ffcc66', emissiveIntensity: 0, flatShading: true, roughness: .4 });
export const lampOnMat = new THREE.MeshStandardMaterial({ color: '#ffd56a', emissive: '#ffc34a', emissiveIntensity: 2.2, flatShading: true });
export const lampOffMat = mat('#6d6a62');
export function vicePresidentKit(ch) {
  const b = ch.userData.body;
  box(b, '#141414', .4, .17, .38, 0, 1.34, -.01);
  const s1 = box(b, '#e6b84a', .09, .66, .03, 0, .48, .16); s1.rotation.z = -.62; s1.position.y = .76;
}
export function presidentKit(ch) {
  const b = ch.userData.body;
  box(b, '#141414', .4, .17, .38, 0, 1.34, -.01);
  const s1 = box(b, '#c4473a', .1, .66, .03, 0, .48, .16); s1.rotation.z = .62; s1.position.y = .76;
  const s2 = box(b, '#f4eee0', .05, .66, .031, 0, .48, .163); s2.rotation.z = .62; s2.position.set(.03, .78, .163);
}
export const flameMat = new THREE.MeshBasicMaterial({ color: '#ffb347' });
export const flameMat2 = new THREE.MeshBasicMaterial({ color: '#ff6a2a' });
export const lanternMat = new THREE.MeshStandardMaterial({ color: '#ffcf70', emissive: '#ffb347', emissiveIntensity: 0.4, flatShading: true });

const G = {
  box: new THREE.BoxGeometry(1, 1, 1),
  cyl6: new THREE.CylinderGeometry(1, 1, 1, 6),
  cyl8: new THREE.CylinderGeometry(1, 1, 1, 8),
  cone4: new THREE.ConeGeometry(1, 1, 4),
  cone6: new THREE.ConeGeometry(1, 1, 6),
  ico: new THREE.IcosahedronGeometry(1, 0),
  dode: new THREE.DodecahedronGeometry(1, 0),
  sph: new THREE.SphereGeometry(1, 6, 4),
};
export { G };

function add(parent, geo, m, sx, sy, sz, x, y, z, ry = 0, shadow = true) {
  const o = new THREE.Mesh(geo, typeof m === 'string' ? mat(m) : m);
  o.scale.set(sx, sy, sz); o.position.set(x, y, z); o.rotation.y = ry;
  o.castShadow = shadow; o.receiveShadow = true;
  parent.add(o); return o;
}
export const box = (p, m, sx, sy, sz, x, y, z, ry) => add(p, G.box, m, sx, sy, sz, x, y + sy / 2, z, ry);
const cyl = (p, m, r, h, x, y, z, seg = 6) => add(p, seg === 8 ? G.cyl8 : G.cyl6, m, r, h, r, x, y + h / 2, z);
const roof4 = (p, m, w, h, d, x, y, z) => { const o = add(p, G.cone4, m, w * .72, h, d * .72, x, y + h / 2, z, Math.PI / 4); return o; };

export function textTexture(lines, opts = {}) {
  const w = opts.w || 512, h = opts.h || 256;
  const c = document.createElement('canvas'); c.width = w; c.height = h;
  const g = c.getContext('2d');
  g.fillStyle = opts.bg || '#a7794a'; g.fillRect(0, 0, w, h);
  if (opts.grain) for (let i = 0; i < 400; i++) { g.fillStyle = `rgba(0,0,0,${Math.random() * .08})`; g.fillRect(Math.random() * w, Math.random() * h, 2 + Math.random() * 30, 1); }
  g.fillStyle = opts.color || '#3a2412'; g.textAlign = 'center'; g.textBaseline = 'middle';
  const fs = opts.size || 40; g.font = `700 ${fs}px "Pixelify Sans", monospace`;
  lines.forEach((l, i) => g.fillText(l, w / 2, h / 2 + (i - (lines.length - 1) / 2) * fs * 1.25));
  const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 4;
  return t;
}

// ---------- characters ----------
const SKIN = ['#f1c9a5', '#d9a478', '#c68a5b', '#a76b3f', '#7d4d2c'], HAIR = ['#2b1d14', '#4a2f1d', '#7a4b26', '#c9a24b', '#1c1c24', '#8a8f99', '#a8442f'],
  SHIRT = ['#d0483a', '#3a7fc2', '#e6b84a', '#5fae6a', '#8e5bc2', '#e07a3a', '#2d9c9a', '#f0e6d0', '#c2508f', '#46546b'], PANTS = ['#3a4a6b', '#5a4632', '#2f3b33', '#6b6b72', '#7a3b3b'];
export function lookOf(name) {
  const s = [...name.toLowerCase()].reduce((a, c) => (a * 31 + c.charCodeAt(0)) | 0, 7);
  const r = k => ((s >>> (k * 3)) ^ (s >>> (k * 5 + 1))) >>> 0;
  return { skin: SKIN[r(1) % 5], hair: HAIR[r(2) % 7], shirt: SHIRT[r(3) % 10], pants: PANTS[r(4) % 5], style: r(5) % 3 };
}
export const ARU = { skin: '#c68a5b', hair: '#2b1d14', shirt: '#ece4d2', pants: '#3a5a7a', style: 1, scarf: '#e2733a' };

export function makeCharacter(lk) {
  const root = new THREE.Group();
  const body = new THREE.Group(); root.add(body);
  const hip = 0.5;
  const leg = (x) => { const g = new THREE.Group(); g.position.set(x, hip, 0); box(g, lk.pants, .16, .5, .18, 0, -.5, 0); box(g, '#3a2a20', .17, .08, .22, 0, -.5, .02); body.add(g); return g; };
  const legL = leg(-.11), legR = leg(.11);
  box(body, lk.shirt, .46, .52, .28, 0, hip, 0);
  if (lk.scarf) { box(body, lk.scarf, .5, .1, .32, 0, hip + .44, 0); box(body, lk.scarf, .1, .26, .06, .12, hip + .24, .16); }
  const arm = (x) => { const g = new THREE.Group(); g.position.set(x, hip + .48, 0); box(g, lk.shirt, .13, .2, .15, 0, -.2, 0); box(g, lk.skin, .11, .26, .12, 0, -.44, 0); body.add(g); return g; };
  const armL = arm(-.3), armR = arm(.3);
  const head = new THREE.Group(); head.position.y = hip + .54; body.add(head);
  box(head, lk.skin, .36, .36, .34, 0, 0, 0);
  box(head, lk.hair, .38, .12, .36, 0, .3, 0);
  box(head, lk.hair, .38, .26, .1, 0, .1, -.14);
  if (lk.style === 1) { box(head, lk.hair, .06, .22, .3, -.19, .1, -.02); box(head, lk.hair, .06, .22, .3, .19, .1, -.02); }
  if (lk.style === 2) box(head, lk.hair, .2, .1, .2, 0, .4, -.05);
  box(head, '#1d1410', .05, .06, .02, -.08, .17, .175); box(head, '#1d1410', .05, .06, .02, .08, .17, .175);
  root.userData = { legL, legR, armL, armR, body, phase: Math.random() * 6 };
  return root;
}
export function animateCharacter(ch, moving, dt) {
  const u = ch.userData;
  if (moving) u.phase += dt * 11; else u.phase *= 0.9;
  const s = moving ? Math.sin(u.phase) * .7 : Math.sin(u.phase) * .7 * 0.2;
  u.legL.rotation.x = s; u.legR.rotation.x = -s; u.armL.rotation.x = -s * .8; u.armR.rotation.x = s * .8;
  u.body.position.y = moving ? Math.abs(Math.cos(u.phase)) * .05 : 0;
}

// ---------- buildings ----------
// each builder returns a Group centred on its footprint, ground at y=0
function palm(g, x, z, s = 1) {
  const trunk = new THREE.Group(); trunk.position.set(x, 0, z); g.add(trunk);
  let px = 0, py = 0;
  for (let i = 0; i < 6; i++) { const seg = add(trunk, G.cyl6, i % 2 ? '#9b7444' : '#83603a', .11 * s, .5 * s, .11 * s, px, py + .25 * s, 0); seg.rotation.z = -.08 * i; px += .05 * i * s; py += .48 * s; }
  for (let k = 0; k < 7; k++) {
    const a = k / 7 * Math.PI * 2; const leaf = new THREE.Group(); leaf.position.set(px, py, 0); leaf.rotation.y = a; trunk.add(leaf);
    const l = add(leaf, G.box, k % 2 ? '#3f9a5a' : '#4fae62', .22 * s, .04, 1.3 * s, 0, 0, .6 * s); l.rotation.x = .45;
  }
  add(trunk, G.sph, '#6b4a2b', .14 * s, .14 * s, .14 * s, px, py - .08, .08);
}
export const BT = {
  rumah: { n: 'Rumah', w: 3, h: 3, land: true, scale: 1.55, build(g) { box(g, '#e3c49a', 1.6, 1.1, 1.4, 0, 0, 0); roof4(g, '#b8523c', 2.1, 1, 1.9, 0, 1.1, 0); box(g, '#5e3b22', .36, .66, .05, 0, 0, .71); box(g, windowMat, .3, .3, .05, -.5, .5, .71); box(g, windowMat, .3, .3, .05, .5, .5, .71); box(g, '#9a9b94', .22, .5, .22, .45, 1.3, -.3); } },
  tenda: { n: 'Tenda', w: 2, h: 2, land: true, build(g) { add(g, G.cone4, '#d9763f', 1, 1.4, 1, 0, .7, 0, Math.PI / 4); box(g, '#3a2a20', .3, .5, .05, 0, 0, .55); add(g, G.cyl6, '#5e3b22', .03, .3, .03, 0, 1.5, 0); } },
  kebun: { n: 'Kebun', w: 3, h: 2, land: true, walk: true, build(g) { box(g, '#7a5534', 2.8, .12, 1.8, 0, 0, 0); for (let r = 0; r < 4; r++) { box(g, '#5d3e24', 2.6, .06, .14, 0, .12, -.6 + r * .4); for (let c = 0; c < 7; c++) add(g, G.cone6, r % 2 ? '#62bd73' : '#e0a84a', .09, .28, .09, -1.1 + c * .36, .3, -.6 + r * .4); } } },
  sumur: { n: 'Sumur', w: 1, h: 1, land: true, build(g) { cyl(g, '#9a9b94', .38, .5, 0, 0, 0, 8); add(g, G.cyl8, '#2b6a85', .3, .02, .3, 0, .45, 0, 0, false); box(g, '#5e3b22', .06, 1.1, .06, -.34, .5, 0); box(g, '#5e3b22', .06, 1.1, .06, .34, .5, 0); roof4(g, '#b8523c', .95, .4, .7, 0, 1.55, 0); } },
  dermaga: { n: 'Dermaga', w: 1, h: 4, water: true, walk: true, build(g) { for (let i = 0; i < 12; i++) box(g, i % 2 ? '#b07a4a' : '#8a5a34', .9, .08, .3, 0, .22, -1.7 + i * .31); for (const z of [-1.8, 0, 1.8]) for (const x of [-.4, .4]) add(g, G.cyl6, '#5e3b22', .07, 1.8, .07, x, -.6, z); } },
  jembatan: { n: 'Jembatan', w: 4, h: 1, water: true, walk: true, build(g) { for (let i = 0; i < 12; i++) box(g, i % 2 ? '#b07a4a' : '#8a5a34', .3, .08, .9, -1.7 + i * .31, .22, 0); for (const x of [-1.8, 0, 1.8]) for (const z of [-.42, .42]) { add(g, G.cyl6, '#5e3b22', .06, 2.2, .06, x, -.6, z); } box(g, '#8a5a34', 3.9, .06, .06, 0, .7, -.42); box(g, '#8a5a34', 3.9, .06, .06, 0, .7, .42); } },
  api: { n: 'Api unggun', w: 1, h: 1, land: true, fire: true, build(g) { campfire(g); } },
  pasar: { n: 'Pasar', w: 3, h: 2, land: true, build(g) { for (const sx of [-.75, .75]) { box(g, '#b07a4a', 1.2, .6, .6, sx, 0, .2); for (const [px, pz] of [[-.55, -.4], [.55, -.4], [-.55, .45], [.55, .45]]) box(g, '#5e3b22', .06, 1.3, .06, sx + px, 0, pz); for (let i = 0; i < 6; i++) box(g, i % 2 ? '#f0e6d0' : '#d0483a', .2, .06, 1.1, sx - .5 + i * .2, 1.3, 0); const cols = ['#e6b84a', '#7bc06a', '#d56b3a']; for (let i = 0; i < 3; i++) add(g, G.sph, cols[i], .1, .1, .1, sx - .35 + i * .35, .7, .25); } } },
  sekolah: { n: 'Sekolah', w: 3, h: 2, land: true, build(g) { box(g, '#efe2c6', 2.6, 1.3, 1.5, 0, 0, 0); roof4(g, '#4e7a9a', 3.3, .9, 2, 0, 1.3, 0); box(g, '#4e7a9a', .4, .5, .4, 0, 2.1, 0); add(g, G.sph, '#e5c06a', .1, .1, .1, 0, 2.4, .21); box(g, '#5e3b22', .4, .8, .05, 0, 0, .76); for (const x of [-.9, -.5, .5, .9]) box(g, windowMat, .26, .3, .05, x, .6, .76); } },
  menara: { n: 'Menara pandang', w: 1, h: 1, land: true, build(g) { for (const [x, z] of [[-.35, -.35], [.35, -.35], [-.35, .35], [.35, .35]]) box(g, '#5e3b22', .08, 2.6, .08, x, 0, z); box(g, '#8a5a34', .95, .1, .95, 0, 2.5, 0); for (let i = 0; i < 4; i++) box(g, '#8a5a34', .8, .05, .05, 0, .6 + i * .5, .36); roof4(g, '#d9b45c', 1.3, .7, 1.3, 0, 3.1, 0); for (const [x, z] of [[-.4, -.4], [.4, -.4], [-.4, .4], [.4, .4]]) box(g, '#5e3b22', .05, .5, .05, x, 2.6, z); } },
  patung: { n: 'Patung', w: 1, h: 1, land: true, build(g) { box(g, '#9a9b94', .8, .5, .8, 0, 0, 0); box(g, '#c2c2b8', .3, .5, .2, 0, .5, 0); box(g, '#c2c2b8', .4, .45, .25, 0, .95, 0); box(g, '#c2c2b8', .3, .3, .28, 0, 1.4, 0); const a = box(g, '#c2c2b8', .1, .45, .1, .26, 1.1, 0); a.rotation.z = -2.6; a.position.y = 1.55; } },
  taman: { n: 'Taman bunga', w: 2, h: 2, land: true, walk: true, build(g) { box(g, '#5aa64c', 1.9, .06, 1.9, 0, 0, 0); const cols = ['#f06b8a', '#ffd25a', '#f4f1ea', '#b48cf0', '#ff9b52']; for (let i = 0; i < 26; i++) { const x = -.8 + ((i * 37) % 17) / 10, z = -.8 + ((i * 53) % 17) / 10; add(g, G.cyl6, '#3f8a42', .015, .25, .015, x, .18, z, 0, false); add(g, G.sph, cols[i % 5], .07, .06, .07, x, .32, z); } for (let i = 0; i < 8; i++) { box(g, '#e8dcc4', .05, .3, .05, -.95 + i * .27, 0, -.95); box(g, '#e8dcc4', .05, .3, .05, -.95 + i * .27, 0, .95); } } },
  kelapa: { n: 'Pohon kelapa', w: 1, h: 1, land: true, build(g) { palm(g, 0, 0, 1); } },
  lumbung: { n: 'Lumbung', w: 2, h: 2, land: true, build(g) { box(g, '#a8443a', 1.6, 1.3, 1.5, 0, 0, 0); const r = add(g, G.cone4, '#5b3b2a', 1.25, .9, 1.15, 0, 1.75, 0, Math.PI / 4); box(g, '#efe2c6', .6, .8, .05, 0, 0, .76); box(g, '#7c2f28', .5, .7, .06, 0, .05, .77); const x1 = box(g, '#efe2c6', .06, .9, .07, 0, 0, .79); x1.rotation.z = .6; x1.position.y = .4; const x2 = box(g, '#efe2c6', .06, .9, .07, 0, 0, .79); x2.rotation.z = -.6; x2.position.y = .4; } },
  perahu: { n: 'Perahu nelayan', w: 2, h: 1, water: true, deep: true, bob: true, build(g) { box(g, '#8a5a34', 1.6, .3, .6, 0, .05, 0); box(g, '#5e3b22', 1.2, .12, .4, 0, -.05, 0); const p = add(g, G.cone4, '#8a5a34', .3, .6, .42, .95, .2, 0, Math.PI / 4); p.rotation.z = -Math.PI / 2; box(g, '#5e3b22', .06, 1.6, .06, -.1, .3, 0); const sh = new THREE.Shape(); sh.moveTo(0, 0); sh.lineTo(0, 1.3); sh.lineTo(.9, .1); const sail = new THREE.Mesh(new THREE.ShapeGeometry(sh), mat('#f2ead8', { side: THREE.DoubleSide })); sail.position.set(-.05, .55, 0); sail.castShadow = true; g.add(sail); } },
  // 13x13 stepped pyramid, 13 tiers of 0.75 m: walkable on top, each tier needs a jump
  piramida: { n: 'Piramida', w: 13, h: 13, land: true, climb: { half: 6.5, inset: .5, step: .75, tiers: 13 }, build(g) {
    const c = ['#d9b77a', '#cfa96a', '#e2c38a', '#c99f60', '#dcb877', '#d4ae70'];
    for (let i = 0; i < 13; i++) { const w = 13 - i; const m = box(g, c[i % c.length], w, .75, w, 0, i * .75, 0); m.receiveShadow = true; box(g, '#b8904f', w + .02, .06, w + .02, 0, i * .75 + .69, 0).castShadow = false; }
    const cap = new THREE.Mesh(G.cone4, new THREE.MeshStandardMaterial({ color: '#f2d06a', emissive: '#c99a20', emissiveIntensity: .25, flatShading: true, metalness: .4, roughness: .4 }));
    cap.scale.set(.7, 1.1, .7); cap.rotation.y = Math.PI / 4; cap.position.y = 9.75 + .55; cap.castShadow = true; g.add(cap);
    box(g, '#3e3122', 1.2, 1.6, .1, 0, 0, 6.52); box(g, '#a8844a', 1.6, .2, .14, 0, 1.6, 6.53);
  } },
  raktombak: { n: 'Rak tombak', w: 1, h: 1, land: true, spear: true, build(g) { box(g, '#5e3b22', .08, 1.3, .08, -.38, 0, 0); box(g, '#5e3b22', .08, 1.3, .08, .38, 0, 0); box(g, '#8a5a34', .9, .07, .1, 0, .45, 0); box(g, '#8a5a34', .9, .07, .1, 0, 1.15, 0); for (let i = 0; i < 3; i++) { const sp = new THREE.Group(); sp.position.set(-.24 + i * .24, .05, .06); sp.rotation.z = .08 - i * .08; g.add(sp); spearMesh(sp); } } },
  // traditional market: two rows of three stalls under striped awnings, a gate with a sign, an aisle in between
  pasartrad: { n: 'Pasar tradisional', w: 6, h: 5, land: true, walk: true, market: true,
    spots: (() => { const sell = [], shop = []; for (const [row, z, f] of [[0, -1.55, 0], [1, 1.25, Math.PI]]) for (const x of [-1.95, 0, 1.95]) { sell.push([x, z + (row ? .55 : -.55), f]); shop.push([x + (Math.random() - .5) * .5, z + (row ? -.95 : .95), f + Math.PI]); } return { sell, shop }; })(),
    build(g) {
      box(g, '#a88a62', 5.9, .05, 4.9, 0, 0, 0);
      const AW = [['#d0483a', '#f4eee0'], ['#3f9a5a', '#f4eee0'], ['#e6a23a', '#f7d774'], ['#3a7fc2', '#f4eee0'], ['#c2508f', '#f4eee0'], ['#e07a3a', '#f7e6b0']];
      const GOODS = [['#ffd24a', '#ff9b52', '#e8463a'], ['#7f97ad', '#7f97ad', '#9fb4c4'], ['#6fbf4a', '#3f9a5a', '#e8463a'], ['#ffb347', '#c9a24b', '#8a5a34'], ['#f06b8a', '#b48cf0', '#ffd25a'], ['#e9dcc0', '#d0483a', '#6fbf4a']];
      let k = 0;
      for (const [row, zc] of [[0, -1.55], [1, 1.25]]) for (const x of [-1.95, 0, 1.95]) {
        const st = new THREE.Group(); st.position.set(x, 0, zc); if (row) st.rotation.y = Math.PI; g.add(st);
        box(st, '#8a5a34', 1.5, .7, .7, 0, 0, 0); box(st, '#6b4a2b', 1.55, .06, .75, 0, .7, 0);
        for (const [px, pz] of [[-.72, -.6], [.72, -.6], [-.72, .32], [.72, .32]]) box(st, '#5e3b22', .07, 1.75, .07, px, 0, pz);
        const [c1, c2] = AW[k % AW.length];
        for (let i = 0; i < 6; i++) { const b = box(st, i % 2 ? c2 : c1, .27, .05, 1.15, -.68 + i * .272, 1.72, -.12); b.rotation.x = .28; }
        box(st, c1, 1.62, .16, .04, 0, 1.6, .45);
        const gd = GOODS[k % GOODS.length];
        for (let i = 0; i < 7; i++) { const m = new THREE.Mesh(i % 3 === 1 && k % 6 === 1 ? G.ico : G.sph, mat(gd[i % 3])); m.scale.setScalar(i % 3 === 1 && k % 6 === 1 ? .1 : .085); m.scale.z *= k % 6 === 1 ? 2 : 1; m.position.set(-.55 + i * .18, .82, .12 + (i % 2) * .12); m.castShadow = true; st.add(m); }
        const bk = new THREE.Mesh(G.cyl8, mat('#b08850')); bk.scale.set(.2, .22, .2); bk.position.set(.55, .11, .55); bk.castShadow = true; st.add(bk);
        for (let i = 0; i < 3; i++) { const f = new THREE.Mesh(G.sph, mat(gd[i])); f.scale.setScalar(.07); f.position.set(.5 + (i - 1) * .08, .26, .55); st.add(f); }
        k++;
      }
      // gate with the market's name
      for (const x of [-2.75, 2.75]) box(g, '#6b4a2b', .16, 2.5, .16, x, 0, 2.35);
      box(g, '#6b4a2b', 5.8, .14, .18, 0, 2.45, 2.35);
      const sign = new THREE.Mesh(G.box, [mat('#8a5a34'), mat('#8a5a34'), mat('#8a5a34'), mat('#8a5a34'), new THREE.MeshStandardMaterial({ map: textTexture(['PASAR'], { size: 120, bg: '#c4473a', color: '#fff3d0' }), flatShading: true }), mat('#8a5a34')]);
      sign.scale.set(2.2, .55, .08); sign.position.set(0, 2.25, 2.38); sign.castShadow = true; g.add(sign);
      for (let i = 0; i < 9; i++) { const l = new THREE.Mesh(G.sph, lanternMat); l.scale.set(.1, .13, .1); l.position.set(-2.6 + i * .65, 2.3 - Math.sin(i / 8 * Math.PI) * .25, 2.35); g.add(l); }
    } },
  // speaking stage for the island's president
  mimbar: { n: 'Mimbar', w: 3, h: 3, land: true, stage: .55,
    spots: { pres: [0, -.25, 0, .55], vp: [.95, -.45, -.25, .55] },
    build(g) {
      box(g, '#8a5a34', 2.8, .55, 2.4, 0, 0, -.1); box(g, '#6b4a2b', 2.85, .06, 2.45, 0, .55, -.1);
      for (let i = 0; i < 3; i++) box(g, '#9a6a3e', 1.0, .18 * (i + 1), .3, 0, 0, 1.25 + (2 - i) * .3);
      box(g, '#c4473a', 2.8, .28, .04, 0, .26, 1.1); box(g, '#f4eee0', 2.8, .27, .04, 0, 0, 1.1);
      box(g, '#5e3b22', .6, 1.0, .35, 0, .55, .45); box(g, '#c4473a', .62, .14, .37, 0, 1.45, .45);
      box(g, '#6b4a2b', 2.8, 1.9, .1, 0, .55, -1.3);
      box(g, '#c4473a', 2.82, .5, .12, 0, 1.95, -1.28); box(g, '#f4eee0', 2.82, .5, .12, 0, 1.45, -1.28);
      box(g, '#cfd3cc', .05, 3.6, .05, 1.25, 0, -1.2);
      box(g, '#d0302a', .7, .22, .02, 1.6, 3.32, -1.2); box(g, '#f8f6f0', .7, .22, .02, 1.6, 3.1, -1.2);
    } },
  // the supporters' monument: a golden statue on a stepped plinth; the top three supporters on the steps,
  // everyone else carved on the wall behind (names come from live.supporters, set by main before building)
  monumen: { n: 'Monumen Dermawan', w: 4, h: 4, land: true, open: 'dermawan',
    build(g) {
      const sup = [...live.supporters].sort((a, b) => (b.count || 0) - (a.count || 0) || (b.total || 0) - (a.total || 0));
      box(g, '#d8d2c2', 3.9, .12, 3.9, 0, 0, 0);
      box(g, '#bfb7a3', 2.2, .35, 2.2, 0, .12, -.2); box(g, '#cfc8b4', 1.6, .35, 1.6, 0, .47, -.2); box(g, '#ddd6c4', 1.0, .5, 1.0, 0, .82, -.2);
      const gold = new THREE.MeshStandardMaterial({ color: '#e6b84a', metalness: .6, roughness: .35, emissive: '#7a5a10', emissiveIntensity: .25, flatShading: true });
      const st = new THREE.Group(); st.position.set(0, 1.32, -.2); g.add(st);
      const part = (sx, sy, sz, x, y, z, rz = 0) => { const m = new THREE.Mesh(G.box, gold); m.scale.set(sx, sy, sz); m.position.set(x, y + sy / 2, z); m.rotation.z = rz; m.castShadow = true; st.add(m); return m; };
      part(.16, .55, .16, -.1, 0, 0); part(.16, .55, .16, .1, 0, 0); part(.46, .6, .26, 0, .55, 0); part(.3, .3, .3, 0, 1.15, 0);
      part(.12, .5, .12, -.3, .6, 0, .2); const arm = part(.12, .55, .12, .3, 1.0, 0, -.15);
      const torch = new THREE.Mesh(G.cone6, mat('#ffb347')); torch.scale.set(.12, .3, .12); torch.position.set(.38, 1.75, 0); st.add(torch);
      const plaque = (lines, w, h, x, y, z, ry = 0, big = false) => {
        const c = document.createElement('canvas'); c.width = 512; c.height = Math.round(512 * h / w); const x2 = c.getContext('2d');
        x2.fillStyle = '#3b2f22'; x2.fillRect(0, 0, c.width, c.height); x2.strokeStyle = '#e6b84a'; x2.lineWidth = 10; x2.strokeRect(5, 5, c.width - 10, c.height - 10);
        x2.fillStyle = '#f2d27a'; x2.textAlign = 'center'; x2.textBaseline = 'middle';
        const fs = big ? 64 : Math.min(40, (c.height - 30) / (lines.length + .5)); x2.font = `700 ${fs}px "Pixelify Sans", monospace`;
        lines.forEach((t, i) => x2.fillText(t, c.width / 2, c.height / 2 + (i - (lines.length - 1) / 2) * fs * 1.2));
        const tex = new THREE.CanvasTexture(c); tex.colorSpace = THREE.SRGBColorSpace;
        const p = new THREE.Mesh(new THREE.PlaneGeometry(w, h), new THREE.MeshStandardMaterial({ map: tex, roughness: .8 })); p.position.set(x, y, z); p.rotation.y = ry; g.add(p); return p;
      };
      const nm = s => s ? '@' + (s.n.length > 14 ? s.n.slice(0, 13) + '…' : s.n) : '…';
      plaque(['DERMAWAN', 'PULAU ARU'], 1.0, .4, 0, .58, .31, 0);
      plaque(['#1', nm(sup[0])], .9, .28, 0, .97, .305, 0);
      plaque(['#2', nm(sup[1])], 1.0, .3, -.65, .28, .91, 0);
      plaque(['#3', nm(sup[2])], 1.0, .3, .65, .28, .91, 0);
      // name wall
      box(g, '#8c8472', 3.6, 1.7, .25, 0, .12, -1.7);
      const rest = sup.slice(3, 27).map(nm); const cols = [rest.slice(0, 12), rest.slice(12, 24)];
      plaque(['TERIMA KASIH'].concat(rest.length ? [] : ['traktir di teer.id/chalidade', 'namamu diukir di sini']), 3.3, .5, 0, 1.55, -1.56, 0);
      if (rest.length) cols.forEach((cl, k) => cl.length && plaque(cl, 1.6, 1.0, k ? .82 : -.82, .78, -1.56, 0));
      for (const [x, z] of [[-1.7, 1.6], [1.7, 1.6]]) { box(g, '#5e3b22', .06, 1.0, .06, x, .12, z); const l = new THREE.Mesh(G.sph, lanternMat); l.scale.set(.1, .13, .1); l.position.set(x, 1.2, z); g.add(l); }
    } },
  // a notice board listing the island's small businesses (UMKM); names from live.umkm
  papanumkm: { n: 'Papan UMKM', w: 2, h: 1, land: true, open: 'umkm',
    build(g) {
      const list = live.umkm.slice(-8).map(u => u.name.length > 22 ? u.name.slice(0, 21) + '…' : u.name);
      for (const x of [-.85, .85]) box(g, '#5e3b22', .08, 1.9, .08, x, 0, 0);
      box(g, '#c4473a', 2.0, .12, .4, 0, 1.9, 0);
      const c = document.createElement('canvas'); c.width = 512; c.height = 360; const x2 = c.getContext('2d');
      x2.fillStyle = '#f4ead2'; x2.fillRect(0, 0, 512, 360); x2.fillStyle = '#c4473a'; x2.fillRect(0, 0, 512, 62);
      x2.fillStyle = '#fff'; x2.textAlign = 'center'; x2.textBaseline = 'middle'; x2.font = '700 40px "Pixelify Sans", monospace'; x2.fillText('ETALASE UMKM', 256, 32);
      x2.fillStyle = '#3a2412'; x2.font = '700 26px "Pixelify Sans", monospace';
      (list.length ? list : ['Daftarkan usahamu!', 'cek menu Etalase UMKM', 'di pulau-aru.web.id']).forEach((t, i) => x2.fillText(t, 256, 92 + i * 34));
      const tex = new THREE.CanvasTexture(c); tex.colorSpace = THREE.SRGBColorSpace;
      const p = new THREE.Mesh(new THREE.PlaneGeometry(1.6, 1.12), new THREE.MeshStandardMaterial({ map: tex, roughness: .9, side: THREE.DoubleSide })); p.position.set(0, 1.2, .05); p.castShadow = true; g.add(p);
    } },
  // the president's decree (episode 6): a mosque with a green dome, a minaret and a small courtyard
  masjid: { n: 'Masjid', w: 7, h: 7, land: true, scale: 1.8,
    build(g) {
      const wall = '#f3eee2', trim = '#2f8a5a', dome = mat('#2e9a63'); dome.flatShading = false;
      box(g, '#cfc8b6', 3.9, .14, 3.9, 0, 0, 0);                                     // courtyard floor
      box(g, wall, 2.8, 1.7, 2.6, 0, .14, -.35);                                     // prayer hall
      box(g, trim, 2.9, .14, 2.7, 0, 1.84, -.35);
      for (const [x, z] of [[-1.38, .97], [1.38, .97]]) box(g, wall, .18, 1.7, .18, x, .14, z);
      box(g, wall, 1.1, 2.1, .25, 0, .14, .95);                                      // entrance portal
      const arch = new THREE.Mesh(new THREE.CircleGeometry(.36, 16, 0, Math.PI), mat('#3b2a1e')); arch.position.set(0, 1.05, 1.085); g.add(arch);
      box(g, '#3b2a1e', .72, .91, .02, 0, .14, 1.075);
      for (const x of [-.95, .95]) { box(g, windowMat, .32, .55, .04, x, .7, .96); const w = new THREE.Mesh(new THREE.CircleGeometry(.16, 12, 0, Math.PI), windowMat); w.position.set(x, 1.25, .985); g.add(w); }
      box(g, wall, .9, .45, .9, 0, 1.98, -.35);                                      // drum
      const dm = new THREE.Mesh(new THREE.SphereGeometry(.62, 16, 10, 0, Math.PI * 2, 0, Math.PI / 2), dome); dm.position.set(0, 2.42, -.35); dm.scale.y = 1.15; dm.castShadow = true; g.add(dm);
      const fin = (x, y, z, k = 1) => { add(g, G.cyl6, '#e5c06a', .025 * k, .3 * k, .025 * k, x, y + .15 * k, z); const c1 = new THREE.Mesh(new THREE.TorusGeometry(.09 * k, .025 * k, 6, 14, Math.PI * 1.4), mat('#e5c06a')); c1.position.set(x, y + .4 * k, z); c1.rotation.z = Math.PI * .8; g.add(c1); };
      fin(0, 3.12, -.35);
      for (const [x, z] of [[-1.15, -1.45], [1.15, -1.45]]) { const sm = new THREE.Mesh(new THREE.SphereGeometry(.26, 12, 8, 0, Math.PI * 2, 0, Math.PI / 2), dome); sm.position.set(x, 1.98, z + .55); g.add(sm); }
      // minaret
      const mx = 1.55, mz = -1.55;
      add(g, G.cyl8, wall, .26, 3.6, .26, mx, 1.94, mz);
      add(g, G.cyl8, trim, .36, .1, .36, mx, 2.6, mz); add(g, G.cyl8, trim, .34, .1, .34, mx, 3.5, mz);
      add(g, G.cyl8, wall, .2, .5, .2, mx, 4.0, mz);
      add(g, G.cone6, trim, .26, .6, .26, mx, 4.55, mz); fin(mx, 4.83, mz, .7);
      for (const [x, z] of [[-1.6, 1.7], [1.6, 1.7]]) { box(g, '#5e3b22', .06, .9, .06, x, .14, z); const l = new THREE.Mesh(G.sph, lanternMat); l.scale.set(.1, .13, .1); l.position.set(x, 1.1, z); g.add(l); }
      for (const [x, z] of [[-1.7, -1.5], [-1.7, 0], [1.7, .1]]) add(g, G.ico, '#4f9b45', .32, .34, .32, x, .45, z);
    } },
  // a small neighbourhood pharmacy: white walls, a green cross sign and a glass front
  apotik: { n: 'Apotik', w: 2, h: 2, land: true,
    build(g) {
      box(g, '#bfc4c0', 1.9, .12, 1.8, 0, 0, .05);
      box(g, '#f6f6f2', 1.7, 1.25, 1.3, 0, .12, -.15);
      box(g, '#2f9a5b', 1.8, .12, 1.4, 0, 1.37, -.15);
      box(g, '#2f9a5b', 1.75, .06, .5, 0, 1.12, .7);
      box(g, windowMat, 1.1, .75, .03, -.15, .2, .515); box(g, '#3d4a46', .05, .75, .04, .4, .2, .52);
      box(g, '#e8f4ec', .3, .8, .03, .62, .2, .515);
      const c = document.createElement('canvas'); c.width = 256; c.height = 96; const x = c.getContext('2d');
      x.fillStyle = '#ffffff'; x.fillRect(0, 0, 256, 96); x.fillStyle = '#2f9a5b';
      x.fillRect(22, 38, 50, 20); x.fillRect(37, 23, 20, 50);
      x.font = '700 44px "Pixelify Sans", sans-serif'; x.textBaseline = 'middle'; x.fillText('APOTIK', 86, 50);
      const tx = new THREE.CanvasTexture(c); tx.colorSpace = THREE.SRGBColorSpace;
      const sign = new THREE.Mesh(new THREE.PlaneGeometry(1.2, .45), new THREE.MeshStandardMaterial({ map: tx, roughness: .8 })); sign.position.set(0, 1.62, .56); g.add(sign);
      box(g, '#2f9a5b', 1.24, .5, .04, 0, 1.39, .53);
      const cross = new THREE.Group(); cross.position.set(.95, 1.25, .62); g.add(cross);
      const gm = new THREE.MeshStandardMaterial({ color: '#35c46e', emissive: '#1f8a4a', emissiveIntensity: .6 });
      for (const [w, h] of [[.36, .12], [.12, .36]]) { const m = new THREE.Mesh(G.box, gm); m.scale.set(w, h, .06); cross.add(m); }
    } },
  // a warung tegal: open front with a glass food display, wooden benches and a striped awning (ep 7, usulan @javaz53)
  warteg: { n: 'Warteg', w: 2, h: 2, land: true,
    build(g) {
      box(g, '#c9bfa8', 1.9, .1, 1.85, 0, 0, 0);
      box(g, '#7fb3a0', 1.75, 1.2, .12, 0, .1, -.75); box(g, '#7fb3a0', .12, 1.2, 1.2, -.82, .1, -.2); box(g, '#7fb3a0', .12, 1.2, 1.2, .82, .1, -.2);
      box(g, '#2f6f5a', 1.85, .1, 1.45, 0, 1.3, -.1);
      for (let i = 0; i < 7; i++) { const a = box(g, i % 2 ? '#f4eee0' : '#2f8a6a', .27, .05, .55, -.81 + i * .27, 1.22, .75); a.rotation.x = .35; }
      box(g, '#8a5a34', 1.3, .55, .45, 0, .1, -.3);                                   // counter
      box(g, '#dfeef0', 1.2, .3, .38, 0, .65, -.3).material = new THREE.MeshStandardMaterial({ color: '#cfe8ee', transparent: true, opacity: .55 });
      const food = ['#f2e6c8', '#e0a84a', '#c4473a', '#62bd73', '#8a5a34', '#ffd25a'];
      for (let i = 0; i < 6; i++) add(g, G.cyl8, food[i], .09, .06, .09, -.47 + i * .19, .7, -.3);
      for (const z of [.25, .6]) { box(g, '#8a5a34', 1.4, .06, .22, 0, .38, z); for (const x of [-.6, .6]) box(g, '#5e3b22', .06, .38, .06, x, 0, z); }
      const c = document.createElement('canvas'); c.width = 256; c.height = 80; const x = c.getContext('2d');
      x.fillStyle = '#f4eee0'; x.fillRect(0, 0, 256, 80); x.fillStyle = '#2f6f5a';
      x.font = '700 52px "Pixelify Sans", sans-serif'; x.textAlign = 'center'; x.textBaseline = 'middle'; x.fillText('WARTEG', 128, 42);
      const tx = new THREE.CanvasTexture(c); tx.colorSpace = THREE.SRGBColorSpace;
      const sign = new THREE.Mesh(new THREE.PlaneGeometry(1.1, .34), new THREE.MeshStandardMaterial({ map: tx, roughness: .8 })); sign.position.set(0, 1.62, .52); g.add(sign);
      box(g, '#2f6f5a', 1.16, .4, .04, 0, 1.42, .49);
    } },
  // a small island hospital: two storeys, white with a teal band, an "H" sign and an ambulance bay (ep 7, usulan @yan.dipanggil.nen3)
  rumahsakit: { n: 'Rumah sakit', w: 4, h: 3, land: true, scale: 1.25,
    build(g) {
      box(g, '#bfc4c0', 3.3, .1, 2.6, 0, 0, 0);
      box(g, '#f7f7f3', 3.0, 2.1, 1.7, 0, .1, -.35);
      box(g, '#3aa6a0', 3.06, .12, 1.76, 0, 1.05, -.35); box(g, '#3aa6a0', 3.1, .14, 1.8, 0, 2.2, -.35);
      for (const yy of [.45, 1.45]) for (const xx of [-1.15, -.65, .65, 1.15]) box(g, windowMat, .32, .38, .04, xx, yy, .51);
      box(g, '#f7f7f3', .9, 1.3, .5, 0, .1, .7); box(g, '#3aa6a0', 1.1, .1, .75, 0, 1.4, .72);
      box(g, windowMat, .6, .8, .03, 0, .1, .955);
      for (const xx of [-.48, .48]) box(g, '#d8dad6', .08, 1.3, .08, xx, .1, .9);
      const c = document.createElement('canvas'); c.width = 384; c.height = 96; const x = c.getContext('2d');
      x.fillStyle = '#ffffff'; x.fillRect(0, 0, 384, 96); x.fillStyle = '#1f7a76'; x.fillRect(14, 14, 68, 68);
      x.fillStyle = '#ffffff'; x.font = '700 60px "Pixelify Sans", sans-serif'; x.textAlign = 'center'; x.textBaseline = 'middle'; x.fillText('H', 48, 50);
      x.fillStyle = '#1f7a76'; x.font = '700 40px "Pixelify Sans", sans-serif'; x.fillText('RUMAH SAKIT', 236, 50);
      const tx = new THREE.CanvasTexture(c); tx.colorSpace = THREE.SRGBColorSpace;
      const sign = new THREE.Mesh(new THREE.PlaneGeometry(1.8, .45), new THREE.MeshStandardMaterial({ map: tx, roughness: .8 })); sign.position.set(0, 2.62, -.02); g.add(sign); box(g, '#1f7a76', 1.86, .52, .04, 0, 2.35, -.06); box(g, '#9a9b94', .05, .2, .05, -.7, 2.24, -.1); box(g, '#9a9b94', .05, .2, .05, .7, 2.24, -.1);
      const hm = new THREE.MeshStandardMaterial({ color: '#46d0c8', emissive: '#1f8a84', emissiveIntensity: .7 });
      const roofH = new THREE.Group(); roofH.position.set(.9, 2.36, -.7); g.add(roofH);
      for (const [w, h, xx] of [[.08, .5, -.16], [.08, .5, .16], [.4, .08, 0]]) { const m = new THREE.Mesh(G.box, hm); m.scale.set(w, .04, h); m.position.x = xx; roofH.add(m); }
      // ambulance (generic, unbranded)
      const amb = new THREE.Group(); amb.position.set(-1.05, .1, .75); amb.rotation.y = .15; g.add(amb);
      box(amb, '#f4f4f0', .42, .36, .78, 0, .08, 0); box(amb, '#f4f4f0', .42, .24, .26, 0, .08, .5); box(amb, windowMat, .38, .14, .04, 0, .26, .64);
      box(amb, '#3aa6a0', .43, .07, .79, 0, .25, 0); add(amb, G.box, lampOnMat, .1, .06, .08, 0, .47, .3);
      for (const [wx, wz] of [[-.2, -.25], [.2, -.25], [-.2, .45], [.2, .45]]) add(amb, G.cyl8, '#222222', .08, .06, .08, wx, .08, wz).rotation.z = Math.PI / 2;
    } },
  // the president's house: white walls, columns on a raised porch, a red roof and a flag pole (ep 7, permintaan presiden @Etet_443)
  rumahpresiden: { n: 'Rumah Presiden', w: 4, h: 3, land: true, scale: 1.35,
    build(g) {
      box(g, '#b8b2a2', 3.4, .22, 2.7, 0, 0, 0);
      box(g, '#f4efe2', 2.9, 1.3, 1.6, 0, .22, -.4);
      box(g, '#f4efe2', 3.0, .1, .7, 0, 1.52, .45);
      for (const xx of [-1.2, -.6, 0, .6, 1.2]) cyl(g, '#ffffff', .07, 1.3, xx, .22, .7);
      roof4(g, '#b8523c', 3.6, .9, 2.6, 0, 1.52, -.15);
      box(g, '#5e3b22', .42, .8, .05, 0, .22, .41); box(g, '#e5c06a', .05, .05, .03, .12, .6, .44);
      for (const xx of [-.95, -.5, .5, .95]) box(g, windowMat, .28, .4, .05, xx, .65, .41);
      for (let i = 0; i < 3; i++) box(g, '#cfc8b6', 1.0 - i * .1, .07, .18, 0, i * .07, 1.3 - i * .14);
      add(g, G.cyl6, '#cfcfc8', .03, 2.6, .03, 1.55, 1.3, 1.15);
      box(g, '#d0483a', .5, .16, .02, 1.8, 2.36, 1.15); box(g, '#f4eee0', .5, .16, .02, 1.8, 2.2, 1.15);
      for (const xx of [-1.55, 1.1]) add(g, G.ico, '#4f9b45', .28, .3, .28, xx, .55, 1.15);
    } },
  // a small waterpark: tiled deck, a blue pool, a tower with a spiral slide and a giant rubber duck (ep 8, usulan warga)
  // slide path in local metres (used by the episode camera too): centre (-1, -.2), r 1.25, angle pi..2.25pi, y 2.4..0.35
  waterpark: { n: 'Waterpark', w: 6, h: 4, land: true,
    slide: { cx: -1, cz: -.2, r: 1.25, a0: Math.PI, a1: Math.PI * 2.25, y0: 2.4, y1: .35 },
    build(g) {
      box(g, '#e9e2d0', 5.9, .12, 3.9, 0, 0, 0);
      for (let i = 0; i < 12; i++) box(g, i % 2 ? '#d9d0ba' : '#e9e2d0', .45, .005, 3.85, -2.7 + i * .49, .12, 0);
      box(g, '#2f7fa8', 3.1, .14, 2.6, 1.25, .04, .15);                                          // pool rim inner
      const wm = new THREE.MeshStandardMaterial({ color: '#46c2e6', emissive: '#1c7fa8', emissiveIntensity: .25, transparent: true, opacity: .88, roughness: .15, flatShading: true });
      box(g, wm, 2.9, .04, 2.4, 1.25, .14, .15).receiveShadow = true;
      for (const [w, d, x, z] of [[3.3, .12, 1.25, -1.1], [3.3, .12, 1.25, 1.4], [.12, 2.6, -.4, .15], [.12, 2.6, 2.9, .15]]) box(g, '#f7f7f3', w, .2, d, x, .12, z);
      // tower + ladder
      for (const [x, z] of [[-2.65, -.55], [-1.85, -.55], [-2.65, .15], [-1.85, .15]]) box(g, '#f2c94c', .1, 2.4, .1, x, .12, z);
      box(g, '#e8573f', 1.0, .1, .9, -2.25, 2.42, -.2);
      for (const x of [-2.72, -1.78]) box(g, '#f7f7f3', .05, .45, .9, x, 2.52, -.2);
      box(g, '#f7f7f3', 1.0, .45, .05, -2.25, 2.52, -.66);
      for (let i = 0; i < 8; i++) box(g, '#c9c2b0', .5, .05, .06, -2.25, .35 + i * .28, .45);
      for (const x of [-2.5, -2.0]) box(g, '#c9c2b0', .05, 2.4, .05, x, .12, .45);
      roof4(g, '#e8573f', 1.3, .5, 1.2, -2.25, 4.45, -.2); for (const [x, z] of [[-2.7, -.6], [-1.8, -.6], [-2.7, .2], [-1.8, .2]]) box(g, '#f2c94c', .05, 1.5, .05, x, 2.95, z);
      // spiral slide: short tilted pieces along the helix
      const S = BT.waterpark.slide, N = 26, sm = mat('#2fa36b'), sm2 = mat('#f2c94c');
      const at = t => { const a = S.a0 + (S.a1 - S.a0) * t; return [S.cx + Math.cos(a) * S.r, S.y0 + (S.y1 - S.y0) * t, S.cz + Math.sin(a) * S.r]; };
      for (let i = 0; i < N; i++) {
        const p = at(i / N), q = at((i + 1) / N), dx = q[0] - p[0], dy = q[1] - p[1], dz = q[2] - p[2], L = Math.hypot(dx, dy, dz);
        const seg = new THREE.Group(); seg.position.set((p[0] + q[0]) / 2, (p[1] + q[1]) / 2, (p[2] + q[2]) / 2); g.add(seg);
        seg.lookAt(seg.position.x + dx, seg.position.y + dy, seg.position.z + dz);
        const base = new THREE.Mesh(G.box, sm); base.scale.set(.5, .06, L + .03); base.castShadow = true; seg.add(base);
        for (const sx of [-.25, .25]) { const w = new THREE.Mesh(G.box, i % 2 ? sm : sm2); w.scale.set(.06, .2, L + .03); w.position.set(sx, .1, 0); seg.add(w); }
        if (i % 4 === 2 && p[1] > .6) { const post = new THREE.Mesh(G.cyl6, mat('#c9c2b0')); post.scale.set(.04, p[1], .04); post.position.y = -p[1] / 2; seg.add(post); }
      }
      // giant rubber duck
      const duck = new THREE.Group(); duck.position.set(1.95, .16, .45); duck.rotation.y = -.6; g.add(duck);
      add(duck, G.sph, '#ffd23f', .5, .36, .6, 0, .22, 0); add(duck, G.sph, '#ffd23f', .3, .3, .3, 0, .62, .28);
      add(duck, G.box, '#f08a24', .2, .07, .2, 0, .58, .58); for (const x of [-.12, .12]) add(duck, G.sph, '#1c1c24', .04, .05, .04, x, .7, .5);
      add(duck, G.cone4, '#ffd23f', .18, .28, .1, 0, .38, -.58).rotation.x = -1.1;
      // rings floating
      for (const [x, z, c] of [[.4, -.5, '#e8573f'], [2.4, -.6, '#f7f7f3'], [.8, 1.0, '#3a7fc2']]) { const r = new THREE.Mesh(new THREE.TorusGeometry(.22, .08, 6, 12), mat(c)); r.rotation.x = Math.PI / 2; r.position.set(x, .2, z); g.add(r); }
      // umbrellas and loungers on the front-left deck
      for (const [x, z, c] of [[-2.3, 1.35, '#e8573f'], [-1.1, 1.35, '#3a7fc2']]) {
        cyl(g, '#f7f7f3', .03, 1.3, x, .12, z); add(g, G.cone6, c, .6, .3, .6, x, 1.45, z);
        const l = box(g, '#f7f7f3', .35, .08, .75, x + .35, .2, z - .1); box(g, '#c9c2b0', .3, .08, .05, x + .35, .12, z - .4);
        box(g, '#f7f7f3', .35, .06, .3, x + .35, .3, z - .45).rotation.x = .6;
      }
      // sign on the back
      const c = document.createElement('canvas'); c.width = 512; c.height = 128; const x = c.getContext('2d');
      const gr = x.createLinearGradient(0, 0, 512, 0); gr.addColorStop(0, '#2fa6d8'); gr.addColorStop(1, '#2fa36b'); x.fillStyle = gr; x.fillRect(0, 0, 512, 128);
      x.fillStyle = '#ffffff'; x.font = '700 70px "Pixelify Sans", sans-serif'; x.textAlign = 'center'; x.textBaseline = 'middle'; x.fillText('WATERPARK', 256, 68);
      const tx = new THREE.CanvasTexture(c); tx.colorSpace = THREE.SRGBColorSpace;
      for (const xx of [.2, 2.4]) box(g, '#c9c2b0', .08, 2.0, .08, xx, .12, -1.75);
      const sign = new THREE.Mesh(new THREE.PlaneGeometry(2.4, .6), new THREE.MeshStandardMaterial({ map: tx, roughness: .8 })); sign.position.set(1.3, 2.0, -1.7); g.add(sign);
      box(g, '#1f6f8a', 2.5, .7, .05, 1.3, 1.65, -1.75);
    } },
  // a fish grill stall near the pier: brick grill with flames, fish on the grate, smoke, a bench (ep 8, usulan warga)
  bakarikan: { n: 'Pembakaran ikan', w: 2, h: 2, land: true, fire: true,
    build(g) {
      box(g, '#c9bfa8', 1.9, .08, 1.85, 0, 0, 0);
      for (const [x, z] of [[-.85, -.8], [.85, -.8], [-.85, .8], [.85, .8]]) box(g, '#6b4a2b', .08, 1.45, .08, x, .08, z);
      roof4(g, '#7a5a3a', 2.3, .45, 2.2, 0, 1.53, 0); box(g, '#5e3b22', 1.9, .06, 1.9, 0, 1.5, 0);
      box(g, '#a0523c', 1.3, .55, .5, 0, .08, -.35);                                               // brick grill
      for (let i = 0; i < 4; i++) box(g, '#8a3f2e', 1.31, .02, .51, 0, .18 + i * .12, -.35);
      box(g, '#2b2b2b', 1.2, .05, .42, 0, .63, -.35);
      const fl = new THREE.Group(); fl.position.set(0, .6, -.35); g.add(fl);
      for (let i = 0; i < 6; i++) { const f = new THREE.Mesh(G.cone4, i % 2 ? flameMat2 : flameMat); f.scale.set(.09, .22, .09); f.position.set(-.45 + i * .18, .02, (i % 2 - .5) * .12); fl.add(f); }
      g.userData.flames = fl;
      for (let i = 0; i < 4; i++) { add(g, G.box, '#2b2b2b', .03, .02, .4, -.45 + i * .3, .68, -.35);
        const fish = new THREE.Group(); fish.position.set(-.45 + i * .3, .74, -.35); fish.rotation.y = Math.PI / 2; g.add(fish);
        add(fish, G.ico, i % 2 ? '#b8743a' : '#c98a4a', .1, .06, .2, 0, 0, 0); add(fish, G.cone4, '#8a5a34', .08, .1, .03, 0, 0, -.24).rotation.x = -Math.PI / 2; }
      const sm = new THREE.MeshStandardMaterial({ color: '#eeeeea', transparent: true, opacity: .28, flatShading: true, depthWrite: false });
      for (let i = 0; i < 3; i++) { const s = new THREE.Mesh(G.ico, sm); s.scale.setScalar(.08 + i * .03); s.position.set(-.25 + i * .22, .9 + i * .18, -.35); g.add(s); }
      box(g, '#8a5a34', 1.3, .06, .4, 0, .45, .45); for (const x of [-.55, .55]) box(g, '#5e3b22', .06, .45, .3, x, .0, .45);
      for (const x of [-.35, .05, .4]) { add(g, G.cyl8, '#f4eee0', .13, .02, .13, x, .52, .45); add(g, G.ico, '#c98a4a', .06, .04, .12, x, .55, .45); }
      add(g, G.cyl8, '#c4473a', .06, .06, .06, .58, .54, .38);
      const c = document.createElement('canvas'); c.width = 384; c.height = 96; const x = c.getContext('2d');
      x.fillStyle = '#f4e3c0'; x.fillRect(0, 0, 384, 96); x.fillStyle = '#a0523c'; x.font = '700 54px "Pixelify Sans", sans-serif'; x.textAlign = 'center'; x.textBaseline = 'middle'; x.fillText('IKAN BAKAR', 192, 50);
      const tx = new THREE.CanvasTexture(c); tx.colorSpace = THREE.SRGBColorSpace;
      const sign = new THREE.Mesh(new THREE.PlaneGeometry(1.3, .33), new THREE.MeshStandardMaterial({ map: tx, roughness: .8 })); sign.position.set(0, 1.32, .97); g.add(sign);
      box(g, '#5e3b22', 1.36, .38, .04, 0, 1.13, .94);
      const lamp = new THREE.Mesh(G.sph, lanternMat); lamp.scale.set(.08, .11, .08); lamp.position.set(.8, 1.25, .85); g.add(lamp);
    } },
  // a cheer billboard from the whole island for a supporter's request (ep 8, traktiran Chalid: "semangat"); text from b.label
  papansemangat: { n: 'Papan Semangat', w: 2, h: 1, land: true,
    build(g, b) {
      const name = (b && b.label) || 'SEMANGAT!';
      for (const x of [-.75, .75]) box(g, '#5e3b22', .1, 1.6, .1, x, 0, 0);
      box(g, '#e6b84a', 2.0, 1.0, .08, 0, 1.25, -.02);
      const c = document.createElement('canvas'); c.width = 512; c.height = 256; const x = c.getContext('2d');
      x.fillStyle = '#fff4dc'; x.fillRect(0, 0, 512, 256); x.fillStyle = '#d0483a'; x.fillRect(0, 0, 512, 14); x.fillRect(0, 242, 512, 14);
      x.textAlign = 'center'; x.textBaseline = 'middle'; x.fillStyle = '#d0483a'; x.font = '700 84px "Pixelify Sans", sans-serif'; x.fillText('SEMANGAT!', 256, 100, 480);
      let fs = 44; x.font = `700 ${fs}px "Pixelify Sans", sans-serif`; while (fs > 22 && x.measureText(name).width > 470) { fs -= 2; x.font = `700 ${fs}px "Pixelify Sans", sans-serif`; }
      x.fillStyle = '#3a2412'; x.fillText(name, 256, 186);
      const tx = new THREE.CanvasTexture(c); tx.colorSpace = THREE.SRGBColorSpace;
      const sign = new THREE.Mesh(new THREE.PlaneGeometry(1.9, .92), new THREE.MeshStandardMaterial({ map: tx, roughness: .8 })); sign.position.set(0, 1.75, .03); g.add(sign);
      for (const x2 of [-.95, -.48, 0, .48, .95]) { const l = new THREE.Mesh(G.sph, lanternMat); l.scale.setScalar(.06); l.position.set(x2, 2.28, .06); g.add(l); }
    } },
  // a small business stall for a real UMKM chosen from the comments (#UMKMPulauAru): the sign shows b.label,
  // the awning colour comes from the name, and tapping it opens the business link (b.link) after a confirmation sheet
  warungumkm: { n: 'Warung UMKM', w: 2, h: 2, land: true,
    build(g, b) {
      const name = (b && b.label) || 'Warung', hue = [...name].reduce((a, c) => (a * 31 + c.charCodeAt(0)) >>> 0, 7) % 6;
      const [c1, c2] = [['#d0483a', '#f4eee0'], ['#2f8a6a', '#f4eee0'], ['#e6b84a', '#5e3b22'], ['#4e7a9a', '#f4eee0'], ['#b06ab3', '#f4eee0'], ['#e07b39', '#fff4dc']][hue];
      box(g, '#c9bfa8', 1.9, .1, 1.85, 0, 0, 0);
      box(g, '#b07a4a', 1.7, 1.15, .1, 0, .1, -.75); box(g, '#9a6a3e', .1, 1.15, 1.1, -.8, .1, -.25); box(g, '#9a6a3e', .1, 1.15, 1.1, .8, .1, -.25);
      for (const [x, z] of [[-.82, .7], [.82, .7]]) box(g, '#5e3b22', .08, 1.35, .08, x, .1, z);
      box(g, c1, 1.85, .08, 1.6, 0, 1.25, -.05);
      for (let i = 0; i < 7; i++) { const a = box(g, i % 2 ? c2 : c1, .27, .05, .5, -.81 + i * .27, 1.18, .82); a.rotation.x = .38; }
      box(g, '#8a5a34', 1.4, .6, .4, 0, .1, .3);                                       // counter
      box(g, c2, 1.42, .06, .42, 0, .7, .3);
      const goods = ['#d0483a', '#e6b84a', '#f2e6c8', '#62bd73', '#c4473a'];
      for (let i = 0; i < 5; i++) add(g, G.cyl8, goods[(i + hue) % 5], .09, .1, .09, -.5 + i * .25, .8, .3);
      box(g, '#8a5a34', 1.3, .06, .3, 0, .9, -.6); for (let i = 0; i < 4; i++) add(g, G.sph, goods[(i + 2) % 5], .1, .1, .1, -.45 + i * .3, 1.0, -.6);
      const c = document.createElement('canvas'); c.width = 512; c.height = 128; const x = c.getContext('2d');
      x.fillStyle = c2; x.fillRect(0, 0, 512, 128); x.fillStyle = c1; x.fillRect(0, 0, 512, 10); x.fillRect(0, 118, 512, 10);
      let fs = 64; x.font = `700 ${fs}px "Pixelify Sans", sans-serif`;
      while (fs > 26 && x.measureText(name).width > 480) { fs -= 2; x.font = `700 ${fs}px "Pixelify Sans", sans-serif`; }
      x.fillStyle = c1 === '#e6b84a' ? '#5e3b22' : c1; x.textAlign = 'center'; x.textBaseline = 'middle'; x.fillText(name, 256, 66);
      const tx = new THREE.CanvasTexture(c); tx.colorSpace = THREE.SRGBColorSpace;
      const sign = new THREE.Mesh(new THREE.PlaneGeometry(1.7, .42), new THREE.MeshStandardMaterial({ map: tx, roughness: .8 })); sign.position.set(0, 1.6, .55); g.add(sign);
      box(g, '#5e3b22', 1.76, .48, .04, 0, 1.36, .52);
      const lamp = new THREE.Mesh(G.sph, lanternMat); lamp.scale.set(.09, .12, .09); lamp.position.set(.75, 1.05, .78); g.add(lamp);
    } },
  // a village cooperative on a floating cloud island, reached by a spiral of cloud steps from the pyramid top
  kopdesawan: { n: 'Kopdes di atas awan', w: 1, h: 1, land: true, float: true,
    layout: (() => {
      const rise = .62, steps = [];
      for (let k = 1; k <= 9; k++) { const a = Math.PI + (k - 9) * .62, r = 1.25 + k * .2; steps.push([Math.sin(a) * r, Math.cos(a) * r, rise * k]); }
      for (let j = 1; j <= 3; j++) steps.push([0, -3.05 - j * 1.05, rise * (9 + j)]);
      const island = { x: 0, z: -11.6, r: 5.2, top: rise * 13 };
      const queue = []; for (let i = 0; i < 6; i++) queue.push([-2.6 + i * 1.05, -9.2 + (i % 2) * .25, Math.PI]);
      const carry = [[-3.6, -8.2, Math.PI * .8], [3.7, -8.6, -Math.PI * .8], [0, -7.4, Math.PI]];
      return { steps, island, queue, carry, kopdes: [0, -12.6] };
    })(),
    build(g) {
      const L = BT.kopdesawan.layout;
      const cloudMat = new THREE.MeshStandardMaterial({ color: '#ffffff', emissive: '#dfe9f2', emissiveIntensity: .25, roughness: 1, flatShading: true });
      const puff = (parent, x, y, z, s, n = 5, seed = 1) => { for (let i = 0; i < n; i++) { const a = i / n * Math.PI * 2 + seed, r = s * (.35 + ((seed * 7 + i * 3) % 5) / 12); const m = new THREE.Mesh(G.ico, cloudMat); const k = s * (.55 + ((seed + i) % 3) * .15); m.scale.set(k, k * .6, k); m.position.set(x + Math.cos(a) * r, y + ((i % 2) - .5) * s * .15, z + Math.sin(a) * r); m.castShadow = true; parent.add(m); } };
      const steps = new THREE.Group(); g.add(steps); g.userData.steps = steps;
      L.steps.forEach(([x, z, y], k) => { const st = new THREE.Group(); st.position.set(x, y, z); steps.add(st); puff(st, 0, -.28, 0, .8, 4, k + 1); const top = new THREE.Mesh(G.cyl8, cloudMat); top.scale.set(.78, .14, .78); top.position.y = -.07; top.receiveShadow = true; st.add(top); });
      const isl = new THREE.Group(); isl.position.set(L.island.x, L.island.top, L.island.z); g.add(isl); g.userData.island = isl;
      for (let ring = 0; ring < 3; ring++) for (let i = 0; i < 9 + ring * 3; i++) { const a = i / (9 + ring * 3) * Math.PI * 2 + ring; const r = L.island.r * (.25 + ring * .33); puff(isl, Math.cos(a) * r, -1.0 - ring * .35 + (ring === 0 ? -.4 : 0), Math.sin(a) * r, 1.6 - ring * .25, 3, i + ring * 5); }
      const grass = new THREE.Mesh(G.cyl8, mat('#7cc25a')); grass.scale.set(L.island.r, .4, L.island.r); grass.position.y = -.2; grass.receiveShadow = true; isl.add(grass);
      const soil = new THREE.Mesh(G.cyl8, mat('#8a6a4a')); soil.scale.set(L.island.r * .96, .5, L.island.r * .96); soil.position.y = -.6; isl.add(soil);
      // the Kopdes building, modelled on the real village cooperatives: long, white, red shutters, red roof, grey sign wall
      const kb = new THREE.Group(); kb.position.set(L.kopdes[0] - L.island.x, 0, L.kopdes[1] - L.island.z); isl.add(kb);
      const W_ = 7.2, D = 2.6, Hh = 1.9;
      box(kb, '#b9bcbd', W_ + .4, .22, D + .7, 0, 0, .15);
      box(kb, '#efede8', W_, Hh, D, 0, .22, 0);
      const roofM = mat('#b3202a');
      for (const sgn of [-1, 1]) { const r = new THREE.Mesh(G.box, roofM); r.scale.set(W_ + .7, .08, D / 2 + .55); r.rotation.x = sgn * .26; r.position.set(0, .22 + Hh + .28, sgn * (D / 4 + .1)); r.castShadow = true; kb.add(r); }
      box(kb, '#efede8', W_ - .05, .32, .06, 0, .22 + Hh, D / 2 - .02);
      const canopy = new THREE.Mesh(G.box, roofM); canopy.scale.set(W_ - 1.6, .05, .65); canopy.rotation.x = .3; canopy.position.set(-.7, .22 + 1.62, D / 2 + .26); canopy.castShadow = true; kb.add(canopy);
      const doors = 5, dw = (W_ - 1.9) / doors;
      for (let i = 0; i < doors; i++) {
        const x = -W_ / 2 + .15 + dw * (i + .5);
        box(kb, '#c61e2a', dw - .14, 1.32, .05, x, .26, D / 2 + .01);
        for (let j = 0; j < 6; j++) box(kb, '#9d1620', dw - .14, .02, .055, x, .4 + j * .2, D / 2 + .015);
        box(kb, '#fbfaf6', .1, 1.5, .1, x + dw / 2, .22, D / 2 + .03);
      }
      box(kb, '#7d8287', 1.55, Hh, .06, W_ / 2 - .8, .22, D / 2 + .02);
      const c = document.createElement('canvas'); c.width = 256; c.height = 256; const x2 = c.getContext('2d');
      x2.fillStyle = '#7d8287'; x2.fillRect(0, 0, 256, 256);
      x2.fillStyle = '#d72630'; x2.beginPath(); x2.moveTo(40, 92); x2.lineTo(98, 40); x2.lineTo(156, 92); x2.lineTo(140, 92); x2.lineTo(98, 56); x2.lineTo(56, 92); x2.fill();
      x2.fillRect(58, 90, 12, 50); x2.fillRect(126, 90, 12, 50); x2.fillRect(58, 132, 80, 10);
      x2.fillStyle = '#ffffff'; x2.fillRect(84, 104, 12, 12); x2.fillRect(100, 104, 12, 12);
      x2.font = '700 46px "Pixelify Sans", sans-serif'; x2.fillStyle = '#d72630'; x2.textAlign = 'left'; x2.fillText('KOP', 150, 88); x2.fillText('DES', 150, 132);
      x2.font = '700 30px sans-serif'; x2.fillStyle = '#ffffff'; x2.textAlign = 'center'; x2.fillText('KOPERASI DESA', 128, 196);
      const tex = new THREE.CanvasTexture(c); tex.colorSpace = THREE.SRGBColorSpace;
      const sign = new THREE.Mesh(new THREE.PlaneGeometry(1.3, 1.3), new THREE.MeshStandardMaterial({ map: tex, roughness: .9 })); sign.position.set(W_ / 2 - .8, 1.15, D / 2 + .06); kb.add(sign);
      // goods waiting to be weighed
      for (let i = 0; i < 4; i++) { const bk = new THREE.Mesh(G.cyl8, mat('#b08850')); bk.scale.set(.22, .24, .22); bk.position.set(-2.4 + i * .5, .12, D / 2 + .9); bk.castShadow = true; kb.add(bk); const f = new THREE.Mesh(G.sph, mat(['#7f97ad', '#6b4a2b', '#ffd24a', '#6fbf4a'][i])); f.scale.setScalar(.12); f.position.set(-2.4 + i * .5, .3, D / 2 + .9); kb.add(f); }
      for (const [lx, lz] of [[-4.2, 1.6], [4.1, 1.2]]) { box(kb, '#5e3b22', .06, 1.3, .06, lx, 0, lz); const l = new THREE.Mesh(G.sph, lanternMat); l.scale.set(.12, .16, .12); l.position.set(lx, 1.35, lz); kb.add(l); }
    } },
  papan: { n: 'Papan nama', w: 1, h: 1, land: true, sign: true, build(g, b) { box(g, '#5e3b22', .08, 1, .08, 0, 0, 0); const board = new THREE.Mesh(G.box, [mat('#8a5a34'), mat('#8a5a34'), mat('#8a5a34'), mat('#8a5a34'), new THREE.MeshStandardMaterial({ map: textTexture(splitLabel(b && b.label || 'Pulau'), { size: 46, grain: true }), flatShading: true }), mat('#8a5a34')]); board.scale.set(.95, .48, .06); board.position.set(0, 1, .05); board.castShadow = true; g.add(board); } },
};
export function spearMesh(parent) {
  add(parent, G.cyl6, '#a9784a', .025, 1.6, .025, 0, .8, 0);
  add(parent, G.cone4, '#cfd3cc', .05, .22, .05, 0, 1.7, 0);
  add(parent, G.box, '#d8c39a', .06, .05, .06, 0, 1.56, 0);
  return parent;
}
function splitLabel(s) { s = String(s).slice(0, 40); if (s.length <= 16) return [s]; const i = s.lastIndexOf(' ', 20); return i > 0 ? [s.slice(0, i), s.slice(i + 1)] : [s.slice(0, 18), s.slice(18)]; }
// data some buildings draw from (supporters, small businesses); main sets it before rebuilding
export const live = { supporters: [], umkm: [] };
export function buildBuilding(b) { const d = BT[b.type]; const g = new THREE.Group(); if (d.scale) { const inner = new THREE.Group(); inner.scale.setScalar(d.scale); g.add(inner); d.build(inner, b); } else d.build(g, b); g.userData.def = d; return g; }

// ---------- landmarks ----------
export function campfire(g) {
  for (let a = 0; a < 8; a++) add(g, G.dode, '#8d8e88', .12, .09, .12, Math.cos(a / 8 * 6.28) * .32, .05, Math.sin(a / 8 * 6.28) * .32);
  const l1 = box(g, '#5e3b22', .55, .1, .1, 0, .05, 0); l1.rotation.y = .6; const l2 = box(g, '#5e3b22', .55, .1, .1, 0, .1, 0); l2.rotation.y = -.6;
  const fl = new THREE.Group(); fl.position.y = .12; g.add(fl);
  for (let i = 0; i < 4; i++) { const f = new THREE.Mesh(G.cone4, i % 2 ? flameMat2 : flameMat); f.scale.set(.12, .4, .12); f.position.set(Math.cos(i * 1.6) * .06, .2, Math.sin(i * 1.6) * .06); fl.add(f); }
  g.userData.flames = fl;
  return g;
}
export function shelter() {
  const g = new THREE.Group();
  box(g, '#5e3b22', .12, 1.9, .12, -1.2, 0, -.7); box(g, '#5e3b22', .12, 1.9, .12, 1.2, 0, -.7);
  box(g, '#5e3b22', .1, .9, .1, -1.2, 0, .8); box(g, '#5e3b22', .1, .9, .1, 1.2, 0, .8);
  const roof = new THREE.Group(); roof.position.set(0, 1.4, 0); roof.rotation.x = .55; g.add(roof);
  for (let i = 0; i < 7; i++) box(roof, i % 2 ? '#7d9a4a' : '#6a8a3a', .38, .06, 1.9, -1.15 + i * .38, 0, 0);
  box(g, '#b39a6a', 1.6, .05, .9, 0, 0, .1); box(g, '#8a6a4a', .45, .14, .3, -.5, .05, -.2);
  box(g, '#5c7a8c', .4, .3, .3, .9, 0, -.3);
  return g;
}
export function mailbox() {
  const g = new THREE.Group();
  box(g, '#5e3b22', .1, 1, .1, 0, 0, 0); box(g, '#3a6ea5', .4, .32, .55, 0, 1, 0); box(g, '#2b5480', .42, .04, .57, 0, 1.3, 0);
  const flag = new THREE.Group(); flag.position.set(.22, 1.1, -.15); g.add(flag); box(flag, '#d0483a', .03, .35, .03, 0, 0, 0); box(flag, '#d0483a', .03, .12, .16, 0, .25, .08);
  g.userData.flag = flag; return g;
}
export function rulesBoard() {
  const g = new THREE.Group();
  box(g, '#5e3b22', .1, 1.6, .1, -.8, 0, 0); box(g, '#5e3b22', .1, 1.6, .1, .8, 0, 0);
  const face = new THREE.Mesh(G.box, [mat('#8a5a34'), mat('#8a5a34'), mat('#8a5a34'), mat('#8a5a34'), new THREE.MeshStandardMaterial({ map: textTexture(['ATURAN', 'PULAU'], { size: 64, grain: true }), flatShading: true }), mat('#8a5a34')]);
  face.scale.set(1.9, .9, .08); face.position.set(0, 1.3, .06); face.castShadow = true; g.add(face);
  return g;
}
export function wreck() {
  const g = new THREE.Group();
  const hull = new THREE.Group(); hull.rotation.set(.12, .4, .35); hull.position.y = .1; g.add(hull);
  const ribs = 7; for (let i = 0; i < ribs; i++) { const z = -1.2 + i * .4, w = 1 - Math.abs(i - 3) * .12; box(hull, i === 4 ? '#3e2716' : '#5e3b22', w * 1.2, .12, .3, 0, 0, z); box(hull, '#6b4529', .12, .55, .3, -w * .6, 0, z); if (i !== 2 && i !== 5) box(hull, '#6b4529', .12, .55, .3, w * .6, 0, z); }
  box(hull, '#4a2f1c', .12, 1.2, .12, 0, .1, .2).rotation.z = .4;
  box(g, '#8a6a4a', .8, .06, .18, 1.4, 0, .6).rotation.y = .8;
  box(g, '#8a6a4a', .6, .06, .18, -1.2, 0, -.7).rotation.y = -.4;
  // coiled rope (the first clue)
  add(g, new THREE.TorusGeometry(.18, .05, 4, 8), '#c9b27a', 1, 1, 1, .9, .06, -.4).rotation.x = Math.PI / 2;
  return g;
}
export function lighthouse() {
  const g = new THREE.Group();
  cyl(g, '#8d8a80', 1.6, .5, 0, 0, 0, 8);
  const hgt = 8, segs = 8;
  for (let i = 0; i < segs; i++) { const r0 = 1.15 - i / segs * .4, r1 = 1.15 - (i + 1) / segs * .4; const m = new THREE.Mesh(new THREE.CylinderGeometry(r1, r0, hgt / segs, 10), mat(i % 2 ? '#f2efe6' : '#c4473a')); m.position.y = .5 + (i + .5) * hgt / segs; m.castShadow = true; m.receiveShadow = true; g.add(m); }
  const top = .5 + hgt;
  cyl(g, '#343a44', 1.05, .15, 0, top, 0, 10);
  for (let a = 0; a < 12; a++) box(g, '#343a44', .04, .4, .04, Math.cos(a / 12 * 6.28) * 1, top + .15, Math.sin(a / 12 * 6.28) * 1);
  const glass = new THREE.MeshStandardMaterial({ color: '#56707a', emissive: '#ffd27a', emissiveIntensity: 0, flatShading: true, roughness: .2 });
  const room = new THREE.Mesh(new THREE.CylinderGeometry(.6, .6, 1, 8), glass); room.position.y = top + .65; g.add(room);
  const roof = new THREE.Mesh(new THREE.ConeGeometry(.8, .8, 8), mat('#c4473a')); roof.position.y = top + 1.55; roof.castShadow = true; g.add(roof);
  add(g, G.sph, '#343a44', .1, .1, .1, 0, top + 2, 0);
  box(g, '#4a3a2a', .5, .9, .1, 0, .5, 1.12);
  // lamps: spiral of small bulbs around the tower, one per resident (first 64 visible)
  const N = 64, lampGeo = new THREE.IcosahedronGeometry(.07, 0);
  const lamps = [];
  for (let i = 0; i < N; i++) {
    const t = i / N, y = .9 + t * (hgt - .7), r = 1.15 - (y - .5) / hgt * .4 + .05, a = i * 2.4;
    const m = new THREE.Mesh(lampGeo, lampOffMat); m.position.set(Math.cos(a) * r, y, Math.sin(a) * r); g.add(m); lamps.push(m);
  }
  // rotating beam
  const beamGeo = new THREE.ConeGeometry(3.2, 30, 16, 1, true); beamGeo.translate(0, -15, 0); beamGeo.rotateZ(Math.PI / 2);
  const beamMat = new THREE.MeshBasicMaterial({ color: '#fff0b8', transparent: true, opacity: 0, depthWrite: false, blending: THREE.AdditiveBlending, side: THREE.DoubleSide });
  const beam = new THREE.Group(); beam.position.y = top + .65; g.add(beam);
  const b1 = new THREE.Mesh(beamGeo, beamMat); beam.add(b1); const b2 = b1.clone(); b2.rotation.y = Math.PI; beam.add(b2);
  g.userData = { lamps, glass, beam, beamMat, top: top + .65 };
  return g;
}
export function nameStone() {
  const g = new THREE.Group();
  const rock = add(g, G.dode, '#7c827d', 1.3, 1.25, .6, 0, 1.05, -.05); rock.rotation.set(.1, .2, .05);
  add(g, G.dode, '#6c716c', .6, .45, .5, -1.1, .25, .3);
  add(g, G.dode, '#6c716c', .45, .35, .4, 1.2, .2, .2);
  const c = document.createElement('canvas'); c.width = 512; c.height = 384;
  const tex = new THREE.CanvasTexture(c); tex.colorSpace = THREE.SRGBColorSpace; tex.anisotropy = 4;
  const face = new THREE.Mesh(new THREE.PlaneGeometry(1.75, 1.3), new THREE.MeshStandardMaterial({ map: tex, roughness: 1, flatShading: true }));
  face.position.set(0, 1.1, .74); face.rotation.x = -.05; g.add(face);
  g.userData.paint = (names, total) => {
    const x = c.getContext('2d');
    x.fillStyle = '#9ba19b'; x.fillRect(0, 0, 512, 384);
    for (let i = 0; i < 300; i++) { x.fillStyle = `rgba(${Math.random() > .5 ? '255,255,255' : '0,0,0'},${Math.random() * .08})`; x.fillRect(Math.random() * 512, Math.random() * 384, 2 + Math.random() * 6, 2 + Math.random() * 6); }
    x.textAlign = 'center'; x.textBaseline = 'middle';
    const carve = (t, px, py, fs) => { x.font = `700 ${fs}px "Pixelify Sans", monospace`; x.fillStyle = 'rgba(255,255,255,.35)'; x.fillText(t, px + 1.5, py + 1.5); x.fillStyle = '#3f4440'; x.fillText(t, px, py); };
    carve('WARGA PULAU', 256, 34, 34);
    if (!names.length) { carve('menunggu', 256, 180, 28); carve('warga pertama', 256, 216, 28); }
    else {
      const show = names.slice(-27); const cols = 3, rowH = 30;
      show.forEach((n, i) => { const col = i % cols, row = (i / cols) | 0; let t = '@' + n; if (t.length > 14) t = t.slice(0, 13) + '…'; carve(t, 90 + col * 166, 82 + row * rowH, 20); });
      carve(total.toLocaleString('id-ID') + ' nama', 256, 362, 22);
    }
    tex.needsUpdate = true;
  };
  return g;
}
export function ship() {
  const g = new THREE.Group();
  box(g, '#3d2a1c', 5, 1, 1.6, 0, 0, 0); box(g, '#c4473a', 5.05, .15, 1.65, 0, .8, 0);
  const bow = add(g, G.cone4, '#3d2a1c', .8, 1.6, 1.15, 3.2, .5, 0, Math.PI / 4); bow.rotation.z = -Math.PI / 2;
  box(g, '#8a5a34', 4.8, .08, 1.4, 0, 1, 0); box(g, '#5e3b22', 1.2, .8, 1.2, -1.8, 1, 0);
  for (let i = 0; i < 5; i++) box(g, lanternMat, .2, .15, .05, -1.6 + i * .8, .45, .82);
  for (const [x, h] of [[-.5, 4.5], [1.5, 3.6]]) { box(g, '#5e3b22', .12, h, .12, x, 1, 0); const s = box(g, '#f6f0de', .05, h * .55, 1.6, x + .15, 1.6, 0); s.castShadow = true; }
  box(g, '#d0483a', .5, .3, .03, -.5, 5.3, 0);
  return g;
}
export function festival(radius = 6) {
  const g = new THREE.Group(); const N = 8; const cols = ['#d0483a', '#ffc94a', '#3a7fc2', '#5fae6a'];
  const pts = []; for (let k = 0; k < N; k++) { const a = k / N * Math.PI * 2; pts.push([Math.cos(a) * radius, Math.sin(a) * radius * .75]); box(g, '#5e3b22', .1, 2.4, .1, pts[k][0], 0, pts[k][1]); }
  const lanterns = [];
  for (let k = 0; k < N; k++) {
    const [ax, az] = pts[k], [bx, bz] = pts[(k + 1) % N];
    for (let i = 0; i < 8; i++) { const t0 = i / 8, t1 = (i + 1) / 8, y0 = 2.3 - Math.sin(t0 * Math.PI) * .5, y1 = 2.3 - Math.sin(t1 * Math.PI) * .5; const x0 = ax + (bx - ax) * t0, z0 = az + (bz - az) * t0, x1 = ax + (bx - ax) * t1, z1 = az + (bz - az) * t1; const len = Math.hypot(x1 - x0, y1 - y0, z1 - z0); const r = new THREE.Mesh(G.box, mat('#e8dcc4')); r.scale.set(.02, .02, len); r.position.set((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2); r.lookAt(x1, y1, z1); g.add(r); }
    for (let i = 1; i < 7; i++) { const t = i / 7, x = ax + (bx - ax) * t, z = az + (bz - az) * t, y = 2.3 - Math.sin(t * Math.PI) * .5; const f = add(g, G.cone4, cols[(i + k) % 4], .12, .22, .03, x, y - .1, z, Math.atan2(bz - az, bx - ax)); f.rotation.x = Math.PI; f.castShadow = false; }
    const l = add(g, G.sph, lanternMat, .16, .2, .16, pts[k][0], 2.5, pts[k][1]); l.castShadow = false; lanterns.push(l);
  }
  g.userData.lanterns = lanterns; return g;
}

// instanced nature
export function makeInstanced(geo, material, count) { const m = new THREE.InstancedMesh(geo, material, Math.max(1, count)); m.castShadow = true; m.receiveShadow = true; m.count = count; return m; }
