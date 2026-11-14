"""Episode 36 "Debat Calon Presiden" shot list (format CERITA).  usage: DPR=2 python3 shots.py c1,c3,...  (DPR=1 + prev for checks; 'pos' prints positions)
PEMILU KE-2, day 14 Nov: the president's term ends. Candidates from komentar.md (ep31 'AKU CALON' comments) stand on the Mimbar with
their promise placards (island.json event demo at 'mimbar', event.carry + event.join), Bu Guru Gina moderates, the audience holds
placards on the main street. Two picked comments: @xzxxxxx67 (Hafidz) 'tidak ada bullying tidak ada korupsi' -> spanduk PULAU TANPA
BULLYING (spanduk x52 y47 r3); @rizyanzet 'patung presiden pertama' -> construction site Patung Presiden Pertama (construct x60 y43).
Mejadaftar becomes the KOTAK SUARA (pendaftaran ditutup), Papan Pemilu lists the 9 candidates. Likes not counted yet (Apify down):
result next episode. Cast: Bu Guru Gina, ALIF HR & NOVA (Klub Warga Biasa), Etet_443. Reuses ep35's helper chain.
"""
import asyncio, sys, os, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'lib'))
from harness import *
def _mod(name, path):
    sp = importlib.util.spec_from_file_location(name, path); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m
E35 = _mod('ep35shots', os.path.join(HERE, '..', 'ep35', 'shots.py'))
E34 = E35.E34
CHAIN = (E35.BASE, "() => { " + E35.NPC + " }", "() => { " + E35.EXTRA + " }", "() => { " + E35.EP29 + " }", "() => { " + E35.EP31 + " }",
         "() => { " + E35.EP32 + " }", E35.SETUP33, E35.SETUP34, E35.SETUP35)
SETUP36 = """() => { const P = window.__pulau; window.__planeU = -1;
  window.__HF = () => P.npcs.find(n => n.cand === 'xzxxxxx67'); window.__RZ = () => P.npcs.find(n => n.cand === 'rizyanzet');
  window.__GINA = () => window.__N('Bu Guru Gina'); window.__ALIF = () => window.__N('ALIF HR'); window.__NOVA = () => window.__N('NOVA');
  window.__fix36 = () => { window.__fix35(); for (const f of [window.__K, window.__G]) { const n = f(); if (n) window.__fix(n); } };
  window.__dy = n => (n.demo && n.demo.dy) || 0;
  window.__SD = (n, x, z, face, pose, T) => window.__poseY(n, x, P.surfaceY(x, z) + window.__dy(n), z, face, pose, T);
  window.__hd = (n, h) => { const [x, z] = window.__dm(n); return [x, z, P.surfaceY(x, z) + (h || 1.2)]; }; }"""
POS = """() => { const P = window.__pulau, o = {}; for (const n of P.npcs) if (n.demo || n.pres || n.vp || n.cand || n.name === 'Penjaga Mercusuar') o[n.name] = [+n.obj.position.x.toFixed(2), +n.obj.position.z.toFixed(2), +n.obj.position.y.toFixed(2), n.demo ? 'demo' : (n.pres ? 'pres' : '')]; return o; }"""
# helper: close-up on a demo NPC at its own spot, talking for `talk` seconds, camera from yaw `yaw`
def close(fn, yaw, dist, pitch, talk, pose='talk', h=1.25, after='still', extra=''):
    return """() => { const P = window.__pulau, n = %s; window.__fix36(); window.__clock = .38; window.__cheer = null; P.player.obj.visible = false;
  const [x, z] = window.__dm(n); n.face0 = n.face0 == null ? n.obj.rotation.y : n.face0; window.__look(x, z, %s, %s, %s, false);
  window.__beforeRender = (dt, T) => { window.__z0(n); window.__SD(n, x, z, n.face0, T > .1 && T < %s ? '%s' : '%s', T); %s
    window.__C(x, P.surfaceY(x, z) + window.__dy(n) + %s, z); P.cam.dist = Math.max(%s * .82, %s - T * .12); P.cam.yaw = %s + T * .015; P.cam.pitch = %s; window.__clr([n], x, z, .55); }; }""" % (
        fn, yaw, pitch, dist, talk, pose, after, extra, h, dist, dist, yaw, pitch)
