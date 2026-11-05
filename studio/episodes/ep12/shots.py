"""Episode 12 "Aru Pulang" shot list.  usage: DPR=2 python3 shots.py c1,c2,...  (DPR=1 + prev for checks)
World: gapura (53..56, 94) centre (-1, 38.5), front (+z) faces the pier; tiang salam (57, 95) at (1.5, 39.5);
Aru's boat lands on the beach east of the pier at about (3.7, 42.6); the big ship is moored at (-.5, 47.2).
Aru is the player character here (setup picks Aru), posed through window.__ARU.
"""
import asyncio, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'lib'))
from harness import *
BASE = """() => { const P = window.__pulau; window.PI = Math.PI;
  window.__look = (x, z, yaw, pitch, dist, show) => { const pl = P.player; pl.x = x; pl.z = z; pl.tx = null; pl.vy = 0; pl.obj.visible = !!show; P.cam.yaw = yaw; P.cam.pitch = pitch; P.cam.dist = dist; P.cam.target.set(x, 1, z); };
  window.__W = () => P.npcs.filter(n => n.num && !n.pres && !n.vp);
  window.__VP = () => P.npcs.find(n => n.vp); window.__PR = () => P.npcs.find(n => n.pres);
  const scene = P.roads.parent; const B = {}; scene.traverse(o => { if (o.userData && o.userData.b && !B[o.userData.b.type]) B[o.userData.b.type] = o; });
  const L = o => (lx, ly, lz) => [o.position.x + lx, o.position.y + ly, o.position.z + lz];
  window.__lL = L(B.ladang); window.__pL = L(B.pospantai); window.__gL = L(B.gapura); window.__tL = L(B.tiangsalam); window.__bL = L(B.bakarikan);
  window.__ARU = { obj: P.player.obj };
  // a fishing boat with a lantern far out at sea (for the night shots), hidden until __boat(true)
  const boat = B.perahu.clone(); boat.visible = false; scene.add(boat); let lm = null; B.pospantai.traverse(o => { if (o.isMesh && o.material.emissive && o.material.emissiveIntensity > 1.5) lm = o; });
  const lamp = lm.clone(); lamp.material = lm.material.clone(); lamp.material.color.set('#ffd56a'); lamp.material.emissive.set('#ffc34a'); lamp.material.emissiveIntensity = 3; lamp.scale.set(.35, .35, .35); lamp.visible = false; scene.add(lamp);
  window.__boat = (on, x = 14, z = 52, T = 0, ry = 2.3) => { boat.visible = lamp.visible = on; boat.position.set(x, Math.sin(T * 1.3) * .06, z); boat.rotation.y = ry + Math.sin(T * .8) * .03; lamp.position.set(x + Math.cos(ry) * .75, .75 + Math.sin(T * 1.3) * .06, z - Math.sin(ry) * .75); };
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
# boat path: from far out (8.5, 51) to the beach (3.7, 42.6), heading north-west; k in 0..1
BOAT = "const bp = k => { const e = 1 - (1 - Math.min(1, Math.max(0, k))) ** 2; return [8.5 + (3.7 - 8.5) * e, 51 + (42.6 - 51) * e]; }, BRY = 2.09;"
# c1 cold open: the guard on the beach shouting, Aru's boat coming in behind him
C1 = f"""() => {{ const P = window.__pulau, g = window.__W()[5], A = window.__ARU; {BOAT} window.__time('siang'); const gx = 2.7, gz = 38.6, gy = {G}(gx, gz);
  window.__look(gx, gz, Math.PI + .35, .1, 3.1, false); window.__camTarget = {V}(gx, gy + 1.0, gz + .4);
  window.__beforeRender = (dt, T) => {{ const [bx, bz] = bp(.55 + T * .05); window.__boat(true, bx, bz, T, BRY); window.__hideNear(gx, gz, 4, [g]);
    window.__poseY(g, gx, gy, gz, Math.PI + .35, T < 1.2 ? 'point' : 'panic', T); window.__poseY(A, bx, .25, bz, Math.PI - .4, 'wave', T); P.cam.dist -= dt * .12; }}; }}"""
# c3 the gate from the pier side, camera rising
C3 = f"""() => {{ const P = window.__pulau, W = window.__W(), [x, y, z] = window.__gL(0, 0, 0); window.__time('siang');
  window.__look(x, z, .12, .02, 7.5, false); window.__camTarget = {V}(x, y + 2.2, z);
  window.__beforeRender = (dt, T) => {{ window.__hideNear(x, z, 5, [W[0], W[1]]); const k = (T + .4) * .45;
    window.__pose(W[0], x - .5, z - 2 + k, 0, 'walk', T * 1.4); window.__pose(W[1], x + .4, z - 2.6 + k, 0, 'walk', T * 1.4 + 1);
    P.cam.pitch += dt * .05; P.cam.dist -= dt * .35; }}; }}"""
# c4 the back of the gate from town: a resident points at "semoga selalu baik-baik saja"
C4 = f"""() => {{ const P = window.__pulau, W = window.__W(), a = W[2], [x, y, z] = window.__gL(0, 0, 0); window.__time('siang');
  window.__look(x, z - 2, Math.PI + .5, .14, 4.4, false); window.__camTarget = {V}(x, y + 2.0, z - .5);
  window.__beforeRender = (dt, T) => {{ window.__hideNear(x, z, 5, [a]); window.__pose(a, x + .55, z - 1.4, -.35 + Math.PI, T < .6 ? 'idle' : 'point', T);
    a.obj.rotation.y = .25; P.cam.yaw -= dt * .05; P.cam.dist -= dt * .15; }}; }}"""
# c5 the signpost: orbit close, BOGOR points out to sea
C5 = f"""() => {{ const P = window.__pulau, [x, y, z] = window.__tL(0, 0, 0); window.__time('siang');
  window.__look(x, z, 1.15, .12, 3.4, false); window.__camTarget = {V}(x, y + 2.35, z);
  window.__beforeRender = (dt, T) => {{ window.__hideNear(x, z, 3, []); P.cam.yaw += dt * .14; P.cam.dist -= dt * .12; }}; }}"""
# c6 the president at the signpost, saluting toward the sea
C6 = f"""() => {{ const P = window.__pulau, pr = window.__PR(), [x, y, z] = window.__tL(0, 0, 0); window.__time('siang');
  window.__look(x - .2, z + .5, -.55, .14, 3.4, false); window.__camTarget = {V}(x - .3, y + 1.35, z + .4);
  window.__beforeRender = (dt, T) => {{ window.__hideNear(x, z, 3.5, [pr]); window.__pose(pr, x - .5, z + .75, -.55, T < 2.2 ? 'talk' : 'wave', T); P.cam.dist -= dt * .1; }}; }}"""
# c7 wide: the boat glides in past the moored ship, the gate behind
C7 = f"""() => {{ const P = window.__pulau, A = window.__ARU; {BOAT} window.__time('siang');
  window.__look(2.6, 42, Math.PI - .6, .42, 10.5, false); window.__camTarget = {V}(2.6, .6, 42);
  window.__beforeRender = (dt, T) => {{ const [bx, bz] = bp(.45 + (T + .4) * .1); window.__boat(true, bx, bz, T, BRY); window.__poseY(A, bx, .25, bz, Math.PI - .4, 'idle', T);
    window.__camTarget.set(bx * .5 + 1.3, .6, bz * .5 + 20.5); P.cam.dist -= dt * .5; }}; }}"""
# c8 close: Aru waving from the boat at the beach
C8 = f"""() => {{ const P = window.__pulau, A = window.__ARU, W = window.__W(); {BOAT} window.__time('siang');
  window.__look(3.7, 42.6, Math.PI - .6, .1, 2.7, false); window.__camTarget = {V}(3.7, 1.3, 42.6);
  window.__beforeRender = (dt, T) => {{ const [bx, bz] = bp(.97 + (T + .4) * .01); window.__boat(true, bx, bz, T, BRY); window.__hideNear(bx, bz, 3, []);
    window.__poseY(A, bx, .25, bz, Math.PI - .25, 'wave', T); window.__camTarget.set(bx, 1.3, bz); P.cam.dist -= dt * .1; }}; }}"""
# c9 under the gate: Aru walks into town, the vice president and residents cheer
C9 = f"""() => {{ const P = window.__pulau, A = window.__ARU, vp = window.__VP(), W = window.__W(), [x, y, z] = window.__gL(0, 0, 0); window.__time('siang');
  window.__look(x, z - 2, Math.PI + .2, .14, 6.0, false); window.__camTarget = {V}(x, y + 1.3, z - .8);
  window.__beforeRender = (dt, T) => {{ const az = z + 1.4 - (T + .4) * .5, ay = {G}(x, az); window.__hideNear(x, z, 6, [vp, W[0], W[1], W[2], W[3]]);
    window.__poseY(A, x, ay, az, Math.PI, 'walk', T); window.__pose(vp, x - .9, z - 2.0, .5, T < 2.6 ? 'talk' : 'cheer', T);
    window.__pose(W[0], x + 1.5, z - 2.0, -.6, 'cheer', T); window.__pose(W[1], x - 1.6, z - 2.6, .5, 'cheer', T + .3); window.__pose(W[2], x + 2.3, z - 2.7, -.8, 'wave', T); window.__pose(W[3], x - 2.4, z - 1.9, .8, 'cheer', T + .6);
    P.cam.dist -= dt * .2; }}; }}"""
# c10 the president at the fish grill, declaring the welcome party
C10 = f"""() => {{ const P = window.__pulau, pr = window.__PR(), [x, y, z] = window.__bL(0, 0, 0); window.__time('siang');
  window.__look(x - 1.0, z + 1.1, -.6, .16, 3.0, false); window.__camTarget = {V}(x - 1.0, y + .75, z + 1.1);
  window.__beforeRender = (dt, T) => {{ window.__hideNear(x, z, 3.5, [pr]); window.__pose(pr, x - 1.0, z + 1.1, -.6, T < 2.4 ? 'talk' : 'cheer', T); P.cam.dist -= dt * .1; }}; }}"""
# c11 aerial: the gate, the pier and the town, pulling out
C11 = f"""() => {{ const P = window.__pulau, A = window.__ARU, [x, y, z] = window.__gL(0, 0, 0); window.__time('siang');
  window.__look(x, z, .5, .85, 9, false); window.__camTarget = {V}(x + .5, y, z);
  window.__beforeRender = (dt, T) => {{ window.__boat(true, 3.7, 42.6, T, 2.09); P.cam.dist += dt * 2.6; P.cam.yaw += dt * .05; }}; }}"""
# c12 night: Aru alone by the campfire, holding a letter
C12 = f"""() => {{ const P = window.__pulau, A = window.__ARU, f = P.LM.fire, fx = f[0] - 56 + .5, fz = f[1] - 56 + .5; window.__time('malam');
  const ax = fx - .9, az = fz + .2, ay = {G}(ax, az);
  window.__look(ax, az, .6, .14, 2.6, false); window.__camTarget = {V}(ax, ay + 1.0, az);
  window.__beforeRender = (dt, T) => {{ window.__hideNear(fx, fz, 4, []); window.__poseY(A, ax, ay, az, .7, 'sipcup', T); P.cam.dist -= dt * .1; }}; }}"""
# c13 night end: the lit gate and the sea, slowly rising
C13 = f"""() => {{ const P = window.__pulau, [x, y, z] = window.__gL(0, 0, 0); window.__time('malam');
  window.__look(x, z, Math.PI + .25, .2, 7, false); window.__camTarget = {V}(x, y + 2.2, z);
  window.__beforeRender = (dt, T) => {{ window.__hideNear(x, z, 5, []); P.cam.pitch += dt * .03; P.cam.dist += dt * .5; P.cam.yaw += dt * .03; }}; }}"""
SHOTS = {'c1': (C1, 115), 'c3': (C3, 138), 'c4': (C4, 162), 'c5': (C5, 152), 'c6': (C6, 142), 'c7': (C7, 104), 'c8': (C8, 110),
         'c9': (C9, 144), 'c10': (C10, 164), 'c11': (C11, 180), 'c12': (C12, 150), 'c13': (C13, 175)}
CLEAR = "() => { window.__cheer = null; window.__camTarget = null; window.__beforeRender = null; window.__boat(false); }"
async def run(which):
    async with async_playwright() as p:
        b, pg = await setup(p)
        await pg.evaluate(BASE)
        for k, (js, n) in SHOTS.items():
            if k in which and 'prev' not in which:
                await shoot(pg, 'e12' + k, n, start_js=js, warm=12)
                await pg.evaluate(CLEAR)
        if 'prev' in which:
            for k, (js, n) in SHOTS.items():
                if 'all' not in which and k not in which: continue
                await shoot(pg, 'p12' + k, 1, start_js=js, warm=int(os.environ.get('WARM', '40')))
                await pg.evaluate(CLEAR)
        await b.close()
if __name__ == "__main__": asyncio.run(run(sys.argv[1].split(",")))
