"""Episode 42 "Surat Dibalas" shot list (format CERITA, run sore 17 Nov).  usage: DPR=2 python3 shots.py c1,c3,...  (DPR=1 + prev for checks)
No new TikTok comments (Apify failed again, Chrome not connected), so the episode moves the ASMARA subplot to clue #3: the Penjaga Mercusuar
goes down to the Ikan Bakar stall for the first time (storyCast spot 55,89 +0,+.7 on the main street, facing the counter, pose keeper),
orders 'yang paling matang', the heart smoke rises again, and he leaves a signed reply on a post beside the stall
(suratmercusuar x56 y91 r1, name 'Surat Balasan', b.lines/b.from 'P.M.'). Cameos: RANUUGLL (Polisi Pantai, 68,91) and whoyss (iseng, 50,42).
World: keeper (-.5,34.2) facing east; reply post (.5,35.5) board facing west; Sekar (1.35,34.8); stall centre (1,34).
"""
import asyncio, sys, os, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'lib'))
from harness import *
def _mod(name, path):
    sp = importlib.util.spec_from_file_location(name, path); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m
E41 = _mod('ep41shots', os.path.join(HERE, '..', 'ep41', 'shots.py'))
CHAIN = E41.CHAIN + (E41.SETUP41,)
SETUP42 = """() => { const P = window.__pulau; let rp = null, lp = null;
  P.scene.traverse(o => { if (o.userData && o.userData.b && o.userData.b.type === 'suratmercusuar') { if (o.userData.b.ep === 42) rp = o; else lp = o; } });
  window.__RP = rp; window.__POST = lp;
  const F = s => P.npcs.find(n => n.name === s || (n.name || '').startsWith(s));
  window.__RA = () => F('RANUUGLL'); window.__WH = () => F('whoyss');
  window.__fix42 = () => { window.__fix41();
    for (const f of [window.__RA, window.__WH]) { const n = f(); if (!n) continue; n.obj.visible = true; const c = n.castSpot; if (c && n.spot && Math.hypot(n.spot.x - c.x, n.spot.z - c.z) > .3) n.spot = Object.assign({}, n.spot, c); if (c && Math.hypot(n.x - c.x, n.z - c.z) > .3) { n.x = c.x; n.z = c.z; n.tx = null; n.tz = null; n.moving = false; n.state = 'work'; n.obj.position.set(c.x, P.surfaceY(c.x, c.z), c.z); n.obj.rotation.y = c.face; } } };
}"""
POS = """() => { const o = {}; for (const [k, f] of Object.entries({ pm: window.__PM, sk: window.__SK, ra: window.__RA, wh: window.__WH })) { const n = f(); o[k] = n ? [n.name, +n.x.toFixed(2), +n.z.toFixed(2), +n.obj.position.y.toFixed(2), +n.obj.rotation.y.toFixed(2)] : null; }
  const p = window.__RP; o.reply = [p.position.x, p.position.y, p.position.z, p.rotation.y]; const q = window.__POST; o.post = [q.position.x, q.position.y, q.position.z]; return o; }"""
HEAD = """const P = window.__pulau; window.__fix42(); window.__clock = .42; window.__cheer = null; P.player.obj.visible = false; """
# c1 cold open: Mbak Sekar turns from the grill to the new letter on the post beside her stall, startled ('Surat... buat aku?!')
C1 = """() => { """ + HEAD + """ const n = window.__SK(), x = n.x, z = n.z, y0 = P.surfaceY(x, z);
  window.__look(x, z, -1.3, .08, 1.9, false);
  window.__beforeRender = (dt, T) => { window.__HEART.visible = false; window.__heartAt(-1); const u = n.obj.userData; n.obj.rotation.y = -1.0;
    if (u.body) { u.body.rotation.y = 0; u.body.rotation.x = .05; } if (u.armR) u.armR.rotation.x = T < .5 ? -1.3 + Math.sin(T * 12) * .45 : -1.9; if (u.armL) u.armL.rotation.x = T < .5 ? -.6 : -1.9;
    n.obj.position.y = y0 + (T > .5 && T < .8 ? Math.sin((T - .5) / .3 * Math.PI) * .05 : 0);
    window.__C(x - .05, y0 + 1.15, z); P.cam.dist = Math.max(1.6, 1.9 - T * .15); P.cam.yaw = -1.3; P.cam.pitch = .08; window.__clr([n], x, z, .4); }; }"""