# c1 cold open: Hafidz on the stage with his placard: 'Kalau aku presiden: tidak ada bullying. Tidak ada KORUPSI!' (crowd cheers at the end)
C1 = close('window.__HF()', .12, 2.7, .1, 4.4, 'talk', 1.3, 'cheer', "window.__cheer = T > 3.3 ? 1 : null;")
# c2 the president (petahana EGA) behind the podium, panicking: 'Eh... lima koin kemarin... itu korupsi bukan?'
C2 = """() => { const P = window.__pulau, e = window.__PR(); window.__fix36(); window.__clock = .38; window.__cheer = null; P.player.obj.visible = false;
  const x = -.8, z = -10.45, y0 = P.surfaceY(x, z) + .55; window.__look(x, z, .3, .12, 2.3, false);
  window.__beforeRender = (dt, T) => { window.__z0(e); window.__poseY(e, x, y0, z, .3, T < 1.2 ? 'panic' : 'talk', T); e.obj.userData.body.rotation.z = Math.sin(T * 13) * .03; window.__VP().obj.visible = false;
    window.__C(x, y0 + 1.25, z); P.cam.dist = Math.max(1.9, 2.3 - T * .15); P.cam.yaw = .3; P.cam.pitch = .12; window.__clr([e], x, z, .55); window.__VP().obj.visible = false; }; }"""
# c3 premise + comment cards: aerial glide from the south of the main street down onto the debate (stage, candidates, audience)
C3 = """() => { const P = window.__pulau; window.__fix36(); window.__clock = .38; window.__cheer = true; P.player.obj.visible = false;
  window.__look(-1.5, 6, .15, 1.05, 46, false);
  window.__beforeRender = (dt, T) => { const k = Math.min(1, Math.max(0, T) / 6.6), e = k * k * (3 - 2 * k); window.__C(-1.5, .6 + .4 * e, 6 + (-10.3 - 6) * e); P.cam.dist = 46 - 37 * e; P.cam.pitch = 1.05 - .5 * e; P.cam.yaw = .15 - .1 * e; }; }"""
# c4 the Penjaga Mercusuar (ketua panitia) behind the desk that is now the KOTAK SUARA: 'Masa jabatan presiden habis hari ini.'
C4 = """() => { const P = window.__pulau, k = window.__K(); window.__fix36(); window.__clock = .38; window.__cheer = null; P.player.obj.visible = false;
  window.__look(2.75, -11.0, -1.85, .26, 3.0, false);
  window.__beforeRender = (dt, T) => { window.__z0(k); window.__S(k, 2.75, -11.0, -1.85, T > .1 && T < 2.8 ? 'talk' : 'still', T); window.__lant(k);
    window.__C(2.6, P.surfaceY(2.75, -11) + 1.45, -11.0); P.cam.dist = Math.max(2.5, 3.0 - T * .12); P.cam.yaw = -1.85; P.cam.pitch = .26; window.__clr([k], 2.6, -11.0, .8); }; }"""
# c5 Bu Guru Gina, moderator, at the front of the stage: 'Debat dimulai! Satu calon, satu janji. Jangan nyontek!'
C5 = close('window.__GINA()', .35, 2.6, .12, 4.0, 'point', 1.25)
# c6 the Papan Pemilu with the 9 candidates, slow push in ('Sembilan calon. Ada yang janji sejahtera... ada yang cuma bilang: aku calon.')
C6 = """() => { const P = window.__pulau; window.__fix36(); window.__clock = .38; window.__cheer = null; P.player.obj.visible = false;
  window.__look(2.5, -5, .1, .12, 6.2, false);
  window.__beforeRender = (dt, T) => { window.__C(2.5, P.surfaceY(2.5, -5.6) + 1.9, -5.6); P.cam.dist = Math.max(5.0, 6.2 - T * .2); P.cam.yaw = .1 - T * .03; P.cam.pitch = .12; window.__clr([], 2.5, -5.6, .9); }; }"""
