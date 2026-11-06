"""Episode 13 "Demo Warga" shot list.  usage: DPR=2 python3 shots.py c1,c3,...  (DPR=1 + prev for checks)
World: stage (mimbar) cells 53..55 x 44..46, centre (-1.5, -10.5), faces south; main street world x -2..0.
Rumah Presiden cells 49..51 x 47..50 (r3, faces east); spanduk 'PEMILU SEKARANG!' cell 52 x 49..50, cloth faces east at x ~ -3.5, z -6.
Warung Fahmi cells 64..67 x 74..76, centre (10, 19.5), faces south; seats local [x,.4,z] back bench z -.1 (face +z), scale 1.5.
Kantor Pulau cells 76..79 x 48..50, centre (22, -6.5), faces south; desk seats local (+-.68, .36, .18), scale 1.6.
Kedai kopi centre (-9.5, -1) faces north.
"""
import asyncio, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'lib'))
from harness import *
BASE = """async () => { const P = window.__pulau; window.PI = Math.PI;
  window.__look = (x, z, yaw, pitch, dist, show) => { const pl = P.player; pl.x = x; pl.z = z; pl.tx = null; pl.vy = 0; pl.obj.visible = !!show; P.cam.yaw = yaw; P.cam.pitch = pitch; P.cam.dist = dist; P.cam.target.set(x, 1, z); };
  window.__W = () => { const a = P.npcs.filter(n => n.role === 'wander' && n.num), b = P.npcs.filter(n => !a.includes(n) && !n.aru && !n.pres && !n.vp && !n.cloud); return a.concat(b); };
  window.__VP = () => P.npcs.find(n => n.vp); window.__PR = () => P.npcs.find(n => n.pres);
  const scene = P.roads.parent; let wp = null; scene.traverse(o => { if (o.userData && o.userData.b && o.userData.b.type === 'waterpark') wp = o; });
  window.__wpL = (lx, ly, lz) => [wp.position.x + lx, wp.position.y + ly, wp.position.z + lz];
  window.__bld = type => { let r = null; P.roads.parent.traverse(o => { if (!r && o.userData && o.userData.b && o.userData.b.type === type) r = o; }); return r; };
  window.__seatW = (type, lx, ly, lz) => { const o = window.__bld(type), s = o.userData.def.scale || 1; o.updateMatrixWorld(true); const v = o.localToWorld(new (P.cam.target.constructor)(lx * s, ly * s, lz * s)); return [v.x, v.y, v.z]; };
  window.__signs = [];
  window.__placard = async (n, text, col) => { const THREE = await import('three'); const c = document.createElement('canvas'); c.width = 256; c.height = 160; const x = c.getContext('2d');
    x.fillStyle = col || '#fff8e6'; x.fillRect(0, 0, 256, 160); x.strokeStyle = '#3a2412'; x.lineWidth = 8; x.strokeRect(4, 4, 248, 152);
    x.fillStyle = '#c0392b'; x.textAlign = 'center'; x.textBaseline = 'middle'; const w = text.split('|'); let fs = 52; x.font = `700 ${fs}px "Pixelify Sans", sans-serif`;
    while (fs > 22 && Math.max(...w.map(t => x.measureText(t).width)) > 236) { fs -= 2; x.font = `700 ${fs}px "Pixelify Sans", sans-serif`; }
    w.forEach((t, i) => x.fillText(t, 128, 80 + (i - (w.length - 1) / 2) * fs * 1.1));
    const tx = new THREE.CanvasTexture(c); tx.colorSpace = THREE.SRGBColorSpace; const g = new THREE.Group();
    const board = new THREE.Mesh(new THREE.PlaneGeometry(.62, .39), new THREE.MeshStandardMaterial({ map: tx, side: THREE.DoubleSide })); board.position.set(0, 2.05, .12); g.add(board);
    const stick = new THREE.Mesh(new THREE.BoxGeometry(.03, .9, .03), new THREE.MeshStandardMaterial({ color: '#8a6a3a' })); stick.position.set(0, 1.5, .1); g.add(stick);
    n.obj.add(g); window.__signs.push(g); return g; };
  window.__clearSigns = () => { for (const g of window.__signs) if (g.parent) g.parent.remove(g); window.__signs = []; };
  let _br = null; Object.defineProperty(window, '__beforeRender', { configurable: true, get() { return _br; }, set(f) { if (!f) { _br = null; return; } let s0 = null; _br = (dt, T) => { if (s0 === null) s0 = T; return f(dt, T - s0 - .4); }; } });
  window.__time = want => { const lab = document.getElementById('time-label'), btn = document.getElementById('b-time'); for (let i = 0; i < 4 && !lab.textContent.includes(want); i++) btn.click(); };
  window.__poseY = (n, x, y, z, face, pose, T) => { n.x = x; n.z = z; n.tx = null; n.wait = 99; n.obj.visible = true; n.obj.position.set(x, y, z); n.obj.rotation.y = face; const u = n.obj.userData;
    u.legL.rotation.x = u.legR.rotation.x = 0; u.armL.rotation.x = u.armR.rotation.x = -.15; u.body.position.y = 0; u.body.rotation.z = 0;
    if (pose === 'eat') { u.armR.rotation.x = -1.3 + Math.sin(T * 8) * .45; u.armL.rotation.x = -.8; }
    if (pose === 'reach') { u.armR.rotation.x = -1.2 + Math.sin(T * 3) * .15; u.armL.rotation.x = -.2; u.body.rotation.z = Math.sin(T * 2.5) * .06; }
    if (pose === 'talk') { u.armR.rotation.x = -1.1 + Math.sin(T * 7) * .4; u.armL.rotation.x = -.6 + Math.sin(T * 5) * .2; }
    if (pose === 'point') { u.armR.rotation.x = -1.55 + Math.sin(T * 10) * .08; u.armL.rotation.x = -.3; }
    if (pose === 'panic') { u.armR.rotation.x = -2.2 + Math.sin(T * 14) * .5; u.armL.rotation.x = -2.2 - Math.sin(T * 14) * .5; u.body.position.y = Math.abs(Math.sin(T * 9)) * .05; }
    if (pose === 'wave') { u.armR.rotation.x = -2.6 + Math.sin(T * 9) * .35; u.armL.rotation.x = -.3; }
    if (pose === 'cheer') { u.armR.rotation.x = u.armL.rotation.x = -2.8 + Math.sin(T * 10) * .2; u.body.position.y = Math.abs(Math.sin(T * 6)) * .08; }
    if (pose === 'swim') { u.armR.rotation.x = -1.6 + Math.sin(T * 6) * .5; u.armL.rotation.x = -1.6 - Math.sin(T * 6) * .5; }
    if (pose === 'sit' || pose === 'sittalk' || pose === 'yawn' || pose === 'sleep' || pose === 'sipcup') { u.legL.rotation.x = u.legR.rotation.x = -1.45; }
    if (pose === 'sittalk') { u.armR.rotation.x = -1.1 + Math.sin(T * 7) * .4; u.armL.rotation.x = -.6 + Math.sin(T * 5) * .2; }
    if (pose === 'yawn') { u.armR.rotation.x = u.armL.rotation.x = -2.9 + Math.sin(T * 2) * .1; u.body.rotation.z = Math.sin(T * 1.5) * .08; }
    if (pose === 'sleep') { u.armR.rotation.x = u.armL.rotation.x = -.1; u.body.rotation.z = .32 + Math.sin(T * 1.6) * .03; u.body.position.y = Math.sin(T * 1.6) * .015; }
    if (pose === 'sipcup') { u.armR.rotation.x = -1.6 + Math.sin(T * 1.2) * .25; u.armL.rotation.x = -.9; }
    if (pose === 'strike') { u.armR.rotation.x = -1.7 + Math.abs(Math.sin(T * 9)) * .9; u.armL.rotation.x = -.4; }
    if (pose === 'sitcup' || pose === 'eatsit' || pose === 'type') { u.legL.rotation.x = u.legR.rotation.x = -1.45; }
    if (pose === 'sitcup') { u.armR.rotation.x = -1.6 + Math.sin(T * 1.2) * .25; u.armL.rotation.x = -.9; }
    if (pose === 'eatsit') { u.armR.rotation.x = -1.3 + Math.sin(T * 8) * .45; u.armL.rotation.x = -.8; }
    if (pose === 'type') { u.armR.rotation.x = -1.2 + Math.sin(T * 14) * .12; u.armL.rotation.x = -1.2 - Math.sin(T * 13) * .12; }
    if (pose === 'walk') { u.legL.rotation.x = Math.sin(T * 7) * .5; u.legR.rotation.x = -Math.sin(T * 7) * .5; u.armL.rotation.x = -Math.sin(T * 7) * .4; u.armR.rotation.x = Math.sin(T * 7) * .4; } };
  window.__pose = (n, x, z, face, pose, T, dy = 0) => window.__poseY(n, x, P.WD.groundY(x, z) + dy, z, face, pose, T);
  window.__hideNear = (x, z, r, keep) => { for (const n of P.npcs) if (!keep.includes(n)) n.obj.visible = Math.hypot(n.x - x, n.z - z) > r; };
}"""
V = "new window.__pulau.cam.target.constructor"
G = "window.__pulau.WD.groundY"
SIGNS = ['PEMILU!', 'PRESIDEN|DIPILIH WARGA', 'GORENGAN|DIBAYAR!', 'RONDA|JANGAN TIDUR', 'MANGGA|MILIK LADANG', 'SUARA|WARGA!', 'PEMILU|SEKARANG', 'KAMI|MAU MEMILIH']
# a protest crowd on the main street south of the stage, facing north (toward the stage), holding placards
CROWD = f"""const W = window.__W(); window.__clearSigns(); const spots = [[-2.3, -6.3], [-1.4, -6.5], [-.5, -6.3], [.4, -6.5], [-1.9, -5.5], [-1.0, -5.6], [-.1, -5.5], [.8, -5.4]];
  for (let i = 0; i < 8; i++) await window.__placard(W[i], {SIGNS!r}[i], i % 3 ? '#fff8e6' : '#ffe08a');
  window.__crowd = (T, pose) => {{ for (let i = 0; i < 8; i++) {{ const [x, z] = spots[i]; window.__pose(W[i], x, z, Math.PI + (i % 3 - 1) * .15, pose(i), T + i * .6); }} }};"""
