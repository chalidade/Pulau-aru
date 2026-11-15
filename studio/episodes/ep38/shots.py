"""Episode 38 "Kapal Pesiar Raksasa" shot list (format CERITA, run sore 15 Nov).  usage: DPR=2 python3 shots.py c1,c3,...  (DPR=1 + prev for checks; 'pos' prints positions)
Two queued comments (komentar.md): @april_stecu989 'tambahin kapal pesiar raksasa aku jadi kaptennya' -> Kapal Pesiar Aru (kapalpesiar x61 y102,
gangway down to the Pelabuhan Nelayan) with Kapten April at the foot of the gangway (pose kapten), and @david.p.h3 'saya pramugari' -> a
flight attendant on a ship (pose pramugari, safety demo). Rayhan's fish flee, Klub Pertama wants to be first passenger, but Nono (healed)
flies first and perches on the bow rail (PENUMPANG PERTAMA: NONO; Taman Pulau b.away hides Nono from the nest). Reuses the ep37 helper chain.
"""
import asyncio, sys, os, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'lib'))
from harness import *
def _mod(name, path):
    sp = importlib.util.spec_from_file_location(name, path); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m
E37 = _mod('ep37shots', os.path.join(HERE, '..', 'ep37', 'shots.py'))
CHAIN = E37.CHAIN + (E37.SETUP37,)
SETUP38 = """() => { const P = window.__pulau;
  const find = t => { let r = null; P.scene.traverse(o => { if (!r && o.userData && o.userData.b && o.userData.b.type === t) r = o; }); return r; };
  window.__SH = find('kapalpesiar'); window.__SH0 = window.__SH.position.clone();
  window.__KAP = () => window.__N('april_stecu989'); window.__PRA = () => window.__N('david.p.h3');
  const pas = window.__SH.userData.chicks[0]; window.__PAS = pas;
  const fly = pas.clone(true); fly.visible = false; P.scene.add(fly); window.__pfly = fly;
  window.__pasW = () => window.__W(window.__SH, 6.6, 2.03, -.55);
  window.__fix38 = () => { window.__fix37(); window.__TC.userData.chicks[1].visible = false; window.__SH.visible = true; window.__SH.position.copy(window.__SH0);
    for (const f of [window.__KAP, window.__PRA, window.__R, window.__F, window.__DB, window.__PN]) { const n = f(); if (n) { window.__fix(n); n.obj.visible = true; } }
    pas.visible = true; fly.visible = false; window.__boatTheta = Math.PI; };
}"""
POS = """() => { const o = {}; for (const [k, f] of Object.entries({ kap: window.__KAP, pra: window.__PRA, r: window.__R, f: window.__F, db: window.__DB, pn: window.__PN })) { const n = f(); o[k] = n ? [n.x, n.z, n.obj.position.y] : null; }
  o.ship = window.__SH.position.toArray(); o.pas = window.__pasW().toArray(); o.nest = window.__W(window.__TC.userData.nest, 0, 0, 0).toArray(); return o; }"""
ARM = """window.__arm = (n, l, r, lz, rz) => { const u = n.obj.userData; if (!u.armR) return; u.armL.rotation.x = l; u.armR.rotation.x = r; u.armL.rotation.z = lz || 0; u.armR.rotation.z = rz || 0; };"""
# c1 cold open: Kapten April at the foot of the gangway, the giant ship towering behind, a salute then talking: 'Kapten April di sini! ...'
C1 = """() => { const P = window.__pulau, k = window.__KAP(); window.__fix38(); """ + ARM + """ window.__clock = .4; window.__cheer = null; P.player.obj.visible = false;
  const x = k.x, z = k.z; window.__look(x, z, Math.PI + .25, .02, 2.7, false);
  window.__beforeRender = (dt, T) => { window.__z0(k); window.__S(k, x, z, Math.PI + .25, 'still', T); if (T < 1.6) window.__arm(k, -.15, -2.75, 0, -.7); else window.__arm(k, -.3 + Math.sin(T * 5) * .15, -1.2 + Math.sin(T * 7) * .45, 0, -.2);
    window.__C(x, P.surfaceY(x, z) + 1.25 + T * .03, z); P.cam.dist = Math.max(2.3, 2.8 - T * .1); P.cam.yaw = Math.PI + .25 - T * .03; P.cam.pitch = .02; window.__clr([k, window.__PRA()], x, z, .5); }; }"""
