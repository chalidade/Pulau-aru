"""Episode 47 "Pencurinya Ketemu!" shot list (format KONSEP, run pagi 20 Nov).  usage: DPR=2 python3 shots.py c1,c3,...  (DPR=1 + prev for checks)
No new TikTok comments (Chrome not connected, komentar.md has none), so the episode closes the MISTERI IKAN BAKAR (part 4): the thief is a
hungry orange kitten hiding in the gap of the Peti Ikan; Mbak Sekar gives it a warm fish, the Detektif closes the case and the island
builds a Rumah Kucing (rumahkucing x66 y87, next to Pojok Ilmu) with a name sign 'NAMAKU: ???' (name from the comments).
Cast: Alexandre (Si Pahlawan, first scene), inyuu (Si Gamer, 'pet langka!'), Mbak Sekar, mhmmdalfaiz0.
"""
import asyncio, sys, os, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'lib'))
from harness import *
def _mod(name, path):
    sp = importlib.util.spec_from_file_location(name, path); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m
E46 = _mod('ep46shots', os.path.join(HERE, '..', 'ep46', 'shots.py'))
E45 = E46.E45
CHAIN = E46.CHAIN + (E46.SETUP46,)
SETUP47 = """() => { const P = window.__pulau;
  const F = s => P.npcs.find(n => n.name === s || (n.name || '').startsWith(s));
  window.__AX = () => F('Alexandre'); window.__INY = () => F('inyuu');
  let rk = null; P.scene.traverse(o => { if (o.userData && o.userData.b && o.userData.b.type === 'rumahkucing') rk = o; });
  window.__RK = rk; const K = rk.userData.kitten;
  const hi = K.children.indexOf(K.userData.head), ti = K.children.indexOf(K.userData.tail);
  window.__KW = () => { const v = K.position.clone(); K.parent.localToWorld(v); return v; };
  // a staged clone of the kitten peeking out of the gap between the fish crates (flashback before the adoption)
  const kp = K.clone(true); kp.userData = { head: kp.children[hi], tail: kp.children[ti] }; kp.visible = false; P.scene.add(kp); window.__KP = kp;
  window.__kitPeti = on => { kp.visible = !!on; if (!on) return; const o = window.__PI, v = K.position.clone().set(-.22, .0, .3); o.localToWorld(v); kp.position.copy(v); kp.rotation.y = o.rotation.y + .25; kp.scale.setScalar(1.25); };
  window.__fix47 = () => { window.__fix46(); window.__kitPeti(false);
    for (const f of [window.__AX, window.__INY, window.__SK]) { const n = f(); if (!n) continue; n.obj.visible = true; const c = n.castSpot; if (c && n.spot && Math.hypot(n.spot.x - c.x, n.spot.z - c.z) > .3) n.spot = Object.assign({}, n.spot, c); if (c && Math.hypot(n.x - c.x, n.z - c.z) > .3) { n.x = c.x; n.z = c.z; n.tx = null; n.tz = null; n.moving = false; n.state = 'work'; n.obj.position.set(c.x, P.surfaceY(c.x, c.z), c.z); n.obj.rotation.y = c.face; } } };
}"""
POS = """() => { const o = {}; for (const [k, f] of Object.entries({ af: window.__AF, ax: window.__AX, iny: window.__INY, sk: window.__SK })) { const n = f(); o[k] = n ? [n.name, +n.x.toFixed(2), +n.z.toFixed(2), +n.obj.position.y.toFixed(2), +n.obj.rotation.y.toFixed(2)] : null; }
  const k = window.__KW(); o.kit = [k.x, k.y, k.z]; o.rk = [window.__RK.position.x, window.__RK.position.y, window.__RK.position.z, window.__RK.rotation.y]; o.pi = [window.__PI.position.x, window.__PI.position.z]; return o; }"""
