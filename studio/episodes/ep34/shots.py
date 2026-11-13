"""Episode 34 "Sarang dari Sandal" shot list (format CERITA).  usage: DPR=2 python3 shots.py c1,c3,...  (DPR=1 + prev for checks)
Mystery subplot part 3 (finale, RUNBOOK 2d): the seagull stacked the eight stolen sandals into a nest for three chicks on the
lighthouse gallery. Two queued comments solve it: @alexander______24 asked for a taman -> Taman Pulau (tamancamar x64 y58 r2) with
the Rumah Camar in the middle (the gull family moves there); @sanel1276 asked for a rumah di pantai -> Rumah Pantai (x70 y85).
The sandals go back on the Rak Sandal Kembali by the mosque (raksandal x46 y51, zidan). Aru's sandal stays as the chicks' blanket.
Reuses ep33 helpers (its SETUP33 gull for the night recap).
"""
import asyncio, sys, os, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'lib'))
from harness import *
def _mod(name, path):
    sp = importlib.util.spec_from_file_location(name, path); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m
E33 = _mod('ep33shots', os.path.join(HERE, '..', 'ep33', 'shots.py'))
E32 = E33.E32
BASE, NPC, EXTRA, EP29, EP31, EP32, SETUP33 = E33.BASE, E33.NPC, E33.EXTRA, E33.EP29, E33.EP31, E33.EP32, E33.SETUP33
SETUP34 = """() => { const P = window.__pulau, sc = P.scene; let L = null, T = null;
  sc.traverse(o => { if (!L && o.userData && o.userData.lamps && o.userData.top) L = o; if (!T && o.userData && o.userData.chicks) T = o; });
  window.__TAMAN = T; window.__LH = L;
  const n = T.userData.nest.clone(true); n.scale.setScalar(.85); n.position.set(.55, L.userData.top - .48, .42); n.visible = false; L.add(n); window.__LNEST = n;
  n.traverse(o => { if (o.isMesh) o.castShadow = false; });
  window.__chicksOf = nest => nest.children.filter(c => c.children.length >= 6 && c.children.length <= 8);
  window.__beg = (nest, T) => window.__chicksOf(nest).forEach((c, i) => { const p = Math.max(0, Math.sin(T * 4 + i * 2.1)); c.position.y = .05 + p * .06; c.rotation.x = -p * .4; });
  window.__wp = o => { const v = new o.position.constructor(); o.updateMatrixWorld(true); o.getWorldPosition(v); return v; };
  window.__ZI = () => (window.__N('panggil aja zidan🤩') || window.__N('panggil aja zidan')); window.__SE = () => window.__N('apriantoro') || window.__N('senar muliya'); window.__ALIF = () => window.__N('ALIF HR'); window.__NOVA = () => window.__N('NOVA');
  window.__fix34 = () => { window.__fix33(); for (const f of [window.__ZI, window.__SE, window.__ALIF, window.__NOVA]) { const m = f(); if (m) window.__fix(m); } };
  window.__GULL.visible = false; }"""
TX, TZ = 11.5, 5.0        # Taman Pulau centre (world)
# c1 cold open: the sandal nest on the lighthouse gallery, chicks begging, camera pushes in ('Sandal kita... jadi SARANG BAYI?!')
C1 = """() => { const P = window.__pulau, n = window.__LNEST; window.__fix34(); window.__clock = .4; window.__cheer = null; P.player.obj.visible = false; n.visible = true; window.__gullT = 39;
  const w = window.__wp(n); window.__look(w.x, w.z, -.6, .3, 1.7, false);
  window.__beforeRender = (dt, T) => { window.__beg(n, T); window.__C(w.x, w.y + .15, w.z); P.cam.dist = Math.max(1.15, 1.7 - T * .2); P.cam.yaw = -.6 + T * .05; P.cam.pitch = .3; }; }"""
# c2 premise: aerial from the town centre gliding toward the new Taman Pulau
C2 = """() => { const P = window.__pulau; window.__fix34(); window.__clock = .38; window.__cheer = null; P.player.obj.visible = false; window.__LNEST.visible = false;
  window.__look(0, 0, .1, 1.05, 50, false);
  window.__beforeRender = (dt, T) => { const k = Math.min(1, Math.max(0, T) / 6.0), e = k * k * (3 - 2 * k); window.__C(%s * e, .5 + 1.0 * e, %s * e); P.cam.dist = 50 - 32 * e; P.cam.pitch = 1.05 - .4 * e; P.cam.yaw = .1 + 2.9 * e; }; }""" % (TX, TZ)
