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
  rumah: { n: 'Rumah', w: 2, h: 2, land: true, build(g) { box(g, '#e3c49a', 1.6, 1.1, 1.4, 0, 0, 0); roof4(g, '#b8523c', 2.1, 1, 1.9, 0, 1.1, 0); box(g, '#5e3b22', .36, .66, .05, 0, 0, .71); box(g, windowMat, .3, .3, .05, -.5, .5, .71); box(g, windowMat, .3, .3, .05, .5, .5, .71); box(g, '#9a9b94', .22, .5, .22, .45, 1.3, -.3); } },
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
export function buildBuilding(b) { const d = BT[b.type]; const g = new THREE.Group(); d.build(g, b); g.userData.def = d; return g; }

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
      const show = names.slice(-30); const cols = 3, rowH = 30;
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
