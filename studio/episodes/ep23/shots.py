"""Episode 23 "Sekretaris & Study Tour" shot list.  usage: DPR=2 python3 shots.py c1,c3,...  (DPR=1 + prev for checks)
Debby becomes Sekretaris Presiden; Bu Guru Gina's study tour walks the island (island.json → tour).
"""
import asyncio, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'lib'))
from harness import *
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
EXTRA = """window.__apt = () => { const o = window.__bld('apartemen'); return [o.position.x, o.position.z]; };
  window.__tgt = (x, z, h) => { const P = window.__pulau; window.__camTarget = new P.cam.target.constructor(x, P.WD.groundY(x, z) + h, z); };
  window.__z0 = n => { const u = n.obj.userData; u.armL.rotation.z = u.armR.rotation.z = 0; u.body.rotation.x = 0; u.body.rotation.y = 0; u.body.position.y = 0; };
  window.__guardP = (n, x, z, face, T, stop) => { window.__pose(n, x, z, face, 'still', T); const u = n.obj.userData; if (stop) { u.armR.rotation.x = -1.6; u.armR.rotation.z = 0; u.armL.rotation.x = -.55; u.armL.rotation.z = .55; } else { u.armL.rotation.x = u.armR.rotation.x = -.55; u.armL.rotation.z = .55; u.armR.rotation.z = -.55; } };
  window.__keep = (K, x, z, R) => { for (const m of window.__pulau.npcs) if (!K.includes(m)) m.obj.visible = Math.hypot(m.x - x, m.z - z) > R; };
  window.__aru = (x, z, face, talk, T) => { const P = window.__pulau, pl = P.player; pl.obj.visible = true; pl.x = x; pl.z = z; pl.tx = null; pl.obj.position.set(x, P.WD.groundY(x, z), z); pl.obj.rotation.y = face; const u = pl.obj.userData; if (u.armR) { u.armR.rotation.x = talk ? -1.1 + Math.sin(T * 7) * .4 : 0; u.armL.rotation.x = talk ? -.6 + Math.sin(T * 5) * .2 : 0; } };"""
GUARD, DEB, GINA = 'Cawetssssss', '🌸 Debby_l0vata👻', 'Bu Guru Gina'
TOUR = """window.__T = () => window.__pulau.npcs.filter(n => n.tour).sort((a, b) => a.tour.i - b.tour.i);
  window.__TN = i => window.__T().find(n => n.tour.i === i);
  window.__stage = () => { const P = window.__pulau, pr = window.__PR(); return pr.obj.position.y; };"""
# c1 cold open: Debby hurries to the stage with her clipboard; the bodyguard steps in front of her (profile, both faces)
C1 = """() => { const P = window.__pulau, g = window.__N('%s'), d = window.__N('%s'); window.__time('siang'); window.__cheer = null; P.player.obj.visible = false;
  const gx = -1.1, gz = -8.0; window.__look(gx, gz, .15, .12, 3.4, false);
  window.__beforeRender = (dt, T) => { const t = Math.max(0, T + 1.0), k = Math.min(1, t / 2.0); window.__z0(d); window.__z0(g);
    const dx = gx - .85 - 1.2 * (1 - k), dz = gz + .1;
    if (k < 1) { window.__pose(d, dx, dz, 1.57, 'walk', T * 1.6); const u = d.obj.userData; u.armL.rotation.x = -1.15; }
    else { window.__pose(d, dx, dz, 1.57, 'still', T); const u = d.obj.userData; u.armL.rotation.x = -1.15; u.armR.rotation.x = T > 2.3 ? -.3 : -2.4 + Math.sin(T * 8) * .15; }
    window.__guardP(g, gx, gz, T > 1.9 ? -1.57 : -.4, T, T > 1.9); window.__keep([g, d], gx, gz, 2.6);
    window.__tgt((dx + gx) / 2 - .05, gz, 1.2); P.cam.dist = Math.max(3.0, 3.5 - T * .15); }; }""" % (GUARD, DEB)
# c3 on the stage: President EGA appoints Debby, she jumps for joy
C3 = """() => { const P = window.__pulau, pr = window.__PR(), d = window.__N('%s'), vp = window.__VP(); window.__time('siang'); window.__cheer = null; P.player.obj.visible = false;
  const y = window.__stage(), px = -2.0, pz = -10.7; window.__look(px - .4, pz, -.12, .12, 3.6, false);
  window.__beforeRender = (dt, T) => { window.__z0(d); window.__z0(pr); window.__poseY(pr, px, y, pz, -1.2, T < 2.6 ? 'talk' : 'still', T); if (T < 1.0) { const u = pr.obj.userData; u.armR.rotation.x = -1.6; }
    window.__poseY(d, px - .85, y, pz + .1, 1.35, T > 2.6 ? 'cheer' : 'still', T); if (T <= 2.6) { const u = d.obj.userData; u.armL.rotation.x = -1.15; }
    window.__keep([pr, d, vp], px, pz, 2.2); window.__tgt(px - .45, pz, .55 + 1.1); P.cam.dist = Math.max(3.0, 3.6 - T * .12); }; }""" % DEB
