"""Episode 46 "Jebakan Ikan Bakar" shot list (format CERITA, run sore 19 Nov).  usage: DPR=2 python3 shots.py c1,c3,...  (DPR=1 + prev for checks)
No new TikTok comments (Chrome not connected, komentar.md has none), so the episode is driven by the Trakteer request of Darwin (x4,
'Semoga ilmunya terus berkembang dan bermanfaat') -> Pojok Ilmu (pojokilmu x63 y86, a small book hut by the harbour) and the
MISTERI IKAN BAKAR part 3: the Detektif Pantai reads up ('bulu oranye, jari empat, suka ikan... kucing'), sets a night trap
(kamerajaga x63 y93: tripod camera, grilled-fish bait, monitor) and at 02:13 the monitor shows a small orange kitten eating the bait.
Cast: D4L (first library visitor, 'boleh pinjam?'), Aidil YZ (cries for the bait fish), Luci ('Hiu darat!'), mhmmdalfaiz0.
World: pojok centre (8.0, 31.0) facing +z, plaque (8.62, 32.25); kamera centre (7.5, 37.5), screen (7.7, 38.14, y+.64) facing +z.
"""
import asyncio, sys, os, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'lib'))
from harness import *
def _mod(name, path):
    sp = importlib.util.spec_from_file_location(name, path); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m
E45 = _mod('ep45shots', os.path.join(HERE, '..', 'ep45', 'shots.py'))
CHAIN = E45.CHAIN + (E45.SETUP45,)
SETUP46 = """() => { const P = window.__pulau;
  const F = s => P.npcs.find(n => n.name === s || (n.name || '').startsWith(s));
  window.__D4 = () => F('D4L'); window.__AI = () => F('Aidil');
  let pj = null, kj = null; P.scene.traverse(o => { if (o.userData && o.userData.b && o.userData.b.type === 'pojokilmu') pj = o; if (o.userData && o.userData.b && o.userData.b.type === 'kamerajaga') kj = o; });
  window.__PJK = pj; window.__KJ = kj;
  window.__fix46 = () => { window.__fix45();
    for (const f of [window.__D4, window.__AI]) { const n = f(); if (!n) continue; n.obj.visible = true; const c = n.castSpot; if (c && n.spot && Math.hypot(n.spot.x - c.x, n.spot.z - c.z) > .3) n.spot = Object.assign({}, n.spot, c); if (c && Math.hypot(n.x - c.x, n.z - c.z) > .3) { n.x = c.x; n.z = c.z; n.tx = null; n.tz = null; n.moving = false; n.state = 'work'; n.obj.position.set(c.x, P.surfaceY(c.x, c.z), c.z); n.obj.rotation.y = c.face; } } };
}"""
POS = """() => { const o = {}; for (const [k, f] of Object.entries({ af: window.__AF, lu: window.__LU, d4: window.__D4, ai: window.__AI })) { const n = f(); o[k] = n ? [n.name, +n.x.toFixed(2), +n.z.toFixed(2), +n.obj.position.y.toFixed(2), +n.obj.rotation.y.toFixed(2)] : null; }
  o.pj = window.__PJK && [window.__PJK.position.x, window.__PJK.position.y, window.__PJK.position.z]; o.kj = window.__KJ && [window.__KJ.position.x, window.__KJ.position.y, window.__KJ.position.z]; return o; }"""
CLK = os.environ.get('CLK', '.36')
HEAD = """const P = window.__pulau; window.__fix46(); window.__clock = """ + CLK + """; window.__cheer = null; P.player.obj.visible = false; """
def close(getter, face, Y, body, dist=2.1, h=1.12, clk=None, pitch=.1):
    return """() => { """ + HEAD + ('' if clk is None else 'window.__clock = ' + str(clk) + ';') + """ const n = """ + getter + """(), x = n.x, z = n.z, y0 = P.surfaceY(x, z), Y = """ + str(Y) + """;
  window.__look(x, z, Y, """ + str(pitch) + """, """ + str(dist) + """, false);
  window.__beforeRender = (dt, T) => { n.obj.rotation.y = """ + str(face) + """; n.obj.position.y = y0; const u = n.obj.userData;
    """ + body + """
    window.__C(x, y0 + """ + str(h) + """, z); P.cam.dist = Math.max(""" + str(dist - .3) + """, """ + str(dist) + """ - T * .1); P.cam.yaw = Y; P.cam.pitch = """ + str(pitch) + """; window.__clr([n], x, z, .5); }; }"""
