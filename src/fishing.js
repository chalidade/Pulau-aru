// Spear fishing: pick up a spear at a "Rak tombak", walk to shallow water, throw at the fish.
import * as THREE from 'three';
import * as WD from './world.js';
import { W, H, tile, groundY } from './world.js';
import { mat, spearMesh, G } from './models.js';
import { store } from './data.js';

const SPECIES = [
  { n: 'ikan baronang', c: '#c9b26a', w: 30 }, { n: 'ikan kakap merah', c: '#d0483a', w: 22 },
  { n: 'ikan tongkol', c: '#4a6a9a', w: 20 }, { n: 'ikan kerapu', c: '#8a6a4a', w: 14 },
  { n: 'ikan badut', c: '#ff8a3a', w: 10 }, { n: 'ikan emas berkilau', c: '#ffd24a', w: 4, rare: true },
];
const pickSpecies = () => { let r = Math.random() * SPECIES.reduce((a, s) => a + s.w, 0); for (const s of SPECIES) { r -= s.w; if (r <= 0) return s; } return SPECIES[0]; };
const statsKey = 'pulau-aru-fish';
const UP = new THREE.Vector3(0, 1, 0);

export function createFishing({ scene, player, toast, onChange }) {
  const st = { active: false, fish: [], flying: null, caught: [], cool: 0 };
  try { const s = JSON.parse(store.get(statsKey) || '{}'); st.total = s.total | 0; st.best = s.best || {}; } catch (e) { st.total = 0; st.best = {}; }
  const group = new THREE.Group(); scene.add(group);

  // spear held in the right hand
  const held = new THREE.Group(); spearMesh(held); held.rotation.x = Math.PI / 2 - .25; held.position.set(0, -.45, .1); held.scale.setScalar(.85);
  // aim ring on the water
  const ring = new THREE.Mesh(new THREE.RingGeometry(.35, .45, 20), new THREE.MeshBasicMaterial({ color: '#fff3c4', transparent: true, opacity: .7, depthWrite: false, side: THREE.DoubleSide }));
  ring.rotation.x = -Math.PI / 2; ring.visible = false; scene.add(ring);
  const splash = new THREE.Mesh(new THREE.RingGeometry(.2, .3, 20), new THREE.MeshBasicMaterial({ color: '#ffffff', transparent: true, opacity: 0, depthWrite: false, side: THREE.DoubleSide }));
  splash.rotation.x = -Math.PI / 2; scene.add(splash);
  let splashT = 9;

  const isWater = (x, z) => { const t = tile[WD.w2cy(z) * W + WD.w2cx(x)]; return t === WD.SHALLOW || t === WD.DEEP; };
  const isShallow = (x, z) => tile[WD.w2cy(z) * W + WD.w2cx(x)] === WD.SHALLOW;

  function makeFish() {
    const sp = pickSpecies(), g = new THREE.Group();
    const m = sp.rare ? new THREE.MeshStandardMaterial({ color: sp.c, emissive: '#ffb020', emissiveIntensity: .6, flatShading: true }) : mat(sp.c);
    const body = new THREE.Mesh(G.ico, m); body.scale.set(.12, .1, .26); g.add(body);
    const tail = new THREE.Mesh(G.cone4, m); tail.scale.set(.1, .14, .03); tail.rotation.x = -Math.PI / 2; tail.position.z = -.3; g.add(tail);
    g.userData.tail = tail;
    return { g, sp, vx: 0, vz: 0, t: Math.random() * 9, flee: 0 };
  }
  function spawnNear() {
    for (let k = 0; k < 12; k++) {
      const a = Math.random() * Math.PI * 2, r = 2.5 + Math.random() * 7, x = player.x + Math.cos(a) * r, z = player.z + Math.sin(a) * r;
      if (Math.abs(x) < W / 2 - 1 && Math.abs(z) < H / 2 - 1 && isShallow(x, z)) { const f = makeFish(); f.x = x; f.z = z; f.g.position.set(x, -.3, z); group.add(f.g); st.fish.push(f); return; }
    }
  }
  function setActive(on) {
    st.active = on;
    const arm = player.obj && player.obj.userData.armR;
    if (on && arm) arm.add(held); else if (held.parent) held.parent.remove(held);
    if (!on) { st.fish.forEach(f => group.remove(f.g)); st.fish = []; ring.visible = false; }
    toast(on ? 'Tombak di tangan. Cari air dangkal, ikan berenang di sana.' : 'Tombak dikembalikan ke rak.');
    onChange && onChange();
  }
  function aimPoint() { const r = player.obj.rotation.y; return { x: player.x + Math.sin(r) * 2.4, z: player.z + Math.cos(r) * 2.4 }; }
  function canThrow() { if (!st.active || st.flying || st.cool > 0) return false; const a = aimPoint(); return isWater(a.x, a.z); }

  function throwAt(target) {
    if (!st.active || st.flying || st.cool > 0) return false;
    const a = target || aimPoint();
    if (!isWater(a.x, a.z)) { toast('Arahkan ke air.'); return false; }
    if (target) player.obj.rotation.y = Math.atan2(a.x - player.x, a.z - player.z);
    const sp = new THREE.Group(); spearMesh(sp); group.add(sp);
    const from = new THREE.Vector3(player.x, player.obj.position.y + 1.3, player.z), to = new THREE.Vector3(a.x, -.25, a.z);
    held.visible = false;
    st.flying = { sp, from, to, t: 0, dur: .32 };
    return true;
  }
  function land(f) {
    const { to, sp } = f;
    splash.position.set(to.x, .03, to.z); splashT = 0;
    let hit = null, bd = .85;
    for (const fish of st.fish) { const d = Math.hypot(fish.x - to.x, fish.z - to.z); if (d < bd) { bd = d; hit = fish; } }
    for (const fish of st.fish) { const d = Math.hypot(fish.x - to.x, fish.z - to.z); if (d < 2.5 && fish !== hit) { fish.flee = 1.2; const k = 1 / Math.max(.2, d); fish.vx = (fish.x - to.x) * k * 2.4; fish.vz = (fish.z - to.z) * k * 2.4; } }
    if (hit) {
      st.fish = st.fish.filter(x => x !== hit);
      st.caught.push({ g: hit.g, t: 0, x: to.x, z: to.z, spear: sp });
      st.total++; st.best[hit.sp.n] = (st.best[hit.sp.n] | 0) + 1;
      store.set(statsKey, JSON.stringify({ total: st.total, best: st.best }));
      toast(`${hit.sp.rare ? 'Langka! ' : ''}Dapat ${hit.sp.n}! Total tangkapanmu: ${st.total}`);
      onChange && onChange();
    } else {
      if (Math.random() < .5) toast(['Meleset! Ikannya kabur.', 'Hampir! Coba lagi.', 'Airnya berkecipak, ikannya lari.'][(Math.random() * 3) | 0]);
      setTimeout(() => group.remove(sp), 500);
    }
    st.cool = .35; held.visible = true;
  }

  function update(dt, T) {
    if (st.cool > 0) st.cool -= dt;
    if (splashT < 1) { splashT += dt * 2; splash.material.opacity = (1 - splashT) * .8; splash.scale.setScalar(1 + splashT * 3); } else splash.material.opacity = 0;
    if (st.flying) {
      const f = st.flying; f.t += dt / f.dur; const t = Math.min(1, f.t);
      const p = f.from.clone().lerp(f.to, t); p.y += Math.sin(t * Math.PI) * .6;
      const dir = p.clone().sub(f.last || f.from); if (dir.lengthSq() > 1e-6) f.sp.quaternion.setFromUnitVectors(UP, dir.normalize());
      f.last = p.clone(); f.sp.position.copy(p).addScaledVector(dir, -1.7);
      if (t >= 1) { st.flying = null; land(f); }
    }
    // caught fish leap out on the spear, then vanish
    st.caught = st.caught.filter(c => {
      c.t += dt; const k = c.t / .9;
      c.g.position.set(c.x, -.2 + Math.sin(Math.min(1, k) * Math.PI) * 1.4, c.z); c.g.rotation.x = -Math.PI / 2; c.g.rotation.z += dt * 10;
      c.spear.position.set(c.x, c.g.position.y - 1.75, c.z); c.spear.quaternion.identity();
      if (k >= 1) { group.remove(c.g); group.remove(c.spear); return false; }
      return true;
    });
    if (!st.active) return;
    while (st.fish.length < 9) { const n = st.fish.length; spawnNear(); if (st.fish.length === n) break; }
    for (const f of st.fish) {
      f.t += dt;
      if (f.flee > 0) f.flee -= dt;
      else if (Math.random() < dt * .8) { const a = Math.random() * Math.PI * 2, s = .4 + Math.random() * .6; f.vx = Math.cos(a) * s; f.vz = Math.sin(a) * s; }
      const nx = f.x + f.vx * dt, nz = f.z + f.vz * dt;
      if (isShallow(nx, nz)) { f.x = nx; f.z = nz; } else { f.vx *= -1; f.vz *= -1; }
      const y = Math.min(-.18, Math.max(groundY(f.x, f.z) + .12, -.45));
      f.g.position.set(f.x, y + Math.sin(f.t * 3) * .03, f.z);
      if (Math.hypot(f.vx, f.vz) > .05) f.g.rotation.y = Math.atan2(f.vx, f.vz);
      f.g.userData.tail.rotation.y = Math.sin(f.t * (f.flee > 0 ? 30 : 12)) * .5;
    }
    st.fish = st.fish.filter(f => { if (Math.hypot(f.x - player.x, f.z - player.z) > 22) { group.remove(f.g); return false; } return true; });
    const a = aimPoint(), ok = isWater(a.x, a.z) && !st.flying;
    ring.visible = ok; if (ok) { ring.position.set(a.x, .04 + Math.sin(T * 4) * .01, a.z); ring.material.opacity = .45 + Math.sin(T * 5) * .2; }
  }
  return { st, setActive, throwAt, canThrow, update, isWater, toggle: () => setActive(!st.active) };
}
