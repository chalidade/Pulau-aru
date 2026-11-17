"""Episode 41 "Surat Tanpa Nama" shot list (format KONSEP, run pagi 17 Nov).  usage: DPR=2 python3 shots.py c1,c3,...  (DPR=1 + prev for checks)
No new TikTok comments (Apify failed again, Chrome not connected, komentar.md has no new usable comment), so the episode sells the premise
and moves the ASMARA subplot to clue #2. New in the game: Surat Tanpa Nama (suratmercusuar x82 y52 r1, a post beside the lighthouse door
with the unsigned letter, signature under a charcoal smudge), the Penjaga Mercusuar now stands at the lighthouse door reading it (pose
keepersurat), Mbak Sekar the fish-grill seller (storyCast, pose ikanbakar: fan + charcoal smudge on the cheek) behind the Ikan Bakar stall
(bakarikan x56 y89 r1, b.heart = heart-shaped smoke). Cameos: inyuu (gamer, by the night camera) and senar muliya (guitar, Rumah Pantai).
World: keeper (26.65,-2.0) facing west; letter post (26.5,-3.5) board facing west; seller (1.35,34.8) south of the grill, facing north (fans the coals); stall centre (1,34).
"""
import asyncio, sys, os, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'lib'))
from harness import *
def _mod(name, path):
    sp = importlib.util.spec_from_file_location(name, path); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m
E40 = _mod('ep40shots', os.path.join(HERE, '..', 'ep40', 'shots.py'))
CHAIN = E40.CHAIN + (E40.SETUP40,)
SETUP41 = """() => { const P = window.__pulau;
  let st = null, post = null; P.scene.traverse(o => { if (o.userData && o.userData.b) { if (o.userData.b.type === 'bakarikan') st = o; if (o.userData.b.type === 'suratmercusuar') post = o; } });
  window.__ST = st; window.__POST = post; window.__HEART = st.userData.heart;
  const F = s => P.npcs.find(n => n.name === s || (n.name || '').startsWith(s));
  window.__PM = () => F('Penjaga Mercusuar'); window.__SK = () => F('Mbak Sekar'); window.__IN = () => F('inyuu'); window.__SM = () => F('senar muliya');
  window.__heartAt = c => { const h = window.__HEART; st.userData.heart = null; h.position.y = 1.75 + c * 1.5; h.scale.setScalar(.8 + c * .8); h.rotation.y = 0; h.children.forEach(m => { m.material.opacity = .9 * (c < .12 ? c / .12 : 1 - Math.max(0, c - .75) / .25); }); };
  window.__fix41 = () => { window.__fix40(); st.userData.heart = window.__HEART;
    for (const f of [window.__PM, window.__SK, window.__IN, window.__SM]) { const n = f(); if (!n) continue; n.obj.visible = true; const c = n.castSpot; if (c && n.spot && Math.hypot(n.spot.x - c.x, n.spot.z - c.z) > .3) n.spot = Object.assign({}, n.spot, c); if (c && Math.hypot(n.x - c.x, n.z - c.z) > .3) { n.x = c.x; n.z = c.z; n.tx = null; n.tz = null; n.moving = false; n.state = 'work'; n.obj.position.set(c.x, P.surfaceY(c.x, c.z), c.z); n.obj.rotation.y = c.face; } } };
}"""
POS = """() => { const o = {}; for (const [k, f] of Object.entries({ pm: window.__PM, sk: window.__SK, in: window.__IN, sm: window.__SM })) { const n = f(); o[k] = n ? [n.name, +n.x.toFixed(2), +n.z.toFixed(2), +n.obj.position.y.toFixed(2), +n.obj.rotation.y.toFixed(2)] : null; }
  const p = window.__POST, s = window.__ST; o.post = [p.position.x, p.position.y, p.position.z, p.rotation.y]; o.stall = [s.position.x, s.position.y, s.position.z, s.rotation.y]; return o; }"""
HEAD = """const P = window.__pulau; window.__fix41(); window.__clock = .42; window.__cheer = null; """
# c1 cold open: the keeper at the lighthouse door, letter in both hands, looks up startled ('Surat... untukku?!')
C1 = """() => { """ + HEAD + """ P.player.obj.visible = false; const k = window.__PM(), x = k.x, z = k.z, y0 = P.surfaceY(x, z);
  window.__look(x, z, -1.3, .06, 1.9, false);
  window.__beforeRender = (dt, T) => { k.obj.rotation.y = -1.45; const b = k.obj.userData.body; if (T > .55) { b.rotation.x = -.08; b.position.y = T < .9 ? Math.sin((T - .55) / .35 * Math.PI) * .06 : 0; }
    window.__C(x - .05, y0 + 1.12, z + .05); P.cam.dist = Math.max(1.55, 1.9 - T * .2); P.cam.yaw = -1.3; P.cam.pitch = .06; window.__clr([k], x, z, .5); }; }"""
