"""Episode 39 "Komentarmu Jadi Rumahmu" shot list (format KONSEP, run pagi 16 Nov).  usage: DPR=2 python3 shots.py c1,c3,...  (DPR=1 + prev for checks)
Two queued requests (komentar.md, 12 Nov): @adamfahriganteng & @nenkrahma16 'rumah warga' -> Jalan Warga (new street y77-78 west of
the main street, x36-53) with Rumah Ganteng (rumahwarga x41 y74, giant gold mirror) and Rumah Kebun (rumahwarga x45 y74, flower bed +
rocking chair), three empty plots (kavling 'KAVLING KOSONG / rumahmu?'). Pinjam Seratus now stands between the two houses (wants to
'borrow the house'), dell_ sits on Rumah Kebun's rocking chair. Every resident stays on its real island.json spot (web parity); shots
only move the camera, Aru, and pop the new buildings up in c3. Reuses the ep38 helper chain.
"""
import asyncio, sys, os, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'lib'))
from harness import *
def _mod(name, path):
    sp = importlib.util.spec_from_file_location(name, path); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m
E38 = _mod('ep38shots', os.path.join(HERE, '..', 'ep38', 'shots.py'))
CHAIN = E38.CHAIN + (E38.SETUP38,)
SETUP39 = """() => { const P = window.__pulau;
  const all = t => { const r = []; P.scene.traverse(o => { if (o.userData && o.userData.b && o.userData.b.type === t && o.userData.b.ep === 39) r.push(o); }); return r; };
  window.__NEW = [...all('rumahwarga'), ...all('kavling'), ...all('papan')].sort((a, b) => b.position.x - a.position.x);
  for (const o of window.__NEW) o.userData.s0 = o.scale.clone();
  window.__AD = () => window.__N('adamfahriganteng'); window.__NE = () => window.__N('nenkrahma16');
  window.__PJ = () => window.__N('Pinjam seratus 💸'); window.__DL = () => window.__N('dell_');
  window.__hid39 = []; { const sc = P.roads.parent, pts = []; for (let x = -21; x <= -1; x += .8) for (let z = 22.9; z <= 26.5; z += .8) pts.push([x, z]);
    sc.traverse(o => { if (!o.isInstancedMesh) return; const m = new (o.matrix.constructor)(), v = new (P.cam.target.constructor)(); const c = o.material && o.material.color ? o.material.color.getHexString() : ''; if (c === '5a9e44') return;
      for (let i = 0; i < o.count; i++) { o.getMatrixAt(i, m); v.setFromMatrixPosition(m); if (pts.some(([x, z]) => Math.hypot(v.x - x, v.z - z) < .75)) { const z0 = m.clone().scale(new (P.cam.target.constructor)(0, 0, 0)); o.setMatrixAt(i, z0); o.instanceMatrix.needsUpdate = true; window.__hid39.push(i); } } }); }
  window.__fix39 = () => { window.__fix38(); for (const o of window.__NEW) { o.visible = true; o.scale.copy(o.userData.s0); }
    for (const f of [window.__AD, window.__NE, window.__PJ, window.__DL]) { const n = f(); if (n) n.obj.visible = true; } };
}"""
POS = """() => { const o = {}; for (const [k, f] of Object.entries({ ad: window.__AD, ne: window.__NE, pj: window.__PJ, dl: window.__DL })) { const n = f(); o[k] = n ? [n.x, n.z, n.obj.position.y, n.obj.rotation.y] : null; }
  o.new = window.__NEW.map(b => [b.userData.b.type, b.position.x, b.position.z]); return o; }"""
ARM = """window.__arm = (n, l, r, lz, rz) => { const u = n.obj.userData; if (!u.armR) return; u.armL.rotation.x = l; u.armR.rotation.x = r; u.armL.rotation.z = lz || 0; u.armR.rotation.z = rz || 0; };"""
HEAD = """const P = window.__pulau; window.__fix39(); """ + ARM + """ window.__clock = .42; window.__cheer = null; """
# c1 cold open: Adam at his giant mirror turns to camera ('Rumahku jadi!'), then back to the mirror on '...ganteng'
C1 = """() => { """ + HEAD + """ P.player.obj.visible = false; const a = window.__AD(), x = a.x, z = a.z, f0 = a.obj.rotation.y;
  window.__look(x, z, .3, .05, 2.4, false);
  window.__beforeRender = (dt, T) => { const k = Math.min(1, Math.max(0, T - 3.6) / .5); a.obj.rotation.y = .35 + (f0 - .35) * k;
    window.__C(x + .1, P.surfaceY(x, z) + 1.2, z - .3); P.cam.dist = Math.max(2.0, 2.5 - T * .08); P.cam.yaw = .3 + T * .02; P.cam.pitch = .05; window.__clr([a], x, z, .5); }; }"""
