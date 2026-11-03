// Island generation: deterministic from SEED so every visitor sees the same island.
import * as THREE from 'three';

export const W = 112, H = 112, SEED = 20261102;
// tile ids
export const DEEP = 0, SHALLOW = 1, SAND = 2, GRASS = 3, HILL = 4;

export function hash(x, y, s) {
  let n = (x * 374761393 + y * 668265263 + s * 1442695041) | 0;
  n = (n ^ (n >>> 13)) * 1274126177 | 0; n = n ^ (n >>> 16);
  return (n >>> 0) / 4294967296;
}
function vnoise(x, y, s) {
  const ix = Math.floor(x), iy = Math.floor(y), fx = x - ix, fy = y - iy;
  const u = fx * fx * (3 - 2 * fx), v = fy * fy * (3 - 2 * fy);
  const a = hash(ix, iy, s), b = hash(ix + 1, iy, s), c = hash(ix, iy + 1, s), d = hash(ix + 1, iy + 1, s);
  return a + (b - a) * u + (c - a) * v + (a - b - c + d) * u * v;
}
export function fbm(x, y, s) {
  let t = 0, a = .5, f = 1, n = 0;
  for (let i = 0; i < 4; i++) { t += vnoise(x * f, y * f, s + i * 17) * a; n += a; a *= .5; f *= 2; }
  return t / n;
}
function hgtAt(x, y) {
  const nx = (x - W / 2) / (W / 2), ny = (y - H / 2) / (H / 2);
  const d = Math.sqrt(nx * nx * 1.05 + ny * ny * 1.2);
  return 0.92 - d * 0.86 + (fbm(x / 20, y / 20, SEED) - 0.5) * 0.62;
}
function elev(a) {
  if (a < 0.30) return -1.6 - (0.30 - a) * 6;
  if (a < 0.36) return -1.6 + (a - 0.30) / 0.06 * 1.45;
  if (a < 0.41) return -0.15 + (a - 0.36) / 0.05 * 0.6;
  return 0.45 + (a - 0.41) * 6 + Math.max(0, a - 0.7) * 18;
}

const tileOf = a => a < 0.30 ? DEEP : a < 0.36 ? SHALLOW : a < 0.41 ? SAND : a < 0.76 ? GRASS : HILL;
export const tile = new Uint8Array(W * H);
const baseA = new Float32Array(W * H);
for (let y = 0; y < H; y++) for (let x = 0; x < W; x++) { const a = hgtAt(x, y); baseA[y * W + x] = a; tile[y * W + x] = tileOf(a); }
// vertex heights at cell corners
const VW = W + 1;
export const Hv = new Float32Array(VW * (H + 1));
const baseV = new Float32Array(VW * (H + 1));
for (let j = 0; j <= H; j++) for (let i = 0; i <= W; i++) { const a = hgtAt(i - 0.5, j - 0.5); baseV[j * VW + i] = a; Hv[j * VW + i] = elev(a); }

// ---------- expansion: new land the residents asked for, one lobe per level ----------
// Each lobe joins the coast and rises to open grassland (no trees: room for new houses).
export const LOBES = [{ x: 93, y: 80, rx: 13.5, ry: 11 }, { x: 22, y: 92, rx: 12, ry: 9 }, { x: 60, y: 22, rx: 14, ry: 8 }];
function lobeA(x, y, level) {
  let best = -1;
  for (let k = 0; k < Math.min(level, LOBES.length); k++) {
    const L = LOBES[k], q = ((x - L.x) / L.rx) ** 2 + ((y - L.y) / L.ry) ** 2;
    if (q >= 1) continue;
    const s = Math.pow(1 - q, .55);
    best = Math.max(best, .24 + s * .44 + (fbm(x / 6 + 70, y / 6 + 70, SEED + 31) - .5) * .12 * s);
  }
  return best;
}
export let expansion = 0;
export const expandedCells = new Uint8Array(W * H);
/** Raise land for `level` lobes; t (0..1) blends from the old shore to the new one for the rising animation. */
export function setExpansion(level, t = 1, from = 0) {
  expansion = level;
  for (let y = 0; y < H; y++) for (let x = 0; x < W; x++) {
    const i = y * W + x, b = baseA[i], lo = Math.max(b, lobeA(x, y, from)), hi = Math.max(b, lobeA(x, y, level));
    const a = lo + (hi - lo) * t; tile[i] = tileOf(a); expandedCells[i] = hi > b + .02 ? 1 : 0;
  }
  for (let j = 0; j <= H; j++) for (let i = 0; i <= W; i++) {
    const k = j * VW + i, b = baseV[k], lo = Math.max(b, lobeA(i - .5, j - .5, from)), hi = Math.max(b, lobeA(i - .5, j - .5, level));
    Hv[k] = elev(lo + (hi - lo) * t);
  }
  applyPads();
}
// level ground under stages and markets (and the space in front where the crowd stands), easing back into the slope
let pads = [];
export function setPads(list) { pads = list || []; setExpansion(expansion, 1, expansion); }
function applyPads() {
  for (const p of pads) {
    let sum = 0, n = 0;
    for (let j = p.y0; j <= p.y1; j++) for (let i = p.x0; i <= p.x1; i++) if (i >= 0 && j >= 0 && i <= W && j <= H) { sum += Hv[j * VW + i]; n++; }
    if (!n) continue;
    const h = Math.max(.7, sum / n), m = p.margin || 3;
    for (let j = p.y0 - m; j <= p.y1 + m; j++) for (let i = p.x0 - m; i <= p.x1 + m; i++) {
      if (i < 0 || j < 0 || i > W || j > H) continue;
      const k = j * VW + i; if (Hv[k] < .3) continue;   // never pull the shore or the sea
      const d = Math.max(p.x0 - i, i - p.x1, p.y0 - j, j - p.y1, 0), w = d === 0 ? 1 : 1 - d / (m + 1), s = w * w * (3 - 2 * w);
      Hv[k] = Hv[k] + (h - Hv[k]) * s;
    }
  }
}

