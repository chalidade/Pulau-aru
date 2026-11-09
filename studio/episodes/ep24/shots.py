"""Episode 24 "Hotel Pulau" shot list.  usage: DPR=2 python3 shots.py c1,c3,...  (DPR=1 + prev for checks)
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
GUARD, GINA, DABY, PRIN, TAN, WHO = 'Cawetssssss', 'Bu Guru Gina', 'D..A..B..Y a..j..a', 'princes_nay', 'KM GPP TAN', 'whoyss'
# hotel door (carpet) in world coords: the hotel faces west onto the main street
HX, HZ = 2.5, 29.0
SX, SZ = .1, 28.8   # the pavement in front of the hotel: camera from the street (west) sees the door behind
# c1 cold open: the bodyguard stands on the red carpet and stops Aru (profile, both faces, hotel door behind)
C1 = """() => { window.__hideInst([[-2.2, 28.8], [.8, 28.8], [-2.2, 31.8]], .6); const P = window.__pulau, g = window.__N('%s'); window.__time('siang'); window.__cheer = null;
  const gx = %s, gz = %s; window.__look(gx, gz - .5, -1.57, .12, 3.3, false);
  window.__beforeRender = (dt, T) => { const t = Math.max(0, T + .9), k = Math.min(1, t / 1.2); window.__z0(g);
    window.__aru(gx, gz - 1.0 - .8 * (1 - k), 0, T > 2.2 && T < 3.5, T); if (k < 1) { const u = P.player.obj.userData; if (u.legL) { u.legL.rotation.x = Math.sin(T * 9) * .5; u.legR.rotation.x = -Math.sin(T * 9) * .5; } }
    window.__guardP(g, gx, gz, PI, T, T < 2.1 || T > 3.5); window.__keep([g], gx, gz - .5, 2.6);
    window.__tgt(gx, gz - .5, 1.15); P.cam.dist = Math.max(3.6, 4.0 - T * .1); P.cam.yaw = -1.57 + Math.sin(T * .5) * .04; }; }""" % (GUARD, SX, SZ + .5)
# c2 Kotak Usulan: Fattan (KM GPP TAN) by the box, two thumbs up twice
C2 = """() => { const n = window.__on('%s', .45, .2, 3.4, 1.1, .12, 2.6, .05); }""" % TAN
# c3 the reveal: an aerial that sinks toward the new hotel by the pier
C3 = """() => { const P = window.__pulau; window.__time('siang'); window.__cheer = null; P.player.obj.visible = false; window.__look(4, 29, -1.0, 1.0, 26, false);
  window.__beforeRender = (dt, T) => { window.__tgt(3.6, 29, 2.5); P.cam.dist = Math.max(10, 26 - T * 3.2); P.cam.pitch = Math.max(.32, 1.0 - T * .12); P.cam.yaw = -1.0 - T * .05; }; }"""
# c4 Klub Pertama at the door (their real spots in island.json): D..A..B..Y cheers, princes_nay points at him
C4 = """() => { window.__hideInst([[-2.2, 28.8], [.8, 28.8], [-2.2, 31.8]], .6); const P = window.__pulau, a = window.__N('%s'), b = window.__N('%s'); window.__time('siang'); window.__cheer = null; P.player.obj.visible = false;
  window.__fix(a); window.__fix(b); const x = %s, z = %s; window.__look(x, z, -1.57, .14, 3.2, false);
  window.__beforeRender = (dt, T) => { window.__z0(a); window.__z0(b); window.__pose(a, x, z - .4, T < 1.6 ? -1.2 : PI, T < 1.6 ? 'cheer' : 'still', T); window.__pose(b, x + .1, z + .45, T < 1.6 ? -1.7 : PI + .2, T < 1.6 ? 'still' : 'point', T);
    window.__keep([a, b], x, z, 2.2); window.__tgt(x, z, 1.1); P.cam.dist = Math.max(3.2, 3.6 - T * .15); }; }""" % (DABY, PRIN, SX, SZ)
# c5 the president books the top floor; Aru reminds him he has an apartment (bodyguard behind him)
C5 = """() => { window.__hideInst([[-2.2, 28.8], [.8, 28.8], [-2.2, 31.8]], .6); const P = window.__pulau, pr = window.__PR(), g = window.__N('%s'); window.__time('siang'); window.__cheer = null;
  const px = %s, pz = %s + .5; window.__look(px, pz - .5, -1.57, .14, 3.4, false);
  window.__beforeRender = (dt, T) => { window.__z0(pr); window.__z0(g); window.__pose(pr, px, pz, PI - .3, T < 1.5 ? 'talk' : 'still', T); if (T < 1.5) { const u = pr.obj.userData; u.armR.rotation.x = -2.5; }
    window.__guardP(g, px + .55, pz + .5, PI, T, false); window.__aru(px, pz - 1.05, -.3, T > 1.55, T);
    window.__keep([pr, g], px, pz, 2.4); window.__tgt(px, pz - .5, 1.15); P.cam.dist = Math.max(3.6, 4.0 - T * .1); }; }""" % (GUARD, SX, SZ)
# c6 close on the president: 'Itu buat hari kerja. Ini buat liburan.'
C6 = """() => { window.__hideInst([[-2.2, 28.8], [.8, 28.8], [-2.2, 31.8]], .6); const P = window.__pulau, pr = window.__PR(); window.__cheer = null; P.player.obj.visible = false;
  const px = %s, pz = %s + .5; window.__look(px, pz, -1.15, .1, 2.4, false);
  window.__beforeRender = (dt, T) => { window.__z0(pr); window.__pose(pr, px, pz, -1.3, 'talk', T); window.__keep([pr], px, pz, 1.8); window.__tgt(px, pz, 1.25); P.cam.dist = Math.max(2.0, 2.4 - T * .12); P.cam.yaw = -1.15 + T * .03; }; }""" % (SX, SZ)
# c7 Bu Guru Gina walks up with her register: 'PR study tour-nya mana?'; the president, caught, looks at the hotel
C7 = """() => { window.__hideInst([[-2.2, 28.8], [.8, 28.8], [-2.2, 31.8]], .6); const P = window.__pulau, pr = window.__PR(), n = window.__N('%s'); window.__fix(n); window.__cheer = null; P.player.obj.visible = false;
  const px = %s, pz = %s; window.__look(px, pz + .5, -1.57, .14, 3.5, false);
  window.__beforeRender = (dt, T) => { const k = Math.min(1, Math.max(0, T + .4) / 1.0); window.__z0(pr); window.__z0(n);
    window.__pose(n, px - .1, pz + 1.7 - .6 * k, PI - .25, k < 1 ? 'walk' : 'talk', T); { const u = n.obj.userData; u.armL.rotation.x = -1.2; }
    window.__pose(pr, px, pz, T < 2.9 ? -.2 : 1.57, 'still', T); if (T > 2.9) { const u = pr.obj.userData; u.armR.rotation.x = -1.9; u.armR.rotation.z = -.4; u.body.rotation.x = .12; }
    window.__keep([pr, n], px, pz + .5, 2.6); window.__tgt(px, pz + .55, 1.15); P.cam.dist = Math.max(3.7, 4.1 - T * .1); }; }""" % (GINA, SX, SZ)
# c8 by the luggage trolley: Aru finds a suitcase out of place, whoyss beside it: 'Hehe... bukan aku.'
C8 = """() => { window.__hideInst([[-2.2, 28.8], [.8, 28.8], [-2.2, 31.8]], .6); const P = window.__pulau, w = window.__N('%s'); window.__fix(w); window.__cheer = null;
  const wx = %s, wz = %s + .5; window.__look(wx, wz - .5, -1.57, .14, 3.0, false);
  window.__beforeRender = (dt, T) => { window.__z0(w); window.__pose(w, wx, wz, T < 1.85 ? PI : -1.3, 'still', T); { const u = w.obj.userData; u.armR.rotation.x = T > 1.85 ? -2.4 + Math.sin(T * 6) * .1 : -.5; u.armL.rotation.x = -.6; }
    window.__aru(wx, wz - 1.0, -.2, T < 1.85, T); window.__keep([w], wx, wz, 2.0); window.__tgt(wx, wz - .5, 1.1); P.cam.dist = Math.max(3.3, 3.6 - T * .12); }; }""" % (WHO, SX, SZ)
# c9 night: the hotel windows light up, a slow push in from the street
C9 = """() => { const P = window.__pulau; window.__time('malam'); window.__cheer = null; P.player.obj.visible = false; window.__look(3.6, 29, -1.3, .28, 13, false);
  window.__beforeRender = (dt, T) => { window.__tgt(3.6, 29, 3.0); P.cam.dist = Math.max(8, 13 - T * 1.1); P.cam.yaw = -1.3 + T * .03; }; }"""
# c10 night: Aru reads the guest book board (over his shoulder): room 3, Penjaga Mercusuar
C10 = """() => { const P = window.__pulau; window.__cheer = null; const bx = .5, bz = 31.0; window.__look(bx, bz, -1.57, .08, 2.4, false);
  window.__beforeRender = (dt, T) => { window.__aru(bx - 1.1, bz + .8, 2.17, false, T); window.__keep([], bx, bz, 2.0); window.__tgt(bx, bz + .1, 1.25); P.cam.dist = Math.max(2.0, 2.4 - T * .15); }; }"""
# c11 end: night, the camera rises from the lit hotel toward the sea and the lighthouse side
C11 = """() => { const P = window.__pulau; window.__cheer = null; P.player.obj.visible = false; window.__look(3.6, 29, -1.0, .3, 9, false);
  window.__beforeRender = (dt, T) => { window.__tgt(3.6, 29, 3.0); P.cam.dist = 9 + T * 2.0; P.cam.pitch = Math.min(.9, .3 + T * .07); P.cam.yaw = -1.0 + T * .06; }; }"""
SHOTS = {'c1': (C1, 195), 'c2': (C2, 205), 'c3': (C3, 205), 'c4': (C4, 118), 'c5': (C5, 118), 'c6': (C6, 90), 'c7': (C7, 190),
         'c8': (C8, 135), 'c9': (C9, 115), 'c10': (C10, 90), 'c11': (C11, 300)}
CLEAR = "() => { window.__showInst(); window.__cheer = null; window.__camTarget = null; window.__beforeRender = null; }"
async def run(which):
    async with async_playwright() as p:
        b, pg = await setup(p)
        await pg.evaluate(BASE); await pg.evaluate("() => { " + NPC + " }"); await pg.evaluate("() => { " + EXTRA + " }"); await pg.evaluate("() => { " + TOUR + " }")
        for k, (js, n) in SHOTS.items():
            if k in which and 'prev' not in which:
                await shoot(pg, 'e24' + k, int(os.environ.get('N_' + k, n)), start_js=js, warm=12)
                await pg.evaluate(CLEAR)
        if 'prev' in which:
            for k, (js, n) in SHOTS.items():
                if 'all' not in which and k not in which: continue
                await shoot(pg, 'p24' + k, 1, start_js=js, warm=int(os.environ.get('WARM', '40')))
                await pg.evaluate(CLEAR)
        await b.close()
if __name__ == "__main__": asyncio.run(run(sys.argv[1].split(",")))
