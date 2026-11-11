"""Episode 31 "Presiden Pulau Dipilih Komentar" shot list (format KONSEP).  usage: DPR=2 python3 shots.py c1,c3,...  (DPR=1 + prev for checks)
No new comments (Apify failed, Chrome not connected, komentar.md & traktir empty), so the episode opens the second election (14 Nov):
the Meja Pendaftaran Calon (mejadaftar x57 y44 r1) next to the stage, the Penjaga Mercusuar as election committee behind it
(storyCast spot), a live queue of candidates with placards (island.json event demo at 'mejadaftar' + event.join for Klub Pertama,
Pinjam Seratus and ex-president Etet), and the Papan Pemilu reset to PEMILU KE-2 · 14 NOV with empty 'namamu?' rows.
Reuses ep25's and ep29's helpers.
"""
import asyncio, sys, os, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'lib'))
from harness import *
def _mod(name, path):
    sp = importlib.util.spec_from_file_location(name, path); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m
E25 = _mod('ep25shots', os.path.join(HERE, '..', 'ep25', 'shots.py')); E29 = _mod('ep29shots', os.path.join(HERE, '..', 'ep29', 'shots.py'))
BASE, NPC, EXTRA, EP29 = E25.BASE, E25.NPC, E25.EXTRA, E29.EP29
EP31 = """const P = window.__pulau;
  window.__K = () => window.__N('Penjaga Mercusuar'); window.__DB = () => window.__N('D..A..B..Y a..j..a'); window.__PN = () => window.__N('princes_nay');
  window.__PS = () => window.__N('Pinjam seratus 💸'); window.__G = () => window.__N('Cawetssssss'); window.__ET = () => P.npcs.find(n => n.cand === 'Etet_443');
  window.__lant = n => { const u = n.obj.userData; u.armR.rotation.x = -1.05; u.armR.rotation.z = -.12; };
  window.__dm = n => n.demo ? [n.demo.x, n.demo.z] : [n.x, n.z];
  window.__clr = (K, x, z, w) => { const P = window.__pulau, d = P.cam.dist * Math.cos(P.cam.pitch), vx = Math.sin(P.cam.yaw) * d, vz = Math.cos(P.cam.yaw) * d, L2 = vx * vx + vz * vz;
    for (const m of P.npcs) { if (K.includes(m)) { m.obj.visible = true; continue; } const px = m.obj.position.x - x, pz = m.obj.position.z - z; const t = Math.max(0, Math.min(1.3, (px * vx + pz * vz) / L2));
      m.obj.visible = !(t > .05 && Math.hypot(px - vx * t, pz - vz * t) < (w || .8)); } };
  window.__fixK = () => { window.__fix(window.__K()); window.__fix(window.__G()); };"""
# c1 cold open: DABY & princes at the front of the queue, desk + banner behind: 'Aku daftar PERTAMA!' / 'Princess duluan, dong!'
C1 = """() => { const P = window.__pulau, d = window.__DB(), p = window.__PN(), k = window.__K(); window.__fixK(); window.__clock = .38; window.__cheer = null; P.player.obj.visible = false;
  window.__look(1.0, -11.0, -1.3, .16, 3.0, false);
  window.__beforeRender = (dt, T) => { window.__z0(d); window.__z0(p);
    const pz = T > 1.35 ? Math.min(-10.95, -11.4 + (T - 1.35) * .5) : -11.4;
    window.__S(d, .95, -10.7, T < 1.4 ? -1.3 : -.4, T < 1.4 ? 'cheer' : 'panic', T); window.__S(p, .85, pz, T > 1.35 ? -1.5 : 1.57, T > 1.35 ? 'talk' : 'still', T);
    window.__C(1.1, P.surfaceY(.95, -11) + 1.25, -11.0); P.cam.dist = Math.max(2.5, 3.0 - T * .15); P.cam.yaw = -1.3 + T * .02; P.cam.pitch = .16; window.__clr([d, p, k], 1.1, -11.0, .7); }; }"""
