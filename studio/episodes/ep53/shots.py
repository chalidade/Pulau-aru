"""Episode 53 "Traktiran Kalian Jadi Api Unggun" shot list (format KONSEP, run pagi 23 Nov).  usage: DPR=2 python3 shots.py c1,c3,...  (DPR=1 + prev for checks)
No new TikTok comments (komentar.md empty, Chrome not connected); two Trakteer supporters drive the episode:
Anon Indo x11 ("Semangat utk cavatomnya 🔥") -> Api Unggun Semangat (apiunggun x38 y68), and umi ZahamaAlkena x2 ("Semangat terus Kaka
inshaa Allaah jadi jariyah") -> Sumur Jariyah (sumurjariyah x41 y71 r2), both west of the school, north of Jalan Warga. The Pos Gotong Royong
board gets a second ticked job. ALIF HR, NOVA (Klub Warga Biasa) and senar muliya (guitar) now stand round the fire (island.json resident
spots, live on the web). Staged only: the time of day (day / dusk -> night).
"""
import asyncio, sys, os, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'lib'))
from harness import *
def _mod(name, path):
    sp = importlib.util.spec_from_file_location(name, path); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m
E52 = _mod('ep52shots', os.path.join(HERE, '..', 'ep52', 'shots.py'))
CHAIN = E52.CHAIN + (E52.SETUP52,)
SETUP53 = """() => { const P = window.__pulau;
  const F = s => P.npcs.find(n => n.name === s || (n.name || '').startsWith(s));
  window.__ALIF = () => F('ALIF HR'); window.__NOVA = () => F('NOVA'); window.__SENAR = () => F('senar muliya');
  const B = {}; P.scene.traverse(o => { if (o.userData && o.userData.b && ['apiunggun', 'sumurjariyah', 'posgotong'].includes(o.userData.b.type)) B[o.userData.b.type] = o; });
  window.__B53 = B;
  window.__fix53 = () => { window.__fix52();
    for (const f of [window.__ALIF, window.__NOVA, window.__SENAR]) { const n = f(); if (!n) continue; n.obj.visible = true; const c = n.castSpot; if (c && n.spot) { n.spot = Object.assign({}, n.spot, c); } if (c && Math.hypot(n.x - c.x, n.z - c.z) > .3) { n.x = c.x; n.z = c.z; n.tx = null; n.tz = null; n.moving = false; n.state = 'work'; n.obj.position.set(c.x, P.surfaceY(c.x, c.z) + (c.y || 0), c.z); } if (c) n.obj.rotation.y = c.face; } };
}"""
POS = """() => { const o = {}; for (const [k, f] of Object.entries({ al: window.__ALIF, nv: window.__NOVA, sn: window.__SENAR })) { const n = f(); o[k] = n ? [n.name, +n.x.toFixed(2), +n.z.toFixed(2), +n.obj.position.y.toFixed(2), +n.obj.rotation.y.toFixed(2), n.role] : null; }
  for (const [k, b] of Object.entries(window.__B53)) o[k] = [b.position.x, b.position.y, b.position.z, b.rotation.y, b.scale.x]; return o; }"""
DAY, NIGHT = os.environ.get('CLK', '.42'), os.environ.get('NCLK', '.71')
def head(clk):
    return """const P = window.__pulau; window.__fix53(); window.__clock = """ + str(clk) + """; window.__cheer = null; window.__cartPos = 1; P.player.obj.visible = false; P.scene.traverse(o => { const g = o.isInstancedMesh && o.geometry.parameters; if (g && ((g.height === 1.4 && g.radiusTop === .04) || (g.width === .18 && g.height === .22))) o.visible = false; }); """
def close(getter, Y, h, d0, d1=None, pitch=.1, dur=3.0, extra='', dyaw=0.0, cheer='null', ox=0.0, oz=0.0, clk=NIGHT):
    d1 = d0 - .3 if d1 is None else d1
    return """() => { """ + head(clk) + extra + """ window.__cheer = """ + cheer + """; const n = """ + getter + """(), x = n.x + """ + str(ox) + """, z = n.z + """ + str(oz) + """, y = Math.max(n.obj.position.y, P.surfaceY(n.x, n.z)) + """ + str(h) + """;
  window.__look(x, z, """ + str(Y) + """, """ + str(pitch) + """, """ + str(d0) + """, false);
  window.__beforeRender = (dt, T) => { const q = Math.min(1, T / """ + str(dur) + """), e = q * q * (3 - 2 * q); window.__C(x, y, z); P.cam.dist = """ + str(d0) + """ + (""" + str(d1 - d0) + """) * e; P.cam.yaw = """ + str(Y) + """ + """ + str(dyaw) + """ * e; P.cam.pitch = """ + str(pitch) + """; window.__clr([n], x, z, .5); }; }"""
