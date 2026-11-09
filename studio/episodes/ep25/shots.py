"""Episode 25 "7 Hari Lalu Aru Sendirian" shot list (episode KONSEP).  usage: DPR=2 python3 shots.py c1,c3,...  (DPR=1 + prev for checks)
The last old Kotak Usulan suggestion (hotel) is built by the pier; Klub Pertama queues to check in, the president books
the top floor, Bu Guru Gina asks for his homework, and the guest book lists room 3: Penjaga Mercusuar.
"""
import asyncio, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'lib'))
from harness import *
BASE = """async () => { const P = window.__pulau; window.PI = Math.PI;
  window.__look = (x, z, yaw, pitch, dist, show) => { const pl = P.player; pl.x = x; pl.z = z; pl.tx = null; pl.vy = 0; pl.obj.visible = !!show; P.cam.yaw = yaw; P.cam.pitch = pitch; P.cam.dist = dist; P.cam.target.set(x, 1, z); };
  window.__W = () => { const d = P.npcs.filter(n => n.demo), a = P.npcs.filter(n => !n.demo && n.role === 'wander' && n.num), b = P.npcs.filter(n => !d.includes(n) && !a.includes(n) && !n.aru && !n.pres && !n.vp && !n.cloud && !n.kit && !n.tool); return d.concat(a.filter(n => !n.kit && !n.tool), b); };
  window.__cand = on => { for (const n of P.npcs) if (n.candSign) n.candSign.visible = on; };
  window.__VP = () => P.npcs.find(n => n.vp); window.__PR = () => P.npcs.find(n => n.pres);
  const scene = P.roads.parent; let wp = null; scene.traverse(o => { if (o.userData && o.userData.b && o.userData.b.type === 'waterpark') wp = o; });
  window.__wpL = (lx, ly, lz) => [wp.position.x + lx, wp.position.y + ly, wp.position.z + lz];
  window.__bld = type => { let r = null; P.roads.parent.traverse(o => { if (!r && o.userData && o.userData.b && o.userData.b.type === type) r = o; }); return r; };
  window.__seatW = (type, lx, ly, lz) => { const o = window.__bld(type), s = o.userData.def.scale || 1; o.updateMatrixWorld(true); const v = o.localToWorld(new (P.cam.target.constructor)(lx * s, ly * s, lz * s)); return [v.x, v.y, v.z]; };
  window.__signs = [];
  window.__placard = async (n, text, col) => { const THREE = await import('three'); const c = document.createElement('canvas'); c.width = 256; c.height = 160; const x = c.getContext('2d');
    x.fillStyle = col || '#fff8e6'; x.fillRect(0, 0, 256, 160); x.strokeStyle = '#3a2412'; x.lineWidth = 8; x.strokeRect(4, 4, 248, 152);
    x.fillStyle = '#c0392b'; x.textAlign = 'center'; x.textBaseline = 'middle'; const w = text.split('|'); let fs = 52; x.font = `700 ${fs}px "Pixelify Sans", sans-serif`;
    while (fs > 22 && Math.max(...w.map(t => x.measureText(t).width)) > 236) { fs -= 2; x.font = `700 ${fs}px "Pixelify Sans", sans-serif`; }
    w.forEach((t, i) => x.fillText(t, 128, 80 + (i - (w.length - 1) / 2) * fs * 1.1));
    const tx = new THREE.CanvasTexture(c); tx.colorSpace = THREE.SRGBColorSpace; const g = new THREE.Group();
    const board = new THREE.Mesh(new THREE.PlaneGeometry(.62, .39), new THREE.MeshStandardMaterial({ map: tx, side: THREE.DoubleSide })); board.position.set(0, 2.05, .12); g.add(board);
    const stick = new THREE.Mesh(new THREE.BoxGeometry(.03, .9, .03), new THREE.MeshStandardMaterial({ color: '#8a6a3a' })); stick.position.set(0, 1.5, .1); g.add(stick);
    n.obj.add(g); window.__signs.push(g); return g; };
  window.__clearSigns = () => { for (const g of window.__signs) if (g.parent) g.parent.remove(g); window.__signs = []; };
  let _br = null; Object.defineProperty(window, '__beforeRender', { configurable: true, get() { return _br; }, set(f) { if (!f) { _br = null; return; } let s0 = null; _br = (dt, T) => { if (s0 === null) s0 = T; return f(dt, T - s0 - .4); }; } });
  window.__time = want => { const lab = document.getElementById('time-label'), btn = document.getElementById('b-time'); for (let i = 0; i < 4 && !lab.textContent.includes(want); i++) btn.click(); };
  window.__poseY = (n, x, y, z, face, pose, T) => { n.x = x; n.z = z; n.tx = null; n.wait = 99; n.obj.visible = true; n.obj.position.set(x, y, z); n.obj.rotation.y = face; const u = n.obj.userData;
    u.legL.rotation.x = u.legR.rotation.x = 0; u.armL.rotation.x = u.armR.rotation.x = -.15; u.body.position.y = 0; u.body.rotation.z = 0;
    if (pose === 'eat') { u.armR.rotation.x = -1.3 + Math.sin(T * 8) * .45; u.armL.rotation.x = -.8; }
    if (pose === 'reach') { u.armR.rotation.x = -1.2 + Math.sin(T * 3) * .15; u.armL.rotation.x = -.2; u.body.rotation.z = Math.sin(T * 2.5) * .06; }
    if (pose === 'talk') { u.armR.rotation.x = -1.1 + Math.sin(T * 7) * .4; u.armL.rotation.x = -.6 + Math.sin(T * 5) * .2; }
    if (pose === 'point') { u.armR.rotation.x = -1.55 + Math.sin(T * 10) * .08; u.armL.rotation.x = -.3; }
    if (pose === 'panic') { u.armR.rotation.x = -2.2 + Math.sin(T * 14) * .5; u.armL.rotation.x = -2.2 - Math.sin(T * 14) * .5; u.body.position.y = Math.abs(Math.sin(T * 9)) * .05; }
    if (pose === 'wave') { u.armR.rotation.x = -2.6 + Math.sin(T * 9) * .35; u.armL.rotation.x = -.3; }
    if (pose === 'cheer') { u.armR.rotation.x = u.armL.rotation.x = -2.8 + Math.sin(T * 10) * .2; u.body.position.y = Math.abs(Math.sin(T * 6)) * .08; }
    if (pose === 'swim') { u.armR.rotation.x = -1.6 + Math.sin(T * 6) * .5; u.armL.rotation.x = -1.6 - Math.sin(T * 6) * .5; }
    if (pose === 'sit' || pose === 'sittalk' || pose === 'yawn' || pose === 'sleep' || pose === 'sipcup') { u.legL.rotation.x = u.legR.rotation.x = -1.45; }
    if (pose === 'sittalk') { u.armR.rotation.x = -1.1 + Math.sin(T * 7) * .4; u.armL.rotation.x = -.6 + Math.sin(T * 5) * .2; }
    if (pose === 'yawn') { u.armR.rotation.x = u.armL.rotation.x = -2.9 + Math.sin(T * 2) * .1; u.body.rotation.z = Math.sin(T * 1.5) * .08; }
    if (pose === 'sleep') { u.armR.rotation.x = u.armL.rotation.x = -.1; u.body.rotation.z = .32 + Math.sin(T * 1.6) * .03; u.body.position.y = Math.sin(T * 1.6) * .015; }
    if (pose === 'sipcup') { u.armR.rotation.x = -1.6 + Math.sin(T * 1.2) * .25; u.armL.rotation.x = -.9; }
    if (pose === 'strike') { u.armR.rotation.x = -1.7 + Math.abs(Math.sin(T * 9)) * .9; u.armL.rotation.x = -.4; }
    if (pose === 'sitcup' || pose === 'eatsit' || pose === 'type') { u.legL.rotation.x = u.legR.rotation.x = -1.45; }
    if (pose === 'sitcup') { u.armR.rotation.x = -1.6 + Math.sin(T * 1.2) * .25; u.armL.rotation.x = -.9; }
    if (pose === 'eatsit') { u.armR.rotation.x = -1.3 + Math.sin(T * 8) * .45; u.armL.rotation.x = -.8; }
    if (pose === 'type') { u.armR.rotation.x = -1.2 + Math.sin(T * 14) * .12; u.armL.rotation.x = -1.2 - Math.sin(T * 13) * .12; }
    if (pose === 'walk') { u.legL.rotation.x = Math.sin(T * 7) * .5; u.legR.rotation.x = -Math.sin(T * 7) * .5; u.armL.rotation.x = -Math.sin(T * 7) * .4; u.armR.rotation.x = Math.sin(T * 7) * .4; } };
  window.__pose = (n, x, z, face, pose, T, dy = 0) => window.__poseY(n, x, P.WD.groundY(x, z) + dy, z, face, pose, T);
  window.__unkit = n => { if (n && n.kit) { n.obj.userData.body.remove(...n.kit); n.kit = null; } if (n && n.candSign) n.candSign.visible = false; };
  window.__hideNear = (x, z, r, keep) => { for (const n of P.npcs) if (!keep.includes(n)) n.obj.visible = Math.hypot(n.x - x, n.z - z) > r; };
}"""
V = "new window.__pulau.cam.target.constructor"
G = "window.__pulau.WD.groundY"
CROWD = """const W = window.__W(); const spots = [[-2.3, -6.3], [-1.4, -6.5], [-.5, -6.3], [.4, -6.5], [-1.9, -5.5], [-1.0, -5.6], [-.1, -5.5], [.8, -5.4]];
  window.__crowd = (T, pose) => { for (let i = 0; i < 8; i++) { const [x, z] = spots[i]; window.__pose(W[i], x, z, Math.PI + (i % 3 - 1) * .15, pose(i), T + i * .6); } };"""
