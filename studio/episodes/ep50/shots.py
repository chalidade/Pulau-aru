"""Episode 50 "Gali Tambang, Nemu Sandal" shot list (format CERITA, run sore 21 Nov).  usage: DPR=2 python3 shots.py c1,c3,...  (DPR=1 + prev for checks)
Two real comments (komentar.md, collected via TikTok Studio 20 Nov): @revan.labublue "tambahin bandara sama penambangan" -> Tambang Pulau
(tambang x31 y69, west end of Jalan Warga) with Revan the miner; @l4.rean "aku mau jadi kepala desa" -> Kantor Kepala Desa (kantordesa x49
y79 r2, on the old kavling) and Pak Kades supervising the mine by the TEMUAN HARI INI board. The first cart brings out one blue sandal
(Rayhan's); whoyss peeks from behind the rocks. All of it is island.json state (live on the web); the cart cycle is live in main.js.
"""
import asyncio, sys, os, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'lib'))
from harness import *
def _mod(name, path):
    sp = importlib.util.spec_from_file_location(name, path); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m
E49 = _mod('ep49shots', os.path.join(HERE, '..', 'ep49', 'shots.py'))
CHAIN = E49.CHAIN + (E49.SETUP49,)
SETUP50 = """() => { const P = window.__pulau;
  const F = s => P.npcs.find(n => n.name === s || (n.name || '').startsWith(s));
  window.__REV = () => F('revan.labublue'); window.__KDS = () => F('l4.rean'); window.__WHO = () => F('whoyss');
  const B = {}; P.scene.traverse(o => { if (o.userData && o.userData.b && ['tambang', 'kantordesa'].includes(o.userData.b.type)) B[o.userData.b.type] = o; });
  window.__B50 = B;
  window.__fix50 = () => { window.__fix49();
    for (const f of [window.__REV, window.__KDS, window.__WHO]) { const n = f(); if (!n) continue; n.obj.visible = true; const c = n.castSpot; if (c && n.spot && Math.hypot(n.spot.x - c.x, n.spot.z - c.z) > .3) n.spot = Object.assign({}, n.spot, c); if (c && Math.hypot(n.x - c.x, n.z - c.z) > .3) { n.x = c.x; n.z = c.z; n.tx = null; n.tz = null; n.moving = false; n.state = 'work'; n.obj.position.set(c.x, P.surfaceY(c.x, c.z) + (c.y || 0), c.z); n.obj.rotation.y = c.face; } } };
}"""
POS = """() => { const o = {}; for (const [k, f] of Object.entries({ rv: window.__REV, kd: window.__KDS, wh: window.__WHO })) { const n = f(); o[k] = n ? [n.name, +n.x.toFixed(2), +n.z.toFixed(2), +n.obj.position.y.toFixed(2), +n.obj.rotation.y.toFixed(2), n.role] : null; }
  for (const [k, b] of Object.entries(window.__B50)) o[k] = [b.position.x, b.position.y, b.position.z, b.rotation.y]; return o; }"""
CLK = os.environ.get('CLK', '.45')
HEAD = """const P = window.__pulau; window.__fix50(); window.__clock = """ + CLK + """; window.__cheer = null; window.__cartPos = 1; P.player.obj.visible = false; P.scene.traverse(o => { const g = o.isInstancedMesh && o.geometry.parameters; if (g && ((g.height === 1.4 && g.radiusTop === .04) || (g.width === .18 && g.height === .22))) o.visible = false; }); """
def close(getter, Y, h, d0, d1=None, pitch=.1, dur=3.0, extra='', dyaw=0.0, cheer='null', ox=0.0, oz=0.0):
    d1 = d0 - .3 if d1 is None else d1
    return """() => { """ + HEAD + extra + """ window.__cheer = """ + cheer + """; const n = """ + getter + """(), x = n.x + """ + str(ox) + """, z = n.z + """ + str(oz) + """, y = Math.max(n.obj.position.y, P.surfaceY(n.x, n.z)) + """ + str(h) + """;
  window.__look(x, z, """ + str(Y) + """, """ + str(pitch) + """, """ + str(d0) + """, false); if (""" + str(abs(ox) + abs(oz)) + """ > 0) { P.player.x += 40; P.player.z += 40; }
  window.__beforeRender = (dt, T) => { const q = Math.min(1, T / """ + str(dur) + """), e = q * q * (3 - 2 * q); window.__C(x, y, z); P.cam.dist = """ + str(d0) + """ + (""" + str(d1 - d0) + """) * e; P.cam.yaw = """ + str(Y) + """ + """ + str(dyaw) + """ * e; P.cam.pitch = """ + str(pitch) + """; window.__clr([n], x, z, .5); }; }"""
def bld(key, lx, lz, ly, Y0, Y1, p0, p1, d0, d1, dur, cheer='null', lx1=None, lz1=None, extra='', cart=None):
    """camera on a local point of an ep50 building (world yaw), easing yaw/pitch/dist (and target) over dur; cart = (k0, k1, t0, t1) animates the mine cart"""
    lx1 = lx if lx1 is None else lx1; lz1 = lz if lz1 is None else lz1
    cj = '' if cart is None else f"{{ const c = Math.min(1, Math.max(0, (T - {cart[2]}) / ({cart[3]} - {cart[2]}))); window.__cartPos = {cart[0]} + ({cart[1] - cart[0]}) * c * c * (3 - 2 * c); }}"
    return """() => { """ + HEAD + extra + """ window.__cheer = """ + cheer + """; const o = window.__B50['""" + key + """'], a = o.position.clone().set(""" + f"{lx}, {ly}, {lz}" + """), b = o.position.clone().set(""" + f"{lx1}, {ly}, {lz1}" + """); o.localToWorld(a); o.localToWorld(b);
  window.__look(a.x, a.z, """ + str(Y0) + """, """ + str(p0) + """, """ + str(d0) + """, false);
  window.__beforeRender = (dt, T) => { """ + cj + """ const q = Math.min(1, T / """ + str(dur) + """), e = q * q * (3 - 2 * q); const x = a.x + (b.x - a.x) * e, z = a.z + (b.z - a.z) * e;
    window.__C(x, a.y, z); P.cam.dist = """ + str(d0) + """ + (""" + str(d1 - d0) + """) * e; P.cam.yaw = """ + str(Y0) + """ + (""" + str(Y1 - Y0) + """) * e; P.cam.pitch = """ + str(p0) + """ + (""" + str(p1 - p0) + """) * e; window.__clr([], x, z, .6); }; }"""
