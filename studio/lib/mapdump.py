"""Dump the island grid (tiles, trees, landmarks, buildings, pier, construction sites) to a planning image.
usage: python3 mapdump.py  -> $STUDIO_WORK/map.json and map.png (8 px per cell, grid every 10 cells, crop 15..105 x 25..110)
Use it before placing new buildings: put them on grass (tile 3), off roads, lined up along the streets.
"""
import asyncio, sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import *
from PIL import Image, ImageDraw
OUT = os.environ.get('STUDIO_WORK', '/tmp/studio')
async def main():
    async with async_playwright() as p:
        b, pg = await setup(p)
        d = await pg.evaluate("""() => { const P = window.__pulau, WD = P.WD; return { tile: Array.from(WD.tile), tree: Array.from(WD.treeAt).map(v => v >= 0 ? 1 : 0), LM: P.LM, PIER: WD.PIER, LMS: WD.LMS, S: P.app.S.buildings, roads: P.app.S.roads, sites: P.acts.spots.build.map(s => [s.cx, s.cy]) }; }""")
        await b.close()
    os.makedirs(OUT, exist_ok=True); json.dump(d, open(OUT + '/map.json', 'w'))
    W = 112; S = 8; im = Image.new('RGB', (W * S, W * S)); dr = ImageDraw.Draw(im)
    col = {0: (20, 60, 110), 1: (50, 120, 150), 2: (230, 210, 150), 3: (110, 180, 90), 4: (80, 140, 70)}
    for i, t in enumerate(d['tile']):
        x, y = i % W, i // W; c = col.get(t, (0, 0, 0))
        if d['tree'][i] and t >= 3: c = (40, 110, 50)
        dr.rectangle((x * S, y * S, x * S + S - 1, y * S + S - 1), fill=c)
    for sg in (d.get('roads') or {}).get('segments', []): dr.rectangle((sg[0] * S, sg[1] * S, (sg[2] + 1) * S - 1, (sg[3] + 1) * S - 1), fill=(60, 60, 66))
    for k, x, y, w, h in d['LMS']: dr.rectangle((x * S, y * S, (x + w) * S - 1, (y + h) * S - 1), outline=(255, 0, 0), width=2); dr.text((x * S, y * S - 10), k, fill=(255, 255, 255))
    for b in d['S']: dr.text((b['x'] * S, b['y'] * S), b['type'][:6], fill=(255, 255, 0)); dr.rectangle((b['x'] * S, b['y'] * S, b['x'] * S + 6, b['y'] * S + 6), fill=(255, 255, 0))
    p = d['PIER']; dr.rectangle((p['x'] * S, p['y0'] * S, p['x'] * S + S - 1, p['y1'] * S), fill=(140, 90, 40))
    for x, y in d['sites']: dr.rectangle(((x - 1) * S, (y - 1) * S, (x + 2) * S - 1, (y + 2) * S - 1), outline=(255, 0, 255), width=2)
    for g in range(0, W, 10): dr.line((g * S, 0, g * S, W * S), fill=(255, 255, 255)); dr.line((0, g * S, W * S, g * S), fill=(255, 255, 255)); dr.text((g * S + 2, 25 * S + 2), str(g), fill=(255, 255, 255)); dr.text((15 * S + 2, g * S + 2), str(g), fill=(255, 255, 255))
    im.crop((15 * S, 25 * S, 105 * S, 110 * S)).save(OUT + '/map.png'); print('wrote', OUT + '/map.png')
asyncio.run(main())
