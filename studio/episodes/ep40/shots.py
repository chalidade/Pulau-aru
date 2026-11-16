"""Episode 40 "Mall Pulau Aru" shot list (format CERITA, run sore 16 Nov).  usage: DPR=2 python3 shots.py c1,c3,...  (DPR=1 + prev for checks)
No new TikTok comments (Apify failed, Chrome not connected); the request is the long-standing 'mall' from komentar.md (asked repeatedly
since 10 Nov). Mall Pulau Aru (mall x68 y80 r2, facade faces north onto the east street y77-78): automatic sliding door
(userData.slide, window.__doorOpen overrides), TOKO BAJU, TOKO BUNGA (one bouquet 'SUDAH DIPESAN untuk: P.M.'), empty unit DISEWAKAN.
Cast on their real island.json spots: D4L at the door (ask), Aidil YZ crying at Toko Baju, Letisya at the empty unit, the Penjaga
Mercusuar (storyCast) in front of Toko Bunga hiding a bouquet (pose keeperbunga) - start of the ASMARA subplot. Reuses the ep39 chain.
World: mall centre (16.5, 26.5), facade z 25.5, door point z 24.5; local x is mirrored (r2): BAJU x 18.95, BUNGA 14.75, unit 13.3.
"""
import asyncio, sys, os, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'lib'))
from harness import *
def _mod(name, path):
    sp = importlib.util.spec_from_file_location(name, path); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m
E39 = _mod('ep39shots', os.path.join(HERE, '..', 'ep39', 'shots.py'))
CHAIN = E39.CHAIN + (E39.SETUP39,)
SETUP40 = """() => { const P = window.__pulau;
  let m = null; P.scene.traverse(o => { if (o.userData && o.userData.b && o.userData.b.type === 'mall') m = o; }); window.__MALL = m; m.userData.s0 = m.scale.clone();
  const F = s => P.npcs.find(n => n.name === s || (n.name || '').startsWith(s));
  window.__D4 = () => F('D4L'); window.__AI = () => F('Aidil'); window.__LE = () => F('Letisya'); window.__PM = () => F('Penjaga Mercusuar');
  window.__fix40 = () => { window.__fix39(); m.visible = true; m.scale.copy(m.userData.s0); window.__doorOpen = 0;
    for (const f of [window.__D4, window.__AI, window.__LE, window.__PM]) { const n = f(); if (!n) continue; n.obj.visible = true; const c = n.castSpot; if (c && n.spot && Math.hypot(n.spot.x - c.x, n.spot.z - c.z) > .3) n.spot = Object.assign({}, n.spot, c); if (c && Math.hypot(n.x - c.x, n.z - c.z) > .3) { n.x = c.x; n.z = c.z; n.tx = null; n.tz = null; n.moving = false; n.state = 'work'; n.obj.position.set(c.x, P.surfaceY(c.x, c.z), c.z); n.obj.rotation.y = c.face; } } };
}"""
POS = """() => { const o = {}; for (const [k, f] of Object.entries({ d4: window.__D4, ai: window.__AI, le: window.__LE, pm: window.__PM })) { const n = f(); o[k] = n ? [n.name, +n.x.toFixed(2), +n.z.toFixed(2), +n.obj.position.y.toFixed(2), +n.obj.rotation.y.toFixed(2)] : null; }
  const m = window.__MALL; o.mall = [m.position.x, m.position.y, m.position.z, m.rotation.y]; return o; }"""
HEAD = """const P = window.__pulau; window.__fix40(); window.__clock = .42; window.__cheer = null; """
DOOR = """const dr = (T, a, b) => { window.__doorOpen = T > a && T < b ? 1 : 0; };"""
# c1 cold open: D4L at the automatic door, three-quarter from the north-west; 'Permisi... boleh masuk?' -> the door slides open
# by itself (T 1.6), D4L hops back, the door closes again (T 2.5)
C1 = """() => { """ + HEAD + DOOR + """ P.player.obj.visible = false; const d = window.__D4(), x = d.x, z = d.z, y0 = d.obj.position.y;
  window.__look(x, z, 2.35, .08, 2.2, false);
  window.__beforeRender = (dt, T) => { dr(T, 1.5, 2.6); const hop = T > 1.65 && T < 2.0 ? Math.sin((T - 1.65) / .35 * Math.PI) * .12 : 0;
    d.obj.rotation.y = T < 1.5 ? 1.75 : 2.2; d.obj.position.y = y0 + hop; d.obj.position.z = z - Math.min(.25, Math.max(0, T - 1.65) * .8);
    window.__C(x - .15, y0 + 1.15, z + .35); P.cam.dist = Math.max(1.9, 2.3 - T * .12); P.cam.yaw = 2.35; P.cam.pitch = .08; window.__clr([d], x, z, .5); }; }"""