# c2 premise: aerial glide from the south of the town to the desk next to the stage
C2 = """() => { const P = window.__pulau; window.__clock = .38; window.__cheer = true; P.player.obj.visible = false;
  window.__look(1, 10, .2, 1.05, 48, false);
  window.__beforeRender = (dt, T) => { const k = Math.min(1, Math.max(0, T) / 5.6), e = k * k * (3 - 2 * k); window.__C(1 + .3 * e, .5, 10 + (-10.5 - 10) * e); P.cam.dist = 48 - 36 * e; P.cam.pitch = 1.05 - .4 * e; P.cam.yaw = .2 - .5 * e; }; }"""
# c3 the president on the stage, bodyguard behind: 'Presiden sekarang, EGA, menang dengan... tiga like.'
C3 = """() => { const P = window.__pulau, e = window.__PR(), g = window.__G(); window.__fixK(); window.__clock = .38; window.__cheer = null; P.player.obj.visible = false;
  window.__look(-.75, -10.6, -.15, .3, 3.0, false);
  window.__beforeRender = (dt, T) => { window.__z0(e); window.__S(e, -.75, -10.6, -.3, T > 2.6 ? 'wave' : 'still', T);
    window.__C(-.75, P.surfaceY(-.75, -10.6) + 1.2, -10.6); P.cam.dist = Math.max(2.6, 3.0 - T * .12); P.cam.yaw = -.15 + T * .03; P.cam.pitch = .3; window.__clr([e, g], -.75, -10.6, .6); window.__VP().obj.visible = false; }; }"""
# c4 close on EGA, proud: 'Tiga like itu banyak, lho!'
C4 = """() => { const P = window.__pulau, e = window.__PR(); window.__fixK(); window.__clock = .38; window.__cheer = null; P.player.obj.visible = false;
  window.__look(-.75, -10.6, .25, .12, 2.2, false);
  window.__beforeRender = (dt, T) => { window.__z0(e); window.__S(e, -.75, -10.6, .25, 'cheer', T);
    window.__C(-.75, P.surfaceY(-.75, -10.6) + 1.3, -10.6); P.cam.dist = Math.max(1.9, 2.2 - T * .2); P.cam.yaw = .25; P.cam.pitch = .12; window.__clr([e], -.75, -10.6, .6); window.__VP().obj.visible = false; }; }"""
# c5 the Penjaga Mercusuar behind the desk (committee): 'Masa jabatannya habis empat belas November. Pemilu harus diulang.'
C5 = """() => { const P = window.__pulau, k = window.__K(); window.__fixK(); window.__clock = .38; window.__cheer = null; P.player.obj.visible = false;
  window.__look(2.75, -11.0, -1.85, .26, 3.0, false);
  window.__beforeRender = (dt, T) => { window.__z0(k); window.__S(k, 2.75, -11.0, -1.85, T > .1 && T < 4.2 ? 'talk' : 'still', T); window.__lant(k);
    window.__C(2.6, P.surfaceY(2.75, -11) + 1.45, -11.0); P.cam.dist = Math.max(2.5, 3.0 - T * .12); P.cam.yaw = -1.85; P.cam.pitch = .26; window.__clr([k], 2.6, -11.0, .8); }; }"""
# c6 Aru at the north end of the desk, arms up, the queue cheering: 'Pendaftaran calon presiden... resmi dibuka!'
C6 = """() => { const P = window.__pulau; window.__fixK(); window.__clock = .38; window.__cheer = true;
  window.__look(1.7, -12.5, -2.0, .22, 3.4, true);
  window.__beforeRender = (dt, T) => { window.__aruS(1.7, -12.5, -2.0, true, T); const u = P.player.obj.userData; if (T > .9 && u.armR) { u.armR.rotation.x = u.armL.rotation.x = -2.7 + Math.sin(T * 10) * .15; }
    window.__C(1.5, P.surfaceY(1.7, -12.5) + 1.2, -12.2); P.cam.dist = 3.4 + T * .3; P.cam.yaw = -2.0 + T * .05; P.cam.pitch = .22 + T * .02; window.__clr([], 1.5, -12.2, .7); }; }"""
