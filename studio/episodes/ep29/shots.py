"""Episode 29 "Mau Jadi Nelayan, Dapat Pelabuhan" shot list (format KONSEP).  usage: DPR=2 python3 shots.py c1,c3,...  (DPR=1 + prev for checks)
@muhamatferos197's comment "bikin pelabuhan kak aku pengen jadi nelayan dah follow" becomes the Pelabuhan Nelayan, a walkable
harbour on the shallow bay east of the pier (cells 63-66 x 95-98, world x 7..11, z 39..43, deck ~.26). He and _Rayhannn` now
fish from its south edge (resident spots); Rayhan still catches a sandal, feros catches a big fish (kit 'rodfish').
Night: the lighthouse blinks three times out to sea every 30 s (main.js, window.__lhPhase shifts it for the camera).
Reuses ep25's helpers.
"""
import asyncio, sys, os, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'lib'))
from harness import *
_sp = importlib.util.spec_from_file_location('ep25shots', os.path.join(HERE, '..', 'ep25', 'shots.py')); E25 = importlib.util.module_from_spec(_sp); _sp.loader.exec_module(E25)
BASE, NPC, EXTRA = E25.BASE, E25.NPC, E25.EXTRA
EP29 = """const P = window.__pulau;
  window.__C = (x, y, z) => { window.__camTarget = new window.__pulau.cam.target.constructor(x, y, z); };
  window.__plain = () => P.npcs.filter(n => !n.demo && !n.castSpot && n.num && !n.pres && !n.vp && !n.aru && !n.cloud && !n.kit && !n.tool && !n.cand && !n.candSign);
  window.__F = () => window.__N('muhamatferos197'); window.__R = () => window.__N('_Rayhannn`');
  window.__S = (n, x, z, face, pose, T) => window.__poseY(n, x, P.surfaceY(x, z), z, face, pose, T);
  window.__aruS = (x, z, face, talk, T) => { const pl = P.player; pl.obj.visible = true; pl.x = x; pl.z = z; pl.tx = null; pl.vy = 0; pl.obj.position.set(x, P.surfaceY(x, z), z); pl.obj.rotation.y = face; const u = pl.obj.userData; if (u.armR) { u.armR.rotation.x = talk ? -1.1 + Math.sin(T * 7) * .4 : 0; u.armL.rotation.x = talk ? -.6 + Math.sin(T * 5) * .2 : 0; } };
  window.__hb = () => window.__bld('pelabuhan');
  window.__hbShow = k => { const h = window.__hb(); const C = h.children[0] && h.children[0].children.length > 3 ? h.children[0].children : h.children; const N = C.length; C.forEach((c, i) => { c.visible = i < k * N; }); };
  // lift the fishing rod: the kit meshes go into a pivot at the hands so the shot can swing the catch up
  window.__rodPivot = async n => { if (n.rodPivot) return n.rodPivot; const THREE = await import('three'); const b = n.obj.userData.body, p = new THREE.Group(); p.position.set(.22, .8, .25); b.add(p); b.updateMatrixWorld(true); (n.kit || []).forEach(m => p.attach(m)); n.rodPivot = p; return p; };
  window.__fixAll = () => { for (const n of [window.__F(), window.__R()]) window.__fix(n); };"""
HX, HZ = 9.0, 41.0            # harbour centre (world)
FX, FZ = 8.8, 42.9            # muhamatferos197's fishing spot on the south edge
RX, RZ = 7.7, 42.9            # _Rayhannn`'s spot beside him
# c1 cold open: feros heaves a big fish up, Rayhan beside him with (again) a sandal: 'Bang Rayhan! Aku dapat ikan beneran!'
C1 = """async () => { const P = window.__pulau, f = window.__F(), r = window.__R(); window.__fixAll(); const pv = await window.__rodPivot(f); window.__clock = .3; window.__cheer = null; P.player.obj.visible = false; window.__hbShow(1);
  window.__look(%s, %s, .55, .02, 4.1, false);
  window.__beforeRender = (dt, T) => { window.__keep([f, r], %s, %s, 4); window.__z0(f); window.__z0(r); const k = Math.min(1, Math.max(0, T + .6) / .7);
    window.__S(f, %s, %s, .35, 'still', T); const u = f.obj.userData; u.armL.rotation.x = u.armR.rotation.x = -1.2 - k * .7; f.obj.userData.body.rotation.x = -.15 * k; pv.rotation.x = -.55 * k + Math.sin(T * 7) * .07 * k; u.body.position.y = k > .95 ? Math.abs(Math.sin(T * 8)) * .06 : 0;
    window.__S(r, %s, %s, .9, 'still', T); const v = r.obj.userData; v.armL.rotation.x = v.armR.rotation.x = -1.1;
    window.__C(%s - .25, .26 + 1.55, %s + .2); P.cam.dist = Math.max(3.7, 4.1 - T * .2); P.cam.yaw = .55; P.cam.pitch = .02; }; }""" % (FX, FZ, FX, FZ, FX, FZ, RX, RZ, FX, FZ)