# c4 Debby reads the president's schedule beside the new Papan Jadwal
C4 = """() => { const P = window.__pulau, d = window.__N('%s'); window.__cheer = null; P.player.obj.visible = false;
  const dx = -5.0, dz = -10.9; window.__look(dx + .5, dz - .4, -.35, .12, 3.4, false);
  window.__beforeRender = (dt, T) => { window.__z0(d); window.__pose(d, dx, dz, -.1, 'still', T); const u = d.obj.userData; u.armL.rotation.x = -1.3; u.armR.rotation.x = T > 2.2 ? -2.3 + Math.sin(T * 5) * .1 : -1.3 + Math.sin(T * 16) * .06; u.armR.rotation.z = T > 2.2 ? .35 : 0;
    window.__keep([d], dx, dz, 1.6); window.__tgt(dx + .5, dz - .3, 1.3); P.cam.dist = Math.max(3.0, 3.4 - T * .1); P.cam.yaw = -.35 + Math.sin(T * .5) * .04; }; }""" % DEB
# c5 payoff: Debby shows the bodyguard his own line on the schedule (two PR), he steps aside: silakan lewat
C5 = """() => { const P = window.__pulau, g = window.__N('%s'), d = window.__N('%s'); window.__cheer = null; P.player.obj.visible = false;
  const gx = -1.1, gz = -8.0; window.__look(gx, gz, -.3, .14, 3.2, false);
  window.__beforeRender = (dt, T) => { window.__z0(d); window.__z0(g); const go = Math.min(1, Math.max(0, T - 3.4) / 1.0);
    window.__pose(d, gx - .8 + .3 * go, gz + .1 - 1.2 * go, 1.57 + 1.2 * go, go > 0 && go < 1 ? 'walk' : 'still', T * 1.5); { const u = d.obj.userData; if (T < 2.5) { u.armL.rotation.x = -1.8; u.armR.rotation.x = -1.9 + Math.sin(T * 7) * .1; } else if (!go) u.armL.rotation.x = -1.15; }
    if (T < 2.5) { window.__guardP(g, gx, gz, -1.57, T, true); const u = g.obj.userData; u.body.rotation.x = T > 1.2 ? .25 : 0; }
    else { const k = Math.min(1, (T - 2.5) / .6); window.__pose(g, gx + .35 * k, gz + .45 * k, -1.57 - .6 * k, 'still', T); const u = g.obj.userData; u.armR.rotation.x = -1.3; u.armR.rotation.z = .5 * k; u.body.rotation.x = .3 * k; u.armL.rotation.x = -.2; }
    window.__keep([g, d], gx, gz, 2.4); window.__tgt(gx - .4, gz - .3 * go, 1.15); P.cam.dist = Math.max(2.8, 3.2 - T * .1); }; }""" % (GUARD, DEB)
# c6 Bu Guru Gina at the study-tour banner by the school calls the pupils into line
C6 = """() => { const P = window.__pulau, n = window.__TN(0); window.__time('siang'); window.__cheer = null; P.player.obj.visible = false; window.__tourS = 0;
  const [x, z] = window.__tourAt(0); window.__look(x, z, 2.75, .16, 4.2, false);
  window.__beforeRender = (dt, T) => { window.__tourS = 0; window.__pose(n, x, z, 2.75, 'talk', T); const u = n.obj.userData; u.armR.rotation.x = -2.6 + Math.sin(T * 4) * .1;
    window.__tgt(x - .3, z + .5, 1.3); P.cam.dist = Math.max(3.6, 4.2 - T * .15); }; }"""
# c7 the tour sets off up the main street; Klub Pertama (D..A..B..Y vs princes_nay) fight over the front row (camera ahead, looking back)
C7 = """() => { const P = window.__pulau; window.__cheer = null; P.player.obj.visible = false; window.__tourS = 3.5;
  const a = window.__TN(1), b = window.__TN(2); window.__look(-1.0, 13, Math.PI, .15, 3.6, false);
  window.__beforeRender = (dt, T) => { window.__tourS = 3.5 + T * .8; const sw = Math.sin(T * 5) * .12;
    a.obj.position.x += sw; b.obj.position.x += sw; if (T > 1.9) { const u = b.obj.userData; u.armR.rotation.x = -1.6; u.armR.rotation.z = .9; u.armL.rotation.x = -2.6; }
    const mx = (a.obj.position.x + b.obj.position.x) / 2, mz = (a.obj.position.z + b.obj.position.z) / 2; window.__tgt(mx, mz - .5, 1.2); P.cam.dist = 3.6; P.cam.yaw = Math.PI - .25 + Math.sin(T * .6) * .05; }; }"""
