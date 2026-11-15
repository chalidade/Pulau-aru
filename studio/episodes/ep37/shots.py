"""Episode 37 "Rumah Sakit Hewan" shot list (format KONSEP, run pagi 15 Nov).  usage: DPR=2 python3 shots.py c1,c3,...  (DPR=1 + prev for checks; 'pos' prints positions)
Two queued comments (komentar.md): @xonixccx_ 'nini nono nana' names the three Rumah Camar chicks (sign on the pole + Nono's bandage,
tamancamar b.names / b.bandage) and @umi.cholifah164 'min bikin rumah sakit' -> Rumah Sakit Hewan (rshewan x71 y62) next to Taman Pulau,
where Luci Ardiansyah (Si Sok Tahu, now 'dokter hewan, katanya', resident spot 69,63 pose dokter) bandages Nono's sprained wing.
Side beats: Penjaga Mercusuar at the KOTAK SUARA (likes still being counted), EGA returns the five coins (mejadaftar foot).
Reuses the ep36 helper chain.
"""
import asyncio, sys, os, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'lib'))
from harness import *
def _mod(name, path):
    sp = importlib.util.spec_from_file_location(name, path); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m
E36 = _mod('ep36shots', os.path.join(HERE, '..', 'ep36', 'shots.py'))
CHAIN = E36.CHAIN + (E36.SETUP36,)
SETUP37 = """() => { const P = window.__pulau, V = P.cam.target.constructor;
  const find = t => { let r = null; P.scene.traverse(o => { if (!r && o.userData && o.userData.b && o.userData.b.type === t) r = o; }); return r; };
  window.__RS = find('rshewan'); window.__TC = find('tamancamar'); window.__MD = find('mejadaftar');
  window.__LU = () => window.__N('Luci Ardiansyah');
  window.__W = (o, x, y, z) => { const v = new V(x, y, z); o.localToWorld(v); return v; };
  const ch = window.__TC.userData.chicks;
  window.__band = (c, on) => { for (let i = 5; i < c.children.length; i++) c.children[i].visible = on; };
  // a stand-in Nono for the bed and for the tumble (the nest chicks are animated by main.js)
  const mk = () => { const c = ch[1].clone(true); c.traverse(o => { if (o.isMesh) o.castShadow = true; }); P.scene.add(c); c.visible = false; return c; };
  window.__nonoBed = mk(); window.__nonoFly = mk();
  window.__nonoBed.scale.setScalar(1.7); for (const c of [window.__nonoBed, window.__nonoFly]) for (let i = 5; i < c.children.length; i++) { const m = c.children[i].material.clone(); m.emissive && m.emissive.set('#ffffff'); m.emissiveIntensity = .35; c.children[i].material = m; }
  window.__bedPos = () => window.__W(window.__RS, -1.1, 1.03, 1.25);
  window.__rest37 = () => { window.__nonoBed.visible = false; window.__nonoFly.visible = false; ch[1].visible = true; window.__band(ch[1], true); window.__RS.scale.set(1, 1, 1); if (window.__coin) window.__coin.visible = false; };
  window.__fix37 = () => { window.__fix36(); window.__rest37(); };
  // EGA's coin (c10): a gold disc in his raised hand
  return import('/lib/three/three.module.min.js').then(T => { const c = new T.Mesh(new T.CylinderGeometry(.075, .075, .018, 16), new T.MeshStandardMaterial({ color: '#e6b84a', metalness: .7, roughness: .3, emissive: '#7a5a10', emissiveIntensity: .3 })); c.rotation.x = Math.PI / 2; c.visible = false; P.scene.add(c); window.__coin = c; });
}"""
POS = """() => { const P = window.__pulau, o = {}, l = window.__LU(); o.luci = l ? [l.x, l.z, l.obj.position.y] : null; o.rs = window.__RS.position.toArray(); o.tc = window.__TC.position.toArray();
  o.bed = window.__bedPos().toArray(); o.nest = window.__W(window.__TC.userData.nest, 0, 0, 0).toArray(); o.md = window.__MD.position.toArray(); return o; }"""

