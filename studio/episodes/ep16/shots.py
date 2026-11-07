"""Episode 16 "Pelantikan & Kopi Dong" shot list.  usage: DPR=2 python3 shots.py c1,c3,...  (DPR=1 + prev for checks)
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
NPC = """window.__N = s => window.__pulau.npcs.find(n => n.name === s);"""
# c1 cold open: the new president 'EGA_ (sash on) on the stage, talking, then both arms up; crowd cheers
C1 = f"""() => {{ const P = window.__pulau, pr = window.__PR(), vp = window.__VP(); window.__time('siang'); window.__cheer = true; P.player.obj.visible = false;
  const st = window.__bld('mimbar'), sy = st.position.y + .55; const x = -2.35, z = -10.0;
  window.__look(x, z, -.18, .3, 4.3, false); window.__camTarget = {V}(x + .3, sy + 1.45, z);
  window.__beforeRender = (dt, T) => {{ window.__poseY(pr, x, sy, z, .1, T < 2.3 ? 'talk' : 'cheer', T); window.__poseY(vp, -.6, sy, -10.3, -.3, T < 2.3 ? 'idle' : 'cheer', T); P.cam.dist = Math.max(3.6, P.cam.dist - dt * .12); }}; }}"""
# c3 the results board: pan down from HASIL PEMILU to the winners' names
C3 = f"""() => {{ const P = window.__pulau; window.__time('siang'); window.__cheer = null; P.player.obj.visible = false; const gy = {G}(2.5, -5.0);
  window.__look(2.5, -5.2, 0, .08, 3.0, false); let ty = 2.75;
  window.__beforeRender = (dt, T) => {{ window.__hideNear(2.5, -4.5, 3.5, []); ty = Math.max(2.05, ty - dt * .25); window.__camTarget = {V}(2.5, gy + ty, -5.4); P.cam.dist = Math.max(2.5, P.cam.dist - dt * .1); }}; }}"""
# c4 the new vice president on his gold chair at the board, shocked he got picked from a tag
C4 = f"""() => {{ const P = window.__pulau, vp = window.__VP(), pr = window.__PR(); window.__time('siang'); window.__cheer = null; P.player.obj.visible = false;
  const x = 3.15, z = -4.5, gy = {G}(2.5, -5.0);
  window.__look(x, z, .2, .14, 2.6, false); window.__camTarget = {V}(x - .2, gy + 1.15, z);
  window.__beforeRender = (dt, T) => {{ window.__hideNear(2.5, -4.5, 4, [vp, pr]); window.__poseY(vp, x, gy + (window.__SITY || .28), z, .2, T < 1.8 ? 'sit' : 'sittalk', T); window.__poseY(pr, 1.85, gy + (window.__SITY || .28), z, -.1, 'sit', T); P.cam.dist -= dt * .1; }}; }}"""
# c5 inauguration: Aru centre stage, president left, vice president right, crowd in front
C5 = f"""() => {{ const P = window.__pulau, pl = P.player, pr = window.__PR(), vp = window.__VP(); window.__time('siang'); window.__cheer = null; window.__room.exit(); {CROWD}
  const st = window.__bld('mimbar'), sy = st.position.y + .55;
  window.__look(-1.5, -10.4, 0, .42, 5.6, true); window.__camTarget = {V}(-1.5, sy + 1.0, -10.2);
  window.__beforeRender = (dt, T) => {{ window.__crowd(T, i => T > 2.6 ? 'cheer' : 'idle'); window.__cheer = T > 2.6;
    window.__poseY(pr, -2.45, sy, -10.35, .25, T > 2.6 ? 'wave' : 'idle', T); window.__poseY(vp, -.55, sy, -10.35, -.25, T > 2.6 ? 'cheer' : 'idle', T);
    pl.x = -1.5; pl.z = -10.0; pl.tx = null; pl.y = sy; pl.vy = 0; pl.obj.position.set(-1.5, sy, -10.0); pl.obj.rotation.y = 0; const u = pl.obj.userData;
    u.armR.rotation.x = -1.1 + Math.sin(T * 7) * .4; u.armL.rotation.x = T > 2.6 ? -2.6 : -.4; P.cam.dist -= dt * .15; }}; }}"""
# c6 the crowd (live event placards: SELAMAT PRES EGA_, KOPI DONG! ...) cheering, seen from the stage
C6 = f"""() => {{ const P = window.__pulau; window.__time('siang'); window.__cheer = true; P.player.obj.visible = false;
  const sp = window.__bld('spanduk'); const x = sp.position.x + 2.6, z = sp.position.z;
  window.__look(x, z, Math.PI - .25, .3, 4.4, false); window.__camTarget = {V}(x, {G}(x, z) + 1.6, z);
  window.__beforeRender = (dt, T) => {{ P.cam.dist -= dt * .3; P.cam.yaw += dt * .04; }}; }}"""
# c7 the former president with his MANTAN PRESIDEN placard, clapping, a little sad
C7 = f"""() => {{ const P = window.__pulau, n = window.__N('@Etet_443'); window.__time('siang'); window.__cheer = null; P.player.obj.visible = false; const x = .6, z = -2.9;
  window.__look(x, z, .15, .15, 3.0, false); window.__camTarget = {V}(x, {G}(x, z) + 1.25, z);
  window.__beforeRender = (dt, T) => {{ window.__hideNear(x, z, 3, [n]); window.__pose(n, x, z, .15, T < 1.4 ? 'idle' : 'talk', T); P.cam.dist -= dt * .08; }}; }}"""
# c8 the new coffee cart KOPI DONG with its seller (wibu cilik pelenger) waving behind the counter
C8 = f"""() => {{ const P = window.__pulau, s = window.__N('@sapta.rajo.ghaisa'); window.__time('siang'); window.__cheer = null; P.player.obj.visible = false;
  const o = window.__bld('gerobakkopi'), x = o.position.x, z = o.position.z;
  window.__look(x, z, .05, .2, 2.9, false); window.__camTarget = {V}(x, {G}(x, z) + .95, z);
  window.__beforeRender = (dt, T) => {{ window.__hideNear(x, z, 3, [s]); window.__pose(s, x, z - .72, 0, T < 2.2 ? 'wave' : 'talk', T); P.cam.dist = Math.max(2.4, P.cam.dist - dt * .12); }}; }}"""
# c9 President 'EGA_ buys a coffee and pays (unlike the old president and the gorengan, ep 9)
C9 = f"""() => {{ const P = window.__pulau, s = window.__N('@sapta.rajo.ghaisa'), pr = window.__PR(); window.__time('siang'); window.__cheer = null; P.player.obj.visible = false;
  const o = window.__bld('gerobakkopi'), x = o.position.x, z = o.position.z;
  window.__look(x, z + .4, .7, .25, 3.0, false); window.__camTarget = {V}(x, {G}(x, z) + 1.0, z + .3);
  window.__beforeRender = (dt, T) => {{ window.__hideNear(x, z, 3, [s, pr]); window.__pose(s, x, z - .72, 0, T < 1.5 ? 'talk' : 'reach', T); window.__pose(pr, x - .1, z + .95, Math.PI, T < 1.5 ? 'reach' : 'talk', T); P.cam.dist -= dt * .08; }}; }}"""
# c10 wide: residents queue at the cart, seller waving
C10 = f"""() => {{ const P = window.__pulau, s = window.__N('@sapta.rajo.ghaisa'); window.__time('siang'); window.__cheer = null; P.player.obj.visible = false;
  const o = window.__bld('gerobakkopi'), x = o.position.x, z = o.position.z, W = window.__W().slice(9, 13);
  window.__look(x, z + .5, .35, .45, 3.9, false); window.__camTarget = {V}(x - .3, {G}(x, z) + .9, z + .6);
  window.__beforeRender = (dt, T) => {{ window.__pose(s, x, z - .72, 0, (T % 3) < 1.5 ? 'wave' : 'talk', T); W.forEach((n, i) => window.__pose(n, x - .9 + i * .62, z + 1.05 + (i % 2) * .25, Math.PI + (i - 1.5) * .15, i === 1 ? 'eat' : 'idle', T + i)); P.cam.yaw += dt * .05; }}; }}"""
# c11 inside the newly opened president's house (current president and VP seated)
C11 = """() => { const P = window.__pulau; window.__time('siang'); window.__cheer = null; window.__room.enter('rumahpresiden'); P.player.obj.visible = false; P.cam.pitch = .38; P.cam.dist = 6.5;
  window.__beforeRender = (dt, T) => { P.cam.dist -= dt * .15; }; }"""
# c12 President 'EGA_ in front of the results board, pointing: "first request... wait and see"
C12 = f"""() => {{ const P = window.__pulau, pr = window.__PR(); window.__room.exit(); window.__time('siang'); window.__cheer = null; P.player.obj.visible = false; const x = 2.5, z = -3.2;
  window.__look(x, z, .2, .12, 2.6, false); window.__camTarget = {V}(x, {G}(x, z) + 1.4, z);
  window.__beforeRender = (dt, T) => {{ window.__hideNear(x, z, 3.5, [pr]); window.__pose(pr, x, z, .2, T < 1.6 ? 'talk' : 'point', T); P.cam.dist -= dt * .1; }}; }}"""
# c13 end: the stage with president + VP, crowd cheering, camera rises and pulls out over the town
C13 = f"""() => {{ const P = window.__pulau, pr = window.__PR(), vp = window.__VP(); window.__room.exit(); window.__time('siang'); window.__cheer = true; P.player.obj.visible = false; {CROWD}
  const st = window.__bld('mimbar'), sy = st.position.y + .55;
  window.__look(-1.0, -8.0, .3, .55, 6, false); window.__camTarget = {V}(-1.0, sy + .6, -8.0);
  window.__beforeRender = (dt, T) => {{ window.__crowd(T, i => i % 2 ? 'cheer' : 'wave'); window.__poseY(pr, -2.0, sy, -10.3, 0, 'wave', T); window.__poseY(vp, -1.0, sy, -10.3, 0, 'cheer', T + 1);
    P.cam.dist += dt * 1.3; P.cam.pitch = Math.min(1.0, P.cam.pitch + dt * .05); P.cam.yaw += dt * .05; }}; }}"""
SHOTS = {'c1': (C1, 140), 'c3': (C3, 165), 'c4': (C4, 215), 'c5': (C5, 125), 'c7': (C7, 115), 'c8': (C8, 155),
         'c9': (C9, 112), 'c10': (C10, 192), 'c11': (C11, 128), 'c12': (C12, 100), 'c13': (C13, 260)}
CLEAR = "() => { window.__cheer = null; window.__camTarget = null; window.__beforeRender = null; }"
async def run(which):
    async with async_playwright() as p:
        b, pg = await setup(p)
        await pg.evaluate(BASE); await pg.evaluate("() => { " + NPC + " }")
        for k, (js, n) in SHOTS.items():
            if k in which and 'prev' not in which:
                await shoot(pg, 'e16' + k, int(os.environ.get('N_' + k, n)), start_js=js, warm=12)
                await pg.evaluate(CLEAR)
        if 'prev' in which:
            for k, (js, n) in SHOTS.items():
                if 'all' not in which and k not in which: continue
                await shoot(pg, 'p16' + k, 1, start_js=js, warm=int(os.environ.get('WARM', '40')))
                await pg.evaluate(CLEAR)
        await b.close()
if __name__ == "__main__": asyncio.run(run(sys.argv[1].split(",")))
