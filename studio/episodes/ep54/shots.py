"""Episode 54 "Enam Episode di Papan Loncat" shot list (format CERITA, run sore 23 Nov).  usage: DPR=2 python3 shots.py c1,c3,...  (DPR=1 + prev for checks)
No new comments (komentar.md empty, traktir.json nothing new, Chrome not connected): the episode pays off the running gag from ep 48, @im.safar4
on the diving board who never jumps. Riski (Si Galau) on the rim, lala cute counting, the Pos Gotong Royong board gets a third job
('Bantu Safar loncat'), -VANZwlee (Si Paling Keren) shows 'how it's done' (his anime pose and stumble), and Safar finally jumps: a belly flop.
Riski gets splashed and laughs. A Papan Skor Loncat goes up at the pool.
Live state (island.json + code): Safar pose 'loncat' (the full jump cycle every 14 s, splash), Riski's 'galau' laughs at each splash,
-VANZwlee's spot moved to the pool deck (oldSpot = name stone), kolamrenang b.score (scoreboard), posgotong b.tasks + 'Bantu Safar loncat'.
Staged only: the jump clock (window.__diveT) so each shot shows the right moment of the cycle.
"""
import asyncio, sys, os, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'lib'))
from harness import *
def _mod(name, path):
    sp = importlib.util.spec_from_file_location(name, path); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m
E53 = _mod('ep53shots', os.path.join(HERE, '..', 'ep53', 'shots.py'))
CHAIN = E53.CHAIN + (E53.SETUP53,)
SETUP54 = """() => { const P = window.__pulau;
  const F = s => P.npcs.find(n => n.name === s || (n.name || '').startsWith(s) || n.tampil === s);
  window.__SAF = () => F('im.safar4'); window.__RIS = () => F('riskki.setya'); window.__LAL = () => F('alivia_vi') || F('lala cute'); window.__VNZ = () => F('-VANZwlee');
  const B = {}; P.scene.traverse(o => { if (o.userData && o.userData.b && ['kolamrenang', 'posgotong'].includes(o.userData.b.type)) B[o.userData.b.type] = o; });
  window.__B54 = B;
  window.__fix54 = () => { window.__fix53();
    for (const f of [window.__SAF, window.__RIS, window.__LAL, window.__VNZ]) { const n = f(); if (!n) continue; n.obj.visible = true; const c = n.castSpot; if (c && n.spot) { n.spot = Object.assign({}, n.spot, c); } if (c && Math.hypot(n.x - c.x, n.z - c.z) > .3) { n.x = c.x; n.z = c.z; n.tx = null; n.tz = null; n.moving = false; n.state = 'work'; n.obj.position.set(c.x, P.surfaceY(c.x, c.z) + (c.y || 0), c.z); } if (c) n.obj.rotation.y = c.face; } };
}"""
POS = """() => { const o = {}; for (const [k, f] of Object.entries({ sf: window.__SAF, rs: window.__RIS, ll: window.__LAL, vz: window.__VNZ })) { const n = f(); o[k] = n ? [n.name, +n.x.toFixed(2), +n.z.toFixed(2), +n.obj.position.y.toFixed(2), +n.obj.rotation.y.toFixed(2), n.role, n.spot && n.spot.pose] : null; }
  for (const [k, b] of Object.entries(window.__B54)) o[k] = [b.position.x, b.position.y, b.position.z, b.rotation.y, b.scale.x]; return o; }"""
CLK = os.environ.get('CLK', '.45')
def head(dt):
    return """const P = window.__pulau; window.__fix54(); window.__clock = """ + CLK + """; window.__cheer = null; window.__cartPos = 1; window.__diveT = """ + str(dt) + """; P.player.obj.visible = false; P.scene.traverse(o => { const g = o.isInstancedMesh && o.geometry.parameters; if (g && ((g.height === 1.4 && g.radiusTop === .04) || (g.width === .18 && g.height === .22))) o.visible = false; }); """
def dive(d0, rate=1.0):
    """per-frame jump clock: starts at d0 seconds into the 14 s cycle (None = keep it pinned at the bounce)"""
    return "window.__diveT = Math.min(13.9, " + str(d0) + " + T * " + str(rate) + ");"
