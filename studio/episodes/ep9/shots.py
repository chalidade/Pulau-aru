"""Episode 9 "Kantin Kejujuran" shot list.  usage: DPR=2 python3 shots.py c1,c3a,...  (DPR=1 + prev for checks)
World: kantin kejujuran cells (51..52, 65..66) r=3, centre (-4, 10), counter faces east (+x) at x ~ -3.1;
lampu semangat at cells x 53 / 56, y 56 63 68 75 82 (world x -2.5 / .5); main street world x -2..0.
Monumen Dermawan centre (3, -8). Waterpark helpers from ep 8.
"""
import asyncio, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'lib'))
from harness import *
BASE = """() => { const P = window.__pulau;
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
    if (pose === 'walk') { u.legL.rotation.x = Math.sin(T * 7) * .5; u.legR.rotation.x = -Math.sin(T * 7) * .5; u.armL.rotation.x = -Math.sin(T * 7) * .4; u.armR.rotation.x = Math.sin(T * 7) * .4; } };
  window.__pose = (n, x, z, face, pose, T, dy = 0) => window.__poseY(n, x, P.WD.groundY(x, z) + dy, z, face, pose, T);
  window.__hideNear = (x, z, r, keep) => { for (const n of P.npcs) if (!keep.includes(n)) n.obj.visible = Math.hypot(n.x - x, n.z - z) > r; };
}"""
V = "new window.__pulau.cam.target.constructor"
G = "window.__pulau.WD.groundY"
# c1 cold open: the president alone at the honesty canteen, hand on the gorengan, looking around
C1 = f"""() => {{ const P = window.__pulau, pr = window.__PR(); window.__time('siang'); const tx = -2.5, tz = 10.15;
  window.__look(tx, tz, 1.0, .16, 2.9, false); window.__camTarget = {V}(tx - .2, {G}(tx, tz) + 1.2, tz);
  window.__beforeRender = (dt, T) => {{ window.__hideNear(-3, 10, 4, [pr]); const look = T < 1.2 ? 1.0 + Math.sin(T * 5) * .6 : T < 2.6 ? -Math.PI / 2 + .5 : 1.0 + Math.sin(T * 4) * .5;
    window.__pose(pr, tx, tz, look, T < 2.6 ? 'reach' : 'talk', T); P.cam.dist -= dt * .2; P.cam.yaw += dt * .05; }}; }}"""
# c3a Monumen Dermawan with residents cheering in front
C3A = f"""() => {{ const P = window.__pulau, W = window.__W(); window.__time('siang'); window.__cheer = true; window.__look(3, -8, -.15, .32, 8.5, false); window.__camTarget = {V}(3, {G}(3, -8) + 1.6, -8);
  window.__beforeRender = (dt, T) => {{ window.__hideNear(3, -5.5, 2.5, []); [0, 1, 2, 3].forEach(i => window.__pose(W[i], 1.6 + i * .95, -5.3 + (i % 2) * .35, Math.PI, 'cheer', T + i)); P.cam.dist -= dt * .5; }}; }}"""
# c3b crowd at the stage cheering
C3B = f"""() => {{ const P = window.__pulau, W = window.__W(); window.__time('siang'); window.__cheer = true; window.__look(1.0, -11.0, .35, .55, 7.5, false); window.__camTarget = {V}(1.0, {G}(1, -11) + 1.0, -11.0);
  window.__beforeRender = (dt, T) => {{ for (let i = 0; i < 8; i++) window.__pose(W[i], -.6 + (i % 4) * 1.0, -10.2 + Math.floor(i / 4) * 1.0, Math.PI - .3, 'cheer', T + i * .7); P.cam.dist -= dt * .4; }}; }}"""
# c4 kantin reveal: slow orbit, two residents taking snacks
C4 = f"""() => {{ const P = window.__pulau, W = window.__W(); window.__time('siang'); window.__look(-3.6, 10, .75, .42, 7.2, false); window.__camTarget = {V}(-3.6, {G}(-3.6, 10) + 1.0, 10);
  window.__beforeRender = (dt, T) => {{ window.__hideNear(-3, 10, 5, [W[4], W[5]]); window.__pose(W[4], -2.45, 9.55, -Math.PI / 2, 'reach', T); window.__pose(W[5], -2.4, 10.6, -Math.PI / 2 - .3, 'eat', T + 1);
    P.cam.yaw += dt * .1; P.cam.dist -= dt * .35; }}; }}"""
# c5 a resident drops the money in the box, then talks to camera
C5 = f"""() => {{ const P = window.__pulau, W = window.__W(), a = W[5]; window.__time('siang'); const x = -2.45, z = 10.5;
  window.__look(x, z, 1.25, .17, 2.7, false); window.__camTarget = {V}(x - .25, {G}(x, z) + 1.2, z - .05);
  window.__beforeRender = (dt, T) => {{ window.__hideNear(-3, 10, 4, [a]); window.__pose(a, x, z, T < 1.4 ? -Math.PI / 2 : 1.1, T < 1.4 ? 'reach' : 'talk', T); P.cam.dist -= dt * .12; }}; }}"""
