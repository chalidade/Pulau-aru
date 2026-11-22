"""Episode 51 "Komen 'Bikin Masjid', Besoknya Berdiri" shot list (format KONSEP, run pagi 22 Nov).  usage: DPR=2 python3 shots.py c1,c3,...  (DPR=1 + prev for checks)
Two real comments (komentar.md, collected via TikTok Studio 20 Nov): @gonrong1231 "bikin masjit" -> Mushola Warga (mushola x74 y73, Jalan Warga)
with zidan (penjaga masjid) sweeping its courtyard; @dayang.qaisara19 "kak aku dayang19" -> Dayang joins as the first volunteer of the Pos
Gotong Royong (posgotong x60 y73), built from Ish's traktiran x10 ("semangat berkarya dan membantu memudahkan pekerjaan orang lain").
The second mine cart brings out the other sandal (tambang b.sandals = 2). All of it is island.json state (live on the web).
"""
import asyncio, sys, os, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'lib'))
from harness import *
def _mod(name, path):
    sp = importlib.util.spec_from_file_location(name, path); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m
E50 = _mod('ep50shots', os.path.join(HERE, '..', 'ep50', 'shots.py'))
CHAIN = E50.CHAIN + (E50.SETUP50,)
SETUP51 = """() => { const P = window.__pulau;
  const F = s => P.npcs.find(n => n.name === s || (n.name || '').startsWith(s));
  window.__DAY = () => F('dayang.qaisara19'); window.__ZID = () => F('panggil aja zidan');
  const B = {}; P.scene.traverse(o => { if (o.userData && o.userData.b && ['tambang', 'mushola', 'posgotong'].includes(o.userData.b.type)) B[o.userData.b.type] = o; });
  window.__B51 = B;
  window.__fix51 = () => { window.__fix50();
    for (const f of [window.__DAY, window.__ZID]) { const n = f(); if (!n) continue; n.obj.visible = true; const c = n.castSpot; if (c && n.spot && Math.hypot(n.spot.x - c.x, n.spot.z - c.z) > .3) n.spot = Object.assign({}, n.spot, c); if (c && Math.hypot(n.x - c.x, n.z - c.z) > .3) { n.x = c.x; n.z = c.z; n.tx = null; n.tz = null; n.moving = false; n.state = 'work'; n.obj.position.set(c.x, P.surfaceY(c.x, c.z) + (c.y || 0), c.z); n.obj.rotation.y = c.face; } } };
}"""
POS = """() => { const o = {}; for (const [k, f] of Object.entries({ dy: window.__DAY, zd: window.__ZID, rv: window.__REV })) { const n = f(); o[k] = n ? [n.name, +n.x.toFixed(2), +n.z.toFixed(2), +n.obj.position.y.toFixed(2), +n.obj.rotation.y.toFixed(2), n.role] : null; }
  for (const [k, b] of Object.entries(window.__B51)) o[k] = [b.position.x, b.position.y, b.position.z, b.rotation.y, b.scale.x]; return o; }"""
CLK = os.environ.get('CLK', '.42')
HEAD = """const P = window.__pulau; window.__fix51(); window.__clock = """ + CLK + """; window.__cheer = null; window.__cartPos = 1; P.player.obj.visible = false; P.scene.traverse(o => { const g = o.isInstancedMesh && o.geometry.parameters; if (g && ((g.height === 1.4 && g.radiusTop === .04) || (g.width === .18 && g.height === .22))) o.visible = false; }); """
def close(getter, Y, h, d0, d1=None, pitch=.1, dur=3.0, extra='', dyaw=0.0, cheer='null'):
    d1 = d0 - .3 if d1 is None else d1
    return """() => { """ + HEAD + extra + """ window.__cheer = """ + cheer + """; const n = """ + getter + """(), x = n.x, z = n.z, y = Math.max(n.obj.position.y, P.surfaceY(n.x, n.z)) + """ + str(h) + """;
  window.__look(x, z, """ + str(Y) + """, """ + str(pitch) + """, """ + str(d0) + """, false);
  window.__beforeRender = (dt, T) => { const q = Math.min(1, T / """ + str(dur) + """), e = q * q * (3 - 2 * q); window.__C(x, y, z); P.cam.dist = """ + str(d0) + """ + (""" + str(d1 - d0) + """) * e; P.cam.yaw = """ + str(Y) + """ + """ + str(dyaw) + """ * e; P.cam.pitch = """ + str(pitch) + """; window.__clr([n], x, z, .5); }; }"""
