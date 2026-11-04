"""Episode 8 "Waterpark & Ikan Bakar" shot list.  usage: DPR=2 python3 shots.py c1,c3,...  (DPR=1 + prev for checks)
World: waterpark fp (62..67, 47..50) centre (9, -7), slide helix in local metres (BT.waterpark.slide);
bakar ikan fp (56..57, 89..90) centre (1, 34), front faces west (-x); papan semangat (58..59, 42) centre (3, -13.5) faces south.
Aru stands on Pulau Seberang west of the stone circle (134.5, -35.5), looking west.
"""
import asyncio, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'lib'))
from harness import *
BASE = """() => { const P = window.__pulau;
  window.__look = (x, z, yaw, pitch, dist, show) => { const pl = P.player; pl.x = x; pl.z = z; pl.tx = null; pl.vy = 0; pl.obj.visible = !!show; P.cam.yaw = yaw; P.cam.pitch = pitch; P.cam.dist = dist; P.cam.target.set(x, 1, z); };
  window.__W = () => P.npcs.filter(n => n.role === 'wander' && n.num);
  window.__VP = () => P.npcs.find(n => n.vp); window.__PR = () => P.npcs.find(n => n.pres);
  const scene = P.roads.parent; let wp = null; scene.traverse(o => { if (o.userData && o.userData.b && o.userData.b.type === 'waterpark') wp = o; });
  window.__wp = wp; window.__wpL = (lx, ly, lz) => [wp.position.x + lx, wp.position.y + ly, wp.position.z + lz];
  window.__poseY = (n, x, y, z, face, pose, T) => { n.x = x; n.z = z; n.tx = null; n.wait = 99; n.obj.visible = true; n.obj.position.set(x, y, z); n.obj.rotation.y = face; const u = n.obj.userData;
    u.legL.rotation.x = u.legR.rotation.x = 0; u.armL.rotation.x = u.armR.rotation.x = -.15; u.body.position.y = 0; u.body.rotation.z = 0;
    if (pose === 'eat') { u.armR.rotation.x = -1.3 + Math.sin(T * 8) * .45; u.armL.rotation.x = -.8; }
    if (pose === 'talk') { u.armR.rotation.x = -1.1 + Math.sin(T * 7) * .4; u.armL.rotation.x = -.6 + Math.sin(T * 5) * .2; }
    if (pose === 'wave') { u.armR.rotation.x = -2.6 + Math.sin(T * 9) * .35; u.armL.rotation.x = -.3; }
    if (pose === 'cheer') { u.armR.rotation.x = u.armL.rotation.x = -2.8 + Math.sin(T * 10) * .2; u.body.position.y = Math.abs(Math.sin(T * 6)) * .08; }
    if (pose === 'swim') { u.armR.rotation.x = -1.6 + Math.sin(T * 6) * .5; u.armL.rotation.x = -1.6 - Math.sin(T * 6) * .5; }
    if (pose === 'sit') { u.legL.rotation.x = u.legR.rotation.x = -1.4; u.armR.rotation.x = u.armL.rotation.x = -2.7; } };
  window.__pose = (n, x, z, face, pose, T, dy = 0) => window.__poseY(n, x, P.WD.groundY(x, z) + dy, z, face, pose, T);
  window.__hideNear = (x, z, r, keep) => { for (const n of P.npcs) if (!keep.includes(n)) n.obj.visible = Math.hypot(n.x - x, n.z - z) > r; };
  // water splash: white droplets cloned from a duck sphere
  const proto = []; wp.traverse(o => { if (o.isMesh && o.geometry.type === 'SphereGeometry' && !proto.length) proto.push(o); });
  const dm = proto[0].material.clone(); dm.color.set('#e8f8ff'); dm.transparent = true; dm.opacity = .9; dm.emissive && dm.emissive.set('#9fdcf0');
  window.__drops = []; for (let i = 0; i < 22; i++) { const m = proto[0].clone(); m.material = dm; m.visible = false; scene.add(m); window.__drops.push(m); }
  window.__splash = (x, y, z, k) => { window.__drops.forEach((m, i) => { const a = i * 2.4, sp = .9 + (i % 5) * .35, up = 2.2 + (i % 4) * .7, t = k * 1.1;
    const yy = y + up * t - 4.9 * t * t; m.visible = k > 0 && k < 1 && yy > y - .05; m.position.set(x + Math.cos(a) * sp * t, yy, z + Math.sin(a) * sp * t); m.scale.setScalar(.07 + (i % 3) * .03); }); };
}"""
V = "new window.__pulau.cam.target.constructor"
WPAT = """const S = window.__pulau.app && 0, SL = { cx: -1, cz: -.2, r: 1.25, a0: Math.PI, a1: Math.PI * 2.25, y0: 2.4, y1: .35 };
  const slideAt = t => { const a = SL.a0 + (SL.a1 - SL.a0) * t; return window.__wpL(SL.cx + Math.cos(a) * SL.r, SL.y0 + (SL.y1 - SL.y0) * t + .06, SL.cz + Math.sin(a) * SL.r); };"""
