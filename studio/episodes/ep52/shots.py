"""Episode 52 "Sandal Pulang, Ikan Datang" shot list (format CERITA, run sore 22 Nov).  usage: DPR=2 python3 shots.py c1,c3,...  (DPR=1 + prev for checks)
No new comments (komentar.md empty, Chrome not connected): the episode pays off the sandal thread (ep 50-51). Dayang, the first volunteer of the
Pos Gotong Royong, brings the pair of blue flip-flops from the mine to _Rayhannn` at the Pelabuhan Nelayan; RANUUGLL (Polisi Pantai) stops her
("barang bukti!") then escorts her; muhamatferos197 calls Rayhan; Rayhan puts the sandals on and catches his first real fish.
Live state (island.json): Rayhan pose 'rodpair' (fish + sandals on his feet), Dayang's spot at the harbour, tambang b.returned (cart empty,
board SUDAH PULANG KE RAYHAN), posgotong b.tasks ['Antar sandal Rayhan'] (PAPAN TUGAS). Staged only for the flashback/earlier beats:
Rayhan without fish/sandals (c3, c9), the pair in the cart (c4) and in Dayang's hands (c5-c9), Dayang at the mine (c5) and at the police post (c7).
"""
import asyncio, sys, os, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'lib'))
from harness import *
def _mod(name, path):
    sp = importlib.util.spec_from_file_location(name, path); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m
E51 = _mod('ep51shots', os.path.join(HERE, '..', 'ep51', 'shots.py'))
CHAIN = E51.CHAIN + (E51.SETUP51,)
SETUP52 = """() => { const P = window.__pulau, T3 = window.THREE || null;
  const F = s => P.npcs.find(n => n.name === s || (n.name || '').startsWith(s));
  window.__RAY = () => F('_Rayhannn'); window.__FER = () => F('muhamatferos197'); window.__RANU = () => F('RANUUGLL');
  const B = {}; P.scene.traverse(o => { if (o.userData && o.userData.b && ['tambang', 'posgotong', 'pelabuhan'].includes(o.userData.b.type)) B[o.userData.b.type] = o; });
  window.__B52 = B;
  // Rayhan's state: fish on the hook? sandals on his feet?
  window.__ray = (fish, feet) => { const n = window.__RAY(); if (!n) return; (n.kit || []).forEach((m, i) => { if (i >= 2) m.visible = fish; }); (n.obj.userData.feet || []).forEach(m => m.visible = feet); };
  // the pair of sandals in the mine cart (flashback) and in Dayang's hands
  window.__cartPair = (v) => { const c = B.tambang && B.tambang.userData.cart; if (!c) return; c.o.children.forEach(ch => { if (ch.isGroup && ch.children.length === 4) ch.visible = v; }); };
  window.__handPair = (v) => { const n = window.__DAY(); if (!n) return; let g = n.obj.userData.pair;
    if (!g) { let bm = null; P.scene.traverse(o => { if (!bm && o.isMesh && o.geometry && o.geometry.type === 'BoxGeometry' && o.material && o.material.isMeshStandardMaterial) bm = o; });
      const BG = bm.geometry.constructor, MM = bm.material.constructor, G0 = bm.parent.constructor; g = new G0();
      const mk = (w, h, d, c, x, y, z) => { const m = new bm.constructor(new BG(w, h, d), new MM({ color: c, roughness: .7 })); m.position.set(x, y, z); return m; };
      for (const [x, r] of [[-.07, .12], [.08, -.12]]) { const s = new G0(); s.position.set(x, 0, 0); s.rotation.set(1.25, 0, r); s.add(mk(.2, .05, .44, '#2f7de1', 0, 0, 0), mk(.17, .05, .05, '#7fb6ff', 0, .05, .06)); g.add(s); }
      g.position.set(0, .6, .34); n.obj.userData.body.add(g); n.obj.userData.pair = g; }
    g.visible = v; };
  // move an npc for a staged beat (restored by __fix)
  window.__put = (n, x, z, face) => { if (n.spot) n.spot = Object.assign({}, n.spot, { x, z, face }); n.x = x; n.z = z; n.tx = null; n.tz = null; n.moving = false; n.state = 'work'; n.obj.position.set(x, P.surfaceY(x, z), z); n.obj.rotation.y = face; };
  window.__fix52 = () => { window.__fix51(); window.__ray(true, true); window.__cartPair(false); window.__handPair(false);
    for (const f of [window.__RAY, window.__FER, window.__RANU]) { const n = f(); if (!n) continue; n.obj.visible = true; const c = n.castSpot; if (c && n.spot) { n.spot = Object.assign({}, n.spot, c); n.obj.rotation.y = c.face; } if (c && Math.hypot(n.x - c.x, n.z - c.z) > .3) { n.x = c.x; n.z = c.z; n.tx = null; n.tz = null; n.moving = false; n.state = 'work'; n.obj.position.set(c.x, P.surfaceY(c.x, c.z) + (c.y || 0), c.z); n.obj.rotation.y = c.face; } } };
}"""
POS = """() => { const o = {}; for (const [k, f] of Object.entries({ dy: window.__DAY, ry: window.__RAY, fr: window.__FER, rn: window.__RANU })) { const n = f(); o[k] = n ? [n.name, +n.x.toFixed(2), +n.z.toFixed(2), +n.obj.position.y.toFixed(2), +n.obj.rotation.y.toFixed(2), n.role, (n.kit || []).length, (n.obj.userData.feet || []).length] : null; }
  for (const [k, b] of Object.entries(window.__B52)) o[k] = [b.position.x, b.position.y, b.position.z, b.rotation.y, b.scale.x]; return o; }"""
