#!/usr/bin/env python3
"""Pulau Netizen episode 6 "Jalan Baru" (60 s, 1080x1920): game footage + ElevenLabs narrator and character voices.
usage: ep4.py plan | preview <t,...> | render [ids] | audio | final
"""
import sys, os, json, math, subprocess, wave
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build as B
from build import W, H, FPS, INK, SAND, LAMP, font, PIX, BODY, BOLD, ITAL, wrap, ease, ease_out_back

CAP = os.environ.get('STUDIO_WORK', '/tmp/studio') + '/cap/'
VO = os.environ.get('VIGENCO', '/home/claude/vigenco') + '/voiceover/pulau-cara-ikut/'
OUT = os.environ.get('STUDIO_WORK', '/tmp/studio') + '/outK'
RES = json.load(open(VO + 'result.json'))['lines']
NAME = {'aru': 'ARU', 'presiden': 'PRESIDEN @Etet_443', 'wapres': 'WAPRES @EGA_91'}

# seg: footage (seq dir or 'undian'), mood, voiced lines [(start, line id)], overlays
SEGS = [
    dict(id='k1', seq='k1', mood='cheer', fade_in=.3, title=('CARA IKUT', 'Pulau Aru · pulau-aru.web.id', .2, 3.7), lines=[(.4, 'a1')]),
    dict(id='k2', seq='k2', mood='cheer', cards=[(.5, 7.4, 'LANGKAH 1', 'FOLLOW = JADI WARGA', 'namamu diukir di Batu Nama')], lines=[(.3, 'n1')]),
    dict(id='k3', seq='k3', mood='cheer', cards=[(.4, 9.0, 'SETIAP HARI', '2 KOMENTAR ACAK', 'diundi & diwujudkan')], comments=(2.6, 9.0), lines=[(.3, 'n2')]),
    dict(id='k4', seq='k4', mood='hype', cards=[(.3, 4.9, 'PRESIDEN · MENJABAT 1 MINGGU', '3 PERMINTAAN', 'tanpa undian'), (5.1, 7.6, 'WAKIL PRESIDEN · 1 MINGGU', '2 PERMINTAAN', 'tanpa undian')], lines=[(.3, 'p1'), (5.1, 'v1')]),
    dict(id='k5', seq='k5', mood='mystery', treat=(1.0, 11.6), lines=[(.3, 'n3')]),
    dict(id='k6', seq='k6', mood='cheer', urlcard=(.8, 6.6), lines=[(.3, 'n4')]),
    dict(id='k7', seq='k7', mood='hype', chips=[(0, 'JALAN-JALAN'), (3.5, 'PANJAT PIRAMIDA'), (4.9, 'TANGGA AWAN KE KOPDES'), (6.6, 'TANGKAP IKAN'), (7.9, 'BERLAYAR'), (9.55, 'CARI NAMAMU DI BATU')], lines=[(.3, 'n5')]),
    dict(id='k8', seq='k8', mood='ending', fade_out=.8, lines=[(.3, 'a2')], endcard=2.0),
]
TOTAL = None

def frames_in(s):
    d = CAP + s['seq']
    return sorted(f for f in os.listdir(d) if f.endswith('.jpg')) if os.path.isdir(d) else []

def seg_len(s, i=None):
    if s.get('undian'): return s['dur']
    base = len(frames_in(s)) / FPS or 4.0
    need = max([t + RES[l]['duration'] + .25 for t, l in s.get('lines', [])] + [0])
    L = max(base, need)
    return round(L * FPS) / FPS

def timeline():
    t = 0; out = []
    for s in SEGS: out.append((t, s)); t += seg_len(s)
    return out, t

# ---------------------------------------------------------------- overlays
F_DLG = font(BODY, 46); F_NAME = font(PIX, 38); F_NAR = font(BODY, 50)
def shown_chars(line_id, tl):
    """characters revealed as the voice speaks them (word timings from ElevenLabs)"""
    r = RES[line_id]; text = r['text']; pos = 0; shown = 0
    for w in r['words']:
        j = text.find(w['text'], pos)
        if j < 0: continue
        pos = j + len(w['text'])
        if w['start'] <= tl: shown = pos
    return len(text) if tl >= r['duration'] else shown