export const T = (x, y) => (x < 0 || y < 0 || x >= W || y >= H) ? DEEP : tile[y * W + x];
export const isLand = (x, y) => T(x, y) >= SAND;
// cell <-> world
export const cx2w = x => x - W / 2 + 0.5;
export const cy2w = y => y - H / 2 + 0.5;
export const w2cx = wx => Math.floor(wx + W / 2);
export const w2cy = wz => Math.floor(wz + H / 2);
export function groundY(wx, wz) {
  const gx = Math.max(0, Math.min(W - 0.001, wx + W / 2)), gz = Math.max(0, Math.min(H - 0.001, wz + H / 2));
  const i = Math.floor(gx), j = Math.floor(gz), fx = gx - i, fz = gz - j;
  const a = Hv[j * VW + i], b = Hv[j * VW + i + 1], c = Hv[(j + 1) * VW + i], d = Hv[(j + 1) * VW + i + 1];
  // match triangle split used by the mesh (a-c-b / b-c-d)
  if (fx + fz < 1) return a + (b - a) * fx + (c - a) * fz;
  return d + (c - d) * (1 - fx) + (b - d) * (1 - fz);
}

// ---------- landmarks ----------
const CX = W / 2 | 0, CY = H / 2 | 0;
function nearest(x, y, want) {
  for (let r = 0; r < 30; r++) for (let dy = -r; dy <= r; dy++) for (let dx = -r; dx <= r; dx++) {
    if (Math.max(Math.abs(dx), Math.abs(dy)) !== r) continue;
    if (T(x + dx, y + dy) === want) return [x + dx, y + dy];
  }
  return [x, y];
}
export const LM = {};
LM.camp = nearest(CX, CY + 5, GRASS);
{ let y = H - 1; while (y > 0 && !isLand(CX, y)) y--; LM.stone = [CX - 1, y - 2]; }
{
  let x = W - 1; while (x > 0 && !isLand(x, CY - 2)) x--; x -= 2;
  while (x > 0 && !(isLand(x, CY - 3) && isLand(x + 1, CY - 3) && isLand(x, CY - 2) && isLand(x + 1, CY - 2))) x--;
  LM.light = [x, CY - 3];
}
{ let x = 4, y = H - 8; while (!isLand(x, y) && x < W / 2) { x++; y--; } LM.wreck = [x + 1, y - 1]; }
LM.mail = [LM.camp[0] + 4, LM.camp[1] + 1];
LM.board = [LM.camp[0] - 5, LM.camp[1] + 1];
LM.fire = [LM.camp[0] + 1, LM.camp[1] + 3];
{ let y = LM.stone[1]; while (y < H - 2 && T(CX, y) !== DEEP) y++; LM.ship = [CX - 7, Math.min(H - 6, y + 4)]; }
// pier from the south beach to where the ship moors (appears at 1.000 residents)
export const PIER = (() => {
  let best = null;
  for (let x = LM.stone[0] - 6; x <= LM.stone[0] + 2; x++) {
    let y = LM.stone[1]; while (y < H - 1 && T(x, y) >= SAND) y++; const y0 = y;
    while (y < H - 1 && T(x, y) === SHALLOW) y++;
    const ok = [1, 2, 3, 4].every(k => T(x, y + k) === DEEP && T(x - 3, y + k) === DEEP && T(x + 3, y + k) === DEEP);
    if (ok && (!best || y - y0 < best.y1 - best.y0)) best = { x, y0, y1: y + 1 };
  }
  return best || { x: LM.stone[0], y0: LM.stone[1] + 2, y1: LM.stone[1] + 4 };
})();
// ship centre in world coords, hull parallel to the shore, touching the end of the pier
export const MOOR = { x: PIER.x - W / 2 + .5, z: PIER.y1 - H / 2 + 2.2, ry: 0 };

