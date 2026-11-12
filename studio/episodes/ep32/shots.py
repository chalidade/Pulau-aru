"""Episode 32 "Misteri Sandal Hilang" shot list (format CERITA).  usage: DPR=2 python3 shots.py c1,c3,...  (DPR=1 + prev for checks)
No new comments (Apify failed again, Chrome not connected, komentar.md & traktir empty), so the episode starts the mystery subplot
(RUNBOOK 2d, Chalid 11 Nov): seven sandals vanish overnight. New in the game (ep 32): Papan BARANG HILANG (papanjadwal x66 y89)
by the Pos Penjaga Pantai, @RANUUGLL as Polisi Pantai (resident spot 68,91), Aidil YZ crying next to the board (66,91),
island.json mystery = a trail of small three-toed prints on the east beach to the lighthouse door, a white feather where it starts,
and the pile of missing sandals on the lighthouse gallery (main.js rebuildMystery). Reuses ep25/ep29/ep31 helpers.
"""
import asyncio, sys, os, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'lib'))
from harness import *
def _mod(name, path):
    sp = importlib.util.spec_from_file_location(name, path); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m
E25 = _mod('ep25shots', os.path.join(HERE, '..', 'ep25', 'shots.py')); E29 = _mod('ep29shots', os.path.join(HERE, '..', 'ep29', 'shots.py')); E31 = _mod('ep31shots', os.path.join(HERE, '..', 'ep31', 'shots.py'))
BASE, NPC, EXTRA, EP29, EP31 = E25.BASE, E25.NPC, E25.EXTRA, E29.EP29, E31.EP31
EP32 = """const P = window.__pulau;
  window.__AI = () => window.__N('Aidil YZ'); window.__RA = () => window.__N('RANUUGLL'); window.__WH = () => window.__N('whoyss');
  window.__AX = () => window.__N('Alexandre'); window.__AL = () => window.__N('ALERXMNC');
  window.__cry = (n, T) => { const u = n.obj.userData, k = Math.sin(T * 5) * .12; u.armL.rotation.x = -2.5 + k; u.armR.rotation.x = -2.5 - k; u.armL.rotation.z = .35; u.armR.rotation.z = -.35; u.body.position.y = Math.abs(Math.sin(T * 4)) * .015; };
  window.__salute = (n, T) => { const u = n.obj.userData; u.armR.rotation.x = -2.7; u.armR.rotation.z = -.6; u.armL.rotation.x = -.1; };
  window.__sneak = (n, T) => { const u = n.obj.userData; u.armL.rotation.x = u.armR.rotation.x = -.9; u.body.rotation.x = .35; u.body.position.y = -.08; u.body.rotation.y = Math.sin(T * 1.3) * .5; };
  window.__hero = (n, T) => { const u = n.obj.userData; u.armL.rotation.x = u.armR.rotation.x = .25; u.armL.rotation.z = -.75; u.armR.rotation.z = .75; u.body.rotation.x = -.08; };
  window.__LT = () => { const o = P.scene ? null : null; return [28, -2]; };
  window.__fixC = () => { for (const f of [window.__AI, window.__RA, window.__WH, window.__AX, window.__AL]) { const n = f(); if (n) window.__fix(n); } };"""
BX, BZ = 11.0, 33.5      # Papan BARANG HILANG (centre, world)
AX_, AZ_ = 10.6, 35.1    # Aidil in front of the board (staged a bit closer than his spot)
WX, WZ = -5.5, -13.5    # whoyss behind the bush near the alun-alun
# c1 cold open: Aidil crying in front of the BARANG HILANG board: 'Sandalku... HILANG! Hiks...'
C1 = """() => { const P = window.__pulau, a = window.__AI(); window.__fixC(); window.__clock = .38; window.__cheer = null; P.player.obj.visible = false;
  window.__look(%s, %s, -.12, .12, 2.4, false);
  window.__beforeRender = (dt, T) => { window.__z0(a); window.__S(a, %s, %s, -.12, 'still', T); window.__cry(a, T);
    window.__C(%s + .15, P.surfaceY(%s, %s) + 1.2, %s - .3); P.cam.dist = Math.max(2.0, 2.4 - T * .12); P.cam.yaw = -.12 + T * .02; P.cam.pitch = .12; window.__clr([a], %s, %s, .7); }; }""" % (AX_, AZ_, AX_, AZ_, AX_, AX_, AZ_, AZ_, AX_, AZ_)
