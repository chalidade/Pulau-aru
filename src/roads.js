// Asphalt roads (episode 6): a tidy two-lane network that starts at the president's stage and reaches every
// landmark and building. Routed with A* on the tile grid, preferring straight runs, gentle slopes and few trees.
import * as THREE from 'three';
import * as WD from './world.js';
import { W, H, tile, treeAt, rockAt, groundY } from './world.js';

const DIRS = [[1, 0], [0, 1], [-1, 0], [0, -1]];

/**
 * @param occ   Int16Array occupancy (-1 free, -2 landmark, >=0 building index); road cells are written as -3
 * @param hub   [x, y] start cell
 * @param goals array of arrays of goal cells (any cell of a group ends that route)
 */
export function planRoads(occ, hub, goals, segments) {
  const road = new Uint8Array(W * H), parentLane = new Int32Array(W * H).fill(-1);
  const land = i => tile[i] >= WD.SAND && tile[i] !== WD.SHALLOW;
  const passable = i => land(i) && (occ[i] === -1 || occ[i] === -3);
  const routes = [];
  if (segments && segments.length) return planGrid(occ, segments, goals, land, passable);
  const sorted = goals.map(g => ({ g, d: Math.min(...g.map(([x, y]) => Math.abs(x - hub[0]) + Math.abs(y - hub[1]))) })).sort((a, b) => a.d - b.d);
  for (const { g } of sorted) {
    const goalSet = new Set(g.map(([x, y]) => y * W + x).filter(i => land(i)));
    if (!goalSet.size) continue;
    const path = astar(hub, goalSet, road, passable);
    if (path) routes.push(path);
    if (path) for (const i of path) road[i] = 1;
  }
  // second lane: to the right/down of each path cell, so roads are two cells wide
  const cells = new Set();
  const marks = [];
  for (const path of routes) for (let k = 0; k < path.length; k++) {
    const i = path[k], x = i % W, y = (i / W) | 0;
    const n = path[Math.min(path.length - 1, k + 1)], p = path[Math.max(0, k - 1)];
    const horiz = Math.abs((n % W) - (p % W)) >= Math.abs(((n / W) | 0) - ((p / W) | 0));
    cells.add(i);
    const j = horiz ? i + W : i + 1;
    if (j < W * H && passable(j)) { cells.add(j); parentLane[j] = i; }
    // a dash on the centre line every other cell along straight runs
    const straight = k > 0 && k < path.length - 1 && ((p % W === x && n % W === x) || (((p / W) | 0) === y && ((n / W) | 0) === y));
    if (straight && k % 2 === 0 && passable(j)) marks.push({ i, horiz });
  }
  for (const i of cells) occ[i] = -3;
  return { cells: [...cells], marks, mask: (() => { const m = new Uint8Array(W * H); for (const i of cells) m[i] = 1; return m; })() };
}

function astar(hub, goalSet, road, passable) {
  const start = hub[1] * W + hub[0];
  const N = W * H * 4, g = new Float32Array(N).fill(Infinity), from = new Int32Array(N).fill(-1);
  const heap = [];
  const push = (s, f) => { heap.push([f, s]); let k = heap.length - 1; while (k > 0) { const p = (k - 1) >> 1; if (heap[p][0] <= heap[k][0]) break; [heap[p], heap[k]] = [heap[k], heap[p]]; k = p; } };
  const pop = () => { const top = heap[0], last = heap.pop(); if (heap.length) { heap[0] = last; let k = 0; for (;;) { const l = 2 * k + 1, r = l + 1; let m = k; if (l < heap.length && heap[l][0] < heap[m][0]) m = l; if (r < heap.length && heap[r][0] < heap[m][0]) m = r; if (m === k) break; [heap[m], heap[k]] = [heap[k], heap[m]]; k = m; } } return top; };
  const gx = [...goalSet].map(i => [i % W, (i / W) | 0]);
  const h = i => { const x = i % W, y = (i / W) | 0; let b = Infinity; for (const [a, c] of gx) b = Math.min(b, Math.abs(a - x) + Math.abs(c - y)); return b * .3; };
  for (let d = 0; d < 4; d++) { g[start * 4 + d] = 0; push(start * 4 + d, h(start)); }
  const hgt = i => groundY(WD.cx2w(i % W), WD.cy2w((i / W) | 0));
  while (heap.length) {
    const [, s] = pop(), i = s >> 2, d = s & 3;
    if (goalSet.has(i)) { const out = []; let t = s; while (t >= 0) { out.push(t >> 2); t = from[t]; } return out.reverse(); }
    const x = i % W, y = (i / W) | 0;
    for (let nd = 0; nd < 4; nd++) {
      const nx = x + DIRS[nd][0], ny = y + DIRS[nd][1];
      if (nx < 1 || ny < 1 || nx >= W - 1 || ny >= H - 1) continue;
      const j = ny * W + nx;
      if (!passable(j) && !goalSet.has(j)) continue;
      let c = road[j] ? .3 : 1;
      if (treeAt[j] >= 0) c += 2.5; if (rockAt[j] >= 0) c += 3;
      c += Math.abs(hgt(j) - hgt(i)) * 6;
      if (nd !== d && i !== start) c += 2.2;                       // turns cost: long straight roads look planned
      const ns = j * 4 + nd, ng = g[s] + c;
      if (ng < g[ns]) { g[ns] = ng; from[ns] = s; push(ns, ng + h(j)); }
    }
  }
  return null;
}