# c2 premise: aerial over the island gliding down onto the east street and the mall
C2 = """() => { """ + HEAD + """ P.player.obj.visible = false;
  window.__look(10, 18, 2.6, 1.08, 62, false);
  window.__beforeRender = (dt, T) => { const k = Math.min(1, Math.max(0, T) / 5.0), e = k * k * (3 - 2 * k); window.__C(10 + 6.5 * e, 1 + 1.5 * e, 18 + 6.5 * e); P.cam.dist = 62 - 46 * e; P.cam.pitch = 1.08 - .33 * e; P.cam.yaw = 2.6 + .54 * e; }; }"""
# c3 'resmi dibuka': the mall pops up (T .5-1.1), the crowd cheers
C3 = """() => { """ + HEAD + """ P.player.obj.visible = false; const m = window.__MALL;
  window.__look(16.5, 25.5, 3.14, 1.0, 12.5, false);
  window.__beforeRender = (dt, T) => { const u = Math.max(0, Math.min(1, (T - .4) / .6)); const s = u <= 0 ? .001 : (u < 1 ? 1 + Math.sin(u * Math.PI) * .2 - (1 - u) * .9 : 1);
    m.scale.set(m.userData.s0.x * Math.max(.001, Math.min(1.2, s)), m.userData.s0.y * Math.max(.001, s), m.userData.s0.z * Math.max(.001, Math.min(1.2, s)));
    for (const f of [window.__D4, window.__AI, window.__LE, window.__PM]) { const n = f(); if (n) n.obj.visible = T > 1.0; }
    window.__cheer = T > .9 ? 1 : null; window.__C(16.5, 2.0, 25.8); P.cam.dist = 12.5 - T * .5; P.cam.yaw = 3.14 + T * .03; P.cam.pitch = 1.0; }; }"""
# c4 two-shot at Toko Baju: Aidil (right) crying happily, Aru (left) 'Dil, tokonya baru tiga.' at T ~3.5
C4 = """() => { """ + HEAD + """ const a = window.__AI(), ax = a.x - .75, az = a.z - .1, mx = (ax + a.x) / 2, mz = (az + a.z) / 2;
  window.__look(ax, az, 3.14, .1, 2.8, true);
  window.__beforeRender = (dt, T) => { window.__aruS(ax, az, T < 3.3 ? 2.2 : 1.7, T > 3.4 && T < 4.6, T); a.obj.rotation.y = 3.4;
    window.__C(mx, P.surfaceY(mx, mz) + 1.0, mz); P.cam.dist = Math.max(2.4, 2.9 - T * .08); P.cam.yaw = 3.14; P.cam.pitch = .1; window.__clr([a], mx, mz, .6); }; }"""
# c5 Aru next to D4L at the door: 'itu pintu otomatis. Jalan aja!' -> D4L steps forward, the door opens (T 2.9), he bows
# 'Makasih ya, pintu...' and steps back; the door closes (T 4.6)
C5 = """() => { """ + HEAD + DOOR + """ const d = window.__D4(), x = d.x, z = d.z, ax = x + .8, az = z - .1, y0 = d.obj.position.y;
  window.__look(x, z, 3.14, .1, 2.9, true);
  window.__beforeRender = (dt, T) => { dr(T, 2.8, 4.6); window.__aruS(ax, az, T < 2.7 ? -1.9 : -2.6, T < 2.7, T);
    const bow = T > 3.0 && T < 4.4 ? Math.sin(Math.min(1, (T - 3.0) / .5) * Math.PI / 2) * .45 : 0; d.obj.rotation.y = T < 2.7 ? 1.7 : .8; d.obj.rotation.x = bow;
    const mx = x + .4, mz = z; window.__C(mx, y0 + 1.0, mz); P.cam.dist = Math.max(2.5, 2.9 - T * .06); P.cam.yaw = 3.14; P.cam.pitch = .1; window.__clr([d], mx, mz, .6); }; }"""