# c7 the spanduk PULAU TANPA BULLYING (Hafidz's promise) by the main street, camera from the east drifting along it
C7 = """() => { const P = window.__pulau; window.__fix36(); window.__clock = .38; window.__cheer = true; P.player.obj.visible = false;
  const x = -3.4, z = -7.6; window.__look(x, z, 1.4, .25, 5.0, false);
  window.__beforeRender = (dt, T) => { window.__C(x, P.surfaceY(x, z) + 1.8, z); P.cam.dist = Math.max(3.6, 5.0 - T * .3); P.cam.yaw = 1.25 + T * .05; P.cam.pitch = .22; window.__clr([], x, z, .7); }; }"""
# c8 the construction site of the Patung Presiden Pertama (rizyanzet's promise), crane down onto the SEGERA DIBANGUN board
C8 = """() => { const P = window.__pulau; window.__fix36(); window.__clock = .38; window.__cheer = null; P.player.obj.visible = false;
  const x = 7.6, z = -11.3, sx = 8.15, sz = -10.85; window.__look(x, z, .35, .75, 6, false);
  window.__beforeRender = (dt, T) => { const k = Math.min(1, T / 3.0), e = k * k * (3 - 2 * k); window.__C(x + (sx - x) * e, P.surfaceY(x, z) + .9 + .3 * e, z + (sz - z) * e); P.cam.dist = 6.5 - 3.9 * e; P.cam.pitch = .8 - .22 * e; P.cam.yaw = .35; window.__clr([], x, z, .7); }; }"""
# c9 ex-president Etet in the audience, touched, then deflated: 'Patung... aku? Aku terharu.' / 'Kalau dia menang.' / '...Oh.'
C9 = """() => { const P = window.__pulau, t = window.__ET(); window.__fix36(); window.__clock = .38; window.__cheer = null; P.player.obj.visible = false;
  const [x, z] = window.__dm(t); window.__look(x, z, 3.0, .12, 2.6, false);
  window.__beforeRender = (dt, T) => { window.__z0(t); window.__S(t, x, z, 3.0, T > .1 && T < 2.7 ? 'talk' : (T > 4.2 ? 'panic' : 'still'), T); if (T > 4.3) t.obj.userData.body.rotation.x = .25;
    window.__C(x, P.surfaceY(x, z) + 1.45, z); P.cam.dist = Math.max(2.2, 2.6 - T * .08); P.cam.yaw = 3.0; P.cam.pitch = .12; window.__clr([t], x, z, .55); }; }"""
# c10 Klub Warga Biasa in the audience: ALIF 'Aku nggak nyalon. Aku warga biasa.' / NOVA 'Aku lebih biasa.'
C10 = """() => { const P = window.__pulau, a = window.__ALIF(), v = window.__NOVA(); window.__fix36(); window.__clock = .38; window.__cheer = null; P.player.obj.visible = false;
  const [ax, az] = window.__dm(a), [vx, vz] = window.__dm(v), x = (ax + vx) / 2, z = (az + vz) / 2; window.__look(x, z, 2.75, .12, 3.0, false);
  window.__beforeRender = (dt, T) => { window.__z0(a); window.__z0(v); window.__S(a, ax, az, 2.75 + .25, T > .1 && T < 2.9 ? 'talk' : 'still', T); window.__S(v, vx, vz, 2.75 - .25, T > 3.0 && T < 4.4 ? 'talk' : 'still', T);
    window.__C(x, P.surfaceY(x, z) + 1.2, z); P.cam.dist = Math.max(2.6, 3.0 - T * .08); P.cam.yaw = 2.75; P.cam.pitch = .12; window.__clr([a, v], x, z, .6); }; }"""
