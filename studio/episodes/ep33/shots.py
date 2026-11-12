"""Episode 33 "Detektif dari Komentar" shot list (format KONSEP).  usage: DPR=2 python3 shots.py c1,c3,...  (DPR=1 + prev for checks)
Mystery subplot part 2 (RUNBOOK 2d). Two calon polisi from the ep31 comments (@mhmmdalfaiz0, @ngala.tcl, queued in komentar.md)
become Detektif Pantai; they set up the Kamera Jaga Malam (cctv x78 y55 r3) by the lighthouse with inyuu's sandal as bait; at night the
camera catches the thief: a seagull (camar) carrying the sandal to the top of the lighthouse. New in the game (ep 33): BT.cctv,
castKit/castPose 'detektif', M.seagull + island.json mystery.gull (perched on the gallery, circles the lamp every 40 s; window.__gullT pins it),
detectives / inyuu / D4L resident spots at the camera. Reuses ep25/ep29/ep31/ep32 helpers.
"""
import asyncio, sys, os, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'lib'))
from harness import *
def _mod(name, path):
    sp = importlib.util.spec_from_file_location(name, path); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m
E32 = _mod('ep32shots', os.path.join(HERE, '..', 'ep32', 'shots.py'))
BASE, NPC, EXTRA, EP29, EP31, EP32 = E32.BASE, E32.NPC, E32.EXTRA, E32.EP29, E32.EP31, E32.EP32
SETUP33 = """async () => { const M = await import('/src/models.js'), P = window.__pulau, sc = P.scene;
  const g = M.seagull(); g.scale.setScalar(1.3); g.visible = false; sc.add(g); window.__GULL = g;
  const bait = g.userData.sandal.clone(); bait.rotation.set(0, .6, 0); bait.visible = false; sc.add(bait); window.__BAIT = bait;
  window.__FA = () => window.__N('mhmmdalfaiz0'); window.__NG = () => window.__N('ngala.tcl'); window.__IN = () => window.__N('inyuu') || window.__N('inyuu416'); window.__DL = () => window.__N('D4L');
  window.__mag = (n, T) => { const u = n.obj.userData; u.armR.rotation.x = -1.75 + Math.sin(T * 2.2) * .05; u.armR.rotation.z = -.1; };
  window.__flap = (T, on) => { const u = window.__GULL.userData, f = on ? Math.sin(T * 16) * .8 : 0; u.wl.rotation.z = f; u.wr.rotation.z = -f; };
  window.__fix33 = () => { window.__fixC(); for (const f of [window.__FA, window.__NG, window.__IN, window.__DL]) { const n = f(); if (n) window.__fix(n); } };
  window.__gullT = 39; }"""
BX, BZ = 24.6, -0.6      # bait sandal between the camera and the lighthouse door
# c1 cold open (night): the seagull at the bait, sandal in its beak, takes off past the camera
C1 = """() => { const P = window.__pulau, g = window.__GULL, gy = P.surfaceY(%s, %s); window.__fix33(); window.__clock = .63; window.__cheer = null; P.player.obj.visible = false;
  window.__look(%s, %s, -1.25, .12, 2.4, false); g.visible = true; window.__BAIT.visible = false; g.userData.sandal.visible = true;
  window.__beforeRender = (dt, T) => { const k = Math.max(0, T - 1.0), x = %s + k * .5, z = %s - k * .35, y = gy + Math.min(2.4, k * k * .35 + k * .3);
    g.position.set(x, y, z); g.rotation.set(T < 1.0 ? .25 * Math.max(0, Math.sin(T * 5)) : -.15, T < 1.0 ? -1.25 : 2.1, 0); window.__flap(T, T > .8);
    window.__C(%s, gy + .75 + Math.min(.6, k * .35), %s); P.cam.dist = Math.max(2.1, 2.4 - T * .1); P.cam.yaw = -1.25 + T * .03; P.cam.pitch = .12; window.__clr([], %s, %s, .5); }; }""" % (BX, BZ, BX, BZ, BX, BZ, BX, BZ, BX, BZ)
# c2 premise: aerial glide from the middle of town to the lighthouse beach (day)
C2 = """() => { const P = window.__pulau; window.__fix33(); window.__clock = .38; window.__cheer = null; P.player.obj.visible = false; window.__GULL.visible = false;
  window.__look(0, 0, .1, 1.05, 50, false);
  window.__beforeRender = (dt, T) => { const k = Math.min(1, Math.max(0, T) / 5.4), e = k * k * (3 - 2 * k); window.__C(23 * e, .5 + 1.5 * e, 0); P.cam.dist = 50 - 37 * e; P.cam.pitch = 1.05 - .6 * e; P.cam.yaw = .1 - .75 * e; }; }"""