# c2 premise: aerial over the island gliding east to the lighthouse
C2 = """() => { """ + HEAD + """ P.player.obj.visible = false;
  window.__look(8, 8, -2.0, 1.08, 62, false);
  window.__beforeRender = (dt, T) => { const k = Math.min(1, Math.max(0, T) / 5.0), e = k * k * (3 - 2 * k); window.__C(8 + 18.5 * e, 1 + 1.5 * e, 8 - 10.5 * e); P.cam.dist = 62 - 50 * e; P.cam.pitch = 1.08 - .62 * e; P.cam.yaw = -2.0 + .55 * e; }; }"""
# c3 'Pagi ini, di pintu mercusuar, ada surat tanpa nama': the door, the post with the letter, the keeper reading; slow push-in
C3 = """() => { """ + HEAD + """ P.player.obj.visible = false; const k = window.__PM();
  window.__look(26.6, -2.7, -1.57, .22, 5.2, false);
  window.__beforeRender = (dt, T) => { window.__C(26.6, 1.3, -2.75); P.cam.dist = 5.2 - T * .35; P.cam.yaw = -1.57 - .15 + T * .04; P.cam.pitch = .22; window.__clr([k], 26.6, -2.7, .6); }; }"""
# c4 the letter text, close (readable): 'Lampumu yang menuntunku pulang, setiap malam.'
C4 = """() => { """ + HEAD + """ P.player.obj.visible = false; const p = window.__POST, y = p.position.y;
  window.__look(26.5, -3.5, -1.57, .02, 1.75, false);
  window.__beforeRender = (dt, T) => { window.__C(p.position.x - .05, y + 1.12, p.position.z); P.cam.dist = Math.max(1.55, 1.75 - T * .05); P.cam.yaw = -1.57; P.cam.pitch = .02; }; }"""
# c5 push-in onto the signature hidden under the charcoal smudge
C5 = """() => { """ + HEAD + """ P.player.obj.visible = false; const p = window.__POST, y = p.position.y;
  window.__look(26.5, -3.5, -1.57, .02, 1.1, false);
  window.__beforeRender = (dt, T) => { const k = Math.min(1, T / 3.5), e = k * k * (3 - 2 * k); window.__C(p.position.x - .05, y + 1.05 - .1 * e, p.position.z + .02 * e); P.cam.dist = 1.3 - .6 * e; P.cam.yaw = -1.57 + .08 * Math.sin(T * 1.3); P.cam.pitch = .02; }; }"""
# c6 two-shot: Aru (south of the keeper) teasing 'Ciee! Dari siapa, Pak?' / keeper looks away 'Ini pasti... salah alamat.'
C6 = """() => { """ + HEAD + """ const k = window.__PM(), ax = k.x - .1, az = k.z + .85, mx = (ax + k.x) / 2, mz = (az + k.z) / 2;
  window.__look(ax, az, -1.57, .1, 3.2, true);
  window.__beforeRender = (dt, T) => { window.__aruS(ax, az, Math.PI - .3, T < 1.35, T); const u = P.player.obj.userData; if (T < 1.35 && u.armR) u.armR.rotation.x = -1.8 + Math.sin(T * 12) * .3;
    k.obj.rotation.y = T < 1.4 ? -.4 : -2.4; window.__C(mx, P.surfaceY(mx, mz) + 1.0, mz); P.cam.dist = Math.max(2.9, 3.2 - T * .08); P.cam.yaw = -1.57; P.cam.pitch = .1; window.__clr([k], mx, mz, .6); }; }"""
# c7 Aru close, pointing up at the lighthouse: 'Pak, mercusuar di pulau ini cuma satu!'
C7 = """() => { """ + HEAD + """ const k = window.__PM(), ax = k.x - .1, az = k.z + .85;
  window.__look(ax, az, -1.2, .12, 1.9, true);
  window.__beforeRender = (dt, T) => { window.__aruS(ax, az, -1.2, true, T); const u = P.player.obj.userData; if (u.armR) { u.armR.rotation.x = -2.8; u.armR.rotation.z = .3; }
    window.__C(ax, P.surfaceY(ax, az) + 1.1, az); P.cam.dist = Math.max(1.6, 1.9 - T * .1); P.cam.yaw = -1.2; P.cam.pitch = .12; window.__clr([], ax, az, .5); }; }"""
# c8 inyuu (gamer) at the night camera, game pad up: 'Quest baru! Cari NPC yang bau arang!'
C8 = """() => { """ + HEAD + """ P.player.obj.visible = false; const n = window.__IN(), x = n.x, z = n.z, y0 = P.surfaceY(x, z);
  window.__look(x, z, 1.57, .08, 2.1, false);
  window.__beforeRender = (dt, T) => { n.obj.rotation.y = 1.57; if (T > .2 && T < .6) n.obj.position.y = y0 + Math.sin((T - .2) / .4 * Math.PI) * .15; else n.obj.position.y = y0;
    window.__C(x, y0 + 1.1, z); P.cam.dist = Math.max(1.7, 2.1 - T * .12); P.cam.yaw = 1.57 + .2; P.cam.pitch = .08; window.__clr([n], x, z, .5); }; }"""
