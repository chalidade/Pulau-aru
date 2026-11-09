"""Episode 26 "Namamu Ada, Karaktermu Mana?" shot list (format CERITA).  usage: DPR=2 python3 shots.py c1,c3,...  (DPR=1 + prev for checks)
New web feature: tap your name on the Batu Nama (or open pulau-aru.web.id/?warga=nama) and your character walks out of the stone
with a gold name tag. Second comment: a glass lift on the Apartemen Presiden. Cameo: muhamatferos197 fishing beside _Rayhannn`.
Reuses the helper JS of ep25 (BASE, NPC, EXTRA).
"""
import asyncio, sys, os, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'lib'))
from harness import *
_sp = importlib.util.spec_from_file_location('ep25shots', os.path.join(HERE, '..', 'ep25', 'shots.py')); E25 = importlib.util.module_from_spec(_sp); _sp.loader.exec_module(E25)
BASE, NPC, EXTRA = E25.BASE, E25.NPC, E25.EXTRA
GUARD, DABY, PRIN, RAY, FER = 'Cawetssssss', 'D..A..B..Y a..j..a', 'princes_nay', '_Rayhannn`', 'muhamatferos197'
SX, SZ = -5.0, 37.5          # Batu Nama centre (world); its carved face looks +z (to the sea)
LX, LZ = -16.78, 1.31        # the lift shaft (world); its glass door faces -z
EP26 = """window.__S = n => window.__pulau.npcs.find(m => m.key === 'r:' + n.toLowerCase()) || window.__pulau.app.summon(n, true);
  window.__sum = n => { const P = window.__pulau; const m = P.app.summon(n, true); return m; };
  window.__cab = () => { const P = window.__pulau, o = window.__bld('apartemen'), c = o.userData.lift; c.updateMatrixWorld(true); return c.getWorldPosition(new P.cam.target.constructor()); };
  window.__lift = 0;"""
# c1 cold open: Aru in front of the Batu Nama full of names, looking up at it (over-the-shoulder, names readable)
C1 = """() => { const P = window.__pulau; window.__clock = .3; window.__cheer = null; const ax = %s + .55, az = %s + 1.55; window.__look(ax, az, .55, .12, 3.0, false);
  window.__beforeRender = (dt, T) => { window.__keep([], ax, az, 7); window.__aru(ax, az, PI - .25 + Math.sin(T * .8) * .06, false, T); window.__tgt(ax - .45, az - .6, 1.45); P.cam.dist = Math.max(3.0, 3.5 - T * .1); P.cam.yaw = .55 + T * .02; }; }""" % (SX, SZ)
# c2 Aru turns to camera: 'Namanya ada di batu... tapi orangnya mana?'
C2 = """() => { const P = window.__pulau; window.__clock = .3; window.__cheer = null; const ax = %s + .55, az = %s + 1.55; window.__look(ax, az, .25, .1, 2.4, false);
  window.__beforeRender = (dt, T) => { window.__keep([], ax, az, 7); window.__aru(ax, az, .25, true, T); window.__tgt(ax, az, 1.2); P.cam.dist = Math.max(2.0, 2.4 - T * .12); }; }""" % (SX, SZ)
# c3 Aru touches the stone; at 2.4 s the stone glows and @wleeeeeeeeecnt pops out of its east side
C3 = """() => { const P = window.__pulau; window.__clock = .3; window.__cheer = null; const ax = %s + .2, az = %s + 1.3; window.__look(ax, az, .55, .22, 5.8, false); let w = null;
  window.__beforeRender = (dt, T) => { window.__keep(w ? [w] : [], ax, az, 7); window.__aru(ax, az, PI - .1, false, T); const u = P.player.obj.userData; if (u.armR) u.armR.rotation.x = T < 2.4 ? -1.5 : -.3;
    if (!w && T > 2.4) { w = window.__sum('wleeeeeeeeecnt'); }
    if (w) { w.wait = 99; w.tx = null; w.obj.rotation.y = .3; }
    window.__tgt(ax + 1.25, az - .4, 1.2); P.cam.dist = Math.max(5.0, 5.8 - T * .2); }; }""" % (SX, SZ)
