"""Episode 28 "Kerja Bakti Pertama Pulau Aru" shot list (format CERITA).  usage: DPR=2 python3 shots.py c1,c3,...  (DPR=1 + prev for checks)
President 'EGA_'s last request (lapangan buat gotong royong) becomes the Lapangan Gotong Royong (cells 41-49 x 60-66) with a live
kerja bakti (island.json event work:true). @vcxn.mx's request becomes the Pos Damkar (cells 48-53 x 84-87, door east) with its fire
engine, and vcxn.mx himself is the Komandan Damkar. Payoff: the engine 'puts out' the fish grill by the pier (bakarikan, (1, 34)).
Cameos: @joe.harry88 as an NPC by the gapura, @potasganteng_ the self-made 'ketua keuangan' at the Gedung Rapat. Reuses ep25's helpers.
"""
import asyncio, sys, os, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'lib'))
from harness import *
_sp = importlib.util.spec_from_file_location('ep25shots', os.path.join(HERE, '..', 'ep25', 'shots.py')); E25 = importlib.util.module_from_spec(_sp); _sp.loader.exec_module(E25)
BASE, NPC, EXTRA = E25.BASE, E25.NPC, E25.EXTRA
EP28 = """const P = window.__pulau;
  window.__C = (x, y, z) => { window.__camTarget = new window.__pulau.cam.target.constructor(x, y, z); };
  window.__D = () => P.npcs.filter(n => n.demo);
  window.__plain = () => P.npcs.filter(n => !n.demo && !n.castSpot && n.num && !n.pres && !n.vp && !n.aru && !n.cloud && !n.kit && !n.tool && !n.cand && !n.candSign);
  window.__V = () => window.__N('vcxn.mx');
  window.__truckObj = () => window.__bld('posdamkar').userData.truck;
  window.__truckHome = null;
  window.__truck = (x, z, yaw, flash, spray, T) => { const t = window.__truckObj(); if (!window.__truckHome) { window.__truckHome = [t.parent, t.position.clone(), t.rotation.y]; P.roads.parent.attach(t); }
    t.position.set(x, P.WD.groundY(x, z) + .02, z); t.rotation.set(0, yaw, 0); const L = t.userData.lights; L[0].visible = !flash || Math.sin(T * 14) > 0; L[1].visible = !flash || Math.sin(T * 14) <= 0;
    const S = t.userData.spray; S.visible = !!spray; if (spray) S.children.forEach((d, i) => { const s = ((T * 1.7 + i / S.children.length) % 1), w = ((i * 37) % 11 - 5) / 5; d.position.set(w * .1 * s * 2, .02 + s * .55 - s * s * 1.15, .45 + s * 1.15); }); };
  window.__truckBack = () => { const h = window.__truckHome; if (!h) return; const t = window.__truckObj(); h[0].attach(t); t.position.copy(h[1]); t.rotation.set(0, h[2], 0); t.userData.spray.visible = false; t.userData.lights.forEach(l => l.visible = true); window.__truckHome = null; };
  window.__grill = () => window.__bld('bakarikan');
  window.__fx = null;
  window.__fxInit = async () => { if (window.__fx) return; const THREE = await import('three'); const g = new THREE.Group(); P.roads.parent.add(g);
    const sm = new THREE.MeshStandardMaterial({ color: '#cfd2d4', transparent: true, opacity: .55, depthWrite: false, flatShading: true }), wm = new THREE.MeshStandardMaterial({ color: '#cfefff', emissive: '#7fc8ff', emissiveIntensity: .4, transparent: true, opacity: .85, depthWrite: false });
    const smoke = [], drops = []; for (let i = 0; i < 10; i++) { const m = new THREE.Mesh(new THREE.IcosahedronGeometry(1, 0), sm); g.add(m); smoke.push(m); }
    for (let i = 0; i < 18; i++) { const m = new THREE.Mesh(new THREE.SphereGeometry(1, 6, 4), wm); m.scale.setScalar(.035); g.add(m); drops.push(m); }
    const broom = new THREE.Group(); const st = new THREE.Mesh(new THREE.BoxGeometry(1, 1, 1), new THREE.MeshStandardMaterial({ color: '#a9784a', flatShading: true })); st.scale.set(1.3, .04, .04); broom.add(st);
    const hd = new THREE.Mesh(new THREE.BoxGeometry(1, 1, 1), new THREE.MeshStandardMaterial({ color: '#d9b45a', flatShading: true })); hd.scale.set(.12, .3, .1); hd.position.x = .7; broom.add(hd); g.add(broom);
    const sacks = []; for (let i = 0; i < 2; i++) { const s = new THREE.Mesh(new THREE.DodecahedronGeometry(1, 0), new THREE.MeshStandardMaterial({ color: '#d8c49a', flatShading: true })); s.scale.set(.3, .22, .24); s.castShadow = true; g.add(s); sacks.push(s); }
    window.__fx = { g, smoke, drops, broom, sacks }; window.__fxOff(); };
  window.__fxOff = () => { const f = window.__fx; if (!f) return; f.smoke.concat(f.drops, f.sacks).forEach(m => m.visible = false); f.broom.visible = false; };
  window.__smoke = (x, y, z, T, k = 1) => window.__fx.smoke.forEach((m, i) => { const s = ((T * .45 + i / 10) % 1); m.visible = true; m.position.set(x + Math.sin(i * 2.1 + T) * .25 * s, y + s * 2.6 * k, z + Math.cos(i * 1.7) * .2 * s); m.scale.setScalar((.18 + s * .5) * k); });
  window.__drip = (x, y, z, T) => window.__fx.drops.forEach((m, i) => { const s = ((T * 1.3 + i / 18) % 1), a = i * 2.4; m.visible = true; m.position.set(x + Math.cos(a) * (.3 + (i % 3) * .25), y - s * y, z + Math.sin(a) * (.3 + (i % 3) * .2)); });
  window.__flames = on => { const f = window.__grill().userData.flames; if (f) f.visible = on; };
  window.__helmet = async n => { if (n.helmet) return; const M = await import('/src/models.js'); const b = n.obj.userData.body, k = b.children.length; M.castKit(n.obj, 'damkar'); n.helmet = b.children.slice(k); };"""