CLK = os.environ.get('CLK', '.62')
HEAD = """const P = window.__pulau; window.__fix52(); window.__clock = """ + CLK + """; window.__cheer = null; window.__cartPos = 1; P.player.obj.visible = false; P.scene.traverse(o => { const g = o.isInstancedMesh && o.geometry.parameters; if (g && ((g.height === 1.4 && g.radiusTop === .04) || (g.width === .18 && g.height === .22))) o.visible = false; }); """
def close(getter, Y, h, d0, d1=None, pitch=.1, dur=3.0, extra='', dyaw=0.0, cheer='null', ox=0.0, oz=0.0, frame=''):
    d1 = d0 - .3 if d1 is None else d1
    return """() => { """ + HEAD + extra + """ window.__cheer = """ + cheer + """; const n = """ + getter + """(), x = n.x + """ + str(ox) + """, z = n.z + """ + str(oz) + """, y = Math.max(n.obj.position.y, P.surfaceY(n.x, n.z)) + """ + str(h) + """;
  window.__look(x, z, """ + str(Y) + """, """ + str(pitch) + """, """ + str(d0) + """, false);
  window.__beforeRender = (dt, T) => { """ + frame + """ const q = Math.min(1, T / """ + str(dur) + """), e = q * q * (3 - 2 * q); window.__C(x, y, z); P.cam.dist = """ + str(d0) + """ + (""" + str(d1 - d0) + """) * e; P.cam.yaw = """ + str(Y) + """ + """ + str(dyaw) + """ * e; P.cam.pitch = """ + str(pitch) + """; window.__clr([n], x, z, .5); }; }"""
def bld(key, lx, lz, ly, Y0, Y1, p0, p1, d0, d1, dur, cheer='null', lx1=None, lz1=None, extra='', cart=None):
    lx1 = lx if lx1 is None else lx1; lz1 = lz if lz1 is None else lz1
    cj = '' if cart is None else f"{{ const c = Math.min(1, Math.max(0, (T - {cart[2]}) / ({cart[3]} - {cart[2]}))); window.__cartPos = {cart[0]} + ({cart[1] - cart[0]}) * c * c * (3 - 2 * c); }}"
    return """() => { """ + HEAD + extra + """ window.__cheer = """ + cheer + """; const o = window.__B52['""" + key + """'], k = o.scale.x || 1, a = o.position.clone().set(""" + f"{lx}*k, {ly}*k, {lz}*k" + """), b = o.position.clone().set(""" + f"{lx1}*k, {ly}*k, {lz1}*k" + """); o.localToWorld(a.divideScalar(k)); o.localToWorld(b.divideScalar(k));
  window.__look(a.x, a.z, """ + str(Y0) + """, """ + str(p0) + """, """ + str(d0) + """, false);
  window.__beforeRender = (dt, T) => { """ + cj + """ const q = Math.min(1, T / """ + str(dur) + """), e = q * q * (3 - 2 * q); const x = a.x + (b.x - a.x) * e, z = a.z + (b.z - a.z) * e;
    window.__C(x, a.y, z); P.cam.dist = """ + str(d0) + """ + (""" + str(d1 - d0) + """) * e; P.cam.yaw = """ + str(Y0) + """ + (""" + str(Y1 - Y0) + """) * e; P.cam.pitch = """ + str(p0) + """ + (""" + str(p1 - p0) + """) * e; window.__clr([], x, z, .6); }; }"""
