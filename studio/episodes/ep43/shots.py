"""Episode 43 "Dua Ikan Bakar" shot list (format KONSEP, run pagi 18 Nov).  usage: DPR=2 python3 shots.py c1,c3,...  (DPR=1 + prev for checks)
No new TikTok comments (Apify failed again, Chrome not connected), so the episode sells the premise and moves the ASMARA subplot to part 4:
the keeper asked 'besok... boleh dua?', Mbak Sekar grills two fish and sets a little table on the beach by the pier
(mejaduaikan x57 y93, 'MEJA DUA IKAN / untuk P.M. & Mbak Sekar'), and confesses she wrote the first letter. He already knew (the charcoal smudge).
The bouquet from the mall is still not given (next episode). Cameos: _Rayhannn` (fisher, sandal again) and lala cute (cookie).
World: table centre (2.0, 38.0); keeper (1.2, 38.0) facing east; Sekar (2.8, 38.0) facing west; tiang salam pole at (1.5, 39.5) (avoid cameras SW of the table).
"""
import asyncio, sys, os, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'lib'))
from harness import *
def _mod(name, path):
    sp = importlib.util.spec_from_file_location(name, path); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m
E42 = _mod('ep42shots', os.path.join(HERE, '..', 'ep42', 'shots.py'))
CHAIN = E42.CHAIN + (E42.SETUP42,)
SETUP43 = """() => { const P = window.__pulau; let mj = null;
  P.scene.traverse(o => { if (o.userData && o.userData.b && o.userData.b.type === 'mejaduaikan') mj = o; }); window.__MJ = mj;
  const F = s => P.npcs.find(n => n.name === s || (n.name || '').startsWith(s));
  window.__RY = () => F('_Rayhannn'); window.__LA = () => F('lala cute');
  window.__fix43 = () => { window.__fix42();
    for (const f of [window.__RY, window.__LA, window.__PM, window.__SK]) { const n = f(); if (!n) continue; n.obj.visible = true; const c = n.castSpot; if (c && n.spot && Math.hypot(n.spot.x - c.x, n.spot.z - c.z) > .3) n.spot = Object.assign({}, n.spot, c); if (c && Math.hypot(n.x - c.x, n.z - c.z) > .3) { n.x = c.x; n.z = c.z; n.tx = null; n.tz = null; n.moving = false; n.state = 'work'; n.obj.position.set(c.x, P.surfaceY(c.x, c.z), c.z); n.obj.rotation.y = c.face; } } };
}"""
POS = """() => { const o = {}; for (const [k, f] of Object.entries({ pm: window.__PM, sk: window.__SK, ry: window.__RY, la: window.__LA })) { const n = f(); o[k] = n ? [n.name, +n.x.toFixed(2), +n.z.toFixed(2), +n.obj.position.y.toFixed(2), +n.obj.rotation.y.toFixed(2)] : null; }
  const m = window.__MJ; o.table = [m.position.x, m.position.y, m.position.z]; return o; }"""
CLK = os.environ.get('CLK', '.42')
HEAD = """const P = window.__pulau; window.__fix43(); window.__clock = """ + CLK + """; window.__cheer = null; P.player.obj.visible = false; """
# Sekar close at the table (keeper hidden, camera from the west-north-west); used for the cold open and the confession
def sekar(arms):
    return """() => { """ + HEAD + """ const k = window.__PM(), n = window.__SK(), x = n.x, z = n.z, y0 = P.surfaceY(x, z), Y = +(window.__Ys || -1.25);
  window.__look(x, z, Y, .08, 2.2, false);
  window.__beforeRender = (dt, T) => { k.obj.visible = false; window.__HEART.visible = false; n.obj.rotation.y = -1.3; const u = n.obj.userData; if (u.body) { u.body.rotation.y = 0; u.body.rotation.x = .05; }
    """ + arms + """
    window.__C(x - .05, y0 + 1.1, z); P.cam.dist = Math.max(1.9, 2.2 - T * .1); P.cam.yaw = Y; P.cam.pitch = .08; window.__clr([n], x, z, .4); }; }"""
# c1 cold open: 'Surat pertama itu... dari aku!' hands to cheeks, a little hop at the end
C1 = sekar("""if (u.armR) u.armR.rotation.x = T < 1.4 ? -1.2 : -2.5; if (u.armL) u.armL.rotation.x = T < 1.4 ? -1.2 : -2.5; n.obj.position.y = y0 + (T > 1.5 && T < 1.9 ? Math.sin((T - 1.5) / .4 * Math.PI) * .07 : 0);""")
# c9 the confession, slower: hands together first, then to the cheeks
C9 = sekar("""if (u.armR) u.armR.rotation.x = T < 2.4 ? -.9 : -2.5; if (u.armL) u.armL.rotation.x = T < 2.4 ? -.9 : -2.5; if (u.body) u.body.rotation.x = T < 2.4 ? .15 : 0;""")
# c11 'Jadi Bapak tahu dari kemarin?!' arms up, bouncing
C11 = sekar("""if (u.armR) u.armR.rotation.x = -2.9; if (u.armL) u.armL.rotation.x = -2.9; n.obj.position.y = y0 + Math.abs(Math.sin(T * 7)) * .08;""")
# c2 premise: aerial over the island gliding south to the beach table
C2 = """() => { """ + HEAD + """
  window.__look(8, 8, -2.6, 1.08, 44, false);
  window.__beforeRender = (dt, T) => { const k = Math.min(1, Math.max(0, T) / 5.0), e = k * k * (3 - 2 * k); window.__C(8 - 6 * e, 1 + .0 * e, 8 + 30 * e); P.cam.dist = 44 - 34 * e; P.cam.pitch = 1.08 - .5 * e; P.cam.yaw = -2.6 + 2.9 * e; }; }"""
