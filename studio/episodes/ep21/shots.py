"""Episode 21 "Bengkel Pulau" shot list.  usage: DPR=2 python3 shots.py c1,c3,...  (DPR=1 + prev for checks)
The coffee cart loses a wheel (staged only for the camera; on the web it stands repaired), Bengkel Pulau opens on the cross street.
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
CART = """window.__cartInit = async () => { if (window.__cart) return; const THREE = await import('three'), P = window.__pulau; const g = window.__bld('gerobakkopi'); window.__cart = g; window.__cartY = g.position.y;
    window.__rw = []; g.traverse(o => { if (o.isMesh && o.position.x > .5 && o.position.x < .7 && Math.abs(o.position.y - .26) < .02) window.__rw.push(o); });
    const M = c => new THREE.MeshStandardMaterial({ color: c, flatShading: true });
    const w = new THREE.Group(); const t = new THREE.Mesh(new THREE.CylinderGeometry(.3, .3, .08, 10), M('#3a2a20')); t.rotation.x = Math.PI / 2; t.castShadow = true; w.add(t);
    const h = new THREE.Mesh(new THREE.CylinderGeometry(.09, .09, .1, 8), M('#9a9b94')); h.rotation.x = Math.PI / 2; w.add(h);
    for (let i = 0; i < 4; i++) { const s = new THREE.Mesh(new THREE.BoxGeometry(.03, .5, .03), M('#6b4a30')); s.rotation.z = i * Math.PI / 4; w.add(s); }
    w.visible = false; P.roads.parent.add(w); window.__wh = w;
    const bo = new THREE.Group(); for (const [x, z] of [[0, 0], [.13, .06], [.05, .15]]) { const b = new THREE.Mesh(new THREE.CylinderGeometry(.03, .03, .08, 6), M('#b8bec2')); b.rotation.z = Math.PI / 2; b.position.set(x, .03, z); bo.add(b); const hd = new THREE.Mesh(new THREE.CylinderGeometry(.05, .05, .02, 6), M('#8a9196')); hd.rotation.z = Math.PI / 2; hd.position.set(x - .05, .03, z); bo.add(hd); }
    bo.visible = false; P.roads.parent.add(bo); window.__bolts = bo; };
  window.__cartSet = k => { const g = window.__cart; g.rotation.z = -.2 * k; g.position.y = window.__cartY - .14 * k; for (const o of window.__rw) o.visible = k < .01; };
  window.__whAt = (x, z, roll, flat, ry) => { const P = window.__pulau, w = window.__wh; w.visible = true; const y = P.WD.groundY(x, z);
    if (flat) { w.position.set(x, y + .05, z); w.rotation.set(Math.PI / 2, 0, 0); } else { w.position.set(x, y + .3, z); w.rotation.set(0, ry || 0, roll); } };
  window.__boltsAt = (x, z) => { const b = window.__bolts; b.visible = true; b.position.set(x, window.__pulau.WD.groundY(x, z), z); };
  window.__hero = (n, x, z, face, T, fist) => { window.__pose(n, x, z, face, 'still', T); const u = n.obj.userData; u.armL.rotation.x = .25; u.armR.rotation.x = fist ? -2.9 : .25; u.armL.rotation.z = -.75; u.armR.rotation.z = fist ? 0 : .75; u.body.rotation.x = -.08; };
  window.__z0 = n => { const u = n.obj.userData; u.armL.rotation.z = u.armR.rotation.z = 0; u.body.rotation.x = 0; u.body.rotation.y = 0; };
  window.__tgt = (x, z, h) => { const P = window.__pulau; window.__camTarget = new P.cam.target.constructor(x, P.WD.groundY(x, z) + h, z); };"""
SELLER = '@sapta.rajo.ghaisa'
# c1 cold open: the coffee cart tips over, a wheel rolls away, the seller panics (camera in front, slightly right)
C1 = """async () => { await window.__cartInit(); const P = window.__pulau, n = window.__N('%s'); window.__time('siang'); window.__cheer = null; P.player.obj.visible = false;
  window.__look(5.6, -4.6, .75, .12, 4.4, false);
  window.__beforeRender = (dt, T) => { const t = Math.max(0, T + .35), k = Math.min(1, t / .35); window.__cartSet(k); const d = t * 1.25;
    window.__whAt(5.71 + d, -4.94 + d * .3, -d / .3, false); window.__pose(n, 5, -5.71, .35, 'panic', T); window.__hideNear(5, -5, 1.5, [n]);
    window.__tgt(5.6 + Math.min(1.0, d * .3), -4.8, 1.3); P.cam.dist = Math.max(3.8, 4.4 - T * .2); }; }""" % SELLER
# c2 Alexandre runs in from the street and strikes the hero pose next to the broken cart
C2 = """() => { const P = window.__pulau, n = window.__N('Alexandre'), s = window.__N('%s'); window.__cartSet(1); window.__whAt(8.0, -3.9, 0, true); window.__look(6.5, -4.0, .35, .14, 3.2, false);
  window.__beforeRender = (dt, T) => { const k = Math.min(1, Math.max(0, T) / .8), x = 8.2 - 1.7 * k, z = -3.6 - .5 * k; window.__z0(n);
    if (k < 1) window.__pose(n, x, z, -1.2, 'walk', T * 1.6); else window.__hero(n, x, z, .25, T, T > 1.6);
    window.__pose(s, 5, -5.71, .35, 'panic', T); window.__hideNear(6, -4.5, 1.6, [n, s]); window.__tgt(6.3, -4.2, 1.25); P.cam.dist = Math.max(3.0, 3.6 - T * .15); }; }""" % SELLER
# c3 five minutes later: wheel back on, crooked; three bolts left on the ground, Alexandre scratches his head
C3 = """() => { const P = window.__pulau, n = window.__N('Alexandre'), s = window.__N('%s'); window.__cartSet(.55); window.__wh.visible = false; window.__boltsAt(6.55, -3.85);
  window.__whAt(5.78, -4.94, 0, false, .45); window.__look(6.2, -4.0, .55, .2, 2.6, false);
  window.__beforeRender = (dt, T) => { window.__z0(n); if (T < 1.4) window.__hero(n, 6.7, -4.3, .4, T, true); else { window.__pose(n, 6.7, -4.3, .2, 'still', T); const u = n.obj.userData; u.armR.rotation.x = -2.7 + Math.sin(T * 10) * .08; u.armR.rotation.z = -.55; u.body.rotation.x = .3; }
    window.__pose(s, 5, -5.71, .35, 'still', T); window.__hideNear(6, -4.5, 1.6, [n, s]); window.__tgt(6.35, -4.1, T < 1.4 ? 1.2 : .9); P.cam.dist = Math.max(2.2, 2.6 - T * .1); }; }""" % SELLER
# c4 Luci (sok tahu) explains: just blow it up like a balloon. Aru: that is a wheel.
C4 = """() => { const P = window.__pulau, n = window.__N('Luci Ardiansyah'), a = window.__N('Alexandre'), pl = P.player; window.__cartSet(.55); window.__whAt(5.78, -4.94, 0, false, .45); window.__boltsAt(6.55, -3.85);
  window.__look(6.9, -3.9, 1.35, .14, 3.3, false);
  window.__beforeRender = (dt, T) => { window.__z0(n); window.__z0(a); window.__pose(n, 7.0, -3.8, 1.25, T < 3.9 ? 'talk' : 'still', T); if (T < 3.9) { const u = n.obj.userData; u.armR.rotation.x = -2.5 + Math.sin(T * 3) * .25; }
    window.__pose(a, 6.2, -4.3, 1.1, 'still', T);
    pl.obj.visible = false; pl.x = 7.85; pl.z = -4.4; pl.tx = null; pl.obj.position.set(7.85, P.WD.groundY(7.85, -4.4), -4.4); pl.obj.rotation.y = -1.2; const u = pl.obj.userData; if (u.armR && T > 3.9) { u.armR.rotation.x = -1.1 + Math.sin(T * 7) * .4; u.armL.rotation.x = -.6 + Math.sin(T * 5) * .2; }
    window.__hideNear(7, -4.0, 1.8, [n, a]); window.__tgt(6.7, -3.95, 1.25); P.cam.yaw = 1.35 - Math.min(.2, T * .04); P.cam.dist = Math.max(2.8, 3.3 - T * .08); }; }"""
# c5 the Kotak Usulan; Fattan (two thumbs, twice) next to it
C5 = """() => { const P = window.__pulau, n = window.__N('KM GPP TAN'); window.__cartSet(.55); P.player.obj.visible = false; window.__fix(n);
  window.__look(-4.3, -4.0, .45, .18, 5.0, false);
  window.__beforeRender = (dt, T) => { window.__hideNear(-4.5, -4.2, 1.6, [n]); window.__tgt(-4.4 + Math.min(.8, Math.max(0, T - 3.0) * .4), -4.0, 1.35); P.cam.dist = Math.max(3.9, 5.0 - T * .15); }; }"""
# c6 President EGA at the box (talk), VP King indo answers, the bodyguard stands guard, Fattan behind
C6 = """() => { const P = window.__pulau, pr = window.__PR(), vp = window.__VP(), g = window.__N('Cawetssssss'), f = window.__N('KM GPP TAN'); P.player.obj.visible = false; window.__fix(f);
  window.__look(-2.2, -3.5, -.15, .14, 4.4, false);
  window.__beforeRender = (dt, T) => { window.__pose(pr, -2.2, -3.4, -.15, T < 3.3 || T > 5.7 ? 'talk' : 'still', T); window.__pose(vp, -3.25, -3.5, .3, T > 3.3 && T < 5.6 ? 'point' : 'still', T);
    if (T > 5.7) { const u = pr.obj.userData; u.armR.rotation.x = -2.6 + Math.sin(T * 9) * .3; u.armL.rotation.x = -.3; }
    window.__pose(g, -1.3, -3.75, -.35, 'still', T); const gu = g.obj.userData; gu.armL.rotation.x = gu.armR.rotation.x = -.55; gu.armL.rotation.z = .55; gu.armR.rotation.z = -.55;
    f.obj.visible = false; window.__hideNear(-2.2, -3.5, 2.2, [pr, vp, g]); window.__tgt(T < 3.3 ? -2.4 : T < 5.6 ? -2.8 : -2.4, -3.5, 1.3); P.cam.dist = Math.max(4.2, 5.0 - T * .1); }; }"""
# c7 Bengkel Pulau revealed: from above, the camera sweeps down to its front on the cross street
C7 = """() => { const P = window.__pulau; window.__cartSet(.55); P.player.obj.visible = false; window.__cheer = true; window.__look(13, -.6, 3.0, .85, 13, false);
  window.__beforeRender = (dt, T) => { const k = Math.min(1, Math.max(0, T) / 3.2), e = k * k * (3 - 2 * k); P.cam.pitch = .85 - .6 * e; P.cam.dist = 13 - 6.5 * e; P.cam.yaw = 3.0 + .25 * e; window.__tgt(13, -.6, 1.4); }; }"""
# c8 Klub Pertama at the bengkel: D..A..B..Y runs in first; princes_nay: you don't even have a vehicle
C8 = """() => { const P = window.__pulau, d = window.__N('D..A..B..Y a..j..a'), p = window.__N('princes_nay'); window.__cheer = null; P.player.obj.visible = false; window.__look(13, -1.5, 3.14, .14, 3.6, false);
  window.__beforeRender = (dt, T) => { window.__z0(d); window.__z0(p); const k = Math.min(1, Math.max(0, T) / .6);
    window.__pose(d, 11.0 + 1.5 * k, -1.6, k < 1 ? 1.57 : 3.0, 'walk', T * 2.2); if (k >= 1) { const u = d.obj.userData; u.armR.rotation.x = u.armL.rotation.x = -2.9 + Math.sin(T * 9) * .2; u.body.position.y = Math.abs(Math.sin(T * 8)) * .07; }
    window.__pose(p, 13.7, -1.75, -2.7, T > 1.5 ? 'point' : 'still', T); if (T > 1.5) { const u = p.obj.userData; u.armL.rotation.x = -2.6; u.armL.rotation.z = -.3; }
    window.__hideNear(13, -1.6, 1.8, [d, p]); window.__tgt(13, -1.6, 1.25); P.cam.dist = Math.max(3.4, 4.0 - T * .15); }; }"""
# c9 the cart stands straight again; the seller cheers; Alexandre does the hero pose next to it
C9 = """() => { const P = window.__pulau, s = window.__N('%s'), a = window.__N('Alexandre'); window.__cartSet(0); window.__wh.visible = false; window.__bolts.visible = false; window.__cheer = null; P.player.obj.visible = false;
  window.__look(5.4, -4.6, .2, .15, 3.3, false);
  window.__beforeRender = (dt, T) => { window.__pose(s, 5, -5.71, .1, 'cheer', T); window.__z0(a); window.__hero(a, 6.6, -4.3, -.1, T, Math.sin(T * 3) > .3); window.__hideNear(5.5, -4.8, 1.8, [s, a]); window.__tgt(5.6, -4.9, 1.3); P.cam.dist = Math.max(3.3, 3.9 - T * .2); }; }""" % SELLER
# c10 the warteg room opens: inside, a slow push
C10 = """() => { const P = window.__pulau; window.__cheer = null; window.__room.enter('warteg'); P.player.obj.visible = false; P.cam.pitch = .38; P.cam.dist = 6.5;
  window.__beforeRender = (dt, T) => { P.cam.dist -= dt * .2; }; }"""
# c11 who took the bolts? whoyss sneaking, three bolts in his hands (castKit 'sneak', also on the web)
C11 = """() => { const P = window.__pulau; window.__room.exit(); window.__time('siang'); const n = window.__on('whoyss', 0, .06, 3.0, 1.05, .12, 2.3); const prev = window.__beforeRender; window.__beforeRender = (dt, T) => { prev(dt, T); P.cam.yaw = n.spot.face + Math.sin(T * .4) * .08; }; }"""
# c12 end: up and away over the cross street, bengkel and the coffee cart below
C12 = """() => { const P = window.__pulau; window.__cartSet(0); window.__time('siang'); window.__cheer = true; P.player.obj.visible = false; window.__look(11, -1.2, 2.9, .45, 7, false);
  window.__beforeRender = (dt, T) => { P.cam.dist += dt * 2.6; P.cam.pitch = Math.min(1.0, P.cam.pitch + dt * .1); P.cam.yaw = 3.0 - T * .05; }; }"""
SHOTS = {'c1': (C1, 84), 'c2': (C2, 86), 'c3': (C3, 138), 'c4': (C4, 192), 'c5': (C5, 186), 'c6': (C6, 236), 'c7': (C7, 164), 'c8': (C8, 132),
         'c9': (C9, 94), 'c10': (C10, 120), 'c11': (C11, 200), 'c12': (C12, 220)}
CLEAR = "() => { window.__cheer = null; window.__camTarget = null; window.__beforeRender = null; }"
async def run(which):
    async with async_playwright() as p:
        b, pg = await setup(p)
        await pg.evaluate(BASE); await pg.evaluate("() => { " + NPC + " }"); await pg.evaluate("() => { " + CART + " }"); await pg.evaluate("async () => { await window.__cartInit(); }")
        for k, (js, n) in SHOTS.items():
            if k in which and 'prev' not in which:
                await shoot(pg, 'e21' + k, int(os.environ.get('N_' + k, n)), start_js=js, warm=12)
                await pg.evaluate(CLEAR)
        if 'prev' in which:
            for k, (js, n) in SHOTS.items():
                if 'all' not in which and k not in which: continue
                await shoot(pg, 'p21' + k, 1, start_js=js, warm=int(os.environ.get('WARM', '40')))
                await pg.evaluate(CLEAR)
        await b.close()
if __name__ == "__main__": asyncio.run(run(sys.argv[1].split(",")))