def close(getter, Y, h, d0, d1=None, pitch=.1, dur=3.0, extra='', dyaw=0.0, cheer='null', ox=0.0, oz=0.0, dt=1.0, frame='', keep='[]'):
    d1 = d0 - .3 if d1 is None else d1
    return """() => { """ + head(dt) + extra + """ window.__cheer = """ + cheer + """; const n = """ + getter + """(), x = n.x + """ + str(ox) + """, z = n.z + """ + str(oz) + """, y = Math.max(n.obj.position.y, P.surfaceY(n.x, n.z)) + """ + str(h) + """;
  window.__look(x, z, """ + str(Y) + """, """ + str(pitch) + """, """ + str(d0) + """, false);
  window.__beforeRender = (dt, T) => { """ + frame + """ const q = Math.min(1, T / """ + str(dur) + """), e = q * q * (3 - 2 * q); window.__C(x, y, z); P.cam.dist = """ + str(d0) + """ + (""" + str(d1 - d0) + """) * e; P.cam.yaw = """ + str(Y) + """ + """ + str(dyaw) + """ * e; P.cam.pitch = """ + str(pitch) + """; window.__clr([n].concat(""" + keep + """.map(g => g())), x, z, .5); }; }"""
def bld(key, lx, lz, ly, Y0, Y1, p0, p1, d0, d1, dur, cheer='null', lx1=None, lz1=None, extra='', dt=1.0, frame=''):
    lx1 = lx if lx1 is None else lx1; lz1 = lz if lz1 is None else lz1
    return """() => { """ + head(dt) + extra + """ window.__cheer = """ + cheer + """; const o = window.__B54['""" + key + """'], k = o.scale.x || 1, a = o.position.clone().set(""" + f"{lx}*k, {ly}*k, {lz}*k" + """), b = o.position.clone().set(""" + f"{lx1}*k, {ly}*k, {lz1}*k" + """); o.localToWorld(a.divideScalar(k)); o.localToWorld(b.divideScalar(k));
  window.__look(a.x, a.z, """ + str(Y0) + """, """ + str(p0) + """, """ + str(d0) + """, false);
  window.__beforeRender = (dt, T) => { """ + frame + """ const q = Math.min(1, T / """ + str(dur) + """), e = q * q * (3 - 2 * q); const x = a.x + (b.x - a.x) * e, z = a.z + (b.z - a.z) * e;
    window.__C(x, a.y, z); P.cam.dist = """ + str(d0) + """ + (""" + str(d1 - d0) + """) * e; P.cam.yaw = """ + str(Y0) + """ + (""" + str(Y1 - Y0) + """) * e; P.cam.pitch = """ + str(p0) + """ + (""" + str(p1 - p0) + """) * e; window.__clr([], x, z, .6); }; }"""
E = os.environ.get
f = lambda k, d: float(E(k, d))
SAF, RIS, LAL, VNZ = 'window.__SAF', 'window.__RIS', 'window.__LAL', 'window.__VNZ'
# c1 cold open (flash-forward): Safar on the board, 3/4 front, he crouches and belly-flops toward the camera side (splash at ~3.0 s)
C1 = close(SAF, f('Y1', '1.45'), f('H1', '1.25'), f('D1', '4.0'), f('D1', '4.0') - .4, pitch=f('P1', '.2'), ox=.6, keep='[window.__RIS]', dt=1.9, frame=dive(1.9))
# c2 premise: aerial descending onto the pool (Safar bouncing, tiny)
C2 = bld('kolamrenang', 0, -.3, 0, .35, .6, 1.1, .85, 55, 14, 4.0)
# c3 Safar on the board, bouncing, never jumping (narrator)
C3 = close(SAF, f('Y3', '1.35'), 1.15, 2.6, 2.1, pitch=.12, dur=4.8, dt=0, frame=dive(0, .6))
# c4 Safar close: 'Siap... loncat! ...bentar'
C4 = close(SAF, f('Y4', '1.0'), 1.2, 1.9, 1.7, pitch=.1, dt=.5, frame=dive(.5, .7))
# c5 Riski on the rim, galau
C5 = close(RIS, f('Y5', '-.15'), .78, 2.0, 1.7, pitch=.12, dt=1.0)
# c6 lala cute counting
C6 = close(LAL, f('Y6', '-.8'), 1.1, 2.0, 1.75, pitch=.1, dt=1.0)
# c7 Safar: 'Tunggu! Belum pemanasan!' (low, from the water side)
C7 = close(SAF, f('Y7', '1.75'), 1.1, 1.8, 1.6, pitch=.02, dt=.2, frame=dive(.2, .8))
# c8 the Pos Gotong Royong job board: third job
C8 = bld('posgotong', 1.05, 1.45, .98, f('Y8', '-.05'), f('Y8', '-.05') + .1, .1, .08, 1.75, 1.45, 4.0)
# c9 -VANZwlee on the deck: anime pose, then the stumble (cool clock 4.0 -> 8)
C9 = close(VNZ, f('Y9', '3.0'), 1.0, 2.4, 2.1, pitch=.1, dur=4.3, dt=1.0, frame="window.__coolT = Math.min(7.99, Math.max(0, 3.6 + T)); " + dive(1.0, .5))
# c10 two-shot Safar (board) + VANZ (deck behind): 'itu kesandung, kan?' 'itu... gaya.'
C10 = close(SAF, f('Y10', '1.8'), f('H10', '2.0'), 2.0, 1.75, pitch=.1, dt=1.0, frame=dive(1.0, .6))
# c10b VANZ: 'itu... gaya.' (pose held, chin up)
C10B = close(VNZ, f('Y10B', '2.85'), 1.05, 1.9, 1.7, pitch=.08, dt=1.0, extra="window.__coolT = 1.0; ", frame="window.__coolT = 1.0; ")
# c11 Safar close, determined: 'demi paket lengkap... bismillah' (bounce, then the crouch begins at the end)
C11 = close(SAF, f('Y11', '1.35'), 1.2, 1.6, 1.35, pitch=.08, dur=3.4, dt=0, frame=dive(0, 1.0))
# c12 THE JUMP: wide side view, belly flop, splash (clock 3.3 + T: leaves the board at .8 s, splash 1.6 s)
C12 = close(SAF, f('Y12', '1.3'), f('H12', '.3'), f('D12', '5.5'), f('D12', '5.5') + .3, pitch=f('P12', '.16'), ox=1.0, keep='[window.__RIS, window.__LAL]', dur=3.5, dt=3.3, frame=dive(3.3))
# c13 Riski laughs (splash moment held: clock pinned in the laugh window)
C13 = close(RIS, f('Y13', '-.3'), .75, 1.8, 1.55, pitch=.1, dt=6.0)
# c14 two-shot Riski + lala: 'Riski senyum!'
C14 = """() => { """ + head(6.2) + """ const a = window.__RIS(), b = window.__LAL(), x = (a.x + b.x) / 2, z = (a.z + b.z) / 2, y = a.obj.position.y + .55;
  const Y = """ + E('Y14', '-.45') + """; window.__look(x, z, Y, .16, 2.8, false);
  window.__beforeRender = (dt, T) => { window.__diveT = 6.2; window.__C(x, y, z); P.cam.dist = Math.max(2.4, 2.8 - T * .15); P.cam.yaw = Y; P.cam.pitch = .16; window.__clr([a, b], x, z, .6); }; }"""
