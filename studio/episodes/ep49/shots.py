"""Episode 49 "Komen 'Mau Masuk', Dapat Rumah" shot list (format KONSEP, run pagi 21 Nov).  usage: DPR=2 python3 shots.py c1,c3,...  (DPR=1 + prev for checks)
Two real comments (komentar.md, collected via TikTok Studio 20 Nov): @v1dy4_0560 "Kaka aku mau ikut nama Ku vidya semoga aku bisa masuk
pulau ini" -> Rumah Vidya on the first empty plot of Jalan Warga (rumahwarga x37 y74, deco 'balon'), Vidya waving at her door;
@hanssmuhammad698 "tambahin hewan" -> Kebun Hewan Mini (kebunhewan x38 y80 r2: hens, goat, cow, ducks, a hen chasing the kitten),
Hans at the gate. Traktiran 'Seseorang' x5 from Aceh -> Tugu Salam (tugusalam x35 y80 r2). Pinjam Seratus moved next to Vidya.
All of it is island.json state (live on the web); Aru is the player character.
"""
import asyncio, sys, os, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'lib'))
from harness import *
def _mod(name, path):
    sp = importlib.util.spec_from_file_location(name, path); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m
E48 = _mod('ep48shots', os.path.join(HERE, '..', 'ep48', 'shots.py'))
CHAIN = E48.CHAIN + (E48.SETUP48,)
SETUP49 = """() => { const P = window.__pulau;
  const F = s => P.npcs.find(n => n.name === s || (n.name || '').startsWith(s));
  window.__VID = () => F('v1dy4_0560'); window.__HAN = () => F('hanssmuhammad698'); window.__PIN = () => F('Pinjam seratus');
  const B = {}; P.scene.traverse(o => { if (o.userData && o.userData.b && ['kebunhewan', 'tugusalam'].includes(o.userData.b.type)) B[o.userData.b.type] = o;
    if (o.userData && o.userData.b && o.userData.b.type === 'rumahwarga' && o.userData.b.label === 'RUMAH VIDYA') B.rumah = o; });
  window.__B49 = B;
  window.__fix49 = () => { window.__fix48();
    for (const f of [window.__VID, window.__HAN, window.__PIN]) { const n = f(); if (!n) continue; n.obj.visible = true; const c = n.castSpot; if (c && n.spot && Math.hypot(n.spot.x - c.x, n.spot.z - c.z) > .3) n.spot = Object.assign({}, n.spot, c); if (c && Math.hypot(n.x - c.x, n.z - c.z) > .3) { n.x = c.x; n.z = c.z; n.tx = null; n.tz = null; n.moving = false; n.state = 'work'; n.obj.position.set(c.x, P.surfaceY(c.x, c.z) + (c.y || 0), c.z); n.obj.rotation.y = c.face; } } };
}"""
POS = """() => { const o = {}; for (const [k, f] of Object.entries({ vd: window.__VID, hn: window.__HAN, pn: window.__PIN })) { const n = f(); o[k] = n ? [n.name, +n.x.toFixed(2), +n.z.toFixed(2), +n.obj.position.y.toFixed(2), +n.obj.rotation.y.toFixed(2), n.role] : null; }
  for (const [k, b] of Object.entries(window.__B49)) o[k] = [b.position.x, b.position.y, b.position.z, b.rotation.y]; return o; }"""
CLK = os.environ.get('CLK', '.4')
HEAD = """const P = window.__pulau; window.__fix49(); window.__clock = """ + CLK + """; window.__cheer = null; P.player.obj.visible = false; """
def close(getter, Y, h, d0, d1=None, pitch=.1, dur=3.0, extra='', dyaw=0.0, cheer='null'):
    d1 = d0 - .3 if d1 is None else d1
    return """() => { """ + HEAD + extra + """ window.__cheer = """ + cheer + """; const n = """ + getter + """(), x = n.x, z = n.z, y = Math.max(n.obj.position.y, P.surfaceY(x, z)) + """ + str(h) + """;
  window.__look(x, z, """ + str(Y) + """, """ + str(pitch) + """, """ + str(d0) + """, false);
  window.__beforeRender = (dt, T) => { const q = Math.min(1, T / """ + str(dur) + """), e = q * q * (3 - 2 * q); window.__C(x, y, z); P.cam.dist = """ + str(d0) + """ + (""" + str(d1 - d0) + """) * e; P.cam.yaw = """ + str(Y) + """ + """ + str(dyaw) + """ * e; P.cam.pitch = """ + str(pitch) + """; window.__clr([n], x, z, .5); }; }"""
def bld(key, lx, lz, ly, Y0, Y1, p0, p1, d0, d1, dur, cheer='null', lx1=None, lz1=None):
    """camera on a local point of an ep49 building (world yaw), easing yaw/pitch/dist (and target) over dur"""
    lx1 = lx if lx1 is None else lx1; lz1 = lz if lz1 is None else lz1
    return """() => { """ + HEAD + """ window.__cheer = """ + cheer + """; const o = window.__B49['""" + key + """'], a = o.position.clone().set(""" + f"{lx}, {ly}, {lz}" + """), b = o.position.clone().set(""" + f"{lx1}, {ly}, {lz1}" + """); o.localToWorld(a); o.localToWorld(b);
  window.__look(a.x, a.z, """ + str(Y0) + """, """ + str(p0) + """, """ + str(d0) + """, false);
  window.__beforeRender = (dt, T) => { const q = Math.min(1, T / """ + str(dur) + """), e = q * q * (3 - 2 * q); const x = a.x + (b.x - a.x) * e, z = a.z + (b.z - a.z) * e;
    window.__C(x, a.y, z); P.cam.dist = """ + str(d0) + """ + (""" + str(d1 - d0) + """) * e; P.cam.yaw = """ + str(Y0) + """ + (""" + str(Y1 - Y0) + """) * e; P.cam.pitch = """ + str(p0) + """ + (""" + str(p1 - p0) + """) * e; window.__clr([], x, z, .6); }; }"""