# c2 premise + both comment cards: aerial gliding from high over the island down onto the ship at the harbour
C2 = """() => { const P = window.__pulau; window.__fix38(); window.__clock = .4; window.__cheer = null; P.player.obj.visible = false;
  window.__look(8, 30, Math.PI - .5, 1.05, 62, false);
  window.__beforeRender = (dt, T) => { const k = Math.min(1, Math.max(0, T) / 5.8), e = k * k * (3 - 2 * k); window.__C(8 + 5 * e, 1 + 1.5 * e, 30 + 17 * e); P.cam.dist = 62 - 44 * e; P.cam.pitch = 1.05 - .5 * e; P.cam.yaw = Math.PI - .5 + .25 * e; }; }"""
# c3 'tadi pagi': the harbour without the ship, Rayhan and the fisherman at the edge, empty sea
C3 = """() => { const P = window.__pulau, r = window.__R(); window.__fix38(); window.__clock = .32; window.__cheer = null; P.player.obj.visible = false;
  window.__SH.visible = false; window.__KAP().obj.visible = false; window.__PRA().obj.visible = false;
  const x = r.x, z = r.z; window.__look(x + .5, z, Math.PI - .55, .22, 4.2, false);
  window.__beforeRender = (dt, T) => { window.__KAP().obj.visible = false; window.__PRA().obj.visible = false; window.__C(x + .6, P.surfaceY(x, z) + .9, z + .4); P.cam.dist = Math.max(3.0, 4.2 - T * .22); P.cam.yaw = Math.PI - .55 + T * .03; P.cam.pitch = .22; }; }"""
# c4 the ship glides in from the south-west and settles at the harbour (horn ~2.0 s), the crew appear at the gangway
C4 = """() => { const P = window.__pulau, S = window.__SH; window.__fix38(); window.__clock = .4; window.__cheer = null; P.player.obj.visible = false;
  const s0 = window.__SH0; window.__look(12, 46.5, 2.2, .3, 20, false);
  window.__beforeRender = (dt, T) => { const k = Math.min(1, Math.max(0, T) / 3.0), e = 1 - Math.pow(1 - k, 3); S.position.set(s0.x - 26 * (1 - e), Math.sin(T * 1.1) * .05 * (1 - e), s0.z + 5 * (1 - e)); S.rotation.y = .12 * (1 - e);
    const on = T > 3.0; window.__KAP().obj.visible = on; window.__PRA().obj.visible = on; window.__cheer = T > 2.2 ? 1 : null;
    window.__C(11, 2.4, 46); P.cam.dist = 20 - T * .8; P.cam.yaw = 2.2 + T * .03; P.cam.pitch = .3; }; }"""
# c5 Rayhan turns to camera, the rod empty: 'Ikanku kabur semua!' (ship hull behind him)
C5 = """() => { const P = window.__pulau, r = window.__R(); window.__fix38(); """ + ARM + """ window.__clock = .4; window.__cheer = null; P.player.obj.visible = false;
  const x = r.x, z = r.z; window.__look(x, z, Math.PI / 2 - .5, .1, 2.0, false);
  window.__beforeRender = (dt, T) => { window.__z0(r); r.obj.position.set(x, P.surfaceY(x, z), z); r.obj.rotation.y = Math.PI / 2 - .5; window.__arm(r, -2.6 + Math.sin(T * 9) * .3, -2.6 - Math.sin(T * 9) * .3, -.3, .3);
    window.__C(x, P.surfaceY(x, z) + .95, z); P.cam.dist = Math.max(1.6, 2.0 - T * .2); P.cam.yaw = Math.PI / 2 - .5; P.cam.pitch = .1; window.__clr([r, window.__F()], x, z, .45); }; }"""
# c6 the captain close, salute then a proud point out to sea: 'Kaptennya saya! Udah follow, jadi resmi!'
C6 = """() => { const P = window.__pulau, k = window.__KAP(); window.__fix38(); """ + ARM + """ window.__clock = .42; window.__cheer = null; P.player.obj.visible = false;
  const x = k.x, z = k.z; window.__look(x, z, Math.PI - .35, .12, 2.0, false);
  window.__beforeRender = (dt, T) => { window.__z0(k); window.__S(k, x, z, Math.PI - .35, 'still', T); if (T < 1.4) window.__arm(k, -.2, -1.0 + Math.sin(T * 8) * .4, 0, 0); else window.__arm(k, -.15, -2.75, 0, -.7);
    window.__C(x, P.surfaceY(x, z) + .95, z); P.cam.dist = Math.max(1.6, 2.0 - T * .15); P.cam.yaw = Math.PI - .35; P.cam.pitch = .12; window.__clr([k, window.__PRA()], x, z, .5); }; }"""