# c3 night recap = ep33 c11 (the gull takes the bait sandal)
C3 = E33.C11.replace("window.__fix33();", "window.__fix34(); window.__LNEST.visible = false;")
# c4 Alexandre at the foot of the lighthouse, hero pose, looks up ('Serahkan padaku! Aku naik!')
C4 = """() => { const P = window.__pulau, a = window.__AX(); window.__fix34(); window.__clock = .4; window.__cheer = null; P.player.obj.visible = false; window.__LNEST.visible = true;
  const x = 25.6, z = -.4; window.__look(x, z, -.9, .05, 2.3, false);
  window.__beforeRender = (dt, T) => { window.__z0(a); window.__S(a, x, z, -.9, 'still', T); if (T < .9) window.__hero(a, T); else { const u = a.obj.userData; u.armR.rotation.x = -2.9; u.armR.rotation.z = .1; u.armL.rotation.x = .2; u.body.rotation.x = -.1; }
    window.__C(x, P.surfaceY(x, z) + 1.1 + Math.min(.35, Math.max(0, T - 1.0) * .3), z); P.cam.dist = Math.max(1.9, 2.3 - T * .15); P.cam.yaw = -.9; P.cam.pitch = .05 - Math.min(.12, Math.max(0, T - 1.0) * .1); window.__clr([a], x, z, .7); }; }"""
# c5 the reveal on the gallery: wider, the gull lands by the nest, chicks beg
C5 = """() => { const P = window.__pulau, n = window.__LNEST; window.__fix34(); window.__clock = .4; window.__cheer = null; P.player.obj.visible = false; n.visible = true;
  const w = window.__wp(n); window.__look(w.x, w.z, -1.0, .45, 3.2, false);
  window.__beforeRender = (dt, T) => { window.__beg(n, T); window.__C(w.x, w.y + .1, w.z); P.cam.dist = Math.max(1.6, 3.2 - T * .35); P.cam.yaw = -1.0 + T * .1; P.cam.pitch = .45 - Math.min(.2, T * .05); }; }"""
# c6 = ep32 c1 (Aidil at the BARANG HILANG board, now happy-crying: 'Hiks... indah banget.')
C6 = E32.C1.replace("window.__fixC();", "window.__fix34(); window.__LNEST.visible = false;")
# c7 Aru at the board: 'Tapi warga butuh sandal. Dan camar butuh rumah.'
C7 = """() => { const P = window.__pulau, a = window.__AI(), r = window.__RA(); window.__fix34(); window.__clock = .38; window.__cheer = null; window.__LNEST.visible = false;
  window.__look(11.4, 34.6, .2, .16, 3.0, true);
  window.__beforeRender = (dt, T) => { a.obj.visible = r.obj.visible = false; window.__aruS(11.8, 34.5, .2, T > .1 && T < 2.6, T);
    window.__C(11.6, P.surfaceY(11.6, 34.3) + 1.15, 34.3); P.cam.dist = Math.max(2.4, 3.0 - T * .15); P.cam.yaw = .2; P.cam.pitch = .16; window.__clr([], 11.6, 34.2, .7); a.obj.visible = r.obj.visible = false; }; }"""
# c8 Taman Pulau reveal: orbit down from above toward the gate (ALIF HR & NOVA, Klub Warga Biasa, next door)
C8 = """() => { const P = window.__pulau; window.__fix34(); window.__clock = .4; window.__cheer = null; P.player.obj.visible = false; window.__LNEST.visible = false;
  window.__look(%s, %s, 3.6, 1.0, 16, false);
  window.__beforeRender = (dt, T) => { const k = Math.min(1, T / 5), e = k * k * (3 - 2 * k); window.__C(%s, P.surfaceY(%s, %s) + .8 + .6 * e, %s); P.cam.dist = 16 - 7 * e; P.cam.pitch = 1.0 - .55 * e; P.cam.yaw = 3.6 - .5 * e; }; }""" % (TX, TZ, TX, TX, TZ, TZ)
# c9 the Rumah Camar in the taman: the gull family, chicks begging under Aru's orange sandal
C9 = """() => { const P = window.__pulau, n = window.__TAMAN.userData.nest; window.__fix34(); window.__clock = .4; window.__cheer = null; P.player.obj.visible = false; window.__LNEST.visible = false;
  const w = window.__wp(n); window.__look(w.x, w.z, 2.7, .3, 2.6, false);
  window.__beforeRender = (dt, T) => { window.__C(w.x, w.y + .15 - Math.max(0, 1 - T) * .3, w.z); P.cam.dist = Math.max(1.5, 2.6 - T * .25); P.cam.yaw = 2.7 + T * .06; P.cam.pitch = .3; }; }"""
# c10 zidan at the Rak Sandal Kembali by the mosque, holding up a sandal ('Sandal siapa ini? Ambil satu-satu ya, kak!')
C10 = """() => { const P = window.__pulau, z = window.__ZI(); window.__fix34(); window.__clock = .38; window.__cheer = null; P.player.obj.visible = false; window.__LNEST.visible = false;
  const x = -9.0, zz = -3.75; window.__look(x, zz, 1.25, .2, 3.0, false); window.__hideInst([[x - 1, zz + 1.5], [x - 2, zz + 2.5], [x + .5, zz + 2], [x - .5, zz + 3]], 1.6);
  window.__beforeRender = (dt, T) => { window.__z0(z); window.__S(z, x, zz, 1.25, 'still', T); const u = z.obj.userData; u.armR.rotation.x = -2.4 + Math.sin(T * 3) * .15; u.armR.rotation.z = -.2; u.armL.rotation.x = T > 1.6 ? -1.2 : -.2;
    window.__C(x - .2, P.surfaceY(x, zz) + 1.0, zz - .45); P.cam.dist = Math.max(2.6, 3.0 - T * .12); P.cam.yaw = 1.25; P.cam.pitch = .2; window.__clr([z], x + .3, zz, .8); }; }"""
