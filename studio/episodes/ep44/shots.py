"""Episode 44 "Bunga untuk Mbak Sekar" shot list (format CERITA, run sore 18 Nov).  usage: DPR=2 python3 shots.py c1,c3,...  (DPR=1 + prev for checks)
No new TikTok comments (Apify failed again, Chrome not connected), so the ASMARA subplot closes (part 5/5): the keeper picks up the bouquet from
the mall (tag now 'SUDAH DIAMBIL', mall b.taken), gives it to Mbak Sekar at the Meja Dua Ikan (storyCast pose 'sekarbunga'), and while they blush
one grilled fish vanishes (mejaduaikan b.missing: bones left) -> a new light mystery starts: little four-toed paw prints toward the harbour
(island.json mystery.paw + trail). Cameos: -VANZwlee (sok keren, trips) and ALERXMNC (misterius, first scene).
World: table centre (2.0, 38.0); keeper (1.2, 38.0) facing east; Sekar (2.8, 38.0) facing west; paw trail (2.8,38.5)->(6.9,39.5).
"""
import asyncio, sys, os, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'lib'))
from harness import *
def _mod(name, path):
    sp = importlib.util.spec_from_file_location(name, path); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m
E43 = _mod('ep43shots', os.path.join(HERE, '..', 'ep43', 'shots.py'))
CHAIN = E43.CHAIN + (E43.SETUP43,)
SETUP44 = """() => { const P = window.__pulau;
  const F = s => P.npcs.find(n => n.name === s || (n.name || '').startsWith(s));
  window.__VA = () => F('-VANZwlee'); window.__AL = () => F('ALERX');
  window.__kb = null; { const mj = window.__MJ; let src = null, bones = null; for (const c of mj.children) { if (c.type === 'Group' && Math.abs(c.position.y - .81) < .01 && c.position.x < 0) src = c; if (c.type === 'Group' && Math.abs(c.position.y - .79) < .01 && c.position.x > 0) bones = c; }
    const cl = src.clone(); cl.position.x = .2; mj.add(cl); window.__fishBack = on => { cl.visible = !!on; bones.visible = !on; }; }
  window.__giveKB = (front) => { const k = window.__PM(), s = window.__SK(); if (window.__kb) { window.__kb.parent && window.__kb.parent.remove(window.__kb); window.__kb = null; }
    if (front == null) return; const q = s.obj.userData.bouquet.clone(); const b = k.obj.userData.body; b.add(q);
    if (front) { q.position.set(0, .72, .36); q.rotation.set(-.35, 0, 0); } else { q.position.set(.05, .62, -.26); q.rotation.set(.5, 0, 0); } window.__kb = q; };
  window.__fix44 = () => { window.__fix43(); window.__giveKB(null); window.__fishBack(!window.__gone); const s = window.__SK(); if (s && s.obj.userData.bouquet) s.obj.userData.bouquet.visible = true;
    for (const f of [window.__VA, window.__AL]) { const n = f(); if (!n) continue; n.obj.visible = true; const c = n.castSpot; if (c && n.spot && Math.hypot(n.spot.x - c.x, n.spot.z - c.z) > .3) n.spot = Object.assign({}, n.spot, c); if (c && Math.hypot(n.x - c.x, n.z - c.z) > .3) { n.x = c.x; n.z = c.z; n.tx = null; n.tz = null; n.moving = false; n.state = 'work'; n.obj.position.set(c.x, P.surfaceY(c.x, c.z), c.z); n.obj.rotation.y = c.face; } } };
}"""
POS = """() => { const o = {}; for (const [k, f] of Object.entries({ pm: window.__PM, sk: window.__SK, va: window.__VA, al: window.__AL })) { const n = f(); o[k] = n ? [n.name, +n.x.toFixed(2), +n.z.toFixed(2), +n.obj.position.y.toFixed(2), +n.obj.rotation.y.toFixed(2)] : null; }
  const m = window.__MJ; o.table = [m.position.x, m.position.y, m.position.z]; o.skb = !!window.__SK().obj.userData.bouquet; return o; }"""