# c15 Safar treading water, waving: 'airnya... DINGIN BANGET!'
C15 = close(SAF, f('Y15', '2.3'), f('H15', '-.55'), 2.4, 2.0, pitch=.15, ox=3.3, dt=10.1, frame=dive(10.1, .6))
# c16 the Papan Skor Loncat, crowd cheering
C16 = bld('kolamrenang', 2.75, -2.3, 1.55, f('Y16', '3.25'), f('Y16', '3.25') - .15, .1, .08, 2.9, 2.5, 3.5, cheer='true', dt=7.0, frame=dive(7.0, .5))
# c17 end: crane up over the pool, Safar's live loop (bounce -> jump)
C17 = bld('kolamrenang', -.5, -.3, 0, 2.6, 3.0, .35, .85, 7, 15, 6.0, dt=2.5, frame=dive(2.5))
SHOTS = {'c1': (C1, 110), 'c2': (C2, 120), 'c3': (C3, 160), 'c4': (C4, 100), 'c5': (C5, 115), 'c6': (C6, 115), 'c7': (C7, 55),
         'c8': (C8, 115), 'c9': (C9, 136), 'c10': (C10, 90), 'c10b': (C10B, 65), 'c11': (C11, 105), 'c12': (C12, 110), 'c13': (C13, 105), 'c14': (C14, 80),
         'c15': (C15, 75), 'c16': (C16, 95), 'c17': (C17, 185)}
CLEAR = E53.CLEAR.replace('() => {', '() => { window.__diveT = null; window.__coolT = null;', 1)
async def run(which):
    async with async_playwright() as p:
        b, pg = await setup(p)
        for js in CHAIN + (SETUP54,): await pg.evaluate(js)
        if os.environ.get('VARS'): await pg.evaluate('() => { ' + os.environ['VARS'] + ' }')
        if 'pos' in which: print(await pg.evaluate(POS))
        for k, (js, n) in SHOTS.items():
            if k in which and 'prev' not in which:
                await shoot(pg, 'e54' + k, int(os.environ.get('N_' + k, n)), start_js=js, warm=12)
                await pg.evaluate(CLEAR)
        if 'prev' in which:
            for k, (js, n) in SHOTS.items():
                if 'all' not in which and k not in which: continue
                await shoot(pg, 'p54' + k, int(os.environ.get('PN', '1')), start_js=js, warm=int(os.environ.get('WARM', '40')))
                await pg.evaluate(CLEAR)
        await b.close()
if __name__ == "__main__": asyncio.run(run(sys.argv[1].split(",")))