# c11 Rumah Pantai reveal: swing around from the sea side to the porch
C11 = """() => { const P = window.__pulau, s = window.__SE(); window.__fix34(); window.__clock = .4; window.__cheer = null; P.player.obj.visible = false; window.__LNEST.visible = false;
  window.__look(15.5, 30.5, -.6, .35, 8.5, false);
  window.__beforeRender = (dt, T) => { const k = Math.min(1, T / 5), e = k * k * (3 - 2 * k); window.__C(15.5, P.surfaceY(15.5, 30.5) + 1.6, 30.6); P.cam.dist = 8.5 - 2.5 * e; P.cam.yaw = -.6 + .7 * e; P.cam.pitch = .35 - .12 * e; }; }"""
# c12 senar muliya plays a housewarming song on the sand in front of the porch; the string snaps
C12 = """() => { const P = window.__pulau, s = window.__SE(); window.__fix34(); window.__clock = .4; window.__cheer = null; P.player.obj.visible = false; window.__LNEST.visible = false;
  const x = 15.5, z = 32.6; window.__look(x, z, .15, .15, 2.6, false);
  window.__beforeRender = (dt, T) => { s.obj.visible = true; window.__S(s, x, z, .15, 'guitar', T); if (T > 3.4) { const u = s.obj.userData, k = Math.min(1, (T - 3.4) / .3); u.body.rotation.x = -.15 * k; u.armR.rotation.x = -.2 * k + (u.armR.rotation.x) * (1 - k); }
    window.__C(x, P.surfaceY(x, z) + 1.15, z - .4); P.cam.dist = Math.max(2.1, 2.6 - T * .1); P.cam.yaw = .15; P.cam.pitch = .15; window.__clr([s], x, z, .6); }; }"""
# c13 end: Aru under the Rumah Camar ('Sandalku? Biar jadi selimut bayi camar aja.'), camera rises over the nest and the taman
C13 = """() => { const P = window.__pulau, n = window.__TAMAN.userData.nest; window.__fix34(); window.__clock = .45; window.__cheer = null; window.__LNEST.visible = false;
  const w = window.__wp(n), x = %s + .2, z = %s + 1.15; window.__look(x, z, 0, .12, 2.6, true);
  window.__beforeRender = (dt, T) => { window.__aruS(x, z, 0, T > .1 && T < 2.6, T); const u = P.player.obj.userData; if (T > 1.5 && T < 2.6 && u.armR) u.armR.rotation.x = -2.6;
    const k = Math.min(1, Math.max(0, T - 2.7) / 4.0), e = k * k * (3 - 2 * k);
    window.__C(x + (w.x - x) * e, P.surfaceY(x, z) + 1.15 + (w.y - P.surfaceY(x, z) - .95) * e, z + (w.z - z) * e); P.cam.dist = 2.6 + 4.5 * e; P.cam.yaw = .4 * e; P.cam.pitch = .12 + .5 * e; window.__clr([], x, z, e < .2 ? .6 : .01); }; }""" % (TX, TZ)
SHOTS = {'c1': (C1, 95), 'c2': (C2, 180), 'c3': (C3, 150), 'c4': (C4, 75), 'c5': (C5, 170), 'c6': (C6, 80), 'c7': (C7, 95),
         'c8': (C8, 160), 'c9': (C9, 150), 'c10': (C10, 115), 'c11': (C11, 160), 'c12': (C12, 175), 'c13': (C13, 270)}
CLEAR = E33.CLEAR
async def run(which):
    async with async_playwright() as p:
        b, pg = await setup(p)
        for js in (BASE, "() => { " + NPC + " }", "() => { " + EXTRA + " }", "() => { " + EP29 + " }", "() => { " + EP31 + " }", "() => { " + EP32 + " }", SETUP33, SETUP34): await pg.evaluate(js)
        print('cast', await pg.evaluate("() => [window.__AX(), window.__AI(), window.__ZI(), window.__SE(), window.__ALIF(), window.__NOVA()].map(n => n ? n.name : null)"))
        for k, (js, n) in SHOTS.items():
            if k in which and 'prev' not in which:
                await shoot(pg, 'e34' + k, int(os.environ.get('N_' + k, n)), start_js=js, warm=12)
                await pg.evaluate(CLEAR)
        if 'prev' in which:
            for k, (js, n) in SHOTS.items():
                if 'all' not in which and k not in which: continue
                for w in os.environ.get('WARMS', os.environ.get('WARM', '40')).split('/'):
                    await shoot(pg, 'p34' + k + ('' if '/' not in os.environ.get('WARMS', '') else '_' + w), 1, start_js=js, warm=int(w))
                    await pg.evaluate(CLEAR)
        await b.close()
if __name__ == "__main__": asyncio.run(run(sys.argv[1].split(",")))
