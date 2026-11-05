"""Episode 10 "Kopi & Pos Ronda" shot list.  usage: DPR=2 python3 shots.py c1,c3a,...  (DPR=1 + prev for checks)
World: pos ronda cells (50..51, 54..55) r=2, centre (-5, -1), front faces north (-z); seat front edge z -1.55, top +.55.
Kedai kopi cells (45..47, 54..55) r=2 scale 1.2, centre (-9.5, -1), counter faces north; seller ~(-8.96, -.76).
Cross street y 52-53 (world z -3.5..-2.5). Aru on Pulau Seberang as in ep 8.
"""
import asyncio, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'lib'))
from harness import *
BASE = """() => { const P = window.__pulau; window.PI = Math.PI;
  window.__look = (x, z, yaw, pitch, dist, show) => { const pl = P.player; pl.x = x; pl.z = z; pl.tx = null; pl.vy = 0; pl.obj.visible = !!show; P.cam.yaw = yaw; P.cam.pitch = pitch; P.cam.dist = dist; P.cam.target.set(x, 1, z); };
  window.__W = () => P.npcs.filter(n => n.role === 'wander' && n.num);
  window.__VP = () => P.npcs.find(n => n.vp); window.__PR = () => P.npcs.find(n => n.pres);
  const scene = P.roads.parent; let wp = null; scene.traverse(o => { if (o.userData && o.userData.b && o.userData.b.type === 'waterpark') wp = o; });
  window.__wpL = (lx, ly, lz) => [wp.position.x + lx, wp.position.y + ly, wp.position.z + lz];
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
    if (pose === 'walk') { u.legL.rotation.x = Math.sin(T * 7) * .5; u.legR.rotation.x = -Math.sin(T * 7) * .5; u.armL.rotation.x = -Math.sin(T * 7) * .4; u.armR.rotation.x = Math.sin(T * 7) * .4; } };
  window.__pose = (n, x, z, face, pose, T, dy = 0) => window.__poseY(n, x, P.WD.groundY(x, z) + dy, z, face, pose, T);
  window.__hideNear = (x, z, r, keep) => { for (const n of P.npcs) if (!keep.includes(n)) n.obj.visible = Math.hypot(n.x - x, n.z - z) > r; };
}"""
V = "new window.__pulau.cam.target.constructor"
G = "window.__pulau.WD.groundY"
PI = 3.14159
# helpers: sit someone on the pos ronda platform at local x offset dx (world x = -5 - dx)
SIT = f"""window.__sit = (n, wx, pose, T, face = Math.PI, dz = 0) => {{ const y = {G}(-5, -1) + .55 - .42; window.__poseY(n, wx, y, -1.42 + dz, face, pose, T); }};"""
# c1 cold open (night): the president alone on the pos ronda, yawning
C1 = f"""() => {{ const P = window.__pulau, pr = window.__PR(); window.__time('malam'); {SIT} const gy = {G}(-5, -1);
  window.__look(-5.1, -1.5, PI - .2, .1, 3.1, false); window.__camTarget = {V}(-5.1, gy + 1.15, -1.5);
  window.__beforeRender = (dt, T) => {{ window.__hideNear(-5, -1, 4, [pr]); window.__sit(pr, -5.1, T > .6 && T < 2.6 ? 'yawn' : 'sittalk', T); P.cam.dist -= dt * .12; P.cam.yaw += dt * .04; }}; }}"""
C3A = f"""() => {{ const P = window.__pulau, W = window.__W(); window.__time('siang'); window.__cheer = true; window.__look(3, -8, -.15, .32, 8.5, false); window.__camTarget = {V}(3, {G}(3, -8) + 1.6, -8);
  window.__beforeRender = (dt, T) => {{ window.__hideNear(3, -5.5, 2.5, []); [0, 1, 2, 3].forEach(i => window.__pose(W[i], 1.6 + i * .95, -5.3 + (i % 2) * .35, Math.PI, 'cheer', T + i)); P.cam.dist -= dt * .5; }}; }}"""
