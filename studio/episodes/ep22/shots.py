"""Episode 22 "Apartemen Presiden" shot list.  usage: DPR=2 python3 shots.py c1,c3,...  (DPR=1 + prev for checks)
President 'EGA_ gets the island's first tall building; Bu Guru Gina at the school gate; Zidan, penjaga masjid.
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
GUARD, DABY, PRIN, PINJ, GINA, ZID, WHO = 'Cawetssssss', 'D..A..B..Y a..j..a', 'princes_nay', 'Pinjam seratus 💸', 'Bu Guru Gina', 'panggil aja zidan🤩', 'whoyss'
# c1 cold open: D..A..B..Y sprints to the new apartment lobby, the bodyguard steps in front (camera on the street, east of the lobby)
C1 = """() => { const P = window.__pulau, g = window.__N('%s'), d = window.__N('%s'), [ax, az] = window.__apt(); window.__time('siang'); window.__cheer = null; P.player.obj.visible = false;
  const lx = ax, lz = az - 2.0; window.__look(lx, lz, 2.5, .2, 4.2, false);
  window.__beforeRender = (dt, T) => { const t = Math.max(0, T + .3), k = Math.min(1, t / .9); window.__z0(d); window.__z0(g);
    if (k < 1) window.__pose(d, lx + 2.4 - 1.5 * k, lz - .5 + 1.1 * k, -2.2, 'walk', T * 2.2); else { window.__pose(d, lx + .9, lz + .6, -2.1, 'still', T); const u = d.obj.userData; u.armR.rotation.x = u.armL.rotation.x = -2.9 + Math.sin(T * 9) * .2; u.body.position.y = Math.abs(Math.sin(T * 8)) * .06; }
    window.__guardP(g, lx - .1, lz + .25, T > 1.0 ? 2.3 : 2.9, T, T > 1.0); window.__keep([g, d], lx, lz, 2.4);
    window.__tgt(lx + .3, lz, 1.25); P.cam.dist = Math.max(3.4, 4.2 - T * .25); }; }""" % (GUARD, DABY)
# c3 President EGA at the Kotak Usulan asks for his apartment, VP King indo notes it down, the bodyguard beside him
C3 = """() => { const P = window.__pulau, pr = window.__PR(), vp = window.__VP(), g = window.__N('%s'); P.player.obj.visible = false; window.__time('siang'); window.__cheer = null;
  window.__look(-2.2, -3.5, -.15, .14, 4.4, false);
  window.__beforeRender = (dt, T) => { window.__z0(g); window.__pose(pr, -2.2, -3.4, -.15, T < 2.6 ? 'talk' : 'still', T);
    window.__pose(vp, -3.25, -3.5, .3, T > 2.6 ? 'talk' : 'still', T);
    window.__guardP(g, -1.3, -3.75, -.35, T, false);
    window.__keep([pr, vp, g], -2.2, -3.5, 2.2); window.__tgt(T < 2.6 ? -2.3 : -2.7, -3.5, 1.3); P.cam.dist = Math.max(4.0, 4.6 - T * .12); }; }""" % GUARD
# c4 the reveal: from above, the camera comes down the tower to the lobby sign
C4 = """() => { const P = window.__pulau, [ax, az] = window.__apt(); window.__time('siang'); window.__cheer = true; P.player.obj.visible = false; window.__look(ax, az, 2.75, 1.05, 30, false);
  window.__beforeRender = (dt, T) => { const k = Math.min(1, Math.max(0, T) / 3.0), e = k * k * (3 - 2 * k); P.cam.pitch = 1.05 - .62 * e; P.cam.dist = 30 - 16 * e; P.cam.yaw = 2.75 + .15 * e; window.__tgt(ax, az - .3, 6 - 3.2 * e); }; }"""
# c5 EGA at the lobby: the top floor is mine. Aru: no lift yet. EGA: stairs are fine too
C5 = """() => { const P = window.__pulau, pr = window.__PR(), g = window.__N('%s'), [ax, az] = window.__apt(); window.__cheer = null; P.player.obj.visible = false;
  const lx = ax, lz = az - 2.0; window.__look(lx, lz, 2.3, .16, 4.0, false);
  window.__beforeRender = (dt, T) => { window.__z0(g); const tk = T < 1.8 || T > 2.9;
    window.__pose(pr, lx - .2, lz - .1, 2.3, tk ? 'talk' : 'still', T); if (T < 1.8) { const u = pr.obj.userData; u.armR.rotation.x = -2.9 + Math.sin(T * 4) * .1; }
    if (T > 2.9) { const u = pr.obj.userData; u.armR.rotation.x = -2.5; u.armR.rotation.z = -.4; u.body.rotation.x = .12; }
    window.__aru(lx + .75, lz + .45, -1.9, T > 1.8 && T < 2.9, T);
    window.__guardP(g, lx - 1.1, lz + .2, 2.6, T, false); window.__keep([pr, g], lx, lz, 2.6);
    window.__tgt(lx + .3, lz - .2, 1.6 - Math.min(.3, T * .05)); P.cam.dist = Math.max(3.4, 4.0 - T * .1); }; }""" % GUARD
# c6 Klub Pertama + Pinjam Seratus queue at the lobby, lined up across the frame; the bodyguard holds them back
C6 = """() => { const P = window.__pulau, g = window.__N('%s'), d = window.__N('%s'), p = window.__N('%s'), q = window.__N('%s'), [ax, az] = window.__apt(); window.__cheer = null; P.player.obj.visible = false;
  const lx = ax + .2, lz = az - 2.3, Y = 1.75, ux = .18, uz = .98, at = s => [lx + ux * s, lz + uz * s]; window.__look(lx, lz, Y, .16, 4.4, false);
  window.__beforeRender = (dt, T) => { for (const n of [g, d, p, q]) window.__z0(n);
    { const [x, z] = at(.85); window.__guardP(g, x, z, Y - .5, T, true); }
    { const [x, z] = at(.28); window.__pose(p, x, z, Y - .25, T < 3.0 ? 'talk' : 'still', T); if (T < 3.0) { const u = p.obj.userData; u.armL.rotation.x = -2.6; u.armL.rotation.z = -.3; } }
    { const [x, z] = at(-.28); window.__pose(d, x, z, Y - .2, 'still', T); const u = d.obj.userData; u.armR.rotation.x = -2.8 + Math.sin(T * 9) * .15; }
    { const [x, z] = at(-.85); window.__pose(q, x, z, Y - .3, 'still', T); const u = q.obj.userData, c = T %% 4; u.armL.rotation.x = u.armR.rotation.x = -1.25 + (T > 3.0 && c < 1 ? Math.sin(c * 12) * .12 : 0); u.armL.rotation.z = .25; u.armR.rotation.z = -.25; u.body.rotation.x = .12; }
    window.__keep([g, d, p, q], lx, lz, 2.8); const f = Math.min(1, Math.max(0, T - 2.9) / .5), [tx, tz] = at(.3 - 1.0 * f); window.__tgt(tx, tz, 1.2); P.cam.dist = Math.max(3.7, 4.4 - T * .15); }; }""" % (GUARD, DABY, PRIN, PINJ)
# c7 Bu Guru Gina at the school gate (her web spot), two residents as pupils: D4L half raises a hand, inyuu with his game pad
C7 = """() => { const P = window.__pulau, n = window.__N('%s'), a = window.__N('D4L'), b = window.__N('inyuu'); window.__time('siang'); window.__cheer = null; window.__fix(n); window.__fix(a); window.__fix(b); P.player.obj.visible = false;
  const x = n.spot.x, z = n.spot.z; window.__look(x, z, 1.4, .14, 3.0, false);
  window.__beforeRender = (dt, T) => { window.__z0(a); window.__z0(b); window.__pose(a, x + .9, z + 1.0, -2.0, 'still', T); { const u = a.obj.userData; u.armR.rotation.x = -2.0 + Math.sin(T * 2) * .15; u.armR.rotation.z = -.1; }
    window.__pose(b, x + .7, z - .9, -1.0, 'still', T); { const u = b.obj.userData; const k = Math.sin(T * 14) * .08; u.armL.rotation.x = -1.25 + k; u.armR.rotation.x = -1.25 - k; }
    window.__keep([n, a, b], x, z, 2.6); window.__tgt(x + .3, z, 1.15); P.cam.dist = Math.max(2.5, 3.0 - T * .15); P.cam.yaw = 1.4 + Math.sin(T * .4) * .05; }; }""" % GINA
# c8 Gina gives homework: to the President, then two to the bodyguard (side view)
C8 = """() => { const P = window.__pulau, n = window.__N('%s'), pr = window.__PR(), g = window.__N('%s'); window.__fix(n); P.player.obj.visible = false; window.__cheer = null;
  const x = n.spot.x, z = n.spot.z; window.__look(x, z, 1.4, .16, 3.6, false);
  window.__beforeRender = (dt, T) => { window.__z0(g); window.__z0(pr); const ph = T < 4.0 ? 0 : T < 5.4 ? 1 : T < 9.2 ? 2 : 3;
    window.__pose(pr, x + .95, z + .7, -2.0, ph === 1 ? 'talk' : 'still', T); if (ph >= 2) { const u = pr.obj.userData; u.armR.rotation.x = -2.6; u.armR.rotation.z = -.5; u.body.rotation.x = .2; }
    window.__pose(g, x + 1.05, z - .7, -1.2, 'still', T); { const u = g.obj.userData; if (ph === 3) { u.armR.rotation.x = -2.7; u.armR.rotation.z = -.6; } else { u.armL.rotation.x = u.armR.rotation.x = -.55; u.armL.rotation.z = .55; u.armR.rotation.z = -.55; } }
    window.__keep([n, pr, g], x, z, 2.6); const f = Math.min(1, Math.max(0, T - 5.4) / .6); window.__tgt(x + .45, z + (ph >= 2 ? -.35 : .2) * (ph >= 2 ? f : 1), 1.2); P.cam.yaw = 1.4 - (ph >= 2 ? .15 * f : 0); P.cam.dist = Math.max(3.1, 3.6 - T * .05); }; }""" % (GINA, GUARD)
# c9 Zidan, penjaga masjid, sweeping the yard in front of the mosque (his web spot)
C9 = """() => { const P = window.__pulau; window.__time('siang'); const n = window.__on('%s', 0, .2, 3.4, 1.35, .2, 2.8); const prev = window.__beforeRender; window.__beforeRender = (dt, T) => { prev(dt, T); P.cam.yaw = Math.sin(T * .4) * .08 - .2; }; }""" % ZID
# c10 Zidan holds up a sandal; whoyss sneaks behind him and gets caught
C10 = """() => { const P = window.__pulau, n = window.__N('%s'), w = window.__N('%s'); window.__fix(n); window.__cheer = null; P.player.obj.visible = false;
  const x = n.spot.x, z = n.spot.z; window.__look(x, z, -.2, .18, 4.0, false);
  window.__beforeRender = (dt, T) => { window.__z0(w); const k = Math.min(1, Math.max(0, T - .3) / 2.4);
    if (T < 3.4) { window.__pose(w, x - 1.6 + .6 * k, z + .4, 1.4, 'still', T); const u = w.obj.userData; u.armL.rotation.x = u.armR.rotation.x = -.9; u.body.rotation.x = .35; u.body.position.y = -.08; u.legL.rotation.x = Math.sin(T * 6) * .3; u.legR.rotation.x = -Math.sin(T * 6) * .3; }
    else { window.__pose(w, x - 1.0, z + .4, 1.2, 'still', T); const u = w.obj.userData; u.armR.rotation.x = -2.7; u.armR.rotation.z = -.55; u.armR.rotation.x += Math.sin(T * 10) * .08; }
    n.obj.rotation.y = T > 3.2 ? -.9 : 0;
    window.__keep([n, w], x, z, 2.4); window.__tgt(x - .4, z, 1.2); P.cam.dist = Math.max(3.4, 4.0 - T * .12); }; }""" % (ZID, WHO)
# c11 Kedai Kopi opens: inside, a slow push
C11 = """() => { const P = window.__pulau; window.__cheer = null; window.__room.enter('kedaikopi'); P.player.obj.visible = false; P.cam.pitch = .38; P.cam.dist = 6.5;
  window.__beforeRender = (dt, T) => { P.cam.dist -= dt * .2; }; }"""
# c12 night: the apartment windows light up, the camera rises away
C12 = """() => { const P = window.__pulau, [ax, az] = window.__apt(); window.__room.exit(); window.__time('malam'); window.__cheer = null; P.player.obj.visible = false; window.__look(ax, az, 2.5, .42, 20, false);
  window.__beforeRender = (dt, T) => { window.__tgt(ax, az, 4.5); P.cam.dist = 20 + T * 1.5; P.cam.pitch = Math.min(.8, .32 + T * .03); P.cam.yaw = 2.5 + T * .04; }; }"""
SHOTS = {'c1': (C1, 140), 'c3': (C3, 95), 'c4': (C4, 110), 'c5': (C5, 140), 'c6': (C6, 215), 'c7': (C7, 120), 'c8': (C8, 350),
         'c9': (C9, 95), 'c10': (C10, 170), 'c11': (C11, 85), 'c12': (C12, 185)}
CLEAR = "() => { window.__cheer = null; window.__camTarget = null; window.__beforeRender = null; }"
async def run(which):
    async with async_playwright() as p:
        b, pg = await setup(p)
        await pg.evaluate(BASE); await pg.evaluate("() => { " + NPC + " }"); await pg.evaluate("() => { " + EXTRA + " }")
        for k, (js, n) in SHOTS.items():
            if k in which and 'prev' not in which:
                await shoot(pg, 'e22' + k, int(os.environ.get('N_' + k, n)), start_js=js, warm=12)
                await pg.evaluate(CLEAR)
        if 'prev' in which:
            for k, (js, n) in SHOTS.items():
                if 'all' not in which and k not in which: continue
                await shoot(pg, 'p22' + k, 1, start_js=js, warm=int(os.environ.get('WARM', '40')))
                await pg.evaluate(CLEAR)
        await b.close()
if __name__ == "__main__": asyncio.run(run(sys.argv[1].split(",")))