CLK = os.environ.get('CLK', '.42')
HEAD = """const P = window.__pulau; window.__gone = 0; window.__fix44(); window.__clock = """ + CLK + """; window.__cheer = null; P.player.obj.visible = false; """
# Sekar close at the table holding the bouquet (keeper hidden, camera from the west-north-west)
def sekar(arms, dist=2.2):
    return """() => { """ + HEAD + """ const k = window.__PM(), n = window.__SK(), x = n.x, z = n.z, y0 = P.surfaceY(x, z), Y = +(window.__Ys || -1.25);
  window.__look(x, z, Y, .08, """ + str(dist) + """, false);
  window.__beforeRender = (dt, T) => { k.obj.visible = false; window.__HEART.visible = false; n.obj.rotation.y = -1.3; const u = n.obj.userData; if (u.body) { u.body.rotation.y = 0; u.body.rotation.x = .05; u.body.rotation.z = 0; }
    if (u.armR) { u.armR.rotation.x = -1.15; u.armR.rotation.z = -.18; } if (u.armL) { u.armL.rotation.x = -1.15; u.armL.rotation.z = .18; }
    """ + arms + """
    window.__C(x - .05, y0 + 1.1, z); P.cam.dist = Math.max(""" + str(dist - .3) + """, """ + str(dist) + """ - T * .1); P.cam.yaw = Y; P.cam.pitch = .08; window.__clr([n], x, z, .4); }; }"""
# c1 cold open (and c9 payoff): 'Bunga?! Buat... aku?!' hugging the bouquet, a happy hop at the end
C1 = sekar("""n.obj.position.y = y0 + (T > 1.6 && T < 2.0 ? Math.sin((T - 1.6) / .4 * Math.PI) * .07 : 0); if (u.body) u.body.rotation.y = Math.sin(T * 2.2) * .12;""")
# c11 'Pak... ikannya jadi gosong.' looks down, embarrassed
C11 = sekar("""if (u.body) u.body.rotation.x = .2;""")
# c14 'Ikanku... mana?!' looks left and right, bouncing
C14 = sekar("""window.__fishBack(false); n.obj.rotation.y = -1.3 + Math.sin(T * 5) * .5; n.obj.position.y = y0 + Math.abs(Math.sin(T * 7)) * .06;""", 2.4)
# c2 premise: aerial over the island gliding south to the beach table (ep43 c2)
C2 = E43.C2.replace('window.__fix43()', 'window.__gone = 0; window.__fix44()')
# c3 the flower-shop counter in the mall: the bouquet is gone, the tag says 'SUDAH DIAMBIL / terima kasih, P.M.'
C3 = E43.C13.replace('window.__fix43()', 'window.__gone = 0; window.__fix44()').replace('v.x + .22', 'v.x + +(window.__X3 || .45)')
# c4 the keeper outside the mall, the bouquet hidden behind his back: 'Hari ini. Harus hari ini.'
C4 = """() => { """ + HEAD + """ const k = window.__PM(), x = 15.3, z = 23.4, y0 = P.surfaceY(x, z); window.__giveKB(false);
  window.__look(x, z, 3.14, .08, 2.0, false);
  window.__beforeRender = (dt, T) => { k.obj.position.set(x, y0, z); k.x = x; k.z = z; k.obj.rotation.y = 3.14 - .25; const u = k.obj.userData;
    if (u.body) { u.body.rotation.y = Math.sin(T * 9) * .03; u.body.rotation.x = .08; } if (u.armR) { u.armR.rotation.x = .55; u.armR.rotation.z = -.12; } if (u.armL) { u.armL.rotation.x = .55; u.armL.rotation.z = .12; }
    window.__C(x, y0 + 1.15, z); P.cam.dist = Math.max(1.7, 2.0 - T * .1); P.cam.yaw = 3.14; P.cam.pitch = .08; window.__clr([k], x, z, .5); }; }"""
