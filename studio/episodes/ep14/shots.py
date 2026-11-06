"""Episode 14 "Menara Sinyal Sal" shot list.  usage: DPR=2 python3 shots.py c1,c3,...  (DPR=1 + prev for checks)
Menara Sinyal Sal cells 71..73 x 54..56 (r2, board faces north onto the cross street), centre (16.5, -0.5), board at z ~ -2.0.
Monumen Dermawan centre (3, -8), faces south. Masjid centre (-10.5, -8.5), faces south. Stage centre (-1.5, -10.5).
Crowd = the live demo residents (island.json event, placards from event.signs); president/VP carry event.presSign/vpSign.
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
  window.__hideNear = (x, z, r, keep) => { for (const n of P.npcs) if (!keep.includes(n)) n.obj.visible = Math.hypot(n.x - x, n.z - z) > r; };
}"""
V = "new window.__pulau.cam.target.constructor"
G = "window.__pulau.WD.groundY"
# the live demo crowd, re-posed on the main street south of the stage facing north
CROWD = """const W = window.__W(); const spots = [[-2.3, -6.3], [-1.4, -6.5], [-.5, -6.3], [.4, -6.5], [-1.9, -5.5], [-1.0, -5.6], [-.1, -5.5], [.8, -5.4]];
  window.__crowd = (T, pose) => { for (let i = 0; i < 8; i++) { const [x, z] = spots[i]; window.__pose(W[i], x, z, Math.PI + (i % 3 - 1) * .15, pose(i), T + i * .6); } };"""
TW = """const W = window.__W(); const tw = [[15.6, -2.55], [16.4, -2.85], [17.25, -2.6], [14.9, -2.35], [18.0, -2.4]];"""
# c1 cold open: residents cheering at the foot of the tower, camera tilts up to the beacon
C1 = f"""() => {{ const P = window.__pulau; window.__time('siang'); window.__cand(false); window.__cheer = true; P.player.obj.visible = false; {TW}
  window.__look(16.4, -3.0, Math.PI + .15, .1, 3.1, false); let ty = 1.4;
  window.__beforeRender = (dt, T) => {{ window.__hideNear(16.5, -2.5, 4, W.slice(8, 13)); for (let i = 0; i < 5; i++) window.__pose(W[8 + i], tw[i][0], tw[i][1], Math.PI + .15 + (i - 2) * .12, 'cheer', T + i * .7);
    ty = Math.min(3.4, 1.4 + Math.max(0, T - .8) * .75); window.__camTarget = {V}(16.5, {G}(16.5, -3) + ty, -2.5); P.cam.dist = Math.min(3.4, P.cam.dist + dt * .1); }}; }}"""
# c2 the president in front of the Monumen Dermawan (Sal now tops the board), shocked
C2 = f"""() => {{ const P = window.__pulau, pr = window.__PR(); window.__time('siang'); window.__cand(false); window.__cheer = null; P.player.obj.visible = false; const x = 3, z = -5.3;
  window.__look(x, z, .15, .14, 3.2, false); window.__camTarget = {V}(x, {G}(x, z) + 1.35, z - .4);
  window.__beforeRender = (dt, T) => {{ window.__hideNear(x, z, 3.5, [pr]); window.__pose(pr, x, z, .15, T < 1.4 ? 'panic' : 'talk', T); P.cam.dist -= dt * .12; }}; }}"""
# c4 Aru on the street in front of the tower, pointing up
C4 = f"""() => {{ const P = window.__pulau, pl = P.player; window.__time('siang'); window.__cand(false); window.__cheer = null; const x = 16.3, z = -2.7;
  window.__look(x, z, Math.PI + .25, .04, 2.5, true); window.__camTarget = {V}(x, {G}(x, z) + 1.65, z + .3);
  window.__beforeRender = (dt, T) => {{ window.__hideNear(x, z, 4, []); pl.x = x; pl.z = z; pl.tx = null; pl.obj.rotation.y = Math.PI + .25; const u = pl.obj.userData;
    u.armR.rotation.x = T < 1.0 ? -1.1 + Math.sin(T * 7) * .4 : -2.7 + Math.sin(T * 8) * .1; u.armL.rotation.x = -.3; P.cam.dist = Math.max(2.2, P.cam.dist - dt * .08); }}; }}"""
