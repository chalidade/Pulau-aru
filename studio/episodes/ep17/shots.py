"""Episode 17 "Kotak Usulan" shot list.  usage: DPR=2 python3 shots.py c1,c3,...  (DPR=1 + prev for checks)
Kotak Usulan cells 50..51 x 51 (r0, faces south onto the cross street). Toilet Umum cells 64..66 x 54..55 (r2, door faces north onto the cross street).
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

KB = "const kb = window.__bld('kotakusulan'), KX = kb.position.x, KZ = kb.position.z, KY = window.__pulau.WD.groundY(KX, KZ);"
TB = "const tb = window.__bld('toiletumum'), TX = tb.position.x, TZ = tb.position.z, TY = window.__pulau.WD.groundY(TX, TZ);"
# c1 cold open: the vice president next to the new suggestion box, panicking: "isinya cuma satu surat!"
C1 = f"""() => {{ const P = window.__pulau, vp = window.__VP(), pr = window.__PR(); window.__time('siang'); window.__cheer = null; P.player.obj.visible = false; {KB}
  const x = KX + .75, z = KZ + .7;
  window.__look(x, z, .3, .12, 2.9, false); window.__camTarget = {V}(x - .2, KY + 1.15, z);
  window.__beforeRender = (dt, T) => {{ window.__hideNear(KX, KZ, 3.5, [vp]); window.__pose(vp, x, z, .3, T < 1.6 ? 'panic' : 'talk', T); P.cam.dist = Math.max(2.2, P.cam.dist - dt * .1); }}; }}"""
# c2 the president on the stage: "rapat kabinet pertama!"
C2 = f"""() => {{ const P = window.__pulau, pr = window.__PR(), vp = window.__VP(); window.__time('siang'); window.__cheer = null; P.player.obj.visible = false;
  const st = window.__bld('mimbar'), sy = st.position.y + .55; const x = -2.35, z = -10.0;
  window.__look(x, z, -.18, .3, 4.0, false); window.__camTarget = {V}(x + .3, sy + 1.4, z);
  window.__beforeRender = (dt, T) => {{ window.__poseY(pr, x, sy, z, .1, T < 1.4 ? 'talk' : 'point', T); window.__poseY(vp, -.6, sy, -10.3, -.3, 'idle', T); P.cam.dist = Math.max(3.4, P.cam.dist - dt * .15); }}; }}"""
# c3 aerial dropping onto the suggestion box in front of the stage
C3 = f"""() => {{ const P = window.__pulau; window.__time('siang'); window.__cheer = null; P.player.obj.visible = false; {KB}
  window.__look(KX, KZ, .35, 1.0, 16, false); window.__camTarget = {V}(KX, KY + 1, KZ);
  window.__beforeRender = (dt, T) => {{ P.cam.dist = Math.max(5.5, P.cam.dist - dt * 2.2); P.cam.pitch = Math.max(.45, P.cam.pitch - dt * .09); P.cam.yaw -= dt * .05; }}; }}"""
# c4 close on the sign and the box, slow push-in
C4 = f"""() => {{ const P = window.__pulau; window.__time('siang'); window.__cheer = null; P.player.obj.visible = false; {KB}
  window.__look(KX, KZ, .08, .1, 3.4, false); window.__camTarget = {V}(KX, KY + 2.1, KZ);
  window.__beforeRender = (dt, T) => {{ window.__hideNear(KX, KZ, 3, []); P.cam.dist = Math.max(2.4, P.cam.dist - dt * .2); }}; }}"""
# c5 the president beside the box, asking who wants to suggest first
C5 = f"""() => {{ const P = window.__pulau, pr = window.__PR(); window.__time('siang'); window.__cheer = null; P.player.obj.visible = false; {KB}
  const x = KX - 1.15, z = KZ + .5;
  window.__look(x, z, -.25, .14, 2.8, false); window.__camTarget = {V}(x + .35, KY + 1.2, z);
  window.__beforeRender = (dt, T) => {{ window.__hideNear(KX, KZ, 3.5, [pr]); window.__pose(pr, x, z, -.25, 'talk', T); P.cam.dist -= dt * .1; }}; }}"""
# c6 the former president (MANTAN PRESIDEN placard) posts the first letter into the box
C6 = f"""() => {{ const P = window.__pulau, n = window.__N('@Etet_443'); window.__time('siang'); window.__cheer = null; P.player.obj.visible = false; {KB}
  const x = KX + .35, z = KZ + .75;
  window.__look(x, z, .55, .14, 2.9, false); window.__camTarget = {V}(x - .2, KY + 1.2, z - .2);
  window.__beforeRender = (dt, T) => {{ window.__hideNear(KX, KZ, 3.5, [n]); window.__pose(n, x, z, .45, T < 1.5 ? 'reach' : 'talk', T); P.cam.dist -= dt * .08; }}; }}"""
# c7 the residents with placards (USUL DONG!, TOILET UMUM!) by the banner
C7 = f"""() => {{ const P = window.__pulau; window.__time('siang'); window.__cheer = true; P.player.obj.visible = false;
  const sp = window.__bld('spanduk'); const x = sp.position.x + 2.6, z = sp.position.z;
  window.__look(x, z, Math.PI - .25, .3, 4.6, false); window.__camTarget = {V}(x, {G}(x, z) + 1.6, z);
  window.__beforeRender = (dt, T) => {{ P.cam.dist -= dt * .25; P.cam.yaw += dt * .04; }}; }}"""
# c8 a resident shouting for a public toilet
C8 = f"""() => {{ const P = window.__pulau, w = window.__W()[10]; window.__time('siang'); window.__cheer = null; P.player.obj.visible = false; {KB}
  const x = KX + 2.2, z = KZ + 1.2;
  window.__look(x, z, .1, .12, 2.5, false); window.__camTarget = {V}(x, KY + 1.15, z);
  window.__beforeRender = (dt, T) => {{ window.__hideNear(x, z, 3, [w]); window.__pose(w, x, z, .1, T < 1.2 ? 'panic' : 'talk', T); P.cam.dist -= dt * .1; }}; }}"""
# c9 the president points: "bangun sekarang!"
C9 = f"""() => {{ const P = window.__pulau, pr = window.__PR(); window.__time('siang'); window.__cheer = null; P.player.obj.visible = false; {KB}
  const x = KX - .8, z = KZ + .65;
  window.__look(x, z, .35, .1, 2.3, false); window.__camTarget = {V}(x, KY + 1.3, z);
  window.__beforeRender = (dt, T) => {{ window.__hideNear(KX, KZ, 3.5, [pr]); window.__pose(pr, x, z, .35, T < 1.8 ? 'talk' : 'point', T); P.cam.dist = Math.max(1.9, P.cam.dist - dt * .12); }}; }}"""
# c10 the new public toilet: push in from the street, residents cheer
C10 = f"""() => {{ const P = window.__pulau; window.__time('siang'); window.__cheer = true; P.player.obj.visible = false; {TB}
  window.__look(TX, TZ, Math.PI + .3, .5, 9, false); window.__camTarget = {V}(TX, TY + 1.4, TZ);
  window.__beforeRender = (dt, T) => {{ P.cam.dist = Math.max(5.2, P.cam.dist - dt * 1.0); P.cam.pitch = Math.max(.22, P.cam.pitch - dt * .07); P.cam.yaw -= dt * .06; }}; }}"""
# c11 a resident hurries from the coffee cart to the toilet door
C11 = f"""() => {{ const P = window.__pulau, w = window.__W()[11]; window.__time('siang'); window.__cheer = null; P.player.obj.visible = false; {TB}
  window.__look(TX - .7, TZ - 1.6, Math.PI + .8, .25, 4.0, false); window.__camTarget = {V}(TX - .7, TY + 1.0, TZ - 1.6);
  window.__beforeRender = (dt, T) => {{ window.__hideNear(TX, TZ, 4, [w]); const k = Math.min(1, Math.max(0, T / 2.6)); const x = TX - 1.6 + k * 1.15, z = TZ - 3.0 + k * 1.7;
    window.__pose(w, x, z, k < 1 ? Math.atan2(1.15, 1.7) : Math.PI, k < 1 ? 'walk' : 'cheer', T * 1.6); P.cam.dist -= dt * .15; }}; }}"""
# c12 inside the newly opened hospital
C12 = """() => { const P = window.__pulau; window.__time('siang'); window.__cheer = null; window.__room.enter('rumahsakit'); P.player.obj.visible = false; P.cam.pitch = .62; P.cam.dist = 7;
  window.__beforeRender = (dt, T) => { P.cam.dist -= dt * .25; }; }"""
# c13 end: president and VP at the box, camera rises over the town
C13 = f"""() => {{ const P = window.__pulau, pr = window.__PR(), vp = window.__VP(); window.__room.exit(); window.__time('siang'); window.__cheer = true; P.player.obj.visible = false; {KB}
  window.__look(KX, KZ + .6, .9, .35, 3.6, false); window.__camTarget = {V}(KX, KY + 1.1, KZ + .6);
  window.__beforeRender = (dt, T) => {{ window.__pose(pr, KX - .75, KZ + .7, .1, 'wave', T); window.__pose(vp, KX + .75, KZ + .7, -.1, 'cheer', T + 1);
    P.cam.dist += dt * 1.4; P.cam.pitch = Math.min(1.0, P.cam.pitch + dt * .07); P.cam.yaw += dt * .04; }}; }}"""
SHOTS = {'c1': (C1, 165), 'c2': (C2, 100), 'c3': (C3, 185), 'c4': (C4, 170), 'c5': (C5, 80), 'c6': (C6, 150), 'c7': (C7, 200),
         'c8': (C8, 130), 'c9': (C9, 160), 'c10': (C10, 160), 'c11': (C11, 135), 'c12': (C12, 90), 'c13': (C13, 240)}
CLEAR = "() => { window.__cheer = null; window.__camTarget = null; window.__beforeRender = null; }"
async def run(which):
    async with async_playwright() as p:
        b, pg = await setup(p)
        await pg.evaluate(BASE); await pg.evaluate("() => { " + NPC + " }")
        for k, (js, n) in SHOTS.items():
            if k in which and 'prev' not in which:
                await shoot(pg, 'e17' + k, int(os.environ.get('N_' + k, n)), start_js=js, warm=12)
                await pg.evaluate(CLEAR)
        if 'prev' in which:
            for k, (js, n) in SHOTS.items():
                if 'all' not in which and k not in which: continue
                await shoot(pg, 'p17' + k, 1, start_js=js, warm=int(os.environ.get('WARM', '40')))
                await pg.evaluate(CLEAR)
        await b.close()
if __name__ == "__main__": asyncio.run(run(sys.argv[1].split(",")))
