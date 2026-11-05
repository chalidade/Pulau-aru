"""Episode 11 "Ladang Wapres & Penjaga Pantai" shot list.  usage: DPR=2 python3 shots.py c1,c2,...  (DPR=1 + prev for checks)
World: ladang cells (68..75, 44..49) r0 centre (16, -9), gate faces south; lapangan sekolah (44..48, 69..72) centre (-9.5, 15);
pos penjaga pantai (58..60, 92..93) centre (3.5, 37), faces the sea (+z); tower platform local (.95, 1.56, -.3).
"""
import asyncio, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'lib'))
from harness import *
BASE = """() => { const P = window.__pulau; window.PI = Math.PI;
  window.__look = (x, z, yaw, pitch, dist, show) => { const pl = P.player; pl.x = x; pl.z = z; pl.tx = null; pl.vy = 0; pl.obj.visible = !!show; P.cam.yaw = yaw; P.cam.pitch = pitch; P.cam.dist = dist; P.cam.target.set(x, 1, z); };
  window.__W = () => P.npcs.filter(n => n.role === 'wander' && n.num);
  window.__VP = () => P.npcs.find(n => n.vp); window.__PR = () => P.npcs.find(n => n.pres);
  const scene = P.roads.parent; const B = {}; scene.traverse(o => { if (o.userData && o.userData.b && !B[o.userData.b.type]) B[o.userData.b.type] = o; });
  const L = o => (lx, ly, lz) => [o.position.x + lx, o.position.y + ly, o.position.z + lz];
  window.__lL = L(B.ladang); window.__fL = L(B.lapangansekolah); window.__pL = L(B.pospantai);
  // a fishing boat with a lantern far out at sea (for the night shots), hidden until __boat(true)
  const boat = B.perahu.clone(); boat.visible = false; scene.add(boat); let lm = null; B.pospantai.traverse(o => { if (o.isMesh && o.material.emissive && o.material.emissiveIntensity > 1.5) lm = o; });
  const lamp = lm.clone(); lamp.material = lm.material.clone(); lamp.material.color.set('#ffd56a'); lamp.material.emissive.set('#ffc34a'); lamp.material.emissiveIntensity = 3; lamp.scale.set(.35, .35, .35); lamp.visible = false; scene.add(lamp);
  window.__boat = (on, x = 14, z = 52, T = 0) => { boat.visible = lamp.visible = on; boat.position.set(x, Math.sin(T * 1.3) * .06, z); boat.rotation.y = 2.3 + Math.sin(T * .8) * .05; lamp.position.set(x, 1.5 + Math.sin(T * 1.3) * .06, z); };
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

# c1 cold open: the vice president in his new farm, furious about a missing mango
C1 = f"""() => {{ const P = window.__pulau, vp = window.__VP(), [x, y, z] = window.__lL(-1.9, 0, -1.3); window.__time('siang');
  window.__look(x, z, .3, .18, 3.3, false); window.__camTarget = {V}(x, y + 1.15, z);
  window.__beforeRender = (dt, T) => {{ window.__hideNear(x, z, 3, [vp]); window.__poseY(vp, x, y + .06, z, .3, T < 1.6 ? 'talk' : 'point', T); P.cam.dist -= dt * .2; }}; }}"""
# c2 the vice president at the farm gate, under the LADANG BUAH sign
C2 = f"""() => {{ const P = window.__pulau, vp = window.__VP(), [x, y, z] = window.__lL(0, 0, 3.6);
  window.__look(x, z - .6, -.6, .36, 4.0, false); window.__camTarget = {V}(x, y + 1.2, z - .4);
  window.__beforeRender = (dt, T) => {{ window.__hideNear(x, z, 3, [vp]); window.__pose(vp, x, z, -.5, 'talk', T); P.cam.dist -= dt * .25; }}; }}"""
# c3 the visitors' beds: plants growing from seed to fruit while the camera orbits
C3 = f"""() => {{ const P = window.__pulau, [x, y, z] = window.__lL(2.0, 0, .05), K = P.kebun;
  window.__look(x, z, .55, .62, 5.2, false); window.__camTarget = {V}(x, y + .3, z);
  window.__beforeRender = (dt, T) => {{ const k = Math.max(0, T + .4) * .19, c = v => Math.min(1, v);
    K.__demo([['cabai', c(.05 + k)], ['jagung', c(.0 + k * .9)], ['semangka', c(.2 + k * .8)], ['pisang', c(.1 + k)], ['mangga', c(k * .85)], ['cabai', c(.3 + k)]]);
    window.__hideNear(x, z, 3.2, []); P.cam.yaw += dt * .12; P.cam.dist -= dt * .25; }}; }}"""
# c4 the school field, aerial orbit, kids running
C4 = f"""() => {{ const P = window.__pulau, W = window.__W(), [x, y, z] = window.__fL(0, 0, 0);
  window.__look(x, z, .5, .78, 10.5, false); window.__camTarget = {V}(x, y + .3, z);
  window.__beforeRender = (dt, T) => {{ window.__hideNear(x, z, 4, W.slice(0, 3)); for (let i = 0; i < 3; i++) {{ const a = T * .9 + i * 2.1, px = x - .3 + Math.cos(a) * 1.3, pz = z + .1 + Math.sin(a) * .8;
      window.__pose(W[i], px, pz, a + Math.PI, 'walk', T * 1.5 + i); }} P.cam.yaw += dt * .1; P.cam.dist -= dt * .5; }}; }}"""
# c5 a resident on the new swing
C5 = f"""() => {{ const P = window.__pulau, W = window.__W(), a = W[3], [x, y, z] = window.__fL(-1.4, 0, 1.65);
  window.__look(x, z, 1.25, .2, 3.4, false); window.__camTarget = {V}(x, y + .85, z);
  window.__beforeRender = (dt, T) => {{ window.__hideNear(x, z, 3, [a]); const s = Math.sin(T * 2.6);
    window.__poseY(a, x, y + .1 + Math.abs(s) * .1, z + s * .35, Math.PI / 2 + .4 - Math.PI / 2, 'sittalk', T); P.cam.dist -= dt * .1; }}; }}"""
# c6 the beach guard post, from the sea side; the new guard on the tower
C6 = f"""() => {{ const P = window.__pulau, W = window.__W(), g = W[5], [x, y, z] = window.__pL(.2, 0, .2), t = window.__pL(.95, 1.56, -.3);
  window.__look(x, z, .35, .26, 7.2, false); window.__camTarget = {V}(x, y + 1.5, z);
  window.__beforeRender = (dt, T) => {{ window.__hideNear(x, z, 4, [g]); window.__poseY(g, t[0], t[1], t[2], .1, T > 2.4 ? 'wave' : 'idle', T); P.cam.dist -= dt * .45; P.cam.yaw -= dt * .03; }}; }}"""
# c7 close on the guard waving, residents cheering below
C7 = f"""() => {{ const P = window.__pulau, W = window.__W(), g = W[5], t = window.__pL(.95, 1.56, -.3);
  window.__look(t[0], t[2], .2, .04, 2.7, false); window.__camTarget = {V}(t[0], t[1] + 1.25, t[2]);
  window.__beforeRender = (dt, T) => {{ window.__hideNear(t[0], t[2], 3, [g]); window.__poseY(g, t[0], t[1], t[2], .2, 'wave', T); P.cam.dist -= dt * .1; }}; }}"""
# c8 the guard walks through the farm looking for the mango thief
C8 = f"""() => {{ const P = window.__pulau, W = window.__W(), g = W[5], [x0, y, z0] = window.__lL(-1.6, 0, 2.1);
  window.__look(x0, z0 - 1, -1.0, .55, 4.0, false); window.__camTarget = {V}(x0, y + 1.0, z0);
  window.__beforeRender = (dt, T) => {{ const k = Math.max(0, T + .4) / 4, zz = z0 - k * 2.6, xx = x0 + Math.sin(k * 6) * .25;
    window.__hideNear(x0, z0 - 1.5, 3.5, [g]); window.__pose(g, xx, zz, Math.PI + Math.cos(k * 6) * .3, 'walk', T); window.__camTarget.set(xx, y + 1.0, zz); P.cam.yaw += dt * .05; }}; }}"""
# c9 caught: the president under the mango tree, mouth full; guard points, vice president panics
C9 = f"""() => {{ const P = window.__pulau, pr = window.__PR(), vp = window.__VP(), g = window.__W()[5], [x, y, z] = window.__lL(-1.9, 0, -1.55);
  window.__look(x + .3, z + .3, -.5, .2, 4.3, false); window.__camTarget = {V}(x + .35, y + 1.05, z + .3);
  window.__beforeRender = (dt, T) => {{ window.__hideNear(x, z, 3.5, [pr, vp, g]);
    window.__poseY(pr, x, y + .06, z, .25, T < .9 ? 'eat' : T < 3.3 ? 'talk' : 'panic', T);
    window.__poseY(g, x + 1.15, y + .06, z + .55, -1.9, 'point', T);
    window.__poseY(vp, x - .95, y + .06, z + .6, 1.5, T > 3.2 ? 'point' : 'idle', T); P.cam.dist -= dt * .15; }}; }}"""
# c10 night: from behind the guard on the tower, a boat lantern far out at sea
C10 = f"""() => {{ const P = window.__pulau, g = window.__W()[5], [x, y, z] = window.__pL(.6, 0, .2), t = window.__pL(.95, 1.56, -.3); window.__time('malam');
  window.__look(x, z, .2, .24, 6.4, false); window.__camTarget = {V}(x, y + 1.7, z);
  window.__beforeRender = (dt, T) => {{ window.__boat(true, 14, 52, T); window.__hideNear(x, z, 4, [g]); window.__poseY(g, t[0], t[1], t[2], .62, 'point', T); P.cam.dist -= dt * .35; P.cam.yaw += dt * .05; }}; }}"""
# c11 night: the boat with its lantern, slowly closer (end card)
C11 = f"""() => {{ const P = window.__pulau; window.__time('malam');
  window.__look(14, 52, -2.4, .32, 9.0, false); window.__camTarget = {V}(14, 1.0, 52);
  window.__beforeRender = (dt, T) => {{ window.__boat(true, 14, 52, T); P.cam.dist -= dt * .35; P.cam.yaw += dt * .04; }}; }}"""
SHOTS = {'c1': (C1, 99), 'c2': (C2, 145), 'c3': (C3, 214), 'c4': (C4, 124), 'c5': (C5, 153), 'c6': (C6, 172), 'c7': (C7, 89),
         'c8': (C8, 127), 'c9': (C9, 156), 'c10': (C10, 140), 'c11': (C11, 215)}
CLEAR = "() => { window.__cheer = null; window.__camTarget = null; window.__beforeRender = null; window.__boat(false); }"
async def run(which):
    async with async_playwright() as p:
        b, pg = await setup(p)
        await pg.evaluate(BASE)
        for k, (js, n) in SHOTS.items():
            if k in which and 'prev' not in which:
                await shoot(pg, 'e11' + k, n, start_js=js, warm=12)
                await pg.evaluate(CLEAR)
        if 'prev' in which:
            for k, (js, n) in SHOTS.items():
                if 'all' not in which and k not in which: continue
                await shoot(pg, 'p11' + k, 1, start_js=js, warm=int(os.environ.get('WARM', '40')))
                await pg.evaluate(CLEAR)
        await b.close()
if __name__ == "__main__": asyncio.run(run(sys.argv[1].split(",")))
