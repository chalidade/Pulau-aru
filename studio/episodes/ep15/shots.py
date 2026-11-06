"""Episode 15 "Kursi Kosong" shot list.  usage: DPR=2 python3 shots.py c1,c3,...  (DPR=1 + prev for checks)
Mimbar (stage) centre (-1.5, -10.5). Papan Pemilu cells 57..59 x 50..51 (r0, faces south onto the cross street), centre (2.5, -5.0);
chairs (scale 1.3) at local (+-.5, .35) -> world (1.85 / 3.15, -4.55), seat top ~ .70 above ground.
Spanduk (52,49) world (-2.5,-6.5). Crowd = live demo residents (event.signs). President/VP still set in island.json during capture
(kit on) for c1/c2; later shots strip the kit (__unkit) because island.json makes both seats empty after this episode.
"""
import asyncio, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'lib'))
from harness import *
BASE = """async () => { const P = window.__pulau; window.PI = Math.PI;
  window.__look = (x, z, yaw, pitch, dist, show) => { const pl = P.player; pl.x = x; pl.z = z; pl.tx = null; pl.vy = 0; pl.obj.visible = !!show; P.cam.yaw = yaw; P.cam.pitch = pitch; P.cam.dist = dist; P.cam.target.set(x, 1, z); };
  window.__W = () => { const d = P.npcs.filter(n => n.demo), a = P.npcs.filter(n => !n.demo && n.role === 'wander' && n.num), b = P.npcs.filter(n => !d.includes(n) && !a.includes(n) && !n.aru && !n.pres && !n.vp && !n.cloud && !n.kit && !n.tool); return d.concat(a.filter(n => !n.kit && !n.tool), b); };
  window.__cand = on => { for (const n of P.npcs) if (n.candSign) n.candSign.visible = on; };
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
  window.__unkit = n => { if (n && n.kit) { n.obj.userData.body.remove(...n.kit); n.kit = null; } if (n && n.candSign) n.candSign.visible = false; };
  window.__hideNear = (x, z, r, keep) => { for (const n of P.npcs) if (!keep.includes(n)) n.obj.visible = Math.hypot(n.x - x, n.z - z) > r; };
}"""
V = "new window.__pulau.cam.target.constructor"
G = "window.__pulau.WD.groundY"
CROWD = """const W = window.__W(); const spots = [[-2.3, -6.3], [-1.4, -6.5], [-.5, -6.3], [.4, -6.5], [-1.9, -5.5], [-1.0, -5.6], [-.1, -5.5], [.8, -5.4]];
  window.__crowd = (T, pose) => { for (let i = 0; i < 8; i++) { const [x, z] = spots[i]; window.__pose(W[i], x, z, Math.PI + (i % 3 - 1) * .15, pose(i), T + i * .6); } };"""
# c1 cold open: the president on the stage, close, announces he quits (talk, then throws his arms up)
C1 = f"""() => {{ const P = window.__pulau, pr = window.__PR(), vp = window.__VP(); window.__time('siang'); window.__cand(false); window.__cheer = null; P.player.obj.visible = false;
  const st = window.__bld('mimbar'), sy = st.position.y + .55; const x = -1.5, z = -10.1;
  window.__look(x, z, .12, .42, 3.4, false); window.__camTarget = {V}(x + .4, sy + 1.25, z);
  window.__beforeRender = (dt, T) => {{ window.__poseY(pr, x, sy, z, 0, T < 2.6 ? 'talk' : 'panic', T); window.__poseY(vp, x + 1.0, sy, z - .5, -.3, 'idle', T); P.cam.dist = Math.max(3.0, P.cam.dist - dt * .1); }}; }}"""
# c2 the vice president, shocked, then quits too
C2 = f"""() => {{ const P = window.__pulau, pr = window.__PR(), vp = window.__VP(); window.__time('siang'); window.__cand(false); window.__cheer = null; P.player.obj.visible = false;
  const st = window.__bld('mimbar'), sy = st.position.y + .55; const x = -.6, z = -10.3;
  window.__look(x, z, .3, .4, 3.0, false); window.__camTarget = {V}(x - .2, sy + 1.25, z);
  window.__beforeRender = (dt, T) => {{ window.__poseY(vp, x, sy, z, .35, T < .9 ? 'panic' : 'talk', T); window.__poseY(pr, -1.6, sy, -10.1, .6, 'idle', T); P.cam.dist -= dt * .1; }}; }}"""