# c3 = ep32 c3 (Aru at the BARANG HILANG board: 'Termasuk sandalku. Satu-satunya!')
C3 = E32.C3.replace("window.__fixC();", "window.__fix33(); window.__GULL.visible = false;")
# c4 the two detectives walk out of the lighthouse beach toward the camera, magnifying glasses up (comment cards pop here)
C4 = """() => { const P = window.__pulau, a = window.__FA(), b = window.__NG(); window.__fix33(); window.__clock = .4; window.__cheer = null; P.player.obj.visible = false; window.__GULL.visible = false;
  window.__look(23.85, .75, -.7, .12, 3.0, false);
  window.__beforeRender = (dt, T) => { const k = Math.min(1, Math.max(0, T + .3) / 1.6), w = k < 1; window.__z0(a); window.__z0(b);
    window.__S(a, 23.55 + .9 * (1 - k), .55 - .9 * (1 - k), -.75, w ? 'walk' : 'still', T); window.__S(b, 24.45 + .9 * (1 - k), .95 - .9 * (1 - k), -.6, w ? 'walk' : 'still', T + .4);
    if (!w) { window.__mag(a, T); window.__mag(b, T + 1); a.obj.userData.body.rotation.y = Math.sin(T * .9) * .3; b.obj.userData.body.rotation.y = -Math.sin(T * .8) * .3; }
    window.__C(23.95, P.surfaceY(23.9, .75) + 1.05, .75); P.cam.dist = Math.max(2.6, 3.0 - T * .1); P.cam.yaw = -.7; P.cam.pitch = .12; window.__clr([a, b], 23.9, .75, .9); }; }"""
# c5 = ep32 c4 (RANUUGLL salutes: 'Permintaan diterima. Selamat datang, Detektif Pantai!')
C5 = E32.C4.replace("window.__fixC();", "window.__fix33(); window.__GULL.visible = false;")
# c6 alfaiz bends over the three-toed prints with the magnifying glass
C6 = """() => { const P = window.__pulau, a = window.__FA(); window.__fix33(); window.__clock = .42; window.__cheer = null; P.player.obj.visible = false; window.__GULL.visible = false;
  window.__look(23.0, .9, -1.6, .3, 2.2, false);
  window.__beforeRender = (dt, T) => { window.__z0(a); window.__S(a, 23.25, .75, -1.75, 'still', T); const u = a.obj.userData; u.body.rotation.x = .35 + Math.sin(T * 1.5) * .05; u.armR.rotation.x = -1.25; u.armL.rotation.x = -.4; if (T > 1.8) { u.body.rotation.x = .1; u.armR.rotation.x = -1.8; }
    window.__C(22.85, P.surfaceY(22.9, .8) + .75, .8); P.cam.dist = Math.max(1.8, 2.2 - T * .12); P.cam.yaw = -1.6 + T * .04; P.cam.pitch = .3; window.__clr([a], 22.9, .8, .6); }; }"""
# c7 Aru at the camera pole: 'Kalau gitu, kita pasang kamera jaga malam!' camera tilts up to the REC camera
C7 = """() => { const P = window.__pulau; window.__fix33(); window.__clock = .44; window.__cheer = null; window.__GULL.visible = false;
  window.__look(21.95, .15, -.55, .15, 3.0, true);
  window.__beforeRender = (dt, T) => { window.__aruS(21.95, .15, -.55, T > .1 && T < 2.4, T); const u = P.player.obj.userData; if (T > 1.2 && u.armR) { u.armR.rotation.x = -2.6; u.armR.rotation.z = .2; }
    const k = Math.min(1, Math.max(0, T - 1.0) / 1.6), e = k * k * (3 - 2 * k), g = P.surfaceY(22.2, -.2);
    window.__C(22.05 + .3 * e, g + 1.15 + 1.15 * e, .05 - .45 * e); P.cam.dist = 3.0 - .2 * e; P.cam.yaw = -.55; P.cam.pitch = .15 - .05 * e; window.__clr([], 22.1, 0, .7); }; }"""