# c6 night: the main street with the new lamps, camera gliding north along it
C6 = f"""() => {{ const P = window.__pulau; window.__time('malam'); window.__look(-1, 22, -.12, .48, 11, false); window.__camTarget = {V}(-1, {G}(-1, 22) + .6, 22);
  window.__beforeRender = (dt, T) => {{ window.__camTarget.z -= dt * 2.6; P.player.z = window.__camTarget.z; P.cam.yaw += dt * .03; }}; }}"""
# c7 night: a resident under the first lamp (with Tiara's plaque) talking
C7 = f"""() => {{ const P = window.__pulau, W = window.__W(), a = W[2]; window.__time('malam'); const x = -1.85, z = .3;
  window.__look(x, z, .55, .14, 3.4, false); window.__camTarget = {V}(x - .3, {G}(x, z) + 1.35, z);
  window.__beforeRender = (dt, T) => {{ window.__hideNear(-2, .5, 3.5, [a]); window.__pose(a, x, z, .55, 'talk', T); P.cam.dist -= dt * .12; }}; }}"""
# c8 the vice president in the pool calling a cabinet meeting, two residents with him
C8 = f"""() => {{ const P = window.__pulau, W = window.__W(), vp = window.__VP(); window.__time('siang'); const [px, py, pz] = window.__wpL(1.15, -.42, .55);
  window.__look(px, pz, .3, .24, 4.2, false); window.__camTarget = {V}(px + .2, py + 1.2, pz);
  window.__beforeRender = (dt, T) => {{ window.__hideNear(px, pz, 3.5, [vp, W[6], W[7]]); window.__poseY(vp, px, py + Math.sin(T * 2) * .025, pz, .3, T < 1.9 ? 'talk' : 'swim', T);
    [[-.2, -.5], [2.2, .1]].forEach(([dx, dz], i) => {{ const p = window.__wpL(1.15 + dx, -.45 + Math.sin(T * 2 + i) * .02, .55 + dz); window.__poseY(W[6 + i], p[0], p[1], p[2], i ? -1.2 : 1.0, 'swim', T + i); }});
    P.cam.dist -= dt * .15; }}; }}"""
# c9a the vice president, dripping, catches the president at the canteen
C9A = f"""() => {{ const P = window.__pulau, vp = window.__VP(), pr = window.__PR(); window.__time('siang');
  window.__look(-1.95, 10.7, 1.2, .2, 4.8, false); window.__camTarget = {V}(-1.95, {G}(-1.95, 10.7) + 1.1, 10.7);
  window.__beforeRender = (dt, T) => {{ window.__hideNear(-3, 10, 4.5, [vp, pr]); window.__pose(pr, -2.5, 10.0, T < .5 ? -Math.PI / 2 : .1, T < .5 ? 'reach' : 'panic', T);
    const k = Math.min(1, T / .9); window.__pose(vp, -1.4, 12.2 - k * .9, Math.PI - .5, k < 1 ? 'walk' : 'point', T); P.cam.dist -= dt * .25; }}; }}"""
# c9b close on the president, flustered, paying double into the box
C9B = f"""() => {{ const P = window.__pulau, vp = window.__VP(), pr = window.__PR(); window.__time('siang'); const x = -2.5, z = 10.0;
  window.__look(x, z, 1.15, .15, 2.7, false); window.__camTarget = {V}(x - .1, {G}(x, z) + 1.2, z + .1);
  window.__beforeRender = (dt, T) => {{ window.__hideNear(-3, 10, 4.5, [vp, pr]); window.__pose(vp, -1.4, 11.3, Math.PI - .5, 'point', T);
    window.__pose(pr, x, z, T < 2.6 ? .9 : -Math.PI / 2 + .3, T < 2.6 ? 'panic' : 'reach', T); P.cam.dist -= dt * .1; }}; }}"""
# c10 end: night aerial over the lit street and the canteen, pulling out
C10 = f"""() => {{ const P = window.__pulau; window.__time('malam'); window.__look(-2, 9, .65, .8, 13, false); window.__camTarget = {V}(-2, {G}(-2, 9), 9);
  window.__beforeRender = (dt) => {{ P.cam.yaw += dt * .05; P.cam.dist += dt * 1.6; }}; }}"""
SHOTS = {'c1': (C1, 165), 'c3a': (C3A, 140), 'c3b': (C3B, 95), 'c4': (C4, 195), 'c5': (C5, 170), 'c6': (C6, 180), 'c7': (C7, 130),
         'c8': (C8, 115), 'c9a': (C9A, 120), 'c9b': (C9B, 155), 'c10': (C10, 200)}
CLEAR = "() => { window.__cheer = null; window.__camTarget = null; window.__beforeRender = null; }"
async def run(which):
    async with async_playwright() as p:
        b, pg = await setup(p)
        await pg.evaluate(BASE)
        for k, (js, n) in SHOTS.items():
            if k in which and 'prev' not in which:
                await shoot(pg, 'e9' + k, n, start_js=js, warm=12)
                await pg.evaluate(CLEAR)
        if 'prev' in which:
            for k, (js, n) in SHOTS.items():
                if 'all' not in which and k not in which: continue
                await shoot(pg, 'p9' + k, 1, start_js=js, warm=int(os.environ.get('WARM', '40')))
                await pg.evaluate(CLEAR)
        await b.close()
if __name__ == "__main__": asyncio.run(run(sys.argv[1].split(",")))