def screen(clk, d0, d1, dur, yaw=0, pitch=.08):
    """the Kamera Jaga monitor, pushing in from d0 to d1 over `dur` s"""
    return """() => { """ + HEAD + """ window.__clock = """ + str(clk) + """; const o = window.__KJ, x = o.position.x + .2, z = o.position.z + .21, y = o.position.y + .64;
  window.__look(x, z, """ + str(yaw) + """, """ + str(pitch) + """, """ + str(d0) + """, false);
  window.__beforeRender = (dt, T) => { const q = Math.min(1, T / """ + str(dur) + """), e = q * q * (3 - 2 * q); window.__C(x, y, z); P.cam.dist = """ + str(d0) + """ + (""" + str(d1 - d0) + """) * e; P.cam.yaw = """ + str(yaw) + """; P.cam.pitch = """ + str(pitch) + """; window.__clr([], x, z, .5); }; }"""
fx = lambda js: js.replace('window.__fix45()', 'window.__fix46()')
# c1 cold open: night, the monitor: REC 02:13, a little orange kitten at the bait
C1 = screen(.86, 1.05, .78, 3.2)
# c2 premise aerial (ep45 c2)
C2 = fx(E45.C2)
# c3 orange fur on the crates (ep45 c6)
C3 = fx(E45.C6)
# c4 the detective: 'Detektif butuh ilmu.'
C4 = close('window.__AF', 1.0, .75, """if (u.body) u.body.rotation.x = 0;""", 2.0)
# c5 Pojok Ilmu from the front, slow push-in; c6 the plaque with Darwin's wish
C5 = """() => { """ + HEAD + """ const o = window.__PJK, x = o.position.x, z = o.position.z + .2, y = o.position.y + 1.5;
  window.__look(x, z, .25, .12, 6.0, false);
  window.__beforeRender = (dt, T) => { window.__C(x, y, z); P.cam.dist = Math.max(4.4, 6.0 - T * .3); P.cam.yaw = .25 - T * .03; P.cam.pitch = .12; window.__clr([], x, z, 1.4); }; }"""
C6 = """() => { """ + HEAD + """ const o = window.__PJK, x = o.position.x + .62, z = o.position.z + 1.29, y = o.position.y + 1.05;
  window.__look(x, z, .05, .05, 1.4, false);
  window.__beforeRender = (dt, T) => { window.__C(x, y, z); P.cam.dist = Math.max(.95, 1.4 - T * .09); P.cam.yaw = .05; P.cam.pitch = .05; window.__clr([], x, z, .5); }; }"""
# c7 D4L at the library, hands together: 'Boleh... aku pinjam bukunya?'
C7 = close('window.__D4', .3, .45, """if (u.armL) u.armL.rotation.x = -1.2; if (u.armR) u.armR.rotation.x = -1.2; if (u.body) u.body.rotation.z = Math.sin(T * 2.5) * .06;""", 2.0)
# c8 the detective, other side, thinking: 'Bulu oranye. Jari empat. Suka ikan...'
C8 = close('window.__AF', 1.0, .95, """if (u.body) u.body.rotation.x = .15 + Math.sin(T * 1.5) * .04;""", 1.9)
# c9 Luci: 'Hiu darat!' (finger up)
C9 = E45.C1.replace('window.__fix45()', 'window.__fix46()')
C9 = C9.replace(HEAD.replace('__fix46', '__fix45'), HEAD) if False else C9
# c10 the detective deadpan: 'Bukan, Bu Dokter. Kucing.'
C10 = close('window.__AF', 1.3, 1.3, """if (u.body) u.body.rotation.x = 0;""", 1.7)
# c11 dusk: the trap, camera on the tripod, the bait, the crates
C11 = """() => { """ + HEAD + """ window.__clock = .62; const o = window.__KJ, x = o.position.x - .3, z = o.position.z, y = o.position.y + .6;
  window.__look(x, z, .15, .5, 3.4, false);
  window.__beforeRender = (dt, T) => { window.__C(x, y, z); P.cam.dist = Math.max(2.4, 3.4 - T * .2); P.cam.yaw = .15 - T * .03; P.cam.pitch = .5; window.__clr([], x, z, .6); }; }"""
