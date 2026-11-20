"""Episode 48 "Obat Galau di Kolam Renang" shot list (format CERITA, run sore 20 Nov).  usage: DPR=2 python3 shots.py c1,c3,...  (DPR=1 + prev for checks)
Two real comments (komentar.md, collected via TikTok Studio 20 Nov): @im.safar4 "bikin kolam renang aku udah follow dan paket lengkap"
-> Kolam Renang (kolamrenang x87 y82 r2, south of the east street next to the market), Safar on the diving board (pose 'dive');
@riskki.setya "aku dan galau aku Riski" -> Riski (Si Galau) sitting on the pool rim (pose 'galau'); senar muliya sings him a sad
song (string breaks), lala cute brings him a strawberry cake. All of them are resident spots in island.json (live on the web).
"""
import asyncio, sys, os, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'lib'))
from harness import *
def _mod(name, path):
    sp = importlib.util.spec_from_file_location(name, path); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m
E47 = _mod('ep47shots', os.path.join(HERE, '..', 'ep47', 'shots.py'))
CHAIN = E47.CHAIN + (E47.SETUP47,)
SETUP48 = """() => { const P = window.__pulau;
  const F = s => P.npcs.find(n => n.name === s || (n.name || '').startsWith(s));
  window.__RIS = () => F('riskki.setya'); window.__SAF = () => F('im.safar4'); window.__LAL = () => F('lala cute'); window.__SNR = () => F('senar muliya');
  let kr = null; P.scene.traverse(o => { if (o.userData && o.userData.b && o.userData.b.type === 'kolamrenang') kr = o; }); window.__KRN = kr;
  window.__fix48 = () => { window.__fix47();
    for (const f of [window.__RIS, window.__SAF, window.__LAL, window.__SNR]) { const n = f(); if (!n) continue; n.obj.visible = true; const c = n.castSpot; if (c && n.spot && Math.hypot(n.spot.x - c.x, n.spot.z - c.z) > .3) n.spot = Object.assign({}, n.spot, c); if (c && Math.hypot(n.x - c.x, n.z - c.z) > .3) { n.x = c.x; n.z = c.z; n.tx = null; n.tz = null; n.moving = false; n.state = 'work'; n.obj.position.set(c.x, P.surfaceY(c.x, c.z) + (c.y || 0), c.z); n.obj.rotation.y = c.face; } } };
}"""
POS = """() => { const o = {}; for (const [k, f] of Object.entries({ rs: window.__RIS, sf: window.__SAF, ll: window.__LAL, sn: window.__SNR })) { const n = f(); o[k] = n ? [n.name, +n.x.toFixed(2), +n.z.toFixed(2), +n.obj.position.y.toFixed(2), +n.obj.rotation.y.toFixed(2), n.role] : null; }
  o.kr = [window.__KRN.position.x, window.__KRN.position.y, window.__KRN.position.z, window.__KRN.rotation.y]; return o; }"""
CLK = os.environ.get('CLK', '.42')
HEAD = """const P = window.__pulau; window.__fix48(); window.__clock = """ + CLK + """; window.__cheer = null; P.player.obj.visible = false; """
def close(getter, Y, h, d0, d1=None, pitch=.1, dur=3.0, extra='', dyaw=0.0):
    """close-up of a cast member in their own live pose (no position override: they sit/stand where the game puts them)"""
    d1 = d0 - .3 if d1 is None else d1
    return """() => { """ + HEAD + extra + """ const n = """ + getter + """(), x = n.x, z = n.z, y = n.obj.position.y + """ + str(h) + """;
  window.__look(x, z, """ + str(Y) + """, """ + str(pitch) + """, """ + str(d0) + """, false);
  window.__beforeRender = (dt, T) => { const q = Math.min(1, T / """ + str(dur) + """), e = q * q * (3 - 2 * q); window.__C(x, y, z); P.cam.dist = """ + str(d0) + """ + (""" + str(d1 - d0) + """) * e; P.cam.yaw = """ + str(Y) + """ + """ + str(dyaw) + """ * e; P.cam.pitch = """ + str(pitch) + """; window.__clr([n], x, z, .5); }; }"""
def pool(lx, lz, ly, Y0, Y1, p0, p1, d0, d1, dur, cheer='null', lx1=None, lz1=None):
    """a camera on a point of the pool (local metres of the kolamrenang model), easing yaw/pitch/dist (and target) over dur"""
    lx1 = lx if lx1 is None else lx1; lz1 = lz if lz1 is None else lz1
    return """() => { """ + HEAD + """ window.__cheer = """ + cheer + """; const o = window.__KRN, a = o.position.clone().set(""" + f"{lx}, {ly}, {lz}" + """), b = o.position.clone().set(""" + f"{lx1}, {ly}, {lz1}" + """); o.localToWorld(a); o.localToWorld(b);
  window.__look(a.x, a.z, """ + str(Y0) + """, """ + str(p0) + """, """ + str(d0) + """, false);
  window.__beforeRender = (dt, T) => { const q = Math.min(1, T / """ + str(dur) + """), e = q * q * (3 - 2 * q); const x = a.x + (b.x - a.x) * e, z = a.z + (b.z - a.z) * e;
    window.__C(x, a.y, z); P.cam.dist = """ + str(d0) + """ + (""" + str(d1 - d0) + """) * e; P.cam.yaw = """ + str(Y0) + """ + (""" + str(Y1 - Y0) + """) * e; P.cam.pitch = """ + str(p0) + """ + (""" + str(p1 - p0) + """) * e; window.__clr([], x, z, .6); }; }"""