# c4 @wleeeeeeeeecnt close-up, confused, looking around: 'Eh? Aku... beneran ada?!'
C4 = """() => { const P = window.__pulau; window.__clock = .3; window.__cheer = null; const w = window.__S('wleeeeeeeeecnt') || window.__sum('wleeeeeeeeecnt'); const x = -4.3, z = 39.0; window.__look(x, z, -.3, .08, 3.0, false);
  window.__beforeRender = (dt, T) => { window.__keep([w], x, z, 5); w.wait = 99; window.__pose(w, x, z, -.3 + Math.sin(T * 2.2) * .7, T > 1.8 ? 'panic' : 'still', T); window.__tgt(x, z, 1.6); P.cam.dist = Math.max(2.7, 3.0 - T * .1); }; }"""
# c5 'AKU ADA! Lihat, ada namaku di kepala!' jumping and pointing at the gold name tag, Aru clapping beside
C5 = """() => { const P = window.__pulau; window.__clock = .3; window.__cheer = null; const w = window.__S('wleeeeeeeeecnt'); const x = -4.3, z = 39.0; window.__look(x, z, -.45, .1, 3.8, false);
  window.__beforeRender = (dt, T) => { window.__keep([w], x, z, 5); w.wait = 99; window.__pose(w, x, z, -.35, T < 1.2 ? 'cheer' : 'wave', T, T < 1.2 ? Math.abs(Math.sin(T * 7)) * .25 : 0); window.__aru(x - 1.1, z + .2, .7, false, T); const u = P.player.obj.userData; if (u.armR) { const k = Math.sin(T * 14) * .25; u.armR.rotation.x = -1.3 + k; u.armL.rotation.x = -1.3 - k; }
    window.__tgt(x - .55, z, 1.55); P.cam.dist = Math.max(3.4, 3.8 - T * .1); }; }"""
# c6 two more names come out (@selia_032, @ranz.bae1) and all three walk off toward the main street on their own (real game AI)
C6 = """() => { const P = window.__pulau; window.__clock = .3; window.__cheer = null; P.player.obj.visible = false; const w = window.__S('wleeeeeeeeecnt'); w.wait = 0; w.tx = -1.5; w.tz = 33.5; let a = null, b = null;
  window.__look(-3.4, 37.2, PI - .45, .3, 6.5, false);
  window.__beforeRender = (dt, T) => { if (!a && T > .4) a = window.__sum('selia_032'); if (!b && T > 1.7) b = window.__sum('ranz.bae1');
    window.__tgt(-3.2 + T * .15, 37.2 - T * .45, 1.0); P.cam.dist = 6.5 + T * .2; P.cam.yaw = PI - .45 + T * .03; }; }"""
# c7 @ranz.bae1 close-up: 'Nah! Sekarang aku kelihatan kan?!' (he complained he is rarely seen)
C7 = """() => { const P = window.__pulau; window.__clock = .3; window.__cheer = null; P.player.obj.visible = false; const r = window.__S('ranz.bae1'); const x = -1.6, z = 34.6; window.__look(x, z, .2, .08, 2.2, false);
  window.__beforeRender = (dt, T) => { window.__keep([r], x, z, 3.5); r.wait = 99; window.__pose(r, x, z, .2, T < .6 ? 'cheer' : 'point', T); const u = r.obj.userData; if (T >= .6) { u.armR.rotation.x = -1.9 + Math.sin(T * 6) * .1; u.armR.rotation.z = .9; }
    window.__tgt(x, z, 1.6); P.cam.dist = Math.max(2.4, 2.7 - T * .1); }; }"""
