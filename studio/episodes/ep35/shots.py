"""Episode 35 "Mau Jadi Pilot, Dapat Bandara" shot list (format KONSEP).  usage: DPR=2 python3 shots.py c1,c3,...  (DPR=1 + prev for checks)
Two queued comments (komentar.md): @salmanajalah3 wants to be a pilot (asked twice) -> Bandara Pulau Aru (bandara x86 y90 r2, deck over
the sea off the east field) with the plane PK-ARU that takes off, circles the island trailing a banner (PEMILU PRESIDEN SEGERA!) and lands
(main.js stepPlane; window.__planeU pins it); salmanajalah3 becomes the Pilot Pertama (resident spot by the plane, pose 'pilot').
@darsetecuu "tambah rumah buat makanan" -> Rumah Makan (rumahmakan x70 y74 r0) whose fish sleeps in the KAMAR IKAN.
Cast: -VANZwlee (Revan, penumpang pertama), lala cute (kue) — neither in the last 4 episodes. Reuses ep34 helpers.
"""
import asyncio, sys, os, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'lib'))
from harness import *
def _mod(name, path):
    sp = importlib.util.spec_from_file_location(name, path); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m
E34 = _mod('ep34shots', os.path.join(HERE, '..', 'ep34', 'shots.py'))
E33 = E34.E33
BASE, NPC, EXTRA, EP29, EP31, EP32, SETUP33, SETUP34 = E34.BASE, E34.NPC, E34.EXTRA, E34.EP29, E34.EP31, E34.EP32, E34.SETUP33, E34.SETUP34
SETUP35 = """() => { const P = window.__pulau; let B = null; P.scene.traverse(o => { if (!B && o.userData && o.userData.plane) B = o; });
  window.__BAN = B; const pl = B.userData.plane; window.__PL = pl;
  window.__ease = u => u < .5 ? 2 * u * u : 1 - Math.pow(-2 * u + 2, 2) / 2;
  window.__pp = u => { const c = pl.userData.curve; return c.getPointAt(Math.min(.9999, Math.max(0, window.__ease(u)))); };
  window.__pdir = u => { const a = window.__pp(u), b = window.__pp(Math.min(1, u + .004)); const d = b.clone().sub(a); if (d.length() < 1e-4) d.set(-1, 0, 0); return d.normalize(); };
  window.__REV = () => window.__N('-VANZwlee'); window.__LALA = () => window.__N('lala cute'); window.__PIL = () => window.__N('salmanajalah3');
  window.__fix35 = () => { window.__fix34(); for (const f of [window.__REV, window.__LALA, window.__PIL]) { const n = f(); if (n) window.__fix(n); } };
  window.__GULL.visible = false; window.__LNEST.visible = false; }"""
# chase helper: camera behind/side of the plane at flight position u. side = yaw offset from 'behind'
CHASE = """const p = window.__pp(u), d = window.__pdir(u); window.__planeU = u; window.__C(p.x - d.x * BACK, p.y + .8 - d.y * BACK, p.z - d.z * BACK); P.cam.yaw = (SIDE > 9 ? Math.atan2(p.x, p.z) + SIDE - 10 : Math.atan2(-d.x, -d.z) + SIDE); P.cam.dist = DIST; P.cam.pitch = PITCH;"""
def chase(u0, u1, dur, side, dist, pitch, extra='', back=0):
    body = CHASE.replace('BACK', str(back)).replace('SIDE', str(side)).replace('DIST', str(dist)).replace('PITCH', str(pitch))
    return """() => { const P = window.__pulau; window.__fix35(); window.__clock = .4; window.__cheer = null; P.player.obj.visible = false;
  window.__planeU = %s; window.__look(0, 0, 0, .5, 10, false);
  window.__beforeRender = (dt, T) => { const u = %s + (%s - %s) * Math.min(1, Math.max(0, T) / %s); %s %s }; }""" % (u0, u0, u1, u0, dur, body, extra)
