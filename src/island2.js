// The second island ("Pulau Seberang"): reachable only by ship. Deterministic, like the first.
import * as THREE from 'three';
import { hash, fbm, SEED, DEEP, SHALLOW, SAND, GRASS, HILL } from './world.js';
import { mat, makeInstanced, G, box } from './models.js';
import { BT } from './models.js';

export const W2 = 64, H2 = 64, OX = 128, OZ = -34; // world position of the island centre
const S2 = SEED + 777;
function hgt(x, y) {
  const nx = (x - W2 / 2) / (W2 / 2), ny = (y - H2 / 2) / (H2 / 2);
  const d = Math.sqrt(nx * nx * 1.15 + ny * ny * .95);
  const peak = Math.max(0, 1 - Math.hypot(x - 40, y - 26) / 10) * .38; // old volcano in the north-east
  return .96 - d * .98 + (fbm(x / 11 + 300, y / 11 + 300, S2) - .5) * .5 + peak;
}
function elev(a) {
  if (a < 0.30) return -1.6 - (0.30 - a) * 6;
  if (a < 0.36) return -1.6 + (a - 0.30) / 0.06 * 1.45;
  if (a < 0.41) return -0.15 + (a - 0.36) / 0.05 * 0.6;
  return 0.45 + (a - 0.41) * 6 + Math.max(0, a - 0.7) * 18;
}
export const tile2 = new Uint8Array(W2 * H2);
for (let y = 0; y < H2; y++) for (let x = 0; x < W2; x++) { const a = hgt(x, y); tile2[y * W2 + x] = a < .30 ? DEEP : a < .36 ? SHALLOW : a < .41 ? SAND : a < .76 ? GRASS : HILL; }
const VW = W2 + 1;
const Hv2 = new Float32Array(VW * (H2 + 1));
for (let j = 0; j <= H2; j++) for (let i = 0; i <= W2; i++) Hv2[j * VW + i] = elev(hgt(i - .5, j - .5));

export const inside2 = (x, z) => Math.abs(x - OX) < W2 / 2 && Math.abs(z - OZ) < H2 / 2;
export const c2x = x => Math.floor(x - OX + W2 / 2), c2y = z => Math.floor(z - OZ + H2 / 2);
export const T2 = (cx, cy) => (cx < 0 || cy < 0 || cx >= W2 || cy >= H2) ? DEEP : tile2[cy * W2 + cx];
export const w2 = (cx, cy) => [OX + cx - W2 / 2 + .5, OZ + cy - H2 / 2 + .5];
export function ground2(x, z) {
  const gx = Math.max(0, Math.min(W2 - .001, x - OX + W2 / 2)), gz = Math.max(0, Math.min(H2 - .001, z - OZ + H2 / 2));
  const i = Math.floor(gx), j = Math.floor(gz), fx = gx - i, fz = gz - j;
  const a = Hv2[j * VW + i], b = Hv2[j * VW + i + 1], c = Hv2[(j + 1) * VW + i], d = Hv2[(j + 1) * VW + i + 1];
  if (fx + fz < 1) return a + (b - a) * fx + (c - a) * fz;
  return d + (c - d) * (1 - fx) + (b - d) * (1 - fz);
}

// ---------- landmarks ----------
const isL = (x, y) => T2(x, y) >= SAND;
export const LM2 = {};
{ let x = 0; while (x < W2 && !isL(x, 32)) x++; LM2.beach = [x + 1, 32]; }          // landing beach faces the first island
{ let x = 0; while (x < W2 && !isL(x, 31)) x++; LM2.dock = [x - 4, 31]; }             // old broken dock reaching into the water
LM2.ruins = [LM2.beach[0] + 8, 29];
LM2.chest = [LM2.ruins[0] + 1, LM2.ruins[1] + 1];
LM2.circle = [38, 30];
export const solid2 = new Uint8Array(W2 * H2);
export const plank2 = new Uint8Array(W2 * H2);
for (let x = LM2.dock[0]; x < LM2.dock[0] + 6; x++) plank2[31 * W2 + x] = 1;