# c9 the Menara Sinyal on the cross street: Luci 'explains' it (the tower is to their right)
C9 = """() => { const P = window.__pulau; window.__cheer = null; P.player.obj.visible = false; window.__tourS = window.__S9 || 36;
  const l = window.__TN(3); window.__look(16, -3.3, 2.2, .3, 6.5, false);
  window.__beforeRender = (dt, T) => { window.__tourS = (window.__S9 || 36) + T * .7; window.__tgt(l.obj.position.x + .6, l.obj.position.z + .6, 1.6); P.cam.dist = Math.max(5.2, 6.5 - T * .35); }; }"""
# c10 the Apartemen Presiden: Luci calls it a palace with a thousand floors; D4L: boleh foto?
C10 = """() => { const P = window.__pulau; window.__cheer = null; P.player.obj.visible = false; window.__tourS = window.__S10 || 70;
  const l = window.__TN(3), d4 = window.__TN(5); window.__look(-14, -3.3, Math.PI - .35, .42, 6, false);
  window.__beforeRender = (dt, T) => { window.__tourS = (window.__S10 || 70) + T * .5; if (T > 3.7) { const u = d4.obj.userData; u.armR.rotation.x = -2.0; u.armL.rotation.x = -2.0; u.armR.rotation.z = -.2; u.armL.rotation.z = .2; }
    window.__tgt(l.obj.position.x, l.obj.position.z + 1.2, 1.8); P.cam.dist = Math.max(5.2, 6 - T * .2); }; }"""
# c11 the apotik opens: inside, a slow push
C11 = """() => { const P = window.__pulau; window.__cheer = null; window.__tourS = null; window.__room.enter('apotik'); P.player.obj.visible = false; P.cam.pitch = .38; P.cam.dist = 6.5;
  window.__beforeRender = (dt, T) => { P.cam.dist -= dt * .2; }; }"""
# c12 the tour ends at the gapura by the pier: Gina turns round and gives homework
C12 = """() => { const P = window.__pulau; window.__room.exit(); window.__time('siang'); window.__cheer = null; P.player.obj.visible = false; const s = window.__S12 || 120; window.__tourS = s;
  const n = window.__TN(0), [x, z] = window.__tourAt(s); window.__look(x, z, -1.3, .2, 4.2, false);
  window.__beforeRender = (dt, T) => { window.__tourS = s; window.__pose(n, x, z, -2.55, 'talk', T); const u = n.obj.userData; u.armR.rotation.x = -2.5;
    for (const m of window.__T()) if (m !== n && T > 3.4) { const v = m.obj.userData; v.armL.rotation.x = v.armR.rotation.x = -.05; v.body.rotation.x = .35; v.armL.rotation.z = v.armR.rotation.z = 0; }
    window.__tgt(x, z - .15, 1.2); P.cam.dist = Math.max(3.9, 4.5 - T * .12); P.cam.yaw = -1.3 + T * .03; }; }"""
# c13 end: the tour walks past the banner by the school, the camera rises away
C13 = """() => { const P = window.__pulau; window.__cheer = null; P.player.obj.visible = false; const s = window.__S13 || 135; window.__tourS = s;
  window.__look(-2.5, 17, 1.2, .3, 7, false);
  window.__beforeRender = (dt, T) => { window.__tourS = s + T * .9; window.__tgt(-2.0, 17.5, 1.6); P.cam.dist = 7 + T * 1.2; P.cam.pitch = Math.min(.75, .3 + T * .05); P.cam.yaw = 1.2 + T * .03; }; }"""
SHOTS = {'c1': (C1, 150), 'c3': (C3, 165), 'c4': (C4, 145), 'c5': (C5, 190), 'c6': (C6, 145), 'c7': (C7, 150), 'c9': (C9, 115),
         'c10': (C10, 165), 'c11': (C11, 120), 'c12': (C12, 160), 'c13': (C13, 200)}
CLEAR = "() => { window.__cheer = null; window.__camTarget = null; window.__beforeRender = null; }"
async def run(which):
    async with async_playwright() as p:
        b, pg = await setup(p)
        await pg.evaluate(BASE); await pg.evaluate("() => { " + NPC + " }"); await pg.evaluate("() => { " + EXTRA + " }"); await pg.evaluate("() => { " + TOUR + " }")
        for k in ('S9', 'S10', 'S12', 'S13'):
            if os.environ.get(k): await pg.evaluate(f"window.__{k} = {float(os.environ[k])}")
        for k, (js, n) in SHOTS.items():
            if k in which and 'prev' not in which:
                await shoot(pg, 'e23' + k, int(os.environ.get('N_' + k, n)), start_js=js, warm=12)
                await pg.evaluate(CLEAR)
        if 'prev' in which:
            for k, (js, n) in SHOTS.items():
                if 'all' not in which and k not in which: continue
                await shoot(pg, 'p23' + k, 1, start_js=js, warm=int(os.environ.get('WARM', '40')))
                await pg.evaluate(CLEAR)
        await b.close()
if __name__ == "__main__": asyncio.run(run(sys.argv[1].split(",")))