# c2 premise: aerial over the island gliding south to the beach stall
C2 = """() => { """ + HEAD + """
  window.__look(8, 8, -2.6, 1.08, 44, false);
  window.__beforeRender = (dt, T) => { const k = Math.min(1, Math.max(0, T) / 5.0), e = k * k * (3 - 2 * k); window.__C(8 - 7 * e, 1 + .6 * e, 8 + 26 * e); P.cam.dist = 44 - 34 * e; P.cam.pitch = 1.08 - .58 * e; P.cam.yaw = -2.6 + 1.2 * e; }; }"""
# c3 yesterday's unsigned letter on the post at the lighthouse door (keeper gone), slow push onto the smudge
C3 = """() => { """ + HEAD + """ const p = window.__POST, y = p.position.y;
  window.__look(26.5, -3.5, -1.57, .05, 2.6, false);
  window.__beforeRender = (dt, T) => { const k = Math.min(1, T / 4.5), e = k * k * (3 - 2 * k); window.__C(p.position.x - .05, y + 1.1 - .08 * e, p.position.z); P.cam.dist = 2.6 - 1.4 * e; P.cam.yaw = -1.57 - .25 + .25 * e; P.cam.pitch = .05; }; }"""
# c4 RANUUGLL the beach police, pointing: 'Polisi pantai turun tangan!'
C4 = """() => { """ + HEAD + """ const n = window.__RA(), x = n.x, z = n.z, y0 = P.surfaceY(x, z);
  window.__look(x, z, .3, .08, 2.0, false);
  window.__beforeRender = (dt, T) => { n.obj.rotation.y = .3; window.__C(x, y0 + 1.15, z); P.cam.dist = Math.max(1.7, 2.0 - T * .12); P.cam.yaw = .3 + .15; P.cam.pitch = .08; window.__clr([n], x, z, 1.2); }; }"""
# c5 whoyss peeks from the bush: 'Bukan aku! Aku mainnya sandal... eh.'
C5 = """() => { """ + HEAD + """ const n = window.__WH(), x = n.x, z = n.z, y0 = P.surfaceY(x, z);
  if (!window.__hid42) { window.__hid42 = 1; const sc = P.roads.parent, pts = []; for (let dx = -1.2; dx <= 1.2; dx += .6) for (let dz = -1.0; dz <= 2.6; dz += .6) pts.push([x + dx, z + dz]);
    sc.traverse(o => { if (!o.isInstancedMesh) return; const m = new (o.matrix.constructor)(), v = new (P.cam.target.constructor)(); const c = o.material && o.material.color ? o.material.color.getHexString() : ''; if (c === '5a9e44') return;
      for (let i = 0; i < o.count; i++) { o.getMatrixAt(i, m); v.setFromMatrixPosition(m); if (pts.some(([a, b]) => Math.hypot(v.x - a, v.z - b) < .7)) { const z0 = m.clone().scale(new (P.cam.target.constructor)(0, 0, 0)); o.setMatrixAt(i, z0); o.instanceMatrix.needsUpdate = true; } } }); }
  window.__look(x, z, 0, .1, 2.0, false);
  window.__beforeRender = (dt, T) => { n.obj.rotation.y = T < 2.2 ? 0 : -.9; window.__C(x - .18, y0 + 1.0, z); P.cam.dist = Math.max(1.6, 2.0 - T * .12); P.cam.yaw = .25; P.cam.pitch = .1; window.__clr([n], x, z, .5); }; }"""
# c6 wide: the stall from the street, the keeper standing at the counter for the first time; push in
C6 = """() => { """ + HEAD + """ window.__RP.visible = false; const k = window.__PM();
  window.__look(.3, 34.3, -1.0, .28, 5.6, false);
  window.__beforeRender = (dt, T) => { window.__C(.4, 1.3, 34.3); P.cam.dist = 5.6 - T * .4; P.cam.yaw = -1.0 - T * .05; P.cam.pitch = .28; window.__clr([k], .3, 34.3, .5); }; }"""