# c1 cold open (flash-forward): Luci in her white coat at the exam table, Nono (bandaged) on the little bed: 'Diagnosa saya: ... kebanyakan makan sandal!'
C1 = """() => { const P = window.__pulau, l = window.__LU(); window.__fix37(); window.__clock = .36; window.__cheer = null; P.player.obj.visible = false;
  const b = window.__bedPos(), nb = window.__nonoBed; nb.visible = true; nb.position.copy(b); nb.rotation.set(0, .5, 0); window.__band(nb, true);
  const lx = b.x + .65, lz = b.z + .3; window.__look(lx, lz, .1, .14, 2.3, false);
  window.__beforeRender = (dt, T) => { window.__z0(l); window.__S(l, lx, lz, -.35, T < 3.6 ? 'talk' : 'point', T); nb.rotation.x = -Math.max(0, Math.sin(T * 3.2)) * .25;
    window.__C((lx + b.x) / 2, b.y + .35, (lz + b.z) / 2); P.cam.dist = Math.max(1.8, 2.3 - T * .12); P.cam.yaw = .1 + T * .02; P.cam.pitch = .14; window.__clr([l], lx, lz, .5); }; }"""
# c2 premise + both comment cards: aerial from high over the island gliding down onto Taman Pulau and the new hospital
C2 = """() => { const P = window.__pulau; window.__fix37(); window.__clock = .36; window.__cheer = null; P.player.obj.visible = false;
  window.__look(11, 4, .3, 1.05, 60, false);
  window.__beforeRender = (dt, T) => { const k = Math.min(1, Math.max(0, T) / 5.2), e = k * k * (3 - 2 * k); window.__C(11 + 3.5 * e, .5 + .8 * e, 4 + 5 * e); P.cam.dist = 60 - 44 * e; P.cam.pitch = 1.05 - .35 * e; P.cam.yaw = .3 + .25 * e; }; }"""
# c3 the Rumah Camar: nest with the three chicks and the pole sign 'NINI · NONO · NANA' (camera from the north, the sign faces north)
C3 = """() => { const P = window.__pulau; window.__fix37(); window.__band(window.__TC.userData.chicks[1], false); window.__clock = .36; window.__cheer = null; P.player.obj.visible = false;
  const n = window.__W(window.__TC.userData.nest, 0, 0, 0), s = window.__W(window.__TC, 0, 1.25, .11); window.__look(n.x, n.z, Math.PI, .2, 3.2, false);
  window.__beforeRender = (dt, T) => { const k = Math.min(1, Math.max(0, T - .2) / 3.2), e = k * k * (3 - 2 * k); window.__C(n.x, s.y + (n.y + .1 - s.y) * e, n.z);
    P.cam.dist = 2.9 - .6 * e; P.cam.pitch = .12 + .22 * e; P.cam.yaw = Math.PI - .15 + .3 * e; window.__clr([], n.x, n.z, .6); }; }"""
# c4 Nono tries to fly: hops up out of the nest flapping its stubby body, then tumbles back in on its side (wing sprained)
C4 = """() => { const P = window.__pulau, ch = window.__TC.userData.chicks; window.__fix37(); window.__clock = .36; window.__cheer = null; P.player.obj.visible = false;
  const f = window.__nonoFly; ch[1].visible = false; f.visible = true; window.__band(f, false); f.scale.setScalar(1.05);
  const nest = window.__TC.userData.nest; const p0 = window.__W(nest, ch[1].position.x, ch[1].position.y, ch[1].position.z);
  window.__look(p0.x, p0.z, Math.PI + .5, .25, 1.6, false);
  window.__beforeRender = (dt, T) => { let y = p0.y, rz = 0, rx = 0, ry = Math.PI + .5;
    if (T < 1.6) { const h = Math.abs(Math.sin(T * 7)) * .07; y += h; rx = -h * 3; }
    else if (T < 2.4) { const u = (T - 1.6) / .8; y += Math.sin(u * Math.PI) * .45; rz = Math.sin(T * 30) * .25; rx = -.4; }
    else { const u = Math.min(1, (T - 2.4) / .25); y += .02; rz = 1.25 * u; rx = 0; }
    f.position.set(p0.x, y, p0.z); f.rotation.set(rx, ry, rz);
    window.__C(p0.x, p0.y + .25, p0.z); P.cam.dist = Math.max(1.25, 1.6 - T * .07); P.cam.yaw = Math.PI + .5; P.cam.pitch = .25; window.__clr([], p0.x, p0.z, .4); }; }"""
# c5 Aru under the Rumah Camar, panicking toward the camera: 'Nono! Kita butuh rumah sakit, sekarang!'
C5 = """() => { const P = window.__pulau; window.__fix37(); window.__clock = .36; window.__cheer = null;
  const n = window.__W(window.__TC.userData.nest, 0, 0, 0), x = n.x + .2, z = n.z + 1.3; window.__look(x, z, 0, .14, 2.4, true);
  window.__beforeRender = (dt, T) => { window.__aruS(x, z, 0, T > .05 && T < 2.2, T); const u = P.player.obj.userData; if (u.armR) { u.armR.rotation.x = -2.6 + Math.sin(T * 12) * .2; u.armL.rotation.x = -2.6 - Math.sin(T * 12) * .2; }
    window.__C(x, P.surfaceY(x, z) + 1.25, z); P.cam.dist = Math.max(1.9, 2.4 - T * .25); P.cam.yaw = 0; P.cam.pitch = .14; window.__clr([], x, z, .5); }; }"""