// footprints occupied by landmarks [key,x,y,w,h]
export const LMS = [
  ['stone', LM.stone[0], LM.stone[1], 2, 1], ['light', LM.light[0], LM.light[1], 2, 2],
  ['shelter', LM.camp[0] - 1, LM.camp[1], 3, 2], ['fire', LM.fire[0], LM.fire[1], 1, 1],
  ['mail', LM.mail[0], LM.mail[1], 1, 1], ['board', LM.board[0], LM.board[1], 2, 1],
  ['wreck', LM.wreck[0], LM.wreck[1], 3, 2],
];

// ---------- nature ----------
const clr = new Uint8Array(W * H);
const clearR = (p, r) => { for (let dy = -r; dy <= r; dy++) for (let dx = -r; dx <= r; dx++) { const x = p[0] + dx, y = p[1] + dy; if (x >= 0 && y >= 0 && x < W && y < H) clr[y * W + x] = 1; } };
clearR(LM.camp, 9); clearR(LM.stone, 3); clearR(LM.light, 3); clearR(LM.wreck, 3); clearR(LM.board, 2); clearR(LM.mail, 2);
// path camp -> stone stays clear
for (let i = 0; i <= 30; i++) { const x = Math.round(LM.camp[0] + (LM.stone[0] + 1 - LM.camp[0]) * i / 30), y = Math.round(LM.camp[1] + (LM.stone[1] - LM.camp[1]) * i / 30); clearR([x, y], 1); }

export const trees = [], rocks = [], tufts = [], flowers = [];
export const treeAt = new Int16Array(W * H).fill(-1), rockAt = new Int16Array(W * H).fill(-1);
for (let y = 0; y < H; y++) for (let x = 0; x < W; x++) {
  const t = tile[y * W + x], i = y * W + x;
  const r = hash(x, y, SEED + 5), f = fbm(x / 9 + 40, y / 9 + 40, SEED + 9);
  if (!clr[i]) {
    if ((t === GRASS || t === HILL) && ((f > 0.56 && r < 0.5) || r < 0.035)) {
      const kind = t === HILL || f > 0.66 ? 'pine' : 'round';
      treeAt[i] = trees.length; trees.push({ x, y, kind, s: 0.8 + hash(x, y, 77) * 0.6, c: hash(x, y, 78) });
      continue;
    }
    if ((t === HILL && r > 0.88) || (t === SAND && r > 0.985)) { rockAt[i] = rocks.length; rocks.push({ x, y, s: 0.5 + hash(x, y, 79) * 0.8 }); continue; }
    if (t === SAND && r < 0.02 && hash(x, y, SEED + 21) < .55) { treeAt[i] = trees.length; trees.push({ x, y, kind: 'palm', s: 0.9 + hash(x, y, 80) * 0.4, c: 0 }); continue; }
  }
  if (t === GRASS) {
    for (let k = 0; k < 3; k++) if (hash(x * 3 + k, y, 81) < 0.55) tufts.push({ x: x + hash(x, y * 7 + k, 82), y: y + hash(x * 7 + k, y, 83) });
    if (hash(x, y, 84) < 0.06) flowers.push({ x: x + .5, y: y + .5, c: (hash(x, y, 85) * 5) | 0 });
  }
}

// village cells: grass near camp, ordered by distance with jitter. Used for NPC homes and night lights.
export const village = [];
for (let y = 0; y < H; y++) for (let x = 0; x < W; x++) {
  if (T(x, y) >= GRASS && treeAt[y * W + x] < 0 && rockAt[y * W + x] < 0) {
    const dx = x - LM.camp[0], dy = y - LM.camp[1];
    village.push({ x, y, d: dx * dx + dy * dy, r: hash(x, y, SEED + 33) });
  }
}
village.sort((a, b) => (a.d + a.r * 500) - (b.d + b.r * 500));

