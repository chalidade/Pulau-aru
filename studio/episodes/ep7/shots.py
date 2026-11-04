"""Episode 7 "Warteg & Rumah Sakit" shot list.  usage: DPR=2 python3 shots.py c1,c3,...  (DPR=1 + prev for checks)
World: warteg fp (59..60, 79..80) centre (4, 24), front faces north (-z); rumah sakit fp (62..65, 79..81) centre (8, 24.5);
rumah presiden fp (49..51, 47..50) centre (-5, -6.5), front faces east (+x); sekolah (-5, 16) faces east, apotik (2, 15) faces west.
"""
import asyncio, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'lib'))
from harness import *
BASE = """() => { const P = window.__pulau;
  window.__look = (x, z, yaw, pitch, dist, show) => { const pl = P.player; pl.x = x; pl.z = z; pl.tx = null; pl.vy = 0; pl.obj.visible = !!show; P.cam.yaw = yaw; P.cam.pitch = pitch; P.cam.dist = dist; P.cam.target.set(x, 1, z); };
  window.__W = () => P.npcs.filter(n => n.role === 'wander' && n.num);
  // hold an npc at (x, z) facing `face`; pose: 'eat' | 'talk' | 'belly' | 'walk' | 'idle'
  window.__pose = (n, x, z, face, pose, T) => { n.x = x; n.z = z; n.tx = null; n.wait = 99; n.obj.position.set(x, P.WD.groundY(x, z) + (pose === 'sit' ? -.22 : 0), z); n.obj.rotation.y = face; const u = n.obj.userData;
    u.legL.rotation.x = u.legR.rotation.x = 0; u.armL.rotation.x = u.armR.rotation.x = -.15; u.body.position.y = 0; u.body.rotation.z = 0;
    if (pose === 'eat') { u.armR.rotation.x = -1.3 + Math.sin(T * 8) * .45; u.armL.rotation.x = -.8; }
    if (pose === 'talk') { u.armR.rotation.x = -1.1 + Math.sin(T * 7) * .4; u.armL.rotation.x = -.6 + Math.sin(T * 5) * .2; }
    if (pose === 'belly') { u.armR.rotation.x = u.armL.rotation.x = -.75; u.body.rotation.z = Math.sin(T * 2.2) * .14; u.body.position.y = Math.abs(Math.sin(T * 4.4)) * .03; }
    if (pose === 'walk') { u.legL.rotation.x = Math.sin(T * 9) * .6; u.legR.rotation.x = -u.legL.rotation.x; u.armL.rotation.x = -u.legL.rotation.x * .7; u.armR.rotation.x = u.legL.rotation.x * .7; }
    if (pose === 'sit') { u.legL.rotation.x = u.legR.rotation.x = -1.4; } };
  window.__hideNear = (x, z, r, keep) => { for (const n of P.npcs) if (!keep.includes(n)) n.obj.visible = Math.hypot(n.x - x, n.z - z) > r; };
}"""
V = "new window.__pulau.cam.target.constructor"
C1 = f"""() => {{ const P = window.__pulau, W = window.__W(), doc = W[0]; window.__look(8, 22.6, 3.1, .34, 7.2, false); window.__camTarget = {V}(8, P.WD.groundY(8, 22.6) + 1.9, 23.4);
  window.__beforeRender = (dt, T) => {{ window.__hideNear(8, 22.5, 3.5, [doc]); window.__pose(doc, 8.75, 22.75, 3.14 + Math.sin(T * .8) * .9, 'idle', T); P.cam.dist -= dt * .35; }}; }}"""
C3 = f"""() => {{ const P = window.__pulau, W = window.__W(), a = W[1], b = W[2], s = W[3]; window.__look(4, 22.2, 2.85, .32, 5.0, false); window.__camTarget = {V}(4, P.WD.groundY(4, 23) + 1.0, 23.4);
  window.__beforeRender = (dt, T) => {{ window.__hideNear(4, 22.5, 3.6, [a, b, s]); window.__pose(a, 3.6, 22.8, Math.PI - .4, 'eat', T); window.__pose(b, 4.55, 22.8, Math.PI + .4, 'eat', T + 1.3); window.__pose(s, 4.0, 24.35, 0, 'talk', T); P.cam.yaw += dt * .05; }}; }}"""
