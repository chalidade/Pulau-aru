import asyncio,base64,sys
from playwright.async_api import async_playwright
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist'])
    pg=await b.new_page(viewport={'width':1024,'height':1024})
    pg.on('pageerror',lambda e:print('ERR',e)); pg.on('console',lambda m:print('C',m.text))
    for v in sys.argv[1:]:
      await pg.goto(f'http://localhost:8765/studio/logo/render.html?v={v}')
      await pg.wait_for_function('window.__done',timeout=120000)
      d=await pg.evaluate('window.__done'); open(f'{v}.png','wb').write(base64.b64decode(d.split(',')[1])); print(v)
    await b.close()
asyncio.run(main())