# c2 premise: aerial glide from the town down to the bay with the new harbour
C2 = """() => { const P = window.__pulau, f = window.__F(), pv = f.rodPivot; if (pv) pv.rotation.x = 0; f.obj.userData.body.rotation.x = 0; window.__clock = .3; window.__cheer = null; P.player.obj.visible = false; window.__hbShow(1);
  window.__look(0, 18, .3, 1.0, 40, false);
  window.__beforeRender = (dt, T) => { const k = Math.min(1, Math.max(0, T) / 6), e = k * k * (3 - 2 * k); window.__C(0 + (%s) * e, 0, 18 + (%s - 18) * e); P.cam.dist = 40 - 26 * e; P.cam.pitch = 1.0 - .35 * e; P.cam.yaw = .3 + .15 * e; }; }""" % (HX, HZ)
# c3 flashback: three days ago, feros on the old pier next to Rayhan, the bay still empty (harbour hidden)
C3 = """() => { const P = window.__pulau, f = window.__F(), r = window.__R(); window.__fixAll(); window.__clock = .3; window.__cheer = null; P.player.obj.visible = false; window.__hb().visible = false;
  window.__look(-.3, 44.4, 1.45, .14, 3.8, false);
  window.__beforeRender = (dt, T) => { window.__keep([f, r], -.3, 44.5, 4); window.__z0(f); window.__z0(r);
    window.__S(r, -.25, 43.6, 1.3, 'still', T); const v = r.obj.userData; v.armL.rotation.x = v.armR.rotation.x = -1.1;
    window.__S(f, -.3, 45.0, 1.9, T > .4 && T < 2.8 ? 'talk' : 'still', T);
    window.__C(-.3, .26 + 1.1, 44.35); P.cam.dist = Math.max(3.2, 3.8 - T * .15); P.cam.yaw = 1.45 + T * .02; P.cam.pitch = .14; }; }"""
# c4 Aru on the beach, the empty bay behind him: 'Pelabuhan? Oke. Kita bangun!'
C4 = """() => { const P = window.__pulau; window.__clock = .3; window.__cheer = null; window.__hb().visible = false;
  window.__look(8.6, 37.2, 2.75, .12, 3.4, false); window.__hideInst([[8.6, 36], [9.5, 37], [7.5, 37]], 2.6);
  window.__beforeRender = (dt, T) => { window.__keep([], 8.6, 37.2, 3); window.__aruS(8.6, 37.2, 2.75, true, T); const u = P.player.obj.userData; if (T > 1.6 && u.armR) { u.armR.rotation.x = -2.7; u.armL.rotation.x = -.3; }
    window.__C(8.6, P.surfaceY(8.6, 37.2) + 1.1, 37.2); P.cam.dist = Math.max(2.8, 3.4 - T * .2); P.cam.yaw = 2.75; P.cam.pitch = .12; }; }"""
# c5 the harbour assembles itself piece by piece over the bay (aerial)
C5 = """() => { const P = window.__pulau; window.__clock = .3; window.__cheer = null; P.player.obj.visible = false; const h = window.__hb(); h.visible = true; window.__hbShow(0);
  window.__look(%s, %s, .4, .8, 13, false);
  window.__beforeRender = (dt, T) => { const k = Math.min(1, Math.max(0, T - .2) / 2.6); window.__hbShow(k); window.__C(%s, .3, %s); P.cam.dist = 13 - T * .9; P.cam.yaw = .4 + T * .08; P.cam.pitch = .8 - T * .05; }; }""" % (HX, HZ, HX, HZ)