# c7 keeper close (3/4 from the south-east): 'Satu ikan bakar. Yang... paling matang.'
C7 = """() => { """ + HEAD + """ window.__RP.visible = false; const k = window.__PM(), x = k.x, z = k.z, y0 = P.surfaceY(x, z), Y = +(window.__Y7 || 0);
  window.__look(x, z, Y, .08, 1.9, false);
  window.__beforeRender = (dt, T) => { k.obj.rotation.y = T < 1.2 ? 1.0 : .7; const b = k.obj.userData.body; if (b) b.rotation.x = T > 1.4 ? .12 : 0;
    window.__C(x + .1, y0 + 1.3, z); P.cam.dist = Math.max(1.6, 1.9 - T * .1); P.cam.yaw = Y; P.cam.pitch = .08; window.__clr([k], x, z, .5); }; }"""
# c8 Mbak Sekar fanning like mad: 'S-siap, Pak! Paling matang! Paling... panas!'
C8 = """() => { """ + HEAD + """ window.__RP.visible = false; const n = window.__SK(), x = n.x, z = n.z, y0 = P.surfaceY(x, z);
  const Y8 = +(window.__Y8 || -1.3); window.__look(x, z, Y8, .08, 1.9, false);
  window.__beforeRender = (dt, T) => { window.__HEART.visible = false; window.__heartAt(-1); const u = n.obj.userData; n.obj.rotation.y = -1.0;
    if (u.body) { u.body.rotation.y = 0; u.body.rotation.x = .05; } if (u.armR) u.armR.rotation.x = -1.3 + Math.sin(T * (T > 1.5 ? 24 : 12)) * .45; if (u.armL) u.armL.rotation.x = -.6;
    n.obj.position.y = y0 + (T > 1.5 ? Math.abs(Math.sin(T * 9)) * .03 : 0);
    window.__C(x - .05, y0 + 1.15, z); P.cam.dist = Math.max(1.5, 1.9 - T * .12); P.cam.yaw = Y8; P.cam.pitch = .08; window.__clr([n], x, z, .4); }; }"""
# c9 the heart smoke rises over the stall; the keeper (foreground) looks up at it
C9 = """() => { """ + HEAD + """ window.__RP.visible = false; const k = window.__PM();
  window.__look(1, 34, -1.57, .12, 4.0, false);
  window.__beforeRender = (dt, T) => { window.__HEART.visible = true; const c = Math.min(.95, .05 + T / 4.3); window.__heartAt(c); const hy = window.__ST.position.y + 1.75 + c * 1.5;
    k.obj.rotation.y = 1.57; const b = k.obj.userData.body; if (b) b.rotation.x = -.25;
    window.__C(.6, hy - .5, 34.1); P.cam.dist = 3.6 - T * .2; P.cam.yaw = -1.57 - .45; P.cam.pitch = .1; window.__clr([k], .6, 34.1, .5); }; }"""
# c10 'Dia pulang. Tapi di samping lapak, ada surat baru.': the street empty of the keeper, the reply post beside the stall
C10 = """() => { """ + HEAD + """ const k = window.__PM(); k.obj.visible = false; const p = window.__RP, y = p.position.y;
  window.__look(p.position.x, p.position.z, -1.3, .15, 3.6, false);
  window.__beforeRender = (dt, T) => { k.obj.visible = false; window.__C(p.position.x, y + 1.0, p.position.z); P.cam.dist = 3.6 - T * .35; P.cam.yaw = -1.3 - T * .04; P.cam.pitch = .15; window.__clr([], p.position.x, p.position.z, .5); }; }"""
# c11 the reply, readable: 'Lampunya akan tetap menyala. Ikannya enak. Besok... boleh dua? Dari: P.M.'
C11 = """() => { """ + HEAD + """ const k = window.__PM(); k.obj.visible = false; const p = window.__RP, y = p.position.y;
  window.__look(p.position.x, p.position.z, -1.57, .02, 1.75, false);
  window.__beforeRender = (dt, T) => { k.obj.visible = false; const q = Math.min(1, T / 5), e = q * q * (3 - 2 * q); window.__C(p.position.x - .05, y + 1.1 - .06 * e, p.position.z + .03 * e); P.cam.dist = 1.75 - .35 * e; P.cam.yaw = -1.57; P.cam.pitch = .02; }; }"""