# c8 dusk: ngala kneels and sets the bait sandal; inyuu: 'Pakai sandalku aja! GG, warga!' (thumbs up, one bare foot)
C8 = """() => { const P = window.__pulau, b = window.__NG(), i = window.__IN(), bt = window.__BAIT; window.__fix33(); window.__clock = .55; window.__cheer = null; P.player.obj.visible = false; window.__GULL.visible = false;
  const gy = P.surfaceY(%s, %s); bt.position.set(%s, gy + .02, %s); bt.visible = true;
  window.__look(24.4, -.6, -.6, .2, 3.3, false);
  window.__beforeRender = (dt, T) => { window.__z0(b); window.__z0(i); window.__FA().obj.visible = false; window.__DL().obj.visible = false;
    window.__S(b, %s + .3, %s - .45, -.6, 'still', T); const u = b.obj.userData; if (T < 2.6) { u.body.position.y = -.28; u.legL.rotation.x = -1.4; u.legR.rotation.x = -.15; u.body.rotation.x = .2; u.armR.rotation.x = -.9 + Math.sin(T * 4) * .1; u.armL.rotation.x = -.7; } else window.__mag(b, T);
    window.__S(i, 23.75, -1.05, -.5, T > 2.9 && T < 5.5 ? 'talk' : 'still', T); const v = i.obj.userData; if (T > 4.3) { v.armR.rotation.x = -2.6; v.armR.rotation.z = -.2; } v.legL.rotation.x = -.35;
    window.__C(24.4, gy + .8, -.6); P.cam.dist = Math.max(2.9, 3.3 - T * .07); P.cam.yaw = -.6; P.cam.pitch = .2; window.__clr([b, i], 24.4, -.6, .9); }; }""" % ((BX, BZ) * 3)
# c10 night: everybody waits by the camera facing the lighthouse; inyuu nods off and keels over ('aku respawn dulu')
C10 = """() => { const P = window.__pulau, a = window.__FA(), b = window.__NG(), i = window.__IN(), d = window.__DL(); window.__fix33(); window.__clock = .63; window.__cheer = null; window.__GULL.visible = false;
  const gy = P.surfaceY(%s, %s); window.__BAIT.position.set(%s, gy + .02, %s); window.__BAIT.visible = true;
  window.__look(23.8, .4, -1.35, .25, 4.6, true);
  window.__beforeRender = (dt, T) => { for (const n of [a, b, i, d]) window.__z0(n); window.__aruS(23.45, -.2, -1.2, false, T);
    window.__S(a, 23.5, .45, -1.45, 'still', T); window.__mag(a, T); window.__S(b, 24.25, .15, -1.6, 'still', T); window.__mag(b, T + 1);
    window.__S(d, 24.25, .85, -1.3, 'still', T); { const u = d.obj.userData; u.armR.rotation.x = -1.9 + Math.sin(T * 2) * .1; }
    window.__S(i, 23.5, 1.1, -1.5, 'still', T); { const u = i.obj.userData, k = Math.min(1, Math.max(0, T - 4.4) / .5); u.body.rotation.x = .25 + Math.sin(T * 2.2) * .12 * (1 - k); u.body.rotation.z = k * 1.45; u.body.position.y = -k * .35; u.armL.rotation.x = u.armR.rotation.x = -.2; }
    window.__C(23.85, P.surfaceY(23.8, .4) + .95, .45); P.cam.dist = Math.max(4.1, 4.6 - T * .1); P.cam.yaw = -1.35 + T * .02; P.cam.pitch = .25; window.__clr([a, b, i, d], 23.8, .45, 1.2); }; }""" % (BX, BZ, BX, BZ)
# c11 night: the seagull swoops in from the sea, lands on the bait, takes the sandal and flies up toward the lamp ('Itu... BURUNG CAMAR?!')
C11 = """() => { const P = window.__pulau, g = window.__GULL, bt = window.__BAIT, gy = P.surfaceY(%s, %s); window.__fix33(); window.__clock = .63; window.__cheer = null; P.player.obj.visible = false;
  bt.position.set(%s, gy + .02, %s); window.__look(%s, %s, -1.2, .2, 3.2, false); g.visible = true;
  window.__beforeRender = (dt, T) => { let x, y, z, ry = -1.57, fl = true;
    if (T < 2.4) { const k = T / 2.4, e = 1 - (1 - k) * (1 - k); x = %s + 6 * (1 - e); y = gy + 3.2 * (1 - e) * (1 - e); z = %s - 1.5 * (1 - e); ry = -1.57 - .3 * (1 - e); }
    else if (T < 3.3) { x = %s; y = gy; z = %s; ry = -1.25 + Math.sin(T * 6) * .15; fl = false; }
    else { const k = T - 3.3; x = %s + k * 1.0; y = gy + k * k * .5 + k * .6; z = %s - k * .45; ry = 2.0; }
    g.position.set(x, y, z); g.rotation.set(T > 2.4 && T < 3.3 ? .3 * Math.max(0, Math.sin((T - 2.4) * 7)) : 0, ry, 0); window.__flap(T, fl);
    bt.visible = T < 2.75; g.userData.sandal.visible = T >= 2.75;
    const f = Math.min(1, Math.max(0, T - 3.4) / 1.6); window.__C(%s - .2 + f * .8, gy + .45 + f * 1.4, %s - f * .3); P.cam.dist = 3.2 - T * .08; P.cam.yaw = -1.2; P.cam.pitch = .2 - f * .1; window.__clr([], %s, %s, .6); }; }""" % ((BX, BZ) * 7 + (BX, BZ))