# c2 premise: aerial glide from the middle of town down to the beach board
C2 = """() => { const P = window.__pulau; window.__fixC(); window.__clock = .38; window.__cheer = null; P.player.obj.visible = false;
  window.__look(0, 0, .1, 1.05, 50, false);
  window.__beforeRender = (dt, T) => { const k = Math.min(1, Math.max(0, T) / 6.4), e = k * k * (3 - 2 * k); window.__C(5 * e, .5 + .8 * e, 0 + 33 * e); P.cam.dist = 50 - 40 * e; P.cam.pitch = 1.05 - .55 * e; P.cam.yaw = .1 - .1 * e; }; }"""
# c3 the board close, Aru steps in beside it: 'Termasuk sandalku! Padahal cuma punya satu!'
C3 = """() => { const P = window.__pulau, a = window.__AI(), r = window.__RA(); window.__fixC(); window.__clock = .38; window.__cheer = null;
  window.__look(11.4, 34.6, .2, .16, 3.6, true);
  window.__beforeRender = (dt, T) => { a.obj.visible = r.obj.visible = false; window.__aruS(11.8, 34.5, -.35, T > 2.2 && T < 4.8, T); const u = P.player.obj.userData; if (T > 3.6 && T < 4.8 && u.armR) { u.armR.rotation.x = -2.4; }
    window.__C(11.35, P.surfaceY(11.3, 34) + 1.2, 34.0); P.cam.dist = Math.max(3.0, 3.6 - T * .1); P.cam.yaw = .2; P.cam.pitch = .16; window.__clr([], 11.6, 34.0, .7); a.obj.visible = r.obj.visible = false; }; }"""
# c4 RANUUGLL salutes in front of the Pos Penjaga Pantai: 'Tenang. Polisi pantai turun tangan!'
C4 = """() => { const P = window.__pulau, r = window.__RA(); window.__fixC(); window.__clock = .38; window.__cheer = null; P.player.obj.visible = false;
  window.__look(10.5, 34.9, .15, .12, 2.5, false);
  window.__beforeRender = (dt, T) => { window.__z0(r); window.__S(r, 10.5, 34.9, .15, T > .25 ? 'still' : 'walk', T); if (T > .25) window.__salute(r, T);
    window.__C(10.5, P.surfaceY(10.5, 34.9) + 1.25, 34.9); P.cam.dist = Math.max(2.1, 2.5 - T * .12); P.cam.yaw = .15; P.cam.pitch = .12; window.__clr([r], 10.5, 34.9, .7); }; }"""
# c5 RANUUGLL points at whoyss sneaking behind the bush: 'Tersangka pertama: whoyss!' / 'Hehe... bukan aku!'
C5 = """() => { const P = window.__pulau, r = window.__RA(), w = window.__WH(); window.__fixC(); window.__clock = .4; window.__cheer = null; P.player.obj.visible = false;
  window.__look(%s, %s, -.5, .2, 3.6, false); window.__hideInst([[%s - .3, %s + 1.8], [%s - 1.1, %s + 3.4], [%s + 1.2, %s + 1.0]], 1.5);
  window.__beforeRender = (dt, T) => { window.__z0(r); window.__z0(w); window.__S(r, %s + 1.3, %s + .5, -1.9, 'point', T);
    window.__S(w, %s, %s, T < 3.0 ? -.4 : .9, 'still', T); if (T < 3.0) window.__sneak(w, T); else { const u = w.obj.userData; u.armR.rotation.x = -2.6 + Math.sin(T * 12) * .15; u.armL.rotation.x = -.3; }
    window.__C(%s + .35, P.surfaceY(%s, %s) + 1.0, %s + .2); P.cam.dist = Math.max(3.0, 3.6 - T * .1); P.cam.yaw = -.5; P.cam.pitch = .2; window.__clr([r, w], %s + .6, %s + .2, .8); }; }""" % ((WX, WZ) * 3 + (WX, WZ) * 3 + (WX, WX, WZ, WZ, WX, WZ))
