"""Episode 30 "Kapal Pertama Pulang Bawa Siapa?" shot list (format CERITA).  usage: DPR=2 python3 shots.py c1,c3,...  (DPR=1 + prev for checks)
No new comments this run (Apify failed, Chrome not connected, komentar.md empty), so the episode answers ep 29's end-card question:
KM NELAYAN BARU sails her first route with muhamatferos197 as captain (main.js: every 150 s, window.__boatTheta pins her on the
route) and comes home at dusk with a passenger: the Penjaga Mercusuar (island.json storyCast, kit/pose 'keeper', lantern),
who now stands in front of Hotel Pulau (Kamar 3, Buku Tamu updated) and brings the news: the president's term ends 14 Nov
(spanduk PEMILU SEGERA! 14 NOV by the stage). Klub Pertama (DABY & princes) now wait at the harbour gate.
Reuses ep25's and ep29's helpers.
"""
import asyncio, sys, os, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'lib'))
from harness import *
def _mod(name, path):
    sp = importlib.util.spec_from_file_location(name, path); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m
E25 = _mod('ep25shots', os.path.join(HERE, '..', 'ep25', 'shots.py')); E29 = _mod('ep29shots', os.path.join(HERE, '..', 'ep29', 'shots.py'))
BASE, NPC, EXTRA, EP29 = E25.BASE, E25.NPC, E25.EXTRA, E29.EP29
EP30 = """const P = window.__pulau; window.__boatTheta = 0;
  window.__K = () => window.__N('Penjaga Mercusuar'); window.__DB = () => window.__N('D..A..B..Y a..j..a'); window.__PN = () => window.__N('princes_nay');
  window.__bt = () => window.__hb().userData.boat;
  window.__V3 = (x, y, z) => new (P.cam.target.constructor)(x, y, z);
  // a character standing on the boat deck at local (lx, lz); rel = turn relative to the bow
  window.__onBoat = (n, lx, lz, rel, pose, T) => { const bt = window.__bt(); bt.updateMatrixWorld(true); const v = bt.localToWorld(window.__V3(lx, .29, lz)), w = bt.localToWorld(window.__V3(lx + 1, .29, lz));
    window.__poseY(n, v.x, v.y, v.z, Math.atan2(w.x - v.x, w.z - v.z) + rel, pose, T); return v; };
  window.__boatW = () => { const bt = window.__bt(); bt.updateMatrixWorld(true); return bt.localToWorld(window.__V3(0, .3, 0)); };
  window.__lant = n => { const u = n.obj.userData; u.armR.rotation.x = -1.05; u.armR.rotation.z = -.12; };
  window.__fixK = () => { for (const n of [window.__K(), window.__DB(), window.__PN()]) window.__fix(n); window.__fixAll(); };"""
HX, HZ = 9.0, 41.0
# c1 cold open (flash-forward): dusk, the hooded keeper steps off the boat onto the harbour deck, lantern glowing, toward the camera
C1 = """() => { const P = window.__pulau, k = window.__K(); window.__fixK(); window.__clock = .56; window.__cheer = null; P.player.obj.visible = false; window.__boatTheta = 0;
  window.__look(10.3, 42.25, -1.5, .06, 3.2, false);
  window.__beforeRender = (dt, T) => { window.__keep([k], 10.3, 42.25, 3.5); window.__z0(k); const x = Math.max(10.15, 10.85 - Math.max(0, T + .4) * .35);
    window.__S(k, x, 42.25, -1.57, x > 10.16 ? 'walk' : 'still', T); window.__lant(k);
    window.__C(10.25, .26 + 1.3, 42.25); P.cam.dist = Math.max(2.5, 3.1 - T * .2); P.cam.yaw = -1.5 + T * .03; P.cam.pitch = .06; }; }"""
# c2 premise: aerial glide from the town down to the harbour, the boat moored (day)
C2 = """() => { const P = window.__pulau; window.__clock = .3; window.__cheer = null; P.player.obj.visible = false; window.__boatTheta = 0;
  window.__look(0, 18, .3, 1.0, 40, false);
  window.__beforeRender = (dt, T) => { const k = Math.min(1, Math.max(0, T) / 5.5), e = k * k * (3 - 2 * k); window.__C(0 + (%s + 1) * e, 0, 18 + (%s - 18) * e); P.cam.dist = 40 - 24 * e; P.cam.pitch = 1.0 - .35 * e; P.cam.yaw = .3 + .15 * e; }; }""" % (HX, HZ)
