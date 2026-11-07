// Things the residents do: fish at the shore, chop trees, build houses together, sit by the fire, stroll.
import * as THREE from 'three';
import * as WD from './world.js';
import { W, H, tile, treeAt, LM, village } from './world.js';
import { mat, box, G, presidentKit, vicePresidentKit, textTexture, BT } from './models.js';

// ---------- props ----------
function axe() { const g = new THREE.Group(); box(g, '#7a5432', .04, .5, .04, 0, -.95, .02); box(g, '#9aa3a8', .04, .14, .2, 0, -.97, .12); return g; }
function hammer() { const g = new THREE.Group(); box(g, '#7a5432', .035, .32, .035, 0, -.8, .02); box(g, '#6d7378', .08, .08, .16, 0, -.82, .06); return g; }
function rod() {
  const g = new THREE.Group();
  const pole = new THREE.Mesh(G.cyl6, mat('#8a6a3a')); pole.scale.set(.018, 2.1, .018); pole.position.set(0, 1.05, 0); g.add(pole);
  g.rotation.x = 1.15; g.position.set(.28, .95, .25);
  return g;
}
function plank() { const g = new THREE.Group(); box(g, '#b07a4a', .9, .06, .16, 0, -.62, .25); return g; }

export function constructionSite() {
  const g = new THREE.Group();
  box(g, '#8a6a4a', 2.6, .12, 2.6, 0, 0, 0);                                       // floor
  for (const [x, z] of [[-1.2, -1.2], [1.2, -1.2], [-1.2, 1.2], [1.2, 1.2]]) box(g, '#6b4a2b', .14, 1.9, .14, x, .1, z);
  for (let i = 0; i < 5; i++) box(g, i % 2 ? '#b07a4a' : '#9a6a3e', 2.5, .16, .08, 0, .25 + i * .2, -1.22);   // back wall half done
  for (let i = 0; i < 3; i++) box(g, i % 2 ? '#b07a4a' : '#9a6a3e', .08, .16, 2.5, -1.22, .25 + i * .2, 0);   // side wall started
  box(g, '#6b4a2b', 2.6, .1, .1, 0, 1.95, -1.2); box(g, '#6b4a2b', 2.6, .1, .1, 0, 1.95, 1.2);
  const r1 = box(g, '#6b4a2b', .08, 1.5, .08, -.7, 1.95, 0); r1.rotation.x = Math.PI / 2; r1.position.y = 2.2;
  for (let i = 0; i < 4; i++) box(g, '#b07a4a', 1.2, .06, .18, 1.9, .02 + i * .07, -.6 + (i % 2) * .05);    // plank pile
  for (let i = 0; i < 3; i++) { const l = new THREE.Mesh(G.cyl6, mat('#7a5432')); l.scale.set(.12, 1.1, .12); l.rotation.z = Math.PI / 2; l.position.set(1.9, .12 + (i === 2 ? .2 : 0), .5 + (i === 2 ? .12 : i * .24)); l.castShadow = true; g.add(l); }
  const lad = new THREE.Group(); lad.position.set(1.3, 0, 1.3); lad.rotation.z = -.25; g.add(lad);
  box(lad, '#8a6a3a', .05, 1.8, .05, -.18, 0, 0); box(lad, '#8a6a3a', .05, 1.8, .05, .18, 0, 0); for (let i = 0; i < 5; i++) box(lad, '#8a6a3a', .4, .04, .04, 0, .25 + i * .32, 0);
  return g;
}
function logSeat() { const l = new THREE.Mesh(G.cyl6, mat('#6b4a2b')); l.scale.set(.16, .9, .16); l.rotation.z = Math.PI / 2; l.castShadow = true; l.receiveShadow = true; return l; }