def bld(key, lx, lz, ly, Y0, Y1, p0, p1, d0, d1, dur, cheer='null', lx1=None, lz1=None, extra='', clk=DAY, clk1=None):
    """camera on a local point of a building, easing yaw/pitch/dist/target; clk1 = time of day at the end (dusk -> night)"""
    lx1 = lx if lx1 is None else lx1; lz1 = lz if lz1 is None else lz1
    cj = '' if clk1 is None else f"window.__clock = {clk} + ({float(clk1) - float(clk)}) * e;"
    return """() => { """ + head(clk) + extra + """ window.__cheer = """ + cheer + """; const o = window.__B53['""" + key + """'], k = o.scale.x || 1, a = o.position.clone().set(""" + f"{lx}*k, {ly}*k, {lz}*k" + """), b = o.position.clone().set(""" + f"{lx1}*k, {ly}*k, {lz1}*k" + """); o.localToWorld(a.divideScalar(k)); o.localToWorld(b.divideScalar(k));
  window.__look(a.x, a.z, """ + str(Y0) + """, """ + str(p0) + """, """ + str(d0) + """, false);
  window.__beforeRender = (dt, T) => { const q = Math.min(1, T / """ + str(dur) + """), e = q * q * (3 - 2 * q); """ + cj + """ const x = a.x + (b.x - a.x) * e, z = a.z + (b.z - a.z) * e;
    window.__C(x, a.y, z); P.cam.dist = """ + str(d0) + """ + (""" + str(d1 - d0) + """) * e; P.cam.yaw = """ + str(Y0) + """ + (""" + str(Y1 - Y0) + """) * e; P.cam.pitch = """ + str(p0) + """ + (""" + str(p1 - p0) + """) * e; window.__clr([], x, z, .6); }; }"""
E = os.environ.get
f = lambda k, d: float(E(k, d))
# c1 cold open (flash-forward): the fire at night, ALIF and NOVA either side, push in
C1 = bld('apiunggun', 0, .1, f('LY1', '.55'), f('Y1', '-.15'), f('Y1', '-.15') + .12, f('P1', '.42'), f('P1', '.42') - .04, f('D1', '3.4'), f('D1', '3.4') - .6, 4.5, clk=NIGHT)
# c2 premise: aerial descending onto the fire and the well (day)
C2 = bld('apiunggun', 1.5, 1.5, 0, .55, .3, 1.1, .85, 50, 16, 5.0)
# c3 under Anon Indo's traktir card: the plaque close (day)
C3 = bld('apiunggun', -.95, 1.3, .9, f('Y3', '.05'), f('Y3', '.05') - .12, .1, .08, 1.7, 1.35, 5.0)
# c4 Aru: 'kita bikin api unggun beneran!' the fire site with its sign (day)
C4 = bld('apiunggun', 0, .5, .6, -.75, -.35, .55, .5, 5.5, 4.6, 3.2)
# c5 the Pos Gotong Royong job board: second job ticked
C5 = bld('posgotong', 1.05, 1.45, .98, f('Y5', '-.05'), f('Y5', '-.05') + .1, .1, .08, 1.75, 1.4, 4.5)
# c6 under umi's traktir card: the well's plaque close (well faces north, r2)
C6 = bld('sumurjariyah', -.2, .4, .45, f('Y6', '3.1'), f('Y6', '3.1') + .12, .12, .1, 1.5, 1.2, 4.2)
# c7 Aru: 'Sumur Jariyah, gratis buat semua!' the well front with its sign
C7 = bld('sumurjariyah', -.2, .3, 1.2, f('Y7', '3.75'), f('Y7', '3.75') + .4, .3, .25, 4.6, 3.6, 4.5)
# c8 the tap's running water and the swaying bucket
C8 = bld('sumurjariyah', .6, .7, .6, f('Y8', '4.4'), f('Y8', '4.4') + .3, .3, .24, 2.0, 1.6, 4.2)
# c9 dusk -> night: the fire lit, wide, the light falls
C9 = bld('apiunggun', 0, 0, .5, .55, .2, .6, .42, 9.0, 6.0, 4.0, clk='.57', clk1=NIGHT)
# c10 ALIF close at the fire
C10 = close('window.__ALIF', f('Y10', '.7'), 1.05, 2.4, 2.1, pitch=.14)
# c11 NOVA close, hood on
C11 = close('window.__NOVA', f('Y11', '-1.25'), 1.0, 3.0, 2.7, pitch=.2)
# c12 senar muliya with the guitar
C12 = close('window.__SENAR', f('Y12', '1.1'), .95, 2.6, 2.2, pitch=.18)
# c13 Aru's thanks: the warm circle, wide, cheer
C13 = bld('apiunggun', 0, 0, .6, -.45, -.85, .5, .45, 5.2, 4.3, 5.0, cheer='true', clk=NIGHT)
# c14 end: crane up from the fire to the night island
C14 = bld('apiunggun', 0, 0, .5, -.6, -.1, .5, 1.0, 4.2, 30, 7.5, cheer='true', clk=NIGHT)
SHOTS = {'c1': (C1, 150), 'c2': (C2, 195), 'c3': (C3, 165), 'c4': (C4, 130), 'c5': (C5, 140), 'c6': (C6, 135), 'c7': (C7, 160),
         'c8': (C8, 130), 'c9': (C9, 130), 'c10': (C10, 160), 'c11': (C11, 130), 'c12': (C12, 160), 'c13': (C13, 140), 'c14': (C14, 200)}
CLEAR = E52.CLEAR
async def run(which):
    async with async_playwright() as p:
        b, pg = await setup(p)
        for js in CHAIN + (SETUP53,): await pg.evaluate(js)
        if os.environ.get('VARS'): await pg.evaluate('() => { ' + os.environ['VARS'] + ' }')
        if 'pos' in which: print(await pg.evaluate(POS))
        for k, (js, n) in SHOTS.items():
            if k in which and 'prev' not in which:
                await shoot(pg, 'e53' + k, int(os.environ.get('N_' + k, n)), start_js=js, warm=12)
                await pg.evaluate(CLEAR)
        if 'prev' in which:
            for k, (js, n) in SHOTS.items():
                if 'all' not in which and k not in which: continue
                await shoot(pg, 'p53' + k, int(os.environ.get('PN', '1')), start_js=js, warm=int(os.environ.get('WARM', '40')))
                await pg.evaluate(CLEAR)
        await b.close()
if __name__ == "__main__": asyncio.run(run(sys.argv[1].split(",")))