# c6 Aru vouches for whoyss: 'Semalam dia tidur di Pos Ronda...' / whoyss: 'Pliss jangan bilang-bilang!'
C6 = """() => { const P = window.__pulau, w = window.__WH(), r = window.__RA(); window.__fixC(); window.__clock = .4; window.__cheer = null;
  window.__look(%s, %s, .25, .18, 3.3, true); window.__hideInst([[%s + .4, %s + 1.6], [%s + .8, %s + 2.8], [%s + 1.2, %s - .7], [%s - 1.2, %s - .7]], 1.5);
  window.__beforeRender = (dt, T) => { window.__z0(w); r.obj.visible = false; window.__aruS(%s - .55, %s + .35, .7, T > .1 && T < 4.3, T);
    window.__S(w, %s + .55, %s + .3, T < 4.3 ? -.9 : -.2, T < 4.3 ? 'still' : 'beg', T); { const u = w.obj.userData; if (T >= 4.3) { u.armL.rotation.x = u.armR.rotation.x = -1.6 + Math.sin(T * 14) * .1; u.armL.rotation.z = .5; u.armR.rotation.z = -.5; } }
    window.__C(%s, P.surfaceY(%s, %s) + 1.1, %s + .3); P.cam.dist = Math.max(2.8, 3.3 - T * .1); P.cam.yaw = .25; P.cam.pitch = .18; window.__clr([w], %s, %s + .3, .8); r.obj.visible = false; }; }""" % ((WX, WZ) * 5 + (WX, WZ) * 2 + (WX, WX, WZ, WZ, WX, WZ))
# c7 the prints on the east beach: camera low along the trail, RANUUGLL crouched over them, then the lighthouse rises behind
C7 = """() => { const P = window.__pulau, r = window.__RA(); window.__fixC(); window.__clock = .42; window.__cheer = null; P.player.obj.visible = false;
  window.__look(22.6, 1.6, -.95, .5, 2.6, false);
  window.__beforeRender = (dt, T) => { window.__z0(r); window.__S(r, 23.6, .6, -2.2, 'point', T); { const u = r.obj.userData; u.body.rotation.x = .12; u.armR.rotation.x = -.9; }
    const k = Math.min(1, Math.max(0, T - 2.6) / 3.6), e = k * k * (3 - 2 * k);
    window.__C(22.6 + 3 * e, P.surfaceY(22.6, 1.0) + .3 + 2.4 * e, 1.0 - 2.4 * e); P.cam.dist = 2.6 + 4.0 * e; P.cam.yaw = -.95 + .25 * e; P.cam.pitch = .5 - .3 * e; window.__clr([r], 22.6, 1.0, .5); }; }"""
# c8 Alexandre at the feather, hero pose, then picks it up: 'Serahkan padaku! ...Eh, ini bulu apa?'
C8 = """() => { const P = window.__pulau, x = window.__AX(); window.__fixC(); window.__clock = .44; window.__cheer = null; P.player.obj.visible = false;
  window.__look(21.4, 2.2, -.4, .14, 3.0, false);
  window.__beforeRender = (dt, T) => { window.__z0(x); window.__S(x, 21.4, 2.2, -.4, 'still', T); if (T < 1.6) window.__hero(x, T); else { const u = x.obj.userData; u.body.rotation.x = Math.min(.3, (T - 1.6) * 1.2); u.armR.rotation.x = -1.3; u.armL.rotation.x = -.2; } 
    window.__C(21.3, P.surfaceY(21.4, 2.2) + 1.05, 2.0); P.cam.dist = Math.max(2.7, 3.0 - T * .08); P.cam.yaw = -.4; P.cam.pitch = .14 + (T > 1.6 ? .12 : 0); window.__clr([x], 21.3, 2.0, .6); }; }"""
# c9 dusk, ALERXMNC already standing at the lighthouse door: 'Aku sudah di sini dari tadi.' ... 'Jejaknya... naik ke atas.'
C9 = """() => { const P = window.__pulau, l = window.__AL(); window.__fixC(); window.__clock = .575; window.__cheer = null; P.player.obj.visible = false;
  window.__look(26.2, -1.0, -1.15, .14, 2.6, false); window.__hideInst([[25.0, -.5], [24.0, -.1], [23.0, .3]], 1.4);
  window.__beforeRender = (dt, T) => { window.__z0(l); window.__S(l, 26.2, -1.0, -1.15, 'still', T); if (T > 2.4) { const u = l.obj.userData; u.armR.rotation.x = -2.9; u.armR.rotation.z = .1; }
    window.__C(26.2, P.surfaceY(26.2, -1.0) + 1.2 + (T > 2.6 ? Math.min(.5, (T - 2.6) * .4) : 0), -1.0); P.cam.dist = Math.max(2.2, 2.6 - T * .1); P.cam.yaw = -1.15; P.cam.pitch = .14; window.__clr([l], 26.2, -1.0, .6); }; }"""