# c7 Pinjam Seratus at the desk: 'Biaya daftarnya... boleh pinjam seratus dulu?' / keeper: 'Gratis.'
C7 = """() => { const P = window.__pulau, s = window.__PS(), k = window.__K(), d = window.__DB(), p = window.__PN(); window.__fixK(); window.__clock = .38; window.__cheer = null; P.player.obj.visible = false;
  window.__look(1.9, -11.1, -2.0, .32, 3.2, false);
  window.__beforeRender = (dt, T) => { window.__z0(s); window.__z0(k); d.obj.visible = p.obj.visible = false;
    window.__S(s, 1.2, -11.3, T < 3.5 ? -2.3 : 2.4, T < 3.5 ? 'reach' : 'panic', T); window.__S(k, 2.7, -10.5, T < 3.5 ? -1.9 : -2.2, T > 3.55 && T < 4.4 ? 'talk' : 'still', T); window.__lant(k);
    window.__C(1.95, P.surfaceY(1.25, -11.15) + 1.25, -11.1); P.cam.dist = Math.max(2.7, 3.2 - T * .1); P.cam.yaw = -2.0 + T * .02; P.cam.pitch = .32; window.__clr([s, k], 1.95, -11.1, .7); d.obj.visible = p.obj.visible = false; }; }"""
# c8 the bodyguard stops his own president on the way to the desk: 'Calon presiden! Identitas dulu!' / 'Aku presidennya!' / 'Tetap. Identitas dulu.'
C8 = """() => { const P = window.__pulau, e = window.__PR(), g = window.__G(); window.__fixK(); window.__clock = .38; window.__cheer = null; P.player.obj.visible = false;
  window.__look(-1.4, -13.9, 2.9, .2, 3.2, false);
  window.__beforeRender = (dt, T) => { window.__z0(e); window.__z0(g); window.__VP().obj.visible = false;
    const ex = Math.min(-1.75, -2.8 + Math.max(0, T) * .9);
    window.__S(e, ex, -13.9, T < 2.8 ? 1.57 : 2.6, ex < -1.76 ? 'walk' : (T > 2.85 && T < 4.0 ? 'talk' : 'still'), T);
    window.__guardP(g, -1.0, -13.9, -1.57, T, T < 2.8 || T > 4.0); if (T > 4.0) { const u = g.obj.userData; u.armR.rotation.x = -1.7; }
    window.__C(-1.4, P.surfaceY(-1.4, -13.9) + 1.15, -13.9); P.cam.dist = Math.max(3.2, 3.6 - T * .08); P.cam.yaw = 2.9; P.cam.pitch = .2; window.__clr([e, g], -1.4, -13.9, .9); }; }"""
# c9 ex-president Etet in the queue with his MANTAN PRESIDEN placard: 'Aku daftar lagi. Kali ini... dipilih beneran.'
C9 = """() => { const P = window.__pulau, t = window.__ET(); window.__fixK(); window.__clock = .38; window.__cheer = null; P.player.obj.visible = false;
  const [tx, tz] = window.__dm(t); window.__look(tx, tz, -1.2, .12, 2.9, false);
  window.__beforeRender = (dt, T) => { window.__z0(t); window.__S(t, tx, tz, -1.2, T > .1 && T < 3.7 ? 'talk' : 'still', T);
    window.__C(tx, P.surfaceY(tx, tz) + 1.6, tz); P.cam.dist = Math.max(2.4, 2.9 - T * .12); P.cam.yaw = -1.2; P.cam.pitch = .12; window.__clr([t], tx, tz, .7); }; }"""
# c10 the election board (PEMILU KE-2 · 14 NOV, empty 'namamu?' rows), then pull back over the queue at the desk
C10 = """() => { const P = window.__pulau; window.__fixK(); window.__clock = .38; window.__cheer = true; P.player.obj.visible = false;
  window.__look(2.5, -5, 0, .12, 4.6, false);
  window.__beforeRender = (dt, T) => { const k = Math.min(1, Math.max(0, T - 3.2) / 5), e = k * k * (3 - 2 * k);
    window.__C(2.5 - 1.5 * e, P.surfaceY(2.5, -5.6) + 1.9 - 1.2 * e, -5.6 - 4.6 * e); P.cam.dist = Math.max(4.0, 4.6 - T * .2) + 7 * e; P.cam.yaw = 0 - .5 * e; P.cam.pitch = .12 + .55 * e; }; }"""
