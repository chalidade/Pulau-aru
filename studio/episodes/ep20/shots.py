"""Episode 20 "Warga Baru Gelombang 2" shot list.  usage: DPR=2 python3 shots.py c1,c3,...  (DPR=1 + prev for checks)
The 6 new regulars (wave 2) stand at their own spots (island.json -> residents[].spot/pose, role 'cast'); shots only frame them.
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
GUARD = 'Cawetssssss'
# c1 cold open: the bodyguard blocks Aru in front of the stage, the president behind him
C1 = ON2(GUARD, -.35, .1, 3.0, 1.2, .15, 2.4, 0, 4.0, extra=AFTER % """const pl = window.__pulau.player; pl.x = n.x + .3; pl.z = n.z + 1.05; pl.tx = null; pl.obj.visible = true; pl.obj.rotation.y = -2.9;
  const u = pl.obj.userData; if (u.armR) { u.armR.rotation.x = -1.1 + Math.sin(T * 7) * .4; u.armL.rotation.x = -.6 + Math.sin(T * 5) * .2; }
  const g = n.obj.userData; g.armR.rotation.x = -1.55; g.armR.rotation.z = 0; g.body.rotation.y = .35;""")
# c2 tight low angle on the bodyguard: identitas?
C2 = ON2(GUARD, .25, .04, 2.2, 1.3, .12, 1.7, .15, 4.0)
# c3 aerial over the stage and the crowd (background for the card montage)
C3 = """() => { const P = window.__pulau; window.__time('siang'); window.__cheer = true; P.player.obj.visible = false; window.__look(-1.5, -8.5, .2, .95, 15, false); }"""
# c4 President EGA on the stage, the bodyguard in front of him
C4 = ON2('@EGA_91', -.45, .32, 4.2, 1.0, .12, 3.4, 0, 3.2, [GUARD])
# c5 Pinjam seratus in front of Bank Pulau
C5 = ON('Pinjam seratus 💸', .55, .12, 2.6, 1.0, .12, 2.0)
# c6 lala cute: no money, but a cookie
C6 = ON('lala cute', .3, .14, 2.6, 1.0, .12, 2.0)
# c7 Rayhan fishing on the pier; at 2.8 s a big tug: a sandal again
C7 = ON('_Rayhannn`', -1.0, .22, 3.0, .9, .08, 2.5, 0, AFTER % """if (T > 2.6) { const u = n.obj.userData; const k = Math.min(1, (T - 2.6) * 3); u.armR.rotation.x = u.armL.rotation.x = -1.1 - .9 * k; u.body.rotation.x = -.15 * k; }""")
# c8 whoyss sneaking (he hid the sandals)
C8 = ON('whoyss', -.5, .38, 3.0, .9, .1, 2.3)
# c9 Fattan, two thumbs, twice
C9 = ON('KM GPP TAN', .3, .14, 2.6, 1.0, .12, 2.0)
# c10 Revan: anime pose... then a stumble at 2.0 s (Klub Pertama runs past)
C10 = ON('-VANZwlee', .4, .1, 2.6, 1.15, .12, 2.0, 0, AFTER % """const u = n.obj.userData; u.body.rotation.x = 0; if (T < 2.0) { u.armL.rotation.x = -.15; u.armR.rotation.x = -2.45; u.armL.rotation.z = 0; u.armR.rotation.z = -.55; u.body.rotation.y = .25; }
  else { const k = Math.min(1, (T - 2.0) * 4); u.armL.rotation.x = u.armR.rotation.x = -2.6 + Math.sin(T * 20) * .3; u.armL.rotation.z = .5; u.armR.rotation.z = -.5; u.body.rotation.y = 0; u.body.rotation.x = .45 * k; u.body.rotation.z = .12 * k; }""")
# c11 D..A..B..Y running on the spot: PERTAMA! Minggir!
C11 = ON('D..A..B..Y a..j..a', -.3, .14, 2.6, 1.0, .12, 2.0)
# c12 NOVA hiding the face
C12 = ON('NOVA', .3, .12, 2.5, 1.1, .1, 1.9)
# c13 ALIF HR next to NOVA: the most ordinary one is me
C13 = ON('ALIF HR', -.3, .14, 2.7, 1.05, .12, 2.0)
# c14 the stage: bodyguard, VP, president. Wapres? Mundur. Presiden? Identitas dulu.
C14 = ON2(GUARD, -.3, .14, 3.8, 1.2, .1, 3.2, 0, 4.0, extra=AFTER % """const P = window.__pulau, pr = window.__PR(); window.__camTarget = new P.cam.target.constructor(n.x + .3, n.obj.position.y + 1.4, n.z - .5);
  const g = n.obj.userData; g.armR.rotation.x = -1.55; g.armR.rotation.z = 0; g.body.rotation.y = T < 2.3 ? .7 : 2.4;
  if (T > 4.9) { const u = pr.obj.userData; u.armR.rotation.x = u.armL.rotation.x = -2.8 + Math.sin(T * 12) * .3; }""")
# c15 end: up and away from the stage, the crowd cheers
C15 = """() => { const P = window.__pulau; window.__time('siang'); window.__cheer = true; P.player.obj.visible = false; window.__look(-1.5, -9.5, .25, .35, 6, false);
  window.__beforeRender = (dt, T) => { P.cam.dist += dt * 3.0; P.cam.pitch = Math.min(1.0, P.cam.pitch + dt * .12); P.cam.yaw = .25 + T * .05; }; }"""
SHOTS = {'c1': (C1, 145), 'c2': (C2, 142), 'c3': (C3, 12), 'c4': (C4, 130), 'c5': (C5, 135), 'c6': (C6, 76), 'c7': (C7, 172), 'c8': (C8, 74),
         'c9': (C9, 132), 'c10': (C10, 96), 'c11': (C11, 72), 'c12': (C12, 94), 'c13': (C13, 96), 'c14': (C14, 197), 'c15': (C15, 175)}
CLEAR = "() => { window.__cheer = null; window.__camTarget = null; window.__beforeRender = null; }"
async def run(which):
    async with async_playwright() as p:
        b, pg = await setup(p)
        await pg.evaluate(BASE); await pg.evaluate("() => { " + NPC + " }")
        for k, (js, n) in SHOTS.items():
            if k in which and 'prev' not in which:
                await shoot(pg, 'e20' + k, int(os.environ.get('N_' + k, n)), start_js=js, warm=12)
                await pg.evaluate(CLEAR)
        if 'prev' in which:
            for k, (js, n) in SHOTS.items():
                if 'all' not in which and k not in which: continue
                await shoot(pg, 'p20' + k, 1, start_js=js, warm=int(os.environ.get('WARM', '40')))
                await pg.evaluate(CLEAR)
        await b.close()
if __name__ == "__main__": asyncio.run(run(sys.argv[1].split(",")))