# c5 aerial reveal of the tower, rising and orbiting
C5 = f"""() => {{ const P = window.__pulau; window.__time('siang'); window.__cand(false); window.__cheer = true; P.player.obj.visible = false;
  window.__look(16.5, -0.5, Math.PI + .5, .32, 11, false); window.__camTarget = {V}(16.5, {G}(16.5, -.5) + 3.6, -.5);
  window.__beforeRender = (dt, T) => {{ P.cam.dist += dt * 2.2; P.cam.pitch = Math.min(.75, P.cam.pitch + dt * .06); P.cam.yaw += dt * .09; }}; }}"""
# c6 residents cheer under the tower, side angle
C6 = f"""() => {{ const P = window.__pulau; window.__time('siang'); window.__cand(false); window.__cheer = true; P.player.obj.visible = false; {TW}
  window.__look(16.4, -3.0, Math.PI - .55, .2, 4.0, false); window.__camTarget = {V}(16.4, {G}(16.4, -3) + 1.3, -2.9);
  window.__beforeRender = (dt, T) => {{ window.__hideNear(16.5, -2.5, 4, W.slice(8, 13)); for (let i = 0; i < 5; i++) window.__pose(W[8 + i], tw[i][0], tw[i][1], Math.PI - .55 + (i - 2) * .1, i % 2 ? 'wave' : 'cheer', T + i * .7); P.cam.dist -= dt * .2; }}; }}"""
# c7 the vice president at the tower board, then points up
C7 = f"""() => {{ const P = window.__pulau, vp = window.__VP(); window.__time('siang'); window.__cand(false); window.__cheer = null; P.player.obj.visible = false; const x = 16, z = -2.7;
  window.__look(x, z, Math.PI + .35, .1, 2.7, false); window.__camTarget = {V}(x, {G}(x, z) + 1.5, z);
  window.__beforeRender = (dt, T) => {{ window.__hideNear(x, z, 4, [vp]); window.__pose(vp, x, z, Math.PI + .35, T < 1.5 ? 'talk' : 'point', T); P.cam.dist -= dt * .1; }}; }}"""
# c8 inside the masjid, newly opened (residents pray, camera set by the room)
C8 = """() => { const P = window.__pulau; window.__time('siang'); window.__cand(false); window.__cheer = null; window.__room.enter('masjid'); P.player.obj.visible = false; P.cam.pitch = .38; P.cam.dist = 6.5;
  window.__beforeRender = (dt, T) => { P.cam.dist -= dt * .15; }; }"""
# c9 the president sits alone on the masjid's front steps, thinking
C9 = f"""() => {{ const P = window.__pulau, pr = window.__PR(); window.__room.exit(); window.__time('siang'); window.__cand(false); window.__cheer = null; P.player.obj.visible = false; const x = -11.6, z = -3.9;
  window.__look(x, z, -.35, .1, 3.0, false); window.__camTarget = {V}(x, {G}(x, z) + .85, z - .2);
  window.__beforeRender = (dt, T) => {{ window.__hideNear(x, z, 4, [pr]); window.__pose(pr, x, z, -.35, T < 2.6 ? 'sit' : 'sittalk', T, -.4); P.cam.dist -= dt * .12; }}; }}"""
# c10 Aru on the stage announces registration, crowd backs in the foreground
C10 = f"""() => {{ const P = window.__pulau, pl = P.player; window.__time('siang'); window.__cand(false); window.__cheer = null; {CROWD}
  const st = window.__bld('mimbar'), sy = st.position.y + .55;
  window.__look(-1.4, -10.4, 0, .5, 4.2, true); window.__camTarget = {V}(-1.3, sy + 1.1, -9.8);
  window.__beforeRender = (dt, T) => {{ window.__crowd(T, i => 'idle'); pl.x = -1.4; pl.z = -10.0; pl.tx = null; pl.y = sy; pl.vy = 0; pl.obj.position.set(-1.4, sy, -10.0); pl.obj.rotation.y = 0; const u = pl.obj.userData;
    u.armR.rotation.x = -1.1 + Math.sin(T * 7) * .4; u.armL.rotation.x = T > 1.6 ? -2.5 : -.4; P.cam.dist -= dt * .15; }}; }}"""