# c1 cold open: PK-ARU rolls and lifts off the runway right past the camera (Aru: 'Satu komentar mau jadi pilot... kami bikinin BANDARA!')
C1 = """() => { const P = window.__pulau; window.__fix35(); window.__clock = .4; window.__cheer = null; P.player.obj.visible = false;
  window.__planeU = .07; window.__look(36, 39, 0, .2, 6, false);
  window.__beforeRender = (dt, T) => { const u = .07 + .085 * Math.min(1, Math.max(0, T) / 3.6); window.__planeU = u; const p = window.__pp(u);
    window.__C(p.x + .3, p.y + .8, p.z); P.cam.yaw = .12 - T * .05; P.cam.dist = 7.5 - T * .3; P.cam.pitch = .12; }; }"""
# c2 premise + comment cards: high chase over the island, banner flying
C2 = chase(.26, .34, 6.6, 10.35, 13, .42)
# c4 Aru on the runway, pointing down the deck ('Pilot butuh pesawat. Pesawat butuh... landasan!')
C4 = """() => { const P = window.__pulau; window.__fix35(); window.__clock = .4; window.__cheer = null; window.__planeU = -1;
  const x = 34.0, z = 38.9; window.__look(x, z, -.35, .15, 2.8, true);
  window.__beforeRender = (dt, T) => { window.__aruS(x, z, -.35, T > .1 && T < 1.4, T); const u = P.player.obj.userData; if (T > 1.4 && u.armR) { u.armR.rotation.x = -1.6; u.armR.rotation.z = .9; }
    window.__C(x + .3, P.surfaceY(x, z) + 1.1, z); P.cam.dist = Math.max(2.3, 2.8 - T * .15); P.cam.yaw = -.35; P.cam.pitch = .15; }; }"""
# c5 reveal: aerial orbit down onto the Bandara (runway, tower, terminal, parked plane)
C5 = """() => { const P = window.__pulau; window.__fix35(); window.__clock = .4; window.__cheer = null; P.player.obj.visible = false; window.__planeU = -1;
  window.__look(38, 37, 2.2, 1.1, 34, false);
  window.__beforeRender = (dt, T) => { const k = Math.min(1, T / 5.6), e = k * k * (3 - 2 * k); window.__C(38 + 2 * e, .5 + 1.0 * e, 37 + .5 * e); P.cam.dist = 34 - 20 * e; P.cam.pitch = 1.1 - .62 * e; P.cam.yaw = 2.2 + .9 * e; }; }"""
# c6 Revan (si paling keren) poses by the terminal with his ticket ('Namaku... Revan. Penumpang pertama.')
C6 = """() => { const P = window.__pulau, r = window.__REV(); window.__fix35(); window.__clock = .4; window.__cheer = null; P.player.obj.visible = false; window.__planeU = -1;
  const x = 41.6, z = 36.9; window.__look(x, z, -.5, .12, 2.6, false);
  window.__beforeRender = (dt, T) => { window.__z0(r); window.__S(r, x, z, -.5, 'still', T); const u = r.obj.userData; if (T < 1.6) { u.armR.rotation.x = -2.3; u.armR.rotation.z = -.3; u.armL.rotation.x = .2; } else { u.armR.rotation.x = -1.2; u.armR.rotation.z = .2; u.body.rotation.x = -.06; }
    window.__C(x, P.surfaceY(x, z) + 1.1, z); P.cam.dist = Math.max(2.1, 2.6 - T * .15); P.cam.yaw = -.5; P.cam.pitch = .12; window.__clr([r], x, z, .6); }; }"""
# c7 the Pilot Pertama salutes beside PK-ARU (title PILOT PERTAMA @salmanajalah3)
C7 = """() => { const P = window.__pulau, s = window.__PIL(); window.__fix35(); window.__clock = .4; window.__cheer = null; P.player.obj.visible = false; window.__planeU = -1;
  const x = 43.0, z = 39.6; window.__look(x, z, -.25, .14, 3.4, false);
  window.__beforeRender = (dt, T) => { window.__z0(s); window.__S(s, x, z, -.25, 'still', T); const u = s.obj.userData, c = T % 3.2; u.armR.rotation.x = c < 1.6 ? -2.7 : -.1; u.armR.rotation.z = c < 1.6 ? -.65 : 0; u.armL.rotation.x = 0;
    window.__C(x - .2, P.surfaceY(x, z) + 1.05, z - .5); P.cam.dist = Math.max(2.8, 3.4 - T * .18); P.cam.yaw = -.25 + T * .04; P.cam.pitch = .14; window.__clr([s], x, z, .6); }; }"""