# c6 the Rumah Sakit Hewan rises out of the grass next to Taman Pulau (pop at ~4.0 s, on 'Jadilah'), camera from the south
C6 = """() => { const P = window.__pulau, rs = window.__RS; window.__fix37(); window.__clock = .36; window.__cheer = null; P.player.obj.visible = false;
  const c = window.__W(rs, 0, 1.6, 0); window.__look(c.x, c.z + 1, 0, .3, 10, false);
  window.__beforeRender = (dt, T) => { const t0 = 3.6, u = Math.max(0, T - t0), s = T < t0 ? .02 : Math.min(1.08, u / .5) - (u > .5 ? Math.min(.08, (u - .5) * .3) : 0);
    rs.scale.set(1, Math.max(.02, s), 1); window.__cheer = T > t0 + .4 ? 1 : null;
    window.__C(c.x, c.y, c.z + .6); P.cam.dist = Math.max(7.2, 10 - T * .45); P.cam.yaw = -.12 + T * .03; P.cam.pitch = .3; window.__clr([], c.x, c.z + .6, .9); }; }"""
# c7 Luci at the hospital porch: (narrator 'Dokternya... Luci') then 'Saya dokter. Dokter apa ya? Pokoknya dokter.'
C7 = """() => { const P = window.__pulau, l = window.__LU(); window.__fix37(); window.__clock = .36; window.__cheer = null; P.player.obj.visible = false;
  const p = window.__W(window.__RS, -.75, 0, 2.0), x = p.x, z = p.z; window.__look(x, z, .35, .12, 2.6, false);
  window.__beforeRender = (dt, T) => { window.__z0(l); window.__S(l, x, z, .35, T < 3.1 ? 'still' : (T < 5.2 ? 'talk' : 'point'), T); if (T > 5.6) l.obj.userData.body.rotation.z = Math.sin(T * 3) * .05;
    window.__C(x, P.surfaceY(x, z) + 1.2, z); P.cam.dist = Math.max(2.1, 2.6 - T * .08); P.cam.yaw = .35; P.cam.pitch = .12; window.__clr([l], x, z, .55); }; }"""
# c8 the bandage: close on Nono on the little bed, the white bandage appears on its wing (warm beat)
C8 = """() => { const P = window.__pulau, l = window.__LU(); window.__fix37(); window.__clock = .36; window.__cheer = null; P.player.obj.visible = false;
  const b = window.__bedPos(), nb = window.__nonoBed; nb.visible = true; nb.position.copy(b); nb.rotation.set(0, .2, .35); window.__band(nb, false);
  const lx = b.x - .55, lz = b.z + .4; window.__look(b.x, b.z, .2, .3, 1.3, false);
  window.__beforeRender = (dt, T) => { window.__z0(l); window.__S(l, lx, lz, 2.3, 'still', T); if (l.obj.userData.armR) l.obj.userData.armR.rotation.x = -1.3 + Math.sin(T * 5) * .15;
    window.__band(nb, T > 1.0); nb.rotation.z = T > 1.0 ? Math.max(0, .35 - (T - 1.0) * .4) : .35; nb.rotation.x = T > 1.8 ? -Math.max(0, Math.sin(T * 3)) * .2 : 0;
    window.__C(b.x, b.y + .15, b.z); P.cam.dist = Math.max(1.0, 1.3 - T * .08); P.cam.yaw = .2; P.cam.pitch = .3; }; }"""
# c9 the Penjaga Mercusuar behind the KOTAK SUARA: 'Like pemilu masih dihitung. Kalkulatornya sampai panas.'
C9 = """() => { const P = window.__pulau, k = window.__K(); window.__fix37(); window.__clock = .38; window.__cheer = null; P.player.obj.visible = false;
  window.__look(2.75, -11.0, -1.75, .26, 3.0, false);
  window.__beforeRender = (dt, T) => { window.__z0(k); window.__S(k, 2.75, -11.0, -1.85, T > .1 && T < 3.9 ? 'talk' : 'still', T); window.__lant(k);
    window.__C(2.6, P.surfaceY(2.75, -11) + 1.45, -11.0); P.cam.dist = Math.max(2.5, 3.0 - T * .12); P.cam.yaw = -1.75 - T * .02; P.cam.pitch = .26; window.__clr([k], 2.6, -11.0, .8); }; }"""
