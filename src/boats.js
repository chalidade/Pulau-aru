// Fishing boats: every "Perahu" a resident sails out, stops to fish, and comes back. Anyone can borrow one.
import * as THREE from 'three';
import { makeCharacter, lookOf, mat, G } from './models.js';

function rod() {
  const g = new THREE.Group();
  const pole = new THREE.Mesh(G.cyl6, mat('#8a6a3a')); pole.scale.set(.018, 1.9, .018); pole.position.set(0, .95, 0); g.add(pole);
  g.rotation.set(1.0, 0, -.4); g.position.set(.2, .7, .1);
  return g;
}

export function createBoats({ scene, navigable, home }) {
  const state = new Map(); // key → { x, z, ry, speed, mode, t, tx, tz, rider, line, bob, obj, held }
  const keyOf = b => `${b.x},${b.y}`;

  function sync(boatObjs, names) {
    const seen = new Set();
    boatObjs.forEach((o, i) => {
      const b = o.userData.b, k = keyOf(b); seen.add(k);
      let s = state.get(k);
      if (!s) {
        s = { x: o.position.x, z: o.position.z, ry: o.rotation.y, speed: 0, mode: 'wait', t: 1 + i * 2.3, tx: null, tz: null, hx: o.position.x, hz: o.position.z };
        state.set(k, s);
      }
      // the building object is rebuilt on every world change: re-dress it
      s.obj = o;
      const r = makeCharacter(lookOf((names[i % Math.max(1, names.length)] || 'nelayan') + i));
      r.scale.setScalar(.8 * .9); r.position.set(-.25, .05, 0); r.rotation.y = Math.PI / 2;
      const u = r.userData; u.legL.rotation.x = -1.4; u.legR.rotation.x = -1.4; u.body.position.y = -.38; u.armL.rotation.x = -.8; u.armR.rotation.x = -1;
      o.add(r); s.rider = r;
      const rd = rod(); r.add(rd); s.rod = rd;
      if (!s.bob) {
        s.line = new THREE.Line(new THREE.BufferGeometry().setAttribute('position', new THREE.BufferAttribute(new Float32Array(6), 3)), new THREE.LineBasicMaterial({ color: '#f0f0f0', transparent: true, opacity: .7 }));
        s.bob = new THREE.Mesh(G.sph, mat('#e8463a')); s.bob.scale.setScalar(.06); scene.add(s.line, s.bob);
      }
    });
    for (const [k, s] of state) if (!seen.has(k)) { scene.remove(s.line, s.bob); state.delete(k); }
  }

  function pickTarget(s) {
    for (let k = 0; k < 24; k++) {
      const a = Math.random() * Math.PI * 2, r = 6 + Math.random() * 16;
      const tx = s.hx + Math.cos(a) * r, tz = s.hz + Math.sin(a) * r;
      let ok = navigable(tx, tz);
      for (let j = 1; ok && j <= 12; j++) { const f = j / 12; ok = navigable(s.x + (tx - s.x) * f, s.z + (tz - s.z) * f); }
      if (ok) { s.tx = tx; s.tz = tz; return true; }
    }
    return false;
  }

  const tip = new THREE.Vector3(), bobP = new THREE.Vector3();
  function update(dt, T) {
    for (const s of state.values()) {
      if (!s.obj) continue;
      if (s.mode !== 'player') {
        s.t -= dt;
        if (s.mode === 'wait' || s.mode === 'fish') {
          s.speed = Math.max(0, s.speed - dt * 2);
          if (s.t <= 0) { if (pickTarget(s)) { s.mode = 'go'; } else s.t = 2; }
        } else if (s.mode === 'go') {
          const dx = s.tx - s.x, dz = s.tz - s.z, d = Math.hypot(dx, dz);
          const want = Math.atan2(-dz, dx); let dr = want - s.ry; dr = Math.atan2(Math.sin(dr), Math.cos(dr));
          s.ry += Math.sign(dr) * Math.min(Math.abs(dr), dt * 1.4);
          s.speed = Math.min(2.6, s.speed + dt * 1.5) * (d < 2 ? Math.max(.3, d / 2) : 1);
          if (d < .6) { s.mode = 'fish'; s.t = 9 + Math.random() * 10; }
        }
        const cx = Math.cos(s.ry), cz = -Math.sin(s.ry), nx = s.x + cx * s.speed * dt, nz = s.z + cz * s.speed * dt;
        if (navigable(nx + cx * 1.2, nz + cz * 1.2)) { s.x = nx; s.z = nz; } else if (s.mode === 'go') { s.mode = 'wait'; s.t = .5; }
      }
      const o = s.obj;
      o.position.set(s.x, Math.sin(T * 1.3 + s.hx) * .06, s.z);
      o.rotation.set(Math.sin(T * 1.1 + s.hz) * .05, s.ry, Math.sin(T * .9 + s.hx) * .05);
      const fishing = s.mode === 'fish' || s.mode === 'wait';
      s.rider.visible = s.mode !== 'player';
      s.rod.visible = fishing; s.line.visible = s.bob.visible = fishing && s.rider.visible;
      const u = s.rider.userData;
      u.armR.rotation.x = fishing ? -1 + Math.sin(T * 1.3 + s.hx) * .05 : -.6 + Math.sin(T * 5) * .6; // rowing while moving
      u.armL.rotation.x = fishing ? -.8 : -.6 - Math.sin(T * 5) * .6;
      if (fishing && s.rider.visible) {
        o.updateMatrixWorld(true); s.rod.updateMatrixWorld(true); tip.set(0, 1.9, 0).applyMatrix4(s.rod.matrixWorld);
        const side = s.ry - Math.PI / 2; bobP.set(s.x + Math.cos(side) * 2.4, Math.sin(T * 2 + s.hx) * .02 - (Math.sin(T * .8 + s.hz) > .97 ? .1 : 0), s.z - Math.sin(side) * 2.4);
        s.bob.position.copy(bobP);
        const p = s.line.geometry.attributes.position; p.setXYZ(0, tip.x, tip.y, tip.z); p.setXYZ(1, bobP.x, bobP.y, bobP.z); p.needsUpdate = true; s.line.geometry.computeBoundingSphere();
      }
    }
  }
  function nearest(x, z, r) { let best = null, bd = r; for (const s of state.values()) { const d = Math.hypot(s.x - x, s.z - z); if (d < bd) { bd = d; best = s; } } return best; }
  return { sync, update, nearest, get all() { return [...state.values()]; } };
}