# c8 nose of the plane, propeller spinning up, pilot in the cockpit ('Penumpang, pasang sabuk pengaman! Kita terbang!')
C8 = """() => { const P = window.__pulau; window.__fix35(); window.__clock = .4; window.__cheer = null; P.player.obj.visible = false; window.__planeU = 0;
  window.__look(44, 38.5, 0, .2, 4, false);
  window.__beforeRender = (dt, T) => { const u = Math.max(0, T - 2.4) * .012; window.__planeU = u; const p = window.__pp(u), pl = window.__PL;
    pl.userData.prop.rotation.z = T * T * 6; window.__C(p.x + .6, p.y + 1.0, p.z); P.cam.yaw = 1.0 + T * .06; P.cam.dist = 4.2 - T * .15; P.cam.pitch = .28; }; }"""
# c9 Aru on the east field cheers as the plane climbs past behind him ('Terbaaang! Pulau kita punya pesawat!')
C9 = """() => { const P = window.__pulau; window.__fix35(); window.__clock = .4; window.__cheer = 1; const x = 31.2, z = 39.6;
  window.__look(x, z, -.7, .0, 3.2, true);
  window.__beforeRender = (dt, T) => { const u = .1 + .07 * Math.min(1, T / 2.4); window.__planeU = u; window.__aruS(x, z, -.7, false, T); const a = P.player.obj.userData;
    if (a.armR) { a.armR.rotation.x = a.armL.rotation.x = -2.8 + Math.sin(T * 9) * .25; } P.player.obj.position.y = P.surfaceY(x, z) + Math.abs(Math.sin(T * 6)) * .25;
    window.__C(x + .3, P.surfaceY(x, z) + 1.5 + T * .3, z - .3); P.cam.dist = 3.2; P.cam.yaw = -.7; P.cam.pitch = -.02 - T * .04; window.__clr([], x, z, .6); }; }"""
# c10 over the island (Revan: 'Dari atas... pulau kita kelihatan kayak kue!')
C10 = chase(.36, .42, 4.0, 10.0, 11, .62)
# c11 the banner close up, side-on ('Spanduknya bilang: sebentar lagi, pemilu presiden pulau!')
C11 = chase(.44, .5, 4.4, 10.55, 11.5, .22, back=1.3)
RX, RZ = 15.5, 19.5   # Rumah Makan centre (world), front faces +z (south, toward the east street)
# c12 Rumah Makan reveal: swing down from above to the front (title RUMAH MAKAN · usulan @darsetecuu)
C12 = """() => { const P = window.__pulau; window.__fix35(); window.__clock = .4; window.__cheer = null; P.player.obj.visible = false; window.__planeU = -1;
  window.__look(%s, %s, -.5, .9, 12, false);
  window.__beforeRender = (dt, T) => { const k = Math.min(1, T / 3.0), e = k * k * (3 - 2 * k); window.__C(%s, P.surfaceY(%s, %s) + 2.0, %s + .5); P.cam.dist = 12 - 5.5 * e; P.cam.pitch = .9 - .62 * e; P.cam.yaw = -.5 + .5 * e; }; }""" % (RX, RZ, RX, RX, RZ, RZ)