# c3 yesterday's reply on the post beside the stall: 'Besok... boleh dua?' slow push
C3 = """() => { """ + HEAD + """ const p = window.__RP, y = p.position.y;
  window.__look(p.position.x, p.position.z, -1.57, .02, 1.9, false);
  window.__beforeRender = (dt, T) => { const q = Math.min(1, T / 6.5), e = q * q * (3 - 2 * q); window.__C(p.position.x - .05, y + 1.1 - .04 * e, p.position.z); P.cam.dist = 1.9 - .45 * e; P.cam.yaw = -1.57 - .2 + .2 * e; P.cam.pitch = .02; }; }"""
# c4 Sekar back at her grill, fanning two fish like mad: 'Jangan gosong, jangan gosong...'; the heart smoke rises
C4 = """() => { """ + HEAD + """ window.__RP.visible = false; const n = window.__SK(), x = 1.35, z = 34.8, y0 = P.surfaceY(x, z);
  window.__look(x, z, -1.3, .08, 1.9, false);
  window.__beforeRender = (dt, T) => { n.obj.position.set(x, y0, z); n.x = x; n.z = z; n.obj.rotation.y = -1.0; const u = n.obj.userData; window.__HEART.visible = true; window.__heartAt(Math.min(.9, .05 + T / 5.5));
    if (u.body) { u.body.rotation.y = 0; u.body.rotation.x = .05; } if (u.armR) u.armR.rotation.x = -1.3 + Math.sin(T * (T > 2.5 ? 24 : 12)) * .45; if (u.armL) u.armL.rotation.x = -.6;
    window.__C(x - .05, y0 + 1.2 + Math.min(.25, T * .05), z); P.cam.dist = Math.max(1.7, 2.1 - T * .08); P.cam.yaw = -1.3; P.cam.pitch = .08; window.__clr([n], x, z, .4); }; }"""
# c5 _Rayhannn` the fisher on the harbour, holding up his catch: '...Sandal lagi. Lumayan.'
C5 = """() => { """ + HEAD + """ const n = window.__RY(), x = n.x, z = n.z, y0 = P.surfaceY(x, z), Y = +(window.__Y5 || .4);
  window.__look(x, z, Y, .1, 2.0, false);
  window.__beforeRender = (dt, T) => { n.obj.rotation.y = Y; window.__C(x, y0 + 1.15, z); P.cam.dist = Math.max(1.7, 2.0 - T * .1); P.cam.yaw = Y; P.cam.pitch = .1; window.__clr([n], x, z, .5); }; }"""
# c6 lala cute with a cookie: 'Mau kue? Biar makan malamnya makin manis!'
C6 = """() => { """ + HEAD + """ const n = window.__LA(), x = n.x, z = n.z, y0 = P.surfaceY(x, z), Y = +(window.__Y6 || .3);
  window.__look(x, z, Y, .1, 2.0, false);
  window.__beforeRender = (dt, T) => { n.obj.rotation.y = Y; n.obj.position.y = y0 + Math.abs(Math.sin(T * 4)) * .06; window.__C(x, y0 + 1.1, z); P.cam.dist = Math.max(1.7, 2.0 - T * .1); P.cam.yaw = Y; P.cam.pitch = .1; window.__clr([n], x, z, .5); }; }"""
# c7 the reveal: crane down from the beach onto the Meja Dua Ikan, both at the table
C7 = """() => { """ + HEAD + """ const k = window.__PM(), n = window.__SK();
  window.__look(2, 38, .6, .75, 9, false);
  window.__beforeRender = (dt, T) => { const q = Math.min(1, T / 4.6), e = q * q * (3 - 2 * q); window.__HEART.visible = false;
    window.__C(2, .9 + .1 * e, 38); P.cam.dist = 9 - 3.5 * e; P.cam.yaw = .6 - .05 * e; P.cam.pitch = .75 - .4 * e; window.__clr([k, n], 2, 38, .8); }; }"""