GX, GZ = 1.0, 34.0            # the fish grill (bakarikan) by the pier
LX, LZ = -10.5, 7.5           # centre of the Lapangan Gotong Royong (its name board at z ~ 10.8)
JX, JZ = -3.5, 24.5           # joe.harry88's NPC spot by the gapura
# c1 cold open: the fire engine sprays the smoking fish grill, Komandan Damkar @vcxn.mx pointing: 'Ada asap! Semprooot!'
C1 = """async () => { await window.__fxInit(); const P = window.__pulau, v = window.__V(), s = window.__plain()[0]; window.__fix(v); window.__clock = .3; window.__cheer = null; P.player.obj.visible = false;
  window.__look(-.2, 34.4, -.75, .16, 4.3, false); window.__hideInst([[-2.6, 37.2], [-1.8, 36.4]], 2.2);
  window.__beforeRender = (dt, T) => { window.__keep([v, s], -.3, 34.4, 5); window.__truck(-1.45, 33.7, PI / 2, true, T > .35, T); window.__smoke(%s, .9, %s, T, T > 1.2 ? .6 : 1);
    window.__z0(v); window.__pose(v, -.55, 35.0, .9, T < 1.0 ? 'point' : 'panic', T); window.__pose(s, 1.6, 35.1, -1.9, 'panic', T);
    window.__C(-.1, P.WD.groundY(-.25, 34.6) + 1.0, 34.5); P.cam.dist = Math.max(3.7, 4.3 - T * .25); P.cam.yaw = -.75; }; }""" % (GX, GZ)
# c2 premise: aerial glide from the town onto the Lapangan Gotong Royong
C2 = """() => { const P = window.__pulau; window.__clock = .3; window.__cheer = null; P.player.obj.visible = false; window.__truckBack(); window.__fxOff();
  window.__look(-4, 2, .35, .95, 34, false);
  window.__beforeRender = (dt, T) => { const k = Math.min(1, T / 3.2), e = k * k * (3 - 2 * k); window.__C(-4 + (%s + 4) * e, 0, 2 + (%s - 2) * e); P.cam.dist = 34 - 21 * e; P.cam.pitch = .95 - .3 * e; P.cam.yaw = .35 - .1 * e; }; }""" % (LX, LZ)