# c6 opening: Aru under the entrance arch (sign readable), residents cheering on the beach: 'Pelabuhan Nelayan Pulau Aru, resmi dibuka!'
C6 = """() => { const P = window.__pulau; window.__hbShow(1); window.__clock = .3; window.__cheer = true; const W = window.__plain().slice(0, 6);
  window.__look(9.0, 38.2, 3.14, .2, 5.2, false); window.__hideInst([[9, 36.5], [9, 38], [8, 37], [10, 37]], 2.6);
  window.__beforeRender = (dt, T) => { window.__keep(W, 9, 38.5, 3.5); window.__aruS(9.0, 39.6, 3.14, T < 2.2, T); const u = P.player.obj.userData; if (T > 2.2 && u.armR) { u.armR.rotation.x = u.armL.rotation.x = -2.8 + Math.sin(T * 9) * .2; }
    W.forEach((n, i) => { window.__z0(n); window.__S(n, 7.6 + i * .55, 40.6 + (i % 2) * .5, Math.PI + (i % 3 - 1) * .2, 'cheer', T + i * .3); });
    window.__C(9.0, 1.7, 39.4); P.cam.dist = Math.max(4.4, 5.2 - T * .3); P.cam.yaw = 3.14; P.cam.pitch = .2; }; }"""
# c7 Klub Pertama race through the arch onto the deck: 'PERTAMA! Aku yang pertama injak pelabuhan!' / 'Aku princess. Princess selalu duluan!'
C7 = """() => { const P = window.__pulau, d = window.__N('D..A..B..Y a..j..a'), p = window.__N('princes_nay'); window.__fix(d); window.__fix(p); window.__clock = .3; window.__cheer = null; P.player.obj.visible = false;
  window.__look(9, 39.5, .3, .22, 4.6, false);
  window.__beforeRender = (dt, T) => { window.__keep([d, p, window.__F(), window.__R()], 9, 39.5, 3); window.__z0(d); window.__z0(p);
    const zd = Math.min(40.3, 37.2 + Math.max(0, T) * 1.6), zp = Math.min(40.0, 36.9 + Math.max(0, T - .25) * 1.5);
    window.__S(d, 8.75, zd, 0, zd < 40.3 ? 'walk' : (T < 3.2 ? 'cheer' : 'still'), T * 1.6); window.__S(p, 9.35, zp, 0, zp < 40.0 ? 'walk' : (T > 3.1 ? 'talk' : 'still'), T * 1.6);
    if (T > 3.1) { p.obj.rotation.y = -.9; d.obj.rotation.y = .7; const u = d.obj.userData; u.armL.rotation.x = u.armR.rotation.x = -1.3; }
    window.__C(9.05, 1.35, Math.min(40.1, 38.0 + Math.max(0, T) * 1.2)); P.cam.dist = 4.4 - Math.min(1, T / 3) * .8; P.cam.yaw = .3 - Math.min(1, T / 3) * .25; P.cam.pitch = .2; }; }"""
# c8 the two fishermen side by side, lines in the water: 'Ikan pertamaku... ayo... ayo...' / 'Sabar. Ikannya lagi otw.'
C8 = """async () => { const P = window.__pulau, f = window.__F(), r = window.__R(); window.__fixAll(); const pv = await window.__rodPivot(f); window.__clock = .3; window.__cheer = null; P.player.obj.visible = false;
  window.__look(%s, %s, -.35, .12, 3.6, false);
  window.__beforeRender = (dt, T) => { window.__keep([f, r], 8.2, %s, 4); window.__z0(f); window.__z0(r); pv.rotation.x = .25 + Math.sin(T * 3) * .03;
    window.__S(f, %s, %s, 0, 'still', T); const u = f.obj.userData; u.armL.rotation.x = u.armR.rotation.x = -1.1 + Math.sin(T * 9) * (T < 2.6 ? .08 : 0); u.body.rotation.x = T < 2.6 ? .08 : 0;
    window.__S(r, %s, %s, 0, 'still', T); const v = r.obj.userData; v.armL.rotation.x = v.armR.rotation.x = -1.1; if (T > 2.6) r.obj.rotation.y = -.6;
    window.__C(8.25, .26 + 1.1, %s + .1); P.cam.dist = Math.max(3.0, 3.6 - T * .12); P.cam.yaw = -.35 + T * .03; P.cam.pitch = .12; }; }""" % (FX, FZ, FZ, FX, FZ, RX, RZ, FZ)
