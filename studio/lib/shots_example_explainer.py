import asyncio, sys
sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
from harness import *
BASE = """() => { const P = window.__pulau;
  window.__look = (x, z, yaw, pitch, dist, show) => { const pl = P.player; pl.x = x; pl.z = z; pl.tx = null; pl.vy = 0; pl.obj.visible = !!show; P.cam.yaw = yaw; P.cam.pitch = pitch; P.cam.dist = dist; P.cam.target.set(x, 1, z); };
  window.__V = (x, y, z) => new P.cam.target.constructor(x, y, z);
  window.__cw = c => [c[0] - 56 + .5, c[1] - 56 + .5];
}"""
WAVE = "const u = pl.obj.userData; u.armR.rotation.x = -2.6 + Math.sin(T * 7) * .35; u.armR.rotation.z = -.3;"
async def run(which):
    async with async_playwright() as p:
        b, pg = await setup(p)
        await pg.evaluate(BASE)
        if 'k1' in which:  # Aru waves hello at the camp
            await shoot(pg, 'k1', 117, start_js="() => { const P = window.__pulau, [x, z] = window.__cw(P.LM.camp); window.__look(x, z + 2.4, .25, .22, 4.4, true); const pl = P.player; pl.y = P.WD.groundY(x, z + 2.4); window.__camTarget = window.__V(x, pl.y + 1.1, z + 2.4); window.__beforeRender = (dt, T) => { pl.obj.rotation.y = .25; " + WAVE + " }; }", warm=15)
            await pg.evaluate("() => { window.__camTarget = null; window.__beforeRender = null; }")
        if 'k2' in which:  # the name stone, close
            await shoot(pg, 'k2', 228, start_js="() => { const P = window.__pulau, [x, z] = window.__cw(P.LM.stone); window.__look(x + .5, z, .15, .18, 5.5, false); window.__camTarget = window.__V(x + .5, P.WD.groundY(x, z) + 1.2, z); window.__beforeRender = (dt) => { P.cam.dist -= dt * .25; P.cam.yaw += dt * .04; }; }", warm=15)
            await pg.evaluate("() => { window.__camTarget = null; window.__beforeRender = null; }")
        if 'k3' in which:  # the village from above
            await shoot(pg, 'k3', 276, start_js="() => { window.__look(-1, 2, .3, .95, 40, false); window.__beforeRender = (dt) => { window.__pulau.cam.yaw += dt * .05; window.__pulau.cam.dist -= dt * .6; }; }", warm=15)
            await pg.evaluate("() => { window.__beforeRender = null; }")
        if 'k4' in which:  # president, then vice president
            await shoot(pg, 'k4', 232, start_js="""() => { const P = window.__pulau, n = P.npcs.find(n => n.pres), v = P.npcs.find(n => n.vp); window.__cheer = false;
              window.__look(n.x, n.z, n.spot.face + .3, .9, 6.4, false); window.__camTarget = window.__V(n.x, n.obj.position.y + .9, n.z + .5); window.__k4 = 0;
              window.__beforeRender = () => { const a = window.__k4 ? v : n; window.__camTarget.set(a.x, a.obj.position.y + .9, a.z + .5); window.__vpTalk = !!window.__k4; }; }""",
              per_frame_js="(f) => { if (f === 153) { const P = window.__pulau, n = P.npcs.find(n => n.pres); window.__k4 = 1; P.cam.yaw = n.spot.face - .4; P.cam.pitch = .95; P.cam.dist = 5.4; } }", warm=12)
            await pg.evaluate("() => { window.__camTarget = null; window.__beforeRender = null; window.__cheer = null; window.__vpTalk = null; }")
        if 'k5' in which:  # the cloud island, slow orbit from below the clouds
            await shoot(pg, 'k5', 351, start_js="""() => { const P = window.__pulau, n = P.npcs.find(n => n.cloud && n.cloud.kind === 'climb'), cl = n.cloud.cl, o = cl.queue[2];
              window.__look(o.x, o.z - 1.5, .9, .12, 17, false); window.__camTarget = window.__V(o.x, cl.top + 1.5, o.z - 1.5); window.__beforeRender = (dt) => { P.cam.yaw += dt * .09; }; }""", warm=12)
            await pg.evaluate("() => { window.__camTarget = null; window.__beforeRender = null; }")
        if 'k6' in which:  # the whole island
            await shoot(pg, 'k6', 201, start_js="() => { window.__look(2, 14, -.2, 1.05, 74, false); window.__beforeRender = (dt) => { window.__pulau.cam.yaw += dt * .04; }; }", warm=15)
            await pg.evaluate("() => { window.__beforeRender = null; }")
        if 'k7' in which:  # montage
            await shoot(pg, 'k7', 351, start_js="""() => { const P = window.__pulau, pl = P.player; window.__look(-1, -6, Math.PI + .25, .32, 5.5, true); pl.y = P.WD.groundY(-1, -6); pl.tx = -1; pl.tz = 8; window.__camTarget = null;
              window.__beforeRender = () => { if (window.__k7 === 0) { P.cam.target.set(pl.x, pl.y + 1, pl.z); } }; window.__k7 = 0; }""",
              per_frame_js="""(f) => { const P = window.__pulau, pl = P.player;
                if (f < 105) { if (pl.tx == null) { pl.tx = -1; pl.tz = 8; } return; }
                const cut = (k, fn) => { if (window.__k7 !== k) { window.__k7 = k; fn(); } };
                if (f < 145) cut(1, () => { const py = P.app.S.buildings.find(b => b.type === 'piramida'); const x = py.x - 5 + 6.5 - 56 + (py.big ? 5 : 0), z = py.y - 5 + 6.5 - 56 + (py.big ? 5 : 0); window.__look(x, z, .7, .32, 26, false); window.__camTarget = window.__V(x, 6, z); window.__beforeRender = (dt) => { P.cam.yaw += dt * .1; }; });
                else if (f < 198) cut(2, () => { const n = P.npcs.find(n => n.cloud && n.cloud.kind === 'climb'), a = n.cloud.cl.path[6]; window.__look(a.x, a.z, 2.3, .26, 15, false); window.__camTarget.set(a.x, a.y - .5, a.z); window.__beforeRender = (dt) => { P.cam.yaw += dt * .08; }; });
                else if (f < 237) cut(3, () => { const n = P.npcs.find(n => n.role === 'fish' && n.state === 'work') || P.npcs.find(n => n.role === 'fish'); window.__look(n.x, n.z, n.spot.face + 2.4, .35, 5, false); window.__camTarget.set(n.x + Math.sin(n.spot.face) * 1.2, n.obj.position.y + .7, n.z + Math.cos(n.spot.face) * 1.2); window.__beforeRender = null; });
                else if (f < 286) cut(4, () => { const s = P.sail; window.__look(s.x, s.z, 2.4, .3, 22, false); window.__camTarget.set(s.x, 1.5, s.z); window.__beforeRender = (dt) => { P.cam.yaw += dt * .12; }; });
                else cut(5, () => { const [x, z] = window.__cw(P.LM.stone); window.__look(x + .5, z, -.35, .2, 4.2, false); window.__camTarget.set(x + .5, P.WD.groundY(x, z) + 1.2, z); window.__beforeRender = null; }); }""", warm=12)
            await pg.evaluate("() => { window.__camTarget = null; window.__beforeRender = null; }")
        if 'k8' in which:  # Aru at the end of the pier waves goodbye
            await shoot(pg, 'k8', 150, start_js="() => { const P = window.__pulau, x = P.WD.PIER.x - 56 + .5, z = P.WD.PIER.y1 - 56 - .5, pl = P.player; window.__look(x, z, .35, .2, 5, true); pl.y = .3; window.__camTarget = window.__V(x, 1.4, z); window.__beforeRender = (dt, T) => { pl.y = .27; pl.obj.position.y = .27; pl.obj.rotation.y = .35; " + WAVE + " P.cam.dist += dt * 1.2; }; }", warm=15)
            await pg.evaluate("() => { window.__camTarget = null; window.__beforeRender = null; }")
        if 'prev' in which:
            for k, js in [('q1', "() => { const P = window.__pulau, [x, z] = window.__cw(P.LM.camp); window.__look(x, z + 2.4, .25, .22, 4.4, true); P.player.y = P.WD.groundY(x, z + 2.4); window.__camTarget = window.__V(x, P.player.y + 1.1, z + 2.4); }"),
                          ('q2', "() => { const P = window.__pulau, [x, z] = window.__cw(P.LM.stone); window.__look(x + .5, z, .15, .18, 5.5, false); window.__camTarget.set(x + .5, P.WD.groundY(x, z) + 1.2, z); }"),
                          ('q5', "() => { const P = window.__pulau, n = P.npcs.find(n => n.cloud && n.cloud.kind === 'climb'), cl = n.cloud.cl, o = cl.queue[2]; window.__look(o.x, o.z - 1.5, .9, .12, 17, false); window.__camTarget.set(o.x, cl.top + 1.5, o.z - 1.5); }"),
                          ('q8', "() => { const P = window.__pulau, x = P.WD.PIER.x - 56 + .5, z = P.WD.PIER.y1 - 56 - .5, pl = P.player; window.__look(x, z, .35, .2, 5, true); pl.y = .3; window.__camTarget.set(x, 1.4, z); }")]:
                await shoot(pg, k, 1, start_js=js, warm=25)
        await b.close()
if __name__ == "__main__": asyncio.run(run(sys.argv[1].split(",")))