# c1 cold open: the vice president on top of the slide tower, waving down
C1 = f"""() => {{ const P = window.__pulau, vp = window.__VP(), [tx, ty, tz] = window.__wpL(-2.25, 2.52, -.25);
  window.__look(tx, tz, .55, .12, 3.4, false); window.__camTarget = {V}(tx, ty + 1.0, tz);
  window.__beforeRender = (dt, T) => {{ window.__poseY(vp, tx, ty, tz, .55, T < 1.4 ? 'wave' : 'talk', T); P.cam.dist -= dt * .25; P.cam.yaw += dt * .04; }}; }}"""
# c3a the cheer billboard, slow push
C3A = f"""() => {{ const P = window.__pulau, W = window.__W(); window.__cheer = true; window.__look(3, -13.4, .18, .16, 5.6, false); window.__camTarget = {V}(3, P.WD.groundY(3, -13.5) + 1.55, -13.5);
  window.__beforeRender = (dt, T) => {{ window.__hideNear(3, -12.5, 2.4, []); [W[0], W[1], W[2]].forEach((n, i) => window.__pose(n, 1.9 + i * 1.1, -11.6 + (i % 2) * .3, Math.PI, 'cheer', T + i)); P.cam.dist -= dt * .3; }}; }}"""
# c3b the crowd at the stage cheering
C3B = f"""() => {{ const P = window.__pulau, W = window.__W(); window.__cheer = true; window.__look(1.0, -11.0, .35, .55, 7.5, false); window.__camTarget = {V}(1.0, P.WD.groundY(1, -11) + 1.0, -11.0);
  window.__beforeRender = (dt, T) => {{ for (let i = 0; i < 8; i++) window.__pose(W[i], -.6 + (i % 4) * 1.0, -10.2 + Math.floor(i / 4) * 1.0, Math.PI - .3, 'cheer', T + i * .7); P.cam.dist -= dt * .4; }}; }}"""
# c4 waterpark reveal: aerial orbit, swimmers in the pool
C4 = f"""() => {{ const P = window.__pulau, W = window.__W(), [cx, cy, cz] = window.__wpL(0, 0, 0); window.__look(cx, cz, .25, .78, 15, false); window.__camTarget = {V}(cx, cy + .5, cz);
  window.__beforeRender = (dt, T) => {{ window.__hideNear(cx, cz, 4, W.slice(3, 7)); [[.5, .5], [1.6, -.4], [2.3, .9]].forEach(([x, z], i) => {{ const p = window.__wpL(x, -.35 + Math.sin(T * 2 + i) * .03, z); window.__poseY(W[3 + i], p[0], p[1], p[2], i * 2.1 + T * .3, 'swim', T + i); }});
    {{ const p = window.__wpL(-1.95, .22, 1.2); window.__poseY(W[6], p[0], p[1], p[2], Math.PI, 'idle', T); }}
    P.cam.yaw += dt * .09; P.cam.dist -= dt * .7; P.cam.pitch -= dt * .02; }}; }}"""
# c5 a resident in the pool next to the giant duck
C5 = f"""() => {{ const P = window.__pulau, W = window.__W(), a = W[3], [px, py, pz] = window.__wpL(1.15, -.42, .55); window.__look(px, pz, .3, .22, 3.6, false); window.__camTarget = {V}(px + .35, py + 1.25, pz);
  window.__beforeRender = (dt, T) => {{ window.__hideNear(px, pz, 3, [a]); window.__poseY(a, px, py + Math.sin(T * 2) * .025, pz, .3, 'talk', T); P.cam.dist -= dt * .12; }}; }}"""
# c6 the fish grill by the pier, push in from the street
C6 = f"""() => {{ const P = window.__pulau, W = window.__W(), s = W[0]; window.__look(1, 34, -1.3, .3, 5.2, false); window.__camTarget = {V}(1, P.WD.groundY(1, 34) + .9, 34);
  window.__beforeRender = (dt, T) => {{ window.__hideNear(1, 34, 3.5, [s]); window.__pose(s, 1.85, 34.0, -Math.PI / 2, 'eat', T); P.cam.dist -= dt * .4; P.cam.yaw -= dt * .06; }}; }}"""
C7 = f"""() => {{ const P = window.__pulau, W = window.__W(), s = W[0]; window.__look(-.1, 33.7, -1.9, .2, 3.0, false); window.__camTarget = {V}(-.1, P.WD.groundY(-.1, 33.7) + 1.15, 33.7);
  window.__beforeRender = (dt, T) => {{ window.__hideNear(1, 34, 3.5, [s]); window.__pose(s, -.1, 33.7, -1.9, 'talk', T); P.cam.dist -= dt * .1; }}; }}"""