# c5 -VANZwlee on the beach, anime pose... then the stumble on 'aduh!'
C5 = """() => { """ + HEAD + """ const n = window.__VA(), x = n.x, z = n.z, y0 = P.surfaceY(x, z), Y = +(window.__Y5 || -.3), TT = +(window.__TT5 || 2.85);
  window.__look(x, z, Y, .1, 2.1, false);
  window.__beforeRender = (dt, T) => { n.obj.rotation.y = Y; const u = n.obj.userData;
    if (T < TT) { u.armL.rotation.x = -.15; u.armR.rotation.x = -2.45; u.armL.rotation.z = 0; u.armR.rotation.z = -.55; u.body.rotation.y = .25; u.body.rotation.x = 0; n.obj.position.y = y0; }
    else { const q = Math.min(1, (T - TT) / .3); u.armL.rotation.x = -2.6; u.armR.rotation.x = -2.6; u.armL.rotation.z = .5; u.armR.rotation.z = -.5; u.body.rotation.y = 0; u.body.rotation.x = .45 * q; n.obj.position.y = y0 - .08 * q; }
    window.__C(x, y0 + 1.1, z); P.cam.dist = Math.max(1.8, 2.1 - T * .08); P.cam.yaw = Y; P.cam.pitch = .1; window.__clr([n], x, z, .5); }; }"""
# c6 ALERXMNC near the lighthouse, very still, slowly turning to the camera: 'Aku sudah di sini dari tadi.'
C6 = """() => { """ + HEAD + """ const n = window.__AL(), x = n.x, z = n.z, y0 = P.surfaceY(x, z), Y = +(window.__Y6 || 2.6);
  window.__look(x, z, Y, .1, 2.0, false);
  window.__beforeRender = (dt, T) => { n.obj.rotation.y = Y + (T < 2.2 ? .9 : .9 * Math.max(0, 1 - (T - 2.2) / .5)); const u = n.obj.userData; u.armL.rotation.x = 0; u.armR.rotation.x = 0;
    window.__C(x, y0 + 1.15, z); P.cam.dist = Math.max(1.5, 2.0 - T * .12); P.cam.yaw = Y; P.cam.pitch = .1; window.__clr([n], x, z, .5); }; }"""
# c7 crane down onto the Meja Dua Ikan, both at the table, the keeper hiding the bouquet behind his back
C7 = E43.C7.replace('window.__fix43()', 'window.__gone = 0; window.__fix44(); window.__giveKB(false); window.__SK().obj.userData.bouquet.visible = false')
# keeper close at the table (Sekar hidden; camera from the east-south-east)
def keeper(body, kb=None):
    return """() => { """ + HEAD + """ const k = window.__PM(), n = window.__SK(), x = k.x, z = k.z, y0 = P.surfaceY(x, z), Y = +(window.__Yk || 1.15); """ + ('' if kb is None else 'window.__giveKB(' + kb + ');') + """
  window.__look(x, z, Y, .08, 2.4, false);
  window.__beforeRender = (dt, T) => { n.obj.visible = false; window.__HEART.visible = false; k.obj.rotation.y = 1.2; const u = k.obj.userData, b = u.body;
    """ + body + """
    window.__C(x + .05, y0 + 1.2, z); P.cam.dist = Math.max(2.1, 2.4 - T * .1); P.cam.yaw = Y; P.cam.pitch = .08; window.__clr([k], x, z, .5); }; }"""
# c8 'Mbak Sekar. Aku menjaga lampu tiap malam. Ini... buat yang menjaga apinya.' bouquet behind the back, then held out on 'Ini...'
C8 = keeper("""const out = T > +(window.__T8 || 2.6); if (out && window.__kb && window.__kb.position.z < 0) window.__giveKB(true); if (!out && window.__kb && window.__kb.position.z > 0) window.__giveKB(false);
    if (u.armR) { u.armR.rotation.x = out ? -1.25 : .55; u.armR.rotation.z = out ? -.15 : -.12; } if (u.armL) { u.armL.rotation.x = out ? -1.25 : .55; u.armL.rotation.z = out ? .15 : .12; } if (b) b.rotation.x = out ? .12 : .02;""", 'false')