Y1 = float(os.environ.get('Y1', '-.15'))
# c1 cold open: Riski on the pool rim, head down (close, pushing in)
C1 = close('window.__RIS', Y1, .78, 2.3, 1.85, pitch=.14)
# c2 premise: high aerial descending onto the new pool
C2 = pool(0, -.3, 0, .3, .65, 1.1, .85, 55, 15, 4.6)
# c3 under the comment cards: slow wide pan over the pool
C3 = pool(0, -.3, 0, .55, .75, .75, .7, 11, 9.5, 4.5)
# c4 the pool from the sign side (south), sign in the foreground
C4 = pool(0, -.6, .5, -2.9, -3.2, .42, .38, 9.5, 7.8, 5.4)
# c5 details: dolly over the lane ropes past the duck float
C5 = pool(1.6, -.3, .2, 2.2, 2.0, .5, .45, 3.6, 3.2, 5.2, lx1=-1.4, lz1=-.6)
# c6 Safar on the diving board (faces the pool, +x)
C6 = close('window.__SAF', float(os.environ.get('Y6', '1.35')), 1.15, 2.4, 2.0, pitch=.12)
# c7 Riski, from the water side, low
C7 = close('window.__RIS', float(os.environ.get('Y7', '-.15')), .78, 1.6, 1.35, pitch=.05)
# c8 senar muliya with the guitar
C8 = close('window.__SNR', float(os.environ.get('Y8', '1.0')), 1.1, 2.1, 1.8, pitch=.1)
# c9 Riski, very close, deadpan: 'makin galau'
C9 = close('window.__RIS', .32, .8, 1.75, 1.65, pitch=.12, dur=1.5)
# c10 lala cute with the cake
C10 = close('window.__LAL', float(os.environ.get('Y10', '-.8')), 1.1, 2.1, 1.8, pitch=.1)
# c11 two-shot Riski + lala
C11 = """() => { """ + HEAD + """ const a = window.__RIS(), b = window.__LAL(), x = (a.x + b.x) / 2, z = (a.z + b.z) / 2, y = a.obj.position.y + .65;
  const Y = +(window.__Y11 || -.25); window.__look(x, z, Y, .18, 3.0, false);
  window.__beforeRender = (dt, T) => { window.__C(x, y, z); P.cam.dist = Math.max(2.5, 3.0 - T * .12); P.cam.yaw = Y; P.cam.pitch = .18; window.__clr([a, b], x, z, .6); }; }"""
# c12 the little group at the rim, wide, crowd cheering
C12 = """() => { """ + HEAD + """ window.__cheer = true; const a = window.__RIS(), x = a.x - .2, z = a.z - .2, y = a.obj.position.y + .5;
  window.__look(x, z, .2, .35, 4.6, false);
  window.__beforeRender = (dt, T) => { window.__C(x, y, z); P.cam.dist = Math.max(3.7, 4.6 - T * .2); P.cam.yaw = .2 + T * .03; P.cam.pitch = .35; window.__clr([a, window.__LAL(), window.__SNR()], x, z, .6); }; }"""
# c13 end: from Riski, crane up over the pool
C13 = """() => { """ + HEAD + """ const a = window.__RIS(), x = a.x, z = a.z, y = a.obj.position.y + .7;
  window.__look(x, z, .2, .2, 1.5, false);
  window.__beforeRender = (dt, T) => { const q = Math.min(1, T / 6), e = q * q * (3 - 2 * q); window.__C(x, y, z + 1.5 * e); P.cam.dist = 1.5 + 13 * e; P.cam.yaw = .2 + .6 * e; P.cam.pitch = .2 + .8 * Math.min(1, T / 2); window.__clr([a, window.__LAL(), window.__SNR()], x, z, .6); }; }"""
SHOTS = {'c1': (C1, 120), 'c2': (C2, 160), 'c3': (C3, 155), 'c4': (C4, 185), 'c5': (C5, 180), 'c6': (C6, 125), 'c7': (C7, 135),
         'c8': (C8, 170), 'c9': (C9, 60), 'c10': (C10, 160), 'c11': (C11, 165), 'c12': (C12, 160), 'c13': (C13, 230)}
CLEAR = E47.CLEAR
async def run(which):
    async with async_playwright() as p:
        b, pg = await setup(p)
        for js in CHAIN + (SETUP48,): await pg.evaluate(js)
        if os.environ.get('VARS'): await pg.evaluate('() => { ' + os.environ['VARS'] + ' }')
        if 'pos' in which: print(await pg.evaluate(POS))
        for k, (js, n) in SHOTS.items():
            if k in which and 'prev' not in which:
                await shoot(pg, 'e48' + k, int(os.environ.get('N_' + k, n)), start_js=js, warm=12)
                await pg.evaluate(CLEAR)
        if 'prev' in which:
            for k, (js, n) in SHOTS.items():
                if 'all' not in which and k not in which: continue
                await shoot(pg, 'p48' + k, 1, start_js=js, warm=int(os.environ.get('WARM', '40')))
                await pg.evaluate(CLEAR)
        await b.close()
if __name__ == "__main__": asyncio.run(run(sys.argv[1].split(",")))
