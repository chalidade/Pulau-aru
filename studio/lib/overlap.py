"""Footprint clashes: buildings vs buildings, streets, landmarks, and water. usage: DPR=1 python3 overlap.py (only road x road should remain)"""
import asyncio, sys, json
sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
from harness import *
async def main():
    async with async_playwright() as p:
        b, pg = await setup(p)
        r = await pg.evaluate("""async () => { const M = await import('/src/models.js'); const P = window.__pulau, S = P.app.S, W = 112, WD = P.WD;
          const owner = new Map(), out = [];
          const fp = b => { const d = M.BT[b.type]; return (b.r | 0) % 2 ? [d.h, d.w] : [d.w, d.h]; };
          const mark = (x, y, who) => { const k = y * W + x; if (owner.has(k)) out.push(who + ' x ' + owner.get(k) + ' @' + x + ',' + y); else owner.set(k, who); };
          for (const [k, x, y, w, h] of WD.LMS) for (let j = 0; j < h; j++) for (let i = 0; i < w; i++) mark(x + i, y + j, 'LM:' + k);
          for (const sg of (S.roads.segments || [])) for (let y = sg[1]; y <= sg[3]; y++) for (let x = sg[0]; x <= sg[2]; x++) mark(x, y, 'road');
          S.buildings.forEach((b, i) => { const d = M.BT[b.type]; if (!d || d.float || d.water || d.arch) return; const [w, h] = fp(b); for (let j = 0; j < h; j++) for (let k = 0; k < w; k++) { mark(b.x + k, b.y + j, b.type + '#' + i); const t = WD.tile[(b.y + j) * W + b.x + k]; if (t < WD.SAND) out.push(b.type + '#' + i + ' on water @' + (b.x + k) + ',' + (b.y + j)); } });
          const agg = {}; for (const o of out) { const key = o.replace(/ @.*/, ''); agg[key] = (agg[key] || 0) + 1; } return agg; }""")
        print(json.dumps(r, indent=1))
        await b.close()
asyncio.run(main())