NPC = """window.__N = s => window.__pulau.npcs.find(n => n.name === s);"""


NPC = """window.__N = s => window.__pulau.npcs.find(n => n.name === s);
  window.__fix = n => { n.state = 'work'; n.t = 0; n.workFor = 999; n.x = n.spot.x; n.z = n.spot.z; n.tx = null; };
  window.__on = (name, off, pitch, dist, h, push, minD, sway) => { const P = window.__pulau, n = window.__N(name); window.__fix(n); window.__time('siang'); window.__cheer = null; P.player.obj.visible = false;
    const f = n.spot.face + off; window.__look(n.x, n.z, f, pitch, dist, false); P.cam.yaw = f;
    window.__beforeRender = (dt, T) => { window.__hideNear(n.x, n.z, 1.4, [n]); window.__camTarget = new P.cam.target.constructor(n.x, n.obj.position.y + h, n.z); P.cam.dist = Math.max(minD, P.cam.dist - dt * push); P.cam.yaw = f + Math.sin(T * .5) * (sway || 0); };
    return n; };
  window.__on2 = (name, off, pitch, dist, h, push, minD, sway, R, keep) => { const n = window.__on(name, off, pitch, dist, h, push, minD, sway), P = window.__pulau;
    const K = [n, window.__PR(), window.__VP()].concat((keep || []).map(window.__N)); for (const k of K) if (k && k.castSpot) window.__fix(k);
    const prev = window.__beforeRender; window.__beforeRender = (dt, T) => { prev(dt, T); for (const m of P.npcs) m.obj.visible = K.includes(m) || Math.hypot(m.x - n.x, m.z - n.z) > R; };
    return n; };"""