# c2 premise + both comment cards: aerial gliding from high over the island down onto Jalan Warga
C2 = """() => { """ + HEAD + """ P.player.obj.visible = false;
  window.__look(-6, 12, -.4, 1.05, 62, false);
  window.__beforeRender = (dt, T) => { const k = Math.min(1, Math.max(0, T) / 6.5), e = k * k * (3 - 2 * k); window.__C(-6 - 5 * e, 1 + .5 * e, 12 + 9 * e); P.cam.dist = 62 - 44 * e; P.cam.pitch = 1.05 - .35 * e; P.cam.yaw = -.4 + .4 * e; }; }"""
# c3 'kami bangun satu jalan baru': houses, plots and the street sign pop up one by one from east to west (t 1.2 - 4.2)
C3 = """() => { """ + HEAD + """ P.player.obj.visible = false; const N = window.__NEW;
  window.__look(-11, 21, .15, .92, 18, false);
  window.__beforeRender = (dt, T) => { N.forEach((o, i) => { const t0 = 1.0 + i * .5, u = Math.max(0, Math.min(1, (T - t0) / .45)); const s = u <= 0 ? 0.001 : (u < 1 ? 1 + Math.sin(u * Math.PI) * .25 - (1 - u) * .9 : 1); o.scale.set(o.userData.s0.x * Math.max(.001, Math.min(1.25, s)), o.userData.s0.y * Math.max(.001, s), o.userData.s0.z * Math.max(.001, Math.min(1.25, s))); });
    for (const f of [window.__AD, window.__NE, window.__PJ, window.__DL]) { const n = f(); if (n) n.obj.visible = T > 4.4; }
    window.__cheer = T > 3.4 ? 1 : null; window.__C(-11, 1.5, 19.8); P.cam.dist = 18 - T * .5; P.cam.yaw = .05 - T * .02; P.cam.pitch = .92; }; }"""
# c4 two-shot: Aru (left) points at the mirror, Adam (right) answers proudly
C4 = """() => { """ + HEAD + """ const a = window.__AD(), ax = a.x - .95, az = a.z + .15, mx = (ax + a.x) / 2, mz = (az + a.z) / 2;
  window.__look(ax, az, 0, .1, 2.8, true);
  window.__beforeRender = (dt, T) => { window.__aruS(ax, az, Math.PI / 2 - .4, T < 1.8, T); if (T < 1.8) { const u = P.player.obj.userData; if (u.armR) u.armR.rotation.x = -2.0; }
    a.obj.rotation.y = T < 1.6 ? 2.8 : -1.1; window.__C(mx, P.surfaceY(mx, mz) + 1.0, mz - .1); P.cam.dist = Math.max(2.4, 2.9 - T * .1); P.cam.yaw = .05; P.cam.pitch = .1; window.__clr([a], mx, mz, .6); }; }"""
# c5 Rumah Kebun: from the flowers and rocking chair the camera pulls back to the sign
C5 = """() => { """ + HEAD + """ P.player.obj.visible = false; const x = -9.5, z = 20.6;
  window.__look(x, z, -.25, .15, 2.0, false);
  window.__beforeRender = (dt, T) => { const k = Math.min(1, T / 4.0), e = k * k * (3 - 2 * k); window.__C(x - .3 + .3 * e, P.surfaceY(x, z) + .8 + .9 * e, z + .2 - .5 * e); P.cam.dist = 2.0 + 3.8 * e; P.cam.yaw = -.25 + .2 * e; P.cam.pitch = .15 + .05 * e; window.__clr([window.__NE()], x, z, .4); }; }"""
# c6 nenkrahma16 close at her flower bed, waving: 'Akhirnya punya rumah!'
C6 = """() => { """ + HEAD + """ P.player.obj.visible = false; const n = window.__NE(), x = n.x, z = n.z;
  window.__look(x, z, .35, .1, 2.1, false);
  window.__beforeRender = (dt, T) => { window.__C(x, P.surfaceY(x, z) + 1.05, z); P.cam.dist = Math.max(1.7, 2.1 - T * .1); P.cam.yaw = .35; P.cam.pitch = .1; window.__clr([n], x, z, .5); }; }"""
# c7 Pinjam Seratus begging in front of Rumah Ganteng: 'Boleh pinjam seratus? Buat DP.'
C7 = """() => { """ + HEAD + """ P.player.obj.visible = false; const n = window.__PJ(), x = n.x, z = n.z;
  window.__look(x, z, -1.0, .1, 2.2, false);
  window.__beforeRender = (dt, T) => { window.__C(x, P.surfaceY(x, z) + 1.0, z); P.cam.dist = Math.max(1.8, 2.2 - T * .07); P.cam.yaw = -1.0 + T * .02; P.cam.pitch = .1; window.__clr([n], x, z, .5); }; }"""