# c3 morning: feros on the bow as the boat leaves the harbour: 'Kapal pertama berangkat! Nelayan pertama, jadi kapten!'
C3 = """() => { const P = window.__pulau, f = window.__F(); window.__fixK(); window.__clock = .28; window.__cheer = null; P.player.obj.visible = false;
  window.__beforeRender = (dt, T) => { window.__boatTheta = Math.max(0.001, .05 + Math.max(0, T) * .08); window.__z0(f); const v = window.__onBoat(f, 1.0, 0, 0, T < 2.4 ? 'talk' : 'cheer', T);
    window.__keep([f], v.x, v.z, 2.5); window.__C(v.x, v.y + 1.1, v.z); P.cam.dist = 3.6 - Math.min(1, T / 3) * .5; P.cam.yaw = Math.atan2(1, 0) * 0 + .35; P.cam.pitch = .12; }; window.__look(11.6, 42, .35, .12, 3.6, false); }"""
# c4 at sea: the boat on her route, the camera follows from above and behind (narrator: the question from yesterday)
C4 = """() => { const P = window.__pulau, f = window.__F(); window.__fixK(); window.__clock = .32; window.__cheer = null; P.player.obj.visible = false;
  window.__beforeRender = (dt, T) => { window.__boatTheta = .7 + Math.max(0, T) * .14; window.__z0(f); window.__onBoat(f, 1.0, 0, 0, 'wave', T); const v = window.__boatW();
    window.__C(v.x, .5, v.z); P.cam.dist = 8.5 - Math.min(1, T / 6) * 1.5; P.cam.yaw = -.6 + T * .05; P.cam.pitch = .55; }; window.__look(18, 46, -.6, .55, 11, false); }"""
# c5 Rayhan on the harbour edge waving out to sea (with his sandal rod): 'Hati-hati, Feros! Jangan pulang bawa sandal kayak aku!'
C5 = """() => { const P = window.__pulau, r = window.__R(); window.__fixK(); window.__clock = .34; window.__cheer = null; P.player.obj.visible = false; window.__boatTheta = 1.6;
  window.__look(7.7, 42.9, .25, .14, 3.4, false);
  window.__beforeRender = (dt, T) => { window.__keep([r], 7.7, 42.9, 2.5); window.__z0(r); window.__S(r, 7.7, 42.9, .25, 'wave', T);
    window.__C(7.7, .26 + 1.15, 42.9); P.cam.dist = Math.max(2.8, 3.4 - T * .15); P.cam.yaw = .25 + T * .02; P.cam.pitch = .14; }; }"""
# c6 dusk, Klub Pertama on the harbour edge waiting for the boat: 'Aku yang pertama sambut kapalnya!' / 'Princess selalu duluan, ya!'
C6 = """() => { const P = window.__pulau, d = window.__DB(), p = window.__PN(); window.__fixK(); window.__clock = .5; window.__cheer = null; P.player.obj.visible = false; window.__boatTheta = 5.2;
  window.__look(9, 42.5, 0, .16, 3.8, false);
  window.__beforeRender = (dt, T) => { window.__keep([d, p], 9, 42.5, 3.5); window.__z0(d); window.__z0(p);
    const zp = T > 2.2 ? Math.min(43.0, 42.5 + (T - 2.2) * .9) : 42.5;
    window.__S(d, 8.6, 42.7, T > 2.3 ? .5 : 0, T < 2.2 ? 'wave' : 'talk', T); window.__S(p, 9.45, zp, T > 2.2 ? -.4 : 0, T < 2.2 ? 'still' : (zp < 43 ? 'walk' : 'wave'), T * 1.4);
    window.__C(9.05, .26 + 1.1, 42.8); P.cam.dist = Math.max(3.0, 3.8 - T * .2); P.cam.yaw = Math.sin(T * .3) * .1; P.cam.pitch = .16; }; }"""
# c7 sunset: the boat comes home, a lantern glowing on the bow next to feros (the passenger), seen from the harbour deck
C7 = """() => { const P = window.__pulau, f = window.__F(), k = window.__K(); window.__fixK(); window.__clock = .56; window.__cheer = null; P.player.obj.visible = false;
  window.__beforeRender = (dt, T) => { window.__boatTheta = Math.min(5.6, 4.6 + Math.max(0, T) * .2); window.__z0(f); window.__z0(k); window.__onBoat(f, .2, .25, 0, 'wave', T); window.__onBoat(k, 1.0, -.1, 0, 'still', T); window.__lant(k); const v = window.__boatW();
    window.__keep([f, k], v.x, v.z, 3); window.__C(v.x, .9, v.z); P.cam.dist = 5.5 - Math.min(1, T / 4) * 1.5; P.cam.yaw = -1.9; P.cam.pitch = .18; }; window.__look(16, 47, -1.9, .18, 5.5, false); }"""
