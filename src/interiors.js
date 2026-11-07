// Interiors: walk into a building. Each room is a cut-away diorama (back and side walls full height, front wall low)
// built far away from the island when you enter and thrown away when you leave. Rooms open one by one through the
// episodes: data/island.json → interiors: ["masjid", ...]. A building with a room but not yet opened shows a lock.
import * as THREE from 'three';
import { bake, box, mat, G, windowMat, lanternMat, makeCharacter, animateCharacter, lookOf, sitBodyY } from './models.js';

const doorMat = new THREE.MeshStandardMaterial({ color: '#ffe7a8', emissive: '#ffd36a', emissiveIntensity: .6 });
export const OX = -320, OZ = 320;           // where rooms are built (far off the map, hidden by fog)
const inside = (x, z) => Math.abs(x - OX) < 40 && Math.abs(z - OZ) < 40;
export const insideRoom = inside;

const canvasPlane = (lines, w, h, o = {}) => {
  const c = document.createElement('canvas'); c.width = 512; c.height = Math.round(512 * h / w); const x = c.getContext('2d');
  x.fillStyle = o.bg || '#1f3b2e'; x.fillRect(0, 0, c.width, c.height);
  if (o.frame) { x.strokeStyle = o.frame; x.lineWidth = 14; x.strokeRect(7, 7, c.width - 14, c.height - 14); }
  x.fillStyle = o.color || '#f2f2ea'; x.textAlign = 'center'; x.textBaseline = 'middle';
  const fs = o.size || Math.min(44, (c.height - 30) / (lines.length + .6)); x.font = `700 ${fs}px "Pixelify Sans", monospace`;
  lines.forEach((t, i) => x.fillText(t, c.width / 2, c.height / 2 + (i - (lines.length - 1) / 2) * fs * 1.25, c.width - 30));
  const tex = new THREE.CanvasTexture(c); tex.colorSpace = THREE.SRGBColorSpace;
  return new THREE.Mesh(new THREE.PlaneGeometry(w, h), new THREE.MeshStandardMaterial({ map: tex, roughness: .9 }));
};
const chair = (g, x, z, ry = 0, col = '#8a5a34') => { const c = new THREE.Group(); c.position.set(x, 0, z); c.rotation.y = ry; g.add(c); box(c, col, .45, .08, .45, 0, .42, 0); box(c, col, .45, .5, .07, 0, .5, -.2); for (const [a, b] of [[-.18, -.18], [.18, -.18], [-.18, .18], [.18, .18]]) box(c, col, .05, .42, .05, a, 0, b); return c; };
const table = (g, x, z, w, d, col = '#9a6b42', h = .75) => { box(g, col, w, .07, d, x, h - .07, z); for (const [a, b] of [[-1, -1], [1, -1], [-1, 1], [1, 1]]) box(g, col, .07, h - .07, .07, x + a * (w / 2 - .1), 0, z + b * (d / 2 - .1)); };