// ---------- spots ----------
const FIRE_SEATS = 7;
export function createActivities(ctx) {
  // ctx: { scene, solid(), occ(), npcWalkable, groundY, surfaceY, fireXZ, player }
  const deco = new THREE.Group(); ctx.scene.add(deco);
  let spots = { fish: [], chop: [], build: [], sit: [], sell: [], shop: [], listen: [], pres: [], vp: [], own: [] }, sites = [];
  const free = i => ctx.occ()[i] === -1 && !ctx.solid()[i];
  const spaced = (list, x, y, d) => list.every(s => Math.abs(s.cx - x) >= d || Math.abs(s.cy - y) >= d);

  function compute() {
    deco.clear(); spots = { fish: [], chop: [], build: [], sit: [], sell: [], shop: [], listen: [], pres: [], vp: [], own: [] }; sites = [];
    const ex = ctx.extraSpots ? ctx.extraSpots() : {}; for (const k of ['sell', 'shop', 'listen', 'pres', 'vp', 'own']) spots[k] = ex[k] || [];
    const cx0 = LM.camp[0], cy0 = LM.camp[1];
    const cells = [];
    for (let y = 2; y < H - 2; y++) for (let x = 2; x < W - 2; x++) { const d = Math.hypot(x - cx0, y - cy0); if (d < 34) cells.push({ x, y, d }); }
    cells.sort((a, b) => a.d - b.d);
    for (const c of cells) {
      const i = c.y * W + c.x, t = tile[i];
      if (t === WD.SAND && free(i) && spots.fish.length < 14) {
        for (const [dx, dy] of [[0, 1], [1, 0], [-1, 0], [0, -1]]) if (tile[(c.y + dy) * W + c.x + dx] === WD.SHALLOW && spaced(spots.fish, c.x, c.y, 3)) { spots.fish.push({ cx: c.x, cy: c.y, x: WD.cx2w(c.x) + dx * .3, z: WD.cy2w(c.y) + dy * .3, face: Math.atan2(dx, dy), water: [WD.cx2w(c.x) + dx * 2.6, WD.cy2w(c.y) + dy * 2.6] }); break; }
      }
      if (t >= WD.GRASS && free(i) && c.d > 6 && c.d < 26 && spots.chop.length < 14) {
        for (const [dx, dy] of [[0, 1], [1, 0], [-1, 0], [0, -1]]) { const j = (c.y + dy) * W + c.x + dx; if (treeAt[j] >= 0 && ctx.occ()[j] === -1 && spaced(spots.chop, c.x, c.y, 3)) { spots.chop.push({ cx: c.x, cy: c.y, x: WD.cx2w(c.x) + dx * .15, z: WD.cy2w(c.y) + dy * .15, face: Math.atan2(dx, dy), tree: j }); break; } }
      }
    }
    // two construction sites: planned spots first, otherwise open 3x3 grass a little away from the camp
    const planned = (ctx.plans ? ctx.plans() : []).filter(p => p && p.x != null);
    const want = planned.length ? planned.map(p => ({ x: p.x, y: p.y, d: 10 })) : [];
    for (const c of [...want, ...cells]) {
      if (sites.length >= 2) break;
      if (!want.includes(c) && (c.d < 9 || c.d > 20 || want.length)) continue;
      let ok = true;
      const pl = want.includes(c), R = pl ? 1 : 2; for (let dy = -R; dy <= R && ok; dy++) for (let dx = -R; dx <= R && ok; dx++) { const i = (c.y + dy) * W + c.x + dx; if (pl ? (tile[i] < WD.SAND || ctx.occ()[i] >= 0 || ctx.occ()[i] === -2) : (tile[i] < WD.GRASS || !free(i))) ok = false; }
      if (!ok || (!pl && sites.some(s => Math.hypot(s.cx - c.x, s.cy - c.y) < 10))) continue;
      const x = WD.cx2w(c.x), z = WD.cy2w(c.y), site = constructionSite();
      site.position.set(x, ctx.groundY(x, z), z); site.rotation.y = (sites.length ? 1 : 0) * Math.PI / 2; deco.add(site);
      // a planned building gets a signboard ("SEGERA DIBANGUN · SEKOLAH")
      const plan = (ctx.plans ? ctx.plans() : [])[sites.length];
      if (plan && BT[plan.type] && plan.type !== 'rumah') {
        const sg = new THREE.Group(); sg.position.set(x + 1.7, ctx.groundY(x + 1.7, z + 1.7), z + 1.7); sg.rotation.y = .5; deco.add(sg);
        for (const px of [-.55, .55]) box(sg, '#5e3b22', .07, 1.5, .07, px, 0, 0);
        const bd = new THREE.Mesh(new THREE.PlaneGeometry(1.4, .75), new THREE.MeshStandardMaterial({ map: textTexture(['SEGERA DIBANGUN', BT[plan.type].n.toUpperCase()], { w: 512, h: 274, bg: '#f4ead2', color: '#1f4f3a', size: 58 }), roughness: .9, side: THREE.DoubleSide }));
        bd.position.y = 1.2; bd.castShadow = true; sg.add(bd);
        sg.userData.plan = plan.type;
      }
      site.userData.plan = plan && plan.type;
      sites.push({ cx: c.x, cy: c.y });
      for (const [dx, dz] of [[0, 2.1], [2.1, 0], [-2.1, 0], [0, -2.1]]) spots.build.push({ x: x + dx, z: z + dz, face: Math.atan2(-dx, -dz), cx: c.x, cy: c.y });
    }
    // seats around the camp fire, leaving the shelter side open
    const [fx, fz] = ctx.fireXZ;
    for (let k = 0; k < FIRE_SEATS; k++) {
      const a = Math.PI * .15 + k / (FIRE_SEATS - 1) * Math.PI * .7; // southern arc
      const x = fx + Math.cos(a) * 2.3, z = fz + Math.sin(a) * 2.3;
      spots.sit.push({ x, z, face: Math.atan2(fx - x, fz - z) });
      const seat = logSeat(); seat.position.set(fx + Math.cos(a) * 2.55, ctx.groundY(x, z) + .12, fz + Math.sin(a) * 2.55); seat.rotation.y = -a; deco.add(seat);
    }
    return sites;
  }
  const siteCells = () => sites.flatMap(s => { const out = []; for (let dy = -1; dy <= 1; dy++) for (let dx = -1; dx <= 1; dx++) out.push((s.cy + dy) * W + s.cx + dx); return out; });

  // ---------- roles ----------
  const ROLE_ORDER = ['fish', 'chop', 'build', 'sit', 'chop', 'fish', 'build', 'wander', 'sit', 'build', 'wander', 'fish'];
  function assign(npcs) {
    const used = { fish: 0, chop: 0, build: 0, sit: 0, sell: 0, shop: 0, listen: 0 };
    let k = 0;
    npcs.forEach((n, i) => {
      if (n.aru) { setRole(n, 'sit', spots.sit[used.sit++] || null); return; }
      if (n.pres) { setRole(n, 'president', spots.pres[0] || null); return; }
      if (n.vp) { setRole(n, 'vicepresident', spots.vp[0] || null); return; }
      if (n.own) { const sp = spots.own.find(s => s.n === n.own); if (sp) { setRole(n, 'sell', sp); n.workFor = Infinity; return; } }
      // market sellers and the crowd at the stage come first, then the usual jobs
      for (const r of ['sell', 'listen', 'shop']) if (used[r] < spots[r].length) { setRole(n, r, spots[r][used[r]++]); return; }
      let want = ROLE_ORDER[k++ % ROLE_ORDER.length];
      if (want !== 'wander' && used[want] >= spots[want].length) want = 'wander';
      setRole(n, want, want === 'wander' ? null : spots[want][used[want]++]);
    });
  }
  function setRole(n, role, spot) {
    if (n.role === role && n.spot === spot) return;
    if (n.kit) { n.obj.userData.body.remove(...n.kit); n.kit = null; }
    if (n.tool) { n.tool.parent && n.tool.parent.remove(n.tool); n.tool = null; }
    if (n.line) { n.obj.remove(n.line); n.line = null; }
    if (n.bob) { ctx.scene.remove(n.bob); n.bob = null; }
    n.role = spot || role === 'wander' ? role : 'wander'; n.spot = spot;
    n.state = spot ? 'work' : 'stroll'; n.t = Math.random() * 20; n.workFor = 35 + Math.random() * 50;
    if (n.role === 'president' || n.role === 'vicepresident') n.workFor = Infinity;
    if (n.role === 'listen') n.workFor = 60 + Math.random() * 90;
    if (n.role === 'shop') { n.workFor = 4 + Math.random() * 6; n.t = 0; }
    n.yOff = spot && spot.y || 0;
    if (n.role === 'president') { const before = n.obj.userData.body.children.length; presidentKit(n.obj); n.kit = n.obj.userData.body.children.slice(before); }
    if (n.role === 'vicepresident') { const before = n.obj.userData.body.children.length; vicePresidentKit(n.obj); n.kit = n.obj.userData.body.children.slice(before); }
    if (spot) { n.x = spot.x; n.z = spot.z; n.obj.rotation.y = spot.face; n.tx = null; }
    const u = n.obj.userData;
    if (n.role === 'chop') { n.tool = axe(); u.armR.add(n.tool); }
    if (n.role === 'build') { n.carry = Math.random() < .35; n.tool = n.carry ? plank() : hammer(); u.armR.add(n.tool); }
    if (n.role === 'fish') {
      n.tool = rod(); n.obj.add(n.tool);
      const lg = new THREE.BufferGeometry().setAttribute('position', new THREE.BufferAttribute(new Float32Array(6), 3));
      n.line = new THREE.Line(lg, new THREE.LineBasicMaterial({ color: '#f0f0f0', transparent: true, opacity: .7 })); n.obj.add(n.line);
      n.bob = new THREE.Mesh(G.sph, mat('#e8463a')); n.bob.scale.setScalar(.06); ctx.scene.add(n.bob);
    }
  }

  // ---------- per frame ----------
  const tip = new THREE.Vector3();
  function walkTo(n, tx, tz, dt, speed = 1.5) {
    const dx = tx - n.x, dz = tz - n.z, d = Math.hypot(dx, dz);
    if (d < .12) { n.moving = false; return true; }
    const sp = Math.min(d, speed * dt), vx = dx / d * sp, vz = dz / d * sp;
    const ox = n.x, oz = n.z;
    if (ctx.npcWalkable(n.x + vx, n.z)) n.x += vx; if (ctx.npcWalkable(n.x, n.z + vz)) n.z += vz;
    const prog = Math.hypot(n.x - ox, n.z - oz);
    n.moving = prog > sp * .25;
    if (n.moving) n.obj.rotation.y = Math.atan2(n.x - ox, n.z - oz);
    // stuck detection: no real progress for 2.5 s
    n.stuck = n.moving ? 0 : (n.stuck || 0) + dt;
    if (n.stuck > 2.5) {
      n.stuck = 0;
      const far = Math.hypot(n.x - ctx.player.x, n.z - ctx.player.z) > 14;
      if (far || n.state === 'return') { n.x = tx; n.z = tz; return true; } // unseen, or heading home: hop there
      n.tx = null; return true;
    }
    return false;
  }
  function strollTarget(n) {
    const hx = n.spot ? WD.w2cx(n.spot.x) : n.hx, hy = n.spot ? WD.w2cy(n.spot.z) : n.hy, R = n.aru ? 3 : n.spot ? 4 : 8;
    for (let k = 0; k < 8; k++) {
      const tx = hx + Math.round((Math.random() * 2 - 1) * R), ty = hy + Math.round((Math.random() * 2 - 1) * R);
      if (tx > 0 && ty > 0 && tx < W && ty < H && tile[ty * W + tx] >= WD.SAND && ctx.npcWalkable(WD.cx2w(tx), WD.cy2w(ty))) { n.tx = WD.cx2w(tx); n.tz = WD.cy2w(ty); return; }
    }
    n.tx = null;
  }
  function update(n, dt, T) {
    const u = n.obj.userData; n.t += dt;
    if (n.state === 'work') {
      if (n.t > n.workFor) {
        if (n.role === 'shop' && spots.shop.length) { n.spot = spots.shop[(Math.random() * spots.shop.length) | 0]; n.state = 'return'; n.t = 0; }
        else { n.state = 'break'; n.t = 0; n.breakFor = 6 + Math.random() * 8; strollTarget(n); }
      }
      n.moving = false; n.obj.rotation.y = n.spot.face;
      animateWork(n, u, T, dt);
      return;
    }
    // walking states reset the work pose
    u.body.position.y = 0;
    if (n.state === 'break' || n.state === 'stroll') {
      if (n.wait > 0) { n.wait -= dt; n.moving = false; walkPose(u, false, dt); return; }
      if (n.tx == null) strollTarget(n);
      if (n.tx == null || walkTo(n, n.tx, n.tz, dt)) { n.tx = null; n.wait = 1 + Math.random() * 3; }
      if (n.state === 'break' && n.t > n.breakFor) { n.state = 'return'; n.t = 0; }
    } else if (n.state === 'return') {
      if (walkTo(n, n.spot.x, n.spot.z, dt)) { n.state = 'work'; n.t = 0; n.workFor = n.role === 'shop' ? 4 + Math.random() * 6 : n.role === 'listen' ? 60 + Math.random() * 90 : 35 + Math.random() * 50; }
    }
    walkPose(u, n.moving, dt);
    if (n.tool && n.role !== 'fish') n.tool.visible = true;
  }
  function walkPose(u, moving, dt) {
    if (moving) u.phase += dt * 11; else u.phase *= .9;
    const s = moving ? Math.sin(u.phase) * .7 : 0;
    u.legL.rotation.x = s; u.legR.rotation.x = -s; u.armL.rotation.x = -s * .8; u.armR.rotation.x = s * .8;
    u.body.position.y = moving ? Math.abs(Math.cos(u.phase)) * .05 : 0;
  }
  function animateWork(n, u, T, dt) {
    const ph = T + (n.seed || (n.seed = Math.random() * 10));
    u.legL.rotation.x = 0; u.legR.rotation.x = 0; u.body.position.y = 0; u.body.rotation.x = 0;
    if (n.role === 'chop') {
      const c = (ph % 1.3) / 1.3, swing = c < .7 ? -2.7 + c / .7 * .6 : -2.1 + (c - .7) / .3 * 1.6;
      u.armR.rotation.x = swing; u.armL.rotation.x = swing * .9; u.body.rotation.x = c > .7 ? .12 : 0;
    } else if (n.role === 'build') {
      if (n.carry) { u.armR.rotation.x = -1.1; u.armL.rotation.x = -1.1; u.body.position.y = Math.abs(Math.sin(ph * 2)) * .02; }
      else { const c = (ph * 2.6) % 1; u.armR.rotation.x = -1.7 + Math.abs(Math.sin(c * Math.PI)) * 1.1; u.armL.rotation.x = -.4; u.body.rotation.x = .25; u.body.position.y = -.08; }
    } else if (n.role === 'sit') {
      u.body.position.y = -.42; u.legL.rotation.x = -1.45; u.legR.rotation.x = -1.4; u.armL.rotation.x = -.5; u.armR.rotation.x = -.5 + Math.sin(ph * 1.7) * .12;
      if (Math.sin(ph * .7) > .6) u.armR.rotation.x = -1.1 + Math.sin(ph * 6) * .3; // talking with hands
    } else if (n.role === 'sell') {
      // calling out to buyers, now and then holding up the goods
      const c = (ph % 5) / 5;
      u.armR.rotation.x = c < .35 ? -1.6 + Math.sin(ph * 9) * .35 : -.4; u.armL.rotation.x = c < .35 ? -.3 : -1.0;
      u.body.position.y = Math.abs(Math.sin(ph * 2.2)) * .02;
    } else if (n.role === 'shop') {
      u.armL.rotation.x = -.9; u.armR.rotation.x = -.5 + Math.sin(ph * 2) * .25; u.body.rotation.x = .12;
    } else if (n.role === 'listen') {
      // the whole crowd cheers together every 12 s
      const c = (T % 12) / 12, cheer = window.__cheer != null ? window.__cheer : c > .82;
      u.armR.rotation.x = cheer ? -2.9 + Math.sin(T * 14 + n.seed) * .25 : -.15; u.armL.rotation.x = cheer && n.seed > 5 ? -2.9 : -.15;
      u.body.position.y = cheer ? Math.abs(Math.sin(T * 8 + n.seed)) * .22 : 0;
    } else if (n.role === 'president') {
      const c = (T % 12) / 12, cheer = window.__cheer != null ? window.__cheer : c > .82;
      u.armR.rotation.x = cheer ? -3.0 : -1.4 + Math.sin(T * 3.1) * .5; u.armR.rotation.z = cheer ? 0 : -.2;
      u.armL.rotation.x = -.6 + Math.sin(T * 1.7) * .15; u.body.rotation.y = Math.sin(T * .7) * .25;
    } else if (n.role === 'vicepresident') {
      // thumbs up for the crowd, clapping along when they cheer
      const c = (T % 12) / 12, cheer = window.__cheer != null ? window.__cheer : c > .82, talk = window.__vpTalk;
      if (cheer) { const k = Math.sin(T * 16) * .25; u.armR.rotation.x = -1.35 + k; u.armL.rotation.x = -1.35 - k; u.armR.rotation.z = .35; u.armL.rotation.z = -.35; }
      else if (talk) { u.armR.rotation.x = -2.2 + Math.sin(T * 7) * .45; u.armL.rotation.x = -1.2 + Math.sin(T * 5) * .3; u.armR.rotation.z = 0; u.armL.rotation.z = 0; u.body.position.y = Math.abs(Math.sin(T * 6)) * .05; }
      else { u.armR.rotation.x = -1.55; u.armR.rotation.z = -.1; u.armL.rotation.x = -.2; u.armL.rotation.z = 0; }
      u.body.rotation.y = Math.sin(T * .9 + 1) * .3;
    } else if (n.role === 'fish') {
      const c = (ph % 14) / 14; // a cast every 14 s, a tug now and then
      u.armR.rotation.x = c < .06 ? -2.4 + c / .06 * 1.4 : -1.0 + Math.sin(ph * 1.3) * .04; u.armL.rotation.x = -.9;
      const tug = Math.sin(ph * .9) > .985;
      if (tug) u.armR.rotation.x -= .4;
      n.tool.rotation.x = 1.15 + (u.armR.rotation.x + 1) * .3;
      n.tool.updateMatrixWorld(); tip.set(0, 2.1, 0).applyMatrix4(n.tool.matrixWorld);
      const [wx, wz] = n.spot.water; const by = Math.sin(ph * 2) * .02 - (tug ? .12 : 0);
      n.bob.position.set(wx, by, wz);
      const p = n.line.geometry.attributes.position, inv = n.obj.worldToLocal.bind(n.obj);
      const a = inv(tip.clone()), b = inv(n.bob.position.clone()); p.setXYZ(0, a.x, a.y, a.z); p.setXYZ(1, b.x, b.y, b.z); p.needsUpdate = true;
    }
  }
  return { compute, assign, update, siteCells, get spots() { return spots; } };
}