CLK = os.environ.get('CLK', '.36')
HEAD = """const P = window.__pulau; window.__fix47(); window.__clock = """ + CLK + """; window.__cheer = null; P.player.obj.visible = false; """
def close(getter, face, Y, body, dist=2.1, h=1.12, clk=None, pitch=.1):
    return """() => { """ + HEAD + ('' if clk is None else 'window.__clock = ' + str(clk) + ';') + """ const n = """ + getter + """(), x = n.x, z = n.z, y0 = P.surfaceY(x, z), Y = """ + str(Y) + """;
  window.__look(x, z, Y, """ + str(pitch) + """, """ + str(dist) + """, false);
  window.__beforeRender = (dt, T) => { n.obj.rotation.y = """ + str(face) + """; n.obj.position.y = y0; const u = n.obj.userData;
    """ + body + """
    window.__C(x, y0 + """ + str(h) + """, z); P.cam.dist = Math.max(""" + str(dist - .3) + """, """ + str(dist) + """ - T * .1); P.cam.yaw = Y; P.cam.pitch = """ + str(pitch) + """; window.__clr([n], x, z, .5); }; }"""
def kit(Y, pitch, d0, d1, dur, dy=.42, extra=''):
    """the adopted kitten at the Rumah Kucing, pushing in from d0 to d1"""
    return """() => { """ + HEAD + extra + """ const k = window.__KW(), x = k.x, z = k.z, y = k.y + """ + str(dy) + """;
  window.__look(x, z, """ + str(Y) + """, """ + str(pitch) + """, """ + str(d0) + """, false);
  window.__beforeRender = (dt, T) => { const q = Math.min(1, T / """ + str(dur) + """), e = q * q * (3 - 2 * q); window.__C(x, y, z); P.cam.dist = """ + str(d0) + """ + (""" + str(d1 - d0) + """) * e; P.cam.yaw = """ + str(Y) + """; P.cam.pitch = """ + str(pitch) + """; window.__clr([], x, z, .6); }; }"""
def peti(Y, pitch, d0, d1, dur, dy=.4):
    """the kitten clone peeking out of the crate gap"""
    return """() => { """ + HEAD + """ window.__kitPeti(true); const k = window.__KP, x = k.position.x, z = k.position.z, y = k.position.y + """ + str(dy) + """;
  window.__look(x, z, """ + str(Y) + """, """ + str(pitch) + """, """ + str(d0) + """, false);
  window.__beforeRender = (dt, T) => { const q = Math.min(1, T / """ + str(dur) + """), e = q * q * (3 - 2 * q); const u = k.userData; u.tail.rotation.z = Math.sin(T * 2.4) * .4; u.head.rotation.z = Math.sin(T * 1.7) * .25; u.head.rotation.y = Math.sin(T * .9) * .3;
    window.__C(x, y, z); P.cam.dist = """ + str(d0) + """ + (""" + str(d1 - d0) + """) * e; P.cam.yaw = """ + str(Y) + """; P.cam.pitch = """ + str(pitch) + """; window.__clr([], x, z, .6); }; }"""
