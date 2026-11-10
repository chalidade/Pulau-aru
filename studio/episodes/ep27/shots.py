"""Episode 27 "Menteri Keuangan & Gedung Rapat" shot list (format KONSEP).  usage: DPR=2 python3 shots.py c1,c3,...  (DPR=1 + prev for checks)
@araa_yinchan's comment ("aku mau jadi mentri keuangan, sekalian gedung buat rapat") becomes the island's first minister and an
open-front Gedung Rapat Pulau on the west cross street (cells 36-40 x 47-50). The anonymous Trakteer gift ("warga jaga warga")
becomes a WARGA JAGA WARGA banner beside it. Reuses the helper JS of ep25 (BASE, NPC, EXTRA).
"""
import asyncio, sys, os, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'lib'))
from harness import *
_sp = importlib.util.spec_from_file_location('ep25shots', os.path.join(HERE, '..', 'ep25', 'shots.py')); E25 = importlib.util.module_from_spec(_sp); _sp.loader.exec_module(E25)
BASE, NPC, EXTRA = E25.BASE, E25.NPC, E25.EXTRA
GUARD, PINJAM, ARAA = 'Cawetssssss', 'Pinjam seratus 💸', 'araa_yinchan'
EP27 = """window.__G = () => window.__bld('gedungrapat');
  window.__FY = () => window.__G().position.y + .24;                       // the hall's floor height
  window.__A = () => window.__N('%s');
  window.__C = (x, y, z) => { window.__camTarget = new window.__pulau.cam.target.constructor(x, y, z); };
  window.__crowdAt = (pts, T, pose) => { const W = window.__W().filter(n => n.obj && !n.castSpot && !n.demo); pts.forEach(([x, z, f], i) => window.__pose(W[i], x, z, f, typeof pose === 'function' ? pose(i) : pose, T + i * .5)); return W.slice(0, pts.length); };
  window.__D = () => window.__pulau.npcs.filter(n => n.demo);
  window.__lamps = () => window.__hideInst([[-19.2, -4.2], [-16.2, -4.2], [-22.2, -4.2], [-13.2, -4.2], [-19.2, -1.8], [-16.2, -1.8]], 1.6);""" % ARAA
AX, AZ = -16.87, -7.75       # araa's live spot: standing at the Menteri Keuangan seat behind the table
# c1 cold open: the new minister behind the meeting table, calculator up, pointing at the viewer
C1 = """() => { const P = window.__pulau, a = window.__A(); window.__clock = .3; window.__cheer = null; P.player.obj.visible = false; window.__lamps(); const y = window.__FY();
  window.__look(%s, %s, -.12, .06, 2.2, false);
  window.__beforeRender = (dt, T) => { window.__keep([a], %s, %s, 2.6); window.__poseY(a, %s, y, %s, -.1, T < 1.3 ? 'cheer' : (T < 3.4 ? 'point' : 'talk'), T); window.__C(%s - .15, y + 1.32, %s); P.cam.dist = Math.max(2.05, 2.5 - T * .12); }; }""" % (AX, AZ, AX, AZ, AX, AZ, AX, AZ)
# c2 premise: from the hall up over the town (follow = warga, comment = kenyataan)
C2 = """() => { const P = window.__pulau; window.__clock = .3; window.__cheer = null; P.player.obj.visible = false; window.__look(-17.5, -7, .55, .5, 9, false);
  window.__beforeRender = (dt, T) => { window.__C(-17.5 + T * 2.2, 0, -7 + T * 1.6); P.cam.pitch = Math.min(1.0, .5 + T * .11); P.cam.dist = 9 + T * 8; P.cam.yaw = .55 + T * .05; }; }"""
# c3 reveal: from the sign, pulling back over the street to the whole hall with residents cheering in front
C3 = """() => { const P = window.__pulau; window.__clock = .3; window.__cheer = null; P.player.obj.visible = false; window.__lamps(); const a = window.__A();
  window.__look(-17.5, -6.5, .25, .3, 4.0, false);
  window.__beforeRender = (dt, T) => { window.__keep(window.__D().concat([a]), -17.5, -5, 6); window.__C(-17.5, window.__FY() + 1.4 - T * .08, -6.4);
    P.cam.dist = Math.min(10.5, 4 + T * 1.4); P.cam.pitch = .3 + T * .02; }; }"""