# c12 the camera climbs the lighthouse: the seagull perched on the sandal pile, sandal in its beak
C12 = """() => { const P = window.__pulau; window.__fix33(); window.__clock = .585; window.__cheer = null; P.player.obj.visible = false; window.__GULL.visible = false; window.__BAIT.visible = false; const g = P.surfaceY(28, -2);
  window.__look(27.6, -1.4, -.6, .1, 4.5, false);
  window.__beforeRender = (dt, T) => { const k = Math.min(1, Math.max(0, T) / 3.2), e = k * k * (3 - 2 * k); window.__gullT = T < 2.6 ? 5.0 + T * .7 : 39;
    window.__C(27.2, g + 1.5 + (7.5 * e), -1.5); P.cam.dist = 4.5 - 1.7 * e + Math.max(0, T - 3.4) * .05; P.cam.yaw = -.95 + .2 * e; P.cam.pitch = .1 + .35 * e; }; }"""
# c13 end: Aru at the foot of the lighthouse at night ('Tapi... buat apa camar ngumpulin sandal?'), camera rises while the gull circles the lamp
C13 = """() => { const P = window.__pulau; window.__fix33(); window.__clock = .63; window.__cheer = null; window.__GULL.visible = false; window.__BAIT.visible = false;
  window.__look(25.6, -.4, -.9, .16, 2.8, true);
  window.__beforeRender = (dt, T) => { window.__aruS(25.6, -.4, -.9, T > .1 && T < 2.6, T); const u = P.player.obj.userData; if (T > .9 && T < 2.0 && u.armR) { u.armR.rotation.x = -2.8; }
    window.__gullT = T < 3.0 ? 39 : Math.min(39, (T - 3.0) * 1.3);
    const k = Math.min(1, Math.max(0, T - 2.8) / 4.5), e = k * k * (3 - 2 * k);
    window.__C(25.6 + 2.0 * e, P.surfaceY(25.6, -.4) + 1.2 + 7.0 * e, -.4 - 1.2 * e); P.cam.dist = 2.8 + 9 * e; P.cam.yaw = -.9 + .3 * e; P.cam.pitch = .16 + .2 * e; window.__clr([], 25.6, -.4, e < .3 ? .6 : .01); }; }"""
SHOTS = {'c1': (C1, 95), 'c2': (C2, 175), 'c3': (C3, 170), 'c4': (C4, 150), 'c5': (C5, 140), 'c6': (C6, 115), 'c7': (C7, 95),
         'c8': (C8, 185), 'c10': (C10, 200), 'c11': (C11, 165), 'c12': (C12, 205), 'c13': (C13, 230)}
CLEAR = "() => { window.__showInst && window.__showInst(); window.__cheer = null; window.__camTarget = null; window.__beforeRender = null; window.__clock = null; window.__tourS = null; window.__gullT = 39; for (const n of window.__pulau.npcs) { n.obj.visible = true; n.obj.userData.body.rotation.x = 0; n.obj.userData.body.rotation.z = 0; } }"
async def run(which):
    async with async_playwright() as p:
        b, pg = await setup(p)
        for js in (BASE, "() => { " + NPC + " }", "() => { " + EXTRA + " }", "() => { " + EP29 + " }", "() => { " + EP31 + " }", "() => { " + EP32 + " }", SETUP33): await pg.evaluate(js)
        print('cast', await pg.evaluate("() => [window.__FA(), window.__NG(), window.__IN(), window.__DL()].map(n => n ? n.name : null)"))
        for k, (js, n) in SHOTS.items():
            if k in which and 'prev' not in which:
                await shoot(pg, 'e33' + k, int(os.environ.get('N_' + k, n)), start_js=js, warm=12)
                await pg.evaluate(CLEAR)
        if 'prev' in which:
            for k, (js, n) in SHOTS.items():
                if 'all' not in which and k not in which: continue
                for w in os.environ.get('WARMS', os.environ.get('WARM', '40')).split('/'):
                    await shoot(pg, 'p33' + k + ('' if '/' not in os.environ.get('WARMS', '') else '_' + w), 1, start_js=js, warm=int(w))
                    await pg.evaluate(CLEAR)
        await b.close()
if __name__ == "__main__": asyncio.run(run(sys.argv[1].split(",")))