# c9 senar muliya plays a love song for the keeper... the string snaps (T ~2.4: a jolt)
C9 = """() => { """ + HEAD + """ P.player.obj.visible = false; const n = window.__SM(), x = n.x, z = n.z, y0 = P.surfaceY(x, z);
  window.__look(x, z, 0, .08, 2.1, false);
  window.__beforeRender = (dt, T) => { n.obj.rotation.y = 0; const b = n.obj.userData.body; b.rotation.x = T > 2.3 && T < 2.7 ? -.25 : 0;
    window.__C(x, y0 + 1.0, z); P.cam.dist = T < 2.3 ? Math.max(1.8, 2.1 - T * .1) : 1.6; P.cam.yaw = -.3; P.cam.pitch = .08; window.__clr([n], x, z, .5); }; }"""
# c10 'cuma satu tempat yang asapnya nggak pernah padam': the Ikan Bakar stall by the pier, smoke rising; slow push
C10 = """() => { """ + HEAD + """ P.player.obj.visible = false;
  window.__look(1, 34, -1.57, .3, 6.5, false);
  window.__beforeRender = (dt, T) => { window.__heartAt(-1); window.__HEART.visible = false; window.__C(1.1, 1.6, 34); P.cam.dist = 6.5 - T * .4; P.cam.yaw = -1.57 - .35; P.cam.pitch = .3; window.__clr([], 1, 34, .6); }; }"""
# c11 Mbak Sekar fanning the coals, smudge on her cheek; at the end she looks dreamily toward the lighthouse
C11 = """() => { """ + HEAD + """ P.player.obj.visible = false; const n = window.__SK(), x = n.x, z = n.z, y0 = P.surfaceY(x, z);
  window.__look(x, z, -.9, .04, 1.5, false);
  window.__beforeRender = (dt, T) => { window.__HEART.visible = false; window.__heartAt(-1); n.obj.rotation.y = -2.3; if (T > 2.6) { n.obj.rotation.y = -2.3 + Math.min(1, (T - 2.6) / .5) * 1.5; }
    window.__C(x - .05, y0 + 1.05, z); P.cam.dist = Math.max(1.25, 1.5 - T * .07); P.cam.yaw = -.9; P.cam.pitch = .04; window.__clr([n], x, z, .4); }; }"""
# c12 'Asapnya... kok bentuk hati?': low angle on the stall roof, the heart-shaped smoke rises and swells
C12 = """() => { """ + HEAD + """ P.player.obj.visible = false;
  window.__look(1, 34, -1.57, .12, 4.0, false);
  window.__beforeRender = (dt, T) => { window.__HEART.visible = true; window.__heartAt(Math.min(.95, .05 + T / 4.3)); const hy = window.__ST.position.y + 1.75 + Math.min(.95, .05 + T / 4.3) * 1.5;
    window.__C(1.0, hy - .3, 34); P.cam.dist = 3.0 - T * .2; P.cam.yaw = -1.57 - .2; P.cam.pitch = .12; window.__clr([], 1, 34, .6); }; }"""
# c13 end: back at the lighthouse, the keeper reading the letter again; crane up past the lamp out over the sea
C13 = """() => { """ + HEAD + """ P.player.obj.visible = false; const k = window.__PM(), x = k.x, z = k.z, y0 = P.surfaceY(x, z);
  window.__look(x, z, -1.3, .1, 2.3, false);
  window.__beforeRender = (dt, T) => { const q = Math.min(1, Math.max(0, T - 1.0) / 7), e = q * q * (3 - 2 * q);
    window.__C(x + .3 * e, y0 + 1.1 + 4.5 * e, z); P.cam.dist = 2.3 + 9 * e; P.cam.yaw = -1.3 - .5 * e; P.cam.pitch = .1 + .55 * e; window.__clr([k], x, z, .5); }; }"""
SHOTS = {'c1': (C1, 85), 'c2': (C2, 160), 'c3': (C3, 135), 'c4': (C4, 125), 'c5': (C5, 150), 'c6': (C6, 140), 'c7': (C7, 90),
         'c8': (C8, 130), 'c9': (C9, 125), 'c10': (C10, 125), 'c11': (C11, 135), 'c12': (C12, 120), 'c13': (C13, 335)}
CLEAR = E40.CLEAR[:-1] + " if (window.__HEART) { window.__HEART.visible = true; } }"
async def run(which):
    async with async_playwright() as p:
        b, pg = await setup(p)
        for js in CHAIN + (SETUP41,): await pg.evaluate(js)
        if 'pos' in which: print(await pg.evaluate(POS))
        for k, (js, n) in SHOTS.items():
            if k in which and 'prev' not in which:
                await shoot(pg, 'e41' + k, int(os.environ.get('N_' + k, n)), start_js=js, warm=12)
                await pg.evaluate(CLEAR)
        if 'prev' in which:
            for k, (js, n) in SHOTS.items():
                if 'all' not in which and k not in which: continue
                for w in os.environ.get('WARMS', os.environ.get('WARM', '40')).split('/'):
                    await shoot(pg, 'p41' + k + ('' if '/' not in os.environ.get('WARMS', '') else '_' + w), 1, start_js=js, warm=int(w))
                    await pg.evaluate(CLEAR)
        await b.close()
if __name__ == "__main__": asyncio.run(run(sys.argv[1].split(",")))
