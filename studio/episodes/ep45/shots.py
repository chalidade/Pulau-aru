"""Episode 45 "Kalian Detektifnya" shot list (format KONSEP, run pagi 19 Nov).  usage: DPR=2 python3 shots.py c1,c3,...  (DPR=1 + prev for checks)
No new TikTok comments (Apify: APIFY_TOKEN still empty, Chrome not connected), so the episode sells the premise ('komentar = cerita, kalian
detektifnya') and moves the MISTERI IKAN BAKAR to part 2: the paw trail ends at new fish crates by the Pelabuhan Nelayan gate
(petiikan x61 y93: orange fur tufts = PETUNJUK #2, blinking little eyes in the gap), Detektif Pantai mhmmdalfaiz0 investigates,
Feros (nelayan) has been missing a fish every morning, Luci (sok tahu) insists on 'hiu darat', and a Papan Tersangka (x65 y91 r2) goes up.
World: crates (x61 y93) centre ~(6.0, 37.5); board (x65 y91) centre ~(10.0, 35.5) facing north; Luci spot (64,90)+(.3,.5) -> (8.8, 35.0); alfaiz (60,92)+(.6,.3) -> (5.1, 36.8).
"""
import asyncio, sys, os, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'lib'))
from harness import *
def _mod(name, path):
    sp = importlib.util.spec_from_file_location(name, path); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m
E44 = _mod('ep44shots', os.path.join(HERE, '..', 'ep44', 'shots.py'))
CHAIN = E44.CHAIN + (E44.SETUP44,)
SETUP45 = """() => { const P = window.__pulau;
  const F = s => P.npcs.find(n => n.name === s || (n.name || '').startsWith(s));
  window.__AF = () => F('mhmmdalfaiz0'); window.__LU = () => F('Luci'); window.__FE = () => F('muhamatferos197');
  let pi = null, pt = null; P.scene.traverse(o => { if (o.userData && o.userData.b && o.userData.b.type === 'petiikan') pi = o; if (o.userData && o.userData.b && o.userData.b.type === 'papantersangka') pt = o; });
  window.__PI = pi; window.__PT = pt;
  window.__fix45 = () => { window.__gone = 1; window.__fix44();
    for (const f of [window.__AF, window.__LU, window.__FE]) { const n = f(); if (!n) continue; n.obj.visible = true; const c = n.castSpot; if (c && n.spot && Math.hypot(n.spot.x - c.x, n.spot.z - c.z) > .3) n.spot = Object.assign({}, n.spot, c); if (c && Math.hypot(n.x - c.x, n.z - c.z) > .3) { n.x = c.x; n.z = c.z; n.tx = null; n.tz = null; n.moving = false; n.state = 'work'; n.obj.position.set(c.x, P.surfaceY(c.x, c.z), c.z); n.obj.rotation.y = c.face; } } };
}"""
POS = """() => { const o = {}; for (const [k, f] of Object.entries({ af: window.__AF, lu: window.__LU, fe: window.__FE })) { const n = f(); o[k] = n ? [n.name, +n.x.toFixed(2), +n.z.toFixed(2), +n.obj.position.y.toFixed(2), +n.obj.rotation.y.toFixed(2)] : null; }
  o.pi = window.__PI && [window.__PI.position.x, window.__PI.position.y, window.__PI.position.z]; o.pt = window.__PT && [window.__PT.position.x, window.__PT.position.y, window.__PT.position.z]; return o; }"""
CLK = os.environ.get('CLK', '.36')
HEAD = """const P = window.__pulau; window.__fix45(); window.__clock = """ + CLK + """; window.__cheer = null; P.player.obj.visible = false; """
def close(getter, face, Y, body, dist=2.1, h=1.12, clk=None):
    """a close-up of one resident facing `face`, camera at yaw Y, with per-frame arm/body code"""
    return """() => { """ + HEAD + ('' if clk is None else 'window.__clock = ' + str(clk) + ';') + """ const n = """ + getter + """(), x = n.x, z = n.z, y0 = P.surfaceY(x, z), Y = """ + str(Y) + """;
  window.__look(x, z, Y, .1, """ + str(dist) + """, false);
  window.__beforeRender = (dt, T) => { n.obj.rotation.y = """ + str(face) + """; n.obj.position.y = y0; const u = n.obj.userData;
    """ + body + """
    window.__C(x, y0 + """ + str(h) + """, z); P.cam.dist = Math.max(""" + str(dist - .3) + """, """ + str(dist) + """ - T * .1); P.cam.yaw = Y; P.cam.pitch = .1; window.__clr([n], x, z, .5); }; }"""
# c1 cold open (and c8): Luci by the suspect board, finger up: 'Pelakunya sudah jelas. Hiu darat!'
C1 = close('window.__LU', 3.9, 3.75, """if (u.armR) { u.armR.rotation.x = T < .9 ? -1.0 : -2.8; u.armR.rotation.z = -.15; } if (u.armL) u.armL.rotation.x = -.3; if (u.body) u.body.rotation.y = Math.sin(T * 3) * .08;
    n.obj.position.y = y0 + (T > 1.3 && T < 1.6 ? Math.sin((T - 1.3) / .3 * Math.PI) * .06 : 0);""")
