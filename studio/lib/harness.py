"""Frame-stepped Playwright capture of the game (deterministic time, canvas grabs).
usage from a shots script: b, pg = await setup(p); await shoot(pg, name, frames, per_frame_js, start_js, warm)
"""
import asyncio, json, sys, time, os, base64
from playwright.async_api import async_playwright

INIT = """
(() => {
  let now = 0; const q = [];
  performance.now = () => now;
  window.requestAnimationFrame = cb => { q.push(cb); return q.length; };
  window.cancelAnimationFrame = () => {};
  window.__step = (ms, n = 1) => { for (let i = 0; i < n; i++) { now += ms; const c = q.splice(0); for (const f of c) f(now); } };
})();
"""
CAP = os.environ.get('STUDIO_WORK', '/tmp/studio') + '/cap'
BOATS = [[45, 101], [49, 99], [61, 100], [65, 102]]

async def setup(p, url=os.environ.get('STUDIO_URL', 'http://localhost:8765/')):
    b = await p.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'])
    ctx = await b.new_context(viewport={'width': 432, 'height': 768}, device_scale_factor=float(os.environ.get('DPR','2')))
    pg = await ctx.new_page(); pg.set_default_timeout(900000)
    pg.on('pageerror', lambda e: print('PAGEERROR', e))
    await pg.route('**/fonts.googleapis.com/**', lambda r: r.abort())
    await pg.add_init_script(INIT)
    await pg.goto(url, wait_until='domcontentloaded')
    for _ in range(40):
        await pg.evaluate('window.__step && window.__step(33.333, 3)')
        if await pg.evaluate("!document.getElementById('st-aru').disabled"): break
        await pg.wait_for_timeout(250)
    await pg.evaluate("document.getElementById('st-aru').click()")
    await pg.evaluate("window.__pulau.toggleRec(); const st=document.createElement('style'); st.textContent='#toast,#hint,#unpub,#prompt,#unhide{display:none!important}'; document.head.appendChild(st)")
    return b, pg

async def shoot(pg, name, frames, per_frame_js=None, start_js=None, warm=20):
    out = f"{CAP}/{name}"; os.makedirs(out, exist_ok=True)
    if start_js: await pg.evaluate(start_js)
    await pg.evaluate(f'window.__step(33.333, {warm})')
    t0 = time.time()
    await pg.evaluate("() => { window.__afterRender = c => { window.__frame = c.toDataURL('image/jpeg', 0.93); }; }")
    for f in range(frames):
        if per_frame_js: await pg.evaluate(per_frame_js, f)
        url = await pg.evaluate('() => { window.__step(33.333, 1); return window.__frame; }')
        open(f'{out}/{f:04d}.jpg', 'wb').write(base64.b64decode(url.split(',', 1)[1]))
    print(name, frames, 'frames', round(time.time() - t0, 1), 's', flush=True)