def ON(name, off=0, pitch=.18, dist=3.0, h=1.0, push=.15, minD=2.0, sway=0, extra=''):
    return f"() => {{ const n = window.__on({name!r}, {off}, {pitch}, {dist}, {h}, {push}, {minD}, {sway}); {extra} }}"
def ON(name, off=0, pitch=.18, dist=3.0, h=1.0, push=.15, minD=2.0, sway=0, extra=''):
    return f"() => {{ const n = window.__on({name!r}, {off}, {pitch}, {dist}, {h}, {push}, {minD}, {sway}); {extra} }}"
def ON2(name, off=0, pitch=.18, dist=3.0, h=1.0, push=.15, minD=2.0, sway=0, R=3.5, keep=(), extra=''):
    return f"() => {{ const n = window.__on2({name!r}, {off}, {pitch}, {dist}, {h}, {push}, {minD}, {sway}, {R}, {list(keep)!r}); {extra} }}"
AFTER = "const prev = window.__beforeRender; window.__beforeRender = (dt, T) => { prev(dt, T); %s };"
EXTRA = """  window.__hid = []; window.__hideInst = (pts, r) => { const P = window.__pulau, sc = P.roads.parent; sc.traverse(o => { if (!o.isInstancedMesh) return; const m = new (o.matrix.constructor)(), v = new (P.cam.target.constructor)();
    for (let i = 0; i < o.count; i++) { o.getMatrixAt(i, m); v.setFromMatrixPosition(m); const c = o.material && o.material.color ? o.material.color.getHexString() : ''; if (c === '5a9e44') continue;
      if (pts.some(([x, z]) => Math.hypot(v.x - x, v.z - z) < r)) { window.__hid.push([o, i, m.clone()]); const z0 = m.clone().scale(new (P.cam.target.constructor)(0, 0, 0)); o.setMatrixAt(i, z0); o.instanceMatrix.needsUpdate = true; } } }); };
  window.__showInst = () => { for (const [o, i, m] of window.__hid) { o.setMatrixAt(i, m); o.instanceMatrix.needsUpdate = true; } window.__hid = []; };
  window.__apt = () => { const o = window.__bld('apartemen'); return [o.position.x, o.position.z]; };
  window.__tgt = (x, z, h) => { const P = window.__pulau; window.__camTarget = new P.cam.target.constructor(x, P.WD.groundY(x, z) + h, z); };
  window.__z0 = n => { const u = n.obj.userData; u.armL.rotation.z = u.armR.rotation.z = 0; u.body.rotation.x = 0; u.body.rotation.y = 0; u.body.position.y = 0; };
  window.__guardP = (n, x, z, face, T, stop) => { window.__pose(n, x, z, face, 'still', T); const u = n.obj.userData; if (stop) { u.armR.rotation.x = -1.6; u.armR.rotation.z = 0; u.armL.rotation.x = -.55; u.armL.rotation.z = .55; } else { u.armL.rotation.x = u.armR.rotation.x = -.55; u.armL.rotation.z = .55; u.armR.rotation.z = -.55; } };
  window.__keep = (K, x, z, R) => { for (const m of window.__pulau.npcs) if (!K.includes(m)) m.obj.visible = Math.hypot(m.x - x, m.z - z) > R; };
  window.__aru = (x, z, face, talk, T) => { const P = window.__pulau, pl = P.player; pl.obj.visible = true; pl.x = x; pl.z = z; pl.tx = null; pl.obj.position.set(x, P.WD.groundY(x, z), z); pl.obj.rotation.y = face; const u = pl.obj.userData; if (u.armR) { u.armR.rotation.x = talk ? -1.1 + Math.sin(T * 7) * .4 : 0; u.armL.rotation.x = talk ? -.6 + Math.sin(T * 5) * .2 : 0; } };"""