# c8 moored: feros on the deck in front of the boat, the keeper behind him: 'Aku nemu dia di Pulau Seberang. Bawa lentera.'
C8 = """() => { const P = window.__pulau, f = window.__F(), k = window.__K(); window.__fixK(); window.__clock = .57; window.__cheer = null; P.player.obj.visible = false; window.__boatTheta = 0;
  window.__look(10.4, 42.2, -1.75, .1, 3.0, false);
  window.__beforeRender = (dt, T) => { window.__keep([f, k], 10.4, 42.2, 3.5); window.__z0(f); window.__z0(k);
    window.__S(f, 10.1, 42.45, -1.6, 'talk', T); window.__onBoat(k, .6, 0, -1.57, 'still', T); window.__lant(k);
    window.__C(10.5, .26 + 1.2, 42.2); P.cam.dist = Math.max(2.6, 3.0 - T * .15); P.cam.yaw = -1.75 - T * .02; P.cam.pitch = .1; }; }"""
# c9 the keeper faces Aru on the deck (Klub Pertama frozen behind Aru): 'Aku... Penjaga Mercusuar.' / Aru: 'Yang kirim surat itu?!'
# then 'Pemimpin pulau harus dipilih warga. Bukan ditunjuk.' (cut back to the keeper, push in)
C9S = """window.__fixK(); window.__clock = .58; window.__cheer = null; window.__boatTheta = 0;
  const pose9 = (T, kt, at) => { window.__keep([k, d, p], 9.6, 42.3, 4); window.__z0(k); window.__z0(d); window.__z0(p);
    window.__S(k, 10.3, 42.3, -1.57, kt ? 'talk' : 'still', T); window.__lant(k);
    window.__aruS(9.1, 42.3, 1.57, at, T); const u = P.player.obj.userData; if (at && u.armR) { u.armR.rotation.x = u.armL.rotation.x = -2.4 + Math.sin(T * 12) * .2; }
    window.__S(d, 8.5, 41.85, 1.3, 'still', T); window.__S(p, 8.45, 42.7, 1.8, 'still', T); for (const n of [d, p]) { const v = n.obj.userData; v.armL.rotation.x = v.armR.rotation.x = -2.0; } };"""
C9 = """() => { const P = window.__pulau, k = window.__K(), d = window.__DB(), p = window.__PN(); """ + C9S + """
  window.__look(10.3, 42.3, -1.2, .08, 3, false);
  window.__beforeRender = (dt, T) => { pose9(T, T > .1 && T < 2.4, false); window.__C(10.3, .26 + 1.3, 42.3); P.cam.dist = 3.0 - T * .15; P.cam.yaw = -1.2; P.cam.pitch = .08; }; }"""
C9B = """() => { const P = window.__pulau, k = window.__K(), d = window.__DB(), p = window.__PN(); """ + C9S + """
  window.__look(9.1, 42.3, 2.3, .1, 2.2, true);
  window.__beforeRender = (dt, T) => { pose9(T, false, true); window.__C(9.1, .26 + 1.05, 42.3); P.cam.dist = 2.2 - T * .1; P.cam.yaw = 2.3; P.cam.pitch = .1; }; }"""
C9C = """() => { const P = window.__pulau, k = window.__K(), d = window.__DB(), p = window.__PN(); """ + C9S + """
  window.__look(10.3, 42.3, -1.0, .05, 2.7, false);
  window.__beforeRender = (dt, T) => { pose9(T, T > .1 && T < 3.7, false); window.__C(10.3, .26 + 1.35, 42.3); P.cam.dist = Math.max(1.9, 2.7 - T * .2); P.cam.yaw = -1.0; P.cam.pitch = .05; }; }"""
# c10 the keeper at Hotel Pulau (Kamar 3), the Buku Tamu board beside him reads 'Kamar 3: Penjaga Mercusuar (SUDAH DATANG)'
C10 = """() => { const P = window.__pulau, k = window.__K(); window.__fixK(); window.__clock = .6; window.__cheer = null; P.player.obj.visible = false; window.__boatTheta = 0;
  window.__look(1.3, 30.2, -1.3, .12, 4.4, false);
  window.__beforeRender = (dt, T) => { window.__keep([k], 1.5, 29.5, 3); window.__z0(k); window.__S(k, 1.8, 29.0, -1.3, 'still', T); window.__lant(k);
    window.__C(1.0, 1.35, 30.2); P.cam.dist = Math.max(3.8, 4.5 - T * .2); P.cam.yaw = -1.1 + T * .03; P.cam.pitch = .12; }; }"""