# keeper close at the table (Sekar hidden; camera from the east-south-east)
def keeper(body):
    return """() => { """ + HEAD + """ const k = window.__PM(), n = window.__SK(), x = k.x, z = k.z, y0 = P.surfaceY(x, z), Y = +(window.__Yk || 1.15);
  window.__look(x, z, Y, .08, 2.4, false);
  window.__beforeRender = (dt, T) => { n.obj.visible = false; window.__HEART.visible = false; k.obj.rotation.y = 1.2; const b = k.obj.userData.body;
    """ + body + """
    window.__C(x + .05, y0 + 1.2, z); P.cam.dist = Math.max(2.1, 2.4 - T * .1); P.cam.yaw = Y; P.cam.pitch = .08; window.__clr([k], x, z, .5); }; }"""
# c8 'Dua ikan. Persis seperti di surat.' looks down at the plates, then up
C8 = keeper("""if (b) b.rotation.x = T < 1.1 ? .25 : 0;""")
# c10 'Aku tahu. Tanda tangannya noda arang.' a small nod
C10 = keeper("""if (b) b.rotation.x = T > 1.6 && T < 2.1 ? .18 : 0;""")
# c12 'Penjaga mercusuar... melihat semuanya.' he turns toward the lighthouse across the bay; the camera rises behind him
C12 = """() => { """ + HEAD + """ const k = window.__PM(), n = window.__SK(), x = k.x, z = k.z, y0 = P.surfaceY(x, z);
  window.__look(x, z, 1.15, .08, 2.4, false);
  window.__beforeRender = (dt, T) => { n.obj.visible = false; const q = Math.min(1, Math.max(0, T - 1.0) / 2.2), e = q * q * (3 - 2 * q);
    k.obj.rotation.y = 1.2 + (2.58 - 1.2) * e; const b = k.obj.userData.body; if (b) b.rotation.x = -.12 * e;
    window.__C(x + .05 + 1.5 * e, y0 + 1.2 + .7 * e, z - 2.4 * e); P.cam.dist = 2.4 + 2.0 * e; P.cam.yaw = 1.15 + (-0.55 - 1.15) * e; P.cam.pitch = .08 + .1 * e; window.__clr([k], x, z, .5); }; }"""
# c13 the bouquet still in the flower-shop window of the mall: 'SUDAH DIPESAN / untuk: P.M.'
C13 = """() => { """ + HEAD + """ const v = window.__MALL.userData.bouquet.getWorldPosition(new P.cam.target.constructor());
  window.__look(v.x, v.z, 3.14, .05, 1.6, false);
  window.__beforeRender = (dt, T) => { window.__C(v.x + .22, v.y + .02, v.z); P.cam.dist = Math.max(1.1, 1.55 - T * .1); P.cam.yaw = 3.14 + .12; P.cam.pitch = .05; window.__clr([], v.x, v.z - .6, .4); }; }"""
# c14 end: both at the table again, lantern on; crane up and back over the beach and the sea
C14 = """() => { """ + HEAD + """ const k = window.__PM(), n = window.__SK();
  window.__look(2, 38, .6, .35, 5.5, false);
  window.__beforeRender = (dt, T) => { const q = Math.min(1, Math.max(0, T - .6) / 7), e = q * q * (3 - 2 * q);
    window.__C(2, 1.0 + 1.5 * e, 38 - 1.5 * e); P.cam.dist = 5.5 + 7 * e; P.cam.yaw = .6 + .3 * e; P.cam.pitch = .35 + .35 * e; window.__clr([k, n], 2, 38, .8); }; }"""
SHOTS = {'c1': (C1, 90), 'c2': (C2, 160), 'c3': (C3, 210), 'c4': (C4, 170), 'c5': (C5, 115), 'c6': (C6, 105), 'c7': (C7, 160),
         'c8': (C8, 80), 'c9': (C9, 135), 'c10': (C10, 92), 'c11': (C11, 62), 'c12': (C12, 108), 'c13': (C13, 135), 'c14': (C14, 260)}
CLEAR = E42.CLEAR[:-1] + " const s = window.__SK && window.__SK(); if (s) s.obj.visible = true; }"
async def run(which):
    async with async_playwright() as p:
        b, pg = await setup(p)
        for js in CHAIN + (SETUP43,): await pg.evaluate(js)
        if os.environ.get('VARS'): await pg.evaluate('() => { ' + os.environ['VARS'] + ' }')
        if 'pos' in which: print(await pg.evaluate(POS))
        for k, (js, n) in SHOTS.items():
            if k in which and 'prev' not in which:
                await shoot(pg, 'e43' + k, int(os.environ.get('N_' + k, n)), start_js=js, warm=12)
                await pg.evaluate(CLEAR)
        if 'prev' in which:
            for k, (js, n) in SHOTS.items():
                if 'all' not in which and k not in which: continue
                for w in os.environ.get('WARMS', os.environ.get('WARM', '40')).split('/'):
                    await shoot(pg, 'p43' + k + ('' if '/' not in os.environ.get('WARMS', '') else '_' + w), 1, start_js=js, warm=int(w))
                    await pg.evaluate(CLEAR)
        await b.close()
if __name__ == "__main__": asyncio.run(run(sys.argv[1].split(",")))