# c3 the president at the field's name board: 'Ini jatah terakhirku sebagai presiden. Bikin lapangan... buat gotong royong!'
C3 = """() => { const P = window.__pulau, pr = window.__PR(); window.__clock = .3; window.__cheer = null; P.player.obj.visible = false;
  const px = %s - 1.75, pz = %s + 3.75; window.__look(px + .6, pz, .3, .1, 3.6, false); window.__hideInst([[px + .6, pz + 1.2], [px + 1.2, pz + .6]], 1.8);
  window.__beforeRender = (dt, T) => { window.__keep([pr].concat(window.__D()), px, pz, 1.6); window.__pose(pr, px, pz, .25, T < 2.6 ? 'talk' : (T < 3.6 ? 'point' : 'cheer'), T);
    window.__C(px + .55, P.WD.groundY(px, pz) + 1.15, pz); P.cam.dist = Math.max(3.0, 3.6 - T * .14); P.cam.yaw = .3 + T * .02; }; }""" % (LX, LZ)
# c4 the whole island at kerja bakti on the new field (event workers with brooms, hoes and sacks)
C4 = """() => { const P = window.__pulau; window.__clock = .3; window.__cheer = null; P.player.obj.visible = false;
  window.__look(%s, %s, .2, .85, 10, false);
  window.__beforeRender = (dt, T) => { window.__C(%s + .3, .4, %s + .4); P.cam.dist = Math.max(7.5, 10.5 - T * .6); P.cam.yaw = .2 + T * .05; P.cam.pitch = .85 - T * .03; }; }""" % (LX, LZ, LX, LZ)
# c5 Alexandre si pahlawan carries two sacks at once across the field: 'Serahkan padaku! Dua karung sekaligus!'
C5 = """async () => { await window.__fxInit(); const P = window.__pulau, a = window.__N('Alexandre'); window.__fix(a); window.__clock = .3; window.__cheer = null; P.player.obj.visible = false;
  window.__look(%s - 2, %s - .5, .5, .12, 3.2, false);
  window.__beforeRender = (dt, T) => { const x = %s - 3.2 + T * .55, z = %s - .5; window.__keep([a], x, z, 4); window.__z0(a); window.__pose(a, x, z, PI / 2, 'walk', T); const u = a.obj.userData; u.armL.rotation.x = u.armR.rotation.x = -2.75; u.armL.rotation.z = .3; u.armR.rotation.z = -.3;
    const [s1, s2] = window.__fx.sacks, y = a.obj.position.y + 1.55; s1.visible = s2.visible = true; s1.position.set(x, y, z - .28); s2.position.set(x, y + .02, z + .28); s1.rotation.y = .3; s2.rotation.y = -.4;
    window.__C(x + .2, P.WD.groundY(x, z) + 1.05, z); P.cam.dist = Math.max(2.7, 3.2 - T * .15); }; }""" % (LX, LZ, LX, LZ)
# c6 Luci si sok tahu gives the wrong instructions while a resident sweeps the dust straight into the air
C6 = """async () => { await window.__fxInit(); const P = window.__pulau, l = window.__N('Luci Ardiansyah'), w = window.__plain()[1]; window.__fix(l); window.__clock = .3; window.__cheer = null; P.player.obj.visible = false; window.__fxOff();
  const lx = %s + 1.6, lz = %s - .6; window.__look(lx + .5, lz, -.25, .12, 3.2, false);
  window.__beforeRender = (dt, T) => { window.__keep([l, w], lx, lz, 4); window.__z0(l); window.__pose(l, lx, lz, -.35, T < 1.7 ? 'point' : 'talk', T); window.__z0(w); window.__pose(w, lx + 1.0, lz - .35, -.3, 'still', T);
    const u = w.obj.userData, k = Math.sin(T * 7); u.armL.rotation.x = -2.0 + k * .5; u.armR.rotation.x = -2.2 + k * .5; const b = window.__fx.broom; b.visible = true; b.position.set(lx + 1.0, w.obj.position.y + 1.45 + k * .25, lz - .1); b.rotation.set(0, .3, 1.15 + k * .3);
    window.__smoke(lx + 1.0, w.obj.position.y + 1.8, lz - .1, T, .45); window.__C(lx + .5, P.WD.groundY(lx, lz) + 1.05, lz); P.cam.dist = Math.max(2.8, 3.2 - T * .1); }; }""" % (LX, LZ)