# c10 EGA in front of the Kotak Suara, raising a gold coin: 'Ini lima koinnya. Aku kembalikan. Beneran hari ini!'
C10 = """() => { const P = window.__pulau, e = window.__PR(); window.__fix37(); window.__clock = .38; window.__cheer = null; P.player.obj.visible = false;
  const x = 1.55, z = -10.55; window.__look(x, z, -.75, .14, 2.4, false);
  window.__beforeRender = (dt, T) => { window.__z0(e); window.__S(e, x, z, -.75, 'talk', T); window.__VP().obj.visible = false; const u = e.obj.userData; if (u.armR) u.armR.rotation.x = -2.5;
    if (u.armR) { const hp = new P.cam.target.constructor(0, -.62, 0); u.armR.updateWorldMatrix(true, false); u.armR.localToWorld(hp); window.__coin.position.copy(hp); window.__coin.rotation.set(Math.PI / 2, 0, -.75 + Math.PI / 2 + T * 2); window.__coin.visible = true; }
    window.__C(x, P.surfaceY(x, z) + 1.25, z); P.cam.dist = Math.max(1.9, 2.4 - T * .14); P.cam.yaw = -.75; P.cam.pitch = .14; window.__clr([e], x, z, .55); window.__VP().obj.visible = false; }; }"""
# c11 Nono back in the nest with its white bandage, Nini and Nana bobbing beside it (Aru: 'Cepat sembuh, Nono!')
C11 = """() => { const P = window.__pulau; window.__fix37(); window.__clock = .4; window.__cheer = null; P.player.obj.visible = false;
  const n = window.__W(window.__TC.userData.nest, 0, 0, 0); window.__look(n.x, n.z, Math.PI + .35, .35, 1.7, false);
  window.__beforeRender = (dt, T) => { window.__C(n.x, n.y + .15, n.z); P.cam.dist = Math.max(1.35, 1.7 - T * .1); P.cam.yaw = Math.PI + .35 - T * .05; P.cam.pitch = .35; }; }"""
# c12 end: Aru in front of the Rumah Sakit Hewan waving, then the camera rises over Taman Pulau + the hospital
C12 = """() => { const P = window.__pulau; window.__fix37(); window.__clock = .4; window.__cheer = true;
  const p = window.__W(window.__RS, .9, 0, 2.6), x = p.x, z = p.z; window.__look(x, z, .1, .15, 2.8, true);
  window.__beforeRender = (dt, T) => { window.__aruS(x, z, .1, T > .1 && T < 5.5, T); const u = P.player.obj.userData; if (T < 5.5 && u.armR) { u.armR.rotation.x = -2.7 + Math.sin(T * 8) * .25; }
    const k = Math.min(1, Math.max(0, T - 4.0) / 5.0), e = k * k * (3 - 2 * k);
    window.__C(x - 3 * e, P.surfaceY(x, z) + 1.2 - .5 * e, z - 3 * e); P.cam.dist = 2.8 + 15 * e; P.cam.yaw = .1 + .3 * e; P.cam.pitch = .15 + .7 * e; window.__clr([], x, z, e < .3 ? .7 : .01); }; }"""
SHOTS = {'c1': (C1, 140), 'c2': (C2, 150), 'c3': (C3, 175), 'c4': (C4, 140), 'c5': (C5, 80), 'c6': (C6, 225), 'c7': (C7, 230),
         'c8': (C8, 90), 'c9': (C9, 130), 'c10': (C10, 130), 'c11': (C11, 90), 'c12': (C12, 330)}
CLEAR = E36.CLEAR
async def run(which):
    async with async_playwright() as p:
        b, pg = await setup(p)
        for js in CHAIN + (SETUP37,): await pg.evaluate(js)
        if 'pos' in which: print(await pg.evaluate(POS))
        print('cast', await pg.evaluate("() => [window.__LU(), window.__K(), window.__PR()].map(n => n ? n.name : null)"))
        for k, (js, n) in SHOTS.items():
            if k in which and 'prev' not in which:
                await shoot(pg, 'e37' + k, int(os.environ.get('N_' + k, n)), start_js=js, warm=12)
                await pg.evaluate(CLEAR)
        if 'prev' in which:
            for k, (js, n) in SHOTS.items():
                if 'all' not in which and k not in which: continue
                for w in os.environ.get('WARMS', os.environ.get('WARM', '40')).split('/'):
                    await shoot(pg, 'p37' + k + ('' if '/' not in os.environ.get('WARMS', '') else '_' + w), 1, start_js=js, warm=int(w))
                    await pg.evaluate(CLEAR)
        await b.close()
if __name__ == "__main__": asyncio.run(run(sys.argv[1].split(",")))