# c10 the camera climbs the lighthouse to the gallery: the pile of missing sandals ('Dan di puncak mercusuar...' / Aru: 'SANDAL KITA?!')
C10 = """() => { const P = window.__pulau; window.__fixC(); window.__clock = .575; window.__cheer = null; P.player.obj.visible = false; const g = P.surfaceY(28, -2);
  window.__look(27.6, -1.4, -.6, .1, 4.5, false);
  window.__beforeRender = (dt, T) => { const k = Math.min(1, Math.max(0, T) / 3.2), e = k * k * (3 - 2 * k);
    window.__C(27.58, g + 1.5 + (7.2 * e), -1.38); P.cam.dist = 4.5 - 2.9 * e + Math.max(0, T - 3.4) * .06; P.cam.yaw = -.6 + .05 * e; P.cam.pitch = .1 + .5 * e; }; }"""
# c11 end: Aru at the foot of the lighthouse at dusk, facing the camera ('Siapa pencurinya? Tulis tebakanmu!'), the camera rises to the gallery and the sea
C11 = """() => { const P = window.__pulau; window.__fixC(); window.__clock = .59; window.__cheer = null;
  window.__look(25.6, -.4, -.9, .16, 2.8, true);
  window.__beforeRender = (dt, T) => { window.__aruS(25.6, -.4, -.9, T > .1 && T < 3.6, T); const u = P.player.obj.userData; if (T > 1.0 && T < 2.2 && u.armR) { u.armR.rotation.x = -2.8; }
    const k = Math.min(1, Math.max(0, T - 3.8) / 5), e = k * k * (3 - 2 * k);
    window.__C(25.6 + 2.4 * e, P.surfaceY(25.6, -.4) + 1.2 + 6.5 * e, -.4 - 1.5 * e); P.cam.dist = 2.8 + 11 * e; P.cam.yaw = -.9 + .3 * e; P.cam.pitch = .16 + .25 * e; window.__clr([], 25.6, -.4, e < .3 ? .6 : .01); }; }"""
SHOTS = {'c1': (C1, 110), 'c2': (C2, 230), 'c3': (C3, 170), 'c4': (C4, 115), 'c5': (C5, 190), 'c6': (C6, 200), 'c7': (C7, 220),
         'c8': (C8, 130), 'c9': (C9, 170), 'c10': (C10, 200), 'c11': (C11, 300)}
CLEAR = "() => { window.__showInst && window.__showInst(); window.__cheer = null; window.__camTarget = null; window.__beforeRender = null; window.__clock = null; window.__tourS = null; for (const n of window.__pulau.npcs) { n.obj.visible = true; n.obj.userData.body.rotation.x = 0; } }"
async def run(which):
    async with async_playwright() as p:
        b, pg = await setup(p)
        for js in (BASE, "() => { " + NPC + " }", "() => { " + EXTRA + " }", "() => { " + EP29 + " }", "() => { " + EP31 + " }", "() => { " + EP32 + " }"): await pg.evaluate(js)
        for k, (js, n) in SHOTS.items():
            if k in which and 'prev' not in which:
                await shoot(pg, 'e32' + k, int(os.environ.get('N_' + k, n)), start_js=js, warm=12)
                await pg.evaluate(CLEAR)
        if 'prev' in which:
            for k, (js, n) in SHOTS.items():
                if 'all' not in which and k not in which: continue
                for w in os.environ.get('WARMS', os.environ.get('WARM', '40')).split('/'):
                    await shoot(pg, 'p32' + k + ('' if '/' not in os.environ.get('WARMS', '') else '_' + w), 1, start_js=js, warm=int(w))
                    await pg.evaluate(CLEAR)
        await b.close()
if __name__ == "__main__": asyncio.run(run(sys.argv[1].split(",")))