C4 = f"""() => {{ const P = window.__pulau; window.__look(6.5, 23, 2.6, .55, 13, false); window.__camTarget = {V}(6.5, P.WD.groundY(6.5, 23) + 1.6, 23.8);
  window.__beforeRender = (dt) => {{ P.cam.yaw += dt * .1; P.cam.dist -= dt * .4; }}; }}"""
C5 = f"""() => {{ const P = window.__pulau, n = P.npcs.find(n => n.pres); window.__cheer = false;
  window.__look(n.x, n.z, n.spot.face + .3, .9, 6.0, false); window.__camTarget = {V}(n.x, n.obj.position.y + .9, n.z + .5);
  window.__beforeRender = (dt) => {{ window.__camTarget.set(n.x, n.obj.position.y + .9, n.z + .5); P.cam.dist -= dt * .3; }}; }}"""
C6 = f"""() => {{ const P = window.__pulau; window.__look(-4, -6.5, 1.3, .5, 17, false); window.__camTarget = {V}(-5, P.WD.groundY(-5, -6.5) + 1.6, -6.5);
  window.__beforeRender = (dt) => {{ P.cam.yaw += dt * .12; P.cam.dist -= dt * .9; }}; }}"""
C7 = f"""() => {{ const P = window.__pulau; window.__look(-1.5, 15.5, 1.57, .85, 17, false); window.__beforeRender = (dt) => {{ P.cam.yaw += dt * .06; P.cam.dist -= dt * .9; }}; }}"""
C8 = f"""() => {{ const P = window.__pulau, W = window.__W(), a = W[1], b = W[2]; window.__look(4.3, 22.6, 2.9, .25, 4.6, false); window.__camTarget = {V}(4.3, P.WD.groundY(4.3, 22.8) + 1.0, 22.9);
  window.__beforeRender = (dt, T) => {{ window.__hideNear(4, 22.5, 3.6, [a, b]); window.__pose(a, 4.3, 22.8, Math.PI + .2, 'belly', T); window.__pose(b, 6.5, 23.2, Math.PI - .3, 'eat', T); P.cam.dist -= dt * .12; }}; }}"""
C9 = f"""() => {{ const P = window.__pulau, W = window.__W(), a = W[1], doc = W[0]; window.__walk = 0; window.__look(6, 21.4, 3.0, .5, 9.5, false); window.__camTarget = {V}(6, P.WD.groundY(6, 22.5) + 1.2, 23);
  window.__beforeRender = (dt, T) => {{ window.__walk = Math.min(1, window.__walk + dt / 4.2); const k = window.__walk, x = 4.05 + (7.6 - 4.05) * k, z = 22.6 + Math.sin(k * Math.PI) * -.5;
    window.__hideNear(6, 22.5, 4.5, [a, doc]); window.__pose(a, x, z, k < 1 ? Math.PI / 2 + .2 : Math.PI, k < 1 ? 'walk' : 'belly', T);
    window.__pose(doc, 8.3, 22.75, k < .6 ? Math.PI : -Math.PI / 2 - .4, k > .8 ? 'talk' : 'idle', T); P.cam.yaw += dt * .03; }}; }}"""
SHOTS = {'c1': (C1, 170), 'c3': (C3, 150), 'c4': (C4, 175), 'c5': (C5, 105), 'c6': (C6, 95), 'c7': (C7, 140), 'c8': (C8, 145), 'c9': (C9, 270)}
async def run(which):
    async with async_playwright() as p:
        b, pg = await setup(p)
        await pg.evaluate(BASE)
        for k, (js, n) in SHOTS.items():
            if k in which and 'prevs' not in which:
                await shoot(pg, 'e7' + k, n, start_js=js, warm=12, per_frame_js="(f) => { window.__cheer = f >= 60 ? true : false; }" if k == 'c5' else None)
                await pg.evaluate("() => { window.__cheer = null; window.__camTarget = null; window.__beforeRender = null; }")
        if 'prev' in which or 'prevs' in which:
            for k, (js, n) in SHOTS.items():
                if 'prevs' in which and k not in which: continue
                await shoot(pg, 'p7' + k, 1, start_js=js, warm=40)
                await pg.evaluate("() => { window.__cheer = null; window.__camTarget = null; window.__beforeRender = null; }")
        await b.close()
if __name__ == "__main__": asyncio.run(run(sys.argv[1].split(",")))