/** Road meshes ordered outward from the hub, so `reveal(f)` paves them progressively (used in the video). */
export function buildRoadMesh(plan, hub) {
  const grp = new THREE.Group(); grp.name = 'roads';
  // distance along the network from the hub
  const dist = new Map(), q = [hub[1] * W + hub[0]]; dist.set(q[0], 0);
  const has = new Set(plan.cells);
  while (q.length) { const i = q.shift(); for (const [dx, dy] of DIRS) { const j = i + dy * W + dx; if (has.has(j) && !dist.has(j)) { dist.set(j, dist.get(i) + 1); q.push(j); } } }
  const rank = i => dist.has(i) ? dist.get(i) : 9999;
  const cy = (x, z) => groundY(x, z) + .04;
  const cells = [...plan.cells].sort((a, b) => rank(a) - rank(b));
  const pos = [], col = [], c = new THREE.Color();
  for (const i of cells) {
    const x0 = (i % W) - W / 2, z0 = ((i / W) | 0) - H / 2;
    const a = [x0, cy(x0, z0), z0], b = [x0 + 1, cy(x0 + 1, z0), z0], cc = [x0, cy(x0, z0 + 1), z0 + 1], d = [x0 + 1, cy(x0 + 1, z0 + 1), z0 + 1];
    const k = WD.hash(i % W, (i / W) | 0, 17);
    c.set('#3d4248').offsetHSL(0, 0, (k - .5) * .03);
    for (const v of [a, cc, b, b, cc, d]) { pos.push(...v); col.push(c.r, c.g, c.b); }
  }
  const geo = new THREE.BufferGeometry();
  geo.setAttribute('position', new THREE.Float32BufferAttribute(pos, 3)); geo.setAttribute('color', new THREE.Float32BufferAttribute(col, 3)); geo.computeVertexNormals();
  const mesh = new THREE.Mesh(geo, new THREE.MeshStandardMaterial({ vertexColors: true, roughness: .92, flatShading: true, polygonOffset: true, polygonOffsetFactor: -2, polygonOffsetUnits: -2 }));
  mesh.receiveShadow = true; grp.add(mesh);
  // centre-line dashes
  const marks = [...plan.marks].sort((a, b) => rank(a.i) - rank(b.i)), mp = [];
  for (const { i, horiz } of marks) {
    const x0 = (i % W) - W / 2, z0 = ((i / W) | 0) - H / 2;
    const [cx, cz] = horiz ? [x0 + .5, z0 + 1] : [x0 + 1, z0 + .5];
    const hx = horiz ? .32 : .05, hz = horiz ? .05 : .32, y = groundY(cx, cz) + .07;
    const q4 = [[cx - hx, cz - hz], [cx + hx, cz - hz], [cx - hx, cz + hz], [cx + hx, cz + hz]].map(([x, z]) => [x, Math.max(y, groundY(x, z) + .07), z]);
    for (const v of [q4[0], q4[2], q4[1], q4[1], q4[2], q4[3]]) mp.push(...v);
  }
  const mg = new THREE.BufferGeometry(); mg.setAttribute('position', new THREE.Float32BufferAttribute(mp, 3)); mg.computeVertexNormals();
  const mm = new THREE.Mesh(mg, new THREE.MeshStandardMaterial({ color: '#f4f1e6', roughness: .7, polygonOffset: true, polygonOffsetFactor: -4, polygonOffsetUnits: -4 }));
  grp.add(mm);
  grp.userData.reveal = f => { f = Math.max(0, Math.min(1, f)); geo.setDrawRange(0, Math.floor(f * cells.length) * 6); mg.setDrawRange(0, Math.floor(f * marks.length) * 6); };
  grp.userData.count = cells.length;
  return grp;
}

