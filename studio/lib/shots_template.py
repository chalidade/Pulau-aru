"""Shot list template (episode 6). Copy to studio/episodes/epN/shots.py, rename shot folders eNcX, edit.
usage: DPR=2 python3 shots.py c1,c2,...   (DPR=1 + a 'prev' entry for quick single-frame checks)
"""
import asyncio, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'lib'))
from harness import *
BASE = """() => { const P = window.__pulau, S = P.app.S;
  window.__look = (x, z, yaw, pitch, dist, show) => { const pl = P.player; pl.x = x; pl.z = z; pl.tx = null; pl.vy = 0; pl.obj.visible = !!show; P.cam.yaw = yaw; P.cam.pitch = pitch; P.cam.dist = dist; P.cam.target.set(x, 1, z); };
  window.__ep6 = (stage) => {   // 0 = before (dirt paths, two houses still being built), 1 = after
    S.buildings = S.buildings.filter(b => !b.ep6);
    S.roads = null; S.construct = [];
    if (stage >= 1) {
      S.roads = { by: 'EN17', ep: 6 };
      S.buildings.push({ type: 'rumah', x: 55, y: 69, r: 0, by: '', ep: 6, ep6: 1 }, { type: 'rumah', x: 64, y: 59, r: 0, by: '', ep: 6, ep6: 1 });
      S.construct = [{ type: 'sekolah', by: 'junaa_yuds', ep: 6 }, { type: 'apotik', by: 'junaa_yuds', ep: 6 }];
    }
    if (stage >= 2) S.buildings.push({ type: 'masjid', x: window.__mx || 59, y: window.__my || 45, r: 0, by: 'Etet_443', ep: 6, ep6: 1 });
    P.applyWorld(false);
  };
}"""
C8 = """() => { window.__ep6(2); const P = window.__pulau, WD = P.WD, cx0 = (window.__mx || 59) + 2 - 56, cz0 = (window.__my || 45) + 2 - 56;
  // find a clear spot near the mosque with no trees between the camera and the pair
  const trees = WD.trees.map(t => [WD.cx2w(t.x), WD.cy2w(t.y)]).filter(([x, z]) => Math.hypot(x - cx0, z - cz0) > 3.2);
  const segD = (px, pz, ax, az, bx, bz) => { const vx = bx - ax, vz = bz - az, t = Math.max(0, Math.min(1, ((px - ax) * vx + (pz - az) * vz) / (vx * vx + vz * vz))); return Math.hypot(px - ax - vx * t, pz - az - vz * t); };
  let best = null;
  for (let r = 4.2; r <= 7.5; r += .5) for (let k = 0; k < 36; k++) { const ang = k / 36 * Math.PI * 2, px = cx0 + Math.sin(ang) * r, pz = cz0 + Math.cos(ang) * r, cx = px + Math.sin(ang) * 4.4, cz = pz + Math.cos(ang) * 4.4;
    if (WD.groundY(px, pz) < .5 || WD.groundY(cx, cz) < .3) continue;
    const bad = trees.filter(([x, z]) => segD(x, z, px, pz, cx, cz) < 2.0).length + trees.filter(([x, z]) => segD(x, z, px, pz, cx0, cz0) < 1.2).length * .5;
    const score = bad * 10 + Math.abs(WD.groundY(px, pz) - WD.groundY(cx, cz)) + r * .3;
    if (!best || score < best.score) best = { score, px, pz, ang }; }
  window.__c8 = best; const mx = best.px, mz = best.pz, yawC = best.ang;
  const W8 = P.npcs.filter(n => n.role === 'wander' && n.num), a = W8[0], b = W8[1]; window.__pair = [a, b];
  window.__look(mx, mz, yawC, .22, 4.0, false); window.__camTarget = new a.obj.position.constructor(mx, P.WD.groundY(mx, mz) + 1.25, mz);
  window.__beforeRender = (dt, T) => {
    const g = P.WD.groundY(mx, mz);
    const sx = Math.cos(yawC) * .5, sz = -Math.sin(yawC) * .5; a.x = mx - sx; a.z = mz - sz; b.x = mx + sx; b.z = mz + sz; a.obj.position.set(a.x, P.WD.groundY(a.x, a.z), a.z); b.obj.position.set(b.x, P.WD.groundY(b.x, b.z), b.z);
    a.obj.rotation.y = Math.atan2(b.x - a.x, b.z - a.z) + .35; b.obj.rotation.y = Math.atan2(a.x - b.x, a.z - b.z) - .35; a.tx = b.tx = null; a.wait = b.wait = 99;
    for (const n of P.npcs) if (n !== a && n !== b) n.obj.visible = Math.hypot(n.x - mx, n.z - mz) > 4;
    for (const [n, on] of [[a, (window.__spk || 0) === 0], [b, (window.__spk || 0) === 1]]) { const u = n.obj.userData; u.legL.rotation.x = u.legR.rotation.x = 0; u.armR.rotation.x = on ? -1.1 + Math.sin(T * 7) * .4 : -.15; u.armL.rotation.x = on ? -.6 + Math.sin(T * 5) * .2 : -.15; u.body.position.y = 0; }
  }; }"""