# c1 cold open: the crowd shouting, close from the stage side
C1 = f"""async () => {{ const P = window.__pulau; window.__time('siang'); window.__cheer = true; {CROWD}
  window.__look(-1.0, -6.0, Math.PI + .12, .12, 3.0, false); window.__camTarget = {V}(-1.0, {G}(-1, -6.0) + 1.45, -6.0);
  window.__beforeRender = (dt, T) => {{ window.__crowd(T, i => 'cheer'); P.cam.dist -= dt * .15; }}; }}"""
# c3 Warung Fahmi reveal: two residents eating on the back bench, camera from the street
C3 = f"""() => {{ const P = window.__pulau, W = window.__W(); window.__time('siang'); window.__clearSigns();
  const a = window.__seatW('warungfahmi', -.62, .4, -.1), b = window.__seatW('warungfahmi', .62, .4, -.1);
  window.__look(10, 20.2, .35, .32, 7.5, false); window.__camTarget = {V}(10, a[1] + .7, 20.0);
  window.__beforeRender = (dt, T) => {{ window.__hideNear(10, 19.5, 5, [W[8], W[9]]); window.__poseY(W[8], a[0], a[1] - .45 + .03, a[2], 0, 'sitcup', T); window.__poseY(W[9], b[0], b[1] - .45 + .03, b[2], 0, 'eatsit', T + 1);
    P.cam.yaw -= dt * .1; P.cam.dist -= dt * .5; }}; }}"""