# c4 the bodyguard stops the minister at the step: 'Berhenti. Identitas dulu.' / 'Aku menteri!' / 'Menteri juga identitas dulu.'
C4 = """() => { const P = window.__pulau, a = window.__A(), g = window.__N('%s'); window.__fix(g); window.__clock = .3; window.__cheer = null; P.player.obj.visible = false; window.__lamps();
  const gx = -17.5, gz = -4.95, ax = -17.45, az = -3.95; window.__look(gx, gz, 1.45, .1, 3.2, false);
  window.__beforeRender = (dt, T) => { window.__keep([a, g], gx, gz, 3); window.__z0(g); window.__z0(a); window.__guardP(g, gx, gz, 0, T, T < 1.9 || T > 3.1);
    window.__pose(a, ax, az, PI, T > 1.75 && T < 3.1 ? 'panic' : (T > 3.1 ? 'still' : 'walk'), T); window.__C(gx, P.WD.groundY(gx, gz) + 1.15, gz + .5); P.cam.dist = Math.max(2.6, 3.2 - T * .12); }; }""" % GUARD
# c5 President 'EGA_ welcomes her in the hall: 'Selamat datang, Bu Menteri Keuangan!' / 'Aku mulai periksa... kas presiden.'
C5 = """() => { const P = window.__pulau, a = window.__A(), pr = window.__PR(); window.__clock = .3; window.__cheer = null; P.player.obj.visible = false; window.__lamps(); const y = window.__FY();
  const px = -17.9, pz = -6.5; window.__look(-17.15, -7.4, -.45, .12, 3.2, false);
  window.__beforeRender = (dt, T) => { window.__keep([a, pr], -17.35, -7.1, 2.4); window.__poseY(pr, px, y, pz, 2.45, T < 1.6 ? 'wave' : 'still', T); window.__poseY(a, %s, y, %s, -.6, T < 1.6 ? 'cheer' : 'talk', T);
    window.__C(-17.15, y + 1.05, -7.4); P.cam.dist = Math.max(2.7, 3.2 - T * .1); P.cam.yaw = -.45 + T * .03; }; }""" % (AX, AZ)
# c6 'Lho? Kenapa dari aku?' over the agenda board: item 1 = the five coins from the Kotak Usulan
C6 = """() => { const P = window.__pulau; window.__clock = .3; window.__cheer = null; P.player.obj.visible = false; const y = window.__G().position.y;
  window.__look(-17.5, -8.4, 0, .04, 2.6, false); window.__keep([], -17.5, -7.5, 3);
  window.__beforeRender = (dt, T) => { window.__keep([], -17.5, -7.5, 3); window.__C(-17.5, y + 2.15 + Math.min(.12, T * .03), -8.45); P.cam.dist = Math.max(2.5, 2.9 - T * .08); }; }"""
# c7 the president panics: 'Itu donasi! Nanti dikembalikan!' while the minister taps her calculator behind him
C7 = """() => { const P = window.__pulau, a = window.__A(), pr = window.__PR(); window.__clock = .3; window.__cheer = null; P.player.obj.visible = false; window.__lamps(); const y = window.__FY();
  const px = -17.45, pz = -6.45; window.__look(px, pz, .15, .08, 2.3, false);
  window.__beforeRender = (dt, T) => { window.__keep([a, pr], px, pz, 2.6); window.__poseY(pr, px, y, pz, .15, 'panic', T); window.__poseY(a, %s, y, %s, 0, 'still', T); const u = a.obj.userData; u.armL.rotation.x = -1.15; u.armR.rotation.x = -1.3 + Math.sin(T * 18) * .08;
    window.__C(px + .15, y + 1.1, pz - .3); P.cam.dist = Math.max(1.9, 2.3 - T * .15); }; }""" % (AX, AZ)
# c8 Pinjam Seratus at the step: 'Bu Menteri... pinjam seratus dulu?' / 'Ditolak. Ajukan proposal.'
C8 = """() => { const P = window.__pulau, a = window.__A(), b = window.__N('%s'); window.__fix(b); window.__clock = .3; window.__cheer = null; P.player.obj.visible = false; window.__lamps(); const y = window.__FY();
  const bx = -16.1, bz = -6.5; window.__look(-16.5, -7.1, -.35, .12, 3.3, false);
  window.__beforeRender = (dt, T) => { window.__keep([a, b], -16.5, -7.1, 2.6); window.__z0(a); window.__z0(b); window.__poseY(b, bx, y, bz, -2.62, T < 3.0 ? 'reach' : 'panic', T); window.__poseY(a, %s, y, %s, .43, T < 3.0 ? 'still' : 'point', T);
    if (T < 3.0) { const u = b.obj.userData; u.armL.rotation.x = u.armR.rotation.x = -1.25; u.armL.rotation.z = .25; u.armR.rotation.z = -.25; }
    window.__C(-16.5, y + 1.05, -7.05); P.cam.dist = Math.max(3.3, 3.8 - T * .1); P.cam.yaw = -.35 + T * .03; }; }""" % (PINJAM, AX, AZ)
