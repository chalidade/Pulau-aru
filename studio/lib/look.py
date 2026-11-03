"""Single-frame views of the live local game (quick visual checks before a full capture).
usage: DPR=1 python3 look.py name "x,z,yaw,pitch,dist" [name2 "..."]   -> $STUDIO_WORK/cap/<name>/0000.jpg
x,z are world coords (cell - 56 + .5); pitch ~1.0 = from above, ~0.3 = eye level.
"""
import asyncio, sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import *
async def main(args):
    async with async_playwright() as p:
        b, pg = await setup(p)
        await pg.evaluate("() => { const P = window.__pulau; window.__look = (x, z, yaw, pitch, dist, show) => { const pl = P.player; pl.x = x; pl.z = z; pl.tx = null; pl.vy = 0; pl.obj.visible = !!show; P.cam.yaw = yaw; P.cam.pitch = pitch; P.cam.dist = dist; P.cam.target.set(x, 1, z); }; }")
        for name, v in zip(args[0::2], args[1::2]):
            await shoot(pg, name, 1, start_js=f"() => window.__look({v}, false)", warm=40)
        await b.close()
asyncio.run(main(sys.argv[1:]))