# c9 payoff: Rayhan pulls up a sandal ('Lumayan... sandal lagi.'), feros: 'Bang Rayhan... itu sandal atau ikan?', then yanks: 'IKAAAN! Gede banget!'
C9 = """async () => { const P = window.__pulau, f = window.__F(), r = window.__R(); window.__fixAll(); const pv = await window.__rodPivot(f); const pr = await window.__rodPivot(r); window.__clock = .3; window.__cheer = null; P.player.obj.visible = false;
  window.__look(8.4, %s, .3, .06, 3.8, false);
  window.__beforeRender = (dt, T) => { window.__keep([f, r], 8.2, %s, 4); window.__z0(f); window.__z0(r);
    const kr = Math.min(1, Math.max(0, T) / .5), kf = Math.min(1, Math.max(0, T - 4.7) / .5);
    pr.rotation.x = T < 4.6 ? -.55 * kr + Math.sin(T * 6) * .05 : -.55 + .55 * Math.min(1, (T - 4.6) / .4); const v = r.obj.userData; window.__S(r, %s, %s, T < 2.6 ? .4 : .9, 'still', T); v.armL.rotation.x = v.armR.rotation.x = -1.2 - kr * .5 * (T < 4.6 ? 1 : 0);
    window.__S(f, %s, %s, T < 2.6 ? 0 : (T < 4.6 ? -.8 : .25), 'still', T); const u = f.obj.userData; u.armL.rotation.x = u.armR.rotation.x = -1.1 - kf * .8; pv.rotation.x = .2 - kf * .8 + Math.sin(T * 7) * .07 * kf; u.body.rotation.x = -.12 * kf; u.body.position.y = kf > .95 ? Math.abs(Math.sin(T * 8)) * .07 : 0;
    if (T < 4.6) { window.__C(8.35, .26 + 1.5, %s + .15); P.cam.dist = Math.max(3.5, 3.9 - T * .08); P.cam.yaw = .3; } else { window.__C(8.55, .26 + 1.55, 43.1); P.cam.dist = 3.7; P.cam.yaw = .55; } P.cam.pitch = .04; }; }""" % (FZ, FZ, RX, RZ, FX, FZ, FZ)
# c10 Aru congratulates the first fisherman, who holds the fish up; residents cheer on the deck: 'Selamat. Nelayan pertama Pulau Aru.' / 'Dah follow, dah jadi nelayan!'
C10 = """async () => { const P = window.__pulau, f = window.__F(), r = window.__R(); window.__fixAll(); const pv = await window.__rodPivot(f); window.__clock = .3; window.__cheer = true; const W = window.__plain().slice(6, 10);
  window.__look(9.4, 42.2, .5, .14, 3.6, false);
  window.__beforeRender = (dt, T) => { window.__keep([f, r].concat(W), 9.4, 42.2, 4); window.__aruS(9.9, 41.9, -2.3, T < 1.9, T);
    window.__z0(f); window.__S(f, %s, %s, .55, T > 2.0 ? 'cheer' : 'still', T); pv.rotation.x = -.55 + Math.sin(T * 6) * .05; if (T <= 2.0) { const u = f.obj.userData; u.armL.rotation.x = u.armR.rotation.x = -2.3; }
    window.__z0(r); window.__S(r, %s, %s, .6, 'still', T); const v = r.obj.userData; v.armR.rotation.x = -2.5 + Math.sin(T * 8) * .2;
    W.forEach((n, i) => { window.__z0(n); window.__S(n, 8.0 + i * .7, 40.4 + (i %% 2) * .4, .2, 'cheer', T + i * .4); });
    window.__C(9.3, .26 + 1.1, 42.4); P.cam.dist = Math.max(3.0, 3.6 - T * .15); P.cam.yaw = .5 + T * .03; P.cam.pitch = .14; }; }""" % (FX, FZ, RX, RZ)