GUARD, DEB, GINA = 'Cawetssssss', '🌸 Debby_l0vata👻', 'Bu Guru Gina'
TOUR = """window.__T = () => window.__pulau.npcs.filter(n => n.tour).sort((a, b) => a.tour.i - b.tour.i);
  window.__TN = i => window.__T().find(n => n.tour.i === i);
  window.__stage = () => { const P = window.__pulau, pr = window.__PR(); return pr.obj.position.y; };"""
GUARD, GINA, DABY, PRIN, KOPI = 'Cawetssssss', 'Bu Guru Gina', 'D..A..B..Y a..j..a', 'princes_nay', '@sapta.rajo.ghaisa'
FIRE = """window.__ring = (cx, cz, r, T, n0, cnt, pose) => { const W = window.__W(); for (let i = 0; i < cnt; i++) { const a = i / cnt * Math.PI * 2 + .4, x = cx + Math.sin(a) * r, z = cz + Math.cos(a) * r;
    window.__pose(W[n0 + i], x, z, a + Math.PI, pose(i), T + i * .7); } };"""
# c1 cold open: senja, Aru alone on the beach by the Batu Nama, close-up, nobody else on the island
C1 = """() => { const P = window.__pulau; window.__clock = .575; window.__cheer = null; const x = -.9, z = 43.6; window.__look(x, z, PI + .25, .1, 2.7, false);
  window.__beforeRender = (dt, T) => { window.__keep([], x, z, 60); window.__aru(x, z, PI + .25 + Math.sin(T * .7) * .08, T > 3.3, T); const sy = P.surfaceY(x, z); P.player.obj.position.y = sy; window.__camTarget = new P.cam.target.constructor(x, sy + 1.32, z); P.cam.dist = Math.max(2.3, 2.7 - T * .08); P.cam.yaw = PI + .25 - T * .02; }; }"""
