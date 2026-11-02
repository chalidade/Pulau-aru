import * as THREE from 'three';
import { EffectComposer } from 'three/addons/postprocessing/EffectComposer.js';
import { RenderPass } from 'three/addons/postprocessing/RenderPass.js';
import { UnrealBloomPass } from 'three/addons/postprocessing/UnrealBloomPass.js';
import { OutputPass } from 'three/addons/postprocessing/OutputPass.js';
import * as WD from './world.js';
import { W, H, LM, LMS, tile, trees, rocks, tufts, flowers, treeAt, rockAt, village, groundY, buildTerrain, buildWater } from './world.js';
import * as M from './models.js';
import { BT, ARU, lookOf, makeCharacter, animateCharacter, buildBuilding } from './models.js';
import { loadState, normalize, store } from './data.js';
import * as UI from './ui.js';
import { createFishing } from './fishing.js';
import * as I2 from './island2.js';
import { $, h, toast, fmt, clean } from './ui.js';

const touch = matchMedia('(pointer:coarse)').matches;
const ADMIN = /[?&#]kelola\b/.test(location.search + location.hash);

// ---------- state ----------
let S = normalize(null), PUB = '{}', dirty = false;
const pop = () => S.followers | 0;
const lamps = () => S.followers | 0;
const curEp = () => S.episodes.length ? Math.max(...S.episodes.map(e => e.ep | 0)) : 0;
const role = { kind: 'aru', name: 'Aru' };

// ---------- renderer ----------
const renderer = new THREE.WebGLRenderer({ antialias: !touch, powerPreference: 'high-performance' });
renderer.setPixelRatio(Math.min(devicePixelRatio, touch ? 1.5 : 2));
renderer.setSize(innerWidth, innerHeight);
renderer.shadowMap.enabled = true; renderer.shadowMap.type = THREE.PCFSoftShadowMap;
renderer.toneMapping = THREE.ACESFilmicToneMapping; renderer.toneMappingExposure = 1.05;
$('game').appendChild(renderer.domElement);
const scene = new THREE.Scene();
scene.fog = new THREE.Fog(0x8fd3f0, 55, 165);
const camera = new THREE.PerspectiveCamera(touch && innerWidth < innerHeight ? 55 : 42, innerWidth / innerHeight, .1, 600);

const hemi = new THREE.HemisphereLight(0xcfeeff, 0x5a7a3a, .9); scene.add(hemi);
const sun = new THREE.DirectionalLight(0xfff1d6, 2.3);
sun.castShadow = true; sun.shadow.mapSize.set(touch ? 1024 : 2048, touch ? 1024 : 2048);
Object.assign(sun.shadow.camera, { left: -24, right: 24, top: 24, bottom: -24, near: 1, far: 160 });
sun.shadow.bias = -0.0004; sun.shadow.normalBias = .03;
scene.add(sun, sun.target);

const composer = new EffectComposer(renderer);
composer.addPass(new RenderPass(scene, camera));
const bloom = new UnrealBloomPass(new THREE.Vector2(innerWidth, innerHeight), .4, .6, .82);
composer.addPass(bloom); composer.addPass(new OutputPass());
if (touch) composer.setPixelRatio(1);

addEventListener('resize', () => {
  camera.aspect = innerWidth / innerHeight; camera.fov = touch && innerWidth < innerHeight ? 55 : 42; camera.updateProjectionMatrix();
  renderer.setSize(innerWidth, innerHeight); composer.setSize(innerWidth, innerHeight);
});

// ---------- world ----------
const terrain = buildTerrain(); scene.add(terrain);
const island2 = I2.buildIsland2(scene);
const { water, floor } = buildWater(); scene.add(water, floor);
const fpCenter = (x, y, w, hh) => [x - W / 2 + w / 2, y - H / 2 + hh / 2];
function fpGround(x, y, w, hh) { let m = Infinity; for (let j = 0; j <= hh; j++) for (let i = 0; i <= w; i++) m = Math.min(m, groundY(x - W / 2 + i, y - H / 2 + j)); return m; }
function placeAtFp(obj, x, y, w, hh, ry = 0) { const [cx, cz] = fpCenter(x, y, w, hh); obj.position.set(cx, fpGround(x, y, w, hh), cz); obj.rotation.y = ry; scene.add(obj); return obj; }

// landmarks
const stoneObj = placeAtFp(M.nameStone(), LM.stone[0], LM.stone[1], 2, 1);
const lightObj = placeAtFp(M.lighthouse(), LM.light[0], LM.light[1], 2, 2, -Math.PI / 2);
const shelterObj = placeAtFp(M.shelter(), LM.camp[0] - 1, LM.camp[1], 3, 2);
const fireObj = placeAtFp(M.campfire(new THREE.Group()), LM.fire[0], LM.fire[1], 1, 1);
const mailObj = placeAtFp(M.mailbox(), LM.mail[0], LM.mail[1], 1, 1);
const boardObj = placeAtFp(M.rulesBoard(), LM.board[0], LM.board[1], 2, 1);
const wreckObj = placeAtFp(M.wreck(), LM.wreck[0], LM.wreck[1], 3, 2);
const shipObj = M.ship(); shipObj.position.set(WD.MOOR.x, 0, WD.MOOR.z); shipObj.rotation.y = WD.MOOR.ry; scene.add(shipObj);
const pierObj = new THREE.Group(); scene.add(pierObj);
{ const x = WD.PIER.x - W / 2 + .5; for (let y = WD.PIER.y0 - 1; y <= WD.PIER.y1; y++) { const z = y - H / 2 + .5; for (let k = 0; k < 3; k++) M.box(pierObj, k % 2 ? '#b07a4a' : '#8a5a34', 1.1, .08, .3, x, .2, z - .33 + k * .33); for (const dx of [-.5, .5]) M.box(pierObj, '#5e3b22', .08, 2, .08, x + dx, -1.6, z); } }
// sailing state (per visitor): the ship stays where you leave it
const sail = { on: false, x: WD.MOOR.x, z: WD.MOOR.z, ry: WD.MOOR.ry, speed: 0, told: false };
const festObj = M.festival(6.5); { const [x, z] = fpCenter(LM.camp[0], LM.camp[1] + 3, 1, 1); festObj.position.set(x, groundY(x, z), z); scene.add(festObj); }
const lightTop = new THREE.Vector3(); lightObj.updateMatrixWorld(); lightTop.set(0, lightObj.userData.top, 0).applyMatrix4(lightObj.matrixWorld);
const lhLight = new THREE.PointLight(0xffd27a, 0, 40, 1.6); lhLight.position.copy(lightTop); scene.add(lhLight);
const firePool = []; for (let i = 0; i < 4; i++) { const l = new THREE.PointLight(0xff8a3a, 0, 12, 1.8); scene.add(l); firePool.push(l); }

// stars
const stars = (() => { const n = 900, p = new Float32Array(n * 3); for (let i = 0; i < n; i++) { const a = Math.random() * Math.PI * 2, e = Math.random() * .9 + .1, r = 280; p[i * 3] = Math.cos(a) * Math.cos(e) * r; p[i * 3 + 1] = Math.sin(e) * r; p[i * 3 + 2] = Math.sin(a) * Math.cos(e) * r; } const g = new THREE.BufferGeometry(); g.setAttribute('position', new THREE.BufferAttribute(p, 3)); return new THREE.Points(g, new THREE.PointsMaterial({ color: 0xffffff, size: 1.6, sizeAttenuation: false, transparent: true, opacity: 0, fog: false, depthWrite: false })); })();
scene.add(stars);

// glow sprite texture for village lights
const glowTex = (() => { const c = document.createElement('canvas'); c.width = c.height = 64; const g = c.getContext('2d'); const gr = g.createRadialGradient(32, 32, 0, 32, 32, 32); gr.addColorStop(0, 'rgba(255,220,140,1)'); gr.addColorStop(.25, 'rgba(255,190,90,.6)'); gr.addColorStop(1, 'rgba(255,170,60,0)'); g.fillStyle = gr; g.fillRect(0, 0, 64, 64); return new THREE.CanvasTexture(c); })();

// ---------- occupancy ----------
let solid = new Uint8Array(W * H), plank = new Uint8Array(W * H), occ = new Int16Array(W * H);
const fpOf = b => { const d = BT[b.type]; return (b.r | 0) % 2 ? { w: d.h, h: d.w } : { w: d.w, h: d.h }; };
function rebuildOcc() {
  solid = new Uint8Array(W * H); plank = new Uint8Array(W * H); occ = new Int16Array(W * H).fill(-1);
  for (const l of LMS) for (let dy = 0; dy < l[4]; dy++) for (let dx = 0; dx < l[3]; dx++) occ[(l[2] + dy) * W + l[1] + dx] = -2;
  S.buildings.forEach((b, bi) => { const d = BT[b.type]; if (!d) return; const f = fpOf(b); for (let dy = 0; dy < f.h; dy++) for (let dx = 0; dx < f.w; dx++) { const x = b.x + dx, y = b.y + dy; if (x < 0 || y < 0 || x >= W || y >= H) continue; occ[y * W + x] = bi; if (d.walk && d.water) plank[y * W + x] = 1; } });
  if (pop() >= 1000) for (let y = WD.PIER.y0 - 1; y <= WD.PIER.y1; y++) plank[y * W + WD.PIER.x] = 1;
  for (let i = 0; i < W * H; i++) {
    let s = tile[i] === WD.DEEP ? 1 : 0;
    if (occ[i] === -2) s = 1;
    else if (occ[i] >= 0) { const d = BT[S.buildings[occ[i]].type]; s = d.walk || d.climb ? 0 : 1; }
    else if (treeAt[i] >= 0 || rockAt[i] >= 0) s = 1;
    if (plank[i]) s = 0;
    solid[i] = s;
  }
}
const free = i => occ[i] === -1;

// ---------- nature (instanced) ----------
const nature = new THREE.Group(); scene.add(nature);
const greens = ['#3f9a5a', '#4fae62', '#358a5e', '#5cb870', '#4f9b45'].map(c => new THREE.Color(c));
const pineCols = ['#2c7344', '#2a6b4a', '#336f3c'].map(c => new THREE.Color(c));
function rebuildNature() {
  nature.clear();
  const m4 = new THREE.Matrix4(), q = new THREE.Quaternion(), e = new THREE.Euler(), v = new THREE.Vector3(), sc = new THREE.Vector3();
  const round = trees.filter(t => t.kind === 'round' && free(t.y * W + t.x)), pines = trees.filter(t => t.kind === 'pine' && free(t.y * W + t.x)), palms = trees.filter(t => t.kind === 'palm' && free(t.y * W + t.x));
  const trunkGeo = new THREE.CylinderGeometry(.1, .16, 1, 5);
  const trunks = M.makeInstanced(trunkGeo, M.mat('#6b4a2b'), round.length + pines.length);
  const canopy = M.makeInstanced(new THREE.IcosahedronGeometry(1, 0), new THREE.MeshStandardMaterial({ flatShading: true, roughness: .9 }), round.length * 2);
  const cones = M.makeInstanced(new THREE.ConeGeometry(1, 1, 6), new THREE.MeshStandardMaterial({ flatShading: true, roughness: .9 }), pines.length * 2);
  let ti = 0, ci = 0, pi = 0;
  const set = (mesh, idx, x, y, z, sx, sy, sz, ry = 0, rx = 0) => { e.set(rx, ry, 0); q.setFromEuler(e); m4.compose(v.set(x, y, z), q, sc.set(sx, sy, sz)); mesh.setMatrixAt(idx, m4); };
  for (const t of round) {
    const x = WD.cx2w(t.x) + (WD.hash(t.x, t.y, 5) - .5) * .4, z = WD.cy2w(t.y) + (WD.hash(t.x, t.y, 6) - .5) * .4, y = groundY(x, z), s = t.s;
    set(trunks, ti++, x, y + .6 * s, z, s, 1.2 * s, s);
    set(canopy, ci, x, y + 1.55 * s, z, .95 * s, .85 * s, .95 * s, t.c * 6, .3); canopy.setColorAt(ci++, greens[(t.c * 5) | 0]);
    set(canopy, ci, x + .25 * s, y + 2.05 * s, z - .1 * s, .6 * s, .55 * s, .6 * s, t.c * 3); canopy.setColorAt(ci++, greens[((t.c * 5) | 0 + 1) % 5]);
  }
  for (const t of pines) {
    const x = WD.cx2w(t.x), z = WD.cy2w(t.y), y = groundY(x, z), s = t.s;
    set(trunks, ti++, x, y + .4 * s, z, s * .9, .8 * s, s * .9);
    set(cones, pi, x, y + 1.3 * s, z, .85 * s, 1.5 * s, .85 * s, t.c * 4); cones.setColorAt(pi++, pineCols[(t.c * 3) | 0]);
    set(cones, pi, x, y + 2.15 * s, z, .6 * s, 1.1 * s, .6 * s, t.c * 2); cones.setColorAt(pi++, pineCols[((t.c * 3) | 0 + 1) % 3]);
  }
  for (const m of [trunks, canopy, cones]) { m.instanceMatrix.needsUpdate = true; if (m.instanceColor) m.instanceColor.needsUpdate = true; nature.add(m); }
  for (const t of palms) { const g = new THREE.Group(); BT.kelapa.build(g); const x = WD.cx2w(t.x), z = WD.cy2w(t.y); g.position.set(x, groundY(x, z), z); g.rotation.y = t.x * 1.3; g.scale.setScalar(t.s); nature.add(g); }
  const rk = rocks.filter(r => free(r.y * W + r.x));
  const rockMesh = M.makeInstanced(new THREE.DodecahedronGeometry(1, 0), M.mat('#959a8e'), rk.length);
  rk.forEach((r, i) => { const x = WD.cx2w(r.x), z = WD.cy2w(r.y); set(rockMesh, i, x, groundY(x, z) + .15 * r.s, z, .55 * r.s, .4 * r.s, .5 * r.s, r.x, .2); });
  rockMesh.instanceMatrix.needsUpdate = true; nature.add(rockMesh);
  const tf = tufts.filter(t => free((t.y | 0) * W + (t.x | 0)));
  const tuft = M.makeInstanced(new THREE.ConeGeometry(.06, .3, 3), M.mat('#5a9e44'), tf.length); tuft.castShadow = false;
  tf.forEach((t, i) => { const x = t.x - W / 2, z = t.y - H / 2; set(tuft, i, x, groundY(x, z) + .1, z, 1, .7 + (i % 5) * .15, 1, i); });
  tuft.instanceMatrix.needsUpdate = true; nature.add(tuft);
  const fcols = ['#f06b8a', '#ffd25a', '#f4f1ea', '#b48cf0', '#ff9b52'].map(c => new THREE.Color(c));
  const fl = flowers.filter(f => free((f.y | 0) * W + (f.x | 0)));
  const fm = M.makeInstanced(new THREE.IcosahedronGeometry(.07, 0), new THREE.MeshStandardMaterial({ flatShading: true }), fl.length * 3); fm.castShadow = false;
  let k = 0; fl.forEach(f => { for (let j = 0; j < 3; j++) { const x = f.x - W / 2 + Math.cos(j * 2.1) * .25, z = f.y - H / 2 + Math.sin(j * 2.1) * .25; set(fm, k, x, groundY(x, z) + .14, z, 1, 1, 1); fm.setColorAt(k++, fcols[(f.c + j) % 5]); } });
  fm.instanceMatrix.needsUpdate = true; if (fm.instanceColor) fm.instanceColor.needsUpdate = true; nature.add(fm);
}

// village lights: lamp posts that appear as the population grows (1 per 10 followers, max 400)
const posts = new THREE.Group(); scene.add(posts);
let postLights = null, postCount = -1;
function rebuildPosts() {
  const n = Math.min(260, Math.floor(lamps() / 20)); if (n === postCount) return; postCount = n;
  posts.clear(); if (!n) { postLights = null; return; }
  // spread posts out: keep at least 3 cells between them, nearest to camp first
  const cells = [];
  for (const v of village) { if (cells.length >= n) break; if (!free(v.y * W + v.x)) continue; if (Math.abs(v.x - LM.camp[0]) < 4 && Math.abs(v.y - LM.camp[1] - 2) < 5) continue; if (cells.some(c => Math.abs(c.x - v.x) < 3 && Math.abs(c.y - v.y) < 3)) continue; cells.push(v); }
  const pole = M.makeInstanced(new THREE.CylinderGeometry(.04, .05, 1.4, 5), M.mat('#4a3a2a'), cells.length);
  const lamp = M.makeInstanced(new THREE.BoxGeometry(.18, .22, .18), M.lanternMat, cells.length); lamp.castShadow = false;
  const p = new Float32Array(cells.length * 3), m4 = new THREE.Matrix4();
  cells.forEach((c, i) => { const x = WD.cx2w(c.x) + .3, z = WD.cy2w(c.y) + .3, y = groundY(x, z); m4.makeTranslation(x, y + .7, z); pole.setMatrixAt(i, m4); m4.makeTranslation(x, y + 1.45, z); lamp.setMatrixAt(i, m4); p.set([x, y + 1.45, z], i * 3); });
  posts.add(pole, lamp);
  const g = new THREE.BufferGeometry(); g.setAttribute('position', new THREE.BufferAttribute(p, 3));
  postLights = new THREE.Points(g, new THREE.PointsMaterial({ map: glowTex, size: 1.2, transparent: true, opacity: 0, depthWrite: false, blending: THREE.AdditiveBlending }));
  posts.add(postLights);
}

// ---------- buildings ----------
const bGroup = new THREE.Group(); scene.add(bGroup);
let bObjs = [];
function rebuildBuildings() {
  bGroup.clear(); bObjs = [];
  S.buildings.forEach((b, i) => {
    if (!BT[b.type]) return;
    const o = buildBuilding(b); const f = fpOf(b); const d = BT[b.type];
    const [cx, cz] = fpCenter(b.x, b.y, f.w, f.h);
    o.position.set(cx, d.water ? 0 : fpGround(b.x, b.y, f.w, f.h), cz); o.rotation.y = -(b.r | 0) * Math.PI / 2;
    o.userData.b = b; bGroup.add(o); bObjs.push(o);
  });
}

// ---------- characters ----------
const player = { obj: null, x: 0, z: 0, y: 0, vy: 0, grounded: true, tx: null, tz: null, moving: false };
function jump() { if (!sail.on && player.grounded && $('start').hidden && $('sheet').hidden && !place) { player.vy = 6.3; player.grounded = false; } }
function setPlayerLook() { if (player.obj) scene.remove(player.obj); player.obj = makeCharacter(role.kind === 'aru' ? ARU : lookOf(role.name + 'me')); scene.add(player.obj); player.obj.traverse(o => { if (o.isMesh) o.castShadow = true; }); }
let npcs = [];
const fishHud = h('div', { class: 'plate fishplate', hidden: true }); $('hud-l').appendChild(fishHud);
function updateFishHud() { const st = fishing.st; fishHud.hidden = !st.active && !st.total; fishHud.replaceChildren(h('span', { class: 'eyebrow' }, 'Tangkapan ikan'), h('b', null, fmt(st.total))); }
const fishing = createFishing({ scene, player, toast: (...a) => toast(...a), onChange: () => { near = null; updateFishHud(); } });
const SEED = Math.random(), rankOf = n => { let h = SEED * 4294967296 >>> 0; for (const c of n.toLowerCase()) h = Math.imul(h ^ c.charCodeAt(0), 2654435761) >>> 0; return h; };
const npcGroup = new THREE.Group(); scene.add(npcGroup);
function rebuildNpcs() {
  // a random pick of named residents, reshuffled per page load but stable while the page is open
  const res = S.residents.map((r, i) => ({ ...r, num: i + 1 })).sort((a, b) => rankOf(a.n) - rankOf(b.n));
  const extra = Math.max(0, lamps() - res.length), N = Math.min(touch ? 60 : 100, res.length + extra);
  const want = [];
  if (role.kind !== 'aru') want.push({ key: 'aru', name: 'Aru', aru: true });
  for (let i = 0; i < N; i++) { const r = i < res.length ? res[i] : null; const key = r ? 'r:' + r.n.toLowerCase() : 'a:' + i; if (role.kind === 'warga' && key === 'r:' + role.name.toLowerCase()) continue; want.push(r ? { key, name: '@' + r.n, num: r.num } : { key, name: 'Warga', num: null }); }
  const old = new Map(npcs.map(n => [n.key, n]));
  const next = want.map((w, i) => {
    const o = old.get(w.key); if (o) { old.delete(w.key); Object.assign(o, w); return o; }
    const home = w.aru ? { x: LM.camp[0] + 1, y: LM.camp[1] + 2 } : village[(i * 13 + 5) % Math.min(village.length, 1600)];
    const obj = makeCharacter(w.aru ? ARU : lookOf(w.name + (w.num || i))); npcGroup.add(obj);
    const x = WD.cx2w(home.x), z = WD.cy2w(home.y);
    return { ...w, obj, x, z, hx: home.x, hy: home.y, wait: Math.random() * 3, tx: null, tz: null, moving: false };
  });
  for (const o of old.values()) npcGroup.remove(o.obj);
  npcs = next;
}
function walkable(x, z) {
  if (I2.inside2(x, z)) return I2.walkable2(x, z);
  if (Math.abs(x) > W / 2 - .5 || Math.abs(z) > H / 2 - .5) return false;
  for (const [dx, dz] of [[-.28, -.2], [.28, -.2], [-.28, .2], [.28, .2]]) { const cx = WD.w2cx(x + dx), cy = WD.w2cy(z + dz); if (cx < 0 || cy < 0 || cx >= W || cy >= H || solid[cy * W + cx]) return false; }
  return true;
}
// climbable surfaces (the pyramid): each entry knows its centre, base height and step profile
let climbs = [];
function rebuildClimbs() { climbs = bObjs.filter(o => o.userData.def.climb).map(o => ({ cx: o.position.x, cz: o.position.z, base: o.position.y, ...o.userData.def.climb })); }
function climbAt(x, z) { let best = -Infinity; for (const c of climbs) { const d = Math.max(Math.abs(x - c.cx), Math.abs(z - c.cz)); if (d > c.half) continue; const k = Math.min(c.tiers - 1, Math.floor((c.half - d) / c.inset)); best = Math.max(best, c.base + (k + 1) * c.step); } return best; }
const climbCell = i => occ[i] >= 0 && !!BT[S.buildings[occ[i]].type].climb;
function npcWalkable(x, z) { if (!walkable(x, z)) return false; for (const [dx, dz] of [[-.3, -.3], [.3, -.3], [-.3, .3], [.3, .3]]) { const i = WD.w2cy(z + dz) * W + WD.w2cx(x + dx); if (climbCell(i)) return false; } return true; }
const playerSurface = (x, z) => Math.max(surfaceY(x, z), climbAt(x, z));
const shallowAt = (x, z) => I2.inside2(x, z) ? I2.shallow2(x, z) : shallowAt1(x, z);
const shallowAt1 = (x, z) => { const i = WD.w2cy(z) * W + WD.w2cx(x); return tile[i] === WD.SHALLOW && !plank[i]; };
const surfaceY = (x, z) => I2.inside2(x, z) ? I2.surface2(x, z) : surfaceY1(x, z);
const surfaceY1 = (x, z) => { const i = WD.w2cy(z) * W + WD.w2cx(x); if (plank[i]) return .26; return Math.max(groundY(x, z), -.55); };
function stepNpc(n, dt) {
  if (n.wait > 0) { n.wait -= dt; n.moving = false; return; }
  if (n.tx == null) {
    const R = n.aru ? 3 : 8;
    for (let k = 0; k < 6; k++) { const tx = n.hx + ((Math.random() * 2 - 1) * R | 0), ty = n.hy + ((Math.random() * 2 - 1) * R | 0); if (tx > 0 && ty > 0 && tx < W && ty < H && !solid[ty * W + tx] && !climbCell(ty * W + tx) && tile[ty * W + tx] >= WD.SAND) { n.tx = WD.cx2w(tx); n.tz = WD.cy2w(ty); break; } }
    if (n.tx == null) { n.wait = 1; return; }
  }
  const dx = n.tx - n.x, dz = n.tz - n.z, d = Math.hypot(dx, dz);
  if (d < .15) { n.tx = null; n.wait = 1 + Math.random() * 5; n.moving = false; return; }
  const sp = 1.5 * dt, vx = dx / d * sp, vz = dz / d * sp; let moved = false;
  if (npcWalkable(n.x + vx, n.z)) { n.x += vx; moved = true; } if (npcWalkable(n.x, n.z + vz)) { n.z += vz; moved = true; }
  if (!moved) { n.tx = null; n.wait = .5; }
  n.moving = moved; if (moved) n.obj.rotation.y = Math.atan2(dx, dz);
}

// ---------- camera & input ----------
const cam = { yaw: 0, pitch: .6, dist: touch ? 14 : 13, target: new THREE.Vector3(), attract: true };
const keys = {};
let place = null, joy = null, drag = null, pinch = null;
const raycaster = new THREE.Raycaster(), ndc = new THREE.Vector2(), waterPlane = new THREE.Plane(new THREE.Vector3(0, 1, 0), 0);
function pickGround(cx, cy) {
  ndc.set(cx / innerWidth * 2 - 1, -(cy / innerHeight) * 2 + 1); raycaster.setFromCamera(ndc, camera);
  const hit = raycaster.intersectObject(terrain, false)[0];
  if (hit && hit.point.y > 0) return hit.point;
  const p = new THREE.Vector3(); return raycaster.ray.intersectPlane(waterPlane, p) ? p : (hit ? hit.point : null);
}
addEventListener('keydown', e => {
  if (e.target.matches('input,textarea,select')) return;
  const k = e.key.toLowerCase();
  if (!$('sheet').hidden) { if (k === 'escape') UI.closeSheet(); return; }
  if (['arrowup', 'arrowdown', 'arrowleft', 'arrowright', ' '].includes(k)) e.preventDefault();
  keys[k] = true;
  if (k === 'e' || k === 'enter') doAct();
  if (k === ' ') jump();
  if (k === 'm') UI.openMap(); if (k === 'h') toggleRec(); if (k === 'escape') { UI.closeDialog(); endPlace(); }
  if (k === 'f') fishing.throwAt();
  if (k === 'r' && place && !place.erase) place.r = ((place.r | 0) + 1) % 4;
  if (k === 'q') cam.yaw += .4; if (k === 'z') cam.yaw -= .4;
});
addEventListener('keyup', e => { keys[e.key.toLowerCase()] = false; });
const cvs = renderer.domElement;
const pointers = new Map();
cvs.addEventListener('pointerdown', e => {
  if (!$('start').hidden) return;
  cvs.setPointerCapture(e.pointerId); pointers.set(e.pointerId, { x: e.clientX, y: e.clientY });
  if (pointers.size === 2) { const [a, b] = [...pointers.values()]; pinch = { d: Math.hypot(a.x - b.x, a.y - b.y), dist: cam.dist }; joy = null; $('joy').hidden = true; drag = null; return; }
  if (!$('dialog').hidden) { UI.closeDialog(); return; }
  if (touch && !place && e.clientX < innerWidth * .45 && e.clientY > innerHeight * .3) {
    joy = { id: e.pointerId, ox: e.clientX, oy: e.clientY, dx: 0, dy: 0 }; const j = $('joy'); j.style.left = e.clientX + 'px'; j.style.top = e.clientY + 'px'; j.hidden = false; return;
  }
  drag = { id: e.pointerId, x: e.clientX, y: e.clientY, sx: e.clientX, sy: e.clientY, moved: false };
});
cvs.addEventListener('pointermove', e => {
  if (pointers.has(e.pointerId)) pointers.set(e.pointerId, { x: e.clientX, y: e.clientY });
  if (pinch && pointers.size === 2) { const [a, b] = [...pointers.values()]; cam.dist = Math.max(6, Math.min(32, pinch.dist * pinch.d / Math.max(20, Math.hypot(a.x - b.x, a.y - b.y)))); return; }
  if (place && !place.erase && !touch) { const p = pickGround(e.clientX, e.clientY); if (p) { place.hx = WD.w2cx(p.x); place.hy = WD.w2cy(p.z); } }
  if (joy && e.pointerId === joy.id) { let dx = e.clientX - joy.ox, dy = e.clientY - joy.oy; const d = Math.hypot(dx, dy), m = 44; if (d > m) { dx = dx / d * m; dy = dy / d * m; } joy.dx = dx / m; joy.dy = dy / m; $('joy').firstElementChild.style.transform = `translate(${dx}px,${dy}px)`; return; }
  if (drag && e.pointerId === drag.id) {
    const dx = e.clientX - drag.x, dy = e.clientY - drag.y; drag.x = e.clientX; drag.y = e.clientY;
    if (Math.hypot(e.clientX - drag.sx, e.clientY - drag.sy) > 6) drag.moved = true;
    if (drag.moved) { cam.yaw -= dx * .006; cam.pitch = Math.max(.35, Math.min(1.3, cam.pitch + dy * .004)); }
  }
});
const endPtr = e => {
  pointers.delete(e.pointerId); if (pointers.size < 2) pinch = null;
  if (joy && e.pointerId === joy.id) { joy = null; $('joy').hidden = true; $('joy').firstElementChild.style.transform = ''; }
  if (drag && e.pointerId === drag.id) { if (!drag.moved && e.type === 'pointerup') tapAt(e.clientX, e.clientY); drag = null; }
};
cvs.addEventListener('pointerup', endPtr); cvs.addEventListener('pointercancel', endPtr);
cvs.addEventListener('wheel', e => { e.preventDefault(); cam.dist = Math.max(6, Math.min(32, cam.dist * (1 + Math.sign(e.deltaY) * .1))); }, { passive: false });
cvs.addEventListener('contextmenu', e => e.preventDefault());
function tapAt(cx, cy) {
  const p = pickGround(cx, cy); if (!p) return;
  if (place) { placeAt(WD.w2cx(p.x), WD.w2cy(p.z)); return; }
  if (fishing.st.active && fishing.isWater(p.x, p.z) && Math.hypot(p.x - player.x, p.z - player.z) < 5.5) { fishing.throwAt({ x: p.x, z: p.z }); return; }
  let hit = null, bd = 1.6; for (const it of interactables()) { const d = Math.hypot(it.x - p.x, it.z - p.z); if (d < bd) { bd = d; hit = it; } }
  if (hit && Math.hypot(hit.x - player.x, hit.z - player.z) < 4) { hit.act(); return; }
  player.tx = p.x; player.tz = p.z;
}
$('act').addEventListener('click', doContext); $('prompt').addEventListener('click', doAct);

// ---------- sailing ----------
function navigable(x, z) {
  if (Math.abs(x) > 205 || Math.abs(z) > 205) return false;
  if (I2.inside2(x, z)) { const cx = I2.c2x(x), cy = I2.c2y(z); return I2.T2(cx, cy) === WD.DEEP && !I2.plank2[cy * I2.W2 + cx]; }
  const cx = WD.w2cx(x), cy = WD.w2cy(z); if (cx < 0 || cy < 0 || cx >= W || cy >= H) return true;
  return tile[cy * W + cx] === WD.DEEP && !plank[cy * W + cx];
}
const landSpot = () => { let best = null, bd = 1e9; for (let r = 2.6; r <= 5; r += .6) for (let k = 0; k < 20; k++) { const a = k / 20 * Math.PI * 2, x = sail.x + Math.cos(a) * r, z = sail.z + Math.sin(a) * r; if (walkable(x, z) && surfaceY(x, z) > -.3 && r < bd) { bd = r; best = { x, z }; } } return best; };
function board() { sail.on = true; player.tx = null; if (fishing.st.active) fishing.setActive(false); toast(sail.told ? 'Kembali ke kemudi.' : 'Kamu di kemudi. Arahkan kapal dengan ' + (touch ? 'jempol kiri' : 'WASD') + '. Pulau seberang ada di timur laut, ikuti arah matahari terbit.'); sail.told = true; near = null; }
function disembark() { const p = landSpot(); if (!p) { toast('Terlalu jauh dari daratan.'); return; } sail.on = false; sail.speed = 0; player.x = p.x; player.z = p.z; player.y = surfaceY(p.x, p.z); player.vy = 0; near = null; toast(I2.inside2(p.x, p.z) ? 'Kamu menginjak pulau seberang. Belum ada yang tinggal di sini…' : 'Kembali ke Pulau Netizen.'); }

// ---------- interactions ----------
function interactables() {
  const L = [];
  if (sail.on) { const p = landSpot(); if (p) L.push({ x: player.x, z: player.z, label: 'Turun ke darat', act: disembark, r: 99, key: 'land' }); return L; }
  if (pop() >= 1000) L.push({ x: sail.x, z: sail.z, label: 'Naik kapal', act: board, r: 4.6, key: 'ship' });
  if (I2.inside2(player.x, player.z)) { for (const it of I2.interactables2()) L.push({ ...it, act: () => UI.dialog(it.key === 'chest' ? 'Peti tua' : it.key === 'circle' ? 'Lingkaran batu' : 'Pantai seberang', I2.LORE[it.key]) }); return L; }
  const at = (x, y, w, hh, dz) => { const [cx, cz] = fpCenter(x, y, w, hh); return { x: cx, z: cz + dz }; };
  L.push({ ...at(LM.stone[0], LM.stone[1], 2, 1, 1.2), label: 'Baca Batu Nama', act: UI.openNames, r: 2 });
  L.push({ ...at(LM.light[0], LM.light[1], 2, 2, 1.8), label: 'Lihat mercusuar', act: UI.openLight, r: 2 });
  L.push({ ...at(LM.mail[0], LM.mail[1], 1, 1, .8), label: 'Buka kotak surat', act: UI.openLetters, r: 1.5 });
  L.push({ ...at(LM.board[0], LM.board[1], 2, 1, .9), label: 'Baca aturan', act: UI.openRules, r: 1.6 });
  L.push({ ...at(LM.wreck[0], LM.wreck[1], 3, 2, 1.4), label: 'Periksa perahu', act: UI.openMystery, r: 2.4 });
  L.push({ ...at(LM.fire[0], LM.fire[1], 1, 1, .9), label: 'Baca catatan', act: UI.openJournal, r: 1.6 });
  bObjs.forEach(o => { const b = o.userData.b, f = fpOf(b); const [cx, cz] = fpCenter(b.x, b.y, f.w, f.h); const sp = BT[b.type].spear; L.push({ x: cx, z: cz + f.h / 2 + .4, label: sp ? (fishing.st.active ? 'Kembalikan tombak' : 'Ambil tombak') : 'Lihat ' + BT[b.type].n.toLowerCase(), act: sp ? fishing.toggle : () => UI.bldDialog(b), r: Math.min(3, Math.max(1.4, f.w * .7)), key: sp ? 'spear' + fishing.st.active : null }); });
  for (const n of npcs) L.push({ npc: true, x: n.x, z: n.z, label: 'Bicara dengan ' + n.name, act: () => { n.obj.rotation.y = Math.atan2(player.x - n.x, player.z - n.z); n.wait = 4; UI.talk(n); }, r: 1.3 });
  return L;
}
let near = null, nearKey = null, lastThr = false;
function findNear() { let best = null, bd = 1e9; for (const it of interactables()) { const d = Math.hypot(it.x - player.x, it.z - player.z); if (d < (it.r || 1.5) && d < bd) { bd = d; best = it; } } return best; }
// one button for everything on phones: interact when something is near, throw when holding a spear over water, otherwise jump
function doContext() { if (!$('dialog').hidden) { UI.closeDialog(); return; } if (near) near.act(); else if (fishing.canThrow()) fishing.throwAt(); else jump(); }
const ICO = { jump: '<svg viewBox="0 0 24 24"><path d="M12 19V5M5 12l7-7 7 7"/></svg>', act: '<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="3"/><path d="M12 3v3M12 18v3M3 12h3M18 12h3"/></svg>', talk: '<svg viewBox="0 0 24 24"><path d="M4 5h16v11H9l-5 4z"/></svg>', spear: '<svg viewBox="0 0 24 24"><path d="M4 20 18 6M14 6h4v4"/></svg>' };
function doAct() { if (!$('dialog').hidden) { UI.closeDialog(); return; } if (near) near.act(); else if (fishing.st.active) fishing.throwAt(); }
function updatePrompt() {
  const p = $('prompt'), thr = !near && fishing.canThrow();
  if (touch) {
    p.hidden = true;
    if (sail.on && !near) { $('act-ico').innerHTML = ICO.act; $('act-t').textContent = 'Berlayar'; $('act').classList.remove('talk'); return; }
    const kind = place ? 'jump' : near ? (near.npc ? 'talk' : 'act') : thr ? 'spear' : 'jump';
    $('act-ico').innerHTML = ICO[kind]; $('act-t').textContent = place ? 'Lompat' : near ? near.label : thr ? 'Lempar tombak' : 'Lompat';
    $('act').classList.toggle('talk', kind === 'talk' || kind === 'act');
    return;
  }
  if ((!near && !thr) || place) { p.hidden = true; return; }
  p.replaceChildren(h('kbd', null, near ? 'E' : 'F'), near ? near.label : 'Lempar tombak'); p.hidden = false;
}

// ---------- placement (admin) ----------
const ghostOk = new THREE.MeshStandardMaterial({ color: '#86d38f', transparent: true, opacity: .55, flatShading: true, depthWrite: false });
const ghostBad = new THREE.MeshStandardMaterial({ color: '#ff8a72', transparent: true, opacity: .55, flatShading: true, depthWrite: false });
let ghost = null, ghostKey = '';
function canPlace(type, x, y, r) {
  const d = BT[type], f = (r | 0) % 2 ? { w: d.h, h: d.w } : { w: d.w, h: d.h };
  for (let dy = 0; dy < f.h; dy++) for (let dx = 0; dx < f.w; dx++) {
    const tx = x + dx, ty = y + dy; if (tx < 1 || ty < 1 || tx >= W - 1 || ty >= H - 1) return false;
    const i = ty * W + tx; if (occ[i] !== -1) return false; const t = tile[i];
    if (d.water) { if (d.deep ? t > WD.SHALLOW : t > WD.SAND) return false; } else if (t < WD.SAND) return false;
  }
  const px = WD.w2cx(player.x), py = WD.w2cy(player.z);
  if (!d.walk && px >= x && px < x + f.w && py >= y && py < y + f.h) return false;
  return true;
}
function startPlace(type, meta) { UI.closeSheet(); place = { type, meta, r: 0, hx: WD.w2cx(player.x) + 1, hy: WD.w2cy(player.z) - BT[type].h - 1 }; $('banner-t').textContent = `${touch ? 'Ketuk' : 'Klik'} lokasi untuk menaruh ${BT[type].n.toLowerCase()}`; $('banner').hidden = false; updatePrompt(); }
function startErase() { UI.closeSheet(); place = { erase: true }; $('banner-t').textContent = `${touch ? 'Ketuk' : 'Klik'} bangunan untuk menghapus`; $('banner').hidden = false; }
function endPlace() { if (!place) return; place = null; $('banner').hidden = true; if (ghost) { scene.remove(ghost); ghost = null; ghostKey = ''; } updatePrompt(); }
function placeAt(x, y) {
  if (place.erase) { if (x < 0 || y < 0 || x >= W || y >= H) return; const bi = occ[y * W + x]; if (bi >= 0) { const b = S.buildings[bi]; S.buildings.splice(bi, 1); markDirty(); toast(BT[b.type].n + ' dihapus'); } return; }
  if (touch && (place.hx !== x || place.hy !== y)) { place.hx = x; place.hy = y; toast('Ketuk sekali lagi untuk menaruh di sini'); return; }
  if (!canPlace(place.type, x, y, place.r)) { toast(BT[place.type].water ? 'Taruh di air dekat pantai.' : 'Tempat itu tidak bisa dibangun.'); return; }
  const m = place.meta || {};
  S.buildings.push({ type: place.type, x, y, r: place.r | 0, label: m.label || '', by: m.by || '', ep: isNaN(m.ep) ? curEp() : m.ep });
  markDirty(); toast(BT[place.type].n + ' dibangun. Jangan lupa terbitkan.');
  if (!keys.shift) { endPlace(); UI.openAdmin('bangun'); }
}
function updateGhost() {
  if (!place || place.erase || place.hx == null) { if (ghost) { scene.remove(ghost); ghost = null; ghostKey = ''; } return; }
  const ok = canPlace(place.type, place.hx, place.hy, place.r), key = place.type + place.r + ok;
  if (key !== ghostKey) { if (ghost) scene.remove(ghost); ghost = buildBuilding({ type: place.type, label: place.meta && place.meta.label }); ghost.traverse(o => { if (o.isMesh) { o.material = ok ? ghostOk : ghostBad; o.castShadow = false; } }); scene.add(ghost); ghostKey = key; }
  const d = BT[place.type], f = place.r % 2 ? { w: d.h, h: d.w } : { w: d.w, h: d.h };
  const [cx, cz] = fpCenter(place.hx, place.hy, f.w, f.h);
  ghost.position.set(cx, d.water ? 0 : fpGround(place.hx, place.hy, f.w, f.h) + .02, cz); ghost.rotation.y = -place.r * Math.PI / 2;
}

// ---------- time of day ----------
let tMode = 0, tClock = .3; const tModes = ['auto', 'day', 'night'];
const darkness = p => { if (p < .05) return .85 * (1 - (p + .05) / .1); if (p < .55) return 0; if (p < .65) return .85 * (p - .55) / .1; if (p < .95) return .85; return .85 * (1 - (p - .95) / .1); };
const duskAmt = p => { const d = Math.min(Math.abs(p - .58), Math.abs(p - .98), Math.abs(p + .02)); return Math.max(0, 1 - d / .07); };
const SKY_DAY = new THREE.Color('#8fd3f0'), SKY_DUSK = new THREE.Color('#f2a463'), SKY_NIGHT = new THREE.Color('#0b1633');
const SUN_DAY = new THREE.Color('#fff1d6'), SUN_DUSK = new THREE.Color('#ffb070'), MOON = new THREE.Color('#9fb8ff');
const sky = new THREE.Color();
$('b-time').onclick = () => { tMode = (tMode + 1) % 3; const n = ['otomatis', 'siang', 'malam'][tMode]; $('time-label').textContent = 'Waktu: ' + n; toast('Waktu: ' + n); };

// ---------- labels ----------
const labelPool = []; for (let i = 0; i < (touch ? 3 : 6); i++) { const d = document.createElement('div'); d.className = 'lbl'; d.hidden = true; $('labels').appendChild(d); labelPool.push(d); }
const pv = new THREE.Vector3();
function updateLabels() {
  const items = [];
  const push = (text, x, y, z, cls, d) => items.push({ text, x, y, z, cls, d });
  for (const n of npcs) { const d = Math.hypot(n.x - player.x, n.z - player.z); if (d < (n.aru ? 10 : 4.5) && (n.num || n.aru)) push(n.name, n.x, n.obj.position.y + 1.75, n.z, n.aru ? 'gold' : '', d); }
  items.sort((a, b) => a.d - b.d);
  labelPool.forEach((el, i) => {
    const it = items[i]; if (!it) { el.hidden = true; return; }
    pv.set(it.x, it.y, it.z).project(camera);
    if (pv.z > 1 || Math.abs(pv.x) > 1.1 || Math.abs(pv.y) > 1.1) { el.hidden = true; return; }
    el.hidden = false; if (el.textContent !== it.text) el.textContent = it.text; el.className = 'lbl ' + it.cls;
    el.style.transform = `translate(${(pv.x * .5 + .5) * innerWidth}px,${(-pv.y * .5 + .5) * innerHeight}px) translate(-50%,-100%)`;
  });
}

// ---------- main loop ----------
const clock = new THREE.Clock(); let T0 = 0;
const fireSources = [];
function frame() {
  const dt = Math.min(.05, clock.getDelta()); T0 += dt;
  if (tModes[tMode] === 'auto') tClock = (tClock + dt / 360) % 1; else tClock = tModes[tMode] === 'day' ? .3 : .8;
  const blocked = !$('start').hidden || !$('sheet').hidden || !$('dialog').hidden;
  // player movement
  let mx = 0, my = 0;
  if (!blocked && !place) {
    if (keys.w || keys.arrowup) my -= 1; if (keys.s || keys.arrowdown) my += 1; if (keys.a || keys.arrowleft) mx -= 1; if (keys.d || keys.arrowright) mx += 1;
    if (joy) { mx = joy.dx; my = joy.dy; }
  } else if (place && !touch) { if (keys.w || keys.arrowup) my -= 1; if (keys.s || keys.arrowdown) my += 1; if (keys.a || keys.arrowleft) mx -= 1; if (keys.d || keys.arrowright) mx += 1; }
  let wx = 0, wz = 0;
  if (mx || my) { player.tx = null; const fx = -Math.sin(cam.yaw), fz = -Math.cos(cam.yaw), rx = Math.cos(cam.yaw), rz = -Math.sin(cam.yaw); wx = rx * mx + fx * -my; wz = rz * mx + fz * -my; }
  else if (player.tx != null) { const dx = player.tx - player.x, dz = player.tz - player.z, d = Math.hypot(dx, dz); if (d < .2) player.tx = null; else { wx = dx / d; wz = dz / d; } }
  const ml = Math.hypot(wx, wz);
  if (sail.on) {
    if (ml > .12 && !blocked) { const want = Math.atan2(-wz, wx); let dr = want - sail.ry; dr = Math.atan2(Math.sin(dr), Math.cos(dr)); sail.ry += Math.sign(dr) * Math.min(Math.abs(dr), dt * 1.3); sail.speed = Math.min(10 * Math.min(1, ml), sail.speed + dt * 4 * Math.max(.2, Math.cos(dr))); }
    else sail.speed = Math.max(0, sail.speed - dt * 3);
    const cx = Math.cos(sail.ry), cz = -Math.sin(sail.ry), nx = sail.x + cx * sail.speed * dt, nz = sail.z + cz * sail.speed * dt;
    if (navigable(nx + cx * 3.4, nz + cz * 3.4) && navigable(nx, nz) && navigable(nx - cx * 2.4, nz - cz * 2.4)) { sail.x = nx; sail.z = nz; } else if (sail.speed > 2) { sail.speed = 0; toast('Kapal menyentuh dasar. Putar arah.'); } else sail.speed = 0;
    player.x = sail.x - cx * .3; player.z = sail.z - cz * .3; player.y = 1.05 + shipObj.position.y; player.obj.rotation.y = sail.ry + Math.PI / 2; player.moving = false; player.grounded = true; player.vy = 0;
  } else if (ml > .12 && !blocked) {
    const sp = 4.2 * dt * Math.min(1, ml) * (shallowAt(player.x, player.z) ? .55 : 1) * (keys.shift && !place ? 1.6 : 1);
    const vx = wx / ml * sp, vz = wz / ml * sp; let moved = false;
    const okAt = (x, z) => walkable(x, z) && playerSurface(x, z) <= player.y + .32;
    if (okAt(player.x + vx, player.z)) { player.x += vx; moved = true; } if (okAt(player.x, player.z + vz)) { player.z += vz; moved = true; }
    if (!moved) player.tx = null; player.moving = moved;
    const want = Math.atan2(wx, wz); let dr = want - player.obj.rotation.y; dr = Math.atan2(Math.sin(dr), Math.cos(dr)); player.obj.rotation.y += dr * Math.min(1, dt * 14);
  } else player.moving = false;
  if (!sail.on) { // gravity, jumping and stepping onto ledges
    const g = playerSurface(player.x, player.z);
    if (!player.grounded || player.vy > 0 || player.y > g + .32) { player.vy -= 16 * dt; player.y += player.vy * dt; if (player.y <= g) { player.y = g; player.vy = 0; player.grounded = true; } else player.grounded = false; }
    else { player.y = g; player.vy = 0; player.grounded = true; }
  }
  player.obj.position.set(player.x, player.y, player.z);
  animateCharacter(player.obj, player.moving, dt);
  fishing.update(dt, T0);
  for (const n of npcs) { stepNpc(n, dt); n.obj.position.set(n.x, surfaceY(n.x, n.z), n.z); animateCharacter(n.obj, n.moving, dt); }
  // camera
  if (cam.attract && !$('start').hidden) { cam.yaw += dt * .05; }
  const tgt = new THREE.Vector3(player.x, player.obj.position.y + 1, player.z);
  if (place && !place.erase && place.hx != null && touch) { const [cx, cz] = fpCenter(place.hx, place.hy, 1, 1); tgt.set(cx, 1, cz); }
  if (sail.on) tgt.set(sail.x, 1.5, sail.z);
  cam.target.lerp(tgt, Math.min(1, dt * 6));
  cam.sailDist = (cam.sailDist || 0) + ((sail.on ? 10 : 0) - (cam.sailDist || 0)) * Math.min(1, dt * 2);
  const cp = Math.cos(cam.pitch);
  const cd = cam.dist + cam.sailDist;
  camera.position.set(cam.target.x + Math.sin(cam.yaw) * cp * cd, cam.target.y + Math.sin(cam.pitch) * cd, cam.target.z + Math.cos(cam.yaw) * cp * cd);
  scene.fog.far = 165 + cam.sailDist * 10; scene.fog.near = 55 + cam.sailDist * 4;
  camera.position.y = Math.max(camera.position.y, (I2.inside2(camera.position.x, camera.position.z) ? I2.ground2(camera.position.x, camera.position.z) : groundY(camera.position.x, camera.position.z)) + 1.2, climbAt(camera.position.x, camera.position.z) + 1);
  camera.lookAt(cam.target);
  // time of day lighting
  const p = tClock, dk = darkness(p), dusk = duskAmt(p);
  sky.copy(SKY_DAY).lerp(SKY_DUSK, dusk * .85).lerp(SKY_NIGHT, dk / .85);
  scene.background = sky; scene.fog.color.copy(sky);
  const th = (p / .6) * Math.PI;
  const isDay = p < .6 || p > .98;
  if (isDay) { sun.position.set(cam.target.x + Math.cos(th) * 60, Math.max(8, Math.sin(th) * 70), cam.target.z - 30); sun.color.copy(SUN_DAY).lerp(SUN_DUSK, dusk); sun.intensity = 2.3 * (1 - dk / .85) + .2; }
  else { sun.position.set(cam.target.x - 40, 60, cam.target.z + 20); sun.color.copy(MOON); sun.intensity = .55; }
  sun.target.position.copy(cam.target);
  hemi.intensity = .9 - dk * .55; hemi.color.copy(sky).lerp(new THREE.Color('#ffffff'), .5);
  stars.material.opacity = Math.max(0, (dk - .3) / .55);
  renderer.toneMappingExposure = 1.05 - dk * .15;
  M.windowMat.emissiveIntensity = dk * 2.4;
  M.lanternMat.emissiveIntensity = .3 + dk * 3;
  bloom.strength = .15 + dk * .6;
  water.userData.update(T0);
  // lighthouse
  const L = lamps(), ud = lightObj.userData;
  ud.lamps.forEach((m, i) => { const on = i < L; if ((m.material === M.lampOnMat) !== on) m.material = on ? M.lampOnMat : M.lampOffMat; });
  ud.glass.emissiveIntensity = L > 0 ? .5 + dk * 3.2 : 0;
  const lg = Math.log10(L + 1);
  lhLight.intensity = L > 0 ? dk * (8 + lg * 14) : 0; lhLight.distance = 25 + lg * 15;
  ud.beamMat.opacity = L > 0 ? dk * .06 * Math.min(1.6, .5 + lg / 2) : 0; ud.beam.rotation.y = T0 * .6; ud.beam.scale.set(1 + lg * .3, 1, 1);
  // fires
  fireSources.length = 0; fireSources.push(fireObj);
  for (const o of bObjs) if (o.userData.def.fire) fireSources.push(o);
  const fl = 1 + Math.sin(T0 * 11) * .08 + Math.sin(T0 * 17) * .05;
  for (const o of fireSources) { const f = o.userData.flames; if (f) { f.scale.set(1, fl, 1); f.rotation.y = T0 * 2; } }
  const sorted = fireSources.map(o => ({ o, d: o.position.distanceToSquared(player.obj.position) })).sort((a, b) => a.d - b.d);
  firePool.forEach((l, i) => { const s = sorted[i]; if (!s) { l.intensity = 0; return; } l.position.set(s.o.position.x, s.o.position.y + .7, s.o.position.z); l.intensity = (1.2 + dk * 9) * fl; });
  // ship, festival, posts
  shipObj.visible = pierObj.visible = pop() >= 1000;
  if (shipObj.visible) { shipObj.position.set(sail.x, Math.sin(T0 * .9) * .12 - .1, sail.z); shipObj.rotation.set(Math.sin(T0 * .8) * .02, sail.ry, Math.sin(T0 * .7) * .03 + (sail.on ? Math.min(.06, sail.speed * .006) : 0)); }
  festObj.visible = pop() >= 100;
  if (postLights) postLights.material.opacity = Math.min(1, dk * 1.3);
  for (const o of bObjs) if (o.userData.def.bob) { o.position.y = Math.sin(T0 * 1.2 + o.position.x) * .08; o.rotation.z = Math.sin(T0 + o.position.x) * .04; }
  mailObj.userData.flag.rotation.x = S.letters.length && (store.get('pulau-aru-seen-letters') | 0) < S.letters.length ? -Math.PI / 2 : 0;
  updateGhost();
  // prompt + labels
  const nn = blocked ? null : findNear();
  const thr = !nn && fishing.canThrow();
  if (nn !== near || (nn && nn.key !== nearKey) || thr !== lastThr || (nn && $('prompt').hidden)) { near = nn; nearKey = nn && nn.key; lastThr = thr; updatePrompt(); }
  if (player.obj) updateLabels();
  composer.render();
  requestAnimationFrame(frame);
}

// ---------- recording mode ----------
let rec = false;
function toggleRec() { rec = !rec; document.body.classList.toggle('rec', rec); $('unhide').hidden = !rec; if (rec) toast('Mode rekam. Tekan H atau ketuk pojok kanan bawah untuk kembali.'); }
$('b-rec').onclick = toggleRec; $('unhide').onclick = toggleRec;

// ---------- map ----------
let mapBase = null;
function mapCanvas() {
  const sc = 4;
  if (!mapBase) { mapBase = document.createElement('canvas'); mapBase.width = W * sc; mapBase.height = H * sc; const g = mapBase.getContext('2d'); const cols = ['#1d6f86', '#3aa0b5', '#ecd59c', '#7cc25a', '#5e9b4a']; for (let y = 0; y < H; y++) for (let x = 0; x < W; x++) { g.fillStyle = cols[tile[y * W + x]]; g.fillRect(x * sc, y * sc, sc, sc); } g.fillStyle = 'rgba(30,80,40,.55)'; for (const t of trees) { g.beginPath(); g.arc(t.x * sc + 2, t.y * sc + 2, 1.6, 0, 7); g.fill(); } }
  const c = h('canvas', { id: 'mapcv', width: W * sc, height: H * sc }); const g = c.getContext('2d'); g.drawImage(mapBase, 0, 0);
  const dot = (x, y, col, s = 7) => { g.fillStyle = col; g.fillRect(x * sc - s / 2, y * sc - s / 2, s, s); };
  S.buildings.forEach(b => { const f = fpOf(b); g.fillStyle = '#e3c49a'; g.fillRect(b.x * sc, b.y * sc, f.w * sc, f.h * sc); });
  dot(LM.stone[0] + 1, LM.stone[1] + .5, '#cfd3cc', 9); dot(LM.light[0] + 1, LM.light[1] + 1, '#ffc94a', 10); dot(LM.camp[0] + .5, LM.camp[1] + 1, '#ff8a72', 9); dot(LM.wreck[0] + 1.5, LM.wreck[1] + 1, '#8a5a34', 9);
  g.strokeStyle = '#fff'; g.lineWidth = 2.5; g.beginPath(); g.arc((player.x + W / 2) * sc, (player.z + H / 2) * sc, 7, 0, 7); g.stroke();
  return c;
}

// ---------- building thumbnails for the palette ----------
const thumbs = {};
let thumbR = null;
function thumb(type) {
  if (!thumbs[type]) {
    if (!thumbR) { thumbR = { r: new THREE.WebGLRenderer({ antialias: true, alpha: true, preserveDrawingBuffer: true }), s: new THREE.Scene(), c: new THREE.PerspectiveCamera(30, 1, .1, 50) }; thumbR.r.setSize(96, 96); thumbR.r.outputColorSpace = THREE.SRGBColorSpace; thumbR.s.add(new THREE.HemisphereLight(0xffffff, 0x667744, 1.6)); const dl = new THREE.DirectionalLight(0xffffff, 1.8); dl.position.set(3, 5, 4); thumbR.s.add(dl); }
    const g = buildBuilding({ type, label: 'Papan' }); thumbR.s.add(g);
    const box = new THREE.Box3().setFromObject(g), size = box.getSize(new THREE.Vector3()), ctr = box.getCenter(new THREE.Vector3());
    const r = Math.max(size.x, size.y, size.z) * 1.6 + .5; thumbR.c.position.set(ctr.x + r * .7, ctr.y + r * .6, ctr.z + r * .9); thumbR.c.lookAt(ctr);
    thumbR.r.render(thumbR.s, thumbR.c); thumbs[type] = thumbR.r.domElement.toDataURL(); thumbR.s.remove(g);
  }
  return h('img', { src: thumbs[type], alt: '', width: '48', height: '48', style: 'width:48px;height:48px' });
}

// ---------- state changes ----------
const draftKey = 'pulau-aru-draft';
function applyWorld() { rebuildOcc(); rebuildNature(); rebuildBuildings(); rebuildClimbs(); rebuildNpcs(); postCount = -1; rebuildPosts(); stoneObj.userData.paint(S.residents.map(r => r.n), S.residents.length); UI.refreshHud(); }
function markDirty() { dirty = true; store.set(draftKey, JSON.stringify(S)); applyWorld(); }
const app = {
  get S() { return S; }, get dirty() { return dirty; }, get base() { try { return JSON.parse(PUB); } catch (e) { return null; } }, role, pop, lamps, curEp,
  markDirty, startPlace, startErase, endPlace, mapCanvas, thumb,
  markPublished() { PUB = JSON.stringify(S); dirty = false; store.del(draftKey); applyWorld(); },
  revert() { S = normalize(JSON.parse(PUB)); dirty = false; store.del(draftKey); applyWorld(); },
  replace(d) { S = d; markDirty(); },
};
UI.initUI(app);

// ---------- start ----------
function begin(kind, name) {
  role.kind = kind; role.name = name || 'Aru'; store.set('pulau-aru-role', JSON.stringify(role));
  if (fishing.st.active) fishing.setActive(false);
  $('start').hidden = true; cam.attract = false; setPlayerLook(); rebuildNpcs(); updateFishHud();
  if (kind === 'warga') {
    const [x, z] = fpCenter(LM.stone[0], LM.stone[1] + 2, 2, 1); player.x = x; player.z = z;
    const i = S.residents.findIndex(r => r.n.toLowerCase() === name.toLowerCase());
    toast(i >= 0 ? `Selamat datang, warga #${i + 1}. Namamu ada di Batu Nama.` : 'Selamat datang. Follow untuk jadi warga, dan namamu diukir di batu.');
  } else toast('Kamu adalah Aru. Jelajahi pulaumu.');
  $('hint').textContent = touch ? 'Geser kiri untuk jalan, kanan untuk kamera' : 'WASD jalan · Spasi lompat · E interaksi · geser mouse untuk kamera';
  $('hint').hidden = false; setTimeout(() => $('hint').hidden = true, 5000);
  if (touch) { $('act').hidden = false; updatePrompt(); }
}
$('st-aru').onclick = () => begin('aru', 'Aru');
const joinFn = () => { const n = clean($('st-user').value); if (!n) { $('st-user').focus(); toast('Tulis username TikTok kamu.'); return; } begin('warga', n); };
$('st-join').onclick = joinFn; $('st-user').addEventListener('keydown', e => { if (e.key === 'Enter') joinFn(); });
if (touch) $('st-keys').textContent = 'Jempol kiri untuk berjalan · geser kanan untuk memutar kamera · tombol AKSI untuk berinteraksi';
try { const r = JSON.parse(store.get('pulau-aru-role') || 'null'); if (r && r.kind === 'warga') $('st-user').value = r.name; } catch (e) { }

// initial placement
{ const [x, z] = fpCenter(LM.camp[0], LM.camp[1] + 4, 1, 1); player.x = x; player.z = z; }
setPlayerLook();
applyWorld();
cam.target.set(player.x, 1, player.z);
requestAnimationFrame(frame);

(async () => {
  S = await loadState(); PUB = JSON.stringify(S);
  if (ADMIN) {
    $('b-admin').hidden = false;
    try { const d = JSON.parse(store.get(draftKey) || 'null'); if (d && JSON.stringify(normalize(d)) !== PUB) { S = normalize(d); dirty = true; setTimeout(() => toast('Draf yang belum terbit dipulihkan.'), 600); } } catch (e) { }
  }
  applyWorld();
  $('st-aru').disabled = false; $('st-aru').textContent = 'Main sebagai Aru'; $('st-join').disabled = false;
  // visitors pick up new published versions without reloading
  setInterval(async () => {
    if (dirty || document.hidden) return;
    const n = await loadState(); const js = JSON.stringify(n);
    if (js !== PUB && n.v) { S = n; PUB = js; applyWorld(); toast('Pulau baru saja diperbarui.'); }
  }, 90000);
})();

window.__pulau = { app, LM, fishing, sail, I2, get player() { return player; } };