# c1 cold open: Vidya waving at her new door, push in
C1 = close('window.__VID', float(os.environ.get('Y1', '.15')), float(os.environ.get('H1', '.95')), 2.6, 2.1, pitch=.12, cheer='true')
# c2 premise: aerial descending onto Jalan Warga (the new house and the farm)
C2 = bld('rumah', 1.5, 3.5, 0, .5, .7, 1.1, .85, 50, 16, 4.4)
# c3 under the comment cards: slow pan over house + farm
C3 = bld('rumah', 1.5, 4.5, 0, .7, .9, .8, .75, 12, 10.5, 6.0)
# c4 the house front with its name sign and balloons
C4 = bld('rumah', 0, .8, 1.6, -.25, .2, .2, .16, 4.6, 4.0, 5.2)
# c5 Aru gives Vidya the house (two-shot, Aru = player)
C5 = """() => { """ + HEAD + """ const n = window.__VID(), ax = n.x + 1.05, az = n.z + .25, x = (n.x + ax) / 2, z = (n.z + az) / 2, y = P.surfaceY(n.x, n.z) + .9;
  window.__look(ax, az, -.3, .3, 4.0, true); const pl = P.player;
  window.__beforeRender = (dt, T) => { pl.obj.visible = true; pl.x = ax; pl.z = az; pl.obj.position.x = ax; pl.obj.position.z = az; pl.obj.rotation.y = -1.0; window.__C(x, y, z); P.cam.dist = Math.max(3.7, 4.0 - T * .1); P.cam.yaw = -.3; P.cam.pitch = .3; window.__clr([n], x, z, .6); }; }"""
# c6 Vidya very close, happy (crowd cheering)
C6 = close('window.__VID', -.35, .95, 1.9, 1.7, pitch=.1, cheer='true')
# c7 Pinjam Seratus (between the houses, facing Vidya)
C7 = close('window.__PIN', float(os.environ.get('Y7', '-.9')), 1.0, 2.0, 1.7, pitch=.1)
# c8 the farm gate with the sign and Hans waving (from the street)
C8 = bld('kebunhewan', -.35, 1.5, 1.1, float(os.environ.get('Y8', '-.4')), float(os.environ.get('Y8', '-.4')) + .15, .24, .28, 3.9, 3.4, 5.4)
# c9 over the animals: cow, goat, ducks (dolly)
C9 = bld('kebunhewan', -.6, -.6, .4, 2.5, 2.1, .45, .4, 3.0, 2.7, 4.4, lx1=1.2, lz1=-.5)
# c10 the kitten chased by the hen round the trough
C10 = bld('kebunhewan', .2, .15, .2, -.5, -.3, 1.0, .95, 5.6, 5.0, 4.2)
# c11 Tugu Salam, the plaque
C11 = bld('tugusalam', 0, .2, 1.15, 3.14, 3.3, .1, .08, 2.6, 2.2, 6.4)
# c12 end: from Vidya's door, crane up over Jalan Warga and the farm
C12 = """() => { """ + HEAD + """ window.__cheer = true; const n = window.__VID(), x = n.x, z = n.z, y = P.surfaceY(x, z) + .9;
  window.__look(x, z, .1, .15, 2.0, false);
  window.__beforeRender = (dt, T) => { const q = Math.min(1, T / 6), e = q * q * (3 - 2 * q); window.__C(x + 1.5 * e, y, z + 2.5 * e); P.cam.dist = 2.0 + 15 * e; P.cam.yaw = .1 + .5 * e; P.cam.pitch = .15 + .8 * Math.min(1, T / 2.5); window.__clr([n], x, z, .6); }; }"""
SHOTS = {'c1': (C1, 195), 'c2': (C2, 145), 'c3': (C3, 190), 'c4': (C4, 165), 'c5': (C5, 115), 'c6': (C6, 110), 'c7': (C7, 125),
         'c8': (C8, 175), 'c9': (C9, 145), 'c10': (C10, 135), 'c11': (C11, 200), 'c12': (C12, 230)}
CLEAR = E48.CLEAR
async def run(which):
    async with async_playwright() as p:
        b, pg = await setup(p)
        for js in CHAIN + (SETUP49,): await pg.evaluate(js)
        if os.environ.get('VARS'): await pg.evaluate('() => { ' + os.environ['VARS'] + ' }')
        if 'pos' in which: print(await pg.evaluate(POS))
        for k, (js, n) in SHOTS.items():
            if k in which and 'prev' not in which:
                await shoot(pg, 'e49' + k, int(os.environ.get('N_' + k, n)), start_js=js, warm=12)
                await pg.evaluate(CLEAR)
        if 'prev' in which:
            for k, (js, n) in SHOTS.items():
                if 'all' not in which and k not in which: continue
                await shoot(pg, 'p49' + k, 1, start_js=js, warm=int(os.environ.get('WARM', '40')))
                await pg.evaluate(CLEAR)
        await b.close()
if __name__ == "__main__": asyncio.run(run(sys.argv[1].split(",")))
