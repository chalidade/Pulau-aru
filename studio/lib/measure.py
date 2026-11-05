"""Size of every building model (w x height x d, metres) next to a person (~1.46 m). usage: DPR=1 python3 measure.py"""
import asyncio, sys, json, os
sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
from harness import *
async def main():
    async with async_playwright() as p:
        b, pg = await setup(p)
        r = await pg.evaluate("""async () => { const M = await import('/src/models.js'); const THREE = await import('three'); const out = {};
          for (const [k, d] of Object.entries(M.BT)) { try { const g = M.buildBuilding({ type: k, x: 0, y: 0, r: 0 }); const bb = new THREE.Box3().setFromObject(g); const s = bb.getSize(new THREE.Vector3()); out[k] = [d.n, d.w, d.h, +s.x.toFixed(2), +s.y.toFixed(2), +s.z.toFixed(2), d.scale || 1]; } catch (e) { out[k] = String(e); } }
          const ch = M.makeCharacter(M.ARU); const bb = new THREE.Box3().setFromObject(ch); out._human = bb.getSize(new THREE.Vector3()).y; return out; }""")
        print(json.dumps(r, ensure_ascii=False, indent=0))
        await b.close()
asyncio.run(main())