// ---------- meshes ----------
const col = (h) => new THREE.Color(h);
const PAL = {
  seabed: col('#1d5f73'), seabed2: col('#3b8a8c'), wet: col('#cdb57c'), sand: col('#ecd59c'), sand2: col('#e2c88a'),
  grass: col('#7cc25a'), grass2: col('#68b04e'), grass3: col('#8fce62'), hill: col('#5e9b4a'), rock: col('#9aa08e'), rock2: col('#878c7c'), path: col('#cfae73'),
};
const pathCells = new Uint8Array(W * H);
for (let i = 0; i <= 40; i++) {
  const x = Math.round(LM.camp[0] + (LM.stone[0] + 1 - LM.camp[0]) * i / 40 + Math.sin(i / 5) * 0.8), y = Math.round(LM.camp[1] + 2 + (LM.stone[1] - LM.camp[1] - 2) * i / 40);
  if (x >= 0 && y >= 0 && x < W && y < H) pathCells[y * W + x] = 1;
}

export function buildTerrain() {
  const geo = new THREE.BufferGeometry();
  fillTerrain(geo);
  const mesh = new THREE.Mesh(geo, new THREE.MeshStandardMaterial({ vertexColors: true, flatShading: true, roughness: .95, metalness: 0 }));
  mesh.receiveShadow = true;
  mesh.name = 'terrain';
  mesh.userData.refresh = () => { fillTerrain(geo); geo.computeBoundingSphere(); geo.computeBoundingBox(); };
  return mesh;
}
function fillTerrain(geo) {
  const pos = [], cols = [];
  const c = new THREE.Color();
  for (let y = 0; y < H; y++) for (let x = 0; x < W; x++) {
    const x0 = x - W / 2, z0 = y - H / 2;
    const a = Hv[y * VW + x], b = Hv[y * VW + x + 1], cc = Hv[(y + 1) * VW + x], d = Hv[(y + 1) * VW + x + 1];
    const tris = [[[x0, a, z0], [x0, cc, z0 + 1], [x0 + 1, b, z0]], [[x0 + 1, b, z0], [x0, cc, z0 + 1], [x0 + 1, d, z0 + 1]]];
    tris.forEach((tri, k) => {
      const avg = (tri[0][1] + tri[1][1] + tri[2][1]) / 3;
      const n = hash(x * 2 + k, y, 91);
      if (avg < -1.0) c.copy(PAL.seabed).lerp(PAL.seabed2, n * .5);
      else if (avg < -0.05) c.copy(PAL.seabed2).lerp(PAL.wet, Math.min(1, (avg + 1) / 0.95));
      else if (avg < 0.62) c.copy(n > .5 ? PAL.sand : PAL.sand2);
      else if (avg < 3.4) { c.copy(n < .33 ? PAL.grass : n < .66 ? PAL.grass2 : PAL.grass3); if (pathCells[y * W + x]) c.copy(PAL.path).lerp(PAL.sand2, n * .3); }
      else if (avg < 4.6) c.copy(PAL.hill).lerp(PAL.rock, (avg - 3.4) / 1.2 * .6);
      else c.copy(n > .5 ? PAL.rock : PAL.rock2);
      c.offsetHSL(0, 0, (n - .5) * 0.04);
      for (const v of tri) { pos.push(v[0], v[1], v[2]); cols.push(c.r, c.g, c.b); }
    });
  }
  geo.setAttribute('position', new THREE.Float32BufferAttribute(pos, 3));
  geo.setAttribute('color', new THREE.Float32BufferAttribute(cols, 3));
  geo.computeVertexNormals();
}

export function buildWater() {
  const geo = new THREE.PlaneGeometry(420, 420, 105, 105);
  geo.rotateX(-Math.PI / 2);
  const mat = new THREE.MeshStandardMaterial({ color: '#2aa3bf', transparent: true, opacity: .72, roughness: .18, metalness: .05, flatShading: true });
  const mesh = new THREE.Mesh(geo, mat);
  mesh.receiveShadow = true;
  const base = geo.attributes.position.array.slice();
  mesh.userData.update = (t) => {
    const p = geo.attributes.position.array;
    for (let i = 0; i < p.length; i += 3) {
      const x = base[i], z = base[i + 2];
      p[i + 1] = Math.sin(x * .32 + t * 1.1) * .07 + Math.cos(z * .27 + t * .9) * .07 + Math.sin((x + z) * .6 + t * 1.7) * .03;
    }
    geo.attributes.position.needsUpdate = true;
  };
  const floor = new THREE.Mesh(new THREE.PlaneGeometry(600, 600).rotateX(-Math.PI / 2), new THREE.MeshBasicMaterial({ color: '#134a5c' }));
  floor.position.y = -3.2;
  return { water: mesh, floor };
}