// Every room: size, colours, what is inside, where people are and what they do.
// spots: [x, z, facing, pose, label?]  pose: sit | pray | stand | write | lie | cook | serve
export const ROOMS = {
  masjid: { title: 'Masjid', w: 13, d: 10, wall: '#f3eee2', trim: '#2f8a5a', floor: '#e9e1cf',
    build(g, c) {
      for (let r = 0; r < 4; r++) box(g, r % 2 ? '#2e9a63' : '#3fae74', 11, .02, 1.6, 0, .05, -2.4 + r * 1.75);  // prayer rugs
      box(g, '#d9cfb4', 2.2, 2.6, .25, 0, 0, -4.85); const arch = new THREE.Mesh(new THREE.CircleGeometry(.8, 18, 0, Math.PI), mat('#2f8a5a')); arch.position.set(0, 2.2, -4.7); g.add(arch); box(g, '#2f8a5a', 1.6, 2.2, .05, 0, 0, -4.7);   // mihrab
      box(g, '#8a5a34', 1, .3, 1, 3.2, 0, -4.2); box(g, '#8a5a34', 1, .3, .7, 3.2, .3, -4.35); box(g, '#8a5a34', 1, .3, .4, 3.2, .6, -4.5); c.push([2.6, -4.8, 3.8, -3.6]);  // minbar
      for (const x of [-4, 0, 4]) { const l = new THREE.Mesh(G.sph, lanternMat); l.scale.set(.25, .3, .25); l.position.set(x, 2.6, -1); g.add(l); box(g, '#5e3b22', .03, .8, .03, x, 2.75, -1); }
      box(g, '#8a5a34', 2.2, .9, .4, -5, 0, -4.6); for (let i = 0; i < 6; i++) box(g, ['#b33', '#36b', '#3a5', '#c93'][i % 4], .12, .3, .25, -5.9 + i * .3, .9, -4.6); c.push([-6.1, -4.9, -3.9, -4.3]);  // Qur'an shelf
    },
    spots: [[-3, -2.4, Math.PI, 'pray'], [-1.5, -2.4, Math.PI, 'pray'], [0, -2.4, Math.PI, 'pray'], [1.5, -2.4, Math.PI, 'pray'], [3, -2.4, Math.PI, 'pray'], [-2.2, -.65, Math.PI, 'pray'], [-.7, -.65, Math.PI, 'pray'], [.8, -.65, Math.PI, 'pray'], [2.3, -.65, Math.PI, 'pray'], [0, -4.1, Math.PI, 'stand', 'Imam']] },
  sekolah: { title: 'Sekolah', w: 11, d: 9, wall: '#fbf3dc', trim: '#c4473a', floor: '#c9a77c',
    build(g, c, ctx) {
      box(g, '#5e3b22', 6.2, 2.2, .12, 0, .7, -4.35);
      const names = ctx.newest(8).map(n => '@' + n);
      const bb = canvasPlane(['Selamat datang, murid baru!'].concat(names.length ? names : ['(belum ada)']), 6, 2.1, { bg: '#26493a', color: '#f4f1e6' }); bb.position.set(0, 1.8, -4.28); g.add(bb);
      table(g, -3.6, -3.2, 1.6, .8, '#7a4f2d'); chair(g, -3.6, -2.5, Math.PI); c.push([-4.5, -3.7, -2.7, -2.7]);
      for (let r = 0; r < 3; r++) for (let k = 0; k < 3; k++) { const x = -2.6 + k * 2.6, z = -1.2 + r * 1.7; table(g, x, z, 1.2, .6, '#b07a48'); chair(g, x, z + .55, Math.PI); c.push([x - .65, z - .35, x + .65, z + .35]); }
      for (const x of [-4.8, 4.8]) { const gl = new THREE.Mesh(G.sph, mat('#4a8fd1')); gl.scale.setScalar(.25); gl.position.set(x, 1.2, -4); g.add(gl); box(g, '#5e3b22', .5, 1, .5, x, 0, -4); c.push([x - .3, -4.3, x + .3, -3.7]); }
    },
    spots: [[-2.6, -.65, Math.PI, 'sit'], [0, -.65, Math.PI, 'sit'], [2.6, -.65, Math.PI, 'sit'], [-2.6, 1.05, Math.PI, 'sit'], [0, 1.05, Math.PI, 'sit'], [2.6, 1.05, Math.PI, 'sit'], [0, 2.75, Math.PI, 'sit'], [-1.6, -3.7, 0, 'write', 'Ibu Guru']] },
  rumahsakit: { title: 'Rumah Sakit', w: 13, d: 9, wall: '#f4f8f7', trim: '#2aa198', floor: '#dfe9e7',
    build(g, c) {
      for (let i = 0; i < 4; i++) { const x = -4.5 + i * 3; box(g, '#c9d3d1', 1.1, .55, 2.1, x, 0, -3.1); box(g, '#ffffff', 1.0, .12, 1.9, x, .55, -3.1); box(g, '#b8e0f2', .9, .12, .4, x, .67, -3.85); box(g, '#9fd3c7', .03, 1.9, 2.2, x + 1.3, 0, -3.1); c.push([x - .6, -4.2, x + .6, -2]); }
      box(g, '#2aa198', 3.4, 1.05, .8, 3.5, 0, 2.2); box(g, '#f4f8f7', 3.4, .08, .9, 3.5, 1.05, 2.2); c.push([1.7, 1.7, 5.3, 2.7]);
      const s = canvasPlane(['UGD', 'Rumah Sakit Pulau'], 2.4, .9, { bg: '#2aa198' }); s.position.set(0, 2.2, -4.28); g.add(s);
      for (let i = 0; i < 4; i++) chair(g, -4.6 + i * .7, 2.6, 0, '#5b7d8a');
    },
    spots: [[-4.5, -3.3, 0, 'lie'], [1.5, -3.3, 0, 'lie'], [-3, -1.6, Math.PI, 'stand', 'Dokter'], [3.5, 1.5, 0, 'serve', 'Perawat'], [-4.6, 2.6, 0, 'sit'], [-3.2, 2.6, 0, 'sit']] },
  rumah: { title: 'Rumah Warga', w: 9, d: 7, wall: '#f6e8cf', trim: '#c4473a', floor: '#b88a5a',
    build(g, c) {
      box(g, '#c98a5a', 3, .02, 2, -1.2, .05, .2);   // rug
      box(g, '#4f7cac', 2.4, .45, .9, -1.2, 0, -1.4); box(g, '#4f7cac', 2.4, .5, .25, -1.2, .45, -1.75); c.push([-2.5, -1.9, .1, -.9]);  // sofa
      table(g, -1.2, .3, 1.2, .6, '#8a5a34', .45); c.push([-1.85, 0, -.55, .6]);
      box(g, '#3b3b3b', 1.4, .5, .4, -1.2, 0, 3.0); box(g, '#111', 1.2, .7, .06, -1.2, .5, 3.0);   // tv
      box(g, '#e8e2d4', 3, .9, .7, 2.7, 0, -2.9); box(g, '#9aa', .5, .1, .4, 2.2, .9, -2.9); const pot = new THREE.Mesh(G.cyl8, mat('#555')); pot.scale.set(.18, .15, .18); pot.position.set(3.2, .98, -2.9); g.add(pot); c.push([1.1, -3.3, 4.3, -2.5]);  // kitchen
      table(g, 2.7, -.6, 1.4, .9, '#a3744a'); chair(g, 2.2, 0, Math.PI); chair(g, 3.2, 0, Math.PI); c.push([1.9, -1.1, 3.5, -.1]);
    },
    spots: [[-1.8, -1.2, 0, 'sit'], [-.6, -1.2, 0, 'sit'], [2.7, -2.4, Math.PI, 'cook'], [3.2, .05, Math.PI, 'sit']] },
  rumahpresiden: { title: 'Rumah Presiden', w: 13, d: 10, wall: '#f3eee2', trim: '#b8862e', floor: '#7a5233',
    build(g, c) {
      box(g, '#8a1d1d', 9, .02, 4.4, 0, .05, -.6);   // red carpet
      table(g, 0, -.6, 6, 1.6, '#5e3b22'); c.push([-3.1, -1.5, 3.1, .3]);
      for (let i = 0; i < 4; i++) { chair(g, -2.25 + i * 1.5, -1.8, 0, '#3b2a1e'); chair(g, -2.25 + i * 1.5, .6, Math.PI, '#3b2a1e'); }
      chair(g, -3.6, -.6, Math.PI / 2, '#b8862e'); chair(g, 3.6, -.6, -Math.PI / 2, '#b8862e');
      box(g, '#d0d0d0', .05, 2.2, .05, 5.4, 0, -4.4); box(g, '#e8343f', .9, .3, .02, 5.85, 1.9, -4.4); box(g, '#ffffff', .9, .3, .02, 5.85, 1.6, -4.4);  // flag
      const p = canvasPlane(['PULAU NETIZEN', 'ruang rapat kabinet'], 3, 1.1, { bg: '#3b2a1e', color: '#f2d27a', frame: '#b8862e' }); p.position.set(0, 1.9, -4.28); g.add(p);
    },
    spots: [[-3.6, -.6, Math.PI / 2, 'sit', 'Presiden'], [3.6, -.6, -Math.PI / 2, 'sit', 'Wakil Presiden'], [-2.25, -1.8, 0, 'sit'], [-.75, -1.8, 0, 'sit'], [.75, .6, Math.PI, 'sit'], [2.25, .6, Math.PI, 'sit']] },
  warteg: { title: 'Warteg', w: 9, d: 7, wall: '#f4ead2', trim: '#2c7a3f', floor: '#d8c7a6',
    build(g, c) {
      box(g, '#cfd8d6', 4, .9, .7, 0, 0, -2.6); box(g, '#bfe3f0', 4, .5, .7, 0, .9, -2.6); for (let i = 0; i < 6; i++) { const b = new THREE.Mesh(G.cyl8, mat(['#e2a23b', '#7a3b1e', '#3f8f3a', '#d8d0b8', '#c7462e', '#f2d27a'][i])); b.scale.set(.25, .08, .2); b.position.set(-1.6 + i * .64, .95, -2.6); g.add(b); } c.push([-2.1, -3, 2.1, -2.2]);
      for (const z of [0, 1.8]) { table(g, 0, z, 3.4, .8, '#a3744a'); box(g, '#7a4f2d', 3.4, .45, .3, 0, 0, z - .65); box(g, '#7a4f2d', 3.4, .45, .3, 0, 0, z + .65); c.push([-1.8, z - .8, 1.8, z + .8]); }
    },
    spots: [[0, -3.2, 0, 'serve', 'Ibu Warteg'], [-1, -.65, 0, 'sit'], [.8, -.65, 0, 'sit'], [-.3, .65, Math.PI, 'sit'], [1, 2.45, Math.PI, 'sit']] },
  kedaikopi: { title: 'Kedai Kopi', w: 9, d: 7, wall: '#e9d9bf', trim: '#5e3b22', floor: '#8a5a34',
    build(g, c) {
      box(g, '#5e3b22', 4, 1.05, .7, -.5, 0, -2.5); box(g, '#3b2a1e', 4.2, .08, .8, -.5, 1.05, -2.5); box(g, '#c9c9c9', .5, .45, .4, -1.8, 1.13, -2.5); c.push([-2.6, -2.9, 1.6, -2.1]);
      for (const [x, z] of [[-2.5, .3], [0, .3], [2.5, .3], [-1.2, 2.2], [1.4, 2.2]]) { const t = new THREE.Mesh(G.cyl8, mat('#3b2a1e')); t.scale.set(.4, .05, .4); t.position.set(x, .72, z); g.add(t); box(g, '#3b2a1e', .08, .7, .08, x, 0, z); chair(g, x - .55, z, Math.PI / 2, '#6b4a2b'); chair(g, x + .55, z, -Math.PI / 2, '#6b4a2b'); c.push([x - .45, z - .45, x + .45, z + .45]); }
    },
    spots: [[-.5, -3.1, 0, 'serve', 'Barista'], [-3.05, .3, Math.PI / 2, 'sit'], [-.55, .3, Math.PI / 2, 'sit'], [3.05, .3, -Math.PI / 2, 'sit'], [-1.75, 2.2, Math.PI / 2, 'sit']] },
  apotik: { title: 'Apotik', w: 8, d: 6, wall: '#f6f6f2', trim: '#2f9a5b', floor: '#e3ece6',
    build(g, c) {
      for (const x of [-2.4, 0, 2.4]) { box(g, '#e8e8e2', 2, 2.1, .4, x, 0, -2.75); for (let s = 0; s < 4; s++) for (let i = 0; i < 6; i++) box(g, ['#e85d5d', '#5d9be8', '#f2c94c', '#8fd18f'][(i + s) % 4], .22, .25, .25, x - .75 + i * .3, .2 + s * .5, -2.65); }
      c.push([-3.5, -3, 3.5, -2.5]);
      box(g, '#2f9a5b', 4, 1.0, .6, 0, 0, -.6); box(g, '#f6f6f2', 4, .06, .7, 0, 1.0, -.6); c.push([-2.1, -1, 2.1, -.2]);
    },
    spots: [[0, -1.3, 0, 'serve', 'Apoteker'], [-.6, .3, Math.PI, 'stand'], [.9, .6, Math.PI, 'stand']] },
};