# c11 the crowd raises their placards
C11 = f"""() => {{ const P = window.__pulau; window.__time('siang'); window.__cand(false); window.__cheer = true; P.player.obj.visible = false; {CROWD}
  window.__look(-.8, -6.0, Math.PI - .3, .3, 4.6, false); window.__camTarget = {V}(-.8, {G}(-.8, -6.0) + 1.5, -6.0);
  window.__beforeRender = (dt, T) => {{ window.__crowd(T, i => 'cheer'); P.cam.dist -= dt * .35; }}; }}"""
# c12 the president jumps in with his own placard
C12 = f"""() => {{ const P = window.__pulau, pr = window.__PR(); window.__time('siang'); window.__cand(true); window.__cheer = null; P.player.obj.visible = false; const x = -1.0, z = -7.0;
  window.__look(x, z, Math.PI - .2, .1, 2.8, false); window.__camTarget = {V}(x, {G}(x, z) + 1.45, z);
  window.__beforeRender = (dt, T) => {{ window.__hideNear(x, z, 3, [pr]); window.__pose(pr, x, z, Math.PI - .2, T < 2.2 ? 'talk' : 'cheer', T); P.cam.dist -= dt * .1; }}; }}"""
# c13 the vice president, calm, holds up 'AKU DAFTAR DULUAN'
C13 = f"""() => {{ const P = window.__pulau, vp = window.__VP(); window.__time('siang'); window.__cand(true); window.__cheer = null; P.player.obj.visible = false; const x = -.2, z = -7.0;
  window.__look(x, z, Math.PI + .25, .1, 2.6, false); window.__camTarget = {V}(x, {G}(x, z) + 1.45, z);
  window.__beforeRender = (dt, T) => {{ window.__hideNear(x, z, 3, [vp]); window.__pose(vp, x, z, Math.PI + .25, 'cheer', T * .4); P.cam.dist -= dt * .08; }}; }}"""
# c14 end: crowd and candidates on the main street, camera rises and pulls out toward the tower side
C14 = f"""() => {{ const P = window.__pulau, pr = window.__PR(), vp = window.__VP(); window.__time('siang'); window.__cand(true); window.__cheer = true; P.player.obj.visible = false; {CROWD}
  window.__look(-1, -6.5, .4, .55, 7, false); window.__camTarget = {V}(-1, {G}(-1, -6.5) + 1.0, -6.5);
  window.__beforeRender = (dt, T) => {{ window.__crowd(T, i => i % 2 ? 'cheer' : 'walk'); window.__pose(pr, -1.4, -7.3, Math.PI, 'cheer', T); window.__pose(vp, -.4, -7.3, Math.PI, 'cheer', T + 1);
    P.cam.dist += dt * 1.6; P.cam.pitch = Math.min(1.0, P.cam.pitch + dt * .05); P.cam.yaw += dt * .05; }}; }}"""
SHOTS = {'c1': (C1, 120), 'c2': (C2, 140), 'c4': (C4, 120), 'c5': (C5, 175), 'c6': (C6, 120), 'c7': (C7, 110), 'c8': (C8, 105),
         'c9': (C9, 200), 'c10': (C10, 115), 'c11': (C11, 90), 'c12': (C12, 170), 'c13': (C13, 75), 'c14': (C14, 260)}
CLEAR = "() => { window.__cheer = null; window.__camTarget = null; window.__beforeRender = null; }"
async def run(which):
    async with async_playwright() as p:
        b, pg = await setup(p)
        await pg.evaluate(BASE)
        for k, (js, n) in SHOTS.items():
            if k in which and 'prev' not in which:
                await shoot(pg, 'e14' + k, n, start_js=js, warm=12)
                await pg.evaluate(CLEAR)
        if 'prev' in which:
            for k, (js, n) in SHOTS.items():
                if 'all' not in which and k not in which: continue
                await shoot(pg, 'p14' + k, 1, start_js=js, warm=int(os.environ.get('WARM', '40')))
                await pg.evaluate(CLEAR)
        await b.close()
if __name__ == "__main__": asyncio.run(run(sys.argv[1].split(",")))
