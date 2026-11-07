"""Episode 19 "Warga Baru" shot list.  usage: DPR=2 python3 shots.py c1,c3,...  (DPR=1 + prev for checks)
The 14 new regulars stand at their own spots (island.json -> residents[].spot/pose, role 'cast'); shots only frame them.
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
    return n; };"""
def ON(name, off=0, pitch=.18, dist=3.0, h=1.0, push=.15, minD=2.0, sway=0, extra=''):
    return f"() => {{ const n = window.__on({name!r}, {off}, {pitch}, {dist}, {h}, {push}, {minD}, {sway}); {extra} }}"
# c1 cold open: princes_nay, hand on forehead: "harusnya aku yang pertama!"
C1 = ON('princes_nay', -.55, .1, 2.7, 1.55, .1, 2.1)
# c2 D..A..B..Y running on the spot at the start line
C2 = ON('D..A..B..Y a..j..a', -.3, .14, 2.6, 1.0, .12, 2.0)
# c3 Alexandre, hero pose by the lighthouse
C3 = ON('Alexandre', -.7, .22, 3.0, 1.1, .2, 2.2)
# c4 whoyss sneaking behind the bushes north of the stage
C4 = ON('whoyss', .8, .3, 3.0, .9, .1, 2.3)
# c5 Luci explaining at the notice board
C5 = ON('Luci Ardiansyah', .3, .14, 2.8, 1.05, .12, 2.1)
# c6 Aru steps up beside Luci: "Itu buat kapal, Luci."
C6 = """() => { const P = window.__pulau, n = window.__on('Luci Ardiansyah', .35, .16, 3.4, 1.0, .1, 2.8), pl = P.player;
  const ax = n.x + .9, az = n.z + .25;
  const prev = window.__beforeRender; window.__beforeRender = (dt, T) => { prev(dt, T); pl.x = ax; pl.z = az; pl.tx = null; pl.obj.visible = true; pl.obj.rotation.y = -.9;
    const u = pl.obj.userData; if (u.armR) { u.armR.rotation.x = -1.1 + Math.sin(T * 7) * .4; u.armL.rotation.x = -.6 + Math.sin(T * 5) * .2; } }; }"""
# c7 inyuu with the game pad by the school playground
C7 = ON('inyuu', .3, .14, 2.6, 1.0, .12, 2.0)
# c8 senar muliya playing at the campfire
C8 = ON('senar muliya', .2, .2, 2.8, .9, .12, 2.1, .2)
# c9 ALIF HR scratching his head beside the houses
C9 = ON('ALIF HR', -.3, .14, 2.7, 1.05, .12, 2.0)
# c10 Letisya, arms folded at the start of the pier
C10 = ON('Letisya Khianantaa', .3, .12, 2.5, 1.1, .1, 1.9)
# c11 Letisya wins: slow orbit
C11 = ON('Letisya Khianantaa', -.6, .3, 3.6, 1.0, .15, 2.8, .5)
# c12 dell_ sitting at the end of the pier, side view towards the sea
C12 = ON('dell_', 1.3, .2, 2.8, .6, .1, 2.2)
# c13 end: from dell_ the camera rises over the pier and the town, crowd cheers
C13 = """() => { const P = window.__pulau, n = window.__on('dell_', 2.6, .3, 3.0, .6, 0, 0); window.__cheer = true;
  window.__beforeRender = (dt, T) => { window.__camTarget = new P.cam.target.constructor(n.x, .6 + Math.min(T, 6) * .5, n.z - Math.min(T, 6) * 2.2); P.cam.dist += dt * 3.2; P.cam.pitch = Math.min(.95, P.cam.pitch + dt * .09); }; }"""
SHOTS = {'c1': (C1, 160), 'c2': (C2, 78), 'c3': (C3, 126), 'c4': (C4, 114), 'c5': (C5, 132), 'c6': (C6, 61), 'c7': (C7, 123),
         'c8': (C8, 132), 'c9': (C9, 162), 'c10': (C10, 88), 'c11': (C11, 158), 'c12': (C12, 120), 'c13': (C13, 200)}
CLEAR = "() => { window.__cheer = null; window.__camTarget = null; window.__beforeRender = null; }"
async def run(which):
    async with async_playwright() as p:
        b, pg = await setup(p)
        await pg.evaluate(BASE); await pg.evaluate("() => { " + NPC + " }")
        for k, (js, n) in SHOTS.items():
            if k in which and 'prev' not in which:
                await shoot(pg, 'e19' + k, int(os.environ.get('N_' + k, n)), start_js=js, warm=12)
                await pg.evaluate(CLEAR)
        if 'prev' in which:
            for k, (js, n) in SHOTS.items():
                if 'all' not in which and k not in which: continue
                await shoot(pg, 'p19' + k, 1, start_js=js, warm=int(os.environ.get('WARM', '40')))
                await pg.evaluate(CLEAR)
        await b.close()
if __name__ == "__main__": asyncio.run(run(sys.argv[1].split(",")))