# c12 Aidil crying for the bait fish (dusk)
C12 = close('window.__AI', .3, .3, """if (u.armL) u.armL.rotation.x = -2.3 + Math.sin(T * 7) * .12; if (u.armR) u.armR.rotation.x = -2.3 + Math.cos(T * 7) * .12; n.obj.position.y = y0 + Math.abs(Math.sin(T * 5)) * .02;""", 2.0, clk=.62)
C13 = C11.replace('window.__clock = .62', 'window.__clock = .86')
# (old c13 framing) night: the trap with the eyes blinking between the crates, slow push
C13old = """() => { """ + HEAD + """ window.__clock = .86; const o = window.__KJ, x = o.position.x - .6, z = o.position.z, y = o.position.y + .45;
  window.__look(x, z, -.25, .42, 3.0, false);
  window.__beforeRender = (dt, T) => { window.__C(x, y, z); P.cam.dist = Math.max(1.8, 3.0 - T * .3); P.cam.yaw = -.25; P.cam.pitch = .42; window.__clr([], x, z, .6); }; }"""
# c14 night: the monitor close (payoff)
C14 = screen(.86, .9, .62, 3.5)
# c15 end: crane up over the harbour at night
C15 = """() => { """ + HEAD + """ window.__clock = .82; const x = 7.5, z = 37.0, y = P.surfaceY(x, z) + .6;
  window.__look(x, z, -.6, .35, 3.0, false);
  window.__beforeRender = (dt, T) => { const q = Math.min(1, T / 6), e = q * q * (3 - 2 * q); window.__C(x, y, z); P.cam.dist = 3.0 + 9 * e; P.cam.yaw = -.6 + .6 * e; P.cam.pitch = .35 + .55 * e; window.__clr([], x, z, .5); }; }"""
SHOTS = {'c1': (C1, 110), 'c2': (C2, 165), 'c3': (C3, 130), 'c4': (C4, 130), 'c5': (C5, 140), 'c6': (C6, 130), 'c7': (C7, 95),
         'c8': (C8, 170), 'c9': (C9, 50), 'c10': (C10, 80), 'c11': (C11, 185), 'c12': (C12, 90), 'c13': (C13, 120), 'c14': (C14, 135), 'c15': (C15, 300)}
CLEAR = E45.CLEAR
async def run(which):
    async with async_playwright() as p:
        b, pg = await setup(p)
        for js in CHAIN + (SETUP46,): await pg.evaluate(js)
        if os.environ.get('VARS'): await pg.evaluate('() => { ' + os.environ['VARS'] + ' }')
        if 'pos' in which: print(await pg.evaluate(POS))
        for k, (js, n) in SHOTS.items():
            if k in which and 'prev' not in which:
                await shoot(pg, 'e46' + k, int(os.environ.get('N_' + k, n)), start_js=js, warm=12)
                await pg.evaluate(CLEAR)
        if 'prev' in which:
            for k, (js, n) in SHOTS.items():
                if 'all' not in which and k not in which: continue
                await shoot(pg, 'p46' + k, 1, start_js=js, warm=int(os.environ.get('WARM', '40')))
                await pg.evaluate(CLEAR)
        await b.close()
if __name__ == "__main__": asyncio.run(run(sys.argv[1].split(",")))