/** Room controller: enter(type, building, residentNames) / exit() / walkable / surface / interactables / update */
export function createInteriors({ scene, newest, who }) {
  let cur = null;
  function build(type) {
    const R = ROOMS[type], g = new THREE.Group(); g.position.set(OX, 0, OZ); scene.add(g);
    const W = R.w, D = R.d, H = 2.8, wall = mat(R.wall), cols = [];
    box(g, R.floor, W + .4, .12, D + .4, 0, -.12, 0);
    const yard = new THREE.Mesh(new THREE.PlaneGeometry(120, 120), mat('#6fa65a')); yard.rotation.x = -Math.PI / 2; yard.position.y = -.2; yard.receiveShadow = true; g.add(yard);
    box(g, wall, W + .4, H, .2, 0, 0, -D / 2 - .1);                                         // back
    for (const s of [-1, 1]) { box(g, wall, .2, H, D + .4, s * (W / 2 + .1), 0, 0); for (const z of [-D / 4, D / 4]) box(g, windowMat, .05, .9, 1.2, s * (W / 2 - .02), 1.1, z); }
    for (const s of [-1, 1]) box(g, wall, W / 2 - .7, .5, .2, s * (W / 4 + .35), 0, D / 2 + .1);   // low front wall with a door gap
    box(g, R.trim, W + .4, .14, .24, 0, H, -D / 2 - .1);
    const dm = new THREE.Mesh(G.box, doorMat); dm.scale.set(1.2, .04, .6); dm.position.set(0, .02, D / 2 + .1); g.add(dm);
    R.build(g, cols, { newest });
    bake(g);   // walls and furniture merge into a handful of meshes; no extra light (adding one recompiles every shader)
    // people
    const people = R.spots.map(([x, z, f, pose, label], i) => {
      const pool = newest(40), real = label && who ? who(label) : null;
      const nm = real || (label ? null : pool[(i * 7) % Math.max(1, pool.length)]) || label || 'Warga';
      const ch = makeCharacter(lookOf(real || (label ? label + ':' + type : nm))); ch.position.set(x, 0, z); ch.rotation.y = f; g.add(ch);
      return { ch, pose, label: real ? label + ' @' + real : label || ('@' + nm), x: OX + x, z: OZ + z, ph: i * 1.3 };
    });
    return { type, R, g, cols, people, W, D };
  }
  function pose(p, T) {
    const u = p.ch.userData, ph = T + p.ph; u.body.rotation.x = 0; u.body.position.y = 0; p.ch.position.y = 0;
    for (const k of ['legL', 'legR', 'armL', 'armR']) { u[k].rotation.x = 0; u[k].rotation.z = 0; }
    if (p.pose === 'sit') { u.body.position.y = sitBodyY(.5); u.legL.rotation.x = -1.3; u.legR.rotation.x = -1.25; u.armL.rotation.x = -.6; u.armR.rotation.x = -.6 + Math.sin(ph * 1.6) * .15; }
    else if (p.pose === 'pray') {          // standing, bowing and prostrating in a slow cycle
      const c = (ph * .25) % 4;
      if (c < 1.4) { u.armL.rotation.x = -1.2; u.armR.rotation.x = -1.2; }
      else if (c < 2.2) { u.body.rotation.x = .9; u.armL.rotation.x = -.6; u.armR.rotation.x = -.6; }
      else { u.body.position.y = -.5; u.body.rotation.x = 1.25; u.legL.rotation.x = -1.6; u.legR.rotation.x = -1.6; u.armL.rotation.x = -2.2; u.armR.rotation.x = -2.2; }
    }
    else if (p.pose === 'write') { u.armR.rotation.x = -2.3 + Math.sin(ph * 5) * .2; u.armR.rotation.z = Math.sin(ph * 3) * .3; }
    else if (p.pose === 'lie') { p.ch.rotation.x = -Math.PI / 2; p.ch.position.y = .72; p.ch.position.z = p.z - OZ + 1; u.armL.rotation.x = Math.sin(ph) * .05; }
    else if (p.pose === 'cook') { u.armR.rotation.x = -1.2 + Math.sin(ph * 6) * .5; u.armL.rotation.x = -1.0; }
    else if (p.pose === 'serve') { u.armR.rotation.x = -1.0 + (Math.sin(ph * .8) > .5 ? -.8 : 0); u.armL.rotation.x = -.4; }
    else { u.armR.rotation.x = Math.sin(ph * .7) * .15; }
  }
  return {
    get current() { return cur; }, OX, OZ,
    inside,
    enter(type) { if (cur) this.exit(); cur = build(type); return { x: OX, z: OZ + cur.D / 2 - .6 }; },
    exit() { if (!cur) return; scene.remove(cur.g); const shared = new Set(Object.values(G)); cur.g.traverse(o => { if (!o.isMesh) return; if (!shared.has(o.geometry)) o.geometry.dispose(); if (o.material.map) { o.material.map.dispose(); o.material.dispose(); } }); cur = null; },
    walkable(x, z) {
      if (!cur) return false; const lx = x - OX, lz = z - OZ;
      if (Math.abs(lx) > cur.W / 2 - .3 || lz < -cur.D / 2 + .3 || lz > cur.D / 2 + .5) return false;
      if (lz > cur.D / 2 - .1 && Math.abs(lx) > .55) return false;   // the front wall, except the doorway
      for (const [a, b, c, d] of cur.cols) if (lx > a - .2 && lx < c + .2 && lz > b - .2 && lz < d + .2) return false;
      for (const p of cur.people) if (Math.hypot(x - p.x, z - p.z) < .45) return false;
      return true;
    },
    surface() { return 0; },
    interactables(px, pz, exit, say) {
      if (!cur) return [];
      const L = [{ x: OX, z: OZ + cur.D / 2 - .2, label: 'Keluar dari ' + cur.R.title.toLowerCase(), act: exit, r: 1.3 }];
      for (const p of cur.people) L.push({ x: p.x, z: p.z, label: 'Sapa ' + p.label, act: () => say(p), r: 1.4 });
      return L;
    },
    update(dt, T) { if (cur) for (const p of cur.people) pose(p, T); },
  };
}