# c3 the Papan Pemilu with its two empty chairs, camera sinking from above toward the chairs
C3 = f"""() => {{ const P = window.__pulau; window.__time('siang'); window.__cand(false); window.__cheer = null; P.player.obj.visible = false; window.__unkit(window.__PR()); window.__unkit(window.__VP());
  window.__look(2.5, -4.6, -.55, .8, 7.5, false); window.__camTarget = {V}(2.5, {G}(2.5, -5) + 1.0, -4.8);
  window.__beforeRender = (dt, T) => {{ window.__hideNear(2.5, -4.5, 3.2, []); P.cam.dist = Math.max(4.2, P.cam.dist - dt * .8); P.cam.pitch = Math.max(.3, P.cam.pitch - dt * .1); }}; }}"""
# c4 the former president sits alone on the empty president's chair
C4 = f"""() => {{ const P = window.__pulau, pr = window.__PR(); window.__time('siang'); window.__cand(false); window.__cheer = null; P.player.obj.visible = false; window.__unkit(pr);
  const x = 1.85, z = -4.5, gy = {G}(2.5, -5.0);
  window.__look(x, z, -.2, .12, 2.6, false); window.__camTarget = {V}(x, gy + 1.15, z);
  window.__beforeRender = (dt, T) => {{ window.__hideNear(2.5, -4.5, 4, [pr]); window.__poseY(pr, x, gy + (window.__SITY || .28), z, -.2, T < 1.6 ? 'sit' : 'sittalk', T); P.cam.dist -= dt * .1; }}; }}"""
# c7 a resident holds up 'AKU KAK' (the shortest campaign)
C7 = f"""() => {{ const P = window.__pulau; window.__time('siang'); window.__cand(false); window.__cheer = null; P.player.obj.visible = false; window.__clearSigns();
  const W = window.__W(), n = W[12]; window.__placard(n, 'AKU|KAK'); const x = -2.6, z = -5.2;
  window.__look(x, z, Math.PI - .1, .12, 2.6, false); window.__camTarget = {V}(x, {G}(x, z) + 1.5, z);
  window.__beforeRender = (dt, T) => {{ window.__hideNear(x, z, 3, [n]); window.__pose(n, x, z, Math.PI - .1, T < 1.3 ? 'cheer' : 'idle', T); P.cam.dist -= dt * .1; }}; }}"""
# c8 Aru on the stage announces the election, crowd in front; former leaders off stage
C8 = f"""() => {{ const P = window.__pulau, pl = P.player, pr = window.__PR(), vp = window.__VP(); window.__time('siang'); window.__cand(false); window.__cheer = null; window.__clearSigns(); {CROWD}
  const st = window.__bld('mimbar'), sy = st.position.y + .55;
  window.__look(-1.4, -10.4, 0, .5, 4.2, true); window.__camTarget = {V}(-1.3, sy + 1.1, -9.8);
  window.__beforeRender = (dt, T) => {{ window.__crowd(T, i => 'idle'); pr.obj.visible = vp.obj.visible = false; pl.x = -1.4; pl.z = -10.0; pl.tx = null; pl.y = sy; pl.vy = 0; pl.obj.position.set(-1.4, sy, -10.0); pl.obj.rotation.y = 0; const u = pl.obj.userData;
    u.armR.rotation.x = -1.1 + Math.sin(T * 7) * .4; u.armL.rotation.x = T > 1.6 ? -2.5 : -.4; P.cam.dist -= dt * .15; }}; }}"""
# c9 the crowd raises their candidate placards
C9 = f"""() => {{ const P = window.__pulau, pr = window.__PR(), vp = window.__VP(); window.__time('siang'); window.__cand(false); window.__cheer = true; P.player.obj.visible = false; {CROWD}
  window.__look(-.8, -6.0, Math.PI - .3, .3, 4.2, false); window.__camTarget = {V}(-.8, {G}(-.8, -6.0) + 1.6, -6.0);
  window.__beforeRender = (dt, T) => {{ window.__crowd(T, i => 'cheer'); pr.obj.visible = vp.obj.visible = false; P.cam.dist -= dt * .35; }}; }}"""