export const ROLE_LINES = {
  president: ['Janji saya: jadi pemimpin yang baik, minn!', 'Mundur dari wapres, nyalon presiden, menang. Namanya strategi!', 'Kali ini dipilih warga, bukan cuma follow duluan.', 'Permintaan presiden? Tunggu komentar kalian.'],
  vicepresident: ['Saya wakil presiden. Ditunjuk langsung di kolom komentar!', 'Pak Presiden janji jadi pemimpin yang baik. Saya yang catat.', 'Sudah ngopi di Kopi Dong? Enak, lho.'],
  kopdes: ['Antre dulu ya, mau setor ikan ke Kopdes.', 'Capek naiknya, tapi pemandangannya juara.', 'Jangan lihat ke bawah. Pokoknya jangan.'],
  climb: ['Lompat… lompat… jangan lihat ke bawah!', 'Awan ini empuk, tapi licin.', 'Tadi aku jatuh dua kali. Coba lagi!'],
  sell: ['Ikan segar, ikan segar! Baru ditangkap perahu nelayan!', 'Mangga manis, murah meriah!', 'Mampir dulu, kak. Lihat-lihat boleh.'],
  shop: ['Lagi cari bahan masak buat nanti malam.', 'Pasarnya rame banget, ya.', 'Kata presiden, belanja di pasar sendiri itu keren.'],
  listen: ['Hidup Pak Presiden!', 'Pidatonya seru. Aku nunggu bagian pembagian kelapa.', 'Aru belum tahu kita punya presiden, hehe.'],
  fish: ['Sstt, jangan berisik. Ikannya hampir makan umpan.', 'Udah dua jam belum dapat. Tapi pemandangannya bagus, kan?', 'Kata Aru, ikan emas berkilau itu beneran ada.'],
  chop: ['Kayu ini buat rumah warga baru. Kita butuh banyak!', 'Hati-hati, pohonnya mau rubuh! …Belum deng.', 'Capek juga ya, tapi seru.'],
  build: ['Kurang dikit lagi atapnya jadi!', 'Siapa yang ambil palu aku?', 'Rumah ini nanti buat siapa ya? Mungkin buat kamu.'],
  sit: ['Duduk sini, apinya hangat.', 'Kamu dengar cerita soal peti di pulau seberang?', 'Aru tadi meleset nombak ikan lagi, hahaha.'],
  wander: ['Aku lagi jalan-jalan keliling pulau.', 'Pulau ini makin ramai aja tiap hari.'],
};