# c7 Klub Pertama: D..A..B..Y and princes_nay both pull the same broom: 'Aku yang pertama nyapu!' / 'Aku princess...'
C7 = """async () => { await window.__fxInit(); const P = window.__pulau, d = window.__N('D..A..B..Y a..j..a'), p = window.__N('princes_nay'); window.__fix(d); window.__fix(p); window.__clock = .3; window.__cheer = null; P.player.obj.visible = false; window.__fxOff();
  const cx = %s - 1.8, cz = %s + 1.2; window.__look(cx, cz, -.12, .14, 3.6, false);
  window.__beforeRender = (dt, T) => { window.__keep([d, p], cx, cz, 3.2); const k = Math.sin(T * 6) * .07, who = T < 1.9; window.__z0(d); window.__z0(p);
    window.__pose(d, cx - .5 + k, cz, PI / 2 - .5, 'still', T); window.__pose(p, cx + .5 + k, cz, -PI / 2 + .5, 'still', T);
    for (const n of [d, p]) { const u = n.obj.userData; u.armL.rotation.x = u.armR.rotation.x = -1.45; u.body.rotation.x = -.18; }
    (who ? d : p).obj.userData.body.position.y = Math.abs(Math.sin(T * 9)) * .06;
    const b = window.__fx.broom; b.visible = true; b.position.set(cx - .35 + k, d.obj.position.y + .95, cz + .2); b.rotation.set(0, 0, 0);
    window.__C(cx + k * .5, P.WD.groundY(cx, cz) + 1.0, cz); P.cam.dist = Math.max(3.0, 3.6 - T * .15); P.cam.yaw = -.12 + (who ? 0 : -.12) * Math.min(1, T - 1.9); }; }""" % (LX, LZ)
# c8 Aru in front of the new Pos Damkar, Komandan vcxn.mx saluting by the engine: 'Siap! Pos Damkar Pulau Aru, lengkap dengan mobilnya!'
C8 = """() => { const P = window.__pulau, v = window.__V(); window.__fix(v); window.__clock = .3; window.__cheer = null; window.__fxOff(); window.__truckBack(); window.__flames(true);
  window.__look(-1.6, 30.3, .95, .16, 4.4, false);
  window.__beforeRender = (dt, T) => { window.__keep([v], -2.2, 30.4, 4); window.__aru(-1.6, 30.0, 1.1, T > 2.6, T); window.__z0(v); window.__pose(v, -2.45, 31.25, 1.45, 'still', T); const u = v.obj.userData; if ((T % 3) < 1.3) { u.armR.rotation.x = -2.7; u.armR.rotation.z = -.6; }
    window.__C(-2.2, P.WD.groundY(-2.9, 30.3) + 1.3, 30.3); P.cam.dist = Math.max(3.6, 4.4 - T * .15); P.cam.yaw = .95 + T * .025; }; }"""
# c9 the engine races down the main street, lights flashing: 'Lapor! Asap di dekat dermaga! Meluncur!'
C9 = """async () => { await window.__fxInit(); const P = window.__pulau; window.__clock = .3; window.__cheer = null; P.player.obj.visible = false; window.__fxOff();
  window.__look(-1.0, 26, -.4, .14, 5, false); window.__hidB = []; P.roads.parent.traverse(o => { if (o.userData && o.userData.b && o.userData.b.type === 'lampusemangat' && o.userData.b.x === 53) { o.visible = false; window.__hidB.push(o); } }); window.__hideInst([[-2.6, 22], [-2.6, 26], [-2.6, 30], [-2.6, 34]], 2.2);
  window.__beforeRender = (dt, T) => { const z = 22.5 + T * 2.3; window.__truck(-1.05, z, 0, true, false, T); window.__keep([], -1.0, z, 3.5);
    window.__C(-1.0, P.WD.groundY(-1, z) + .9, z + .4); P.cam.dist = 4.6 - Math.min(1, T * .3) * .8; P.cam.yaw = -.45 + T * .08; }; }"""