# c10 'Maaf lama. Tiga hari aku... latihan ngomong.' scratching his head
C10 = keeper("""if (u.armR) u.armR.rotation.x = -2.7 + Math.sin(T * 10) * .12; if (b) b.rotation.x = T < 1.5 ? .15 : 0;""")
# c12 wide two-shot at the table from the south: 'Tidak apa. Yang gosong... juga kumakan.'
C12 = """() => { """ + HEAD + """ const k = window.__PM(), n = window.__SK();
  window.__look(2, 38, .6, .3, 3.8, false);
  window.__beforeRender = (dt, T) => { window.__HEART.visible = false; k.obj.rotation.y = 1.57; n.obj.rotation.y = -1.57; const u = n.obj.userData; if (u.armR) u.armR.rotation.x = -1.15; if (u.armL) u.armL.rotation.x = -1.15;
    window.__C(2, P.surfaceY(2, 38) + 1.0, 38); P.cam.dist = Math.max(3.2, 3.8 - T * .15); P.cam.yaw = .6; P.cam.pitch = .3; window.__clr([k, n], 2, 38, .8); }; }"""
# c13 close on the table from above: one plate holds only a fish bone
C13 = """() => { """ + HEAD + """ window.__gone = 1; window.__fishBack(false); const k = window.__PM(), n = window.__SK(), y = P.surfaceY(2, 38) + .8;
  window.__look(2.0, 38.05, .3, 1.15, 1.7, false);
  window.__beforeRender = (dt, T) => { k.obj.visible = false; n.obj.visible = false; window.__HEART.visible = false;
    window.__C(2.05, y, 38.05); P.cam.dist = Math.max(1.2, 1.7 - T * .12); P.cam.yaw = .3; P.cam.pitch = 1.15; window.__clr([], 2, 38, .5); }; }"""
# c15 the paw prints on the sand, the camera glides along them toward the harbour
C15 = """() => { """ + HEAD + """ window.__gone = 1; window.__fishBack(false);
  window.__look(3, 37.5, 2.6, .85, 2.0, false);
  window.__beforeRender = (dt, T) => { window.__HEART.visible = false; const q = Math.min(1, T / 4.5), e = q * q * (3 - 2 * q), x = 3 + 3.4 * e, z = 37.5 - .2 * e;
    window.__C(x, P.surfaceY(x, z) + .1, z); P.cam.dist = 2.0 + .4 * e; P.cam.yaw = 2.6 - .3 * e; P.cam.pitch = .85 - .15 * e; window.__clr([], x, z, .5); }; }"""
# c16 end: both at the table, lantern on; crane up over the beach and the harbour (ep43 c14)
C16 = E43.C14.replace('window.__fix43()', 'window.__gone = 1; window.__fix44()')
SHOTS = {'c1': (C1, 90), 'c2': (C2, 180), 'c3': (C3, 170), 'c4': (C4, 125), 'c5': (C5, 120), 'c6': (C6, 140), 'c7': (C7, 75),
         'c8': (C8, 170), 'c9': (C1, 90), 'c10': (C10, 120), 'c11': (C11, 60), 'c12': (C12, 120), 'c13': (C13, 135), 'c14': (C14, 60),
         'c15': (C15, 125), 'c16': (C16, 135)}
CLEAR = E43.CLEAR[:-1] + " if (window.__giveKB) window.__giveKB(null); }"
async def run(which):
    async with async_playwright() as p:
        b, pg = await setup(p)
        for js in CHAIN + (SETUP44,): await pg.evaluate(js)
        if os.environ.get('VARS'): await pg.evaluate('() => { ' + os.environ['VARS'] + ' }')
        if 'pos' in which: print(await pg.evaluate(POS))
        for k, (js, n) in SHOTS.items():
            if k in which and 'prev' not in which:
                await shoot(pg, 'e44' + k, int(os.environ.get('N_' + k, n)), start_js=js, warm=12)
                await pg.evaluate(CLEAR)
        if 'prev' in which:
            for k, (js, n) in SHOTS.items():
                if 'all' not in which and k not in which: continue
                for w in os.environ.get('WARMS', os.environ.get('WARM', '40')).split('/'):
                    await shoot(pg, 'p44' + k + ('' if '/' not in os.environ.get('WARMS', '') else '_' + w), 1, start_js=js, warm=int(w))
                    await pg.evaluate(CLEAR)
        await b.close()
if __name__ == "__main__": asyncio.run(run(sys.argv[1].split(",")))