# c2 the Batu Nama full of names (camera glides along it), the new 'PULAU ARU: 7 HARI' sign behind
C2 = """() => { const P = window.__pulau; window.__clock = .5; window.__cheer = null; const x = -5.0, z = 37.6; window.__look(x, z, -.35, .22, 4.2, false);
  window.__beforeRender = (dt, T) => { window.__tgt(x, z, .9); P.cam.dist = Math.max(3.0, 4.2 - T * .25); P.cam.yaw = -.35 + T * .1; }; }"""
# c3 fast aerial swoop over the town: 'setiap komentar kalian jadi kenyataan'
C3 = """() => { const P = window.__pulau; window.__clock = .3; window.__cheer = null; P.player.obj.visible = false; window.__look(2, 6, .3, 1.05, 62, false);
  window.__beforeRender = (dt, T) => { window.__tgt(2, 6, 0); P.cam.dist = Math.max(30, 62 - T * 11); P.cam.yaw = .3 + T * .12; P.cam.pitch = Math.max(.75, 1.05 - T * .08); }; }"""
def BLD(t, yaw, pitch, dist, h, push=.6, dyaw=.05, dh=0, minD=3):
    return """() => { const P = window.__pulau, o = window.__bld('%s'); window.__clock = .3; window.__cheer = null; P.player.obj.visible = false; const x = o.position.x, z = o.position.z; window.__look(x, z, %s, %s, %s, false);
  window.__beforeRender = (dt, T) => { window.__tgt(x, z, %s + T * %s); P.cam.dist = Math.max(%s, %s - T * %s); P.cam.yaw = %s + T * %s; }; }""" % (t, yaw, pitch, dist, h, dh, minD, dist, push, yaw, dyaw)
C4 = BLD('warteg', 'PI + .35', .3, 9, 1.4, push=.9)
C5 = BLD('waterpark', .45, .55, 15, 1.5, push=1.2)
C6 = BLD('menarasinyal', 'PI - .3', .12, 13, 2.0, push=.5, dh=1.6, minD=8)
# c7 the KOPI DONG cart, its seller waving (ep16 C8)
C7 = """() => { const P = window.__pulau, s = window.__N('%s'); window.__clock = .3; window.__cheer = null; P.player.obj.visible = false;
  const o = window.__bld('gerobakkopi'), x = o.position.x, z = o.position.z; window.__look(x, z, .05, .3, 3.0, false); window.__tgt(x, z, 1.2);
  window.__beforeRender = (dt, T) => { window.__hideNear(x, z, 3, [s]); window.__pose(s, x, z - .72, 0, T < 1.2 ? 'wave' : 'talk', T); window.__tgt(x, z, 1.2); P.cam.dist = Math.max(2.6, 3.0 - T * .12); }; }""" % KOPI