const keep = new Uint8Array(W2 * H2);
const clear = (p, r) => { for (let dy = -r; dy <= r; dy++) for (let dx = -r; dx <= r; dx++) { const x = p[0] + dx, y = p[1] + dy; if (x >= 0 && y >= 0 && x < W2 && y < H2) keep[y * W2 + x] = 1; } };
clear(LM2.beach, 3); clear(LM2.ruins, 4); clear(LM2.circle, 5);
for (let x = LM2.beach[0]; x < LM2.ruins[0]; x++) clear([x, 31], 1);
const trees2 = [], rocks2 = [];
for (let y = 0; y < H2; y++) for (let x = 0; x < W2; x++) {
  const t = tile2[y * W2 + x], i = y * W2 + x; if (keep[i]) continue;
  const r = hash(x, y, S2 + 5), f = fbm(x / 7 + 90, y / 7 + 90, S2 + 9);
  if ((t === GRASS || t === HILL) && ((f > .52 && r < .55) || r < .05)) { trees2.push({ x, y, kind: t === HILL ? 'pine' : 'round', s: .8 + hash(x, y, 7) * .7, c: hash(x, y, 8) }); solid2[i] = 1; }
  else if ((t === HILL && r > .8) || (t === SAND && r > .975)) { rocks2.push({ x, y, s: .6 + hash(x, y, 9) * .9 }); solid2[i] = 1; }
  else if (t === SAND && r < .045) { trees2.push({ x, y, kind: 'palm', s: .9 + hash(x, y, 10) * .5 }); solid2[i] = 1; }
}
for (let i = 0; i < W2 * H2; i++) if (tile2[i] === DEEP && !plank2[i]) solid2[i] = 1;
// ruins and stone circle footprints
for (let dy = 0; dy < 3; dy++) for (let dx = 0; dx < 4; dx++) if (!(dy === 2 && dx === 1)) solid2[(LM2.ruins[1] + dy) * W2 + LM2.ruins[0] + dx] = 1;
solid2[(LM2.ruins[1] + 1) * W2 + LM2.ruins[0] + 1] = 0; solid2[(LM2.ruins[1] + 1) * W2 + LM2.ruins[0] + 2] = 0; // inside the hut is open
const circleStones = []; for (let k = 0; k < 8; k++) { const a = k / 8 * Math.PI * 2; const cx = Math.round(LM2.circle[0] + Math.cos(a) * 3.2), cy = Math.round(LM2.circle[1] + Math.sin(a) * 3.2); circleStones.push([cx, cy, a]); solid2[cy * W2 + cx] = 1; }

export function walkable2(x, z) {
  for (const [dx, dz] of [[-.28, -.2], [.28, -.2], [-.28, .2], [.28, .2]]) { const cx = c2x(x + dx), cy = c2y(z + dz); if (cx < 0 || cy < 0 || cx >= W2 || cy >= H2 || solid2[cy * W2 + cx]) return false; }
  return true;
}
export const surface2 = (x, z) => { const i = c2y(z) * W2 + c2x(x); if (plank2[i]) return .26; return Math.max(ground2(x, z), -.55); };
export const shallow2 = (x, z) => { const i = c2y(z) * W2 + c2x(x); return tile2[i] === SHALLOW && !plank2[i]; };