# c8 the Apartemen Presiden with its new glass lift; the cabin rides up during the shot
C8 = """() => { const P = window.__pulau; window.__clock = .3; window.__cheer = null; P.player.obj.visible = false; window.__look(%s, %s, PI + .75, .16, 13, false);
  window.__beforeRender = (dt, T) => { window.__keep([], %s, %s, 4); window.__lift = Math.max(0, Math.min(1, (T - .6) / 2.4)); window.__lift = window.__lift * window.__lift * (3 - 2 * window.__lift); window.__tgt(%s + .6, %s, 3.2 + T * .5); P.cam.dist = Math.max(10, 13 - T * .6); P.cam.yaw = PI + .75 - T * .03; }; }""" % (LX, LZ, LX, LZ, LX, LZ)
# c9 President 'EGA_ marches to the lift: 'Akhirnya! Presiden naik duluan!'
C9 = """() => { const P = window.__pulau, pr = window.__PR(); window.__clock = .3; window.__cheer = null; window.__lift = 0; P.player.obj.visible = false; const x = %s, z = %s - 1.05, y = window.__bld('apartemen').position.y;
  window.__look(x, z, PI + .35, .1, 2.8, false);
  window.__beforeRender = (dt, T) => { window.__keep([pr], x, z, 3); window.__poseY(pr, x, y, z, PI + .35, T < 1.2 ? 'cheer' : 'point', T); window.__tgt(x, z, 1.3 + (y - P.WD.groundY(x, z))); P.cam.target.y; P.cam.dist = Math.max(2.4, 2.8 - T * .12); }; }""" % (LX, LZ)
# c10 the bodyguard blocks the lift door: 'Berhenti. Identitas dulu.' / 'Ini liftku sendiri!'
C10 = """() => { const P = window.__pulau, pr = window.__PR(), g = window.__N('%s'); window.__fix(g); window.__clock = .3; window.__cheer = null; window.__lift = 0; P.player.obj.visible = false;
  const y = window.__bld('apartemen').position.y, gx = %s, gz = %s - .55, px = gx - .15, pz = gz - .95; window.__look(gx, gz - .5, PI + 1.1, .12, 3.4, false);
  window.__beforeRender = (dt, T) => { window.__keep([g, pr], gx, gz, 3); window.__z0(g); window.__guardP(g, gx, gz, PI, T, T < 2.6); g.obj.position.y = y; window.__poseY(pr, px, y, pz, .1, T > 2.6 ? 'panic' : 'still', T);
    window.__camTarget = new P.cam.target.constructor(gx - .1, y + 1.2, gz - .5); P.cam.dist = Math.max(3.0, 3.4 - T * .1); }; }""" % (GUARD, LX, LZ)
# c11 Klub Pertama sprint to the lift door: 'PERTAMA naik lift!' / 'Kamu kan nggak tinggal di sini!'
C11 = """() => { const P = window.__pulau, a = window.__N('%s'), b = window.__N('%s'); window.__fix(a); window.__fix(b); window.__clock = .3; window.__cheer = null; window.__lift = 0; P.player.obj.visible = false;
  const y = window.__bld('apartemen').position.y, x = %s + .1, z = %s - .9; window.__look(x, z, PI + .2, .12, 3.0, false);
  window.__beforeRender = (dt, T) => { window.__keep([a, b], x, z, 3); window.__z0(a); window.__z0(b); const ax = x - .35, az = z - .2 - Math.max(0, 1.4 - T * 2);
    window.__poseY(a, ax, y, az, PI, T < .7 ? 'walk' : 'cheer', T); window.__poseY(b, x + .4, y, z - .45, T < 1.5 ? -.6 : PI + .5, T < 1.5 ? 'still' : 'point', T);
    window.__camTarget = new P.cam.target.constructor(x, y + 1.15, z - .3); P.cam.dist = Math.max(2.6, 3.0 - T * .12); }; }""" % (DABY, PRIN, LX, LZ)