C8 = f"""() => {{ const P = window.__pulau, W = window.__W(), s = W[0], pr = window.__PR(); window.__look(-.1, 34.3, -1.95, .2, 2.9, false); window.__camTarget = {V}(-.1, P.WD.groundY(-.1, 34.3) + 1.15, 34.3);
  window.__beforeRender = (dt, T) => {{ window.__hideNear(1, 34, 3.5, [s, pr]); window.__pose(s, 1.85, 34.0, -Math.PI / 2, 'idle', T); window.__pose(pr, -.1, 34.3, -1.95, T < 1.6 ? 'eat' : 'talk', T); P.cam.dist -= dt * .12; }}; }}"""
# c9a the lighthouse, slow orbit
C9A = f"""() => {{ const P = window.__pulau, L = P.LM.light, x = L[0] + 1 - 56, z = L[1] + 1 - 56; window.__look(x, z, 2.2, .3, 9, false); window.__camTarget = {V}(x, P.WD.groundY(x, z) + 3.2, z);
  window.__beforeRender = (dt) => {{ P.cam.yaw += dt * .1; P.cam.dist -= dt * .3; }}; }}"""
# c9b Aru on Pulau Seberang, looking west across the sea
C9B = f"""() => {{ const P = window.__pulau, B = P.I2.LM2.beach, x = B[0] + 2.5 - 32 + 128, z = B[1] + .5 - 32 - 34; window.__look(x, z, 1.57 + .45, .18, 3.4, true);
  window.__beforeRender = (dt, T) => {{ P.player.obj.rotation.y = -Math.PI / 2 - .2; P.cam.dist -= dt * .15; }}; }}"""
# c10 payoff: the vice president slides down and splashes; the president watches from the deck
C10 = f"""() => {{ const P = window.__pulau, vp = window.__VP(), pr = window.__PR(), W = window.__W(); {WPAT}
  const [cx, cy, cz] = window.__wpL(-.3, 0, 0); window.__look(cx, cz, .42, .42, 8.0, false); window.__camTarget = {V}(cx, cy + 1.3, cz);
  window.__beforeRender = (dt, T) => {{ window.__hideNear(cx, cz, 4.5, [vp, pr]); const k = Math.min(1, Math.max(0, (T - .15) / 1.15));
    if (k < 1) {{ const p = slideAt(k), q = slideAt(Math.min(1, k + .02)); window.__poseY(vp, p[0], p[1], p[2], Math.atan2(q[0] - p[0], q[2] - p[2]), 'sit', T); }}
    else {{ const p = window.__wpL(1.15, -.45 + Math.sin(T * 2) * .03, 1.0); window.__poseY(vp, p[0], p[1], p[2], .4, T < 2.6 ? 'swim' : 'wave', T); }}
    const s = window.__wpL(1.05, .16, .95); window.__splash(s[0], s[1], s[2], (T - 1.3) / .9);
    const q = window.__wpL(-.15, .12, 1.7); window.__poseY(pr, q[0], q[1], q[2], .5, T < 2.0 ? 'idle' : 'talk', T);
    P.cam.dist -= dt * .35; }}; }}"""
# c11 end: wide aerial over the new waterpark and the town
C11 = f"""() => {{ const P = window.__pulau, [cx, cy, cz] = window.__wpL(-3, 0, 2); window.__look(cx, cz, .6, .95, 30, false); window.__camTarget = {V}(cx, cy, cz);
  window.__beforeRender = (dt) => {{ P.cam.yaw += dt * .06; P.cam.dist += dt * 1.2; }}; }}"""
SHOTS = {'c1': (C1, 104), 'c3a': (C3A, 168), 'c3b': (C3B, 108), 'c4': (C4, 196), 'c5': (C5, 132), 'c6': (C6, 122), 'c7': (C7, 132),
         'c8': (C8, 128), 'c9a': (C9A, 166), 'c9b': (C9B, 96), 'c10': (C10, 178), 'c11': (C11, 190)}
CLEAR = "() => { window.__cheer = null; window.__camTarget = null; window.__beforeRender = null; window.__splash && window.__splash(0, 0, 0, -1); }"
async def run(which):
    async with async_playwright() as p:
        b, pg = await setup(p)
        await pg.evaluate(BASE)
        for k, (js, n) in SHOTS.items():
            if k in which and 'prev' not in which:
                await shoot(pg, 'e8' + k, n, start_js=js, warm=12)
                await pg.evaluate(CLEAR)
        if 'prev' in which:
            for k, (js, n) in SHOTS.items():
                if 'all' not in which and k not in which: continue
                await shoot(pg, 'p8' + k, 1, start_js=js, warm=int(os.environ.get('WARM', '40')))
                await pg.evaluate(CLEAR)
        await b.close()
if __name__ == "__main__": asyncio.run(run(sys.argv[1].split(",")))
