"""Episode 18 "Bank Pulau" shot list.  usage: DPR=2 python3 shots.py c1,c3,...  (DPR=1 + prev for checks)
Bank Pulau cells 59..62 x 54..56 (r2, door faces north onto the cross street). Kotak Usulan cells 50..51 x 51.
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
BB = "const bb = window.__bld('bankpulau'), BX = bb.position.x, BZ = bb.position.z, BY = window.__pulau.WD.groundY(BX, BZ - 2);"
# bank faces -z (north). Door at about (BX, BZ - 0.6); ATM at about (BX - 1.75, BZ - 0.5); steps reach BZ - 1.5.
# c1 cold open: the former president at the ATM, demanding his old salary
C1 = f"""() => {{ const P = window.__pulau, n = window.__N('@Etet_443'); window.__time('siang'); window.__cheer = null; P.player.obj.visible = false; {BB}
  const x = BX - 1.55, z = BZ - 1.45;
  window.__look(x, z, Math.PI + .35, .12, 2.7, false); window.__camTarget = {V}(x + .1, BY + 1.15, z);
  window.__beforeRender = (dt, T) => {{ window.__hideNear(x, z, 3, [n]); window.__pose(n, x, z, Math.PI + .35, T < 1.4 ? 'panic' : 'point', T); P.cam.dist = Math.max(2.1, P.cam.dist - dt * .12); }}; }}"""
# c2 the vice president, as teller at the door: "saldo nol"
C2 = f"""() => {{ const P = window.__pulau, vp = window.__VP(); window.__time('siang'); window.__cheer = null; P.player.obj.visible = false; {BB}
  const x = BX - .2, z = BZ - 1.5;
  window.__look(x, z, Math.PI - .3, .14, 2.6, false); window.__camTarget = {V}(x, BY + 1.2, z);
  window.__beforeRender = (dt, T) => {{ window.__hideNear(x, z, 3, [vp]); window.__pose(vp, x, z, Math.PI - .3, 'talk', T); P.cam.dist = Math.max(2.1, P.cam.dist - dt * .1); }}; }}"""
# c3 the suggestion box, slow push-in
C3 = f"""() => {{ const P = window.__pulau; window.__time('siang'); window.__cheer = null; P.player.obj.visible = false; {KB}
  window.__look(KX, KZ, -.35, .3, 4.0, false); window.__camTarget = {V}(KX, KY + 1.8, KZ);
  window.__beforeRender = (dt, T) => {{ window.__hideNear(KX, KZ, 3, []); P.cam.dist = Math.max(2.6, P.cam.dist - dt * .3); P.cam.yaw -= dt * .04; }}; }}"""
# c4 the president beside the box
C4 = f"""() => {{ const P = window.__pulau, pr = window.__PR(); window.__time('siang'); window.__cheer = null; P.player.obj.visible = false; {KB}
  const x = KX - 1.15, z = KZ + .5;
  window.__look(x, z, -.25, .14, 2.8, false); window.__camTarget = {V}(x + .35, KY + 1.2, z);
  window.__beforeRender = (dt, T) => {{ window.__hideNear(KX, KZ, 3.5, [pr]); window.__pose(pr, x, z, -.25, T < 1.6 ? 'talk' : 'point', T); P.cam.dist -= dt * .1; }}; }}"""
# c5 the vice president pulls a letter out of the box
C5 = f"""() => {{ const P = window.__pulau, vp = window.__VP(); window.__time('siang'); window.__cheer = null; P.player.obj.visible = false; {KB}
  const x = KX + .4, z = KZ + .75;
  window.__look(x, z, .5, .14, 2.8, false); window.__camTarget = {V}(x - .2, KY + 1.2, z - .2);
  window.__beforeRender = (dt, T) => {{ window.__hideNear(KX, KZ, 3.5, [vp]); window.__pose(vp, x, z, .45, T < 1.3 ? 'reach' : 'talk', T); P.cam.dist -= dt * .08; }}; }}"""
# c6 a resident cheering about saving her mango coins
C6 = f"""() => {{ const P = window.__pulau, w = window.__W()[10]; window.__time('siang'); window.__cheer = null; P.player.obj.visible = false; {KB}
  const x = KX + 2.2, z = KZ + 1.2;
  window.__look(x, z, .1, .12, 2.5, false); window.__camTarget = {V}(x, KY + 1.15, z);
  window.__beforeRender = (dt, T) => {{ window.__hideNear(x, z, 3, [w]); window.__pose(w, x, z, .1, 'cheer', T); P.cam.dist -= dt * .1; }}; }}"""
# c7 aerial dropping onto the new bank
C7 = f"""() => {{ const P = window.__pulau; window.__time('siang'); window.__cheer = true; P.player.obj.visible = false; {BB}
  window.__look(BX, BZ, Math.PI - .5, 1.0, 18, false); window.__camTarget = {V}(BX, BY + 1.4, BZ);
  window.__beforeRender = (dt, T) => {{ P.cam.dist = Math.max(7, P.cam.dist - dt * 2.6); P.cam.pitch = Math.max(.42, P.cam.pitch - dt * .1); P.cam.yaw += dt * .06; }}; }}"""
# c8 close on the sign, slow push-in
C8 = f"""() => {{ const P = window.__pulau; window.__time('siang'); window.__cheer = null; P.player.obj.visible = false; {BB}
  window.__look(BX, BZ - 1, Math.PI + .3, .42, 5.0, false); window.__camTarget = {V}(BX, BY + 2.2, BZ - 1);
  window.__beforeRender = (dt, T) => {{ window.__hideNear(BX, BZ - 1, 3.5, []); P.cam.dist = Math.max(4.2, P.cam.dist - dt * .25); }}; }}"""
# c9 the president at the ATM, depositing five coins
C9 = f"""() => {{ const P = window.__pulau, pr = window.__PR(); window.__time('siang'); window.__cheer = null; P.player.obj.visible = false; {BB}
  const x = BX - 1.55, z = BZ - 1.4;
  window.__look(x, z, Math.PI + .4, .14, 2.6, false); window.__camTarget = {V}(x + .1, BY + 1.15, z);
  window.__beforeRender = (dt, T) => {{ window.__hideNear(x, z, 3, [pr]); window.__pose(pr, x, z, Math.PI + .4, T < 1.2 ? 'talk' : 'reach', T); P.cam.dist = Math.max(2.0, P.cam.dist - dt * .1); }}; }}"""
# c10 the vice president, suspicious
C10 = f"""() => {{ const P = window.__pulau, vp = window.__VP(); window.__time('siang'); window.__cheer = null; P.player.obj.visible = false; {BB}
  const x = BX - .6, z = BZ - 1.7;
  window.__look(x, z, Math.PI - .35, .12, 2.3, false); window.__camTarget = {V}(x, BY + 1.15, z);
  window.__beforeRender = (dt, T) => {{ window.__hideNear(x, z, 3, [vp]); window.__pose(vp, x, z, Math.PI - .35, 'point', T); P.cam.dist = Math.max(1.9, P.cam.dist - dt * .1); }}; }}"""
# c11 the president panics
C11 = f"""() => {{ const P = window.__pulau, pr = window.__PR(); window.__time('siang'); window.__cheer = null; P.player.obj.visible = false; {BB}
  const x = BX - 1.3, z = BZ - 1.6;
  window.__look(x, z, Math.PI + .2, .1, 2.1, false); window.__camTarget = {V}(x, BY + 1.25, z);
  window.__beforeRender = (dt, T) => {{ window.__hideNear(x, z, 3, [pr]); window.__pose(pr, x, z, Math.PI + .2, 'panic', T); P.cam.dist = Math.max(1.8, P.cam.dist - dt * .1); }}; }}"""
# c12 the former president sits on the bank steps, starting from zero
C12 = f"""() => {{ const P = window.__pulau, n = window.__N('@Etet_443'); window.__time('siang'); window.__cheer = null; P.player.obj.visible = false; {BB}
  const x = BX + .9, z = BZ - 1.55;
  window.__look(x, z, Math.PI - .45, .2, 3.0, false); window.__camTarget = {V}(x, BY + .9, z);
  window.__beforeRender = (dt, T) => {{ window.__hideNear(x, z, 3, [n]); window.__pose(n, x, z, Math.PI - .45, T < 2 ? 'sit' : 'sittalk', T, -.05); P.cam.dist = Math.max(2.3, P.cam.dist - dt * .12); }}; }}"""
# c13 inside the newly opened house
C13 = """() => { const P = window.__pulau; window.__time('siang'); window.__cheer = null; window.__room.enter('rumah'); P.player.obj.visible = false; P.cam.pitch = .85; P.cam.dist = 9.5; P.cam.yaw = .25;
  const pl = P.player; window.__camTarget = new P.cam.target.constructor(pl.x - .5, pl.y + .4, pl.z - 3.2);
  window.__beforeRender = (dt, T) => { P.cam.dist -= dt * .35; P.cam.yaw -= dt * .05; }; }"""
# c14 end: president and VP wave in front of the bank, camera rises over the town
C14 = f"""() => {{ const P = window.__pulau, pr = window.__PR(), vp = window.__VP(); window.__room.exit(); window.__time('siang'); window.__cheer = true; P.player.obj.visible = false; {BB}
  window.__look(BX, BZ - 1.6, Math.PI + .95, .38, 3.6, false); window.__camTarget = {V}(BX, BY + 1.3, BZ - 1.6);
  window.__beforeRender = (dt, T) => {{ window.__pose(pr, BX - .6, BZ - 1.6, Math.PI + .2, 'wave', T); window.__pose(vp, BX + .6, BZ - 1.6, Math.PI - .2, 'cheer', T + 1);
    P.cam.dist += dt * 1.5; P.cam.pitch = Math.min(1.0, P.cam.pitch + dt * .07); P.cam.yaw -= dt * .04; }}; }}"""
SHOTS = {'c1': (C1, 110), 'c2': (C2, 105), 'c3': (C3, 165), 'c4': (C4, 120), 'c5': (C5, 140), 'c6': (C6, 120), 'c7': (C7, 135),
         'c8': (C8, 195), 'c9': (C9, 95), 'c10': (C10, 115), 'c11': (C11, 110), 'c12': (C12, 165), 'c13': (C13, 115), 'c14': (C14, 270)}
CLEAR = "() => { window.__cheer = null; window.__camTarget = null; window.__beforeRender = null; }"
async def run(which):
    async with async_playwright() as p:
        b, pg = await setup(p)
        await pg.evaluate(BASE); await pg.evaluate("() => { " + NPC + " }")
        for k, (js, n) in SHOTS.items():
            if k in which and 'prev' not in which:
                await shoot(pg, 'e18' + k, int(os.environ.get('N_' + k, n)), start_js=js, warm=12)
                await pg.evaluate(CLEAR)
        if 'prev' in which:
            for k, (js, n) in SHOTS.items():
                if 'all' not in which and k not in which: continue
                await shoot(pg, 'p18' + k, 1, start_js=js, warm=int(os.environ.get('WARM', '40')))
                await pg.evaluate(CLEAR)
        await b.close()
if __name__ == "__main__": asyncio.run(run(sys.argv[1].split(",")))