# c12 Sekar reads it, hops with joy: 'Dua?! Besok aku bakar dua...'
C12 = """() => { """ + HEAD + """ const k = window.__PM(); k.obj.visible = false; const n = window.__SK(), x = n.x, z = n.z, y0 = P.surfaceY(x, z), Y = +(window.__Y12 || -1.3);
  window.__look(x, z, Y, .1, 2.1, false);
  window.__beforeRender = (dt, T) => { k.obj.visible = false; window.__HEART.visible = false; window.__heartAt(-1); n.obj.rotation.y = -1.0; const u = n.obj.userData;
    if (u.armR) u.armR.rotation.x = T > 1.0 ? -2.6 : -1.9; if (u.armL) u.armL.rotation.x = T > 1.0 ? -2.6 : -1.9; if (u.body) u.body.rotation.x = 0;
    n.obj.position.y = y0 + (T > 1.0 ? Math.abs(Math.sin((T - 1.0) * 6)) * .12 : 0);
    window.__C(x - .05, y0 + 1.15, z); P.cam.dist = Math.max(1.9, 2.1 - T * .06); P.cam.yaw = Y; P.cam.pitch = .1; window.__clr([n], x, z, .45); }; }"""
# c13 RANUUGLL closes the case with a salute: 'Ini bukan kasus kriminal. Ini... kasus hati.'
C13 = """() => { """ + HEAD + """ const n = window.__RA(), x = n.x, z = n.z, y0 = P.surfaceY(x, z);
  const Y13 = +(window.__Y13 || .9); window.__look(x, z, Y13, .1, 1.7, false);
  window.__beforeRender = (dt, T) => { n.obj.rotation.y = Y13 - .15; const u = n.obj.userData; if (u.armR && T > 1.6) { u.armR.rotation.x = -2.5; u.armR.rotation.z = -.5; }
    window.__C(x, y0 + 1.25, z); P.cam.dist = Math.max(1.45, 1.7 - T * .08); P.cam.yaw = Y13; P.cam.pitch = .1; window.__clr([n], x, z, .5); }; }"""
# c14 end: the keeper back at the counter with the heart smoke; crane up over the stall toward the lighthouse across the bay
C14 = """() => { """ + HEAD + """ const k = window.__PM();
  window.__look(.4, 34.2, -1.2, .2, 3.2, false);
  window.__beforeRender = (dt, T) => { window.__HEART.visible = true; window.__heartAt(.55 + .3 * Math.sin(T * .4)); const q = Math.min(1, Math.max(0, T - .8) / 8), e = q * q * (3 - 2 * q);
    window.__C(.5, 1.4 + 3.5 * e, 34.2 - 3 * e); P.cam.dist = 3.2 + 10 * e; P.cam.yaw = -1.2 + 1.0 * e; P.cam.pitch = .2 + .5 * e; window.__clr([k], .4, 34.2, .5); }; }"""
SHOTS = {'c1': (C1, 85), 'c2': (C2, 170), 'c3': (C3, 170), 'c4': (C4, 130), 'c5': (C5, 105), 'c6': (C6, 150), 'c7': (C7, 110),
         'c8': (C8, 120), 'c9': (C9, 130), 'c10': (C10, 110), 'c11': (C11, 150), 'c12': (C12, 130), 'c13': (C13, 120), 'c14': (C14, 330)}
CLEAR = E41.CLEAR[:-1] + " if (window.__RP) window.__RP.visible = true; const k = window.__PM && window.__PM(); if (k) k.obj.visible = true; }"
async def run(which):
    async with async_playwright() as p:
        b, pg = await setup(p)
        for js in CHAIN + (SETUP42,): await pg.evaluate(js)
        if os.environ.get('VARS'): await pg.evaluate('() => { ' + os.environ['VARS'] + ' }')
        if 'pos' in which: print(await pg.evaluate(POS))
        for k, (js, n) in SHOTS.items():
            if k in which and 'prev' not in which:
                await shoot(pg, 'e42' + k, int(os.environ.get('N_' + k, n)), start_js=js, warm=12)
                await pg.evaluate(CLEAR)
        if 'prev' in which:
            for k, (js, n) in SHOTS.items():
                if 'all' not in which and k not in which: continue
                for w in os.environ.get('WARMS', os.environ.get('WARM', '40')).split('/'):
                    await shoot(pg, 'p42' + k + ('' if '/' not in os.environ.get('WARMS', '') else '_' + w), 1, start_js=js, warm=int(w))
                    await pg.evaluate(CLEAR)
        await b.close()
if __name__ == "__main__": asyncio.run(run(sys.argv[1].split(",")))