C3B = f"""() => {{ const P = window.__pulau, W = window.__W(); window.__time('siang'); window.__cheer = true; window.__look(1.0, -11.0, .35, .55, 7.5, false); window.__camTarget = {V}(1.0, {G}(1, -11) + 1.0, -11.0);
  window.__beforeRender = (dt, T) => {{ for (let i = 0; i < 8; i++) window.__pose(W[i], -.6 + (i % 4) * 1.0, -10.2 + Math.floor(i / 4) * 1.0, Math.PI - .3, 'cheer', T + i * .7); P.cam.dist -= dt * .4; }}; }}"""
# c4 kedai kopi reveal: slow orbit, two customers at the counter, seller behind it
C4 = f"""() => {{ const P = window.__pulau, W = window.__W(); window.__time('siang'); const gy = {G}(-9.5, -1);
  window.__look(-9.3, -1.6, PI + .45, .42, 6.6, false); window.__camTarget = {V}(-9.3, gy + 1.0, -1.6);
  window.__beforeRender = (dt, T) => {{ window.__hideNear(-9.5, -1.5, 5, [W[4], W[5], W[3]]); window.__pose(W[4], -9.0, -2.05, 0, 'reach', T); window.__pose(W[5], -9.8, -2.1, .2, 'eat', T + 1);
    window.__poseY(W[3], -8.96, gy + .12, -.7, Math.PI, 'talk', T); P.cam.yaw += dt * .1; P.cam.dist -= dt * .4; }}; }}"""
# c5 the seller behind the counter talks to camera
C5 = f"""() => {{ const P = window.__pulau, W = window.__W(), s = W[3]; window.__time('siang'); const gy = {G}(-9.5, -1);
  window.__look(-8.96, -.8, PI + .3, .13, 2.7, false); window.__camTarget = {V}(-8.96, gy + 1.25, -.8);
  window.__beforeRender = (dt, T) => {{ window.__hideNear(-9.5, -1, 4, [s]); window.__poseY(s, -8.96, gy + .12, -.7, PI + .25, T < 2.4 ? 'talk' : 'wave', T); P.cam.dist -= dt * .1; }}; }}"""
# c6 pos ronda reveal (day): two residents playing checkers on the platform, one strikes the kentongan
C6 = f"""() => {{ const P = window.__pulau, W = window.__W(); window.__time('siang'); {SIT} const gy = {G}(-5, -1);
  window.__look(-5.2, -1.4, -2.2, .3, 5.5, false); window.__camTarget = {V}(-5.2, gy + .9, -1.4);
  window.__beforeRender = (dt, T) => {{ window.__hideNear(-5, -1.5, 4.5, [W[0], W[1]]); window.__sit(W[0], -4.6, 'sittalk', T, PI + .3); window.__sit(W[1], -5.5, 'sit', T + 1, PI - .3); P.cam.yaw += dt * .09; P.cam.dist -= dt * .35; }}; }}"""
# c7 the vice president sentences the president to night watch, pointing at the hut
C7 = f"""() => {{ const P = window.__pulau, vp = window.__VP(), pr = window.__PR(); window.__time('siang'); const gy = {G}(-4.4, -2.4);
  window.__look(-4.1, -2.45, -1.9, .2, 4.0, false); window.__camTarget = {V}(-4.1, gy + 1.1, -2.45);
  window.__beforeRender = (dt, T) => {{ window.__hideNear(-4.5, -2, 4.5, [vp, pr]); window.__pose(vp, -3.7, -2.9, -.66, T < 1.4 ? 'talk' : 'point', T); window.__pose(pr, -4.4, -2.0, -1.9, T < .8 ? 'idle' : 'panic', T); P.cam.dist -= dt * .15; }}; }}"""