# c8 the president chosen by likes on the stage, crowd cheering (ep16 C1)
C8 = """() => { const P = window.__pulau, pr = window.__PR(), vp = window.__VP(); window.__clock = .3; window.__cheer = true; P.player.obj.visible = false;
  const st = window.__bld('mimbar'), sy = st.position.y + .55; const x = -2.35, z = -10.0;
  window.__look(x, z, .05, .34, 4.0, false); window.__camTarget = new P.cam.target.constructor(x + .3, sy + 1.45, z);
  window.__beforeRender = (dt, T) => { window.__poseY(pr, x, sy, z, .1, T < 1.0 ? 'talk' : 'cheer', T); window.__poseY(vp, -.6, sy, -10.3, -.3, 'cheer', T); P.cam.dist = Math.max(3.6, P.cam.dist - dt * .15); }; }"""
# c9 the Apartemen Presiden: tilt up from the plaza to the golden crown (angle from the east, ep22 note)
C9 = BLD('apartemen', 1.75, .22, 17, 1.5, push=.25, dyaw=.02, dh=1.5, minD=12)
# c10 Bu Guru Gina leads the study tour (ep23 C6)
C10 = """() => { const P = window.__pulau, n = window.__TN(0); window.__clock = .3; window.__cheer = null; P.player.obj.visible = false; window.__tourS = 0;
  const [x, z] = window.__tourAt(0); window.__look(x, z, 2.75, .16, 4.2, false);
  window.__beforeRender = (dt, T) => { window.__tourS = 0; window.__pose(n, x, z, 2.75, 'talk', T); const u = n.obj.userData; u.armR.rotation.x = -2.6 + Math.sin(T * 4) * .1;
    window.__tgt(x - .3, z + .5, 1.3); P.cam.dist = Math.max(3.6, 4.2 - T * .15); }; }"""
# c11 'hampir tujuh ribu warga': the whole crowd at the stage square cheering, camera rising
C11 = """() => { const P = window.__pulau; window.__tourS = null; window.__clock = .3; window.__cheer = true; P.player.obj.visible = false; window.__look(0, -4, .3, .45, 14, false);
  window.__beforeRender = (dt, T) => { window.__tgt(0, -4, 0); P.cam.dist = 14 + T * 4; P.cam.pitch = Math.min(.95, .45 + T * .15); P.cam.yaw = .3 + T * .06; }; }"""
# c12 Klub Pertama at their spots by the hotel: D..A..B..Y cheers 'PERTAMA', princes_nay points at herself
C12 = """() => { window.__hideInst([[-2.2, 28.8], [.8, 28.8], [-2.2, 31.8]], .6); const P = window.__pulau, a = window.__N('%s'), b = window.__N('%s'); window.__clock = .3; window.__cheer = null; P.player.obj.visible = false;
  window.__fix(a); window.__fix(b); const x = .1, z = 28.8; window.__look(x, z, -1.57, .14, 3.2, false);
  window.__beforeRender = (dt, T) => { window.__z0(a); window.__z0(b); window.__pose(a, x, z - .4, -1.2, 'cheer', T); window.__pose(b, x + .1, z + .45, T < 1.3 ? -1.7 : -1.4, T < 1.3 ? 'still' : 'point', T);
    window.__keep([a, b], x, z, 2.2); window.__tgt(x, z, 1.1); P.cam.dist = Math.max(3.0, 3.4 - T * .15); }; }""" % (DABY, PRIN)