# c11 the news: the keeper at the hotel: 'Masa jabatan presiden... berakhir empat belas November.', cut to the spanduk PEMILU SEGERA! 14 NOV by the stage,
# then Aru in front of it: 'Berarti... pemilu lagi?!'
C11 = """() => { const P = window.__pulau, k = window.__K(); window.__fixK(); window.__clock = .6; window.__cheer = null; P.player.obj.visible = false; window.__boatTheta = 0;
  window.__look(1.8, 29.0, -1.3, .08, 2.8, false);
  window.__beforeRender = (dt, T) => { window.__keep([k], 1.8, 29.0, 2.5); window.__z0(k); window.__S(k, 1.8, 29.0, -1.3, T > .2 && T < 4 ? 'talk' : 'still', T); window.__lant(k); P.player.obj.visible = false;
    window.__C(1.8, 1.85, 29.0); P.cam.dist = Math.max(2.2, 2.8 - T * .15); P.cam.yaw = -1.3; P.cam.pitch = .06; }; }"""
C11B = """() => { const P = window.__pulau; window.__clock = .32; window.__cheer = null; window.__boatTheta = 0;
  window.__look(-2.4, -5.75, 2.3, .12, 2.9, true);
  window.__beforeRender = (dt, T) => { window.__aruS(-2.2, -5.6, 2.0, true, T); const u = P.player.obj.userData; if (u.armR) { u.armR.rotation.x = u.armL.rotation.x = -2.7 + Math.sin(T * 10) * .15; } window.__C(-2.4, P.surfaceY(-2.2, -5.6) + 1.25, -5.75); P.cam.dist = Math.max(2.6, 2.9 - T * .1); P.cam.yaw = 2.3; P.cam.pitch = .12; }; }"""
# c12 end: dusk, Aru and the keeper in front of the hotel, residents waving, the camera rises over the main street and the harbour
C12 = """() => { const P = window.__pulau, k = window.__K(); window.__fixK(); window.__clock = .6; window.__cheer = true; const W = window.__plain().slice(0, 6); window.__boatTheta = 0;
  window.__look(1.2, 29.6, -1.1, .3, 4.2, false);
  window.__beforeRender = (dt, T) => { window.__keep([k].concat(W), 1.2, 29.5, 3); window.__z0(k); window.__S(k, 1.8, 29.0, -1.4, 'still', T); window.__lant(k);
    window.__aruS(1.0, 30.25, -1.2, T > 4.4 && T < 7.6, T); const u = P.player.obj.userData; if (T <= 4.4 && u.armR) { u.armR.rotation.x = -2.6 + Math.sin(T * 8) * .3; }
    const SP = [[1.3, 27.7], [.6, 28.1], [1.5, 31.3], [.8, 31.0], [2.1, 27.4], [2.2, 31.7]]; W.forEach((n, i) => { window.__z0(n); window.__S(n, SP[i][0], SP[i][1], -1.1, 'wave', T + i * .4); });
    window.__C(1.2, 1.3 + T * .12, 29.6); P.cam.yaw = -1.1 + T * .02; P.cam.dist = 4.2 + T * .8; P.cam.pitch = Math.min(.8, .3 + T * .06); }; }"""
SHOTS = {'c1': (C1, 105), 'c2': (C2, 170), 'c3': (C3, 115), 'c4': (C4, 180), 'c5': (C5, 150), 'c6': (C6, 135), 'c7': (C7, 135),
         'c8': (C8, 90), 'c9': (C9, 85), 'c9b': (C9B, 50), 'c9c': (C9C, 125), 'c10': (C10, 135), 'c11': (C11, 135), 'c11b': (C11B, 80), 'c12': (C12, 260)}
CLEAR = "() => { window.__showInst(); window.__cheer = null; window.__camTarget = null; window.__beforeRender = null; window.__clock = null; window.__tourS = null; window.__boatTheta = 0; const h = window.__bld('pelabuhan'); if (h) { h.visible = true; window.__hbShow(1); } for (const n of window.__pulau.npcs) { if (n.rodPivot) n.rodPivot.rotation.x = 0; n.obj.userData.body.rotation.x = 0; } }"
async def run(which):
    async with async_playwright() as p:
        b, pg = await setup(p)
        await pg.evaluate(BASE); await pg.evaluate("() => { " + NPC + " }"); await pg.evaluate("() => { " + EXTRA + " }"); await pg.evaluate("() => { " + EP29 + " }"); await pg.evaluate("() => { " + EP30 + " }")
        for k, (js, n) in SHOTS.items():
            if k in which and 'prev' not in which:
                await shoot(pg, 'e30' + k, int(os.environ.get('N_' + k, n)), start_js=js, warm=12)
                await pg.evaluate(CLEAR)
        if 'prev' in which:
            for k, (js, n) in SHOTS.items():
                if 'all' not in which and k not in which: continue
                for w in os.environ.get('WARMS', os.environ.get('WARM', '40')).split('/'):
                    await shoot(pg, 'p30' + k + ('' if '/' not in os.environ.get('WARMS', '') else '_' + w), 1, start_js=js, warm=int(w))
                    await pg.evaluate(CLEAR)
        await b.close()
if __name__ == "__main__": asyncio.run(run(sys.argv[1].split(",")))