# c11 EGA at the podium, waving to the crowd, then sheepish: 'Pilih aku lagi! Lima koinnya... aku kembalikan. Besok.'
C11 = """() => { const P = window.__pulau, e = window.__PR(); window.__fix36(); window.__clock = .38; window.__cheer = null; P.player.obj.visible = false;
  const x = -.8, z = -10.45, y0 = P.surfaceY(x, z) + .55; window.__look(x, z, -.2, .16, 2.8, false);
  window.__beforeRender = (dt, T) => { window.__z0(e); window.__poseY(e, x, y0, z, -.1, T < 1.4 ? 'wave' : (T < 3.6 ? 'talk' : 'still'), T); window.__cheer = T < 1.5 ? 1 : null; window.__VP().obj.visible = false;
    window.__C(x, y0 + 1.2, z); P.cam.dist = Math.max(2.2, 2.8 - T * .18); P.cam.yaw = -.2 + T * .03; P.cam.pitch = .16; window.__clr([e], x, z, .55); window.__VP().obj.visible = false; }; }"""
# c12 end: Aru in front of the stage steps facing the camera ('Like kalian lagi dihitung. Hasilnya... episode berikutnya!'), then the camera rises over the debate
C12 = """() => { const P = window.__pulau; window.__fix36(); window.__clock = .4; window.__cheer = true;
  const x = -1.5, z = -8.0; window.__look(x, z, 0, .15, 2.8, true);
  window.__beforeRender = (dt, T) => { window.__aruS(x, z, 0, T > .1 && T < 3.8, T); const u = P.player.obj.userData; if (T > 2.4 && T < 3.8 && u.armR) { u.armR.rotation.x = -1.6; }
    const k = Math.min(1, Math.max(0, T - 3.9) / 4.5), e = k * k * (3 - 2 * k);
    window.__C(x, P.surfaceY(x, z) + 1.2 - .6 * e, z - 2.4 * e); P.cam.dist = 2.8 + 12 * e; P.cam.yaw = 0 + .35 * e; P.cam.pitch = .15 + .65 * e; window.__clr([], x, z, e < .3 ? .7 : .01); }; }"""
SHOTS = {'c1': (C1, 150), 'c2': (C2, 88), 'c3': (C3, 215), 'c4': (C4, 95), 'c5': (C5, 145), 'c6': (C6, 172), 'c7': (C7, 135),
         'c8': (C8, 118), 'c9': (C9, 178), 'c10': (C10, 145), 'c11': (C11, 120), 'c12': (C12, 265)}
CLEAR = E35.CLEAR
async def run(which):
    async with async_playwright() as p:
        b, pg = await setup(p)
        for js in CHAIN + (SETUP36,): await pg.evaluate(js)
        if 'pos' in which:
            print(await pg.evaluate(POS)); print('site', await pg.evaluate("() => window.__pulau.acts.spots.build.map(s => [s.cx, s.cy, s.x, s.z])"))
        print('cast', await pg.evaluate("() => [window.__HF(), window.__RZ(), window.__GINA(), window.__ALIF(), window.__NOVA(), window.__ET(), window.__K(), window.__PR()].map(n => n ? n.name : null)"))
        for k, (js, n) in SHOTS.items():
            if k in which and 'prev' not in which:
                await shoot(pg, 'e36' + k, int(os.environ.get('N_' + k, n)), start_js=js, warm=12)
                await pg.evaluate(CLEAR)
        if 'prev' in which:
            for k, (js, n) in SHOTS.items():
                if 'all' not in which and k not in which: continue
                for w in os.environ.get('WARMS', os.environ.get('WARM', '40')).split('/'):
                    await shoot(pg, 'p36' + k + ('' if '/' not in os.environ.get('WARMS', '') else '_' + w), 1, start_js=js, warm=int(w))
                    await pg.evaluate(CLEAR)
        await b.close()
if __name__ == "__main__": asyncio.run(run(sys.argv[1].split(",")))