FX, FZ = 11.5, 13.5
# c13 night by the campfire: Aru among the residents, smiling (warm beat)
C13 = """() => { const P = window.__pulau; window.__clock = .62; window.__cheer = null; const fx = %s, fz = %s, ax = fx + .2, az = fz + 1.25; window.__look(ax, az, .5, .14, 2.6, false);
  window.__beforeRender = (dt, T) => { window.__keep([], fx, fz, 4.5); window.__ring(fx, fz, 1.55, T, 0, 7, i => i %% 3 ? 'sit' : 'sittalk');
    const W = window.__W(); for (let i = 0; i < 7; i++) { const n = W[i]; if (Math.hypot(n.x - ax, n.z - az) < .7) n.obj.visible = false; }
    window.__aru(ax, az, .3, T > .2 && T < 1.0, T); window.__tgt(ax, az, 1.25); P.cam.dist = Math.max(2.1, 2.6 - T * .15); P.cam.yaw = .5 + T * .03; }; }""" % (FX, FZ)
# c14 the bodyguard (Si Bodyguard) blocks Aru at his own campfire: 'Identitas dulu!'
C14 = """() => { const P = window.__pulau, g = window.__N('%s'); window.__fix(g); window.__clock = .62; window.__cheer = null;
  const gx = %s - 2.2, gz = %s + .4; window.__look(gx, gz - .5, -1.3, .12, 3.3, false);
  window.__beforeRender = (dt, T) => { window.__z0(g); window.__aru(gx, gz - 1.0, 0, T > 1.1, T); window.__guardP(g, gx, gz, PI, T, T < 1.1);
    window.__keep([g], gx, gz - .5, 2.6); window.__tgt(gx, gz - .5, 1.15); P.cam.dist = Math.max(3.4, 3.8 - T * .12); P.cam.yaw = -1.3 + Math.sin(T * .5) * .04; }; }""" % (GUARD, FX, FZ)
# c15 end: the camera rises from the busy campfire over the night island
C15 = """() => { const P = window.__pulau; window.__clock = .62; window.__cheer = true; P.player.obj.visible = false; const fx = %s, fz = %s; window.__look(fx, fz, .8, .35, 6, false);
  window.__beforeRender = (dt, T) => { window.__ring(fx, fz, 1.6, T, 0, 9, i => i %% 2 ? 'cheer' : 'wave'); window.__tgt(fx, fz, .8); P.cam.dist = 6 + T * 3.2; P.cam.pitch = Math.min(.95, .35 + T * .07); P.cam.yaw = .8 + T * .05; }; }""" % (FX, FZ)
SHOTS = {'c1': (C1, 165), 'c2': (C2, 160), 'c3': (C3, 105), 'c4': (C4, 66), 'c5': (C5, 72), 'c6': (C6, 90), 'c7': (C7, 72), 'c8': (C8, 105),
         'c9': (C9, 162), 'c10': (C10, 100), 'c11': (C11, 96), 'c12': (C12, 92), 'c13': (C13, 80), 'c14': (C14, 100), 'c15': (C15, 300)}
CLEAR = "() => { window.__showInst(); window.__cheer = null; window.__camTarget = null; window.__beforeRender = null; window.__clock = null; window.__tourS = null; }"
async def run(which):
    async with async_playwright() as p:
        b, pg = await setup(p)
        await pg.evaluate(BASE); await pg.evaluate("() => { " + NPC + " }"); await pg.evaluate("() => { " + EXTRA + " }"); await pg.evaluate("() => { " + TOUR + " }"); await pg.evaluate("() => { " + FIRE + " }")
        for k, (js, n) in SHOTS.items():
            if k in which and 'prev' not in which:
                await shoot(pg, 'e25' + k, int(os.environ.get('N_' + k, n)), start_js=js, warm=12)
                await pg.evaluate(CLEAR)
        if 'prev' in which:
            for k, (js, n) in SHOTS.items():
                if 'all' not in which and k not in which: continue
                await shoot(pg, 'p25' + k, 1, start_js=js, warm=int(os.environ.get('WARM', '40')))
                await pg.evaluate(CLEAR)
        await b.close()
if __name__ == "__main__": asyncio.run(run(sys.argv[1].split(",")))