# c4 Aru (the player) at Warung Fahmi with a plate of nasi goreng
C4 = f"""() => {{ const P = window.__pulau, W = window.__W(); window.__time('siang'); const s = window.__seatW('warungfahmi', 0, .4, -.1);
  window.__look(s[0], s[2], .25, .16, 2.4, true); P.kerja.__sit('warungfahmi', 1, 'nasgor'); window.__camTarget = {V}(s[0], s[1] + .55, s[2] + .1);
  window.__beforeRender = (dt, T) => {{ window.__hideNear(10, 19.5, 5, []); P.cam.dist -= dt * .1; }}; }}"""
# c5 Kantor Pulau reveal from the cross street
C5 = f"""() => {{ const P = window.__pulau, W = window.__W(); window.__time('siang'); if (P.kerja.sitting()) P.kerja.stand(); P.player.obj.visible = false;
  window.__look(22, -6, .2, .28, 7.5, false); window.__camTarget = {V}(22, {G}(22, -6.5) + 1.8, -6.2);
  window.__beforeRender = (dt, T) => {{ window.__hideNear(22, -6, 5, [W[10]]); const s = window.__seatW('kantor', .68, .36, .18); window.__poseY(W[10], s[0], s[1] - .45 + .03, s[2], 0, 'type', T); P.cam.yaw -= dt * .08; P.cam.dist -= dt * .45; }}; }}"""