fx = lambda js: js.replace('window.__fix45()', 'window.__fix47()').replace('window.__fix46()', 'window.__fix47()')
Y1 = float(os.environ.get('Y1', '.15'))
# c1 cold open: the kitten close at its new home (flash-forward)
C1 = kit(Y1, .18, 1.25, .95, 3.0)
# c2 premise aerial (ep45 c2)
C2 = fx(E45.C2)
# c3 the Kamera Jaga monitor (day): the recorded kitten
C3 = fx(E46.screen(.36, 1.0, .75, 3.0))
# c4 the detective: 'Pagi ini kita tangkap. Pelan-pelan.'
C4 = close('window.__AF', 1.0, .75, """if (u.body) u.body.rotation.x = 0;""", 2.0)
# c5 Alexandre, hero pose: 'Serahkan padaku!'
C5 = close('window.__AX', 0, float(os.environ.get('Y5', '.25')), """if (u.armR) { u.armR.rotation.x = T < .6 ? -1.0 : -3.0; u.armR.rotation.z = -.2; } if (u.armL) u.armL.rotation.x = -.4; n.obj.position.y = y0 + (T > .5 && T < .8 ? Math.sin((T - .5) / .3 * Math.PI) * .08 : 0);""", 2.0)
# c6 the crates: the kitten peeking from the gap; c7 closer, low
C6 = peti(float(os.environ.get('Y6', '.2')), .22, 2.0, 1.4, 3.0)
C7 = peti(float(os.environ.get('Y6', '.2')) + .3, .2, 1.1, .9, 3.0, dy=.32)
# c8 Mbak Sekar at the Meja Dua Ikan
C8 = close('window.__SK', float(os.environ.get('F8', '2.0')), float(os.environ.get('Y8', '2.0')), """if (u.body) u.body.rotation.z = Math.sin(T * 2) * .04;""", 2.2, h=float(os.environ.get("H8", "1.2")))
# c9 inyuu, gamer pose: 'Pet langka muncul!'
C9 = close('window.__INY', float(os.environ.get('F9', '0')), float(os.environ.get('Y9', '-.2')), """if (u.armL) u.armL.rotation.x = -1.3 + Math.sin(T * 14) * .1; if (u.armR) u.armR.rotation.x = -1.3 + Math.cos(T * 14) * .1; n.obj.position.y = y0 + Math.abs(Math.sin(T * 6)) * .03;""", 2.0)
# c10 the detective, deadpan: 'Kasus ditutup.'
C10 = close('window.__AF', 1.3, 1.3, """if (u.body) u.body.rotation.x = 0;""", 1.7)
# c11 the Rumah Kucing, wide push-in (Alexandre and inyuu beside it)
C11 = """() => { """ + HEAD + """ const o = window.__RK, x = o.position.x, z = o.position.z + .3, y = o.position.y + .6;
  const Y = +(window.__Y11 || .8); window.__look(x, z, Y, .42, 3.6, false);
  window.__beforeRender = (dt, T) => { window.__C(x, y, z); P.cam.dist = Math.max(2.6, 3.6 - T * .25); P.cam.yaw = Y - T * .04; P.cam.pitch = .42; window.__clr([], x, z, .8); }; }"""
# c12 the name sign: NAMAKU: ???
C12 = """() => { """ + HEAD + """ const o = window.__RK, v = o.position.clone().set(.8, 1.18, -.26); o.localToWorld(v); const x = v.x, z = v.z, y = v.y;
  window.__look(x, z, .05, .05, 2.1, false);
  window.__beforeRender = (dt, T) => { window.__C(x, y, z); P.cam.dist = Math.max(1.6, 2.1 - T * .12); P.cam.yaw = .05; P.cam.pitch = .05; window.__clr([], x, z, .5); }; }"""
# c13 end: from the kitten, crane up over the harbour
C13 = """() => { """ + HEAD + """ const k = window.__KW(), x = k.x, z = k.z, y = k.y + .4;
  window.__look(x, z, .15, .2, 1.1, false);
  window.__beforeRender = (dt, T) => { const q = Math.min(1, T / 6), e = q * q * (3 - 2 * q); window.__C(x, y, z); P.cam.dist = 1.1 + 11 * e; P.cam.yaw = .15 + .5 * e; P.cam.pitch = .2 + .9 * Math.min(1, T / 1.5); window.__clr([], x, z, .6); }; }"""
SHOTS = {'c1': (C1, 110), 'c2': (C2, 165), 'c3': (C3, 160), 'c4': (C4, 110), 'c5': (C5, 105), 'c6': (C6, 100), 'c7': (C7, 100),
         'c8': (C8, 150), 'c9': (C9, 130), 'c10': (C10, 160), 'c11': (C11, 150), 'c12': (C12, 180), 'c13': (C13, 300)}
CLEAR = E46.CLEAR
async def run(which):
    async with async_playwright() as p:
        b, pg = await setup(p)
        for js in CHAIN + (SETUP47,): await pg.evaluate(js)
        if os.environ.get('VARS'): await pg.evaluate('() => { ' + os.environ['VARS'] + ' }')
        if 'pos' in which: print(await pg.evaluate(POS))
        for k, (js, n) in SHOTS.items():
            if k in which and 'prev' not in which:
                await shoot(pg, 'e47' + k, int(os.environ.get('N_' + k, n)), start_js=js, warm=12)
                await pg.evaluate(CLEAR)
        if 'prev' in which:
            for k, (js, n) in SHOTS.items():
                if 'all' not in which and k not in which: continue
                await shoot(pg, 'p47' + k, 1, start_js=js, warm=int(os.environ.get('WARM', '40')))
                await pg.evaluate(CLEAR)
        await b.close()
if __name__ == "__main__": asyncio.run(run(sys.argv[1].split(",")))