# c6 'Yah, ketutup. Boleh buka lagi?': D4L alone in front of the closed glass, from the side, hand half-raised; push-in
C6 = """() => { """ + HEAD + """ P.player.obj.visible = false; window.__doorOpen = 0; const d = window.__D4(), x = d.x, z = d.z, y0 = d.obj.position.y;
  window.__look(x, z, 1.9, .06, 2.0, false);
  window.__beforeRender = (dt, T) => { d.obj.rotation.y = 1.85; window.__C(x, y0 + 1.1, z + .2); P.cam.dist = Math.max(1.6, 2.1 - T * .15); P.cam.yaw = 1.9; P.cam.pitch = .06; window.__clr([d], x, z, .5); }; }"""
# c7 'Ada toko baju. Ada toko bunga. Dan toko ketiga...': a dolly along the facade from east to west
C7 = """() => { """ + HEAD + """ P.player.obj.visible = false;
  window.__look(19, 24.8, 3.14, .12, 3.4, false);
  window.__beforeRender = (dt, T) => { const k = Math.min(1, Math.max(0, T) / 3.7), e = k * k * (3 - 2 * k); const x = 19.2 - 6.0 * e;
    window.__C(x, 1.4, 25.0); P.cam.dist = 3.4; P.cam.yaw = 3.14 + .25 - .25 * e; P.cam.pitch = .12; window.__clr([], x, 25, .5); }; }"""
# c8 Letisya, arms folded, in front of the DISEWAKAN poster: 'Masih kosong. Santai aja...'
C8 = """() => { """ + HEAD + """ P.player.obj.visible = false; const l = window.__LE(), x = l.x, z = l.z, y0 = l.obj.position.y;
  window.__look(x, z, 3.0, .08, 2.3, false);
  window.__beforeRender = (dt, T) => { l.obj.rotation.y = 3.0; window.__C(x + .2, y0 + 1.15, z + .5); P.cam.dist = Math.max(2.0, 2.4 - T * .08); P.cam.yaw = 3.0; P.cam.pitch = .08; window.__clr([l], x, z, .5); }; }"""
# c9 the bouquet in the flower shop window with its tag 'SUDAH DIPESAN / untuk: P.M.' (slow push-in)
C9 = """() => { """ + HEAD + """ P.player.obj.visible = false; const v = window.__MALL.userData.bouquet.getWorldPosition(new P.cam.target.constructor());
  window.__look(v.x, v.z, 3.14, .05, 1.6, false);
  window.__beforeRender = (dt, T) => { window.__C(v.x + .22, v.y + .02, v.z); P.cam.dist = Math.max(1.15, 1.55 - T * .08); P.cam.yaw = 3.14 + .12; P.cam.pitch = .05; window.__clr([], v.x, v.z - .6, .4); }; }"""
# c10 two-shot: Aru (left) 'Penjaga Mercusuar? Bunga itu buat siapa?' / the keeper (right) 'Bukan buat siapa-siapa.'
C10 = """() => { """ + HEAD + """ const k = window.__PM(), ax = k.x + .95, az = k.z - .15, mx = (ax + k.x) / 2, mz = (az + k.z) / 2;
  window.__look(ax, az, 3.14, .1, 2.9, true);
  window.__beforeRender = (dt, T) => { window.__aruS(ax, az, -1.9, T < 2.5, T); k.obj.rotation.y = T < 2.4 ? 3.14 : 2.5;
    window.__C(mx, P.surfaceY(mx, mz) + 1.0, mz); P.cam.dist = Math.max(2.5, 2.9 - T * .08); P.cam.yaw = 3.14; P.cam.pitch = .1; window.__clr([k], mx, mz, .6); }; }"""