# c8 'Hiu darat memang berbulu. Saya dokter, lho.' hand on chest, proud
C8 = close('window.__LU', 3.7, 3.55, """if (u.armR) { u.armR.rotation.x = -1.4; u.armR.rotation.z = .5; } if (u.armL) u.armL.rotation.x = -.2; if (u.body) u.body.rotation.x = -.08;""")
# c2 premise aerial (ep43/44): over the island gliding south to the beach
C2 = E44.C2.replace('window.__gone = 0; window.__fix44()', 'window.__fix45()')
# c3 the table: one plate holds only a bone (ep44 c13)
C3 = E44.C13.replace('window.__gone = 0; window.__fix44()', 'window.__fix45()')
# c4 the paw prints, gliding toward the harbour (ep44 c15)
C4 = E44.C15.replace('window.__gone = 0; window.__fix44()', 'window.__fix45()')
# c5 Detektif Pantai at the crates with his magnifier: 'Detektif Pantai turun tangan.'
C5 = close('window.__AF', 1.0, .75, """if (u.body) u.body.rotation.x = T < 1.5 ? 0 : .25;""", 2.0)
# c9 'Hiu tidak punya bulu, Bu Dokter.' deadpan, straight to camera
C9 = close('window.__AF', 1.3, 1.3, """if (u.body) u.body.rotation.x = 0;""", 1.8)
# c6 the crates close: orange fur on the corner and the evidence tag
C6 = """() => { """ + HEAD + """ const o = window.__PI, x = o.position.x - .95, z = o.position.z + .3, y = P.surfaceY(x, z) + .45, Y = +(window.__Y6 || .2);
  window.__look(x, z, Y, .25, 2.5, false);
  window.__beforeRender = (dt, T) => { window.__C(x + T * .05, y, z); P.cam.dist = Math.max(1.9, 2.5 - T * .13); P.cam.yaw = Y; P.cam.pitch = .25; window.__clr([], x, z, .5); }; }"""
# c7 Feros on the harbour deck, turning to the camera: 'Pantas! Tiap pagi ikanku kurang satu.'
C7 = close('window.__FE', -.15, -.2, """if (u.armL) u.armL.rotation.x = -2.6 + Math.sin(T * 9) * .15; if (u.body) u.body.rotation.y = Math.sin(T * 4) * .1;""", 2.2)
# c10 the Papan Tersangka from the front, slow push-in; c11 drift to the '???' photo
C10 = """() => { """ + HEAD + """ const o = window.__PT, x = o.position.x, z = o.position.z, y = P.surfaceY(x, z) + 1.5;
  window.__look(x, z, 3.14, .12, 3.0, false);
  window.__beforeRender = (dt, T) => { window.__C(x, y, z); P.cam.dist = Math.max(2.3, 3.0 - T * .15); P.cam.yaw = 3.14; P.cam.pitch = .12; window.__clr([], x, z, .5); }; }"""
C11 = """() => { """ + HEAD + """ const o = window.__PT, x = o.position.x, z = o.position.z, y = P.surfaceY(x, z) + 1.5;
  window.__look(x, z, 3.14, .1, 2.0, false);
  window.__beforeRender = (dt, T) => { const q = Math.min(1, T / 3), e = q * q * (3 - 2 * q); window.__C(x + .55 * e * +(window.__SX || -1), y, z); P.cam.dist = 2.0 - .6 * e; P.cam.yaw = 3.14; P.cam.pitch = .1; window.__clr([], x, z, .5); }; }"""
# c12 night: push in on the dark gap between the crates, two little eyes blink
C12 = """() => { """ + HEAD + """ window.__clock = .86; const o = window.__PI, x = o.position.x - .22, z = o.position.z + .4, y = P.surfaceY(x, z) + .3, Y = +(window.__Y12 || .15);
  window.__look(x, z, Y, .12, 2.4, false);
  window.__beforeRender = (dt, T) => { window.__C(x, y, z); P.cam.dist = Math.max(.9, 2.4 - T * .32); P.cam.yaw = Y; P.cam.pitch = .12; window.__clr([], x, z, .5); }; }"""
# c13 end: crane up over the beach and the harbour (ep44 c16), dusk
C13 = """() => { """ + HEAD + """ window.__clock = .6; const x = 7.5, z = 37.0, y = P.surfaceY(x, z) + .6;
  window.__look(x, z, -.6, .35, 3.0, false);
  window.__beforeRender = (dt, T) => { const q = Math.min(1, T / 6), e = q * q * (3 - 2 * q); window.__C(x, y, z); P.cam.dist = 3.0 + 9 * e; P.cam.yaw = -.6 + .6 * e; P.cam.pitch = .35 + .55 * e; window.__clr([], x, z, .5); }; }"""
SHOTS = {'c1': (C1, 100), 'c2': (C2, 150), 'c3': (C3, 145), 'c4': (C4, 115), 'c5': (C5, 135), 'c6': (C6, 135), 'c7': (C7, 120),
         'c8': (C8, 120), 'c9': (C9, 75), 'c10': (C10, 150), 'c11': (C11, 155), 'c12': (C12, 160), 'c13': (C13, 300)}
CLEAR = E44.CLEAR
async def run(which):
    async with async_playwright() as p:
        b, pg = await setup(p)
        for js in CHAIN + (SETUP45,): await pg.evaluate(js)
        if os.environ.get('VARS'): await pg.evaluate('() => { ' + os.environ['VARS'] + ' }')
        if 'pos' in which: print(await pg.evaluate(POS))
        for k, (js, n) in SHOTS.items():
            if k in which and 'prev' not in which:
                await shoot(pg, 'e45' + k, int(os.environ.get('N_' + k, n)), start_js=js, warm=12)
                await pg.evaluate(CLEAR)
        if 'prev' in which:
            for k, (js, n) in SHOTS.items():
                if 'all' not in which and k not in which: continue
                await shoot(pg, 'p45' + k, 1, start_js=js, warm=int(os.environ.get('WARM', '40')))
                await pg.evaluate(CLEAR)
        await b.close()
if __name__ == "__main__": asyncio.run(run(sys.argv[1].split(",")))