def bld(key, lx, lz, ly, Y0, Y1, p0, p1, d0, d1, dur, cheer='null', lx1=None, lz1=None, extra='', cart=None):
    """camera on a local point of a building (local units; the building's own scale is applied), easing yaw/pitch/dist/target"""
    lx1 = lx if lx1 is None else lx1; lz1 = lz if lz1 is None else lz1
    cj = '' if cart is None else f"{{ const c = Math.min(1, Math.max(0, (T - {cart[2]}) / ({cart[3]} - {cart[2]}))); window.__cartPos = {cart[0]} + ({cart[1] - cart[0]}) * c * c * (3 - 2 * c); }}"
    return """() => { """ + HEAD + extra + """ window.__cheer = """ + cheer + """; const o = window.__B51['""" + key + """'], k = o.scale.x || 1, a = o.position.clone().set(""" + f"{lx}*k, {ly}*k, {lz}*k" + """), b = o.position.clone().set(""" + f"{lx1}*k, {ly}*k, {lz1}*k" + """); o.localToWorld(a.divideScalar(k)); o.localToWorld(b.divideScalar(k));
  window.__look(a.x, a.z, """ + str(Y0) + """, """ + str(p0) + """, """ + str(d0) + """, false);
  window.__beforeRender = (dt, T) => { """ + cj + """ const q = Math.min(1, T / """ + str(dur) + """), e = q * q * (3 - 2 * q); const x = a.x + (b.x - a.x) * e, z = a.z + (b.z - a.z) * e;
    window.__C(x, a.y, z); P.cam.dist = """ + str(d0) + """ + (""" + str(d1 - d0) + """) * e; P.cam.yaw = """ + str(Y0) + """ + (""" + str(Y1 - Y0) + """) * e; P.cam.pitch = """ + str(p0) + """ + (""" + str(p1 - p0) + """) * e; window.__clr([], x, z, .6); }; }"""
E = os.environ.get
f = lambda k, d: float(E(k, d))
# c1 cold open: zidan close in the mushola courtyard, the mushola behind him, push in
C1 = close('window.__ZID', f('Y1', '.35'), f('H1', '1.45'), f('D1', '4.2'), f('D1', '4.2') - .6, pitch=f('P1', '.1'))
# c2 premise: aerial descending onto Jalan Warga and the mushola
C2 = bld('mushola', 0, 0, 0, .55, .3, 1.1, .8, 55, 20, 4.4)
# c3 under the comment cards: slow pan along Jalan Warga from the pos to the mushola
C3 = bld('mushola', 0, 2.0, 0, float(E('Y3', '3.0')), float(E('Y3', '3.0')) + .3, float(E('P3', '.85')), float(E('P3', '.85')) - .1, 15, 13, 6.0, lx1=-9)
# c4 the Mushola Warga, front, sign readable
C4 = bld('mushola', 0, 1.2, 1.5, f('Y4', '.2'), f('Y4', '.2') + .35, .38, .3, 7.0, 6.0, 5.5)
# c5 zidan close, other side (the sandal rack)
C5 = close('window.__ZID', f('Y5', '-.5'), 1.0, 3.1, 2.6, pitch=.14)
# c6 Dayang close at the pos
C6 = close('window.__DAY', f('Y6', '.2'), 1.0, 2.6, 2.1, pitch=.12)
# c7 Ish's plaque close
C7 = bld('posgotong', -1.0, 1.45, .95, f('Y7', '.1'), f('Y7', '.1') - .1, .1, .08, 1.7, 1.35, 4.0)
# c8 the pos, slow pan from the plaque side to the kentongan and the tea table
C8 = bld('posgotong', -.6, .8, 1.2, .5, .15, .3, .26, 5.0, 4.2, 5.0, lx1=.5)
# c9 the pos wide reveal with the crowd cheering
C9 = bld('posgotong', 0, .6, 1.4, -.35, .1, .35, .3, 7.5, 6.0, 4.0, cheer='true')
# c10 Dayang close again (other angle) pulling back
C10 = close('window.__DAY', f('Y10', '-.4'), 1.0, 2.2, 2.9, pitch=.12, cheer='true')
# c11 the cart rolls out of the tunnel
C11 = bld('tambang', 0, 1.0, .6, .0, .12, .2, .24, 4.6, 3.6, 4.0, cart=(0, 1, .4, 3.4))
# c12 the cart close: now a pair of blue sandals
C12 = bld('tambang', 0, 1.7, f('LY12', '1.0'), f('Y12', '.45'), f('Y12', '.45') + .25, .55, .45, 1.9, 1.5, 6.0)
# c13 end: crane up from the pos over Jalan Warga toward the mushola
C13 = bld('posgotong', 0, .5, 1.0, .3, .55, .3, .95, 6.0, 30, 7.0, cheer='true', lx1=7, lz1=1)
SHOTS = {'c1': (C1, 130), 'c2': (C2, 110), 'c3': (C3, 150), 'c4': (C4, 180), 'c5': (C5, 130), 'c6': (C6, 200), 'c7': (C7, 130),
         'c8': (C8, 160), 'c9': (C9, 130), 'c10': (C10, 90), 'c11': (C11, 110), 'c12': (C12, 200), 'c13': (C13, 260)}
CLEAR = E50.CLEAR
async def run(which):
    async with async_playwright() as p:
        b, pg = await setup(p)
        for js in CHAIN + (SETUP51,): await pg.evaluate(js)
        if os.environ.get('VARS'): await pg.evaluate('() => { ' + os.environ['VARS'] + ' }')
        if 'pos' in which: print(await pg.evaluate(POS))
        for k, (js, n) in SHOTS.items():
            if k in which and 'prev' not in which:
                await shoot(pg, 'e51' + k, int(os.environ.get('N_' + k, n)), start_js=js, warm=12)
                await pg.evaluate(CLEAR)
        if 'prev' in which:
            for k, (js, n) in SHOTS.items():
                if 'all' not in which and k not in which: continue
                await shoot(pg, 'p51' + k, 1, start_js=js, warm=int(os.environ.get('WARM', '40')))
                await pg.evaluate(CLEAR)
        await b.close()
if __name__ == "__main__": asyncio.run(run(sys.argv[1].split(",")))