E = os.environ.get
f = lambda k, d: float(E(k, d))
NOFISH = "window.__ray(false, false); "
PAIR = "window.__handPair(true); "
# c1 cold open (flash-forward): Rayhan close with the fish, sandals on
C1 = close('window.__RAY', f('Y1', '-.2'), f('H1', '1.1'), f('D1', '3.0'), f('D1', '3.0') - .5, pitch=f('P1', '.15'))
# c2 premise: aerial descending onto the harbour
C2 = bld('pelabuhan', 0, 0, 0, .5, .25, 1.1, .8, 55, 18, 4.0)
# c3 Rayhan, still apes: sandal on the hook (swap fish for nothing: rod only), no sandals on feet, side angle
C3 = close('window.__RAY', f('Y3', '-.5'), 1.0, 4.0, 3.3, pitch=.16, extra=NOFISH, dur=5.5, oz=.3)
# c4 flashback: the pair in the mine cart
C4 = bld('tambang', 0, 1.7, f('LY4', '1.0'), f('Y4', '.45'), f('Y4', '.45') + .25, .55, .45, 2.1, 1.6, 5.0, extra="window.__cartPair(true); ")
# c5 Dayang at the mine with the pair in her hands
C5 = close('window.__DAY', f('Y5', '.3'), 1.0, 2.6, 2.1, pitch=.12, extra=PAIR + "{ const t = window.__B52.tambang, v = t.position.clone().set(-1.2, 0, 2.6); t.localToWorld(v); window.__put(window.__DAY(), v.x, v.z, t.rotation.y); } ")
# c6 RANUUGLL stops her (two-shot, Dayang in front of him)
PUTR = PAIR + "{ const r = window.__RANU(); window.__put(window.__DAY(), r.x - 1.0, r.z + .9, 2.3); r.obj.rotation.y = -.84; if (r.spot) r.spot = Object.assign({}, r.spot, { face: -.84 }); } "
C6 = close('window.__RANU', f('Y6', '-.6'), 1.0, 2.6, 2.2, pitch=.12, extra=PUTR, ox=.1, oz=.1)
# c7 Dayang answers, Ranu escorts (two-shot wider)
C7 = close('window.__DAY', f('Y7', '2.1'), 1.0, 2.4, 3.8, pitch=.13, extra=PUTR, dyaw=.35, dur=5.0)
# c8 feros calls Rayhan
C8 = close('window.__FER', f('Y8', '.9'), 1.0, 2.6, 2.2, pitch=.12, extra=NOFISH + PAIR)
# c9 Rayhan + Dayang two-shot at the harbour (no fish, no sandals yet; pair in her hands)
C9 = close('window.__DAY', f('Y9', '-.5'), 1.0, 3.2, 2.6, pitch=.13, extra=NOFISH + PAIR, dur=6.0)
# c10 Rayhan close, sandals appear on his feet halfway (put on), then camera on the feet
C10 = close('window.__RAY', f('Y10', '.3'), f('H10', '.25'), 2.6, 2.2, pitch=.45, extra="window.__ray(false, false); ", frame="if (T > 2.4) window.__ray(false, true);", dur=4.5)
# c11 the tug: rod bends, fish appears
C11 = close('window.__RAY', f('Y11', '-1.45'), .9, 4.4, 3.8, pitch=.1, oz=.75, extra="window.__ray(false, true); ", frame="window.__ray(T > 1.5, true);", dur=3.0)
# c12 harbour wide, cheer
C12 = bld('pelabuhan', 0, 1.0, 0, f('Y12', '-.6'), f('Y12', '-.6') + .3, .45, .5, 8.0, 11.0, 5.0, cheer='true')
# c13 end: PAPAN TUGAS at the Pos Gotong Royong, crane up
C13 = bld('posgotong', 1.05, 1.45, .95, .1, .45, .1, .8, 1.6, 14, 7.0, cheer='true', lx1=0, lz1=.5)
SHOTS = {'c1': (C1, 140), 'c2': (C2, 135), 'c3': (C3, 205), 'c4': (C4, 155), 'c5': (C5, 135), 'c6': (C6, 115), 'c7': (C7, 190),
         'c8': (C8, 135), 'c9': (C9, 125), 'c10': (C10, 165), 'c11': (C11, 100), 'c12': (C12, 185), 'c13': (C13, 200)}
CLEAR = E51.CLEAR
async def run(which):
    async with async_playwright() as p:
        b, pg = await setup(p)
        for js in CHAIN + (SETUP52,): await pg.evaluate(js)
        if os.environ.get('VARS'): await pg.evaluate('() => { ' + os.environ['VARS'] + ' }')
        if 'pos' in which: print(await pg.evaluate(POS))
        for k, (js, n) in SHOTS.items():
            if k in which and 'prev' not in which:
                await shoot(pg, 'e52' + k, int(os.environ.get('N_' + k, n)), start_js=js, warm=12)
                await pg.evaluate(CLEAR)
        if 'prev' in which:
            for k, (js, n) in SHOTS.items():
                if 'all' not in which and k not in which: continue
                await shoot(pg, 'p52' + k, int(os.environ.get('PN', '1')), start_js=js, warm=int(os.environ.get('WARM', '40')))
                await pg.evaluate(CLEAR)
        await b.close()
if __name__ == "__main__": asyncio.run(run(sys.argv[1].split(",")))