// Planned streets: straight two-lane segments [x0, y0, x1, y1] (inclusive cells), then short spurs from every
// building and landmark to the nearest street.
function planGrid(occ, segments, goals, land, passable) {
  const cells = new Set(), marks = [], inSeg = (x, y, sg) => x >= sg[0] && x <= sg[2] && y >= sg[1] && y <= sg[3];
  segments.forEach((sg, si) => {
    const [x0, y0, x1, y1] = sg, vertical = (y1 - y0) > (x1 - x0);
    for (let y = y0; y <= y1; y++) for (let x = x0; x <= x1; x++) { const i = y * W + x; if (x > 0 && y > 0 && x < W && y < H && passable(i)) cells.add(i); }
    // centre dashes, skipped where another street crosses
    if (vertical) { for (let y = y0 + 1; y < y1; y += 2) if (!segments.some((o, oi) => oi !== si && (inSeg(x0, y, o) || inSeg(x0, y - 1, o) || inSeg(x0, y + 1, o)))) marks.push({ i: y * W + x0, horiz: false }); }
    else { for (let x = x0 + 1; x < x1; x += 2) if (!segments.some((o, oi) => oi !== si && (inSeg(x, y0, o) || inSeg(x - 1, y0, o) || inSeg(x + 1, y0, o)))) marks.push({ i: y0 * W + x, horiz: true }); }
  });
  const marksOk = marks.filter(m => cells.has(m.i));
  for (const i of cells) occ[i] = -3;
  // spurs (one lane wide is enough for a driveway, two looks tidier)
  for (const g of goals) {
    const starts = g.map(([x, y]) => y * W + x).filter(i => i >= 0 && i < W * H && land(i) && (occ[i] === -1 || occ[i] === -3));
    if (!starts.length || starts.some(i => cells.has(i))) continue;
    const path = dijkstra(starts, cells, passable);
    if (!path) continue;
    for (let k = 0; k < path.length; k++) {
      const i = path[k]; cells.add(i); occ[i] = -3;
      const n = path[Math.min(path.length - 1, k + 1)], p = path[Math.max(0, k - 1)], horiz = Math.abs((n % W) - (p % W)) >= Math.abs(((n / W) | 0) - ((p / W) | 0));
      const j = horiz ? i + W : i + 1; if (j < W * H && passable(j)) { cells.add(j); occ[j] = -3; }
    }
  }
  const mask = new Uint8Array(W * H); for (const i of cells) mask[i] = 1;
  return { cells: [...cells], marks: marksOk, mask };
}
function dijkstra(starts, goal, passable) {
  const dist = new Float32Array(W * H).fill(Infinity), from = new Int32Array(W * H).fill(-1), dirOf = new Int8Array(W * H).fill(-1);
  const heap = [];
  const push = (s, f) => { heap.push([f, s]); let k = heap.length - 1; while (k > 0) { const p = (k - 1) >> 1; if (heap[p][0] <= heap[k][0]) break; [heap[p], heap[k]] = [heap[k], heap[p]]; k = p; } };
  const pop = () => { const top = heap[0], last = heap.pop(); if (heap.length) { heap[0] = last; let k = 0; for (;;) { const l = 2 * k + 1, r = l + 1; let m = k; if (l < heap.length && heap[l][0] < heap[m][0]) m = l; if (r < heap.length && heap[r][0] < heap[m][0]) m = r; if (m === k) break; [heap[m], heap[k]] = [heap[k], heap[m]]; k = m; } } return top; };
  for (const s of starts) { dist[s] = 0; push(s, 0); }
  while (heap.length) {
    const [d, i] = pop(); if (d > dist[i]) continue;
    if (goal.has(i)) { const out = []; let t = i; while (t >= 0) { out.push(t); t = from[t]; } return out.reverse(); }
    if (d > 60) return null;
    const x = i % W, y = (i / W) | 0;
    for (let nd = 0; nd < 4; nd++) {
      const nx = x + DIRS[nd][0], ny = y + DIRS[nd][1]; if (nx < 1 || ny < 1 || nx >= W - 1 || ny >= H - 1) continue;
      const j = ny * W + nx; if (!passable(j) && !goal.has(j)) continue;
      let c = 1 + (treeAt[j] >= 0 ? 1.5 : 0) + (dirOf[i] >= 0 && dirOf[i] !== nd ? 2 : 0);
      if (d + c < dist[j]) { dist[j] = d + c; from[j] = i; dirOf[j] = nd; push(j, d + c); }
    }
  }
  return null;
}