# c8 the president on the hut with a coffee, bargaining
C8 = f"""() => {{ const P = window.__pulau, pr = window.__PR(); window.__time('siang'); {SIT} const gy = {G}(-5, -1);
  window.__look(-4.9, -1.5, PI + .35, .13, 2.6, false); window.__camTarget = {V}(-4.9, gy + 1.05, -1.5);
  window.__beforeRender = (dt, T) => {{ window.__hideNear(-5, -1, 4, [pr]); window.__sit(pr, -4.9, T < 1.8 ? 'sittalk' : 'sipcup', T); P.cam.dist -= dt * .1; }}; }}"""
# c9 night: the main street with the lamps, camera gliding south toward the sea
C9 = f"""() => {{ const P = window.__pulau; window.__time('malam'); window.__look(-1, 2, PI - .1, .5, 11, false); window.__camTarget = {V}(-1, {G}(-1, 2) + .6, 2);
  window.__beforeRender = (dt, T) => {{ window.__camTarget.z += dt * 2.6; P.player.z = window.__camTarget.z; P.cam.yaw -= dt * .03; }}; }}"""
# c10 night: the president asleep on the hut, a resident bangs the kentongan
C10 = f"""() => {{ const P = window.__pulau, pr = window.__PR(), W = window.__W(); window.__time('malam'); {SIT} const gy = {G}(-5, -1);
  window.__look(-5.4, -1.5, -2.25, .24, 4.6, false); window.__camTarget = {V}(-5.4, gy + 1.0, -1.5);
  window.__beforeRender = (dt, T) => {{ window.__hideNear(-5, -1.5, 4.5, [pr, W[2]]); window.__sit(pr, -5.0, T < 3.2 ? 'sleep' : 'panic', T); window.__pose(W[2], -6.35, -1.75, Math.PI / 2, 'strike', T); P.cam.dist -= dt * .08; }}; }}"""
# c11 night: Aru on Pulau Seberang, looking west at the lit island
C11 = f"""() => {{ const P = window.__pulau, B = P.I2.LM2.beach, x = B[0] + 2.5 - 32 + 128, z = B[1] + .5 - 32 - 34; window.__time('malam'); window.__look(x, z, 1.57 + .45, .16, 3.2, true);
  window.__beforeRender = (dt, T) => {{ P.player.obj.rotation.y = -Math.PI / 2 - .2; P.cam.dist -= dt * .12; }}; }}"""
# c12 end: night aerial over the lit town, pulling out
C12 = f"""() => {{ const P = window.__pulau; window.__time('malam'); window.__look(-3, 2, .65, .8, 13, false); window.__camTarget = {V}(-3, {G}(-3, 2), 2);
  window.__beforeRender = (dt) => {{ P.cam.yaw += dt * .05; P.cam.dist += dt * 1.6; }}; }}"""
SHOTS = {'c1': (C1, 140), 'c3a': (C3A, 150), 'c3b': (C3B, 62), 'c4': (C4, 155), 'c5': (C5, 160), 'c6': (C6, 150), 'c7': (C7, 115),
         'c8': (C8, 125), 'c9': (C9, 165), 'c10': (C10, 150), 'c11': (C11, 120), 'c12': (C12, 215)}
CLEAR = "() => { window.__cheer = null; window.__camTarget = null; window.__beforeRender = null; }"
async def run(which):
    async with async_playwright() as p:
        b, pg = await setup(p)
        await pg.evaluate(BASE)
        for k, (js, n) in SHOTS.items():
            if k in which and 'prev' not in which:
                await shoot(pg, 'e10' + k, n, start_js=js, warm=12)
                await pg.evaluate(CLEAR)
        if 'prev' in which:
            for k, (js, n) in SHOTS.items():
                if 'all' not in which and k not in which: continue
                await shoot(pg, 'p10' + k, 1, start_js=js, warm=int(os.environ.get('WARM', '40')))
                await pg.evaluate(CLEAR)
        await b.close()
if __name__ == "__main__": asyncio.run(run(sys.argv[1].split(",")))