E = os.environ.get
# c1 cold open: Revan next to the cart with the sandal, push in
C1 = close('window.__REV', float(E('Y1', '.3')), float(E('H1', '.95')), 2.7, 2.2, pitch=.14)
# c2 premise: aerial descending onto the mine and Jalan Warga
C2 = bld('tambang', 1.5, 4.5, 0, .45, .7, 1.1, .85, 52, 17, 4.4)
# c3 under the comment cards: slow pan from the mine toward the village
C3 = bld('tambang', 0, 2.5, 0, .2, .45, .85, .75, 13, 12, 6.0, lx1=7, lz1=4)
# c4 the Kantor Kepala Desa with its sign (building faces world -z: camera yaw ~pi)
C4 = bld('kantordesa', 0, 1.6, 1.7, float(E('Y4', '3.35')), float(E('Y4', '3.35')) + .2, .5, .42, 5.6, 4.8, 5.0)
# c5 Pak Kades close, stamping (the mine behind him)
C5 = close('window.__KDS', float(E('Y5', '.05')), .95, 2.3, 1.9, pitch=.12)
# c6 the mine, wide: tunnel, sign, rails, Revan and Kades
C6 = bld('tambang', .45, 1.2, 1.2, -.25, .15, .32, .28, 8.5, 7.2, 5.6)
# c7 Revan close: pasti ada emas
C7 = close('window.__REV', float(E('Y7', '-.3')), .95, 2.0, 1.7, pitch=.1)
# c8 the cart rolls out of the tunnel (low, along the rails)
C8 = bld('tambang', 0, 1.0, .6, .0, .12, .2, .24, 4.6, 3.6, 4.0, cart=(0, 1, .4, 3.4))
# c9 the cart close: one blue sandal on the ore
C9 = bld('tambang', 0, 1.7, .75, float(E('Y9', '.45')), float(E('Y9', '.45')) + .2, .6, .5, 1.9, 1.4, 4.0)
# c10 Pak Kades recognises the sandal (other angle)
C10 = close('window.__KDS', float(E('Y10', '.6')), .95, 2.1, 1.8, pitch=.1)
# c11 whoyss peeking from behind the rocks
C11 = close('window.__WHO', float(E('Y11', '-.9')), .8, 2.1, 1.8, pitch=.12)
# c12 end: the cart rolls back in, crane up over the mine and Jalan Warga
C12 = bld('tambang', 0, 1.7, .5, .2, .7, .35, 1.0, 3.0, 20, 6.5, cheer='true', lx1=2, lz1=5, cart=(1, 0, .8, 4.0))
# c13 cold open (used instead of c1): two-shot, the cart with the sandal on the left, Revan on the right, push in
C13 = bld('tambang', float(E('LX13', '.5')), 1.8, float(E('LY13', '1.15')), float(E('Y13', '-.4')), float(E('Y13', '-.4')) + .08, .24, .2, float(E('D13', '3.1')), float(E('D13', '3.6')) - .5, 4.5)
# c14 cold open (final): the cart close-up framed lower so the sandal sits under the hook
C14 = bld('tambang', 0, 1.7, float(E('LY14', '1.1')), .45, .6, .55, .48, 1.9, 1.5, 4.0)
SHOTS = {'c14': (C14, 130), 'c13': (C13, 150), 'c1': (C1, 150), 'c2': (C2, 145), 'c3': (C3, 200), 'c4': (C4, 170), 'c5': (C5, 150), 'c6': (C6, 190), 'c7': (C7, 120),
         'c8': (C8, 130), 'c9': (C9, 130), 'c10': (C10, 140), 'c11': (C11, 120), 'c12': (C12, 290)}
CLEAR = E49.CLEAR[:-1] + " window.__cartPos = null; }"
async def run(which):
    async with async_playwright() as p:
        b, pg = await setup(p)
        for js in CHAIN + (SETUP50,): await pg.evaluate(js)
        if os.environ.get('VARS'): await pg.evaluate('() => { ' + os.environ['VARS'] + ' }')
        if 'pos' in which: print(await pg.evaluate(POS))
        for k, (js, n) in SHOTS.items():
            if k in which and 'prev' not in which:
                await shoot(pg, 'e50' + k, int(os.environ.get('N_' + k, n)), start_js=js, warm=12)
                await pg.evaluate(CLEAR)
        if 'prev' in which:
            for k, (js, n) in SHOTS.items():
                if 'all' not in which and k not in which: continue
                await shoot(pg, 'p50' + k, 1, start_js=js, warm=int(os.environ.get('WARM', '40')))
                await pg.evaluate(CLEAR)
        await b.close()
if __name__ == "__main__": asyncio.run(run(sys.argv[1].split(",")))