# c11 night: the harbour lamps on, the two fishermen as silhouettes, the lighthouse far off blinking three times out to sea
C11 = """() => { const P = window.__pulau; window.__clock = .64; window.__cheer = null; P.player.obj.visible = false;
  window.__lhPhase = (30 - ((P.T0 + 1.8) % 30) + 30) % 30;
  window.__look(27.5, -2.5, -1.75, .1, 14, false);
  window.__beforeRender = (dt, T) => { window.__C(28, 5.5, -2); P.cam.dist = 14 - T * .5; P.cam.yaw = -1.75 + T * .02; P.cam.pitch = .12; }; }"""
# c12 end: dusk over the harbour, everyone on the deck waving out to sea, the camera pulls up and away
C12 = """() => { const P = window.__pulau, f = window.__F(), r = window.__R(); window.__fixAll(); window.__clock = .56; window.__cheer = true; const W = window.__plain().slice(0, 8);
  window.__look(%s, %s, .2, .3, 4.5, false);
  window.__beforeRender = (dt, T) => { window.__keep([f, r].concat(W), %s, %s, 3); window.__aruS(9.4, 42.3, 0, false, T); const u = P.player.obj.userData; if (u.armR) { u.armR.rotation.x = -2.7 + Math.sin(T * 8) * .3; u.armL.rotation.x = -.3; }
    window.__S(f, %s, %s, 0, 'wave', T); window.__S(r, %s, %s, 0, 'wave', T + .5);
    W.forEach((n, i) => { window.__z0(n); window.__S(n, 7.5 + (i %% 4) * .95, 40.2 + Math.floor(i / 4) * .9, .1 * (i %% 3 - 1), 'wave', T + i * .4); });
    window.__C(%s, .3 + 1.0 + T * .1, %s + .5); P.cam.yaw = .2 + T * .03; P.cam.dist = 4.5 + T * 1.4; P.cam.pitch = Math.min(.8, .3 + T * .07); }; }""" % (HX, HZ, HX, HZ, FX, FZ, RX, RZ, HX, HZ)
SHOTS = {'c1': (C1, 85), 'c2': (C2, 205), 'c3': (C3, 120), 'c4': (C4, 100), 'c5': (C5, 115), 'c6': (C6, 90), 'c7': (C7, 210),
         'c8': (C8, 170), 'c9': (C9, 215), 'c10': (C10, 155), 'c11': (C11, 150), 'c12': (C12, 245)}
CLEAR = "() => { window.__showInst(); window.__cheer = null; window.__camTarget = null; window.__beforeRender = null; window.__clock = null; window.__tourS = null; const h = window.__bld('pelabuhan'); if (h) { h.visible = true; window.__hbShow(1); } for (const n of window.__pulau.npcs) { if (n.rodPivot) n.rodPivot.rotation.x = 0; n.obj.userData.body.rotation.x = 0; } }"
async def run(which):
    async with async_playwright() as p:
        b, pg = await setup(p)
        await pg.evaluate(BASE); await pg.evaluate("() => { " + NPC + " }"); await pg.evaluate("() => { " + EXTRA + " }"); await pg.evaluate("() => { " + EP29 + " }")
        for k, (js, n) in SHOTS.items():
            if k in which and 'prev' not in which:
                await shoot(pg, 'e29' + k, int(os.environ.get('N_' + k, n)), start_js=js, warm=12)
                await pg.evaluate(CLEAR)
        if 'prev' in which:
            for k, (js, n) in SHOTS.items():
                if 'all' not in which and k not in which: continue
                for w in os.environ.get('WARMS', os.environ.get('WARM', '40')).split('/'):
                    await shoot(pg, 'p29' + k + ('' if '/' not in os.environ.get('WARMS', '') else '_' + w), 1, start_js=js, warm=int(w))
                    await pg.evaluate(CLEAR)
        await b.close()
if __name__ == "__main__": asyncio.run(run(sys.argv[1].split(",")))