# c7 the flight attendant: (narrator 'Dan pramugarinya...') then the safety demo, both arms out on 'kiri dan kanan' (~ last 1.5 s)
C7 = """() => { const P = window.__pulau, p = window.__PRA(); window.__fix38(); """ + ARM + """ window.__clock = .42; window.__cheer = null; P.player.obj.visible = false;
  const x = p.x, z = p.z; window.__look(x, z, Math.PI - .55, .12, 2.3, false); window.__TL = +(window.__TL || 7.0);
  window.__beforeRender = (dt, T) => { window.__z0(p); window.__S(p, x, z, Math.PI - .55, 'still', T);
    if (T < 1.5) window.__arm(p, -1.0, -1.0, .35, -.35); else if (T < 3.6) window.__arm(p, -.3, -2.3 + Math.sin(T * 6) * .3, 0, .4); else if (T < window.__TL) window.__arm(p, -1.2, -.4 + Math.sin(T * 3) * .1, .1, -.05); else window.__arm(p, -1.5, -1.5, -1.3, 1.3);
    window.__C(x, P.surfaceY(x, z) + .95, z); P.cam.dist = Math.max(1.9, 2.3 - T * .06); P.cam.yaw = Math.PI - .55 + T * .015; P.cam.pitch = .12; window.__clr([p, window.__KAP()], x, z, .5); }; }"""
# c8 two-shot: Aru (left) asks, the attendant (right) answers
C8 = """() => { const P = window.__pulau, p = window.__PRA(); window.__fix38(); """ + ARM + """ window.__clock = .42; window.__cheer = null;
  const ax = p.x - .8, az = p.z - .25, mx = (ax + p.x) / 2, mz = (az + p.z) / 2; window.__look(ax, az, Math.PI, .14, 2.8, true);
  window.__beforeRender = (dt, T) => { window.__aruS(ax, az, Math.PI - .7, T < 1.7, T); window.__z0(p); window.__S(p, p.x, p.z, Math.PI + .7, 'still', T); if (T > 1.75) window.__arm(p, -.3, -1.0 + Math.sin(T * 6) * .35, 0, 0); else window.__arm(p, -1.0, -1.0, .35, -.35);
    window.__C(mx, P.surfaceY(mx, mz) + .9, mz); P.cam.dist = Math.max(2.4, 2.8 - T * .08); P.cam.yaw = Math.PI; P.cam.pitch = .14; window.__clr([p], mx, mz, .6); }; }"""
# c9 Klub Pertama at the harbour gate, jumping: 'Penumpang pertama itu aku! Aku duluan!'
C9 = """() => { const P = window.__pulau, a = window.__DB(), b = window.__PN(); window.__fix38(); """ + ARM + """ window.__clock = .42; window.__cheer = null; P.player.obj.visible = false;
  const mx = (a.x + b.x) / 2, mz = (a.z + b.z) / 2; window.__look(mx, mz, .15, .12, 2.6, false);
  window.__beforeRender = (dt, T) => { for (const [n, s] of [[a, 0], [b, 1.3]]) { window.__z0(n); n.x = mx + (s ? .38 : -.38); n.z = mz + (s ? .12 : 0); n.obj.position.set(n.x, P.surfaceY(n.x, n.z) + Math.max(0, Math.sin(T * 9 + s)) * .18, n.z); n.obj.rotation.y = .15 + (s ? -.35 : .35); window.__arm(n, -.4, -2.9 + Math.sin(T * 10 + s) * .2, 0, .2); }
    window.__C(mx, P.surfaceY(mx, mz) + .9, mz); P.cam.dist = Math.max(2.5, 2.9 - T * .15); P.cam.yaw = .15; P.cam.pitch = .12; window.__clr([a, b], mx, mz, .6); }; }"""
# c10 the Rumah Camar: Nono (no bandage now) bobs, flaps, and takes off out of the top of the frame (~4.6 s)
C10 = """() => { const P = window.__pulau, ch = window.__TC.userData.chicks; window.__fix38(); window.__clock = .42; window.__cheer = null; P.player.obj.visible = false;
  const f = window.__nonoFly; f.visible = true; f.scale.setScalar(1.05); const nest = window.__TC.userData.nest; const p0 = window.__W(nest, -.12, .05, .2);
  window.__look(p0.x, p0.z, Math.PI + .5, .25, 1.7, false);
  window.__beforeRender = (dt, T) => { let y = p0.y, rx = 0, rz = 0; const t0 = 4.4;
    if (T < t0) { const h = Math.max(0, Math.sin(T * 6)) * .06; y += h; rx = -h * 4; rz = T > 2.6 ? Math.sin(T * 30) * .2 : 0; }
    else { const u = T - t0; y += u * u * 1.8 + u * .8; rz = Math.sin(T * 34) * .3; rx = -.5; }
    f.position.set(p0.x, y, p0.z); f.rotation.set(rx, Math.PI + .5, rz);
    window.__C(p0.x, p0.y + .25 + Math.max(0, T - 4.4) * .25, p0.z); P.cam.dist = Math.max(1.3, 1.7 - T * .07); P.cam.yaw = Math.PI + .5; P.cam.pitch = .25 - Math.max(0, T - 4.4) * .1; window.__clr([], p0.x, p0.z, .4); }; }"""