# c13 Aru at the counter, then the camera finds the KAMAR IKAN on the back wall ('Rumah... buat makanan? Ya udah, makanannya kita kasih kamar!')
C13 = """() => { const P = window.__pulau; window.__fix35(); window.__clock = .4; window.__cheer = null; const x = %s - .7, z = %s + 1.9;
  window.__look(x, z, .3, .12, 2.6, true);
  window.__beforeRender = (dt, T) => { window.__aruS(x, z, .3, T > .1 && T < 3.8, T); const k = Math.min(1, Math.max(0, T - 1.8) / 1.4), e = k * k * (3 - 2 * k);
    window.__C(x + (.95 + .2) * e, P.surfaceY(x, z) + 1.15 + .55 * e, z - 2.85 * e); P.cam.dist = 2.6 - .6 * e; P.cam.yaw = .3 - .3 * e; P.cam.pitch = .12; window.__clr([], x, z, .6); }; }""" % (RX, RZ)
# c14 lala cute offers a cookie at the outside tables ('Rumah makan buka! Mau kue? Semangaaat!')
C14 = """() => { const P = window.__pulau, l = window.__LALA(); window.__fix35(); window.__clock = .4; window.__cheer = null; P.player.obj.visible = false; const x = %s + 1.6, z = %s + 2.4;
  window.__look(x, z, .35, .12, 2.6, false);
  window.__beforeRender = (dt, T) => { window.__z0(l); window.__S(l, x, z, .35, 'still', T); const u = l.obj.userData; u.armR.rotation.x = -1.5 + Math.sin(T * 4) * .15; u.armL.rotation.x = T > 1.8 ? -2.8 + Math.sin(T * 10) * .2 : -.2;
    window.__C(x - .2, P.surfaceY(x, z) + 1.1, z); P.cam.dist = Math.max(2.2, 2.6 - T * .12); P.cam.yaw = .35; P.cam.pitch = .12; window.__clr([l], x, z, .6); }; }""" % (RX, RZ)
# c15 end: the plane lands back on the Bandara at sunset, wide (end card)
C15 = """() => { const P = window.__pulau; window.__fix35(); window.__clock = .45; window.__cheer = null; P.player.obj.visible = false; window.__planeU = .8;
  window.__look(38, 37, .4, .35, 18, false);
  window.__beforeRender = (dt, T) => { const u = .8 + .12 * Math.min(1, T / 4.5); window.__planeU = u; const p = window.__pp(u);
    window.__C(p.x + (38 - p.x) * .4, 1.5, p.z + (37 - p.z) * .4); P.cam.dist = 17 - T * .5; P.cam.yaw = .4 + T * .03; P.cam.pitch = .3; }; }"""
SHOTS = {'c1': (C1, 110), 'c2': (C2, 205), 'c4': (C4, 100), 'c5': (C5, 180), 'c6': (C6, 110), 'c7': (C7, 105), 'c8': (C8, 120),
         'c9': (C9, 80), 'c10': (C10, 125), 'c11': (C11, 135), 'c12': (C12, 95), 'c13': (C13, 125), 'c14': (C14, 100), 'c15': (C15, 200)}
CLEAR = E34.CLEAR[:-1] + " window.__planeU = null; }"
async def run(which):
    async with async_playwright() as p:
        b, pg = await setup(p)
        for js in (BASE, "() => { " + NPC + " }", "() => { " + EXTRA + " }", "() => { " + EP29 + " }", "() => { " + EP31 + " }", "() => { " + EP32 + " }", SETUP33, SETUP34, SETUP35): await pg.evaluate(js)
        print('cast', await pg.evaluate("() => [window.__REV(), window.__LALA(), window.__PIL()].map(n => n ? n.name : null)"))
        for k, (js, n) in SHOTS.items():
            if k in which and 'prev' not in which:
                await shoot(pg, 'e35' + k, int(os.environ.get('N_' + k, n)), start_js=js, warm=12)
                await pg.evaluate(CLEAR)
        if 'prev' in which:
            for k, (js, n) in SHOTS.items():
                if 'all' not in which and k not in which: continue
                for w in os.environ.get('WARMS', os.environ.get('WARM', '40')).split('/'):
                    await shoot(pg, 'p35' + k + ('' if '/' not in os.environ.get('WARMS', '') else '_' + w), 1, start_js=js, warm=int(w))
                    await pg.evaluate(CLEAR)
        await b.close()
if __name__ == "__main__": asyncio.run(run(sys.argv[1].split(",")))