# c6 the vice president at a kantor desk, typing, then turning to camera
C6 = f"""() => {{ const P = window.__pulau, vp = window.__VP(), W = window.__W(); window.__time('siang'); P.player.obj.visible = false; const s = window.__seatW('kantor', -.68, .36, .18);
  window.__look(s[0], s[2], .3, .14, 2.5, false); window.__camTarget = {V}(s[0], s[1] + .6, s[2] + .15);
  window.__beforeRender = (dt, T) => {{ window.__hideNear(22, -6, 5, [vp]); window.__poseY(vp, s[0], s[1] - .45 + .03, s[2], T < 1.2 ? 0 : .35, T < 1.2 ? 'type' : 'sittalk', T); P.cam.dist -= dt * .08; }}; }}"""
# c7 residents at the kedai kopi keeping a list of the president's mistakes
C7 = f"""() => {{ const P = window.__pulau, W = window.__W(); window.__time('siang'); P.player.obj.visible = false;
  window.__look(-9.4, -2.4, Math.PI + .12, .18, 3.0, false); window.__camTarget = {V}(-9.4, {G}(-9.4, -2.4) + 1.1, -2.4);
  window.__beforeRender = (dt, T) => {{ window.__hideNear(-9.5, -2, 4.5, [W[11], W[12], W[13]]); window.__pose(W[11], -9.4, -2.55, Math.PI + .3, 'talk', T); window.__pose(W[12], -10.2, -2.3, Math.PI - .6, 'idle', T + 1); window.__pose(W[13], -8.6, -2.25, Math.PI + .9, T > 3.6 ? 'point' : 'idle', T + 2);
    P.cam.dist -= dt * .12; }}; }}"""
# c8 night: Aru reads the letter under a Lampu Semangat on the main street
C8 = f"""() => {{ const P = window.__pulau, pl = P.player; window.__time('malam'); window.__clearSigns(); const x = -1.85, z = 7.9;
  window.__look(x, z, .5, .12, 2.6, true); window.__camTarget = {V}(x - .1, {G}(x, z) + 1.15, z);
  window.__beforeRender = (dt, T) => {{ window.__hideNear(x, z, 3.5, []); pl.x = x; pl.z = z; pl.tx = null; const u = pl.obj.userData; pl.obj.rotation.y = .5; u.armR.rotation.x = -1.25 + Math.sin(T * 1.5) * .05; u.armL.rotation.x = -1.25; P.cam.dist -= dt * .1; }}; }}"""
# c9 day: Aru on the stage telling the crowd, crowd backs in the foreground
C9 = f"""async () => {{ const P = window.__pulau, pl = P.player; window.__time('siang'); window.__cheer = null; {CROWD}
  window.__clearSigns(); const st = window.__bld('mimbar'), sy = st.position.y + .55;
  window.__look(-1.4, -10.4, 0, .26, 4.6, true); window.__camTarget = {V}(-1.3, sy + 1.0, -9.6);
  window.__beforeRender = (dt, T) => {{ window.__crowd(T, i => 'idle'); pl.x = -1.4; pl.z = -10.0; pl.tx = null; pl.y = sy; pl.vy = 0; pl.obj.position.set(-1.4, sy, -10.0); pl.obj.rotation.y = 0; const u = pl.obj.userData;
    u.armR.rotation.x = -1.1 + Math.sin(T * 7) * .4; u.armL.rotation.x = T > 2.4 ? -2.5 : -.4; P.cam.dist -= dt * .15; }}; }}"""