# c10 pan across the board: candidate names, then down to the KOSONG tags
C10 = f"""() => {{ const P = window.__pulau; window.__time('siang'); window.__cand(false); window.__cheer = null; P.player.obj.visible = false; const gy = {G}(2.5, -5.0);
  window.__look(2.5, -5.2, 0, .08, 3.3, false); let ty = 1.95, tx = 1.7;
  window.__beforeRender = (dt, T) => {{ window.__hideNear(2.5, -4.5, 3.5, []); tx = Math.min(3.3, tx + dt * .45); ty = T < 2.2 ? 1.95 : Math.max(.75, ty - dt * .6); window.__camTarget = {V}(tx, gy + ty, -5.4); P.cam.dist = T < 2.2 ? 3.3 : Math.max(2.4, P.cam.dist - dt * .3); }}; }}"""
# c11 inside the newly opened school (blackboard lists the newest residents)
C11 = """() => { const P = window.__pulau; window.__time('siang'); window.__cand(false); window.__cheer = null; window.__room.enter('sekolah'); P.player.obj.visible = false; P.cam.pitch = .38; P.cam.dist = 6.5;
  window.__beforeRender = (dt, T) => { P.cam.dist -= dt * .15; }; }"""
# c12 the former vice president with his own placard 'EGA_ NYALON' in front of the board
C12 = f"""() => {{ const P = window.__pulau, vp = window.__VP(); window.__room.exit(); window.__time('siang'); window.__cand(false); window.__cheer = null; P.player.obj.visible = false; window.__clearSigns(); window.__unkit(vp);
  window.__placard(vp, 'EGA_|NYALON'); const x = 2.5, z = -3.0;
  window.__look(x, z, .25, .12, 2.6, false); window.__camTarget = {V}(x, {G}(x, z) + 1.5, z);
  window.__beforeRender = (dt, T) => {{ window.__hideNear(x, z, 3.5, [vp]); window.__pose(vp, x, z, .25, T < 2.4 ? 'talk' : 'cheer', T); P.cam.dist -= dt * .1; }}; }}"""
# c13 end: crowd, former president and VP with placards, board behind; camera rises and pulls out
C13 = f"""() => {{ const P = window.__pulau, pr = window.__PR(), vp = window.__VP(); window.__time('siang'); window.__cand(false); window.__cheer = true; P.player.obj.visible = false; window.__clearSigns(); {CROWD}
  window.__unkit(pr); window.__unkit(vp); window.__placard(pr, 'MANTAN|PRESIDEN'); window.__placard(vp, 'EGA_|NYALON');
  window.__look(.5, -5.8, .3, .5, 6, false); window.__camTarget = {V}(.5, {G}(.5, -5.8) + 1.0, -5.8);
  window.__beforeRender = (dt, T) => {{ window.__crowd(T, i => i % 2 ? 'cheer' : 'wave'); window.__pose(pr, 1.6, -3.4, 0, 'wave', T); window.__pose(vp, 2.6, -3.3, 0, 'cheer', T + 1);
    P.cam.dist += dt * 1.4; P.cam.pitch = Math.min(1.0, P.cam.pitch + dt * .05); P.cam.yaw += dt * .05; }}; }}"""
SHOTS = {'c1': (C1, 140), 'c2': (C2, 85), 'c3': (C3, 160), 'c4': (C4, 125), 'c7': (C7, 135), 'c8': (C8, 150), 'c9': (C9, 75),
         'c10': (C10, 150), 'c11': (C11, 120), 'c12': (C12, 120), 'c13': (C13, 300)}
CLEAR = "() => { window.__cheer = null; window.__camTarget = null; window.__beforeRender = null; }"
async def run(which):
    async with async_playwright() as p:
        b, pg = await setup(p)
        await pg.evaluate(BASE)
        for k, (js, n) in SHOTS.items():
            if k in which and 'prev' not in which:
                await shoot(pg, 'e15' + k, n, start_js=js, warm=12)
                await pg.evaluate(CLEAR)
        if 'prev' in which:
            for k, (js, n) in SHOTS.items():
                if 'all' not in which and k not in which: continue
                await shoot(pg, 'p15' + k, 1, start_js=js, warm=int(os.environ.get('WARM', '40')))
                await pg.evaluate(CLEAR)
        await b.close()
if __name__ == "__main__": asyncio.run(run(sys.argv[1].split(",")))