# c11 the keeper close, looking at his feet: '...Buat mercusuar.' then a quick pan to Aru (T ~2.3): 'Mercusuar nggak butuh bunga!'
C11 = """() => { """ + HEAD + """ const k = window.__PM(), ax = k.x + .95, az = k.z - .15;
  window.__look(k.x, k.z, 3.14, .08, 1.9, true);
  window.__beforeRender = (dt, T) => { window.__aruS(ax, az, -1.9, T > 2.3, T); k.obj.rotation.y = 2.6;
    const e = Math.min(1, Math.max(0, T - 2.1) / .3); const tx = k.x + (ax - k.x) * e, tz = k.z + (az - k.z) * e;
    window.__C(tx, P.surfaceY(tx, tz) + 1.1, tz); P.cam.dist = 1.9; P.cam.yaw = 3.14 - .25 + .4 * e; P.cam.pitch = .08; window.__clr([k], tx, tz, .5); }; }"""
# c12 mystery: from behind the keeper, the bouquet hidden behind his back; the camera rises and looks past him north toward the lighthouse
C12 = """() => { """ + HEAD + """ P.player.obj.visible = false; const k = window.__PM(), x = k.x, z = k.z, y0 = k.obj.position.y;
  window.__look(x, z, 0, .1, 1.4, false);
  window.__beforeRender = (dt, T) => { k.obj.rotation.y = 3.14; const q = Math.min(1, Math.max(0, T - 2.6) / 3.0), e = q * q * (3 - 2 * q);
    window.__C(x, y0 + .7 + .3 * e, z - .3 * e); P.cam.dist = 1.4 + 1.2 * e; P.cam.yaw = 0 + .3 * e; P.cam.pitch = .1 + .45 * e; window.__clr([k], x, z, .4); }; }"""
# c13 end: Aru waving in front of the mall door, crane up over the mall and the street
C13 = """() => { """ + HEAD + """ window.__cheer = true; const x = 16.5, z = 23.6;
  window.__look(x, z, 3.14, .12, 2.8, true);
  window.__beforeRender = (dt, T) => { window.__aruS(x, z, 3.14, false, T); const u = P.player.obj.userData; if (u.armR) u.armR.rotation.x = -2.7 + Math.sin(T * 8) * .25;
    const k = Math.min(1, Math.max(0, T - 1.5) / 6), e = k * k * (3 - 2 * k);
    window.__C(x, P.surfaceY(x, z) + 1.1 + 1.0 * e, z + 1.2 * e); P.cam.dist = 2.8 + 5.5 * e; P.cam.yaw = 3.14; P.cam.pitch = .12 + 1.15 * Math.sqrt(e); window.__clr([], x, z, .6); }; }"""
SHOTS = {'c1': (C1, 95), 'c2': (C2, 165), 'c3': (C3, 115), 'c4': (C4, 160), 'c5': (C5, 165), 'c6': (C6, 90), 'c7': (C7, 130),
         'c8': (C8, 130), 'c9': (C9, 160), 'c10': (C10, 135), 'c11': (C11, 125), 'c12': (C12, 185), 'c13': (C13, 290)}
CLEAR = E39.CLEAR
async def run(which):
    async with async_playwright() as p:
        b, pg = await setup(p)
        for js in CHAIN + (SETUP40,): await pg.evaluate(js)
        if 'pos' in which: print(await pg.evaluate(POS))
        for k, (js, n) in SHOTS.items():
            if k in which and 'prev' not in which:
                await shoot(pg, 'e40' + k, int(os.environ.get('N_' + k, n)), start_js=js, warm=12)
                await pg.evaluate(CLEAR)
        if 'prev' in which:
            for k, (js, n) in SHOTS.items():
                if 'all' not in which and k not in which: continue
                for w in os.environ.get('WARMS', os.environ.get('WARM', '40')).split('/'):
                    await shoot(pg, 'p40' + k + ('' if '/' not in os.environ.get('WARMS', '') else '_' + w), 1, start_js=js, warm=int(w))
                    await pg.evaluate(CLEAR)
        await b.close()
if __name__ == "__main__": asyncio.run(run(sys.argv[1].split(",")))