# c12 the ride: the president in the glass cabin rising to the penthouse, the camera tilting up with him: 'Wuuuuih! Cepat banget!'
C12 = """() => { const P = window.__pulau, pr = window.__PR(); window.__clock = .3; window.__cheer = null; P.player.obj.visible = false; window.__lift = 0;
  window.__look(%s, %s, PI + .55, .05, 5.5, false);
  window.__beforeRender = (dt, T) => { const k = Math.max(0, Math.min(1, (T - .3) / 2.3)); window.__lift = k * k * (3 - 2 * k); const c = window.__cab();
    window.__poseY(pr, c.x, c.y + .05, c.z, PI + .2, k > .05 && k < .95 ? 'cheer' : 'wave', T); window.__keep([pr], c.x, c.z, 2.5);
    window.__camTarget = new P.cam.target.constructor(c.x, c.y + 1.0, c.z); P.cam.pitch = .05 + k * .25; P.cam.dist = 5.5 + k * 1.5; }; }""" % (LX, LZ)
# c13 the pier: new resident muhamatferos197 fishing beside _Rayhannn`, whose rod brings up... a sandal (again)
C13 = """() => { const P = window.__pulau, r = window.__N('%s'), f = window.__N('%s'); window.__fix(r); window.__fix(f); window.__clock = .3; window.__cheer = null; P.player.obj.visible = false;
  const x = .05, z = 44.5; window.__look(x, z, 1.4, .22, 5.0, false);
  window.__beforeRender = (dt, T) => { window.__keep([r, f], x, z, 3.5); window.__camTarget = new P.cam.target.constructor(x, 1.2, z); P.cam.dist = Math.max(4.0, 5.0 - T * .15); P.cam.yaw = 1.4 - T * .02; }; }""" % (RAY, FER)
# c14 end: the three summoned characters stroll the main street with their name tags; the camera rises over the Batu Nama and the town
C14 = """() => { const P = window.__pulau; window.__clock = .3; window.__cheer = null; P.player.obj.visible = false;
  const S = ['wleeeeeeeeecnt', 'selia_032', 'ranz.bae1'].map(window.__S); const pts = [[-1.8, 33.2], [-.9, 32.4], [-1.4, 31.4]];
  S.forEach((n, i) => { n.wait = 0; n.x = pts[i][0]; n.z = pts[i][1]; n.tx = pts[i][0] + .3; n.tz = 22 - i; n.state = 'stroll'; });
  window.__look(-1.3, 30, PI - .25, .25, 6, false);
  window.__beforeRender = (dt, T) => { const c = S[1]; window.__tgt(c.x, c.z, 1.2); P.cam.dist = 5 + T * 1.8; P.cam.pitch = Math.min(.9, .22 + T * .09); P.cam.yaw = PI - .25 + T * .03; }; }"""
SHOTS = {'c1': (C1, 160), 'c2': (C2, 95), 'c3': (C3, 140), 'c4': (C4, 110), 'c5': (C5, 125), 'c6': (C6, 180), 'c7': (C7, 95),
         'c8': (C8, 115), 'c9': (C9, 95), 'c10': (C10, 125), 'c11': (C11, 115), 'c12': (C12, 100), 'c13': (C13, 210), 'c14': (C14, 225)}
CLEAR = "() => { window.__showInst(); window.__cheer = null; window.__camTarget = null; window.__beforeRender = null; window.__clock = null; window.__tourS = null; }"
async def run(which):
    async with async_playwright() as p:
        b, pg = await setup(p)
        await pg.evaluate(BASE); await pg.evaluate("() => { " + NPC + " }"); await pg.evaluate("() => { " + EXTRA + " }"); await pg.evaluate("() => { " + EP26 + " }")
        await pg.evaluate("() => { try { localStorage.removeItem('pulau-aru-karakter'); } catch (e) {} }")
        for k, (js, n) in SHOTS.items():
            if k in which and 'prev' not in which:
                await shoot(pg, 'e26' + k, int(os.environ.get('N_' + k, n)), start_js=js, warm=12)
                await pg.evaluate(CLEAR)
        if 'prev' in which:
            for k, (js, n) in SHOTS.items():
                if 'all' not in which and k not in which: continue
                await shoot(pg, 'p26' + k, 1, start_js=js, warm=int(os.environ.get('WARM', '40')))
                await pg.evaluate(CLEAR)
        await b.close()
if __name__ == "__main__": asyncio.run(run(sys.argv[1].split(",")))