# c8 two-shot: Aru (left) 'Ini gratis, Farel.' / Pinjam (right) '...pinjam rumahnya.'
C8 = """() => { """ + HEAD + """ const n = window.__PJ(), ax = n.x - .9, az = n.z + .1, mx = (ax + n.x) / 2, mz = (az + n.z) / 2;
  window.__look(ax, az, 0, .1, 2.8, true);
  window.__beforeRender = (dt, T) => { window.__aruS(ax, az, Math.PI / 2, T < 1.15, T); n.obj.rotation.y = -Math.PI / 2 + .25;
    window.__C(mx, P.surfaceY(mx, mz) + 1.0, mz); P.cam.dist = Math.max(2.5, 2.9 - T * .08); P.cam.yaw = 0; P.cam.pitch = .1; window.__clr([n], mx, mz, .6); }; }"""
# c9 dell_ on Rumah Kebun's rocking chair, rocking gently: Aru (off) 'Dell? Itu kursi goyang orang.' -> 'hm.' (push-in)
C9 = """() => { """ + HEAD + """ P.player.obj.visible = false; const n = window.__DL(), x = n.x, z = n.z, y0 = n.obj.position.y; const kb = window.__NEW.find(o => o.userData.b.deco === 'kebun'); const ch = kb && kb.userData.chair;
  window.__look(x, z, -.35, .12, 2.4, false);
  window.__beforeRender = (dt, T) => { const r = Math.sin(T * 2.2) * .07; n.obj.rotation.x = r; if (ch) ch.rotation.x = r;
    const k = Math.min(1, Math.max(0, T - 1.9) / .5); window.__C(x, y0 + .75, z); P.cam.dist = 2.4 - .7 * k; P.cam.yaw = -.35; P.cam.pitch = .12; window.__clr([n], x, z, .5); }; }"""
# c10 the empty plot at the end of the street: the sign close, then pull back over the three plots
C10 = """() => { """ + HEAD + """ P.player.obj.visible = false; const x = -16.8, z = 20.6;
  window.__look(x, z, .1, .12, 1.8, false);
  window.__beforeRender = (dt, T) => { const k = Math.min(1, Math.max(0, T - 1.2) / 2.6), e = k * k * (3 - 2 * k); window.__C(x + 3 * e, P.surfaceY(x, z) + 1.3 + .3 * e, z + 1.5 * e); P.cam.dist = 1.8 + 11 * e; P.cam.yaw = .1 + .2 * e; P.cam.pitch = .12 + .55 * e; }; }"""
# c11 end: Aru waving in the middle of Jalan Warga, the camera cranes up over the whole street
C11 = """() => { """ + HEAD + """ window.__cheer = true; const x = -11.5, z = 22.0;
  window.__look(x, z, 0, .12, 2.8, true);
  window.__beforeRender = (dt, T) => { window.__aruS(x, z, 0, T > .1 && T < 6.5, T); const u = P.player.obj.userData; if (u.armR) u.armR.rotation.x = -2.7 + Math.sin(T * 8) * .25;
    const k = Math.min(1, Math.max(0, T - 2.0) / 5.5), e = k * k * (3 - 2 * k);
    window.__C(x, P.surfaceY(x, z) + 1.1 + .4 * e, z - 1.5 * e); P.cam.dist = 2.8 + 17 * e; P.cam.yaw = .3 * e; P.cam.pitch = .12 + .65 * e; window.__clr([], x, z, e < .25 ? .5 : .01); }; }"""
SHOTS = {'c1': (C1, 190), 'c2': (C2, 215), 'c3': (C3, 175), 'c4': (C4, 145), 'c5': (C5, 152), 'c6': (C6, 124), 'c7': (C7, 182),
         'c8': (C8, 158), 'c9': (C9, 95), 'c10': (C10, 122), 'c11': (C11, 310)}
CLEAR = E38.CLEAR
async def run(which):
    async with async_playwright() as p:
        b, pg = await setup(p)
        for js in CHAIN + (SETUP39,): await pg.evaluate(js)
        if 'pos' in which: print(await pg.evaluate(POS))
        print('cast', await pg.evaluate("() => [window.__AD(), window.__NE(), window.__PJ(), window.__DL()].map(n => n ? n.name : null)"))
        for k, (js, n) in SHOTS.items():
            if k in which and 'prev' not in which:
                await shoot(pg, 'e39' + k, int(os.environ.get('N_' + k, n)), start_js=js, warm=12)
                await pg.evaluate(CLEAR)
        if 'prev' in which:
            for k, (js, n) in SHOTS.items():
                if 'all' not in which and k not in which: continue
                for w in os.environ.get('WARMS', os.environ.get('WARM', '40')).split('/'):
                    await shoot(pg, 'p39' + k + ('' if '/' not in os.environ.get('WARMS', '') else '_' + w), 1, start_js=js, warm=int(w))
                    await pg.evaluate(CLEAR)
        await b.close()
if __name__ == "__main__": asyncio.run(run(sys.argv[1].split(",")))