# c11 the bow: Nono flies in over the sea and lands on the rail (~2.1 s), the PENUMPANG PERTAMA sign below; Aru (off) 'Nono penumpang pertama!'
C11 = """() => { const P = window.__pulau, pas = window.__PAS, f = window.__pfly; window.__fix38(); window.__clock = .42; window.__cheer = null; P.player.obj.visible = false;
  const e = window.__pasW(); pas.visible = false; f.visible = true; window.__look(e.x - .3, e.z - .5, Math.PI + .45, .16, 2.6, false);
  window.__beforeRender = (dt, T) => { const t1 = 2.1; pas.visible = T >= t1; f.visible = T < t1;
    if (T < t1) { const u = T / t1, w = 1 - u; f.position.set(e.x - 6 * w, e.y + 2.2 * w * w + Math.sin(T * 9) * .05 * w, e.z - 3.5 * w); f.rotation.set(-.3 * w, Math.PI / 2 + .9 - .8 * w, Math.sin(T * 30) * .35 * w); f.scale.setScalar(1.6); }
    window.__C(e.x - .35, e.y - .05, e.z - .3); P.cam.dist = Math.max(1.9, 2.6 - T * .2); P.cam.yaw = Math.PI + .45; P.cam.pitch = .16; }; }"""
# c12 end: Aru waving on the harbour deck in front of the gangway, the camera rises over the whole ship and the harbour
C12 = """() => { const P = window.__pulau; window.__fix38(); window.__clock = .45; window.__cheer = true;
  const x = 10.0, z = 41.2; window.__look(x, z, Math.PI + .2, .12, 2.8, true);
  window.__beforeRender = (dt, T) => { window.__aruS(x, z, Math.PI + .2, T > .1 && T < 4.2, T); const u = P.player.obj.userData; if (u.armR) u.armR.rotation.x = -2.7 + Math.sin(T * 8) * .25;
    const k = Math.min(1, Math.max(0, T - 2.2) / 5.0), e = k * k * (3 - 2 * k);
    window.__C(x + 3 * e, P.surfaceY(x, z) + 1.2 + 1.2 * e, z + 5.5 * e); P.cam.dist = 2.8 + 22 * e; P.cam.yaw = Math.PI + .2 - .45 * e; P.cam.pitch = .12 + .55 * e; window.__clr([window.__KAP(), window.__PRA()], x, z, e < .25 ? .5 : .01); }; }"""
SHOTS = {'c1': (C1, 160), 'c2': (C2, 185), 'c3': (C3, 160), 'c4': (C4, 120), 'c5': (C5, 65), 'c6': (C6, 100), 'c7': (C7, 270),
         'c8': (C8, 150), 'c9': (C9, 115), 'c10': (C10, 205), 'c11': (C11, 145), 'c12': (C12, 260)}
CLEAR = E37.CLEAR
async def run(which):
    async with async_playwright() as p:
        b, pg = await setup(p)
        for js in CHAIN + (SETUP38,): await pg.evaluate(js)
        if 'pos' in which: print(await pg.evaluate(POS))
        print('cast', await pg.evaluate("() => [window.__KAP(), window.__PRA(), window.__R(), window.__DB(), window.__PN()].map(n => n ? n.name : null)"))
        for k, (js, n) in SHOTS.items():
            if k in which and 'prev' not in which:
                await shoot(pg, 'e38' + k, int(os.environ.get('N_' + k, n)), start_js=js, warm=12)
                await pg.evaluate(CLEAR)
        if 'prev' in which:
            for k, (js, n) in SHOTS.items():
                if 'all' not in which and k not in which: continue
                for w in os.environ.get('WARMS', os.environ.get('WARM', '40')).split('/'):
                    await shoot(pg, 'p38' + k + ('' if '/' not in os.environ.get('WARMS', '') else '_' + w), 1, start_js=js, warm=int(w))
                    await pg.evaluate(CLEAR)
        await b.close()
if __name__ == "__main__": asyncio.run(run(sys.argv[1].split(",")))