// ---------- meshes ----------
export function buildIsland2(scene) {
  const g = new THREE.Group(); scene.add(g);
  const pos = [], cols = [], c = new THREE.Color();
  const P = { seabed: new THREE.Color('#1d5f73'), seabed2: new THREE.Color('#3b8a8c'), wet: new THREE.Color('#c9ae78'), sand: new THREE.Color('#e9d6a4'), sand2: new THREE.Color('#ddc58e'), g1: new THREE.Color('#6fb455'), g2: new THREE.Color('#5ea44a'), g3: new THREE.Color('#82c25e'), hill: new THREE.Color('#5b8b4a'), rock: new THREE.Color('#7d7a72'), rock2: new THREE.Color('#5f5c57') };
  for (let y = 0; y < H2; y++) for (let x = 0; x < W2; x++) {
    const x0 = OX + x - W2 / 2, z0 = OZ + y - H2 / 2;
    const a = Hv2[y * VW + x], b = Hv2[y * VW + x + 1], cc = Hv2[(y + 1) * VW + x], d = Hv2[(y + 1) * VW + x + 1];
    [[[x0, a, z0], [x0, cc, z0 + 1], [x0 + 1, b, z0]], [[x0 + 1, b, z0], [x0, cc, z0 + 1], [x0 + 1, d, z0 + 1]]].forEach((tri, k) => {
      const avg = (tri[0][1] + tri[1][1] + tri[2][1]) / 3, n = hash(x * 2 + k, y, S2 + 91);
      if (avg < -1) c.copy(P.seabed).lerp(P.seabed2, n * .5);
      else if (avg < -.05) c.copy(P.seabed2).lerp(P.wet, Math.min(1, (avg + 1) / .95));
      else if (avg < .62) c.copy(n > .5 ? P.sand : P.sand2);
      else if (avg < 3.2) c.copy(n < .33 ? P.g1 : n < .66 ? P.g2 : P.g3);
      else if (avg < 4.4) c.copy(P.hill).lerp(P.rock, (avg - 3.2) / 1.2 * .7);
      else c.copy(n > .5 ? P.rock : P.rock2);
      c.offsetHSL(0, 0, (n - .5) * .04);
      for (const v of tri) { pos.push(...v); cols.push(c.r, c.g, c.b); }
    });
  }
  const geo = new THREE.BufferGeometry(); geo.setAttribute('position', new THREE.Float32BufferAttribute(pos, 3)); geo.setAttribute('color', new THREE.Float32BufferAttribute(cols, 3)); geo.computeVertexNormals();
  const terrain = new THREE.Mesh(geo, new THREE.MeshStandardMaterial({ vertexColors: true, flatShading: true, roughness: .95 })); terrain.receiveShadow = true; g.add(terrain);

  // nature
  const m4 = new THREE.Matrix4(), q = new THREE.Quaternion(), e = new THREE.Euler(), v = new THREE.Vector3(), sc = new THREE.Vector3();
  const set = (mesh, i, x, y, z, sx, sy, sz, ry = 0) => { e.set(0, ry, 0); q.setFromEuler(e); m4.compose(v.set(x, y, z), q, sc.set(sx, sy, sz)); mesh.setMatrixAt(i, m4); };
  const round = trees2.filter(t => t.kind === 'round'), pines = trees2.filter(t => t.kind === 'pine'), palms = trees2.filter(t => t.kind === 'palm');
  const trunks = makeInstanced(new THREE.CylinderGeometry(.1, .16, 1, 5), mat('#5e4128'), round.length + pines.length);
  const canopy = makeInstanced(new THREE.IcosahedronGeometry(1, 0), new THREE.MeshStandardMaterial({ flatShading: true, roughness: .9 }), round.length);
  const cones = makeInstanced(new THREE.ConeGeometry(1, 1, 6), new THREE.MeshStandardMaterial({ flatShading: true, roughness: .9 }), pines.length * 2);
  const greens = ['#2f7a48', '#3a8f52', '#2a6b4a', '#4a9a4a'].map(x => new THREE.Color(x));
  let ti = 0, ci = 0, pi = 0;
  for (const t of round) { const [x, z] = w2(t.x, t.y), y = ground2(x, z); set(trunks, ti++, x, y + .7 * t.s, z, t.s, 1.4 * t.s, t.s); set(canopy, ci, x, y + 1.8 * t.s, z, 1.1 * t.s, 1 * t.s, 1.1 * t.s, t.c * 6); canopy.setColorAt(ci++, greens[(t.c * 4) | 0]); }
  for (const t of pines) { const [x, z] = w2(t.x, t.y), y = ground2(x, z); set(trunks, ti++, x, y + .4 * t.s, z, t.s * .9, .8 * t.s, t.s * .9); set(cones, pi, x, y + 1.3 * t.s, z, .85 * t.s, 1.5 * t.s, .85 * t.s); cones.setColorAt(pi++, greens[2]); set(cones, pi, x, y + 2.15 * t.s, z, .6 * t.s, 1.1 * t.s, .6 * t.s); cones.setColorAt(pi++, greens[0]); }
  for (const mm of [trunks, canopy, cones]) { mm.instanceMatrix.needsUpdate = true; if (mm.instanceColor) mm.instanceColor.needsUpdate = true; g.add(mm); }
  for (const t of palms) { const pg = new THREE.Group(); BT.kelapa.build(pg); const [x, z] = w2(t.x, t.y); pg.position.set(x, ground2(x, z), z); pg.rotation.y = t.x * 1.7; pg.scale.setScalar(t.s); g.add(pg); }
  const rk = makeInstanced(new THREE.DodecahedronGeometry(1, 0), mat('#7f7c74'), rocks2.length);
  rocks2.forEach((r, i) => { const [x, z] = w2(r.x, r.y); set(rk, i, x, ground2(x, z) + .2 * r.s, z, .6 * r.s, .45 * r.s, .55 * r.s, r.x); }); rk.instanceMatrix.needsUpdate = true; g.add(rk);

  // old dock (broken planks)
  { const dg = new THREE.Group(); const [x, z] = w2(LM2.dock[0], LM2.dock[1]); dg.position.set(x - .5, 0, z); g.add(dg);
    for (let i = 0; i < 18; i++) { if (i === 5 || i === 11) continue; box(dg, i % 2 ? '#7a5a3a' : '#6b4a2b', .3, .08, .9, .2 + i * .33, .2, 0).rotation.y = (hash(i, 3, 4) - .5) * .15; }
    for (let i = 0; i < 4; i++) for (const zz of [-.42, .42]) box(dg, '#4a3320', .1, 1.8, .1, .2 + i * 1.8, -1.5, zz); }
  // ruined hut
  { const rg = new THREE.Group(); const [x, z] = w2(LM2.ruins[0] + 1.5, LM2.ruins[1] + 1); rg.position.set(x, ground2(x, z), z); g.add(rg);
    const st = '#9a968c', st2 = '#86827a';
    box(rg, st, 4, 1.4, .3, 0, 0, -1.35); box(rg, st2, .3, 1.1, 2.7, -1.85, 0, 0); box(rg, st, .3, .7, 2.7, 1.85, 0, 0); box(rg, st2, 1.2, 1, .3, -1.4, 0, 1.35); box(rg, st, 1.2, .5, .3, 1.4, 0, 1.35);
    const beam = box(rg, '#5e4128', 4.2, .14, .14, 0, 1.2, 0); beam.rotation.z = .25; beam.position.y = .9;
    for (let i = 0; i < 6; i++) box(rg, '#7d6a3a', .5, .05, 1.4, -1.5 + i * .55, 0, -.2 + (i % 2) * .3).rotation.y = i * .5;
    // chest
    const ch = new THREE.Group(); ch.position.set(-.6, 0, -.6); rg.add(ch); box(ch, '#6b4226', .8, .45, .5, 0, 0, 0); box(ch, '#7d5030', .82, .18, .52, 0, .45, 0); box(ch, '#d4a84a', .84, .06, .06, 0, .3, .26); box(ch, '#d4a84a', .1, .14, .06, 0, .44, .27);
    g.userData.chest = ch; }
  // stone circle on the hill
  for (const [cx, cy, a] of circleStones) { const [x, z] = w2(cx, cy); const s = box(g, '#8d8a82', .5, 1.6 + hash(cx, cy, 2) * .8, .35, x, ground2(x, z) - .1, z); s.rotation.y = -a; }
  { const [x, z] = w2(LM2.circle[0], LM2.circle[1]); box(g, '#6f6c66', 1.4, .35, 1.4, x, ground2(x, z) - .1, z); }
  return g;
}

export function interactables2() {
  const at = (p, dx = 0, dz = 0) => { const [x, z] = w2(p[0], p[1]); return { x: x + dx, z: z + dz }; };
  return [
    { ...at(LM2.chest, 0, 1), key: 'chest', label: 'Buka peti tua', r: 1.6 },
    { ...at(LM2.circle, 0, 0), key: 'circle', label: 'Periksa lingkaran batu', r: 2.4 },
    { ...at(LM2.beach, 0, 0), key: 'beach', label: 'Lihat pantai', r: 1.5 },
  ];
}
export const LORE = {
  chest: 'Di dalam peti ada peta yang digambar tangan. Pulau Netizen dilingkari tinta merah. Di pojoknya tertulis kecil: "Untuk Aru, kalau aku tidak kembali."',
  circle: 'Delapan batu berdiri melingkar menghadap ke barat, tepat ke arah mercusuar. Seseorang pernah menyalakan api di tengahnya.',
  beach: 'Ada bekas jejak kaki yang sudah lama tertimbun pasir, menuju ke reruntuhan rumah.',
};