async def run(which):
    async with async_playwright() as p:
        b, pg = await setup(p)
        await pg.evaluate(BASE)
        if 'test' in which:
            await pg.evaluate("() => window.__ep6(2)")
            print(await pg.evaluate("() => { const P = window.__pulau; return [P.roads.children.length, P.roads.children[0] && P.roads.children[0].userData.count, P.acts.spots.build.map(s => s.cx + ',' + s.cy).filter((v, i, a) => a.indexOf(v) === i)]; }"))
            await shoot(pg, 't6a', 1, start_js="() => { window.__look(-2, 2, .3, 1.25, 46, false); }", warm=40)
            await shoot(pg, 't6b', 1, start_js="() => { window.__look(5, -9, .5, .55, 16, false); }", warm=30)
        if 'c1' in which:  # before: dirt paths, two houses still being built
            await shoot(pg, 'e6c1', 207, start_js="""() => { window.__ep6(0); window.__look(-1, 6, .35, 1.0, 44, false); window.__beforeRender = (dt) => { const c = window.__pulau.cam; c.yaw += dt * .05; c.dist -= dt * 1.0; }; }""", warm=20)
        if 'c2' in which:  # the president: the island must be tidy
            await shoot(pg, 'e6c2', 189, start_js="""() => { window.__ep6(0); const P = window.__pulau, n = P.npcs.find(n => n.pres); window.__cheer = false;
              window.__look(n.x, n.z, n.spot.face + .3, .95, 6.6, false); window.__camTarget = new n.obj.position.constructor(n.x, n.obj.position.y + .9, n.z + .5);
              window.__beforeRender = (dt) => { window.__camTarget.set(n.x, n.obj.position.y + .9, n.z + .5); P.cam.dist -= dt * .25; }; }""",
              per_frame_js="(f) => { window.__cheer = f >= 160; }", warm=12)
            await pg.evaluate("() => { window.__cheer = null; window.__camTarget = null; window.__beforeRender = null; }")
        if 'c4' in which:  # paving: the asphalt spreads out from the stage; then a resident on the new road
            await shoot(pg, 'e6c4', 228, start_js="""() => { window.__ep6(1); const P = window.__pulau; window.__roadReveal = 0; P.roads.userData.reveal(0);
              window.__look(-3, 4, .35, 1.12, 40, false); window.__beforeRender = (dt) => { P.cam.yaw += dt * .04; }; }""",
              per_frame_js="""(f) => { const P = window.__pulau; if (f <= 105) { window.__roadReveal = f / 105; P.roads.userData.reveal(window.__roadReveal); }
                if (f === 114) { const L = P.npcs.filter(n => n.role === 'listen'), n = L[L.length - 3]; window.__who = n; window.__look(n.x, n.z, n.spot.face + .7, .42, 4.2, false); window.__camTarget = new n.obj.position.constructor(n.x, n.obj.position.y + .8, n.z);
                  window.__beforeRender = (dt, T) => { const u = n.obj.userData; n.obj.rotation.y = n.spot.face + .7 + Math.sin(T * .9) * .2; u.armR.rotation.x = -1.2 + Math.sin(T * 6) * .4; u.armL.rotation.x = -.4; }; } }""", warm=12)
            await pg.evaluate("() => { window.__roadReveal = null; window.__camTarget = null; window.__beforeRender = null; }")
        if 'c5' in which:  # a finished house, then the new site with its sign
            await shoot(pg, 'e6c5', 222, start_js="""() => { window.__ep6(1); const P = window.__pulau; window.__look(0, 14, .6, .48, 9, false); window.__camTarget = new P.cam.target.constructor(0, 1.5, 14);
              window.__beforeRender = (dt) => { P.cam.yaw += dt * .12; }; }""",
              per_frame_js="""(f) => { if (f !== 111) return; const P = window.__pulau, sp = P.acts.spots.build[0], x = P.WD.cx2w(sp.cx), z = P.WD.cy2w(sp.cy);
                window.__look(x, z, .9, .5, 8.5, false); window.__camTarget.set(x + .6, 1.4, z + .6); window.__beforeRender = (dt) => { P.cam.yaw += dt * .06; }; }""", warm=12)
            await pg.evaluate("() => { window.__camTarget = null; window.__beforeRender = null; }")
        if 'c6' in which:  # the president decrees a mosque
            await shoot(pg, 'e6c6', 201, start_js="""() => { window.__ep6(1); const P = window.__pulau, n = P.npcs.find(n => n.pres); window.__cheer = false;
              window.__look(n.x, n.z, n.spot.face - .35, .9, 6.2, false); window.__camTarget = new n.obj.position.constructor(n.x, n.obj.position.y + .9, n.z + .5);
              window.__beforeRender = (dt) => { window.__camTarget.set(n.x, n.obj.position.y + .9, n.z + .5); }; }""", warm=12)
            await pg.evaluate("() => { window.__camTarget = null; window.__beforeRender = null; }")
        if 'c7' in which:  # the mosque, orbiting
            await shoot(pg, 'e6c7', 135, start_js="""() => { window.__ep6(2); const P = window.__pulau, x = (window.__mx || 59) + 2 - 56, z = (window.__my || 45) + 2 - 56;
              window.__look(x, z, .2, .38, 13, false); window.__camTarget = new P.cam.target.constructor(x, P.WD.groundY(x, z) + 2.0, z);
              window.__beforeRender = (dt) => { P.cam.yaw += dt * .16; P.cam.dist -= dt * .5; }; }""", warm=12)
            await pg.evaluate("() => { window.__camTarget = null; window.__beforeRender = null; }")
        if 'c8' in which:  # two residents grumbling on the new road, the mosque behind them
            await shoot(pg, 'e6c8', 225, start_js=C8, per_frame_js="(f) => { window.__spk = f < 108 ? 0 : 1; }", warm=12)
            await pg.evaluate("() => { window.__camTarget = null; window.__beforeRender = null; }")
        if 'c9' in which:  # after: asphalt roads, two new houses, the mosque, the new sites
            await shoot(pg, 'e6c9', 207, start_js="""() => { window.__ep6(2); window.__look(1, 2, -.3, .92, 50, false); window.__beforeRender = (dt) => { window.__pulau.cam.yaw += dt * .05; }; }""", warm=20)
        if 'c8t' in which:
            await shoot(pg, 'c8t', 1, start_js=C8, warm=12)
        if 'prev' in which:
            for nm, js, pf, fr in [('p4', "() => { window.__ep6(1); window.__look(-3, 4, .35, 1.12, 40, false); window.__pulau.roads.userData.reveal(.55); }", 0, 1),
                                   ('p5', "() => { const P = window.__pulau, sp = P.acts.spots.build[0], x = P.WD.cx2w(sp.cx), z = P.WD.cy2w(sp.cy); window.__look(x, z, .9, .5, 8.5, false); }", 0, 1),
                                   ('p7', "() => { window.__ep6(2); const P = window.__pulau, x = 5, z = -9; window.__look(x, z, .2, .38, 13, false); }", 0, 1),
                                   ('p9', "() => { window.__look(1, 2, -.3, .92, 50, false); }", 0, 1)]:
                await shoot(pg, nm, fr, start_js=js, warm=30)
        await b.close()
if __name__ == "__main__": asyncio.run(run(sys.argv[1].split(",")))