# c10 payoff: the grill soaked, the fish dripping, the seller: 'Pak... ini ikan BAKAR. Bukan kebakaran!' / vcxn: '...Oh. Maaf. Terlalu semangat.'
C10 = """async () => { await window.__fxInit(); const P = window.__pulau, v = window.__V(), s = window.__plain()[0]; window.__fix(v); window.__clock = .3; window.__cheer = null; P.player.obj.visible = false; window.__fxOff(); window.__flames(false);
  window.__look(.5, 32.8, 3.1, .15, 3.0, false); window.__board = null; P.roads.parent.traverse(o => { if (o.userData && o.userData.b && o.userData.b.type === 'papanjadwal' && o.userData.b.x === 56) { window.__board = o; o.visible = false; } });
  window.__beforeRender = (dt, T) => { window.__keep([v, s], .5, 35.5, 5); window.__truck(-1.45, 33.7, PI / 2, false, false, T); window.__drip(%s, 1.9, %s, T); window.__smoke(%s, .75, %s, T, .25);
    window.__z0(s); window.__z0(v); window.__pose(s, 1.0, 32.75, PI - .3, T < 3.1 ? 'talk' : 'still', T); window.__pose(v, .05, 32.85, PI + .35, 'still', T); const u = v.obj.userData; if (T > 3.2) { u.armR.rotation.x = -2.6; u.armR.rotation.z = -.5 + Math.sin(T * 10) * .08; v.obj.rotation.y = PI + .35 - Math.min(.35, (T - 3.2) * .6); }
    window.__C(T < 3.1 ? .65 : .35, P.WD.groundY(.5, 33) + 1.05, 32.8); P.cam.dist = T < 3.1 ? Math.max(3.1, 3.6 - T * .15) : 3.1; P.cam.yaw = T < 3.1 ? 3.0 : 3.25; P.cam.pitch = .15; }; }""" % (GX, GZ, GX, GZ)
# c11 @joe.harry88 asked to be an NPC: Aru greets him, he only ever says one line
C11 = """() => { const P = window.__pulau, j = window.__N('joe.harry88'); window.__fix(j); window.__clock = .3; window.__cheer = null; window.__fxOff(); window.__flames(true); window.__truckBack();
  window.__look(%s + .55, %s, 3.0, .12, 3.4, false); P.player.obj.visible = true; window.__hideInst([[%s + .5, %s - 1.2], [%s + .5, %s - 2.4]], 2.0);
  window.__beforeRender = (dt, T) => { window.__keep([j], %s + .5, %s, 4); window.__aru(%s + .95, %s + .1, -PI / 2 - .55, T < 1.3 || (T > 3.6 && T < 4.3), T); window.__z0(j);
    const say = (T > 1.4 && T < 3.5) || T > 4.4; window.__pose(j, %s, %s, PI / 2 + .55, 'still', T); const u = j.obj.userData; if (say && ((T - 1.4) %% 3) < .8) { u.armR.rotation.x = -2.6; u.armR.rotation.z = .25 * Math.sign(Math.sin(T * 14)); }
    window.__C(%s + .48, P.WD.groundY(%s, %s) + 1.08, %s); P.cam.dist = T > 4.4 ? Math.max(2.5, 3.4 - (T - 4.4) * .5) : 3.4; P.cam.yaw = 3.0; }; }""" % (JX, JZ, JX, JZ, JX, JZ, JX, JZ, JX, JZ, JX, JZ, JX, JX, JZ, JZ)