def speaker_box(name, text, shown, tl):
    layer = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(layer)
    bx, bw = 56, W - 56 - 150
    lines = wrap(d, text, F_DLG, bw - 72); lh = 62; bh = 52 + lh * len(lines) + 22; by = 1480 - bh
    sc = .86 + .14 * ease_out_back(tl / .22)
    box = Image.new('RGBA', (bw, bh), (0, 0, 0, 0)); bd = ImageDraw.Draw(box)
    bd.rounded_rectangle((0, 8, bw - 1, bh - 1), 14, fill=(0, 0, 0, 90))
    bd.rounded_rectangle((0, 0, bw - 1, bh - 9), 14, fill=SAND + (246,), outline=INK + (255,), width=5)
    y = 30; left = shown
    for ln in lines:
        bd.text((36, y), ln[:max(0, left)], font=F_DLG, fill=INK); left -= len(ln) + 1; y += lh
    if sc < .999: box = box.resize((max(1, int(bw * sc)), max(1, int(bh * sc))), Image.BICUBIC)
    layer.alpha_composite(box, (bx + (bw - box.width) // 2, by + (bh - box.height) // 2))
    tw = int(d.textlength(name, font=F_NAME)) + 44
    tag = Image.new('RGBA', (tw, 62), (0, 0, 0, 0)); td = ImageDraw.Draw(tag)
    td.rounded_rectangle((0, 0, tw - 1, 61), 10, fill=INK + (255,))
    td.text((tw // 2, 30), name, font=F_NAME, fill=LAMP, anchor='mm')
    layer.alpha_composite(tag, (bx + 26, by - 40))
    return layer

def narrator_caption(text, shown, tl, dur):
    """narration: a cinematic subtitle on a soft dark band, no box"""
    layer = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(layer)
    a = min(1, tl / .25, max(0, (dur + .5 - tl) / .3))
    lines = wrap(d, text, F_NAR, W - 300)
    y0 = 1330 - 70 * len(lines); top, bot = y0 - 110, y0 + 70 * len(lines) + 90
    for y in range(top, bot):
        k = min(1, (y - top) / 90, (bot - y) / 90)
        d.line([(0, y), (W, y)], fill=(5, 14, 18, int(135 * k * a)))
    y = y0; left = shown
    for ln in lines:
        d.text((W // 2 - 70, y), ln[:max(0, left)], font=F_NAR, fill=(250, 244, 228, int(255 * a)), anchor='ma', stroke_width=3, stroke_fill=(5, 14, 18, int(255 * a)))
        left -= len(ln) + 1; y += 70
    return layer

ATT = '/mnt/user-data/attachments/d8a8f54d-3261-580a-b176-410c1c3e68e9/'
COMMENTS = {'aspal': (ATT + 'e895623f-image.jpg', 'TERPILIH'), 'sekolah': (ATT + '779c8416-image.jpg', 'TERPILIH')}
TREAT = 'teer.id/chalidade'
CARD_T = {}
DECREE = ATT + 'dfa7065a-image.jpg'
_U = {}
def word_time(line_id, word):
    for w in RES[line_id]['words']:
        if w['text'].lower().startswith(word.lower()): return w['start']
    return None

def undian_frame(t):
    if 'bg' not in _U:
        src = sorted(os.listdir(CAP + 'e6c2'))[-1]
        bg = Image.open(CAP + 'e6c2/' + src).resize((W, H), Image.LANCZOS).filter(ImageFilter.GaussianBlur(14))
        _U['bg'] = Image.blend(bg, Image.new('RGB', (W, H), INK), .55)
        _U['cards'] = []
        for k, (pth, tag) in COMMENTS.items():
            im = Image.open(pth).convert('RGB'); sc = 900 / im.width; im = im.resize((900, int(im.height * sc)), Image.LANCZOS)
            m = Image.new('L', im.size, 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, im.width - 1, im.height - 1), 26, fill=255)
            c = Image.new('RGBA', im.size); c.paste(im, (0, 0), m)
            t0 = CARD_T[k] if k in CARD_T else .4 + (word_time('n2', k) or 3.0)
            _U['cards'].append((c, t0, tag))
    img = _U['bg'].copy().convert('RGBA'); d = ImageDraw.Draw(img)
    d.text((W // 2, 300), 'UNDIAN KOMENTAR', font=B.F_UT, fill=LAMP, anchor='mm', stroke_width=6, stroke_fill=INK)
    d.text((W // 2, 380), 'acak · tanpa hadiah', font=B.F_US, fill=SAND, anchor='mm')
    first = _U['cards'][0][1]
    if t < first - .1:
        d.rounded_rectangle((140, 560, W - 140, 700), 28, fill=SAND + (255,), outline=INK + (255,), width=6)
        d.text((W // 2, 630), B.SPIN[int(t * 14) % len(B.SPIN)], font=B.F_UN, fill=INK, anchor='mm')
    y = 440
    for card, t0, tag in _U['cards']:
        if t < t0 - .15: break
        p = ease_out_back((t - t0 + .15) / .4); sc = .6 + .4 * p
        c = card.resize((max(1, int(card.width * sc)), max(1, int(card.height * sc))), Image.BICUBIC)
        x0 = (W - c.width) // 2; img.alpha_composite(c, (x0, y))
        if t - t0 > .2:
            tw = d.textlength(tag, font=B.F_US) + 40
            d.rounded_rectangle((W - 120 - tw, y - 26, W - 120, y + 30), 28, fill=LAMP + (255,), outline=INK + (255,), width=4)
            d.text((W - 120 - tw / 2, y + 2), tag, font=B.F_US, fill=INK, anchor='mm')
        y += card.height + 70
    return img.convert('RGB')

F_E1 = font(BOLD, 40); F_EU = font(PIX, 86); F_EB = font(ITAL, 60)
def end_layer(t, t0):
    layer = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(layer)
    k = t - t0
    if k < 0: return layer
    a = int(255 * min(1, k / .5)); d.rectangle((0, 0, W, H), fill=(5, 14, 18, int(160 * min(1, k / .5))))
    y = 470 + int((1 - ease_out_back(k / .5)) * 60)
    rows = [('1', 'Follow akun ini', 'jadi warga + namamu di batu'), ('2', 'Komentar usulanmu', '2 diwujudkan setiap hari'), ('3', 'Traktir = langsung jadi', TREAT)]
    for i, (n, h1, h2) in enumerate(rows):
        yy = y + i * 170
        d.ellipse((150, yy - 50, 250, yy + 50), fill=LAMP + (a,), outline=INK + (a,), width=5); d.text((200, yy), n, font=font(PIX, 64), fill=INK + (a,), anchor='mm')
        d.text((290, yy - 24), h1, font=font(BOLD, 52), fill=(255, 255, 255, a), anchor='lm'); d.text((290, yy + 30), h2, font=font(BODY, 40), fill=SAND + (a,), anchor='lm')
    if k > .6:
        a2 = int(255 * min(1, (k - .6) / .4)); yy = y + 3 * 170 + 40
        d.rounded_rectangle((W // 2 - 400, yy, W // 2 + 400, yy + 130), 26, fill=LAMP + (a2,), outline=INK + (a2,), width=6)
        d.text((W // 2, yy + 65), 'pulau-aru.web.id', font=F_EU, fill=INK + (a2,), anchor='mm')
    return layer

F_CJK = ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc', 46)
def title_fit(t1, t2, t, t0, t1end):
    """title card whose headline shrinks to fit the frame"""
    layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    k = t - t0; out = max(0, (t - (t1end - .35)) / .35)
    if k < 0 or out >= 1: return layer
    p = ease_out_back(k / .45); a = int(255 * (1 - out))
    size = 150
    while size > 60 and ImageDraw.Draw(layer).textlength(t1, font=font(PIX, size)) > W - 120: size -= 6
    F1 = font(PIX, size)
    txt = Image.new('RGBA', (W, 400), (0, 0, 0, 0)); td = ImageDraw.Draw(txt)
    td.text((W // 2 + 7, 167), t1, font=F1, fill=INK + (a,), anchor='mm')
    td.text((W // 2, 160), t1, font=F1, fill=LAMP + (a,), anchor='mm', stroke_width=6, stroke_fill=INK + (a,))
    if k > .3:
        F2 = F_CJK if any(ord(ch) > 0x2000 for ch in t2) else B.F_T2
        a2 = int(a * min(1, (k - .3) / .3)); tw = td.textlength(t2, font=F2)
        td.rounded_rectangle((W // 2 - tw / 2 - 26, 262, W // 2 + tw / 2 + 26, 336), 37, fill=INK + (int(a2 * .9),))
        td.text((W // 2, 299), t2, font=F2, fill=SAND + (a2,), anchor='mm')
    sc = .5 + .5 * p; txt = txt.resize((int(W * sc), int(400 * sc)), Image.BICUBIC)
    layer.alpha_composite(txt, ((W - txt.width) // 2, 250 + (400 - txt.height) // 2))
    return layer

_M = {}
def map_card(t, t0, t1):
    """the back of Aru's old map: a lighthouse drawn in ink, one of its three lamps lit"""
    layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    k = t - t0
    if k < 0 or t > t1: return layer
    if 'card' not in _M:
        cw, ch = 640, 820; c = Image.new('RGBA', (cw, ch), (0, 0, 0, 0)); d = ImageDraw.Draw(c)
        d.rounded_rectangle((0, 10, cw - 1, ch - 1), 18, fill=(0, 0, 0, 90))
        d.rounded_rectangle((0, 0, cw - 1, ch - 11), 18, fill=(236, 218, 176, 255), outline=(120, 88, 50, 255), width=6)
        rng = np.random.default_rng(5)
        for _ in range(900):
            x, y = rng.integers(10, cw - 10), rng.integers(10, ch - 20); d.point((int(x), int(y)), fill=(196, 170, 120, 255))
        ink = (70, 48, 30, 255); cx = cw // 2
        d.polygon([(cx - 80, 690), (cx + 80, 690), (cx + 50, 310), (cx - 50, 310)], outline=ink, width=6)
        for yy in (440, 570): d.line([(cx - 50 - (yy - 310) * 30 // 380, yy), (cx + 50 + (yy - 310) * 30 // 380, yy)], fill=ink, width=5)
        d.rectangle((cx - 95, 195, cx + 95, 310), outline=ink, width=6)
        d.polygon([(cx - 115, 195), (cx + 115, 195), (cx, 115)], outline=ink, width=6)
        d.line([(40, 700), (cw - 40, 700)], fill=ink, width=5)
        for i in range(5): d.arc((60 + i * 110, 715, 150 + i * 110, 760), 200, 340, fill=ink, width=4)
        lamps = [(cx - 56, 252), (cx, 252), (cx + 56, 252)]
        for i, (x, y) in enumerate(lamps):
            if i == 1:
                glow = Image.new('RGBA', (cw, ch), (0, 0, 0, 0)); gd = ImageDraw.Draw(glow)
                gd.ellipse((x - 55, y - 55, x + 55, y + 55), fill=(255, 190, 60, 210)); glow = glow.filter(ImageFilter.GaussianBlur(16)); c.alpha_composite(glow)
                d.ellipse((x - 24, y - 24, x + 24, y + 24), fill=(255, 205, 70, 255), outline=ink, width=5)
            else: d.ellipse((x - 22, y - 22, x + 22, y + 22), fill=(120, 100, 80, 255), outline=ink, width=5)
        d.text((cx, 62), '1 dari 3', font=font(ITAL, 44), fill=ink, anchor='mm')
        _M['card'] = c.rotate(-4, resample=Image.BICUBIC, expand=True)
    c = _M['card']; p = ease_out_back(k / .5); out = max(0, (t - (t1 - .35)) / .35); sc = (.4 + .32 * p) * (1 - .1 * out)
    cc = c.resize((max(1, int(c.width * sc)), max(1, int(c.height * sc))), Image.BICUBIC)
    if out > 0: cc.putalpha(cc.getchannel('A').point(lambda v: int(v * (1 - out))))
    layer.alpha_composite(cc, (60 + (int(c.width * .72) - cc.width) // 2, 140 + (int(c.height * .72) - cc.height) // 2))
    return layer

F_K1 = font(BOLD, 36); F_K3 = font(BODY, 40)
def info_card(t, t0, t1, eyebrow, head, sub):
    layer = Image.new('RGBA', (W, H), (0, 0, 0, 0)); k = t - t0
    if k < 0 or t > t1: return layer
    out = max(0, (t - (t1 - .3)) / .3); a = int(255 * (1 - out)); p = ease_out_back(k / .45)
    size = 92
    while size > 50 and ImageDraw.Draw(layer).textlength(head, font=font(PIX, size)) > W - 200: size -= 4
    F2 = font(PIX, size); cw = W - 120; ch = 300
    c = Image.new('RGBA', (cw, ch), (0, 0, 0, 0)); d = ImageDraw.Draw(c)
    d.rounded_rectangle((0, 10, cw - 1, ch - 1), 26, fill=(0, 0, 0, 80))
    d.rounded_rectangle((0, 0, cw - 1, ch - 11), 26, fill=INK + (235,), outline=LAMP + (255,), width=5)
    d.text((cw // 2, 62), eyebrow, font=F_K1, fill=SAND + (255,), anchor='mm')
    d.text((cw // 2, 148), head, font=F2, fill=LAMP + (255,), anchor='mm', stroke_width=3, stroke_fill=INK + (255,))
    d.text((cw // 2, 232), sub, font=F_K3, fill=SAND + (255,), anchor='mm')
    sc = .7 + .3 * p; c = c.resize((int(cw * sc), int(ch * sc)), Image.BICUBIC)
    if a < 255: c.putalpha(c.getchannel('A').point(lambda v: v * a // 255))
    layer.alpha_composite(c, ((W - c.width) // 2, 230 + (ch - c.height) // 2)); return layer

_CM = {}
def comment_cards(t, t0, t1):
    layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    if t < t0 or t > t1: return layer
    if not _CM:
        for k, (pth, tag) in COMMENTS.items():
            im = Image.open(pth).convert('RGB'); sc = 820 / im.width; im = im.resize((820, int(im.height * sc)), Image.LANCZOS)
            m = Image.new('L', im.size, 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, im.width - 1, im.height - 1), 24, fill=255)
            c = Image.new('RGBA', im.size); c.paste(im, (0, 0), m); _CM[k] = c
    y = 590
    for i, c in enumerate(_CM.values()):
        k = t - t0 - i * .5
        if k < 0: break
        p = ease_out_back(k / .4); cc = c.resize((max(1, int(c.width * (.6 + .4 * p))), max(1, int(c.height * (.6 + .4 * p)))), Image.BICUBIC)
        layer.alpha_composite(cc, ((W - cc.width) // 2, y)); y += c.height + 30
    return layer

def chip(t, chips):
    layer = Image.new('RGBA', (W, H), (0, 0, 0, 0)); cur = None
    for t0, lab in chips:
        if t >= t0: cur = (t0, lab)
    if not cur: return layer
    k = t - cur[0]; d = ImageDraw.Draw(layer); F = font(PIX, 64); tw = d.textlength(cur[1], font=F)
    p = ease_out_back(k / .3); y = 300 - int((1 - p) * 60)
    d.rounded_rectangle((W // 2 - tw / 2 - 40, y - 56, W // 2 + tw / 2 + 40, y + 56), 30, fill=LAMP + (255,), outline=INK + (255,), width=6)
    d.text((W // 2, y), cur[1], font=F, fill=INK, anchor='mm'); return layer

def big_url(t, t0, t1, eyebrow, url, sub, stamp=None):
    layer = Image.new('RGBA', (W, H), (0, 0, 0, 0)); k = t - t0
    if k < 0 or t > t1: return layer
    out = max(0, (t - (t1 - .3)) / .3); a = int(255 * (1 - out)); d = ImageDraw.Draw(layer)
    p = ease_out_back(k / .5); y = 330 - int((1 - p) * 80)
    d.text((W // 2, y), eyebrow, font=font(PIX, 70), fill=LAMP + (a,), anchor='mm', stroke_width=5, stroke_fill=INK + (a,))
    if k > .4:
        a2 = int(a * min(1, (k - .4) / .3)); Fu = font(PIX, 80); tw = d.textlength(url, font=Fu)
        d.rounded_rectangle((W // 2 - tw / 2 - 40, y + 70, W // 2 + tw / 2 + 40, y + 200), 26, fill=LAMP + (a2,), outline=INK + (a2,), width=6)
        d.text((W // 2, y + 135), url, font=Fu, fill=INK + (a2,), anchor='mm')
        d.text((W // 2, y + 250), sub, font=font(BOLD, 42), fill=(255, 255, 255, a2), anchor='mm', stroke_width=4, stroke_fill=INK + (a2,))
    if stamp and k > stamp:
        q = min(1, (k - stamp) / .18); st = Image.new('RGBA', (560, 140), (0, 0, 0, 0)); sd = ImageDraw.Draw(st)
        sd.rounded_rectangle((6, 6, 553, 133), 14, outline=(214, 48, 49, 255), width=9); sd.text((280, 70), 'TANPA UNDIAN', font=font(PIX, 68), fill=(214, 48, 49, 255), anchor='mm')
        st = st.rotate(-8, expand=True, resample=Image.BICUBIC); z = 1.8 - .8 * q; st = st.resize((int(st.width * z), int(st.height * z)), Image.BICUBIC)
        st.putalpha(st.getchannel('A').point(lambda v: int(v * q * a / 255)))
        layer.alpha_composite(st, ((W - st.width) // 2, y + 300))
    return layer

_D = {}
def decree_card(t, t0, t1):
    layer = Image.new('RGBA', (W, H), (0, 0, 0, 0)); k = t - t0
    if k < 0 or t > t1: return layer
    if 'c' not in _D:
        im = Image.open(DECREE).convert('RGB'); sc = 900 / im.width; im = im.resize((900, int(im.height * sc)), Image.LANCZOS)
        m = Image.new('L', im.size, 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, im.width - 1, im.height - 1), 26, fill=255)
        c = Image.new('RGBA', im.size); c.paste(im, (0, 0), m); _D['c'] = c
        st = Image.new('RGBA', (520, 130), (0, 0, 0, 0)); sd = ImageDraw.Draw(st)
        sd.rounded_rectangle((6, 6, 513, 123), 14, outline=(214, 48, 49, 255), width=9)
        sd.text((260, 66), 'TANPA UNDIAN', font=font(PIX, 64), fill=(214, 48, 49, 255), anchor='mm')
        _D['s'] = st.rotate(-9, expand=True, resample=Image.BICUBIC)
    c = _D['c']; out = max(0, (t - (t1 - .3)) / .3); p = ease_out_back(k / .4); sc = .6 + .4 * p
    cc = c.resize((max(1, int(c.width * sc)), max(1, int(c.height * sc))), Image.BICUBIC)
    if out: cc.putalpha(cc.getchannel('A').point(lambda v: int(v * (1 - out))))
    y = 330; layer.alpha_composite(cc, ((W - cc.width) // 2, y + (c.height - cc.height) // 2))
    if k > 1.2:
        q = min(1, (k - 1.2) / .18); s2 = _D['s']; z = 1.8 - .8 * q
        st = s2.resize((int(s2.width * z), int(s2.height * z)), Image.BICUBIC)
        a = int(255 * q * (1 - out)); st.putalpha(st.getchannel('A').point(lambda v: v * a // 255))
        layer.alpha_composite(st, (W - 110 - st.width, y + c.height + 30))
    return layer

def compose(s, t, base):
    img = base.convert('RGBA')
    if 'title' in s: img.alpha_composite(title_fit(*s['title'][:2], t, *s['title'][2:]))
    if 'stat' in s: img.alpha_composite(B.stat_layer(*s['stat'][:2], t, *s['stat'][2:]))
    for c in s.get('cards', []): img.alpha_composite(info_card(t, *c))
    if 'comments' in s: img.alpha_composite(comment_cards(t, *s['comments']))
    if 'chips' in s: img.alpha_composite(chip(t, s['chips']))
    if 'treat' in s: img.alpha_composite(big_url(t, *s['treat'], 'MAU LANGSUNG JADI?', TREAT, 'traktir, lalu tulis request-mu', stamp=4.5))
    if 'urlcard' in s: img.alpha_composite(big_url(t, *s['urlcard'], 'SEMUANYA ADA DI', 'pulau-aru.web.id', 'kunjungi kapan saja, gratis'))
    if 'banner' in s: img.alpha_composite(B.banner_layer(*s['banner'][:2], t, *s['banner'][2:]))
    if 'place' in s: img.alpha_composite(B.place_layer(*s['place'][:2], t, *s['place'][2:]))
    active = [(t0, l) for t0, l in s.get('lines', []) if t0 <= t]
    ec = s.get('endcard')
    if active and not (ec and t >= ec):
        t0, l = active[-1]; r = RES[l]; tl = t - t0
        if r['who'] == 'narrator':
            if tl < r['duration'] + .8: img.alpha_composite(narrator_caption(r['text'], shown_chars(l, tl), tl, r['duration']))
        else:
            img.alpha_composite(speaker_box(NAME[r['who']], r['text'], shown_chars(l, tl), tl))
    if ec: img.alpha_composite(end_layer(t, ec))
    out = img.convert('RGB')
    L = seg_len(s); fi = s.get('fade_in', 0); fo = s.get('fade_out', 0); k = 1.0
    if fi and t < fi: k = t / fi
    if fo and t > L - fo: k = min(k, (L - t) / fo)
    if k < 1: out = Image.eval(out, lambda v: int(v * max(0, k)))
    return out

def base_frame(s, f):
    if s.get('undian'): return undian_frame(f / FPS)
    fs = frames_in(s)
    return Image.open(CAP + s['seq'] + '/' + fs[min(f, len(fs) - 1)]).convert('RGB').resize((W, H), Image.LANCZOS)

def render_seg(s):
    n = int(round(seg_len(s) * FPS)); dst = f'{OUT}/seg_{s["id"]}.mp4'; tmp = dst + '.tmp.mp4'
    enc = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', '30', '-i', '-',
                            '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '19', '-pix_fmt', 'yuv420p', '-r', '30', tmp], stdin=subprocess.PIPE)
    for f in range(n): enc.stdin.write(compose(s, f / FPS, base_frame(s, f)).tobytes())
    enc.stdin.close(); assert enc.wait() == 0; os.replace(tmp, dst)
    print(f'seg_{s["id"]} {n / FPS:.2f}s', flush=True)

# ---------------------------------------------------------------- audio
S = B.S
def load_mp3(path):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', path, '-ac', '1', '-ar', str(S.SR), '-f', 's16le', '-'], capture_output=True).stdout
    return np.frombuffer(raw, np.int16).astype(float) / 32768

def crowd_cheer(d=2.4):
    y = S.band_noise(d, 250, 3200, seed=21) * .5 + S.band_noise(d, 900, 5000, seed=22) * .3
    tt = S.t_axis(d); env = np.minimum(1, tt / .15) * np.exp(-np.maximum(0, tt - .9) / .7)
    am = 1 + .35 * np.sin(2 * np.pi * 5.5 * tt) * np.sin(2 * np.pi * .7 * tt)
    return y * env * am * .6

def murmur(d):
    y = S.band_noise(d, 200, 1400, seed=31); tt = S.t_axis(d)
    return y * (.6 + .4 * np.sin(2 * np.pi * 1.3 * tt + np.sin(tt * 3))) * .14

def build_audio(path):
    tl, total = timeline()
    music = S.Bus(total); sfx = S.Bus(total); voice = S.Bus(total)
    runs = []
    for (t, s) in tl:
        L = seg_len(s)
        if runs and runs[-1][0] == s['mood']: runs[-1][2] = t + L
        else: runs.append([s['mood'], t, t + L])
    for mood, a, b in runs:
        m = S.Bus(b - a); B.music(m, mood, 0, b - a)
        n = int((b - a) * S.SR); env = np.ones(n); fi = int(.12 * S.SR); fo = int(.35 * S.SR)
        env[:fi] = np.linspace(0, 1, fi); env[-fo:] = np.linspace(1, 0, fo)
        music.add(m.L[:n] * env, a, 1.0, pan=-1); music.add(m.R[:n] * env, a, 1.0, pan=1)
    for (t, s) in tl:
        for t0, l in s.get('lines', []):
            v = load_mp3(VO + l + '.mp3'); voice.add(v, t + t0, 1.0)
        for key in ('title', 'banner', 'place'):
            if key in s: sfx.add(S.sfx_whoosh(1.0), t + s[key][2], .8); sfx.add(S.sfx_shimmer(), t + s[key][2] + .25, .5)
        if 'cheer' in s: sfx.add(crowd_cheer(), t + s['cheer'], 1.0)
        for c in s.get('cards', []): sfx.add(S.sfx_whoosh(.6), t + c[0], .5); sfx.add(S.sfx_chime([72, 79]), t + c[0] + .2, .4)
        for c0, _ in s.get('chips', []): sfx.add(S.sfx_tick(3), t + c0, .8)
        if 'treat' in s: sfx.add(S.sfx_shimmer(), t + s['treat'][0], .6); sfx.add(S.sfx_chime([60, 67]), t + s['treat'][0] + 4.5, .6)
        if 'urlcard' in s: sfx.add(S.sfx_chime([76, 81, 84]), t + s['urlcard'][0] + .4, .5)
        if s.get('market'): sfx.add(murmur(seg_len(s)), t, 1.0)
        if s.get('undian'):
            for k in range(int(max(0, _card_times()[0]) * 14)): sfx.add(S.sfx_tick(k), t + k / 14, .7)
            for c in _card_times(): sfx.add(S.sfx_chime([76, 81, 84]), t + c, .55)
        if s.get('endcard'): sfx.add(S.sfx_chime([72, 76, 79, 84]), t + s['endcard'], .7)
    n = int(total * S.SR)
    # duck the music under speech
    vmono = np.abs(voice.L[:n] + voice.R[:n])
    win = int(.05 * S.SR); envv = np.convolve(vmono, np.ones(win) / win, mode='same')
    duck = 1 - .62 * np.clip(envv / (np.percentile(envv[envv > 1e-4], 60) + 1e-9), 0, 1)
    sm = int(.25 * S.SR); duck = np.convolve(duck, np.ones(sm) / sm, mode='same')
    L = music.L[:n] * duck * .55 + sfx.L[:n] + voice.L[:n] * 1.25
    R = music.R[:n] * duck * .55 + sfx.R[:n] + voice.R[:n] * 1.25
    st = np.stack([L, R], 1); st = st / (np.max(np.abs(st)) + 1e-9) * .89
    with wave.open(path, 'wb') as wv:
        wv.setnchannels(2); wv.setsampwidth(2); wv.setframerate(S.SR); wv.writeframes((st * 32767).astype('<i2').tobytes())
    return total

def _card_times():
    return [CARD_T[k] if k in CARD_T else .4 + (word_time('n2', k) or 3.0) for k in COMMENTS]

if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    cmd = sys.argv[1]
    if cmd == 'plan':
        tl, total = timeline()
        for t, s in tl: print(f'{t:6.2f} {seg_len(s):5.2f} {s["id"]} {s.get("seq", "undian")} frames={len(frames_in(s)) if s.get("seq") else "-"}')
        print('total', round(total, 2))
    elif cmd == 'preview':
        tl, total = timeline()
        for ts in sys.argv[2].split(','):
            T = float(ts)
            for t, s in tl:
                if t <= T < t + seg_len(s): break
            f = int((T - t) * FPS); compose(s, f / FPS, base_frame(s, f)).save(f'{OUT}/prev_{T:05.2f}.jpg', quality=88)
    elif cmd == 'render':
        only = sys.argv[2].split(',') if len(sys.argv) > 2 else None
        for s in SEGS:
            if only is None or s['id'] in only: render_seg(s)
    elif cmd == 'audio':
        print('audio', build_audio(f'{OUT}/audio.wav'))
    elif cmd == 'final':
        open(f'{OUT}/list.txt', 'w').write(''.join(f"file 'seg_{s['id']}.mp4'\n" for s in SEGS))
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', f'{OUT}/list.txt', '-c', 'copy', f'{OUT}/video.mp4'], check=True)
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', f'{OUT}/video.mp4', '-i', f'{OUT}/audio.wav', '-map', '0:v', '-map', '1:a', '-c:v', 'copy',
                        '-af', 'loudnorm=I=-14:TP=-1.5:LRA=11', '-ar', '48000', '-c:a', 'aac', '-b:a', '192k', '-shortest', '-movflags', '+faststart', f'{OUT}/final.tmp.mp4'], check=True)
        os.replace(f'{OUT}/final.tmp.mp4', f'{OUT}/pulau-aru-cara-ikut.mp4'); print('done')
