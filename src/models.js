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
// ep 19/20: props for the regular cast (guitar, game pad, cookie tray, bodyguard suit, fishing rod, hood)
export function castKit(ch, pose) {
  const b = ch.userData.body;
  if (pose === 'guitar') { box(b, '#b5651d', .34, .4, .1, .05, .42, .2); box(b, '#2a1a10', .1, .1, .11, .05, .44, .21); box(b, '#6b4226', .06, .5, .05, .38, .6, .2); box(b, '#3a2412', .08, .1, .06, .55, .75, .2); }
  if (pose === 'game') { box(b, '#2b2d42', .3, .08, .14, 0, .62, .38); box(b, '#e63946', .05, .03, .05, .08, .67, .38); box(b, '#43aa8b', .05, .03, .05, -.08, .67, .38); }
  // ep 20: the bodyguard's dark suit and sunglasses, Rayhan's rod with (as always) a sandal on the hook, NOVA's hood
  if (pose === 'guard') { box(b, '#16181d', .48, .55, .3, 0, .49, 0); box(b, '#0a0a0a', .32, .07, .03, 0, 1.21, .18); box(b, '#0a0a0a', .03, .1, .03, .19, 1.1, .05); box(b, '#d9d9d9', .08, .2, .02, 0, .8, .155); box(b, '#8b1e1e', .04, .2, .022, 0, .78, .158); }
  if (pose === 'rod') { const r = box(b, '#6b4226', .04, 1.7, .04, .22, .35, .95); r.rotation.x = 1.0; const l = box(b, '#e8e8e8', .012, 1.42, .012, .22, .24, 1.66); const s1 = box(b, '#2f7de1', .12, .03, .26, .22, .2, 1.66); s1.rotation.x = .5; box(b, '#1b4f9a', .1, .03, .03, .22, .26, 1.6); }
  // ep 29: the new harbour's first fisherman (@muhamatferos197) has a real fish on his hook, not a sandal
  if (pose === 'rodfish') { const r = box(b, '#6b4226', .04, 1.7, .04, .22, .35, .95); r.rotation.x = 1.0; box(b, '#e8e8e8', .012, 1.42, .012, .22, .24, 1.66); const f = add(b, G.sph, new THREE.MeshStandardMaterial({ color: '#b9e2f5', emissive: '#3a6f8f', emissiveIntensity: .25, metalness: .2, roughness: .35, flatShading: true }), .09, .27, .07, .22, .02, 1.66); add(b, G.cone4, '#e8a33a', .13, .14, .04, .22, -.33, 1.66); add(b, G.cone4, '#e8a33a', .03, .1, .06, .22, .1, 1.6); add(b, G.sph, '#1d1d1d', .02, .02, .02, .28, .16, 1.66); }
  // ep 30: the Penjaga Mercusuar: long navy coat, hood, white beard, a glowing lantern in the right hand
  if (pose === 'keeper') { box(b, '#22344a', .5, .62, .32, 0, .45, 0); box(b, '#4a6a86', .5, .16, .48, 0, 1.44, -.02); box(b, '#4a6a86', .5, .4, .08, 0, 1.2, -.24); for (const x of [-.24, .24]) box(b, '#4a6a86', .06, .4, .44, x, 1.22, -.02); box(b, '#eeeae2', .3, .12, .06, 0, .98, .2); box(b, '#eeeae2', .18, .1, .06, 0, .88, .2); box(b, '#eeeae2', .07, .04, .05, -.07, 1.07, .2); box(b, '#eeeae2', .07, .04, .05, .07, 1.07, .2); box(b, '#c9a24a', .5, .04, .33, 0, .78, 0);
    add(b, G.cyl6, '#2a2a2a', .012, .16, .012, .3, .8, .4); add(b, G.cyl6, '#2a2a2a', .1, .03, .1, .3, .72, .4); add(b, G.cyl6, '#2a2a2a', .09, .03, .09, .3, .52, .4); const gl = add(b, G.cyl6, new THREE.MeshStandardMaterial({ color: '#ffe3a0', emissive: '#ffb84a', emissiveIntensity: 1.6, transparent: true, opacity: .9 }), .075, .17, .075, .3, .62, .4); gl.castShadow = false; }
  if (pose === 'hide') { box(b, '#5b5f6b', .4, .14, .4, 0, 1.36, -.02); box(b, '#5b5f6b', .4, .3, .08, 0, 1.18, -.2); }
  // ep 21: whoyss (sneak) still holds the three cart bolts he 'didn't' take
  if (pose === 'sneak') { for (const [x, y] of [[.3, .52], [.36, .47], [.27, .44]]) { add(b, G.cyl6, '#b8bec2', .035, .07, .035, x, y, .26); add(b, G.cyl6, '#8a9196', .055, .02, .055, x, y + .04, .26); } }
  // ep 22: Bu Guru Gina's attendance book and pen, Zidan's broom (penjaga masjid)
  if (pose === 'teach') { box(b, '#2f5e8a', .26, .34, .05, -.24, .5, .3).rotation.x = -.5; box(b, '#f4eee0', .22, .3, .052, -.24, .505, .3).rotation.x = -.5; box(b, '#c4473a', .02, .16, .02, .3, 1.0, .1); }
  if (pose === 'sweep') { const st = box(b, '#a9784a', .035, 1.3, .035, .26, -.1, .38); st.rotation.x = -.35; const br = box(b, '#d9b45a', .3, .2, .1, .26, -.12, .62); br.rotation.x = -.35; box(b, '#2f7de1', .1, .03, .22, -.3, .42, .22).rotation.x = -1.2; box(b, '#1b4f9a', .08, .03, .03, -.3, .47, .2); }
  // ep 23: Debby's clipboard with the president's schedule, Bu Guru Gina's study-tour flag, the pupils' yellow tour caps
  if (pose === 'clip') { const cb = box(b, '#8a5a34', .26, .34, .03, -.22, .48, .32); cb.rotation.x = -.6; const pg = box(b, '#fbf7ee', .22, .26, .032, -.22, .5, .325); pg.rotation.x = -.6; box(b, '#9a9b94', .1, .04, .04, -.22, .8, .27); box(b, '#2f5e8a', .02, .18, .02, .3, .7, .2); }
  if (pose === 'flag') { add(b, G.cyl6, '#c9a868', .018, 1.5, .018, .3, 1.25, .28); const fl = box(b, '#ffd25a', .42, .26, .015, .52, 1.78, .28); box(b, '#d0483a', .42, .05, .016, .52, 1.9, .28); }
  if (pose === 'cap') { box(b, '#ffd25a', .42, .1, .42, 0, 1.4, -.01); box(b, '#ffd25a', .3, .03, .2, 0, 1.4, .26); box(b, '#d0483a', .43, .03, .43, 0, 1.43, -.01); }
  // ep 27: Menteri Keuangan @araa_yinchan: a big calculator in the left hand, a gold coin in the right
  if (pose === 'calc') { const cb = box(b, '#2b2d42', .2, .28, .04, -.22, .48, .32); cb.rotation.x = -.6; box(b, '#9fd8a8', .15, .06, .042, -.22, .66, .29).rotation.x = -.6; add(b, G.cyl8, '#e6b84a', .06, .015, .06, .3, .62, .3).rotation.x = Math.PI / 2; }
  // ep 28: Komandan Damkar @vcxn.mx: red helmet with a brim, a reflective yellow band on the shirt, a radio on the belt
  if (pose === 'damkar') { box(b, '#d0302a', .42, .16, .42, 0, 1.35, -.01); box(b, '#d0302a', .5, .03, .5, 0, 1.33, -.01); box(b, '#f2c230', .1, .08, .02, 0, 1.4, .22); box(b, '#f2c230', .47, .06, .29, 0, .62, 0); box(b, '#f2c230', .47, .06, .29, 0, .8, 0); box(b, '#2b2b2b', .08, .14, .06, .2, .5, .16); }
  if (pose === 'cookie') { box(b, '#e9d8a6', .34, .03, .24, -.1, .66, .36); for (const [x, z] of [[-.2, .3], [-.06, .32], [-.14, .42], [0, .42]]) box(b, '#b07040', .07, .04, .07, x, .69, z); box(b, '#d62828', .06, .06, .06, -.24, .7, .44); }
  // ep 33: the two detectives from the comments (@mhmmdalfaiz0, @ngala.tcl): brown checked detective hat, a magnifying glass held up to the eye
  if (pose === 'detektif') { box(b, '#7a5a3a', .42, .16, .42, 0, 1.36, -.01); box(b, '#7a5a3a', .54, .03, .54, 0, 1.35, -.01); box(b, '#5a3f26', .43, .04, .43, 0, 1.4, -.01); box(b, '#c9a24a', .1, .05, .02, .12, 1.42, .22);
    add(b, G.cyl6, '#3a2a1a', .025, .26, .025, .3, .86, .34); const ring = add(b, G.cyl8, '#c9a24a', .12, .02, .12, .3, 1.06, .36); ring.rotation.x = Math.PI / 2; const gl = add(b, G.cyl8, new THREE.MeshStandardMaterial({ color: '#cfeaf5', emissive: '#7fb8d0', emissiveIntensity: .35, transparent: true, opacity: .6 }), .1, .022, .1, .3, 1.06, .36); gl.rotation.x = Math.PI / 2; gl.castShadow = false; }
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

export const CHAR_SCALE = .9;
// body offset that puts a character's seat (bottom of the torso, hip .5 in unscaled units) exactly on a surface
// `top` metres above the character's feet; was a fixed -.42, which sank people deep into chairs and logs
export const sitBodyY = (top) => top / CHAR_SCALE - .5;
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
  bake(head);   // head never animates on its own: one mesh per colour
  root.scale.setScalar(CHAR_SCALE);   // people are 10% smaller than built, so buildings read at a realistic size
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
  tenda: { n: 'Tenda', w: 3, h: 3, scale: 1.35, land: true, build(g) { add(g, G.cone4, '#d9763f', 1, 1.4, 1, 0, .7, 0, Math.PI / 4); box(g, '#3a2a20', .3, .5, .05, 0, 0, .55); add(g, G.cyl6, '#5e3b22', .03, .3, .03, 0, 1.5, 0); } },
  kebun: { n: 'Kebun', w: 3, h: 2, land: true, walk: true, build(g) { box(g, '#7a5534', 2.8, .12, 1.8, 0, 0, 0); for (let r = 0; r < 4; r++) { box(g, '#5d3e24', 2.6, .06, .14, 0, .12, -.6 + r * .4); for (let c = 0; c < 7; c++) add(g, G.cone6, r % 2 ? '#62bd73' : '#e0a84a', .09, .28, .09, -1.1 + c * .36, .3, -.6 + r * .4); } } },
  sumur: { n: 'Sumur', w: 2, h: 2, scale: 1.2, land: true, build(g) { cyl(g, '#9a9b94', .38, .5, 0, 0, 0, 8); add(g, G.cyl8, '#2b6a85', .3, .02, .3, 0, .45, 0, 0, false); box(g, '#5e3b22', .06, 1.1, .06, -.34, .5, 0); box(g, '#5e3b22', .06, 1.1, .06, .34, .5, 0); roof4(g, '#b8523c', .95, .4, .7, 0, 1.55, 0); } },
  dermaga: { n: 'Dermaga', w: 1, h: 4, water: true, walk: true, build(g) { for (let i = 0; i < 12; i++) box(g, i % 2 ? '#b07a4a' : '#8a5a34', .9, .08, .3, 0, .22, -1.7 + i * .31); for (const z of [-1.8, 0, 1.8]) for (const x of [-.4, .4]) add(g, G.cyl6, '#5e3b22', .07, 1.8, .07, x, -.6, z); } },
  jembatan: { n: 'Jembatan', w: 4, h: 1, water: true, walk: true, build(g) { for (let i = 0; i < 12; i++) box(g, i % 2 ? '#b07a4a' : '#8a5a34', .3, .08, .9, -1.7 + i * .31, .22, 0); for (const x of [-1.8, 0, 1.8]) for (const z of [-.42, .42]) { add(g, G.cyl6, '#5e3b22', .06, 2.2, .06, x, -.6, z); } box(g, '#8a5a34', 3.9, .06, .06, 0, .7, -.42); box(g, '#8a5a34', 3.9, .06, .06, 0, .7, .42); } },
  api: { n: 'Api unggun', w: 1, h: 1, land: true, fire: true, build(g) { campfire(g); } },
  pasar: { n: 'Pasar', w: 5, h: 3, scale: 1.6, land: true, build(g) { for (const sx of [-.75, .75]) { box(g, '#b07a4a', 1.2, .6, .6, sx, 0, .2); for (const [px, pz] of [[-.55, -.4], [.55, -.4], [-.55, .45], [.55, .45]]) box(g, '#5e3b22', .06, 1.3, .06, sx + px, 0, pz); for (let i = 0; i < 6; i++) box(g, i % 2 ? '#f0e6d0' : '#d0483a', .2, .06, 1.1, sx - .5 + i * .2, 1.3, 0); const cols = ['#e6b84a', '#7bc06a', '#d56b3a']; for (let i = 0; i < 3; i++) add(g, G.sph, cols[i], .1, .1, .1, sx - .35 + i * .35, .7, .25); } } },
  sekolah: { n: 'Sekolah', w: 6, h: 4, scale: 1.8, land: true, build(g) { box(g, '#efe2c6', 2.6, 1.3, 1.5, 0, 0, 0); roof4(g, '#4e7a9a', 3.3, .9, 2, 0, 1.3, 0); box(g, '#4e7a9a', .4, .5, .4, 0, 2.1, 0); add(g, G.sph, '#e5c06a', .1, .1, .1, 0, 2.4, .21); box(g, '#5e3b22', .4, .8, .05, 0, 0, .76); for (const x of [-.9, -.5, .5, .9]) box(g, windowMat, .26, .3, .05, x, .6, .76); } },
  menara: { n: 'Menara pandang', w: 2, h: 2, scale: 1.3, land: true, build(g) { for (const [x, z] of [[-.35, -.35], [.35, -.35], [-.35, .35], [.35, .35]]) box(g, '#5e3b22', .08, 2.6, .08, x, 0, z); box(g, '#8a5a34', .95, .1, .95, 0, 2.5, 0); for (let i = 0; i < 4; i++) box(g, '#8a5a34', .8, .05, .05, 0, .6 + i * .5, .36); roof4(g, '#d9b45c', 1.3, .7, 1.3, 0, 3.1, 0); for (const [x, z] of [[-.4, -.4], [.4, -.4], [-.4, .4], [.4, .4]]) box(g, '#5e3b22', .05, .5, .05, x, 2.6, z); } },
  patung: { n: 'Patung', w: 1, h: 1, scale: 1.5, land: true, build(g) { box(g, '#9a9b94', .8, .5, .8, 0, 0, 0); box(g, '#c2c2b8', .3, .5, .2, 0, .5, 0); box(g, '#c2c2b8', .4, .45, .25, 0, .95, 0); box(g, '#c2c2b8', .3, .3, .28, 0, 1.4, 0); const a = box(g, '#c2c2b8', .1, .45, .1, .26, 1.1, 0); a.rotation.z = -2.6; a.position.y = 1.55; } },
  taman: { n: 'Taman bunga', w: 2, h: 2, land: true, walk: true, build(g) { box(g, '#5aa64c', 1.9, .06, 1.9, 0, 0, 0); const cols = ['#f06b8a', '#ffd25a', '#f4f1ea', '#b48cf0', '#ff9b52']; for (let i = 0; i < 26; i++) { const x = -.8 + ((i * 37) % 17) / 10, z = -.8 + ((i * 53) % 17) / 10; add(g, G.cyl6, '#3f8a42', .015, .25, .015, x, .18, z, 0, false); add(g, G.sph, cols[i % 5], .07, .06, .07, x, .32, z); } for (let i = 0; i < 8; i++) { box(g, '#e8dcc4', .05, .3, .05, -.95 + i * .27, 0, -.95); box(g, '#e8dcc4', .05, .3, .05, -.95 + i * .27, 0, .95); } } },
  kelapa: { n: 'Pohon kelapa', w: 1, h: 1, land: true, build(g) { palm(g, 0, 0, 1); } },
  lumbung: { n: 'Lumbung', w: 4, h: 4, scale: 1.45, land: true, build(g) { box(g, '#a8443a', 1.6, 1.3, 1.5, 0, 0, 0); const r = add(g, G.cone4, '#5b3b2a', 1.25, .9, 1.15, 0, 1.75, 0, Math.PI / 4); box(g, '#efe2c6', .6, .8, .05, 0, 0, .76); box(g, '#7c2f28', .5, .7, .06, 0, .05, .77); const x1 = box(g, '#efe2c6', .06, .9, .07, 0, 0, .79); x1.rotation.z = .6; x1.position.y = .4; const x2 = box(g, '#efe2c6', .06, .9, .07, 0, 0, .79); x2.rotation.z = -.6; x2.position.y = .4; } },
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
  apotik: { n: 'Apotik', w: 4, h: 3, scale: 1.7, land: true,
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
  warteg: { n: 'Warteg', w: 3, h: 3, scale: 1.6, land: true,
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
  rumahsakit: { n: 'Rumah sakit', w: 6, h: 5, scale: 1.7, land: true, scale: 1.25,
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
      for (const x of [-.75, .75]) box(g, '#5e3b22', .1, 1.6, .1, x, 0, -.13);
      box(g, '#e6b84a', 2.0, 1.0, .08, 0, 1.25, -.03);
      const c = document.createElement('canvas'); c.width = 512; c.height = 256; const x = c.getContext('2d');
      x.fillStyle = '#fff4dc'; x.fillRect(0, 0, 512, 256); x.fillStyle = '#d0483a'; x.fillRect(0, 0, 512, 14); x.fillRect(0, 242, 512, 14);
      x.textAlign = 'center'; x.textBaseline = 'middle'; x.fillStyle = '#d0483a'; x.font = '700 84px "Pixelify Sans", sans-serif'; x.fillText('SEMANGAT!', 256, 100, 480);
      let fs = 44; x.font = `700 ${fs}px "Pixelify Sans", sans-serif`; while (fs > 22 && x.measureText(name).width > 470) { fs -= 2; x.font = `700 ${fs}px "Pixelify Sans", sans-serif`; }
      x.fillStyle = '#3a2412'; x.fillText(name, 256, 186);
      const tx = new THREE.CanvasTexture(c); tx.colorSpace = THREE.SRGBColorSpace;
      const sign = new THREE.Mesh(new THREE.PlaneGeometry(1.9, .92), new THREE.MeshStandardMaterial({ map: tx, roughness: .8 })); sign.position.set(0, 1.75, .03); g.add(sign);
      for (const x2 of [-.95, -.48, 0, .48, .95]) { const l = new THREE.Mesh(G.sph, lanternMat); l.scale.setScalar(.06); l.position.set(x2, 2.28, .06); g.add(l); }
    } },
  // an honesty canteen with no cashier: take a snack, drop the money in the box (ep 9, traktiran "jujur dan punya prinsip")
  kantinjujur: { n: 'Kantin Kejujuran', w: 3, h: 3, scale: 1.5, land: true,
    build(g) {
      box(g, '#c9bfa8', 1.9, .1, 1.85, 0, 0, 0);
      box(g, '#e8dcc0', 1.75, 1.2, .1, 0, .1, -.78); box(g, '#d8caa8', .1, 1.2, 1.1, -.82, .1, -.28); box(g, '#d8caa8', .1, 1.2, 1.1, .82, .1, -.28);
      for (const [x, z] of [[-.84, .72], [.84, .72]]) box(g, '#5e3b22', .08, 1.4, .08, x, .1, z);
      box(g, '#3f7f5a', 1.95, .08, 1.7, 0, 1.3, -.05);                                                   // green roof
      for (let i = 0; i < 7; i++) { const a = box(g, i % 2 ? '#f4eee0' : '#3f7f5a', .28, .05, .48, -.84 + i * .28, 1.23, .84); a.rotation.x = .38; }
      box(g, '#8a5a34', 1.5, .62, .42, 0, .1, .28); box(g, '#f4eee0', 1.52, .06, .44, 0, .72, .28);        // counter
      for (let i = 0; i < 3; i++) { const tray = -.55 + i * .42; add(g, G.cyl8, '#d8d2c4', .17, .03, .17, tray, .79, .26);   // trays of gorengan
        for (let k = 0; k < 4; k++) add(g, G.ico, ['#d99a3e', '#c98a3a', '#e0b050'][i], .055, .035, .08, tray - .07 + (k % 2) * .13, .84 + (k >> 1) * .03, .22 + (k >> 1) * .08); }
      box(g, '#7a4a28', .3, .24, .24, .58, .78, .3); box(g, '#2b1a10', .16, .02, .04, .58, 1.02, .3);    // money box with a slot
      const c = document.createElement('canvas'); c.width = 512; c.height = 160; const x = c.getContext('2d');
      x.fillStyle = '#fff8e6'; x.fillRect(0, 0, 512, 160); x.fillStyle = '#3f7f5a'; x.fillRect(0, 0, 512, 12); x.fillRect(0, 148, 512, 12);
      x.textAlign = 'center'; x.textBaseline = 'middle'; x.fillStyle = '#2f6a48'; x.font = '700 56px "Pixelify Sans", sans-serif'; x.fillText('KANTIN KEJUJURAN', 256, 62, 490);
      x.fillStyle = '#5e3b22'; x.font = '700 30px "Pixelify Sans", sans-serif'; x.fillText('ambil sendiri · bayar sendiri', 256, 118, 490);
      const tx = new THREE.CanvasTexture(c); tx.colorSpace = THREE.SRGBColorSpace;
      const sign = new THREE.Mesh(new THREE.PlaneGeometry(1.75, .55), new THREE.MeshStandardMaterial({ map: tx, roughness: .8 })); sign.position.set(0, 1.66, .56); g.add(sign);
      box(g, '#5e3b22', 1.82, .62, .04, 0, 1.35, .53);
      const c2 = document.createElement('canvas'); c2.width = 128; c2.height = 64; const y = c2.getContext('2d');
      y.fillStyle = '#f4e3c0'; y.fillRect(0, 0, 128, 64); y.fillStyle = '#3a2412'; y.font = '700 30px "Pixelify Sans", sans-serif'; y.textAlign = 'center'; y.textBaseline = 'middle'; y.fillText('BAYAR', 64, 34);
      const t2 = new THREE.CanvasTexture(c2); t2.colorSpace = THREE.SRGBColorSpace;
      const lab = new THREE.Mesh(new THREE.PlaneGeometry(.26, .13), new THREE.MeshStandardMaterial({ map: t2, roughness: .8 })); lab.position.set(.58, .9, .425); g.add(lab);
      const lamp = new THREE.Mesh(G.sph, lanternMat); lamp.scale.set(.09, .12, .09); lamp.position.set(-.75, 1.08, .8); g.add(lamp);
    } },
  // a street lamp along the main street; ten of them from Tiara's ten traktiran (ep 9). b.label puts a small plaque on the post
  lampusemangat: { n: 'Lampu Semangat', w: 1, h: 1, land: true,
    build(g, b) {
      box(g, '#6b6b66', .26, .12, .26, 0, 0, 0); box(g, '#3d4a52', .08, 2.3, .08, 0, .1, 0);
      box(g, '#3d4a52', .06, .06, .5, 0, 2.3, .2); box(g, '#2b3338', .26, .06, .26, 0, 2.28, .44);
      const l = new THREE.Mesh(G.sph, lanternMat); l.scale.set(.13, .15, .13); l.position.set(0, 2.14, .44); g.add(l);
      const h = new THREE.Mesh(G.sph, mat('#e6b84a')); h.scale.set(.1, .1, .03); h.position.set(0, 1.55, .06); g.add(h);
      if (b && b.label) {
        const c = document.createElement('canvas'); c.width = 256; c.height = 96; const x = c.getContext('2d');
        x.fillStyle = '#e6b84a'; x.fillRect(0, 0, 256, 96); x.fillStyle = '#3a2412'; x.textAlign = 'center'; x.textBaseline = 'middle';
        x.font = '700 30px "Pixelify Sans", sans-serif'; x.fillText('LAMPU SEMANGAT', 128, 30, 240); x.font = '700 26px "Pixelify Sans", sans-serif'; x.fillText(b.label, 128, 68, 240);
        const tx = new THREE.CanvasTexture(c); tx.colorSpace = THREE.SRGBColorSpace;
        const p = new THREE.Mesh(new THREE.PlaneGeometry(.56, .21), new THREE.MeshStandardMaterial({ map: tx, roughness: .8 })); p.position.set(0, 1.15, .06); g.add(p);
      }
    } },
  // the vice president's fruit farm: mango and banana trees, a watermelon patch, a scarecrow, a seed kiosk and six
  // soil beds where every visitor grows their own plants (src/kebun.js, saved on their device) (ep 11, wapres @EGA_91)
  ladang: { n: 'Ladang Buah', w: 8, h: 6, land: true, open: 'kebun', openLabel: 'Berkebun',
    plots: [[.9, -.55], [2.0, -.55], [3.1, -.55], [.9, .65], [2.0, .65], [3.1, .65]],
    build(g) {
      box(g, '#8a6a44', 7.9, .06, 5.9, 0, 0, 0);
      // fence with a gate at the front
      const fm = mat('#a07a4a');
      for (let x = -3.9; x <= 3.91; x += .65) for (const z of [-2.9, 2.9]) if (z < 0 || Math.abs(x) > .7) box(g, fm, .07, .55, .07, x, .06, z);
      for (let z = -2.9; z <= 2.91; z += .58) for (const x of [-3.9, 3.9]) box(g, fm, .07, .55, .07, x, .06, z);
      for (const y of [.25, .48]) { box(g, fm, 7.8, .05, .04, 0, y, -2.9); box(g, fm, .04, .05, 5.8, -3.9, y, 0); box(g, fm, .04, .05, 5.8, 3.9, y, 0);
        for (const sx of [-1, 1]) box(g, fm, 3.2, .05, .04, sx * 2.3, y, 2.9); }
      const c0 = document.createElement('canvas'); c0.width = 512; c0.height = 112; const x0 = c0.getContext('2d');
      x0.fillStyle = '#f4e3c0'; x0.fillRect(0, 0, 512, 112); x0.fillStyle = '#3f7a2e'; x0.font = '700 62px "Pixelify Sans", sans-serif'; x0.textAlign = 'center'; x0.textBaseline = 'middle'; x0.fillText('LADANG BUAH', 256, 60, 490);
      const t0 = new THREE.CanvasTexture(c0); t0.colorSpace = THREE.SRGBColorSpace;
      for (const x of [-.75, .75]) box(g, '#6b4a2b', .1, 1.6, .1, x, .06, 2.95);
      const arch = new THREE.Mesh(new THREE.PlaneGeometry(1.6, .35), new THREE.MeshStandardMaterial({ map: t0, roughness: .8 })); arch.position.set(0, 1.5, 3.02); g.add(arch);
      box(g, '#6b4a2b', 1.7, .42, .05, 0, 1.29, 2.97);
      // mango trees (back left) and banana plants (back right)
      for (const [x, z] of [[-3.2, -2.2], [-1.9, -2.3], [-.6, -2.2]]) {
        add(g, G.cyl6, '#6b4a2b', .1, 1.1, .1, x, .6, z);
        add(g, G.dode, '#3f8a3a', .75, .6, .75, x, 1.45, z); add(g, G.dode, '#4f9b45', .5, .45, .5, x + .3, 1.75, z + .1);
        for (let i = 0; i < 6; i++) add(g, G.sph, i % 2 ? '#f0a030' : '#e8c040', .09, .12, .09, x + Math.cos(i * 1.1) * .55, 1.15 + (i % 3) * .2, z + Math.sin(i * 1.1) * .5);
      }
      for (const [x, z] of [[1.0, -2.3], [2.2, -2.2], [3.3, -2.3]]) {
        add(g, G.cyl6, '#7a9a3a', .09, 1.0, .09, x, .55, z);
        for (let i = 0; i < 5; i++) { const l = add(g, G.box, '#4fa040', .9, .03, .26, x + Math.cos(i * 1.26) * .42, 1.1, z + Math.sin(i * 1.26) * .42); l.rotation.y = -i * 1.26; l.rotation.z = .35; }
        for (let i = 0; i < 4; i++) add(g, G.cyl6, '#ffd84a', .045, .22, .045, x + .12 + (i % 2) * .07, .82 - Math.floor(i / 2) * .12, z + .12 + (i % 2) * .05);
      }
      // watermelon patch (front left of the middle)
      box(g, '#6e4f2e', 3.0, .08, 1.7, -2.2, .06, -.1);
      for (let i = 0; i < 9; i++) { const x = -3.3 + (i % 3) * 1.05 + (i % 2) * .15, z = -.6 + Math.floor(i / 3) * .55;
        add(g, G.sph, '#2f7a32', .2, .16, .25, x, .26, z).rotation.y = i; add(g, G.box, '#57b04a', .35, .02, .12, x - .2, .16, z + .12).rotation.y = i * .7; }
      // scarecrow
      const sc = new THREE.Group(); sc.position.set(-.35, .06, 1.3); g.add(sc);
      box(sc, '#6b4a2b', .06, 1.3, .06, 0, 0, 0); box(sc, '#6b4a2b', .9, .05, .05, 0, .95, 0);
      box(sc, '#c4473a', .4, .45, .22, 0, .65, 0); add(sc, G.sph, '#e8d6a0', .17, .17, .17, 0, 1.25, 0);
      add(sc, G.cone6, '#d8b04a', .32, .22, .32, 0, 1.45, 0); box(sc, '#e8c87a', .12, .2, .06, -.45, .78, 0); box(sc, '#e8c87a', .12, .2, .06, .45, .78, 0);
      // the visitors' beds (plants are added at runtime by kebun.js)
      for (const [x, z] of BT.ladang.plots) { box(g, '#5a3d22', .85, .12, .85, x, .06, z); box(g, '#6e4f2e', .7, .04, .7, x, .18, z); }
      const c1 = document.createElement('canvas'); c1.width = 384; c1.height = 96; const x1 = c1.getContext('2d');
      x1.fillStyle = '#fff4dc'; x1.fillRect(0, 0, 384, 96); x1.fillStyle = '#3f7a2e'; x1.font = '700 50px "Pixelify Sans", sans-serif'; x1.textAlign = 'center'; x1.textBaseline = 'middle'; x1.fillText('KEBUN WARGA', 192, 50, 370);
      const t1 = new THREE.CanvasTexture(c1); t1.colorSpace = THREE.SRGBColorSpace;
      box(g, '#6b4a2b', .06, .8, .06, 2.0, .06, 1.6);
      const s1 = new THREE.Mesh(new THREE.PlaneGeometry(.9, .23), new THREE.MeshStandardMaterial({ map: t1, roughness: .8 })); s1.position.set(2.0, .85, 1.64); g.add(s1);
      // seed kiosk (front left)
      const k = new THREE.Group(); k.position.set(-2.6, .06, 1.9); g.add(k);
      box(k, '#8a5a34', 1.1, .5, .45, 0, 0, 0); for (const x of [-.5, .5]) box(k, '#6b4a2b', .06, 1.2, .06, x, 0, -.2);
      box(k, '#57b04a', 1.25, .06, .7, 0, 1.2, -.05);
      const seedC = ['#d0483a', '#f2c94c', '#2f8a3a', '#ffd84a', '#f0a030'];
      for (let i = 0; i < 5; i++) box(k, seedC[i], .14, .14, .16, -.4 + i * .2, .5, .05);
      const c2 = document.createElement('canvas'); c2.width = 256; c2.height = 80; const x2 = c2.getContext('2d');
      x2.fillStyle = '#57b04a'; x2.fillRect(0, 0, 256, 80); x2.fillStyle = '#ffffff'; x2.font = '700 48px "Pixelify Sans", sans-serif'; x2.textAlign = 'center'; x2.textBaseline = 'middle'; x2.fillText('BIBIT', 128, 42);
      const t2 = new THREE.CanvasTexture(c2); t2.colorSpace = THREE.SRGBColorSpace;
      const s2 = new THREE.Mesh(new THREE.PlaneGeometry(.8, .25), new THREE.MeshStandardMaterial({ map: t2, roughness: .8 })); s2.position.set(0, 1.0, .25); k.add(s2);
    } },
  // a school sports field, "paket lengkap": flag pole, goals, a small library and a swing (ep 11, usulan @by5m4)
  lapangansekolah: { n: 'Lapangan Sekolah', w: 5, h: 4, land: true,
    build(g) {
      box(g, '#6fbf5a', 4.9, .05, 3.9, 0, 0, 0);
      for (const [w, d, x, z] of [[4.4, .04, 0, -1.5], [4.4, .04, 0, 1.5], [.04, 3.0, -2.2, 0], [.04, 3.0, 2.2, 0], [.04, 3.0, 0, 0]]) box(g, '#f7f7f3', w, .01, d, x, .05, z);
      for (const sx of [-1, 1]) { const x = sx * 2.15; box(g, '#f7f7f3', .05, .7, .05, x, .05, -.5); box(g, '#f7f7f3', .05, .7, .05, x, .05, .5); box(g, '#f7f7f3', .05, .05, 1.05, x, .73, 0); }
      // flag pole with red-white flag
      add(g, G.cyl6, '#d8dad6', .035, 3.0, .035, -1.0, 1.55, -1.75); box(g, '#cfc8b6', .5, .12, .5, -1.0, .05, -1.75);
      box(g, '#d0483a', .6, .2, .02, -.68, 2.75, -1.75); box(g, '#f7f7f3', .6, .2, .02, -.68, 2.55, -1.75);
      // small library
      const lb = new THREE.Group(); lb.position.set(1.2, .05, -1.45); g.add(lb);
      box(lb, '#e7d7b0', 1.4, .9, .8, 0, 0, 0); roof4(lb, '#4e7a9a', 1.7, .45, 1.1, 0, .9, 0);
      box(lb, '#5e3b22', .35, .6, .04, 0, 0, .41); for (const x of [-.45, .45]) box(lb, windowMat, .25, .25, .04, x, .45, .41);
      const c = document.createElement('canvas'); c.width = 384; c.height = 80; const x = c.getContext('2d');
      x.fillStyle = '#ffffff'; x.fillRect(0, 0, 384, 80); x.fillStyle = '#4e7a9a'; x.font = '700 46px "Pixelify Sans", sans-serif'; x.textAlign = 'center'; x.textBaseline = 'middle'; x.fillText('PERPUSTAKAAN', 192, 42, 370);
      const tx = new THREE.CanvasTexture(c); tx.colorSpace = THREE.SRGBColorSpace;
      const s = new THREE.Mesh(new THREE.PlaneGeometry(1.1, .23), new THREE.MeshStandardMaterial({ map: tx, roughness: .8 })); s.position.set(0, .8, .43); lb.add(s);
      // swing
      const sw = new THREE.Group(); sw.position.set(-1.6, .05, 1.65); g.add(sw);
      for (const x of [-.45, .45]) { const a = box(sw, '#d0483a', .06, 1.2, .06, x, 0, -.15); a.rotation.x = .15; const b = box(sw, '#d0483a', .06, 1.2, .06, x, 0, .15); b.rotation.x = -.15; }
      box(sw, '#d0483a', 1.0, .06, .06, 0, 1.15, 0);
      for (const x of [-.2, .2]) { box(sw, '#9a9b94', .02, .8, .02, x - .08, .37, 0); box(sw, '#9a9b94', .02, .8, .02, x + .08, .37, 0); box(sw, '#e6b84a', .25, .04, .15, x, .35, 0); }
    } },
  // beach guard post: a small police post with a blue light and a lifeguard tower facing the sea (ep 11, penjaga @RANUUGLL)
  pospantai: { n: 'Pos Penjaga Pantai', w: 6, h: 4, scale: 1.5, land: true,
    build(g, b) {
      box(g, '#d9cfb4', 3.9, .08, 2.1, -.45, 0, -.05);
      // police post (left), built at its old size and scaled up so its door is taller than a person
      const pg = new THREE.Group(); pg.position.set(-1.45 + .75 * 1.7, .08 - .08 * 1.7, -.35 + .35 * 1.7); pg.scale.setScalar(1.7); g.add(pg);
      box(pg, '#f4f4f0', 1.2, 1.15, 1.0, -.75, .08, -.35); box(pg, '#2c4f86', 1.25, .12, 1.05, -.75, .65, -.35); box(pg, '#2c4f86', 1.35, .1, 1.15, -.75, 1.23, -.35);
      box(pg, windowMat, .5, .35, .04, -.95, .55, .16); box(pg, '#3b3b3b', .3, .75, .04, -.35, .08, .16);
      const lt = new THREE.MeshStandardMaterial({ color: '#4aa8ff', emissive: '#2a7fff', emissiveIntensity: 1.6 }); add(pg, G.box, lt, .22, .12, .14, -.75, 1.4, -.35);
      const c = document.createElement('canvas'); c.width = 256; c.height = 72; const x = c.getContext('2d');
      x.fillStyle = '#2c4f86'; x.fillRect(0, 0, 256, 72); x.fillStyle = '#ffffff'; x.font = '700 46px "Pixelify Sans", sans-serif'; x.textAlign = 'center'; x.textBaseline = 'middle'; x.fillText('POLISI', 128, 38);
      const tx = new THREE.CanvasTexture(c); tx.colorSpace = THREE.SRGBColorSpace;
      const s = new THREE.Mesh(new THREE.PlaneGeometry(.75, .21), new THREE.MeshStandardMaterial({ map: tx, roughness: .8 })); s.position.set(-.75, 1.02, .17); pg.add(s);
      // lifeguard tower (right): red and white, ladder in front, flag on top
      for (const [px, pz] of [[.65, -.6], [1.25, -.6], [.65, 0], [1.25, 0]]) box(g, '#f4f4f0', .08, 1.4, .08, px, .08, pz);
      box(g, '#d0483a', .9, .08, .9, .95, 1.48, -.3); for (const px of [.52, 1.38]) box(g, '#f4f4f0', .05, .35, .9, px, 1.56, -.3); box(g, '#f4f4f0', .9, .35, .05, .95, 1.56, -.73);
      for (const [px, pz] of [[.55, -.72], [1.35, -.72], [.55, .12], [1.35, .12]]) box(g, '#d0483a', .04, 1.65, .04, px, 1.56, pz);
      roof4(g, '#d0483a', 1.15, .3, 1.15, .95, 3.21, -.3);
      for (let i = 0; i < 6; i++) box(g, '#c9c2b0', .4, .04, .05, .95, .25 + i * .22, .25 + i * .0);
      for (const px of [.77, 1.13]) box(g, '#c9c2b0', .04, 1.45, .04, px, .08, .25);
      add(g, G.cyl6, '#d8dad6', .02, .7, .02, 1.35, 3.7, -.7); box(g, '#ffd23f', .32, .2, .02, 1.53, 3.85, -.7);
      const rb = new THREE.Mesh(new THREE.TorusGeometry(.17, .06, 6, 12), mat('#ff7a2a')); rb.position.set(1.32, .75, .05); g.add(rb);
      // name board: the guard on duty
      const name = (b && b.label) || 'Penjaga Pantai';
      const c2 = document.createElement('canvas'); c2.width = 384; c2.height = 72; const x2 = c2.getContext('2d');
      x2.fillStyle = '#ffd23f'; x2.fillRect(0, 0, 384, 72); x2.fillStyle = '#1c1c24'; x2.font = '700 36px "Pixelify Sans", sans-serif'; x2.textAlign = 'center'; x2.textBaseline = 'middle'; x2.fillText(name, 192, 38, 370);
      const t2 = new THREE.CanvasTexture(c2); t2.colorSpace = THREE.SRGBColorSpace;
      const s2 = new THREE.Mesh(new THREE.PlaneGeometry(.95, .18), new THREE.MeshStandardMaterial({ map: t2, roughness: .8 })); s2.position.set(.95, 1.45, .17); g.add(s2);
    } },
  // a welcome gate over the main street where it meets the pier (ep 12, the day Aru sailed home). Front (to the pier):
  // "Selamat datang"; back (to town): the wish of an anonymous supporter's traktiran, "semoga selalu baik-baik saja"
  gapura: { n: 'Gapura Selamat Datang', w: 4, h: 1, land: true, arch: true,
    build(g, b) {
      const sign = (t1, t2, bg, fg) => { const c = document.createElement('canvas'); c.width = 1024; c.height = 192; const x = c.getContext('2d');
        x.fillStyle = bg; x.fillRect(0, 0, 1024, 192); x.fillStyle = '#e6b84a'; x.fillRect(0, 0, 1024, 12); x.fillRect(0, 180, 1024, 12);
        x.textAlign = 'center'; x.textBaseline = 'middle'; x.fillStyle = fg; x.font = '700 78px "Pixelify Sans", sans-serif'; x.fillText(t1, 512, 76, 980);
        x.font = '700 40px "Pixelify Sans", sans-serif'; x.fillStyle = '#ffe9a8'; x.fillText(t2, 512, 148, 980);
        const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 4; return new THREE.MeshStandardMaterial({ map: t, roughness: .8 }); };
      for (const s of [-1, 1]) {
        const px = s * 1.62;
        box(g, '#8d8a80', .7, .25, .62, px, 0, 0);
        for (let i = 0; i < 5; i++) box(g, i % 2 ? '#f4eee0' : '#c4473a', .5 - i * .01, .62, .46, px, .25 + i * .62, 0);
        box(g, '#8d8a80', .64, .16, .58, px, 3.35, 0);
        roof4(g, '#c4473a', .66, .55, .66, px, 3.51, 0); add(g, G.sph, '#e6b84a', .08, .08, .08, px, 4.1, 0);
        const l = new THREE.Mesh(G.sph, lanternMat); l.scale.set(.14, .18, .14); l.position.set(px - s * .38, 2.35, .32); g.add(l);
        box(g, '#2b1a10', .02, .3, .02, px - s * .38, 2.5, .32);
        // umbul-umbul: a tall bamboo pole with a long curved banner
        const ux = s * 2.2; add(g, G.cyl6, '#c9a35a', .035, 4.6, .035, ux, 2.3, -.1);
        for (let k = 0; k < 6; k++) { const f = box(g, k % 2 ? '#f4eee0' : '#d0483a', .02, .42, .26, ux + s * .03, 3.9 - k * .38, -.1 - k * k * .012); f.rotation.x = -.05 * k; }
      }
      box(g, '#5e3b22', 3.95, .72, .3, 0, 2.62, 0);
      box(g, '#c4473a', 4.15, .12, .42, 0, 3.34, 0);
      const front = new THREE.Mesh(new THREE.PlaneGeometry(2.75, .55), sign('SELAMAT DATANG', 'di Pulau Aru · Pulau Netizen', '#2f6a48', '#ffffff')); front.position.set(0, 2.98, .16); g.add(front);
      const back = new THREE.Mesh(new THREE.PlaneGeometry(2.75, .55), sign('SEMOGA SELALU', 'baik-baik saja · dari dermawan pulau', '#2c4f86', '#ffffff')); back.position.set(0, 2.98, -.16); back.rotation.y = Math.PI; g.add(back);
      for (let i = 0; i < 7; i++) { const l = new THREE.Mesh(G.sph, lanternMat); l.scale.setScalar(.06); l.position.set(-1.2 + i * .4, 2.5, .17); g.add(l); }
    } },
  // a signpost by the pier with arrows to faraway places (ep 12, traktiran adis "salam dari Bogor"): Bogor points out to sea
  tiangsalam: { n: 'Tiang Salam', w: 1, h: 1, land: true,
    build(g) {
      const arrow = (t1, t2, bg, y, ry, len = 1.15) => {
        const tex = flip => { const c = document.createElement('canvas'); c.width = 512; c.height = 128; const x = c.getContext('2d');
          x.save(); if (flip) { x.translate(512, 0); x.scale(-1, 1); }
          x.fillStyle = bg; x.beginPath(); x.moveTo(0, 6); x.lineTo(440, 6); x.lineTo(506, 64); x.lineTo(440, 122); x.lineTo(0, 122); x.closePath(); x.fill(); x.restore();
          const cx = flip ? 287 : 225; x.fillStyle = '#fff8e6'; x.textAlign = 'center'; x.textBaseline = 'middle'; x.font = '700 50px "Pixelify Sans", sans-serif'; x.fillText(t1, cx, t2 ? 48 : 66, 420);
          if (t2) { x.font = '700 28px "Pixelify Sans", sans-serif'; x.fillText(t2, cx, 98, 420); }
          const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; return new THREE.MeshStandardMaterial({ map: t, roughness: .8, transparent: true, alphaTest: .5 }); };
        const p = new THREE.Group(); p.position.y = y; p.rotation.y = ry; g.add(p);
        const geo = new THREE.PlaneGeometry(len, len / 4);
        const a = new THREE.Mesh(geo, tex(false)); a.position.set(len / 2 - .05, 0, .012); p.add(a);
        const b = new THREE.Mesh(geo, tex(true)); b.position.set(len / 2 - .05, 0, -.012); b.rotation.y = Math.PI; p.add(b);
      };
      box(g, '#6b6b66', .3, .14, .3, 0, 0, 0); box(g, '#f4eee0', .1, 2.9, .1, 0, .14, 0);
      add(g, G.sph, '#d0483a', .1, .1, .1, 0, 3.1, 0);
      arrow('BOGOR', 'salam dari adis!', '#2f6a48', 2.75, -Math.PI / 2 - .25);
      arrow('PULAU SEBERANG', 'ikuti matahari terbit', '#2c4f86', 2.35, .55);
      arrow('PASAR', '', '#c4473a', 1.95, Math.PI / 2 - .2, .9);
      arrow('PANGGUNG', '', '#a0703a', 1.6, Math.PI / 2 + .25, .9);
    } },
  // a small business stall for a real UMKM chosen from the comments (#UMKMPulauAru): the sign shows b.label,
  // the awning colour comes from the name, and tapping it opens the business link (b.link) after a confirmation sheet
  // a small coffee house on the cross street, from Kak Alfi's traktiran "selamat menikmati kopinya" (ep 10)
  kedaikopi: { n: 'Kedai Kopi', w: 3, h: 2, land: true, scale: 1.2,
    build(g) {
      box(g, '#b9a88a', 2.9, .1, 1.9, 0, 0, 0);
      box(g, '#6b4a30', 1.9, 1.65, .1, -.45, .1, -.8); box(g, '#5a3c26', .1, 1.65, 1.2, -1.36, .1, -.25); box(g, '#5a3c26', .1, 1.65, 1.2, .46, .1, -.25);
      for (const [x, z] of [[-1.38, .72], [.48, .72]]) box(g, '#3a2618', .08, 1.8, .08, x, .1, z);
      box(g, '#2f2a26', 2.0, .08, 1.7, -.45, 1.75, -.05);                                                   // dark roof
      for (let i = 0; i < 7; i++) { const a = box(g, i % 2 ? '#f2e6d0' : '#7a4a2a', .29, .05, .48, -1.32 + i * .29, 1.68, .86); a.rotation.x = .38; }
      box(g, '#7a5232', 1.6, .64, .42, -.45, .1, .28); box(g, '#e8d8bc', 1.62, .06, .44, -.45, .74, .28);      // bar counter
      box(g, '#9a9b94', .34, .36, .28, -1.0, .8, .25); box(g, '#2b2b2b', .08, .1, .08, -1.0, .78, .42);       // espresso machine
      for (let i = 0; i < 4; i++) { add(g, G.cyl8, '#f4eee0', .055, .1, .055, -.6 + i * .2, .85, .32); add(g, G.cyl8, '#4a2a16', .045, .01, .045, -.6 + i * .2, .9, .32, 0, false); }
      box(g, '#5a3c26', 1.5, .05, .25, -.45, 1.15, -.65); for (let i = 0; i < 6; i++) add(g, G.cyl8, ['#c98a3a', '#3a2618', '#e8d8bc'][i % 3], .07, .16, .07, -1.05 + i * .24, 1.28, -.65);
      box(g, '#c2a476', .38, .42, .3, .2, .1, -.5); box(g, '#a88a5c', .36, .1, .28, .2, .52, -.5);           // coffee sack
      // outdoor table with two stools on the right
      add(g, G.cyl8, '#5a3c26', .05, .55, .05, .95, .38, .25); add(g, G.cyl8, '#8a5a34', .32, .04, .32, .95, .66, .25);
      add(g, G.cyl8, '#f4eee0', .05, .08, .05, .9, .72, .2); add(g, G.cyl8, '#f4eee0', .05, .08, .05, 1.05, .72, .32);
      for (const dx of [-.42, .42]) { add(g, G.cyl8, '#3a2618', .04, .32, .04, .95 + dx, .26, .25); add(g, G.cyl8, '#7a4a2a', .14, .04, .14, .95 + dx, .44, .25); }
      const c = document.createElement('canvas'); c.width = 512; c.height = 160; const x = c.getContext('2d');
      x.fillStyle = '#2f2a26'; x.fillRect(0, 0, 512, 160); x.fillStyle = '#c98a3a'; x.fillRect(0, 0, 512, 10); x.fillRect(0, 150, 512, 10);
      x.textAlign = 'center'; x.textBaseline = 'middle'; x.fillStyle = '#f2e6d0'; x.font = '700 62px "Pixelify Sans", sans-serif'; x.fillText('KEDAI KOPI', 256, 62, 490);
      x.fillStyle = '#e6b84a'; x.font = '700 28px "Pixelify Sans", sans-serif'; x.fillText('selamat menikmati kopinya', 256, 120, 490);
      const tx = new THREE.CanvasTexture(c); tx.colorSpace = THREE.SRGBColorSpace;
      const sign = new THREE.Mesh(new THREE.PlaneGeometry(1.8, .56), new THREE.MeshStandardMaterial({ map: tx, roughness: .8 })); sign.position.set(-.45, 2.09, .56); g.add(sign);
      box(g, '#3a2618', 1.86, .62, .04, -.45, 1.78, .53);
      const lamp = new THREE.Mesh(G.sph, lanternMat); lamp.scale.set(.09, .12, .09); lamp.position.set(.4, 1.45, .8); g.add(lamp);
    } },
  // a night-watch hut ("pos ronda") with a kentongan, from the traktiran "warga saling jaga" (ep 10)
  posronda: { n: 'Pos Ronda', w: 2, h: 2, land: true,
    build(g) {
      for (const [x, z] of [[-.8, -.7], [.8, -.7], [-.8, .7], [.8, .7]]) box(g, '#5e3b22', .1, 2.2, .1, x, 0, z);
      box(g, '#a8844e', 1.7, .08, 1.5, 0, .45, 0);                                                          // bamboo platform
      for (let i = 0; i < 9; i++) box(g, i % 2 ? '#c9a868' : '#b8955a', .17, .02, 1.48, -.76 + i * .19, .53, 0, 0);
      box(g, '#8a6a3a', 1.7, .35, .06, 0, .55, -.72);                                                       // back rail
      roof4(g, '#8c6a3a', 2.4, .75, 2.1, 0, 2.2, 0);                                                       // thatched roof
      add(g, G.cone4, '#a07c46', 2.25 * .72, .1, 1.95 * .72, 0, 2.23, 0, Math.PI / 4);
      // kentongan: a hollow log hanging from the front-right post, with a mallet
      const k = add(g, G.cyl8, '#7a4a28', .09, .55, .09, .92, 1.15, .72); add(g, G.box, '#2b1a10', .02, .3, .05, .92, 1.15, .81);
      box(g, '#3a2618', .02, .14, .02, .92, 1.42, .72);
      const m = add(g, G.cyl6, '#5e3b22', .025, .35, .025, .7, .8, .78); m.rotation.z = .5;
      // on the platform: a thermos, two cups, a checkers board and a sarong
      add(g, G.cyl8, '#d0483a', .07, .26, .07, -.5, .66, -.35); add(g, G.cyl8, '#f4eee0', .04, .07, .04, -.32, .58, -.3); add(g, G.cyl8, '#f4eee0', .04, .07, .04, -.22, .58, -.4);
      box(g, '#e8dcc4', .36, .02, .36, .25, .55, -.1); for (let i = 0; i < 6; i++) add(g, G.cyl8, i % 2 ? '#d0483a' : '#2b2b2b', .03, .02, .03, .13 + (i % 3) * .12, .58, -.2 + (i >> 1) * .1, 0, false);
      box(g, '#4e7a9a', .5, .05, .3, .45, .55, .35);
      const lamp = new THREE.Mesh(G.sph, lanternMat); lamp.scale.set(.09, .12, .09); lamp.position.set(0, 2.0, .3); g.add(lamp);
      box(g, '#3a2618', .02, .2, .02, 0, 2.07, .3);
      const c = document.createElement('canvas'); c.width = 512; c.height = 160; const x = c.getContext('2d');
      x.fillStyle = '#fff4dc'; x.fillRect(0, 0, 512, 160); x.fillStyle = '#d0483a'; x.fillRect(0, 0, 512, 10); x.fillRect(0, 150, 512, 10);
      x.textAlign = 'center'; x.textBaseline = 'middle'; x.fillStyle = '#5e3b22'; x.font = '700 64px "Pixelify Sans", sans-serif'; x.fillText('POS RONDA', 256, 62, 490);
      x.fillStyle = '#d0483a'; x.font = '700 32px "Pixelify Sans", sans-serif'; x.fillText('warga saling jaga', 256, 120, 490);
      const tx = new THREE.CanvasTexture(c); tx.colorSpace = THREE.SRGBColorSpace;
      const sign = new THREE.Mesh(new THREE.PlaneGeometry(1.3, .4), new THREE.MeshStandardMaterial({ map: tx, roughness: .8 })); sign.position.set(0, 1.98, .78); g.add(sign);
    } },
  // a small eatery with a long table and benches where visitors can sit and order (ep 13, usulan @FAHMI "pengen nge warung").
  // seats: [x, y, z, face] in unscaled local metres (y = seat top); face 0 looks +z (toward the street)
  warungfahmi: { n: 'Warung Fahmi', w: 4, h: 3, land: true, scale: 1.5, open: 'warung', openLabel: 'Duduk & pesan makan',
    seats: [[-.62, .4, -.1, 0], [0, .4, -.1, 0], [.62, .4, -.1, 0], [-.62, .4, .72, Math.PI], [0, .4, .72, Math.PI], [.62, .4, .72, Math.PI]], table: [.58, .27],
    build(g) {
      box(g, '#c9bfa8', 2.6, .1, 1.9, 0, 0, 0);
      box(g, '#e8c48a', 2.5, 1.75, .1, 0, .1, -.88); box(g, '#d9b277', .1, 1.75, .9, -1.22, .1, -.45); box(g, '#d9b277', .1, 1.75, .9, 1.22, .1, -.45);
      for (const [x, z] of [[-1.22, .86], [1.22, .86]]) box(g, '#5e3b22', .09, 1.75, .09, x, .1, z);
      box(g, '#b8523c', 2.7, .1, 2.0, 0, 1.85, -.02);                                                     // roof
      for (let i = 0; i < 9; i++) { const a = box(g, i % 2 ? '#fff4dc' : '#d0483a', .3, .05, .5, -1.2 + i * .3, 1.78, .95); a.rotation.x = .38; }
      // kitchen along the back: stove, wok, pots, a glass food display
      box(g, '#8a5a34', 2.2, .6, .4, 0, .1, -.6); box(g, '#f4eee0', 2.22, .05, .42, 0, .7, -.6);
      box(g, '#5a5a58', .5, .12, .3, -.7, .75, -.6); add(g, G.cyl8, '#2b2b2b', .17, .05, .17, -.8, .9, -.6); add(g, G.cyl8, '#9a9b94', .1, .14, .1, -.5, .94, -.62);
      const glass = box(g, '#cfe8ee', .8, .32, .32, .5, .75, -.6); glass.material = new THREE.MeshStandardMaterial({ color: '#cfe8ee', transparent: true, opacity: .5 });
      const food = ['#e0a84a', '#c4473a', '#f2e6c8', '#62bd73', '#d99a3e'];
      for (let i = 0; i < 5; i++) add(g, G.cyl8, food[i], .07, .05, .07, .22 + i * .14, .82, -.6);
      box(g, '#8a5a34', 1.6, .05, .2, 0, 1.25, -.8); for (let i = 0; i < 6; i++) add(g, G.cyl8, ['#d0483a', '#f2c94c', '#3f7f5a'][i % 3], .05, .16, .05, -.6 + i * .24, 1.3, -.8);
      // long table with two benches
      box(g, '#a8763e', 2.0, .05, .44, 0, .52, .32); for (const x of [-.9, .9]) for (const z of [.15, .49]) box(g, '#5e3b22', .05, .42, .05, x, .1, z);
      box(g, '#f0e6d0', 1.9, .01, .3, 0, .57, .32);
      for (const z of [-.1, .72]) { box(g, '#7a4a28', 2.0, .05, .2, 0, .35, z); for (const x of [-.85, .85]) box(g, '#5e3b22', .05, .25, .05, x, .1, z); }
      for (let i = 0; i < 3; i++) { add(g, G.cyl8, '#c0702a', .035, .1, .035, -.62 + i * .62, .6, .44); add(g, G.cyl8, '#e8e2d4', .03, .06, .03, -.45 + i * .62, .6, .2); }  // tea glasses, sambal
      const c = document.createElement('canvas'); c.width = 512; c.height = 160; const x = c.getContext('2d');
      x.fillStyle = '#fff4dc'; x.fillRect(0, 0, 512, 160); x.fillStyle = '#d0483a'; x.fillRect(0, 0, 512, 12); x.fillRect(0, 148, 512, 12);
      x.textAlign = 'center'; x.textBaseline = 'middle'; x.fillStyle = '#b8523c'; x.font = '700 66px "Pixelify Sans", sans-serif'; x.fillText('WARUNG FAHMI', 256, 64, 490);
      x.fillStyle = '#5e3b22'; x.font = '700 28px "Pixelify Sans", sans-serif'; x.fillText('duduk · pesan · makan', 256, 122, 490);
      const tx = new THREE.CanvasTexture(c); tx.colorSpace = THREE.SRGBColorSpace;
      const sign = new THREE.Mesh(new THREE.PlaneGeometry(1.8, .56), new THREE.MeshStandardMaterial({ map: tx, roughness: .8 })); sign.position.set(0, 2.23, 1.0); g.add(sign);
      box(g, '#5e3b22', 1.86, .62, .04, 0, 1.92, .97);
      const lamp = new THREE.Mesh(G.sph, lanternMat); lamp.scale.set(.08, .11, .08); lamp.position.set(0, 1.62, .35); g.add(lamp);
    } },
  // the island office where visitors take a shift and earn coins (ep 13, usulan wapres @EGA_91 "kantor untuk nyari uang")
  kantor: { n: 'Kantor Pulau', w: 4, h: 3, land: true, scale: 1.6, open: 'kantor', openLabel: 'Kerja di kantor',
    seats: [[-.68, .36, .18, 0], [.68, .36, .18, 0]], table: [.54, .3],
    build(g) {
      box(g, '#bdbab2', 2.4, .08, 1.8, 0, 0, 0);
      box(g, '#eef0f2', 2.3, 2.1, .85, 0, .08, -.45);                                                     // two-storey block
      box(g, '#3f6f9a', 2.32, .12, .87, 0, 1.12, -.45); box(g, '#d8dadc', 2.4, .12, .95, 0, 2.18, -.45);
      for (const xx of [-.8, -.27, .27, .8]) { box(g, windowMat, .36, .42, .02, xx, 1.45, -.02); }
      box(g, '#2e3a46', .45, 1.0, .03, 0, .08, -.01); box(g, '#cfe0ec', .36, .82, .02, 0, .14, .01);         // glass door, taller than a person
      for (const xx of [-.8, .8]) box(g, windowMat, .5, .5, .02, xx, .45, -.02);
      // porch with canopy and two work desks facing the street
      box(g, '#3f6f9a', 2.4, .06, .9, 0, 1.06, .4); for (const xx of [-1.12, 1.12]) box(g, '#d8dadc', .07, 1.0, .07, xx, .06, .8);
      for (const xx of [-.68, .68]) {
        box(g, '#8a6a4a', .7, .04, .32, xx, .48, .5); box(g, '#5e3b22', .04, .4, .3, xx - .32, .08, .5); box(g, '#5e3b22', .04, .4, .3, xx + .32, .08, .5);
        box(g, '#2b2b2b', .3, .02, .2, xx, .52, .48); const scr = box(g, '#2b2b2b', .3, .15, .02, xx, .53, .4); scr.rotation.x = -.25;    // laptop
        box(g, '#f4eee0', .16, .03, .2, xx + .22, .52, .5);                                                   // papers
        box(g, '#3a4a6b', .3, .04, .28, xx, .3, .18); box(g, '#3a4a6b', .3, .32, .04, xx, .34, .03); add(g, G.cyl6, '#2b2b2b', .03, .24, .03, xx, .06, .18);  // chair
      }
      const c = document.createElement('canvas'); c.width = 512; c.height = 160; const x = c.getContext('2d');
      x.fillStyle = '#3f6f9a'; x.fillRect(0, 0, 512, 160); x.fillStyle = '#e6b84a'; x.fillRect(0, 148, 512, 12);
      x.textAlign = 'center'; x.textBaseline = 'middle'; x.fillStyle = '#ffffff'; x.font = '700 66px "Pixelify Sans", sans-serif'; x.fillText('KANTOR PULAU', 256, 62, 490);
      x.fillStyle = '#e6b84a'; x.font = '700 28px "Pixelify Sans", sans-serif'; x.fillText('kerja jujur, dapat koin', 256, 122, 490);
      const tx = new THREE.CanvasTexture(c); tx.colorSpace = THREE.SRGBColorSpace;
      const sign = new THREE.Mesh(new THREE.PlaneGeometry(1.5, .46), new THREE.MeshStandardMaterial({ map: tx, roughness: .8 })); sign.position.set(0, 1.85, .01); g.add(sign);
      add(g, G.cyl6, '#9a9b94', .025, 1.0, .025, 1.0, 2.24 + .5, -.3); const fl = box(g, '#d0483a', .3, .1, .02, 1.15, 2.95, -.3); box(g, '#f4eee0', .3, .1, .02, 1.15, 2.85, -.3);
    } },
  // a red-and-white lattice signal tower with dishes and a beacon, from Sal's 440 traktiran "semoga bisa segera up di
  // playstore dan ios" (ep 14); the board at its foot carries the message, the beacon glows at night
  menarasinyal: { n: 'Menara Sinyal Sal', w: 3, h: 3, land: true, scale: 1.5, clear: 4,   // clears trees 4 cells around (open view from the street)
    build(g) {
      box(g, '#9a9b94', 1.7, .12, 1.7, 0, 0, 0);
      const H = 5.2, seg = 8;
      for (let i = 0; i < seg; i++) {                                                   // tapering legs, red/white bands
        const y0 = .12 + i * H / seg, t0 = .62 - i * .055, t1 = .62 - (i + 1) * .055, col = i % 2 ? '#f4eee0' : '#d0483a';
        for (const [sx, sz] of [[-1, -1], [1, -1], [-1, 1], [1, 1]]) {
          const lg = box(g, col, .07, H / seg + .02, .07, sx * (t0 + t1) / 2, y0, sz * (t0 + t1) / 2); lg.rotation.z = sx * .05; lg.rotation.x = -sz * .05;
        }
        const yy = y0 + H / seg - .02, tt = t1;
        for (const sz of [-1, 1]) { box(g, col, tt * 2 + .06, .04, .04, 0, yy, sz * tt); box(g, col, .04, .04, tt * 2 + .06, sz * tt, yy, 0); }
        for (const sz of [-1, 1]) { const d = box(g, '#c9c9c2', .03, H / seg * 1.25, .03, 0, y0, sz * (t0 + t1) / 2); d.rotation.z = (i % 2 ? 1 : -1) * .9; d.position.y = y0 + H / seg / 2; }
      }
      box(g, '#d8dadc', .5, .06, .5, 0, H + .1, 0);                                        // platform
      add(g, G.cyl6, '#3d4a52', .03, 1.0, .03, 0, H + .65, 0);                            // mast
      const bc = new THREE.Mesh(G.sph, lanternMat); bc.scale.set(.1, .1, .1); bc.position.set(0, H + 1.2, 0); g.add(bc);
      for (const [x, z, ry] of [[.28, 0, Math.PI / 2], [-.28, 0, -Math.PI / 2], [0, .28, 0]]) {     // dishes and panels
        const d = add(g, G.cyl8, '#eef0f2', .17, .05, .17, x, H - .2, z, 0); d.rotation.set(Math.PI / 2, 0, 0); d.rotation.y = ry; d.rotation.order = 'YXZ';
      }
      for (const [x, z] of [[.22, .22], [-.22, .22], [.22, -.22], [-.22, -.22]]) box(g, '#eef0f2', .08, .45, .04, x, H - 1.1, z, Math.atan2(x, z));
      // signal bars on the platform rail
      for (let i = 0; i < 5; i++) box(g, '#5fae6a', .05, .08 + i * .06, .03, -.14 + i * .07, H + .16, .26);
      // board at the foot: name + Sal's message
      const c = document.createElement('canvas'); c.width = 512; c.height = 256; const x = c.getContext('2d');
      x.fillStyle = '#1f2f45'; x.fillRect(0, 0, 512, 256); x.fillStyle = '#e6b84a'; x.fillRect(0, 0, 512, 10); x.fillRect(0, 246, 512, 10);
      x.textAlign = 'center'; x.textBaseline = 'middle'; x.fillStyle = '#ffffff'; x.font = '700 58px "Pixelify Sans", sans-serif'; x.fillText('MENARA SINYAL', 256, 54, 490);
      x.fillStyle = '#e6b84a'; x.font = '700 40px "Pixelify Sans", sans-serif'; x.fillText('dari Kak Sal ♥ 440 traktiran', 256, 112, 490);
      x.fillStyle = '#cfe0ec'; x.font = '700 30px "Pixelify Sans", sans-serif'; x.fillText('"Semoga segera rilis', 256, 168, 490); x.fillText('di Play Store & iOS!"', 256, 208, 490);
      const tx = new THREE.CanvasTexture(c); tx.colorSpace = THREE.SRGBColorSpace;
      for (const xx of [-.42, .42]) box(g, '#3d4a52', .05, .9, .05, xx, .12, .95);
      const bd = new THREE.Mesh(new THREE.PlaneGeometry(1.0, .5), new THREE.MeshStandardMaterial({ map: tx, roughness: .8 })); bd.position.set(0, .82, .98); g.add(bd);
      box(g, '#2b3338', 1.04, .54, .03, 0, .55, .955);
    } },
  // a cloth protest banner between two bamboo poles; the text is b.label (ep 13, demo warga minta pemilu)
  spanduk: { n: 'Spanduk warga', w: 2, h: 1, land: true,
    build(g, b) {
      for (const x of [-.95, .95]) { add(g, G.cyl6, '#c9a868', .04, 2.3, .04, x, 1.15, 0); add(g, G.sph, '#8a6a3a', .05, .05, .05, x, 2.32, 0); }
      const text = (b && b.label) || 'SUARA WARGA';
      const c = document.createElement('canvas'); c.width = 512; c.height = 140; const x = c.getContext('2d');
      x.fillStyle = '#f7f1e3'; x.fillRect(0, 0, 512, 140); x.fillStyle = '#d0483a'; x.fillRect(0, 0, 512, 8); x.fillRect(0, 132, 512, 8);
      let fs = 72; x.font = `700 ${fs}px "Pixelify Sans", sans-serif`; while (fs > 30 && x.measureText(text).width > 480) { fs -= 2; x.font = `700 ${fs}px "Pixelify Sans", sans-serif`; }
      x.fillStyle = '#c0392b'; x.textAlign = 'center'; x.textBaseline = 'middle'; x.fillText(text, 256, 72);
      const tx = new THREE.CanvasTexture(c); tx.colorSpace = THREE.SRGBColorSpace;
      const cloth = new THREE.Mesh(new THREE.PlaneGeometry(1.86, .52), new THREE.MeshStandardMaterial({ map: tx, roughness: .9, side: THREE.DoubleSide })); cloth.position.set(0, 1.85, 0); g.add(cloth);
      for (const y of [1.59, 2.11]) box(g, '#8a6a3a', 1.9, .015, .015, 0, y, 0);
    } },
  // the election board (ep 15): president and vice president resigned, so two empty chairs wait in front of a board
  // listing every candidate from the comments. Candidates from b.cands, rule line from b.label
  papanpemilu: { n: 'Papan Pemilu', w: 3, h: 2, scale: 1.3, land: true,
    build(g, b) {
      const cands = (b && b.cands) || ['Calon dari komentar'];
      box(g, '#c9bfa8', 2.3, .08, 1.5, 0, 0, 0);
      for (const x of [-1.0, 1.0]) box(g, '#5e3b22', .1, 2.2, .1, x, 0, -.5);
      box(g, '#c4473a', 2.2, .14, .14, 0, 2.2, -.5);
      const c = document.createElement('canvas'); c.width = 512; c.height = 400; const x = c.getContext('2d');
      x.fillStyle = '#fff8e6'; x.fillRect(0, 0, 512, 400); x.fillStyle = '#c4473a'; x.fillRect(0, 0, 512, 64); x.fillStyle = '#f4eee0'; x.fillRect(0, 64, 512, 6);
      x.textAlign = 'center'; x.textBaseline = 'middle'; x.fillStyle = '#fff8e6'; x.font = '700 44px "Pixelify Sans", sans-serif'; x.fillText((b && b.head) || 'PEMILU PULAU ARU', 256, 34, 490);
      // ep 16: once the votes are counted, b.win = { pres, vp, note } turns the board into the results board
      const win = b && b.win;
      if (win) {
        x.fillStyle = '#2f8a4a'; x.fillRect(0, 0, 512, 64); x.fillStyle = '#fff8e6'; x.font = '700 44px "Pixelify Sans", sans-serif'; x.fillText('HASIL PEMILU', 256, 34, 490);
        x.fillStyle = '#c4473a'; x.font = '700 22px "Pixelify Sans", sans-serif'; x.fillText('PRESIDEN', 256, 92);
        x.fillStyle = '#3a2412'; x.font = '700 50px "Pixelify Sans", sans-serif'; x.fillText(win.pres, 256, 132, 480);
        x.fillStyle = '#b8862a'; x.font = '700 22px "Pixelify Sans", sans-serif'; x.fillText('WAKIL PRESIDEN', 256, 180);
        x.fillStyle = '#3a2412'; x.font = '700 42px "Pixelify Sans", sans-serif'; x.fillText(win.vp, 256, 216, 480);
        x.font = '700 19px "Pixelify Sans", sans-serif'; x.fillStyle = '#6a5a48'; x.fillText('calon: ' + cands.join(' · '), 256, 262, 496);
        x.font = '700 22px "Pixelify Sans", sans-serif'; x.fillStyle = '#3a2412'; x.fillText(win.note || '', 256, 304, 496);
      } else
      x.fillStyle = '#3a2412', x.font = '700 24px "Pixelify Sans", sans-serif', x.fillText((b && b.sub) || 'CALON PRESIDEN', 256, 92, 490);
      const cols = cands.length > 5 ? 2 : 1, rows = Math.ceil(cands.length / cols), lh = Math.min(42, 210 / rows);
      x.font = `700 ${Math.round(lh * .78)}px "Pixelify Sans", sans-serif`; x.textAlign = 'left';
      if (!win) cands.forEach((n, i) => { const cx = cols === 2 ? 30 + (i % 2) * 245 : 120, cy = 128 + Math.floor(cols === 2 ? i / 2 : i) * lh + lh / 2;
        x.strokeStyle = '#3a2412'; x.lineWidth = 3; x.strokeRect(cx, cy - 11, 22, 22); x.fillStyle = '#3a2412'; x.fillText(n, cx + 32, cy + 1, 200); });
      x.fillStyle = '#e6b84a'; x.fillRect(0, 344, 512, 56); x.fillStyle = '#3a2412'; x.textAlign = 'center'; x.font = '700 24px "Pixelify Sans", sans-serif';
      x.fillText((b && b.label) || 'LIKE TERBANYAK = PRESIDEN · KEDUA = WAPRES', 256, 373, 496);
      const tx = new THREE.CanvasTexture(c); tx.colorSpace = THREE.SRGBColorSpace; tx.anisotropy = 4;
      box(g, '#5e3b22', 2.04, 1.62, .06, 0, .64, -.53);
      const board = new THREE.Mesh(new THREE.PlaneGeometry(1.96, 1.53), new THREE.MeshStandardMaterial({ map: tx, roughness: .8 })); board.position.set(0, 1.45, -.49); g.add(board);
      // two empty chairs with a 'KOSONG' tag: the president's (red cushion) and the vice president's (gold)
      const tag = (text, who) => { const c2 = document.createElement('canvas'); c2.width = 256; c2.height = 96; const y = c2.getContext('2d');
        y.fillStyle = '#f4eee0'; y.fillRect(0, 0, 256, 96); y.strokeStyle = '#3a2412'; y.lineWidth = 6; y.strokeRect(3, 3, 250, 90); y.fillStyle = '#3a2412'; y.textAlign = 'center'; y.textBaseline = 'middle';
        y.font = '700 30px "Pixelify Sans", sans-serif'; y.fillText(text, 128, 30, 236); y.fillStyle = who ? '#2f8a4a' : '#c0392b'; y.font = '700 38px "Pixelify Sans", sans-serif'; y.fillText(who || 'KOSONG', 128, 68, 236);
        const t = new THREE.CanvasTexture(c2); t.colorSpace = THREE.SRGBColorSpace; return new THREE.MeshStandardMaterial({ map: t, roughness: .8 }); };
      for (const [cx, cush, lab] of [[-.5, '#c4473a', 'PRESIDEN'], [.5, '#e6b84a', 'WAPRES']]) {
        for (const [lx, lz] of [[-.17, .18], [.17, .18], [-.17, .52], [.17, .52]]) box(g, '#5e3b22', .05, .42, .05, cx + lx, 0, lz);
        box(g, '#7a4a28', .44, .06, .44, cx, .42, .35); box(g, cush, .4, .06, .4, cx, .48, .35);
        box(g, '#7a4a28', .44, .62, .06, cx, .42, .13); box(g, cush, .36, .46, .03, cx, .5, .17);
        box(g, '#e6b84a', .46, .06, .08, cx, 1.04, .13);
        const t = new THREE.Mesh(new THREE.PlaneGeometry(.34, .13), tag(lab, (win && (lab === 'PRESIDEN' ? win.pres : win.vp)) || (b && b.seats && (lab === 'PRESIDEN' ? b.seats.pres : b.seats.vp)))); t.position.set(cx, .27, .58); g.add(t);
      }
    } },
  // ep 16: a coffee cart run by a resident (komentar @sapta.rajo.ghaisa "wibu cilik pelenger": "aku tukang jualan kopidong").
  // b.label = sign text, b.seller = the resident who always stands behind it (main.js extraSpots → own)
  gerobakkopi: { n: 'Gerobak Kopi', w: 2, h: 2, scale: 1.15, land: true,
    spots: { seller: [0, -.62, 0] },
    build(g, b) {
      const name = (b && b.label) || 'KOPI';
      for (const x of [-.62, .62]) { const w = add(g, G.cyl8, '#3a2a20', .26, .07, .26, x, .26, .05); w.rotation.z = Math.PI / 2; add(g, G.cyl8, '#9a9b94', .08, .08, .08, x, .26, .05).rotation.z = Math.PI / 2; }
      box(g, '#8a5a34', 1.3, .08, .66, 0, .3, 0);                         // base
      box(g, '#c4473a', 1.3, .44, .62, 0, .38, 0);                        // cart body
      box(g, '#f4eee0', 1.34, .06, .66, 0, .82, 0);                       // counter top
      box(g, '#5e3b22', .06, .5, .06, -.7, .5, -.28); const hd = box(g, '#5e3b22', .5, .05, .05, -.95, .95, -.28); hd.rotation.z = .2;   // push handle
      // thermos, cups, a kettle and a jar of sugar on the counter
      add(g, G.cyl8, '#d0483a', .1, .32, .1, -.42, 1.01, -.05); add(g, G.cyl8, '#f4eee0', .11, .04, .11, -.42, 1.18, -.05);
      for (let i = 0; i < 4; i++) add(g, G.cyl8, i % 2 ? '#f4eee0' : '#e6b84a', .055, .1, .055, -.12 + i * .14, .9, .16);
      add(g, G.sph, '#6d6a62', .12, .1, .12, .42, .94, -.08); add(g, G.cyl6, '#6d6a62', .02, .14, .02, .54, .96, -.08).rotation.z = -.9;
      add(g, G.cyl8, '#e8dcc4', .07, .14, .07, .25, .92, -.16);
      // the big umbrella
      add(g, G.cyl6, '#5e3b22', .025, 1.4, .025, .5, 1.6, -.22);
      add(g, G.cone6, '#e6b84a', .95, .32, .95, .5, 2.42, -.22); add(g, G.cone6, '#c4473a', .55, .2, .55, .5, 2.52, -.22);
      // sign on the front
      const c = document.createElement('canvas'); c.width = 512; c.height = 192; const x = c.getContext('2d');
      x.fillStyle = '#fff4dc'; x.fillRect(0, 0, 512, 192); x.fillStyle = '#5e3b22'; x.fillRect(0, 0, 512, 12); x.fillRect(0, 180, 512, 12);
      x.textAlign = 'center'; x.textBaseline = 'middle'; let fs = 92; x.font = `700 ${fs}px "Pixelify Sans", sans-serif`;
      while (fs > 30 && x.measureText(name).width > 480) { fs -= 2; x.font = `700 ${fs}px "Pixelify Sans", sans-serif`; }
      x.fillStyle = '#c4473a'; x.fillText(name, 256, 82); x.fillStyle = '#5e3b22'; x.font = '700 30px "Pixelify Sans", sans-serif'; x.fillText((b && b.sub) || 'kopi hangat buat warga', 256, 152, 490);
      const tx = new THREE.CanvasTexture(c); tx.colorSpace = THREE.SRGBColorSpace; tx.anisotropy = 4;
      const sign = new THREE.Mesh(new THREE.PlaneGeometry(1.2, .4), new THREE.MeshStandardMaterial({ map: tx, roughness: .8 })); sign.position.set(0, .6, .32); g.add(sign);
      // a small stool for customers
      for (const sx of [-.4, .4]) { add(g, G.cyl8, '#8a5a34', .14, .05, .14, sx, .45, .62); add(g, G.cyl6, '#5e3b22', .03, .45, .03, sx, .22, .62); }
    } },
  warungumkm: { n: 'Warung UMKM', w: 3, h: 3, scale: 1.5, land: true,
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
      const steps = new THREE.Group(); g.add(steps);
      L.steps.forEach(([x, z, y], k) => { const st = new THREE.Group(); st.position.set(x, y, z); steps.add(st); puff(st, 0, -.28, 0, .8, 4, k + 1); const top = new THREE.Mesh(G.cyl8, cloudMat); top.scale.set(.78, .14, .78); top.position.y = -.07; top.receiveShadow = true; st.add(top); });
      const isl = new THREE.Group(); isl.position.set(L.island.x, L.island.top, L.island.z); g.add(isl);
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
  // ep 17: the president's suggestion box in front of the stage. Tapping it opens the usulan panel (ui.js openUsulan):
  // old suggestions, what got built, and a button to write a suggestion in the TikTok comments.
  kotakusulan: { n: 'Kotak Usulan', w: 2, h: 1, land: true, scale: 1.2, open: 'usulan', openLabel: 'Baca kotak usulan',
    build(g) {
      box(g, '#8a8578', .7, .08, .5, 0, 0, 0);                                                              // small stone base
      box(g, '#3a3a38', .1, .78, .1, 0, .08, 0);                                                            // post
      box(g, '#c4473a', .62, .5, .44, 0, .86, 0);                                                           // the box
      box(g, '#a63a2f', .68, .06, .5, 0, 1.36, 0); box(g, '#a63a2f', .56, .06, .38, 0, 1.42, 0);           // lid
      box(g, '#1d1d1b', .34, .035, .03, 0, 1.2, .225);                                                      // letter slot
      box(g, '#e6b84a', .08, .08, .03, .2, .95, .225);                                                      // little lock
      // letters sticking out of the slot
      for (let i = 0; i < 3; i++) { const l = box(g, ['#fff4dc', '#f4eee0', '#e8dcc4'][i], .18, .12, .01, -.1 + i * .1, 1.17, .22 - i * .005); l.rotation.z = (i - 1) * .2; }
      // sign board on two poles above the box
      for (const x of [-.5, .5]) box(g, '#5e3b22', .05, 1.9, .05, x, 0, -.12);
      const c = document.createElement('canvas'); c.width = 512; c.height = 200; const x = c.getContext('2d');
      x.fillStyle = '#fff4dc'; x.fillRect(0, 0, 512, 200); x.fillStyle = '#c4473a'; x.fillRect(0, 0, 512, 14); x.fillRect(0, 186, 512, 14);
      x.textAlign = 'center'; x.textBaseline = 'middle'; x.fillStyle = '#c4473a'; x.font = '700 76px "Pixelify Sans", sans-serif'; x.fillText('KOTAK USULAN', 256, 78, 490);
      x.fillStyle = '#5e3b22'; x.font = '700 34px "Pixelify Sans", sans-serif'; x.fillText('tulis usulanmu di komentar', 256, 148, 490);
      const tx = new THREE.CanvasTexture(c); tx.colorSpace = THREE.SRGBColorSpace; tx.anisotropy = 4;
      const sign = new THREE.Mesh(new THREE.PlaneGeometry(1.1, .43), new THREE.MeshStandardMaterial({ map: tx, roughness: .8 })); sign.position.set(0, 1.78, -.09); g.add(sign);
      box(g, '#3a2618', 1.14, .47, .03, 0, 1.555, -.12);
    } },
  // ep 31: the candidates' registration desk for the second election (14 Nov): a table with a red-white cloth, a ballot box,
  // a stack of forms and a pen, two chairs for the committee, and a banner on two poles. Banner text from b.label / b.sub
  mejadaftar: { n: 'Meja Pendaftaran Calon', w: 2, h: 2, land: true, scale: 1.25,
    build(g, b) {
      for (const [lx, lz] of [[-.72, -.12], [.72, -.12], [-.72, .2], [.72, .2]]) box(g, '#5e3b22', .05, .7, .05, lx, 0, lz);   // table legs
      box(g, '#7a4a28', 1.6, .05, .5, 0, .7, .04);                                                               // table top
      box(g, '#f4eee0', 1.62, .2, .01, 0, .52, .3); box(g, '#c4473a', 1.62, .2, .01, 0, .32, .3);                 // red-white cloth at the front
      box(g, '#f4eee0', 1.62, .02, .52, 0, .75, .04);
      // ballot box: white with a red band and a slot, a folded vote sticking out
      box(g, '#f7f3ea', .36, .3, .3, -.45, .77, .02); box(g, '#c4473a', .37, .06, .31, -.45, .93, .02); box(g, '#1d1d1b', .18, .012, .04, -.45, 1.07, .02);
      const v = box(g, '#fff4dc', .1, .08, .01, -.45, 1.07, .02); v.rotation.y = .4;
      // forms and a pen
      for (let i = 0; i < 4; i++) { const f = box(g, i % 2 ? '#fffaf0' : '#f2ead8', .22, .006, .3, .1 + i * .012, .77 + i * .006, .06 + i * .01); f.rotation.y = (i - 1.5) * .08; }
      const pen = box(g, '#2a4a8a', .015, .015, .2, .3, .8, .1); pen.rotation.y = .6;
      box(g, '#e6b84a', .2, .14, .02, .52, .77, .26);                                                            // little 'GRATIS' plate
      // two committee chairs behind the table
      for (const cx of [-.4, .4]) { for (const [lx, lz] of [[-.15, -.4], [.15, -.4], [-.15, -.68], [.15, -.68]]) box(g, '#4a3a2a', .04, .4, .04, cx + lx, 0, lz);
        box(g, '#5e4632', .38, .05, .36, cx, .4, -.54); box(g, '#5e4632', .38, .5, .05, cx, .45, -.74); }
      // the banner
      for (const x of [-.95, .95]) { box(g, '#5e3b22', .06, 2.5, .06, x, 0, -.95); box(g, '#c4473a', .1, .1, .1, x, 2.5, -.95); }
      const c = document.createElement('canvas'); c.width = 640; c.height = 240; const x = c.getContext('2d');
      x.fillStyle = '#c4473a'; x.fillRect(0, 0, 640, 120); x.fillStyle = '#f7f3ea'; x.fillRect(0, 120, 640, 120);
      x.textAlign = 'center'; x.textBaseline = 'middle'; x.fillStyle = '#fff8e6'; x.font = '700 62px "Pixelify Sans", sans-serif'; x.fillText((b && b.label) || 'PENDAFTARAN CALON', 320, 52, 610);
      x.font = '700 34px "Pixelify Sans", sans-serif'; x.fillText('PRESIDEN PULAU ARU', 320, 100, 610);
      x.fillStyle = '#3a2412'; x.font = '700 38px "Pixelify Sans", sans-serif'; x.fillText((b && b.sub) || 'komentar: AKU CALON + janjimu', 320, 160, 610);
      x.fillStyle = '#c4473a'; x.font = '700 34px "Pixelify Sans", sans-serif'; x.fillText((b && b.foot) || 'PEMILU 14 NOV · GRATIS', 320, 208, 610);
      const tx = new THREE.CanvasTexture(c); tx.colorSpace = THREE.SRGBColorSpace; tx.anisotropy = 4;
      box(g, '#3a2618', 1.86, .74, .03, 0, 1.58, -.97);
      const bn = new THREE.Mesh(new THREE.PlaneGeometry(1.8, .68), new THREE.MeshStandardMaterial({ map: tx, roughness: .85 })); bn.position.set(0, 1.95, -.95); g.add(bn);
    } },
  // ep 17: a public toilet from the old residents' suggestions (two doors, sink outside, water tank on the roof)
  toiletumum: { n: 'Toilet Umum', w: 3, h: 2, land: true, scale: 1.45,
    build(g) {
      box(g, '#c9bfa8', 2.0, .08, 1.5, 0, 0, 0);
      box(g, '#e9f1ee', 1.8, 1.5, 1.0, 0, .08, -.2);                                                        // tiled walls
      for (let i = 0; i < 7; i++) box(g, '#cfe0dc', 1.81, .02, 1.01, 0, .2 + i * .2, -.2);                 // tile lines
      box(g, '#2aa198', 1.82, .14, 1.02, 0, .08, -.2);                                                      // skirting
      box(g, '#7a8f8c', 2.0, .08, 1.25, 0, 1.58, -.15);                                                     // flat roof
      add(g, G.cyl8, '#4e7a9a', .22, .42, .22, .55, 1.66, -.35); add(g, G.cyl8, '#3d6580', .23, .04, .23, .55, 2.08, -.35);   // water tank
      // two doors with symbols
      for (const [dx, col, lab] of [[-.45, '#3a7fc2', 'PRIA'], [.45, '#c4473a', 'WANITA']]) {
        box(g, '#5e3b22', .52, 1.2, .04, dx, .08, .31); box(g, '#e6b84a', .04, .04, .02, dx + .18, .65, .335);
        const c = document.createElement('canvas'); c.width = 128; c.height = 160; const x = c.getContext('2d');
        x.fillStyle = col; x.fillRect(0, 0, 128, 160); x.fillStyle = '#fff'; x.beginPath(); x.arc(64, 38, 16, 0, Math.PI * 2); x.fill();
        if (lab === 'PRIA') x.fillRect(48, 58, 32, 50); else { x.beginPath(); x.moveTo(64, 56); x.lineTo(88, 108); x.lineTo(40, 108); x.fill(); }
        x.font = '700 26px "Pixelify Sans", sans-serif'; x.textAlign = 'center'; x.fillText(lab, 64, 138);
        const tx = new THREE.CanvasTexture(c); tx.colorSpace = THREE.SRGBColorSpace;
        const s = new THREE.Mesh(new THREE.PlaneGeometry(.26, .32), new THREE.MeshStandardMaterial({ map: tx })); s.position.set(dx, 1.0, .336); g.add(s);
      }
      // sign over the doors
      const c = document.createElement('canvas'); c.width = 512; c.height = 128; const x = c.getContext('2d');
      x.fillStyle = '#2aa198'; x.fillRect(0, 0, 512, 128); x.fillStyle = '#fff'; x.textAlign = 'center'; x.textBaseline = 'middle';
      x.font = '700 62px "Pixelify Sans", sans-serif'; x.fillText('TOILET UMUM', 256, 52, 490); x.font = '700 26px "Pixelify Sans", sans-serif'; x.fillText('gratis · bersih · ada sabun', 256, 104, 490);
      const tx = new THREE.CanvasTexture(c); tx.colorSpace = THREE.SRGBColorSpace; tx.anisotropy = 4;
      const sign = new THREE.Mesh(new THREE.PlaneGeometry(1.3, .32), new THREE.MeshStandardMaterial({ map: tx })); sign.position.set(0, 1.4, .315); g.add(sign);
      // sink outside on the right wall, with a mirror and soap
      box(g, '#f4f8f7', .14, .08, .36, .97, .72, .05); box(g, '#9a9b94', .04, .72, .04, .97, 0, .05); box(g, '#9a9b94', .02, .12, .02, 1.0, .8, .05);
      box(g, '#cfe8ee', .02, .3, .26, .91, 1.0, .05); add(g, G.cyl8, '#f2c94c', .025, .06, .025, .97, .8, .18);
      // a small bin and a potted plant
      add(g, G.cyl8, '#3f7f5a', .1, .3, .1, -.85, .08, .55); add(g, G.cyl8, '#8a5a34', .12, .2, .12, .75, .08, .6); add(g, G.ico, '#62bd73', .18, .2, .18, .75, .42, .6);
    } },
  // ep 18: the president's first request, picked from the suggestion box: Bank Pulau. Tapping it opens the bank sheet
  // (kebun.js openBank): save island coins in a savings account that earns a little interest every day.
  bankpulau: { n: 'Bank Pulau', w: 4, h: 3, land: true, scale: 1.75, open: 'bank', openLabel: 'Masuk Bank Pulau',
    build(g) {
      box(g, '#bdb6a4', 2.0, .1, 1.5, 0, 0, 0);                                                             // stone plinth
      box(g, '#cfc8b6', 1.5, .06, .3, 0, .1, .6); box(g, '#d8d2c2', 1.3, .06, .2, 0, .16, .62);             // front steps
      box(g, '#f3eee2', 1.8, 1.45, 1.05, 0, .1, -.2);                                                        // white hall
      box(g, '#e2dac8', 1.84, .12, 1.09, 0, .1, -.2);                                                        // skirting
      box(g, '#d9cfb8', 1.9, .12, 1.15, 0, 1.55, -.18);                                                      // cornice
      // portico: four columns, an architrave and a triangular pediment with a gold coin
      for (const x of [-.72, -.26, .26, .72]) { add(g, G.cyl8, '#fbf8f0', .07, 1.3, .07, x, .22 + .65, .55); box(g, '#e6dfcd', .18, .06, .18, x, .2, .55); box(g, '#e6dfcd', .18, .06, .18, x, 1.5, .55); }
      box(g, '#e9e2d0', 1.8, .14, .34, 0, 1.55, .46);
      const ped = new THREE.Shape(); ped.moveTo(-.95, 0); ped.lineTo(.95, 0); ped.lineTo(0, .5); ped.lineTo(-.95, 0);
      const pg = new THREE.Mesh(new THREE.ExtrudeGeometry(ped, { depth: 1.5, bevelEnabled: false }), mat('#b5413a')); pg.position.set(0, 1.69, -.82); pg.castShadow = true; g.add(pg);
      const pf = new THREE.Mesh(new THREE.ExtrudeGeometry(ped, { depth: .04, bevelEnabled: false }), mat('#f3eee2')); pf.scale.set(.86, .8, 1); pf.position.set(0, 1.71, .685); g.add(pf);
      const coin = add(g, G.cyl8, '#e6b84a', .14, .04, .14, 0, 1.86, .72); coin.rotation.x = Math.PI / 2; coin.position.y = 1.86;
      // big wooden door and two barred windows
      box(g, '#5e3b22', .44, .95, .04, 0, .1, .335); box(g, '#e6b84a', .03, .03, .02, .12, .55, .36); box(g, '#e6b84a', .03, .03, .02, -.12, .55, .36);
      for (const x of [-.6, .6]) { box(g, windowMat, .32, .5, .03, x, .6, .335); for (let i = 0; i < 4; i++) box(g, '#3a3a38', .02, .5, .04, x - .12 + i * .08, .6, .34); }
      // sign
      const c = document.createElement('canvas'); c.width = 512; c.height = 128; const x = c.getContext('2d');
      x.fillStyle = '#1f4e5f'; x.fillRect(0, 0, 512, 128); x.strokeStyle = '#e6b84a'; x.lineWidth = 8; x.strokeRect(6, 6, 500, 116);
      x.fillStyle = '#ffe9a8'; x.textAlign = 'center'; x.textBaseline = 'middle'; x.font = '700 66px "Pixelify Sans", sans-serif'; x.fillText('BANK PULAU', 256, 54, 480);
      x.font = '700 26px "Pixelify Sans", sans-serif'; x.fillStyle = '#ffffff'; x.fillText('tabungan koin pulau · ada bunganya', 256, 104, 480);
      const tx = new THREE.CanvasTexture(c); tx.colorSpace = THREE.SRGBColorSpace; tx.anisotropy = 4;
      const sign = new THREE.Mesh(new THREE.PlaneGeometry(1.5, .37), new THREE.MeshStandardMaterial({ map: tx })); sign.position.set(0, 1.3, .64); g.add(sign);
      // a coin machine (ATM) on the right side, and a stack of gold coins by the steps
      box(g, '#6f8a96', .26, .62, .22, 1.0, .1, .3); box(g, '#22313a', .18, .12, .02, 1.0, .5, .415); box(g, '#e6b84a', .12, .03, .02, 1.0, .36, .415);
      for (let i = 0; i < 4; i++) add(g, G.cyl8, '#e6b84a', .09, .03, .09, -.88 + (i % 2) * .02, .1 + i * .035, .62);
      add(g, G.cyl8, '#8a5a34', .12, .2, .12, .85, .1, .68); add(g, G.ico, '#62bd73', .17, .2, .17, .85, .42, .68);
    } },
  // ep 21: Bengkel Pulau, the old suggestion from the Kotak Usulan, built after the coffee cart lost a wheel.
  // An open-front garage: tool wall, workbench, tyre stack, oil drum, an air pump and a spare cart wheel.
  bengkel: { n: 'Bengkel Pulau', w: 4, h: 3, land: true, scale: 1.45,
    build(g, b) {
      box(g, '#a9a49a', 2.1, .08, 1.7, 0, 0, 0);                                                              // concrete floor
      box(g, '#7d7a72', 1.6, .01, .02, 0, .08, .3); box(g, '#7d7a72', 1.6, .01, .02, 0, .08, -.2);            // floor joints
      box(g, '#e8c25a', 1.9, 1.6, .08, 0, .08, -.78);                                                         // back wall
      for (const sx of [-.95, .95]) box(g, '#d9b04a', .08, 1.6, 1.5, sx, .08, -.05);                          // side walls
      box(g, '#2f3b46', 1.9, .16, .09, 0, .08, -.73);                                                          // dark skirting
      for (const sx of [-.95, .95]) box(g, '#2f3b46', .1, .16, 1.5, sx, .08, -.05);
      box(g, '#5f6b74', 2.2, .08, 1.85, 0, 1.68, -.02);                                                        // flat roof
      for (const sx of [-1.02, 1.02]) box(g, '#2f3b46', .12, 1.62, .12, sx, .08, .72);                        // front posts
      // shutter rolled up under the roof edge, with stripes
      add(g, G.cyl8, '#9aa3a8', .1, 1.86, .1, 0, 1.58, .74).rotation.z = Math.PI / 2;
      // tool wall: pegboard with wrenches, a hammer, a saw outline
      box(g, '#c99a5a', 1.2, .7, .03, -.15, .75, -.73);
      for (let i = 0; i < 6; i++) { const w = box(g, '#b8bec2', .04, .32 - (i % 3) * .05, .02, -.6 + i * .12, .95, -.71); w.rotation.z = (i % 2 ? .12 : -.12); }
      box(g, '#c4473a', .06, .22, .02, .18, 1.0, -.71); box(g, '#3a3a38', .16, .06, .025, .18, 1.2, -.71);
      box(g, '#b8bec2', .26, .1, .02, .34, .9, -.71);
      // workbench with a vice and a toolbox
      box(g, '#7a4a28', 1.1, .06, .36, -.2, .52, -.55); for (const [x, z] of [[-.7, -.68], [.3, -.68], [-.7, -.42], [.3, -.42]]) box(g, '#5e3b22', .05, .52, .05, x, 0, z);
      box(g, '#4e5a62', .14, .1, .1, -.6, .58, -.45); box(g, '#c4473a', .3, .14, .16, .08, .58, -.55); box(g, '#9e3329', .3, .03, .16, .08, .72, -.55);
      // the car-less lift: a wooden cart on two stands, being fixed (for any cart that loses a wheel)
      box(g, '#8a5a34', .9, .08, .5, .1, .42, .15); box(g, '#c4473a', .9, .22, .46, .1, .5, .15);
      for (const x of [-.25, .45]) box(g, '#4e5a62', .08, .42, .08, x, 0, .15);
      const wh = add(g, G.cyl8, '#2b2b2b', .2, .06, .2, .62, .2, .42); wh.rotation.x = Math.PI / 2; wh.rotation.z = .25;
      add(g, G.cyl8, '#9a9b94', .07, .07, .07, .62, .2, .42).rotation.x = Math.PI / 2;
      // tyre stack outside on the right, oil drum and air pump on the left
      for (let i = 0; i < 4; i++) { add(g, G.cyl8, '#232323', .22, .1, .22, 1.3, .13 + i * .11, .35); add(g, G.cyl8, '#5a5a5a', .1, .102, .1, 1.3, .13 + i * .11, .35); }
      add(g, G.cyl8, '#2f6fa8', .16, .44, .16, -1.25, .3, .5); add(g, G.cyl8, '#245a88', .165, .03, .165, -1.25, .52, .5);
      box(g, '#c4473a', .26, .34, .2, -1.28, .08, .05); box(g, '#f4eee0', .14, .07, .02, -1.28, .3, .16); const hose = box(g, '#1a1a1a', .03, .03, .5, -1.18, .12, .35); hose.rotation.y = .5;
      // the sign above the door
      const c = document.createElement('canvas'); c.width = 512; c.height = 128; const x = c.getContext('2d');
      x.fillStyle = '#2f3b46'; x.fillRect(0, 0, 512, 128); x.fillStyle = '#e8c25a'; for (let i = 0; i < 512; i += 48) { x.beginPath(); x.moveTo(i, 120); x.lineTo(i + 24, 120); x.lineTo(i + 16, 128); x.lineTo(i - 8, 128); x.fill(); }
      x.textAlign = 'center'; x.textBaseline = 'middle'; x.fillStyle = '#ffd25a'; x.font = '700 64px "Pixelify Sans", sans-serif'; x.fillText((b && b.label) || 'BENGKEL PULAU', 256, 50, 490);
      x.fillStyle = '#ffffff'; x.font = '700 24px "Pixelify Sans", sans-serif'; x.fillText((b && b.sub) || 'tambal ban · servis gerobak · angin gratis', 256, 98, 490);
      const tx = new THREE.CanvasTexture(c); tx.colorSpace = THREE.SRGBColorSpace; tx.anisotropy = 4;
      box(g, '#2f3b46', 2.12, .46, .05, 0, 1.76, .8);
      const sign = new THREE.Mesh(new THREE.PlaneGeometry(2.04, .42), new THREE.MeshStandardMaterial({ map: tx, roughness: .8 })); sign.position.set(0, 1.99, .83); g.add(sign);
      // a wrench-shaped hanging lamp
      const lamp = new THREE.Mesh(G.sph, lanternMat); lamp.scale.set(.08, .1, .08); lamp.position.set(.6, 1.45, .3); g.add(lamp);
    } },
  // ep 22: the president's second request ("aku kan presiden aku mau apartemen"): the island's first tall building.
  // Five floors with balconies and windows that light up at night, a glass lobby, a gold penthouse on top for the president.
  apartemen: { n: 'Apartemen Presiden', w: 5, h: 4, land: true, scale: 1.5,
    build(g, b) {
      const F = 1.15, N = 5, W = 2.4, D = 1.7, y0 = .12;
      box(g, '#bdb6a4', 2.9, .12, 2.3, 0, 0, 0);                                                             // plaza
      box(g, '#d8d2c2', 1.2, .05, .3, 0, .12, 1.0);                                                          // entrance step
      for (let i = 0; i < N; i++) {
        const y = y0 + i * F, top = i === N - 1;
        box(g, top ? '#e9dcc0' : (i % 2 ? '#f1ece0' : '#ebe4d4'), W, F, D, 0, y, -.15);                         // floor block
        box(g, '#b8523c', W + .06, .07, D + .06, 0, y + F - .07, -.15);                                        // floor band
        if (i === 0) {                                                                                        // glass lobby
          box(g, windowMat, 1.4, .95, .04, 0, y, .71); box(g, '#3a3a38', .05, 1.0, .06, 0, y, .73);
          box(g, '#3a3a38', 1.5, .06, .06, 0, y + .95, .73);
          box(g, '#2f3b46', 1.7, .06, .5, 0, y + 1.0, .9);                                                     // canopy
          for (const x of [-.8, .8]) box(g, '#2f3b46', .05, 1.0, .05, x, y, 1.12);
          for (const x of [-1.0, 1.0]) box(g, windowMat, .22, .5, .04, x, y + .35, .71);
        } else {
          for (const x of [-.85, -.3, .3, .85]) box(g, windowMat, .3, .5, .04, x, y + .3, .71);                // front windows
          for (const z of [-.6, .1]) { box(g, windowMat, .04, .5, .32, W / 2 + .01, y + .3, z); box(g, windowMat, .04, .5, .32, -W / 2 - .01, y + .3, z); }
          for (const x of [-.58, .58]) {                                                                      // two balconies per floor
            box(g, '#cfc8b6', .8, .05, .3, x, y + .02, .85);
            box(g, '#7b8b94', .8, .25, .03, x, y + .07, 1.0); for (const sx of [-.4, .4]) box(g, '#7b8b94', .03, .25, .3, x + sx, y + .07, .85);
          }
          if (i === 2) { box(g, '#e63946', .08, .14, .02, -.38, y + .15, 1.0); box(g, '#2f7de1', .08, .14, .02, -.26, y + .15, 1.0); }   // laundry on a rail
          if (i === 3) add(g, G.ico, '#62bd73', .1, .12, .1, .8, y + .17, .9);                                // a potted plant
        }
        for (const x of [-W / 2, W / 2]) box(g, '#d4c7a8', .1, F, .1, x, y, .69);                             // corner pilasters
      }
      // the penthouse on the roof: gold trim, a crown sign and a flag (for the president, naturally)
      const ry = y0 + N * F;
      box(g, '#8a8478', W + .1, .1, D + .1, 0, ry, -.15);
      box(g, '#f7f2e4', 1.3, .7, 1.0, 0, ry + .1, -.35); box(g, '#e6b84a', 1.36, .08, 1.06, 0, ry + .8, -.35);
      box(g, windowMat, 1.0, .4, .04, 0, ry + .25, .16);
      for (const x of [-1.1, 1.1]) box(g, '#7b8b94', .03, .25, D, x, ry + .1, -.15);
      box(g, '#7b8b94', W - .1, .25, .03, 0, ry + .1, .68);
      const crown = new THREE.Group(); crown.position.set(0, ry + .88, -.35); g.add(crown);
      box(crown, '#e6b84a', .5, .14, .12, 0, 0, 0); for (const x of [-.2, 0, .2]) add(crown, G.cone4, '#e6b84a', .07, .18, .07, x, .23, 0);
      add(g, G.cyl6, '#9a9b94', .02, 1.0, .02, .95, ry + .6, -.85);
      const flag = box(g, '#c4473a', .36, .2, .02, 1.13, ry + .9, -.85); box(g, '#f4eee0', .36, .1, .021, 1.13, ry + .9, -.85);
      // the sign over the lobby canopy
      const c = document.createElement('canvas'); c.width = 512; c.height = 128; const x = c.getContext('2d');
      x.fillStyle = '#1f2a44'; x.fillRect(0, 0, 512, 128); x.strokeStyle = '#e6b84a'; x.lineWidth = 8; x.strokeRect(6, 6, 500, 116);
      x.textAlign = 'center'; x.textBaseline = 'middle'; x.fillStyle = '#ffd25a'; x.font = '700 60px "Pixelify Sans", sans-serif'; x.fillText((b && b.label) || 'APARTEMEN PRESIDEN', 256, 52, 480);
      x.fillStyle = '#ffffff'; x.font = '700 24px "Pixelify Sans", sans-serif'; x.fillText((b && b.sub) || 'lantai paling atas: khusus presiden', 256, 100, 480);
      const tx = new THREE.CanvasTexture(c); tx.colorSpace = THREE.SRGBColorSpace; tx.anisotropy = 4;
      const sign = new THREE.Mesh(new THREE.PlaneGeometry(1.6, .4), new THREE.MeshStandardMaterial({ map: tx, roughness: .8 })); sign.position.set(0, y0 + 1.32, 1.16); g.add(sign);
      // ep 26: the glass lift on the east side ("apartemenya kasih lift dong", @vcxn.mx). The cabin rides the shaft (main.js animates g.userData.lift)
      { const lx = 1.52, lz = .46, top = ry + 1.2, sw = .62, sd = .5, glass = new THREE.MeshStandardMaterial({ color: '#bfe6ff', roughness: .1, metalness: .1, transparent: true, opacity: .3, depthWrite: false });
        box(g, '#3a4650', sw + .04, .1, sd + .04, lx, .12, lz); box(g, '#3a4650', sw + .04, .1, sd + .04, lx, top, lz);
        for (const [dx, dz] of [[-1, -1], [1, -1], [-1, 1], [1, 1]]) box(g, '#3a4650', .04, top - .12, .04, lx + dx * sw / 2, .12, lz + dz * sd / 2);
        for (let i = 1; i <= N; i++) box(g, '#3a4650', sw, .03, .03, lx, y0 + i * F - .05, lz + sd / 2);
        box(g, glass, sw - .04, top - .22, .01, lx, .22, lz + sd / 2); box(g, glass, .01, top - .22, sd - .04, lx + sw / 2, .22, lz);
        const cab = new THREE.Group(); cab.position.set(lx, .22, lz); g.add(cab); g.userData.lift = cab; cab.userData.span = [.22, ry + .02];
        const cw = sw - .1, cd = sd - .08; box(cab, '#e6b84a', cw, .05, cd, 0, 0, 0); box(cab, '#e6b84a', cw, .05, cd, 0, 1.06, 0); box(cab, '#f1ece0', cw, 1.06, .03, 0, .02, -cd / 2 + .02);
        for (const dx of [-1, 1]) box(cab, '#e6b84a', .03, 1.06, .03, dx * cw / 2, .02, cd / 2);
        const lt = new THREE.Mesh(G.sph, lanternMat); lt.scale.set(.05, .03, .05); lt.position.set(0, 1.04, 0); cab.add(lt);
        const lc = document.createElement('canvas'); lc.width = 128; lc.height = 64; const lx2 = lc.getContext('2d'); lx2.fillStyle = '#1f2a44'; lx2.fillRect(0, 0, 128, 64); lx2.fillStyle = '#ffd25a'; lx2.font = '700 40px "Pixelify Sans", sans-serif'; lx2.textAlign = 'center'; lx2.textBaseline = 'middle'; lx2.fillText('LIFT', 64, 34);
        const lt2 = new THREE.CanvasTexture(lc); lt2.colorSpace = THREE.SRGBColorSpace; const ls = new THREE.Mesh(new THREE.PlaneGeometry(.36, .18), new THREE.MeshStandardMaterial({ map: lt2, roughness: .8 })); ls.position.set(lx, 1.45, lz + sd / 2 + .03); g.add(ls); }
      // planters and a bench on the plaza, a lamp by the door
      for (const x of [-1.25, 1.25]) { box(g, '#8a5a34', .3, .2, .3, x, .12, .95); add(g, G.ico, '#62bd73', .2, .22, .2, x, .48, .95); }
      const lamp = new THREE.Mesh(G.sph, lanternMat); lamp.scale.set(.08, .1, .08); lamp.position.set(.62, 1.0, .95); g.add(lamp);
    } },
  // ep 23: the president's schedule board, kept by Sekretaris Presiden Debby (items from b.items, footer from b.label)
  // ep 33: Kamera Jaga Malam: the detectives' night camera on a pole by the lighthouse, aimed at its door (+z at r=0).
  // A blinking red REC light (userData.led), a small sign; b.label = who installed it.
  cctv: { n: 'Kamera Jaga Malam', w: 1, h: 1, land: true,
    build(g, b) {
      add(g, G.cyl6, '#9a9b94', .2, .12, .2, 0, .06, 0); add(g, G.cyl6, '#6b6f75', .05, 2.5, .05, 0, 1.25, 0);
      box(g, '#6b6f75', .06, .06, .42, 0, 2.38, .12); const cam = box(g, '#f2f2ee', .26, .22, .46, 0, 2.3, .36); cam.rotation.x = .18; box(g, '#f2f2ee', .34, .04, .5, 0, 2.53, .34);
      add(g, G.cyl8, '#111318', .08, .06, .08, 0, 2.38, .62).rotation.x = Math.PI / 2 - .18;
      const led = add(g, G.sph, new THREE.MeshBasicMaterial({ color: '#ff2a2a' }), .035, .035, .035, .09, 2.47, .6, 0, false); g.userData.led = led;
      const c = document.createElement('canvas'); c.width = 512; c.height = 256; const x = c.getContext('2d');
      x.fillStyle = '#1f2a44'; x.fillRect(0, 0, 512, 256); x.fillStyle = '#ffd25a'; x.fillRect(0, 0, 512, 12); x.fillRect(0, 244, 512, 12);
      x.textAlign = 'center'; x.textBaseline = 'middle'; x.fillStyle = '#ff4a3a'; x.font = '700 40px "Pixelify Sans", sans-serif'; x.fillText('● REC', 256, 50, 480);
      x.fillStyle = '#ffffff'; x.font = '700 50px "Pixelify Sans", sans-serif'; x.fillText('KAMERA JAGA MALAM', 256, 118, 490);
      x.fillStyle = '#ffd25a'; x.font = '700 28px "Pixelify Sans", sans-serif'; x.fillText((b && b.label) || 'Detektif Pantai', 256, 196, 490);
      const tx = new THREE.CanvasTexture(c); tx.colorSpace = THREE.SRGBColorSpace; tx.anisotropy = 4;
      const sign = new THREE.Mesh(new THREE.PlaneGeometry(.9, .45), new THREE.MeshStandardMaterial({ map: tx, roughness: .8 })); sign.position.set(0, 1.25, -.06); sign.rotation.y = Math.PI; g.add(sign); box(g, '#1f2a44', .92, .47, .02, 0, 1.015, -.04);
    } },
  papanjadwal: { n: 'Papan Jadwal Presiden', w: 2, h: 1, land: true,
    build(g, b) {
      for (const x of [-.6, .6]) { const l = box(g, '#5e3b22', .07, 1.7, .07, x, 0, -.12); l.rotation.x = .12; }
      box(g, '#5e3b22', 1.5, 1.1, .06, 0, .75, -.02); box(g, '#5e3b22', 1.3, .05, .12, 0, .73, .04);
      const items = (b && b.items) || ['PR dari Bu Guru Gina'], hc = (b && b.color) || '#2f5e8a';
      const c = document.createElement('canvas'); c.width = 512; c.height = 384; const x = c.getContext('2d');
      x.fillStyle = '#fbfaf5'; x.fillRect(0, 0, 512, 384); x.fillStyle = hc; x.fillRect(0, 0, 512, 72);
      x.textAlign = 'center'; x.textBaseline = 'middle'; x.fillStyle = '#ffffff'; x.font = '700 46px "Pixelify Sans", sans-serif'; x.fillText((b && b.head) || 'JADWAL PRESIDEN', 256, 38, 490);
      x.textAlign = 'left'; x.fillStyle = '#1f2a44';
      items.slice(0, 4).forEach((t, i) => { const ck = i === 0 || /^✓/.test(t); t = t.replace(/^✓\s*/, ''); let fs = 34; x.font = `700 ${fs}px "Pixelify Sans", sans-serif`; while (fs > 18 && x.measureText(t).width > 400) { fs -= 2; x.font = `700 ${fs}px "Pixelify Sans", sans-serif`; }
        x.strokeStyle = '#2f5e8a'; x.lineWidth = 4; x.strokeRect(30, 104 + i * 58, 28, 28); if (ck) { x.strokeStyle = '#c0392b'; x.beginPath(); x.moveTo(34, 118 + i * 58); x.lineTo(44, 130 + i * 58); x.lineTo(62, 98 + i * 58); x.stroke(); } x.fillText(t, 74, 120 + i * 58); });
      x.textAlign = 'center'; x.fillStyle = '#c0392b'; x.font = '700 26px "Pixelify Sans", sans-serif'; x.fillText((b && b.label) || 'Sekretaris: Debby', 256, 356, 490);
      const tx = new THREE.CanvasTexture(c); tx.colorSpace = THREE.SRGBColorSpace; tx.anisotropy = 4;
      const sign = new THREE.Mesh(new THREE.PlaneGeometry(1.4, 1.05), new THREE.MeshStandardMaterial({ map: tx, roughness: .8 })); sign.position.set(0, 1.3, .015); g.add(sign);
    } },
  // ep 24: Hotel Pulau, the last old suggestion from the Kotak Usulan (for study-tour guests and visitors from the pier).
  // Three floors with numbered windows that light up at night, a glass lobby with a reception desk, a striped awning,
  // a roof sign and a luggage trolley at the door. b.label = sign, b.sub = small line under it.
  hotel: { n: 'Hotel Pulau', w: 4, h: 4, land: true, scale: 1.5,
    build(g, b) {
      const F = 1.1, N = 3, W = 2.2, D = 1.6, y0 = .12;
      box(g, '#d9cfb8', 2.6, .12, 2.4, 0, 0, 0);                                                              // forecourt
      box(g, '#c94f6d', .9, .02, .5, 0, .12, .95);                                                            // red carpet
      for (let i = 0; i < N; i++) {
        const y = y0 + i * F;
        box(g, i % 2 ? '#bfe3dd' : '#a9d8d1', W, F, D, 0, y, -.25);                                            // floor block (sea-green)
        box(g, '#f7f2e4', W + .06, .07, D + .06, 0, y + F - .07, -.25);                                       // white floor band
        if (i === 0) {
          box(g, windowMat, 1.3, .9, .04, 0, y, .56); box(g, '#f7f2e4', .05, .95, .06, 0, y, .58); box(g, '#f7f2e4', 1.4, .06, .06, 0, y + .9, .58);
          box(g, '#8a5a34', .9, .4, .25, 0, y, .1); box(g, '#e6b84a', .92, .04, .27, 0, y + .4, .1);          // reception desk behind the glass
          add(g, G.sph, '#e6b84a', .05, .04, .05, .3, y + .46, .12);                                          // the little bell
          for (const x of [-.85, .85]) box(g, windowMat, .3, .5, .04, x, y + .3, .56);
        } else {
          for (const x of [-.75, -.25, .25, .75]) { box(g, windowMat, .3, .5, .04, x, y + .3, .56); box(g, '#f7f2e4', .36, .05, .08, x, y + .26, .58); }
          for (const z of [-.75, -.15]) { box(g, windowMat, .04, .5, .3, W / 2 + .01, y + .3, z); box(g, windowMat, .04, .5, .3, -W / 2 - .01, y + .3, z); }
          box(g, '#f7f2e4', W - .1, .04, .22, 0, y, .66); box(g, '#7b8b94', W - .1, .2, .03, 0, y + .04, .77); // balcony rail
        }
      }
      // striped awning over the door, on two gold posts
      for (let i = 0; i < 6; i++) { const s = box(g, i % 2 ? '#f7f2e4' : '#c94f6d', .25, .05, .7, -.62 + i * .25, y0 + 1.08, .95); s.rotation.x = -.18; }
      for (const x of [-.7, .7]) box(g, '#e6b84a', .05, 1.05, .05, x, y0, 1.28);
      // roof: parapet, water tank and the big sign with three stars
      const ry = y0 + N * F;
      box(g, '#8a8478', W + .1, .1, D + .1, 0, ry, -.25);
      add(g, G.cyl8, '#9aa3a8', .2, .35, .2, -.7, ry + .28, -.6);
      const c = document.createElement('canvas'); c.width = 512; c.height = 160; const x = c.getContext('2d');
      x.fillStyle = '#c94f6d'; x.fillRect(0, 0, 512, 160); x.strokeStyle = '#ffd25a'; x.lineWidth = 8; x.strokeRect(6, 6, 500, 148);
      x.textAlign = 'center'; x.textBaseline = 'middle'; x.fillStyle = '#ffd25a'; x.font = '700 72px "Pixelify Sans", sans-serif'; x.fillText((b && b.label) || 'HOTEL PULAU', 256, 62, 480);
      x.fillStyle = '#ffffff'; x.font = '700 26px "Pixelify Sans", sans-serif'; x.fillText((b && b.sub) || '★ ★ ★  usulan warga', 256, 126, 480);
      const tx = new THREE.CanvasTexture(c); tx.colorSpace = THREE.SRGBColorSpace; tx.anisotropy = 4;
      for (const x2 of [-.7, .7]) box(g, '#5f6b74', .05, .45, .05, x2, ry + .1, .3);
      const sign = new THREE.Mesh(new THREE.PlaneGeometry(1.9, .6), new THREE.MeshStandardMaterial({ map: tx, roughness: .8 })); sign.position.set(0, ry + .75, .34); g.add(sign);
      box(g, '#5f6b74', 1.96, .64, .04, 0, ry + .43, .31);
      // luggage trolley by the door (gold frame, two suitcases), planters, a lamp
      box(g, '#e6b84a', .5, .03, .3, .98, .3, 1.0); for (const x2 of [.75, 1.21]) box(g, '#e6b84a', .03, .7, .03, x2, .12, 1.0); box(g, '#e6b84a', .5, .03, .03, .98, .82, 1.0);
      box(g, '#2f7de1', .3, .22, .18, .9, .33, 1.0); box(g, '#e63946', .22, .16, .14, 1.05, .55, 1.0);
      for (const x2 of [-1.05]) { box(g, '#8a5a34', .3, .2, .3, x2, .12, 1.0); add(g, G.ico, '#62bd73', .2, .22, .2, x2, .48, 1.0); }
      const lamp = new THREE.Mesh(G.sph, lanternMat); lamp.scale.set(.08, .1, .08); lamp.position.set(-.55, 1.0, .95); g.add(lamp);
    } },
  // ep 23: the study tour banner by the school (a comment asked for a study tour once a year); the tour itself walks the island (island.json → tour)
  spandukstudytour: { n: 'Spanduk Study Tour', w: 4, h: 1, land: true,
    build(g, b) {
      for (const x of [-1.85, 1.85]) { add(g, G.cyl6, '#c9a868', .05, 2.7, .05, x, 1.35, 0); add(g, G.sph, '#e6b84a', .07, .07, .07, x, 2.72, 0); }
      const c = document.createElement('canvas'); c.width = 1024; c.height = 256; const x = c.getContext('2d');
      x.fillStyle = '#ffd25a'; x.fillRect(0, 0, 1024, 256); x.fillStyle = '#2f5e8a'; x.fillRect(0, 0, 1024, 16); x.fillRect(0, 240, 1024, 16);
      x.textAlign = 'center'; x.textBaseline = 'middle'; x.fillStyle = '#c0392b'; x.font = '700 112px "Pixelify Sans", sans-serif'; x.fillText((b && b.label) || 'STUDY TOUR', 512, 100, 980);
      x.fillStyle = '#1f2a44'; x.font = '700 44px "Pixelify Sans", sans-serif'; x.fillText((b && b.sub) || 'Sekolah Pulau Aru · setahun sekali', 512, 196, 980);
      const tx = new THREE.CanvasTexture(c); tx.colorSpace = THREE.SRGBColorSpace; tx.anisotropy = 4;
      const cloth = new THREE.Mesh(new THREE.PlaneGeometry(3.6, .9), new THREE.MeshStandardMaterial({ map: tx, roughness: .9, side: THREE.DoubleSide })); cloth.position.set(0, 2.1, 0); g.add(cloth);
      for (const y of [1.64, 2.56]) box(g, '#8a6a3a', 3.7, .02, .02, 0, y, 0);
      const cols = ['#d0483a', '#2f7de1', '#62bd73', '#ffd25a'];
      for (let i = 0; i < 9; i++) { const f = add(g, G.cone4, cols[i % 4], .1, .16, .02, -1.6 + i * .4, 2.62, 0, Math.PI / 4); f.rotation.z = Math.PI; }
    } },
  // ep 27: Gedung Rapat Pulau ("aku mau jadi mentri keuangan, sekalian gedung buat rapat", @araa_yinchan).
  // An open-front hall (pendopo style) so the meeting is visible from the street: long table, five chairs, the
  // president's red chair in the middle, the Menteri Keuangan's seat with a big calculator, a KAS PULAU coin jar,
  // and the agenda whiteboard on the back wall (b.items, up to 4). b.label = sign, b.sub = small line.
  gedungrapat: { n: 'Gedung Rapat Pulau', w: 5, h: 4, land: true, scale: 1.5,
    build(g, b) {
      const tex = (w, h, draw) => { const c = document.createElement('canvas'); c.width = w; c.height = h; draw(c.getContext('2d')); const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 4; return t; };
      const plane = (t, w, h, x, y, z, ry = 0) => { const m = new THREE.Mesh(new THREE.PlaneGeometry(w, h), new THREE.MeshStandardMaterial({ map: t, roughness: .8 })); m.position.set(x, y, z); m.rotation.y = ry; g.add(m); return m; };
      const font = (x, fs) => { x.font = `700 ${fs}px "Pixelify Sans", sans-serif`; };
      box(g, '#c9bfa8', 3.0, .15, 2.3, 0, 0, 0);                                                              // stone plinth
      box(g, '#b8ae96', 1.3, .08, .3, 0, 0, 1.25);                                                           // front step
      box(g, '#a8784a', 2.8, .02, 2.1, 0, .15, -.02);                                                        // wooden floor
      box(g, '#efe2c6', 2.9, 1.75, .1, 0, .15, -1.08);                                                       // back wall
      for (const sx of [-1.43, 1.43]) box(g, '#e6d6b4', .1, 1.75, 1.0, sx, .15, -.6);                        // short side walls
      for (const sx of [-1.43, 1.43]) box(g, '#8a5a34', .1, .35, 1.1, sx, .15, .5);                          // low side rails
      for (const [x, z] of [[-1.42, 1.05], [1.42, 1.05], [-1.42, -.08], [1.42, -.08]]) cyl(g, '#f4eee0', .07, 1.75, x, .15, z, 8);   // white columns
      box(g, '#7c2f28', 3.1, .12, 2.5, 0, 1.9, -.02);                                                        // beam ring
      roof4(g, '#8e3a2e', 3.6, .55, 3.0, 0, 2.02, -.02); roof4(g, '#a8443a', 1.6, .45, 1.35, 0, 2.5, -.02);   // two-tier roof
      add(g, G.sph, '#e6b84a', .09, .09, .09, 0, 3.0, -.02);                                                 // gold finial
      // the long table with five chairs behind it, all facing the street
      box(g, '#6b4226', 2.2, .05, .6, 0, .62, -.15); for (const [x, z] of [[-1.0, -.4], [1.0, -.4], [-1.0, .1], [1.0, .1]]) box(g, '#5e3b22', .05, .47, .05, x, .15, z);
      box(g, '#2f5e8a', 2.22, .2, .02, 0, .47, .16);                                                         // table skirt
      const seats = [-.84, -.42, 0, .42, .84];
      seats.forEach((x, i) => { const pres = i === 2, min = i === 3, col = pres ? '#b33a2e' : min ? '#2f7a4a' : '#5e3b22';
        box(g, col, .3, .05, .28, x, .42, -.62); box(g, col, .3, pres ? .62 : .42, .05, x, .47, -.76);
        for (const [dx, dz] of [[-.12, -.5], [.12, -.5], [-.12, -.74], [.12, -.74]]) box(g, '#3a2412', .03, .27, .03, x + dx, .15, dz);
        if (pres) add(g, G.cone4, '#e6b84a', .06, .1, .06, x, 1.15, -.76); });
      // nameplates on the table
      const np = (t, x) => { box(g, '#f4eee0', .3, .08, .02, x, .67, .05); plane(tex(256, 64, c => { c.fillStyle = '#f4eee0'; c.fillRect(0, 0, 256, 64); c.fillStyle = '#1f2a44'; c.textAlign = 'center'; c.textBaseline = 'middle'; font(c, 26); c.fillText(t, 128, 34, 246); }), .3, .075, x, .71, .065); };
      np('PRESIDEN', 0); np('MENTERI KEUANGAN', .42); np('WAPRES', -.42); np('SEKRETARIS', .84); np('WARGA', -.84);
      // the minister's desk kit: a big calculator and a KAS PULAU coin jar
      box(g, '#2b2d42', .2, .03, .26, .42, .67, -.2); box(g, '#9fd8a8', .14, .01, .06, .42, .7, -.29); for (let r = 0; r < 3; r++) for (let k = 0; k < 3; k++) box(g, k === 2 && r === 2 ? '#e63946' : '#e8e8e8', .035, .012, .035, .38 + k * .045, .7, -.22 + r * .05);
      const jar = new THREE.MeshStandardMaterial({ color: '#cfefff', transparent: true, opacity: .45, roughness: .1, depthWrite: false });
      add(g, G.cyl8, jar, .12, .26, .12, .72, .8, -.2); add(g, G.cyl8, '#e6b84a', .1, .12, .1, .72, .73, -.2); add(g, G.cyl8, '#8a5a34', .125, .03, .125, .72, .95, -.2);
      box(g, '#c0392b', .2, .05, .01, .72, .76, -.07);
      // coin stacks for the treasury
      for (let i = 0; i < 4; i++) add(g, G.cyl8, '#e6b84a', .045, .02, .045, -.15 + (i % 2) * .06, .66 + Math.floor(i / 2) * .02, -.25, 0, false);
      // the agenda whiteboard on the back wall
      const items = (b && b.items) || ['Lima koin kotak usulan (Presiden)', 'Pelabuhan untuk nelayan?', 'Usulan rapat dari komentar'];
      const wb = tex(768, 480, x => { x.fillStyle = '#fbfaf5'; x.fillRect(0, 0, 768, 480); x.fillStyle = '#2f7a4a'; x.fillRect(0, 0, 768, 84);
        x.textAlign = 'center'; x.textBaseline = 'middle'; x.fillStyle = '#fff'; font(x, 58); x.fillText((b && b.head) || 'AGENDA RAPAT', 384, 44, 740);
        x.textAlign = 'left'; x.fillStyle = '#1f2a44';
        items.slice(0, 4).forEach((t, i) => { let fs = 44; font(x, fs); while (fs > 22 && x.measureText(t).width > 640) { fs -= 2; font(x, fs); } x.fillStyle = '#c0392b'; x.fillText((i + 1) + '.', 30, 136 + i * 84); x.fillStyle = '#1f2a44'; x.fillText(t, 84, 136 + i * 84); });
        x.textAlign = 'right'; x.fillStyle = '#2f7a4a'; font(x, 28); x.fillText((b && b.foot) || 'Menteri Keuangan: @araa_yinchan', 750, 456, 700); });
      box(g, '#5e3b22', 1.66, 1.0, .04, 0, .9, -1.02); plane(wb, 1.58, .94, 0, 1.4, -.995);
      // the sign on the roof fascia
      const sg = tex(1024, 192, x => { x.fillStyle = '#1f3b2a'; x.fillRect(0, 0, 1024, 192); x.strokeStyle = '#e6b84a'; x.lineWidth = 10; x.strokeRect(8, 8, 1008, 176);
        x.textAlign = 'center'; x.textBaseline = 'middle'; x.fillStyle = '#ffd25a'; font(x, 92); x.fillText((b && b.label) || 'GEDUNG RAPAT PULAU', 512, 78, 960);
        x.fillStyle = '#fff'; font(x, 38); x.fillText((b && b.sub) || 'rapat warga · kas pulau · Menteri Keuangan', 512, 152, 960); });
      box(g, '#1f3b2a', 2.3, .42, .05, 0, 1.48, 1.12); plane(sg, 2.22, .38, 0, 1.69, 1.15);
      // planters by the step and a lantern
      for (const x of [-1.2, 1.2]) { box(g, '#8a5a34', .26, .2, .26, x, .15, 1.2); add(g, G.ico, '#62bd73', .18, .2, .18, x, .5, 1.2); }
      const lamp = new THREE.Mesh(G.sph, lanternMat); lamp.scale.set(.08, .1, .08); lamp.position.set(1.1, 1.78, .5); g.add(lamp);
    } },
  // ep 28 (jatah terakhir Presiden 'EGA_, komentar "buat lapangan minn buat gotong royong"): a grass field for kerja bakti:
  // pitch lines, two goals, a red-white flag pole, a tool shed with brooms and hoes, sacks, and the name board (b.label / b.sub)
  lapangangr: { n: 'Lapangan Gotong Royong', w: 9, h: 7, land: true,
    build(g, b) {
      const tex = (w, h, draw) => { const c = document.createElement('canvas'); c.width = w; c.height = h; draw(c.getContext('2d')); const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 4; return t; };
      box(g, '#76c25e', 8.8, .05, 6.8, 0, 0, 0);
      for (let i = 0; i < 6; i++) box(g, i % 2 ? '#6fb957' : '#7cc864', 1.3, .006, 6.0, -3.25 + i * 1.3, .05, 0);   // mowed stripes
      for (const [w, d, x, z] of [[7.8, .05, 0, -3.0], [7.8, .05, 0, 3.0], [.05, 6.0, -3.9, 0], [.05, 6.0, 3.9, 0], [.05, 6.0, 0, 0]]) box(g, '#f7f7f3', w, .012, d, x, .058, z);
      for (let a = 0; a < 16; a++) { const t = a / 16 * Math.PI * 2; box(g, '#f7f7f3', .2, .012, .05, Math.cos(t) * .8, .058, Math.sin(t) * .8, -t + Math.PI / 2); }
      for (const sx of [-1, 1]) { const x = sx * 3.8; for (const z of [-.75, .75]) box(g, '#f7f7f3', .07, 1.0, .07, x, .05, z); box(g, '#f7f7f3', .07, .07, 1.57, x, 1.02, 0);
        for (let i = 0; i < 4; i++) box(g, '#dcdcd6', .01, .95, .01, x + sx * .25, .05, -.6 + i * .4); box(g, '#dcdcd6', .3, .01, 1.5, x + sx * .14, 1.0, 0); }
      add(g, G.cyl6, '#d8dad6', .04, 3.6, .04, -3.0, 1.85, -3.25); box(g, '#cfc8b6', .55, .14, .55, -3.0, .05, -3.25);
      box(g, '#d0483a', .75, .24, .02, -2.6, 3.3, -3.25); box(g, '#f7f7f3', .75, .24, .02, -2.6, 3.06, -3.25);
      // tool shed (gudang alat kerja bakti) in the back right corner
      const sh = new THREE.Group(); sh.position.set(3.1, .05, -2.75); g.add(sh);
      box(sh, '#e8c98a', 1.9, 1.7, 1.0, 0, 0, 0); roof4(sh, '#8e3a2e', 2.3, .55, 1.4, 0, 1.7, 0); box(sh, '#4a2f1d', .9, 1.35, .04, -.2, 0, .51);
      for (let i = 0; i < 4; i++) { const st = box(sh, '#a9784a', .04, 1.3, .04, .45 + i * .12, 0, .62); st.rotation.z = .1; box(sh, '#d9b45a', .14, .3, .06, .45 + i * .12, 0, .62); }
      const hoe = box(sh, '#a9784a', .04, 1.3, .04, -.85, 0, .62); hoe.rotation.z = -.12; box(sh, '#8a9196', .22, .16, .04, -.93, 1.2, .64);
      // sacks and a wheelbarrow, ready for gotong royong
      for (const [x, z, r] of [[2.1, -2.1, .2], [2.45, -2.0, -.3], [2.25, -1.75, .1]]) { add(g, G.dode, '#d8c49a', .26, .22, .2, x, .25, z).rotation.y = r; }
      const wb = new THREE.Group(); wb.position.set(1.5, .05, -2.35); wb.rotation.y = .4; g.add(wb);
      box(wb, '#3a7fc2', .55, .25, .8, 0, .2, 0); add(wb, G.cyl8, '#2b2b2b', .14, .06, .14, 0, .14, .48).rotation.z = Math.PI / 2; for (const x of [-.22, .22]) box(wb, '#5e3b22', .04, .04, .8, x, .3, -.55);
      // the name board at the front edge, facing the street side (+z)
      for (const x of [-1.2, 1.2]) box(g, '#5e3b22', .1, 1.75, .1, x, .05, 3.3);
      const t = tex(768, 220, c => { c.fillStyle = '#2f7a4a'; c.fillRect(0, 0, 768, 220); c.strokeStyle = '#f4eee0'; c.lineWidth = 10; c.strokeRect(10, 10, 748, 200);
        c.fillStyle = '#ffffff'; c.textAlign = 'center'; c.textBaseline = 'middle'; c.font = '700 64px "Pixelify Sans", sans-serif'; c.fillText((b && b.label) || 'LAPANGAN GOTONG ROYONG', 384, 82, 720);
        c.fillStyle = '#ffe08a'; c.font = '700 34px "Pixelify Sans", sans-serif'; c.fillText((b && b.sub) || '', 384, 158, 720); });
      const m = new THREE.MeshStandardMaterial({ map: t, roughness: .8 });
      for (const [z, ry] of [[3.36, 0], [3.24, Math.PI]]) { const pl = new THREE.Mesh(new THREE.PlaneGeometry(2.6, .75), m); pl.position.set(0, 1.45, z); pl.rotation.y = ry; g.add(pl); }
      box(g, '#5e3b22', 2.7, .85, .08, 0, 1.02, 3.3);
    } },
  // ep 28 (komentar @vcxn.mx "tambahin pemadam kebakaran"): a red fire post with an open garage, a watch tower with a siren
  // light and the fire engine parked on the apron (g.userData.truck: unbaked, so a shot can drive it; truck.userData.hose / spray)
  posdamkar: { n: 'Pos Pemadam Kebakaran', w: 4, h: 6, land: true, scale: 1.5,
    build(g, b) {
      const tex = (w, h, draw) => { const c = document.createElement('canvas'); c.width = w; c.height = h; draw(c.getContext('2d')); const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 4; return t; };
      box(g, '#bdb5a2', 2.6, .06, 3.8, 0, 0, 0);                                                        // concrete apron
      for (let i = 0; i < 5; i++) box(g, i % 2 ? '#f2c230' : '#2b2b2b', .3, .008, .12, -.6 + i * .3, .06, .3);   // hazard stripe at the door
      box(g, '#c0392b', 2.5, 1.6, 2.1, 0, .06, -.85);                                                  // the station (red)
      box(g, '#f4eee0', 2.56, .16, 2.16, 0, 1.66, -.85); box(g, '#9a2a20', 2.6, .1, 2.2, 0, 1.82, -.85);
      box(g, '#2b2b2b', 1.3, 1.15, .04, 0, .06, .2);                                                   // open garage door (dark inside)
      box(g, '#e6e0d0', 1.42, .08, .06, 0, 1.21, .21); for (const x of [-.71, .71]) box(g, '#e6e0d0', .06, 1.15, .06, x, .06, .21);
      for (const x of [-1.0, 1.0]) box(g, windowMat, .3, .35, .04, x, .85, .2);
      // watch tower with the siren light on the back left
      box(g, '#c0392b', .7, 2.7, .7, -.85, .06, -1.55); box(g, '#f4eee0', .8, .1, .8, -.85, 2.76, -1.55); roof4(g, '#7c2f28', 1.0, .35, 1.0, -.85, 2.86, -1.55);
      const siren = add(g, G.sph, new THREE.MeshStandardMaterial({ color: '#ff3b30', emissive: '#ff2a1a', emissiveIntensity: 1.2, flatShading: true }), .1, .1, .1, -.85, 3.3, -1.55); g.userData.siren = siren;
      // hose reel on the wall and a fire hydrant
      add(g, G.cyl8, '#f2c230', .22, .08, .22, 1.0, .5, .21).rotation.x = Math.PI / 2; add(g, G.cyl8, '#d0483a', .14, .1, .14, 1.0, .5, .23).rotation.x = Math.PI / 2;
      add(g, G.cyl8, '#d0483a', .08, .32, .08, 1.15, .22, 1.3); add(g, G.sph, '#d0483a', .08, .06, .08, 1.15, .38, 1.3); box(g, '#d0483a', .22, .05, .05, 1.15, .24, 1.3);
      // sign over the door, both faces
      const t = tex(512, 128, c => { c.fillStyle = '#f4eee0'; c.fillRect(0, 0, 512, 128); c.fillStyle = '#c0392b'; c.textAlign = 'center'; c.textBaseline = 'middle'; c.font = '700 66px "Pixelify Sans", sans-serif'; c.fillText((b && b.label) || 'POS DAMKAR', 256, 50, 490); c.font = '700 26px "Pixelify Sans", sans-serif'; c.fillStyle = '#2b2b2b'; c.fillText((b && b.sub) || 'siaga 24 jam', 256, 102, 490); });
      const sg = new THREE.Mesh(new THREE.PlaneGeometry(1.5, .37), new THREE.MeshStandardMaterial({ map: t, roughness: .8 })); sg.position.set(0, 1.47, .22); g.add(sg);
      // the fire engine
      const tr = new THREE.Group(); tr.position.set(0, .06, .85); g.add(tr); g.userData.truck = tr;
      const R = '#d0302a';
      box(tr, R, .78, .55, 1.25, 0, .18, -.25); box(tr, R, .78, .66, .55, 0, .18, .62); box(tr, '#2f4a5a', .7, .26, .02, 0, .52, .9);   // body, cab, windscreen
      for (const x of [-.395, .395]) box(tr, '#2f4a5a', .02, .22, .32, x, .54, .64);
      box(tr, '#f4eee0', .8, .06, 1.8, 0, .44, .0); box(tr, '#e6e0d0', .82, .05, .06, 0, .18, .9);   // white stripe, bumper
      for (const x of [-.3, .3]) box(tr, '#ffe9a8', .12, .07, .02, x, .27, .9);
      box(tr, '#bfc3c7', .06, .06, 1.3, -.24, .76, -.3); box(tr, '#bfc3c7', .06, .06, 1.3, .24, .76, -.3); for (let i = 0; i < 5; i++) box(tr, '#bfc3c7', .5, .04, .04, 0, .78, -.85 + i * .27);   // ladder
      for (const [x, z] of [[-.4, .55], [.4, .55], [-.4, -.55], [.4, -.55]]) add(tr, G.cyl8, '#1d1d1d', .17, .1, .17, x, .17, z).rotation.z = Math.PI / 2;
      const lb = new THREE.MeshStandardMaterial({ color: '#3b6dff', emissive: '#2a5bff', emissiveIntensity: 1.0, flatShading: true }), lr = new THREE.MeshStandardMaterial({ color: '#ff3b30', emissive: '#ff2a1a', emissiveIntensity: 1.0, flatShading: true });
      tr.userData.lights = [box(tr, lr, .14, .08, .1, -.2, .84, .62), box(tr, lb, .14, .08, .1, .2, .84, .62)];
      const reel = add(tr, G.cyl8, '#f2c230', .16, .2, .16, 0, .9, -.6); reel.rotation.z = Math.PI / 2;
      // the nozzle on the roof (a spray made of droplets, hidden unless a shot turns it on)
      const hose = new THREE.Group(); hose.position.set(0, .95, .25); tr.add(hose); tr.userData.hose = hose;
      box(hose, '#bfc3c7', .08, .08, .45, 0, 0, .1);
      const wm = new THREE.MeshStandardMaterial({ color: '#cfefff', emissive: '#7fc8ff', emissiveIntensity: .4, transparent: true, opacity: .8, depthWrite: false });
      const spray = new THREE.Group(); spray.visible = false; hose.add(spray); tr.userData.spray = spray;
      for (let i = 0; i < 40; i++) { const d = new THREE.Mesh(G.sph, wm); d.scale.setScalar(.04 + (i % 4) * .015); spray.add(d); }
    } },
  // ep 29 (komentar @muhamatferos197 "bikin pelabuhan kak aku pengen jadi nelayan"): a walkable fishing harbour on the shallow
  // bay east of the pier. Deck over the whole footprint (water + walk = plank cells), an entrance arch facing the beach (-z),
  // a little fish-auction shed, fish crates, bollards, lamps and a moored fishing boat KM NELAYAN BARU (g.userData.boat).
  pelabuhan: { n: 'Pelabuhan Nelayan', w: 4, h: 4, water: true, walk: true, clearTrees: true, clear: 2,
    build(g, b) {
      const tex = (w, h, draw) => { const c = document.createElement('canvas'); c.width = w; c.height = h; draw(c.getContext('2d')); const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 4; return t; };
      // deck planks, a darker rim, pilings
      for (let i = 0; i < 13; i++) box(g, i % 2 ? '#b07a4a' : '#9a663c', 3.9, .08, .29, 0, .22, -1.8 + i * .3);
      for (const [sx, sz, x, z] of [[4.0, .12, 0, -1.98], [4.0, .12, 0, 1.98], [.12, 4.0, -1.98, 0], [.12, 4.0, 1.98, 0]]) box(g, '#6b4426', sx, .1, sz, x, .2, z);
      for (const x of [-1.9, -.65, .65, 1.9]) for (const z of [-1.9, -.3, 1.9]) add(g, G.cyl6, '#5e3b22', .09, 1.8, .09, x, -.6, z);
      // bollards and rope along the sea side
      for (const x of [-1.5, -.2, 1.1]) { cyl(g, '#2b2b2b', .09, .22, x, .3, 1.82, 8); cyl(g, '#2b2b2b', .12, .04, x, .5, 1.82, 8); }
      // lamps on the two sea corners
      for (const x of [-1.85, 1.85]) { cyl(g, '#3a3a3a', .04, 1.9, x, .3, 1.85); const l = add(g, G.sph, new THREE.MeshStandardMaterial({ color: '#ffe9a8', emissive: '#ffcf70', emissiveIntensity: .9, flatShading: true }), .13, .13, .13, x, 2.25, 1.85); l.castShadow = false; }
      // entrance arch facing the beach, sign on both faces
      for (const x of [-.75, .75]) box(g, '#2f6f8f', .12, 2.4, .12, x, .3, -1.85);
      box(g, '#2f6f8f', 1.8, .1, .14, 0, 2.7, -1.85);
      const t = tex(512, 160, c => { c.fillStyle = '#f4eee0'; c.fillRect(0, 0, 512, 160); c.fillStyle = '#2f6f8f'; c.fillRect(0, 0, 512, 10); c.fillRect(0, 150, 512, 10); c.textAlign = 'center'; c.textBaseline = 'middle'; c.font = '700 62px "Pixelify Sans", sans-serif'; c.fillText((b && b.label) || 'PELABUHAN NELAYAN', 256, 62, 490); c.font = '700 28px "Pixelify Sans", sans-serif'; c.fillStyle = '#2b2b2b'; c.fillText((b && b.sub) || 'Pulau Aru', 256, 122, 490); });
      const sm = new THREE.MeshStandardMaterial({ map: t, roughness: .8 });
      box(g, '#2f6f8f', 1.76, .6, .05, 0, 2.08, -1.85);
      const sg = new THREE.Mesh(new THREE.PlaneGeometry(1.7, .53), sm); sg.position.set(0, 2.38, -1.88); sg.rotation.y = Math.PI; g.add(sg);
      const sg2 = new THREE.Mesh(new THREE.PlaneGeometry(1.7, .53), sm); sg2.position.set(0, 2.38, -1.82); g.add(sg2);
      // fish-auction shed on the west half: four posts, a tin roof, a table with fish, a little sign
      for (const [x, z] of [[-1.85, -1.1], [-.55, -1.1], [-1.85, .5], [-.55, .5]]) box(g, '#8a5a34', .1, 1.9, .1, x, .3, z);
      box(g, '#7f8c8d', 1.6, .06, 1.9, -1.2, 2.2, -.3); box(g, '#95a5a6', 1.65, .05, .1, -1.2, 2.15, .66);
      box(g, '#d9cfb8', 1.0, .07, .55, -1.2, .95, -.3); for (const [x, z] of [[-1.6, -.5], [-.8, -.5], [-1.6, -.1], [-.8, -.1]]) box(g, '#8a5a34', .06, .65, .06, x, .3, z);
      const fishM = new THREE.MeshStandardMaterial({ color: '#8fb3c9', metalness: .3, roughness: .4, flatShading: true });
      for (let i = 0; i < 4; i++) { const f = add(g, G.sph, fishM, .2, .05, .07, -1.55 + i * .23, 1.05, -.3 + (i % 2 ? .1 : -.1)); f.rotation.y = .4 * (i % 2 ? 1 : -1); }
      const ts = tex(256, 64, c => { c.fillStyle = '#c0392b'; c.fillRect(0, 0, 256, 64); c.fillStyle = '#fff'; c.textAlign = 'center'; c.textBaseline = 'middle'; c.font = '700 34px "Pixelify Sans", sans-serif'; c.fillText('LELANG IKAN', 128, 34, 240); });
      const ls = new THREE.Mesh(new THREE.PlaneGeometry(1.0, .25), new THREE.MeshStandardMaterial({ map: ts, side: THREE.DoubleSide })); ls.position.set(-1.2, 1.95, .71); g.add(ls);
      // crates of fish and a net pile on the east side
      for (const [x, z, c] of [[1.4, -1.2, '#2e86c1'], [1.4, -.75, '#e67e22'], [.95, -1.2, '#2e86c1']]) { box(g, c, .4, .26, .38, x, .3, z); for (let k = 0; k < 2; k++) add(g, G.sph, fishM, .14, .04, .05, x - .08 + k * .16, .58, z); }
      add(g, G.dode, '#6d8a4e', .35, .14, .3, 1.35, .38, -.1);
      // flag pole
      cyl(g, '#d0d0d0', .03, 2.6, 1.85, .3, -1.85); box(g, '#e03a3a', .02, .22, .45, 1.85, 2.6, -1.6); box(g, '#f4f4f4', .02, .22, .45, 1.85, 2.38, -1.6);
      // the moored fishing boat on the sea side, a small cabin and her name on both sides
      const bt = new THREE.Group(); bt.position.set(2.62, 0, .4); bt.rotation.y = -Math.PI / 2; g.add(bt); g.userData.boat = bt;
      box(bt, '#1f6fa8', 3.0, .45, 1.0, 0, -.12, 0); box(bt, '#f4eee0', 3.05, .08, 1.05, 0, .33, 0); box(bt, '#7a4b2a', 2.8, .04, .85, 0, .26, 0);
      const bow = add(bt, G.cone4, '#1f6fa8', .5, .9, .7, 1.85, .1, 0, Math.PI / 4); bow.rotation.z = -Math.PI / 2;
      box(bt, '#f4eee0', .9, .7, .75, -.6, .3, 0); box(bt, '#c0392b', 1.0, .08, .85, -.6, 1.0, 0); box(bt, '#2f4a5a', .02, .25, .5, -.14, .62, 0);
      cyl(bt, '#d0d0d0', .03, 1.5, .5, .3, 0); box(bt, '#e03a3a', .02, .18, .35, .5, 1.6, .2); box(bt, '#f4f4f4', .02, .18, .35, .5, 1.42, .2);
      const tn = tex(512, 96, c => { c.fillStyle = '#1f6fa8'; c.fillRect(0, 0, 512, 96); c.fillStyle = '#fff'; c.textAlign = 'center'; c.textBaseline = 'middle'; c.font = '700 54px "Pixelify Sans", sans-serif'; c.fillText((b && b.boat) || 'KM NELAYAN BARU', 256, 50, 500); });
      const nm = new THREE.MeshStandardMaterial({ map: tn });
      for (const s of [-1, 1]) { const p = new THREE.Mesh(new THREE.PlaneGeometry(2.0, .3), nm); p.position.set(.35, .1, s * .505); if (s < 0) p.rotation.y = Math.PI; bt.add(p); }
      cyl(g, '#2b2b2b', .09, .22, 1.8, .3, .9, 8); box(g, '#c9b48a', .5, .03, .03, 1.95, .4, .9);   // east bollard + mooring rope
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
// Performance: a building is built from dozens of small boxes; draw calls (not triangles) are what make the island
// heavy, so after building we bake every plain mesh into one mesh per material. Textured, transparent or animated
// parts (anything reachable from g.userData, e.g. flames, cloud steps) stay as they are.
const _m = new THREE.Matrix4(), _inv = new THREE.Matrix4();
export function bake(root) {
  root.updateMatrixWorld(true); _inv.copy(root.matrixWorld).invert();
  const keep = new Set();
  for (const v of Object.values(root.userData)) if (v && v.isObject3D) v.traverse(o => keep.add(o));
  const groups = new Map(), done = [];
  root.traverse(o => {
    if (!o.isMesh || o.isInstancedMesh || keep.has(o) || !o.visible) return;
    const m = o.material; if (Array.isArray(m) || m.map || m.transparent || m.side === THREE.DoubleSide) return;
    let k = groups.get(m); if (!k) groups.set(m, k = { list: [], cast: false, recv: false });
    k.list.push(o); k.cast = k.cast || o.castShadow; k.recv = k.recv || o.receiveShadow;
  });
  for (const [mat, k] of groups) {
    if (k.list.length < 2) continue;
    let n = 0; const parts = [];
    for (const o of k.list) {
      const geo = o.geometry.index ? o.geometry.toNonIndexed() : o.geometry;
      _m.multiplyMatrices(_inv, o.matrixWorld);
      const pos = geo.attributes.position, nor = geo.attributes.normal; parts.push({ pos, nor, mat4: _m.clone(), nm: new THREE.Matrix3().getNormalMatrix(_m) }); n += pos.count;
      if (geo !== o.geometry) geo.dispose();
    }
    const P = new Float32Array(n * 3), N = new Float32Array(n * 3), v = new THREE.Vector3(); let off = 0;
    for (const { pos, nor, mat4, nm } of parts) {
      for (let i = 0; i < pos.count; i++, off++) {
        v.fromBufferAttribute(pos, i).applyMatrix4(mat4); P.set([v.x, v.y, v.z], off * 3);
        if (nor) { v.fromBufferAttribute(nor, i).applyMatrix3(nm).normalize(); N.set([v.x, v.y, v.z], off * 3); }
      }
    }
    const geo = new THREE.BufferGeometry(); geo.setAttribute('position', new THREE.BufferAttribute(P, 3)); geo.setAttribute('normal', new THREE.BufferAttribute(N, 3));
    geo.computeBoundingSphere();
    const mesh = new THREE.Mesh(geo, mat); mesh.castShadow = k.cast; mesh.receiveShadow = k.recv; mesh.userData.baked = true;
    for (const o of k.list) o.parent.remove(o);
    root.add(mesh); done.push(mesh);
  }
  return done.length;
}
export function buildBuilding(b) {
  const d = BT[b.type]; const g = new THREE.Group();
  if (d.scale) { const inner = new THREE.Group(); inner.scale.setScalar(d.scale); g.add(inner); d.build(inner, b); Object.assign(g.userData, inner.userData); } else d.build(g, b);
  if (!d.noBake && !d.water) bake(g);
  g.userData.def = d; return g;
}

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
// ep 33: the sandal thief, a seagull (camar) holding a sandal in its beak. Faces +z; wings in userData for flapping.
export function seagull() {
  const g = new THREE.Group();
  add(g, G.sph, '#f7f7f2', .16, .14, .26, 0, .22, 0); add(g, G.sph, '#f7f7f2', .1, .1, .1, 0, .36, .2);
  add(g, G.cone4, '#9aa3ad', .08, .16, .05, 0, .24, -.3).rotation.x = -Math.PI / 2;
  const bk = add(g, G.cone4, '#f2b632', .035, .12, .035, 0, .35, .33); bk.rotation.x = Math.PI / 2; add(g, G.box, '#d0483a', .02, .02, .02, 0, .335, .34);
  for (const x of [-.055, .055]) add(g, G.sph, '#111111', .018, .018, .018, x, .38, .27);
  for (const x of [-.05, .05]) { add(g, G.cyl6, '#f2a03a', .012, .12, .012, x, .06, 0); add(g, G.box, '#f2a03a', .05, .01, .06, x, .005, .02); }
  const wing = s => { const w = new THREE.Group(); w.position.set(s * .12, .27, .02); add(w, G.box, '#c9ced4', .34, .025, .2, s * .17, 0, 0); add(w, G.box, '#2b2d33', .1, .026, .18, s * .37, 0, -.01); g.add(w); return w; };
  const wl = wing(-1), wr = wing(1);
  const sd = new THREE.Group(); sd.position.set(0, .3, .44); add(sd, G.box, '#ff8a3d', .12, .03, .28, 0, 0, 0); add(sd, G.box, '#222222', .13, .04, .03, 0, .02, -.06); sd.rotation.set(.3, .4, 0); g.add(sd);
  g.userData = { wl, wr, sandal: sd };
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