# c12 @potasganteng_ declares himself 'ketua keuangan' in front of the Gedung Rapat; the real Menteri Keuangan walks up with her calculator
C12 = """() => { const P = window.__pulau, p = window.__N('potasganteng_'), a = window.__N('araa_yinchan'); window.__fix(p); window.__fix(a); window.__clock = .3; window.__cheer = null; P.player.obj.visible = false;
  const px = -15.2, pz = -4.0; window.__look(px - .6, pz, .5, .18, 3.6, false);
  window.__beforeRender = (dt, T) => { window.__keep([p, a], px - .6, pz, 4); window.__z0(p); window.__pose(p, px, pz, -.35, T < 2.1 ? 'cheer' : 'still', T); if (T >= 2.1) { const u = p.obj.userData; u.armL.rotation.x = u.armR.rotation.x = -1.35; u.armL.rotation.z = .45; u.armR.rotation.z = -.45; }
    const ax = px - 1.35, az = pz - Math.max(0, 1.3 - T * .8); window.__z0(a); window.__pose(a, ax, az, .35, T < 1.6 ? 'walk' : 'point', T);
    window.__C(px - .65, P.WD.groundY(px, pz) + 1.05, pz); P.cam.dist = Math.max(3.0, 3.6 - T * .15); P.cam.yaw = .5; }; }"""
# c13 end: dusk over the finished field, everyone cheering, Aru in the middle: 'Pulau ini butuh apa lagi? Tulis di komentar!'
C13 = """() => { const P = window.__pulau; window.__clock = .56; window.__cheer = true;
  window.__look(%s, %s + 1.5, 2.7, .3, 4.5, false);
  window.__beforeRender = (dt, T) => { window.__aru(%s, %s - .4, PI - .45, T < 2.4, T); const u = P.player.obj.userData; if (T > 2.4 && u.armR) { u.armR.rotation.x = u.armL.rotation.x = -2.8 + Math.sin(T * 9) * .2; }
    window.__D().forEach((n, i) => { const o = n.obj.userData; o.armL.rotation.x = o.armR.rotation.x = -2.8 + Math.sin(T * 10 + i) * .2; o.body.position.y = Math.abs(Math.sin(T * 6 + i)) * .08; });
    window.__C(%s, P.WD.groundY(%s, %s) + 1.0 + T * .1, %s - .6); P.cam.yaw = 2.7; P.cam.dist = 4.0 + T * 1.6; P.cam.pitch = Math.min(.85, .3 + T * .09); }; }""" % (LX, LZ, LX, LZ, LX, LX, LZ, LZ)
SHOTS = {'c1': (C1, 80), 'c2': (C2, 100), 'c3': (C3, 160), 'c4': (C4, 155), 'c5': (C5, 100), 'c6': (C6, 115), 'c7': (C7, 150),
         'c8': (C8, 200), 'c9': (C9, 115), 'c10': (C10, 230), 'c11': (C11, 200), 'c12': (C12, 155), 'c13': (C13, 150)}
CLEAR = "() => { window.__showInst(); window.__cheer = null; window.__camTarget = null; window.__beforeRender = null; window.__clock = null; window.__tourS = null; window.__fxOff && window.__fxOff(); if (window.__board) { window.__board.visible = true; window.__board = null; } (window.__hidB || []).forEach(o => o.visible = true); window.__hidB = []; }"
async def run(which):
    async with async_playwright() as p:
        b, pg = await setup(p)
        await pg.evaluate(BASE); await pg.evaluate("() => { " + NPC + " }"); await pg.evaluate("() => { " + EXTRA + " }"); await pg.evaluate("() => { " + EP28 + " }")
        for k, (js, n) in SHOTS.items():
            if k in which and 'prev' not in which:
                await shoot(pg, 'e28' + k, int(os.environ.get('N_' + k, n)), start_js=js, warm=12)
                await pg.evaluate(CLEAR)
        if 'prev' in which:
            for k, (js, n) in SHOTS.items():
                if 'all' not in which and k not in which: continue
                await shoot(pg, 'p28' + k, 1, start_js=js, warm=int(os.environ.get('WARM', '40')))
                await pg.evaluate(CLEAR)
        await b.close()
if __name__ == "__main__": asyncio.run(run(sys.argv[1].split(",")))