# c11 DABY's campaign promise, princes outraged: 'Janjiku: semua warga jadi yang pertama!' / 'Itu nggak mungkin!'
C11 = """() => { const P = window.__pulau, d = window.__DB(), p = window.__PN(); window.__fixK(); window.__clock = .38; window.__cheer = null; P.player.obj.visible = false;
  window.__look(.9, -11.0, -1.75, .14, 2.6, false);
  window.__beforeRender = (dt, T) => { window.__z0(d); window.__z0(p);
    window.__S(d, .95, -10.7, -1.75, T < 3.1 ? 'cheer' : 'still', T); window.__S(p, .85, -11.4, T < 3.1 ? 1.2 : -1.6, T < 3.1 ? 'still' : 'panic', T);
    window.__C(.9, P.surfaceY(.9, -11) + 1.2, -11.05); P.cam.dist = Math.max(2.2, 2.6 - T * .08); P.cam.yaw = -1.75 + (T > 3.1 ? .25 : 0); P.cam.pitch = .14; window.__clr([d, p], .9, -11.05, .7); }; }"""
# c12 end: Aru north of the queue facing the camera ('Empat belas November, kita hitung. Kamu... mau jadi presiden?'), then the camera rises over the stage, desk and board
C12 = """() => { const P = window.__pulau; window.__fixK(); window.__clock = .4; window.__cheer = true;
  window.__look(-.3, -12.9, -2.5, .2, 2.8, true);
  window.__beforeRender = (dt, T) => { window.__aruS(-.3, -12.9, -2.5, T > .1 && T < 3.8, T); const u = P.player.obj.userData; if (T > 2.6 && T < 3.8 && u.armR) { u.armR.rotation.x = -1.6; }
    const k = Math.min(1, Math.max(0, T - 3.9) / 5), e = k * k * (3 - 2 * k);
    window.__C(-.3 + 1.5 * e, P.surfaceY(-.3, -12.9) + 1.2 - .7 * e, -12.9 + 3 * e); P.cam.dist = 2.8 + 15 * e; P.cam.yaw = -2.5 + 1.0 * e; P.cam.pitch = .2 + .7 * e; window.__clr([], -.3, -12.9, e < .3 ? .7 : .01); }; }"""
SHOTS = {'c1': (C1, 115), 'c2': (C2, 195), 'c3': (C3, 140), 'c4': (C4, 60), 'c5': (C5, 150), 'c6': (C6, 90), 'c7': (C7, 155),
         'c8': (C8, 200), 'c9': (C9, 135), 'c10': (C10, 280), 'c11': (C11, 160), 'c12': (C12, 310)}
CLEAR = "() => { window.__showInst && window.__showInst(); window.__cheer = null; window.__camTarget = null; window.__beforeRender = null; window.__clock = null; window.__tourS = null; for (const n of window.__pulau.npcs) { n.obj.visible = true; n.obj.userData.body.rotation.x = 0; } }"
async def run(which):
    async with async_playwright() as p:
        b, pg = await setup(p)
        await pg.evaluate(BASE); await pg.evaluate("() => { " + NPC + " }"); await pg.evaluate("() => { " + EXTRA + " }"); await pg.evaluate("() => { " + EP29 + " }"); await pg.evaluate("() => { " + EP31 + " }")
        for k, (js, n) in SHOTS.items():
            if k in which and 'prev' not in which:
                await shoot(pg, 'e31' + k, int(os.environ.get('N_' + k, n)), start_js=js, warm=12)
                await pg.evaluate(CLEAR)
        if 'prev' in which:
            for k, (js, n) in SHOTS.items():
                if 'all' not in which and k not in which: continue
                for w in os.environ.get('WARMS', os.environ.get('WARM', '40')).split('/'):
                    await shoot(pg, 'p31' + k + ('' if '/' not in os.environ.get('WARMS', '') else '_' + w), 1, start_js=js, warm=int(w))
                    await pg.evaluate(CLEAR)
        await b.close()
if __name__ == "__main__": asyncio.run(run(sys.argv[1].split(",")))