# c10 the crowd reacts: shock, then placards up
C10 = f"""async () => {{ const P = window.__pulau; window.__time('siang'); window.__cheer = true; P.player.obj.visible = false; {CROWD}
  window.__look(-.8, -6.0, Math.PI - .3, .32, 5.0, false); window.__camTarget = {V}(-.8, {G}(-.8, -6.0) + 1.2, -6.0);
  window.__beforeRender = (dt, T) => {{ window.__crowd(T, i => T < 1.0 ? 'panic' : 'cheer'); P.cam.dist -= dt * .4; }}; }}"""
# c11 the president in front of the 'PEMILU SEKARANG!' banner by his house, flustered
C11 = f"""() => {{ const P = window.__pulau, pr = window.__PR(); window.__time('siang'); window.__clearSigns(); window.__cheer = null; P.player.obj.visible = false; const x = -2.5, z = -6.0;
  window.__look(x, z, Math.PI / 2 + .25, .12, 3.0, false); window.__camTarget = {V}(x - .3, {G}(x, z) + 1.35, z);
  window.__beforeRender = (dt, T) => {{ window.__hideNear(x, z, 3.5, [pr]); window.__pose(pr, x, z, Math.PI / 2 + .2, T < 1.3 ? 'panic' : 'talk', T); P.cam.dist -= dt * .1; }}; }}"""
# c12 end: the crowd marches on the main street with placards, camera rises and pulls out
C12 = f"""async () => {{ const P = window.__pulau; window.__time('siang'); window.__cheer = true; P.player.obj.visible = false; {CROWD}
  window.__look(-1, -6.5, .4, .55, 7, false); window.__camTarget = {V}(-1, {G}(-1, -6.5) + 1.0, -6.5);
  window.__beforeRender = (dt, T) => {{ window.__crowd(T, i => i % 2 ? 'cheer' : 'walk'); P.cam.dist += dt * 1.5; P.cam.pitch = Math.min(1.0, P.cam.pitch + dt * .05); P.cam.yaw += dt * .05; }}; }}"""
# c13 the vice president steps in front of the crowd with his own placard
C13 = f"""async () => {{ const P = window.__pulau, vp = window.__VP(); window.__time('siang'); window.__cheer = true; P.player.obj.visible = false; {CROWD}
  await window.__placard(vp, 'AKU|DAFTAR DULUAN', '#ffe08a'); const x = -1.0, z = -6.9;
  window.__look(x, z, Math.PI + .2, .12, 2.6, false); window.__camTarget = {V}(x, {G}(x, z) + 1.4, z);
  window.__beforeRender = (dt, T) => {{ window.__crowd(T, i => 'cheer'); window.__pose(vp, x, z, Math.PI + .2, T < 1.6 ? 'talk' : 'cheer', T); P.cam.dist -= dt * .1; }}; }}"""
SHOTS = {'c1': (C1, 125), 'c3': (C3, 125), 'c4': (C4, 100), 'c5': (C5, 150), 'c6': (C6, 95), 'c7': (C7, 180), 'c8': (C8, 165),
         'c9': (C9, 140), 'c10': (C10, 95), 'c11': (C11, 105), 'c12': (C12, 265), 'c13': (C13, 100)}
CLEAR = "() => { window.__cheer = null; window.__camTarget = null; window.__beforeRender = null; }"
async def run(which):
    async with async_playwright() as p:
        b, pg = await setup(p)
        await pg.evaluate(BASE)
        for k, (js, n) in SHOTS.items():
            if k in which and 'prev' not in which:
                await shoot(pg, 'e13' + k, n, start_js=js, warm=12)
                await pg.evaluate(CLEAR)
        if 'prev' in which:
            for k, (js, n) in SHOTS.items():
                if 'all' not in which and k not in which: continue
                await shoot(pg, 'p13' + k, 1, start_js=js, warm=int(os.environ.get('WARM', '40')))
                await pg.evaluate(CLEAR)
        await b.close()
if __name__ == "__main__": asyncio.run(run(sys.argv[1].split(",")))