# c9 the gift: WARGA JAGA WARGA banner beside the hall, residents cheering under it
C9 = """() => { const P = window.__pulau; window.__clock = .3; window.__cheer = null; P.player.obj.visible = false; window.__lamps();
  const pts = [[-24.2, -5.3, -.1], [-23.3, -5.0, 0], [-22.4, -5.3, .1], [-21.6, -5.0, .2]];
  window.__look(-23, -6.5, -.15, .12, 6.5, false);
  window.__beforeRender = (dt, T) => { const C = window.__crowdAt(pts, T, i => i % 2 ? 'cheer' : 'wave'); window.__keep(C, -23, -5.5, 5); window.__C(-23, P.WD.groundY(-23, -6.5) + 2.0, -6.5); P.cam.dist = Math.max(5.2, 6.5 - T * .25); P.cam.yaw = -.15 + T * .03; }; }"""
# c10 'Rapat pertama Pulau Aru... resmi dimulai!': Aru at the front of the hall, the minister at her seat, residents cheering on the street
C10 = """() => { const P = window.__pulau, a = window.__A(); window.__clock = .3; window.__cheer = true; window.__lamps(); const y = window.__FY();
  window.__look(-17.5, -5.6, .05, .2, 6.5, false);
  window.__beforeRender = (dt, T) => { window.__keep(window.__D().concat([a]), -17.5, -5, 5); window.__poseY(a, %s, y, %s, 0, 'cheer', T);
    window.__aru(-17.5, -5.9, 0, false, T); P.player.obj.position.y = y; const u = P.player.obj.userData; if (u.armR) { u.armR.rotation.x = T < 1.4 ? -1.2 + Math.sin(T * 8) * .4 : -2.9; u.armL.rotation.x = T < 1.4 ? -.4 : -2.9; }
    window.__C(-17.5, y + 1.1, -6.2); P.cam.dist = Math.max(4.6, 6.5 - T * .6); }; }""" % (AX, AZ)
# c11 end: up from the hall over the cross street and the town
C11 = """() => { const P = window.__pulau, a = window.__A(); window.__clock = .3; window.__cheer = null; window.__lamps(); const y = window.__FY();
  window.__look(-17.5, -6.2, -.7, .22, 5.5, false);
  window.__beforeRender = (dt, T) => { window.__keep([a], -17.5, -6, 2.5); window.__aru(-17.5, -5.9, 0, T > 4.6, T); P.player.obj.position.y = y; window.__C(-17.5 + T * .6, y + 1.0, -6.2 + T * .3); P.cam.dist = 5.5 + T * 4.2; P.cam.pitch = Math.min(1.0, .22 + T * .14); P.cam.yaw = -.7 + T * .04; }; }"""
SHOTS = {'c1': (C1, 185), 'c2': (C2, 150), 'c3': (C3, 185), 'c4': (C4, 165), 'c5': (C5, 195), 'c6': (C6, 200), 'c7': (C7, 85),
         'c8': (C8, 175), 'c9': (C9, 170), 'c10': (C10, 115), 'c11': (C11, 300)}
CLEAR = "() => { window.__showInst(); window.__cheer = null; window.__camTarget = null; window.__beforeRender = null; window.__clock = null; window.__tourS = null; }"
async def run(which):
    async with async_playwright() as p:
        b, pg = await setup(p)
        await pg.evaluate(BASE); await pg.evaluate("() => { " + NPC + " }"); await pg.evaluate("() => { " + EXTRA + " }"); await pg.evaluate("() => { " + EP27 + " }")
        for k, (js, n) in SHOTS.items():
            if k in which and 'prev' not in which:
                await shoot(pg, 'e27' + k, int(os.environ.get('N_' + k, n)), start_js=js, warm=12)
                await pg.evaluate(CLEAR)
        if 'prev' in which:
            for k, (js, n) in SHOTS.items():
                if 'all' not in which and k not in which: continue
                await shoot(pg, 'p27' + k, 1, start_js=js, warm=int(os.environ.get('WARM', '40')))
                await pg.evaluate(CLEAR)
        await b.close()
if __name__ == "__main__": asyncio.run(run(sys.argv[1].split(",")))
