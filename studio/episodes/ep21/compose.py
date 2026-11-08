#!/usr/bin/env python3
"""Pulau Aru episode 21 "Bengkel Pulau" (copied from episode 20).
Copy to studio/episodes/epN/compose.py, edit SEGS/COMMENTS/texts, run with EP=N. (60 s, 1080x1920): game footage + ElevenLabs narrator and character voices.
usage: ep4.py plan | preview <t,...> | render [ids] | audio | final
"""
import sys, os, json, math, subprocess, wave
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'lib'))
import build as B
from build import W, H, FPS, INK, SAND, LAMP, font, PIX, BODY, BOLD, ITAL, wrap, ease, ease_out_back

B.SPIN = ['warga', 'netizen']
WORK = os.environ.get('STUDIO_WORK', '/tmp/studio')
CAP = WORK + '/cap/'
EP = int(os.environ.get('EP', '21'))
VO = os.environ.get('VIGENCO', '/home/claude/vigenco') + f'/voiceover/pulau-ep{EP}/'
OUT = WORK + f'/out{EP}'
RES = json.load(open(VO + 'result.json'))['lines']
NAME = {'ega': "PRESIDEN 'EGA_", 'aru': 'ARU', 'kingindo': 'WAPRES KING INDO', 'penjual': 'wibu cilik pelenger', 'alexandre': 'Alexandre', 'luci': 'Luci Ardiansyah',
        'fattan': 'KM GPP TAN', 'daby': 'D..A..B..Y a..j..a', 'princes': 'princes_nay', 'whoyss': 'whoyss'}

# seg: footage (seq dir or 'undian'), mood, voiced lines [(start, line id)], overlays
SC = os.path.dirname(os.path.abspath(__file__)) + '/'
CY = 1640
SEGS = [
    dict(id='h0', seq='e21c1', mood='hype', capy=CY, hook=('RODA GEROBAK', 'KABUR!', 0, 2.6), lines=[(0.05, 's1')]),
    dict(id='s2', seq='e21c2', mood='hype', capy=CY, title=('ALEXANDRE', 'Si Pahlawan', .1, 2.4), lines=[(.1, 'x1')]),
    dict(id='s3', seq='e21c3', mood='sad', capy=CY, title=('5 MENIT KEMUDIAN', 'rodanya... miring', .05, 2.0), lines=[(.3, 'x2')]),
    dict(id='s4', seq='e21c4', mood='hype', capy=CY, title=('LUCI', 'Si Sok Tahu', .1, 2.2), lines=[(.1, 'l1'), (4.05, 'a1')]),
    dict(id='s5', seq='e21c5', mood='mystery', capy=CY, usulan=(.3, 3.6), lines=[(.1, 'n2'), (3.5, 'f1')]),
    dict(id='s6', seq='e21c6', mood='cheer', capy=CY, lines=[(.1, 'e1')]),
    dict(id='s6b', seq='e21c6', mood='cheer', capy=CY, **{'from': 100}, lines=[(.1, 'k1'), (2.35, 'e2')]),
    dict(id='s7', seq='e21c7', mood='cheer', capy=CY, cheer=.3, title=('BENGKEL PULAU', 'usulan warga · jalan silang', .3, 4.2), lines=[(.4, 'n3')]),
    dict(id='s8', seq='e21c8', mood='hype', capy=CY, title=('KLUB PERTAMA', 'selalu ribut', .1, 1.6), lines=[(.5, 'd1'), (1.9, 'h1')]),
    dict(id='s9', seq='e21c9', mood='cheer', capy=CY, lines=[(.1, 's2')]),
    dict(id='s10', seq='e21c10', mood='cheer', capy=CY, title=('WARTEG DIBUKA', 'ruang keenam di pulau', .1, 2.8), lines=[(.1, 'a2')]),
    dict(id='s11', seq='e21c11', mood='mystery', capy=CY, title=('WHOYSS', 'Si Iseng', 4.0, 6.3), lines=[(.1, 'n4'), (4.0, 'w1')]),
    dict(id='s12', seq='e21c12', mood='ending', cheer=.2, fade_out=.6, lines=[(.1, 'n5')], endcard=5.1),
]
TOTAL = 60.0

def frames_in(s):
    d = CAP + s['seq']
    return sorted(f for f in os.listdir(d) if f.endswith('.jpg')) if os.path.isdir(d) else []

def seg_len(s, i=None):
    if s.get('undian'): return round((.1 + RES[s['line']]['duration'] + .35) * FPS) / FPS
    if s.get('dur'): return round(s['dur'] * FPS) / FPS
    base = max(0, len(frames_in(s)) - s.get('from', 0)) / FPS or 4.0
    need = max([t + RES[l]['duration'] + .2 for t, l in s.get('lines', [])] + [0])
    L = need if need > 0 else base   # tight: each shot lasts as long as its voice lines (retention)
    if s is SEGS[-1]:   # the last shot holds under the end card so the episode lands on 60 s
        L = TOTAL - sum(seg_len(x) for x in SEGS[:-1])
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

# the two chosen comments: key = a word the narrator says when the card should pop (from line n2),
# value = (username, comment text, tag). A value may also be (path to a screenshot, tag).
HERE = os.path.dirname(os.path.abspath(__file__)) + '/'
COMMENTS = {}
CARD_T = {}
UNDIAN_BG = 'e21c7'     # capture folder whose last frame, blurred, sits behind the comment cards
DECREE = None   # (username, text) for a 'decree' segment, or None
def comment_card(user, text, width=900, avatar=None):
    """a TikTok-style comment drawn from text: the real profile photo (avatar = path from studio/comments.json, downloaded
    by the comments workflow) or an initial, the exact username, comment, reply row"""
    F_U = ImageFont.truetype(B.F + 'rethink-latin-500-normal.ttf', 30); F_T = ImageFont.truetype(B.F + 'rethink-latin-500-normal.ttf', 40)
    try: F_J = ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc', 30)
    except Exception: F_J = F_U
    d0 = ImageDraw.Draw(Image.new('RGB', (10, 10))); lines = wrap(d0, text, F_T, width - 200)
    h = 120 + 52 * len(lines) + 40
    c = Image.new('RGBA', (width, h), (0, 0, 0, 0)); d = ImageDraw.Draw(c)
    d.rounded_rectangle((0, 0, width - 1, h - 1), 26, fill=(255, 255, 255, 255))
    hue = sum(map(ord, user)) % 6; col = [(232, 98, 82), (86, 154, 214), (98, 178, 120), (226, 170, 66), (150, 110, 200), (70, 170, 170)][hue]
    d.ellipse((34, 34, 124, 124), fill=col); d.text((79, 80), (user.strip('@._ ') or '?')[0].upper(), font=ImageFont.truetype(B.F + 'rethink-latin-700-normal.ttf', 46), fill=(255, 255, 255), anchor='mm')
    if avatar and os.path.exists(avatar):
        try:
            av = Image.open(avatar).convert('RGB').resize((90, 90), Image.LANCZOS); m = Image.new('L', (90, 90), 0); ImageDraw.Draw(m).ellipse((0, 0, 89, 89), fill=255)
            c.paste(av, (34, 34), m)
        except Exception: pass
    fu = F_J if any(ord(ch) > 0x2000 for ch in user) else F_U
    d.text((150, 44), user, font=fu, fill=(120, 120, 120)); y = 88
    for ln in lines: d.text((150, y), ln, font=F_T, fill=(20, 20, 20)); y += 52
    d.text((150, y + 8), 'Reply', font=F_U, fill=(130, 130, 130))
    return c

def comment_image(path, width=900):
    im = Image.open(path).convert('RGB'); sc = width / im.width; im = im.resize((width, int(im.height * sc)), Image.LANCZOS)
    m = Image.new('L', im.size, 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, im.width - 1, im.height - 1), 26, fill=255)
    c = Image.new('RGBA', im.size); c.paste(im, (0, 0), m); return c

_U = {}
def word_time(line_id, word):
    for w in RES[line_id]['words']:
        if w['text'].lower().startswith(word.lower()): return w['start']
    return None

def card_t(s, when):
    return when if isinstance(when, (int, float)) else .1 + (word_time(s['line'], when) or 2.0)

def undian_frame(s, t):
    key = s['id']
    if key not in _U:
        bgd = s.get('bg', UNDIAN_BG); src = sorted(os.listdir(CAP + bgd))[-1]
        bg = Image.open(CAP + bgd + '/' + src).resize((W, H), Image.LANCZOS).filter(ImageFilter.GaussianBlur(14))
        _U[key] = (Image.blend(bg, Image.new('RGB', (W, H), INK), .55), [(comment_image(SC + f, 470), tag, card_t(s, w)) for f, tag, w in s['cards']])
    bg, cards = _U[key]
    img = bg.copy().convert('RGBA'); d = ImageDraw.Draw(img)
    d.text((W // 2, 300), s['head'][0], font=B.F_UT, fill=LAMP, anchor='mm', stroke_width=6, stroke_fill=INK)
    d.text((W // 2, 380), s['head'][1], font=B.F_US, fill=SAND, anchor='mm')
    FT = font(BOLD, 34)
    for i, (card, tag, t0) in enumerate(cards):
        if t < t0 - .15: break
        col, row = i % 2, i // 2; cx = 290 + col * 500; y = 470 + row * 300
        if i == len(cards) - 1 and len(cards) % 2: cx = W // 2
        p = ease_out_back((t - t0 + .15) / .4); sc = .6 + .4 * p
        c = card.resize((max(1, int(card.width * sc)), max(1, int(card.height * sc))), Image.BICUBIC)
        img.alpha_composite(c, (cx - c.width // 2, y + (card.height - c.height) // 2))
        if t - t0 > .2:
            tw = d.textlength(tag, font=FT) + 36; ty = y + card.height + 34
            d.rounded_rectangle((cx - tw / 2, ty - 27, cx + tw / 2, ty + 27), 27, fill=LAMP + (255,), outline=INK + (255,), width=4)
            d.text((cx, ty), tag, font=FT, fill=INK, anchor='mm')
    return img.convert('RGB')

F_E1 = font(BOLD, 40); F_EU = font(PIX, 86); F_EB = font(ITAL, 60)
def end_layer(t, t0):
    layer = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(layer)
    k = t - t0
    if k < 0: return layer
    a = int(255 * min(1, k / .5)); d.rectangle((0, 0, W, H), fill=(5, 14, 18, int(150 * min(1, k / .5))))
    y = 560 + int((1 - ease_out_back(k / .5)) * 60)
    d.text((W // 2, y), 'Bengkel Pulau sudah buka di pulau', font=F_E1, fill=SAND + (a,), anchor='mm')
    d.text((W // 2, y + 66), 'Kendaraan apa', font=font(PIX, 64), fill=LAMP + (a,), anchor='mm', stroke_width=4, stroke_fill=INK + (a,))
    d.text((W // 2, y + 138), 'yang harus ada?', font=font(PIX, 64), fill=LAMP + (a,), anchor='mm', stroke_width=4, stroke_fill=INK + (a,))
    if k > .6:
        a2 = int(255 * min(1, (k - .6) / .4))
        d.rounded_rectangle((W // 2 - 400, y + 230, W // 2 + 400, y + 360), 26, fill=LAMP + (a2,), outline=INK + (a2,), width=6)
        d.text((W // 2, y + 295), 'pulau-aru.web.id', font=F_EU, fill=INK + (a2,), anchor='mm')
        d.text((W // 2, y + 410), 'tulis di komentar · mampir ke bengkelnya', font=font(BODY, 34), fill=SAND + (a2,), anchor='mm')
        d.text((W // 2, y + 460), 'Punya usaha? Komentar #UMKMPulauAru nama - jenis - IG/WA', font=font(BODY, 34), fill=SAND + (a2,), anchor='mm')
    if k > 1.6:
        a3 = int(255 * min(1, (k - 1.6) / .5))
        d.text((W // 2, 1200), 'Bersambung…', font=F_EB, fill=(255, 255, 255, a3), anchor='mm', stroke_width=4, stroke_fill=INK + (a3,))
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
            if i in (0, 1, 2):
                glow = Image.new('RGBA', (cw, ch), (0, 0, 0, 0)); gd = ImageDraw.Draw(glow)
                gd.ellipse((x - 55, y - 55, x + 55, y + 55), fill=(255, 190, 60, 210)); glow = glow.filter(ImageFilter.GaussianBlur(16)); c.alpha_composite(glow)
                d.ellipse((x - 24, y - 24, x + 24, y + 24), fill=(255, 205, 70, 255), outline=ink, width=5)
            else: d.ellipse((x - 22, y - 22, x + 22, y + 22), fill=(120, 100, 80, 255), outline=ink, width=5)
        d.text((cx, 62), '3 dari 3', font=font(ITAL, 44), fill=ink, anchor='mm')
        _M['card'] = c.rotate(-4, resample=Image.BICUBIC, expand=True)
    c = _M['card']; p = ease_out_back(k / .5); out = max(0, (t - (t1 - .35)) / .35); sc = (.4 + .32 * p) * (1 - .1 * out)
    cc = c.resize((max(1, int(c.width * sc)), max(1, int(c.height * sc))), Image.BICUBIC)
    if out > 0: cc.putalpha(cc.getchannel('A').point(lambda v: int(v * (1 - out))))
    layer.alpha_composite(cc, (60 + (int(c.width * .72) - cc.width) // 2, 140 + (int(c.height * .72) - cc.height) // 2))
    return layer

_UI = {}
def ui_card(t, t0, t1, fname='kebun_ui.png', w=600, y0=170):
    layer = Image.new('RGBA', (W, H), (0, 0, 0, 0)); k = t - t0
    if k < 0 or t > t1: return layer
    if fname not in _UI:
        im = Image.open(WORK + '/' + fname).convert('RGB'); im = im.resize((w, int(im.height * w / im.width)), Image.LANCZOS)
        c = Image.new('RGBA', (w + 24, im.height + 24), (0, 0, 0, 0)); d = ImageDraw.Draw(c)
        d.rounded_rectangle((0, 0, c.width - 1, c.height - 1), 34, fill=INK + (255,))
        m = Image.new('L', im.size, 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, im.width - 1, im.height - 1), 24, fill=255); c.paste(im, (12, 12), m)
        _UI[fname] = c.rotate(3, expand=True, resample=Image.BICUBIC)
    c = _UI[fname]; p = ease_out_back(k / .45); out = max(0, (t - (t1 - .3)) / .3); sc = (.55 + .45 * p) * (1 - .1 * out)
    cc = c.resize((max(1, int(c.width * sc)), max(1, int(c.height * sc))), Image.BICUBIC)
    if out: cc.putalpha(cc.getchannel('A').point(lambda v: int(v * (1 - out))))
    layer.alpha_composite(cc, ((W - cc.width) // 2 + 40, y0 + (c.height - cc.height) // 2))
    return layer

_P = {}
def paper_card(key, title, lines, t, t0, t1, ink=(70, 48, 30), rot=-4, y0=150, strike=False):
    """a hand-written paper note that pops in (the letter from the lighthouse keeper, the residents' list)"""
    layer = Image.new('RGBA', (W, H), (0, 0, 0, 0)); k = t - t0
    if k < 0 or t > t1: return layer
    if key not in _P:
        cw = 760; Ft = font(ITAL, 50); Fl = font(ITAL, 44); dd = ImageDraw.Draw(Image.new('RGB', (9, 9)))
        wl = [w for ln in lines for w in (wrap(dd, ln, Fl, cw - 110) or [''])]
        ch = 150 + 62 * len(wl) + 60; c = Image.new('RGBA', (cw, ch), (0, 0, 0, 0)); d = ImageDraw.Draw(c)
        d.rounded_rectangle((0, 10, cw - 1, ch - 1), 16, fill=(0, 0, 0, 90))
        d.rounded_rectangle((0, 0, cw - 1, ch - 11), 16, fill=(240, 226, 192, 255), outline=(150, 112, 70, 255), width=5)
        rng = np.random.default_rng(len(key))
        for _ in range(700): d.point((int(rng.integers(8, cw - 8)), int(rng.integers(8, ch - 18))), fill=(205, 182, 136, 255))
        d.text((cw // 2, 70), title, font=Ft, fill=ink + (255,), anchor='mm'); d.line([(60, 112), (cw - 60, 112)], fill=ink + (255,), width=3)
        y = 140
        for ln in wl:
            d.text((56, y), ln, font=Fl, fill=ink + (255,))
            if strike and ln.startswith('-'): d.line([(56, y + 30), (56 + d.textlength(ln, font=Fl), y + 26)], fill=(192, 57, 43, 255), width=5)
            y += 62
        _P[key] = c.rotate(rot, expand=True, resample=Image.BICUBIC)
    c = _P[key]; p = ease_out_back(k / .45); out = max(0, (t - (t1 - .3)) / .3); sc = (.55 + .45 * p) * (1 - .08 * out)
    cc = c.resize((max(1, int(c.width * sc)), max(1, int(c.height * sc))), Image.BICUBIC)
    if out: cc.putalpha(cc.getchannel('A').point(lambda v: int(v * (1 - out))))
    layer.alpha_composite(cc, ((W - cc.width) // 2, y0 + (c.height - cc.height) // 2))
    return layer

_BADGE = {}
_D = {}
def decree_card(t, t0, t1):
    layer = Image.new('RGBA', (W, H), (0, 0, 0, 0)); k = t - t0
    if k < 0 or t > t1: return layer
    if 'c' not in _D:
        _D['c'] = comment_card(*DECREE) if isinstance(DECREE, tuple) else comment_image(DECREE)
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

# ---------------------------------------------------------------- retention helpers
CAPTIONS = 'pop'          # 'pop' = big word-by-word captions in the middle (TikTok style); 'box' = old boxes
BADGE = f'EP {EP} · PULAU ARU'
F_POP = font(PIX, 74); F_POPN = font(BOLD, 34); F_HOOK = font(PIX, 92); F_BADGE = font(BOLD, 30)
def pop_caption(line_id, tl, who, y=1250):
    """3-word chunks timed to the voice, current word in yellow, big and centred (never a slow typewriter)"""
    layer = Image.new('RGBA', (W, H), (0, 0, 0, 0)); r = RES[line_id]; words = r['words']
    if not words or tl > r['duration'] + .35: return layer
    i = 0
    for k, w in enumerate(words):
        if w['start'] <= tl: i = k
    c0 = (i // 3) * 3; chunk = words[c0:c0 + 3]
    d = ImageDraw.Draw(layer); texts = [w['text'] for w in chunk]
    size = 74
    while size > 46 and d.textlength(' '.join(texts), font=font(PIX, size)) > W - 120: size -= 4
    F = font(PIX, size); total = d.textlength(' '.join(texts), font=F); x = (W - total) / 2
    if who != 'narrator':
        name = NAME.get(who, who.upper()); tw = d.textlength(name, font=F_POPN) + 36
        d.rounded_rectangle((W / 2 - tw / 2, y - 112, W / 2 + tw / 2, y - 58), 10, fill=INK + (235,)); d.text((W / 2, y - 85), name, font=F_POPN, fill=LAMP, anchor='mm')
    for k, tx in enumerate(texts):
        cur = c0 + k == i; pop = 1 + .12 * max(0, 1 - (tl - chunk[k]['start']) / .15) if cur else 1
        Fk = font(PIX, int(size * pop)) if pop > 1.001 else F
        d.text((x, y), tx, font=Fk, fill=LAMP if cur else (255, 255, 255), anchor='lm', stroke_width=7, stroke_fill=INK)
        x += d.textlength(tx + ' ', font=F)
    return layer

# hook position: below TikTok's top tabs and inside the 3:4 profile-grid crop (y 240..1680), big enough to read
# as a thumbnail. Was y=300 / 92px (sat under the "Following | For You" tabs and looked tiny in the grid).
HOOK_Y, HOOK_SIZE = 600, 128
def hook_layer(l1, l2, t, t0, t1):
    """the first-second hook: two big lines on a slanted yellow band, popping in immediately"""
    layer = Image.new('RGBA', (W, H), (0, 0, 0, 0)); k = t - t0
    if k < 0 or t > t1: return layer
    out = max(0, (t - (t1 - .2)) / .2); a = int(255 * (1 - out)); d = ImageDraw.Draw(layer)
    p = min(1, .7 + k / .12 * .3)
    for j, ln in enumerate([l1, l2]):
        if not ln: continue
        size = int(HOOK_SIZE * p)
        while size > 50 and d.textlength(ln, font=font(PIX, size)) > W - 120: size -= 4
        F = font(PIX, size); tw = d.textlength(ln, font=F); y = HOOK_Y + j * (int(HOOK_SIZE * p) + 40)
        band = Image.new('RGBA', (int(tw + 60), size + 30), LAMP + (a,) if j == 0 else (255, 255, 255, a)); band = band.rotate(-2 if j == 0 else 1.5, expand=True, resample=Image.BICUBIC)
        layer.alpha_composite(band, (int((W - band.width) / 2), int(y - band.height / 2)))
        d.text((W // 2, y), ln, font=F, fill=INK + (a,), anchor='mm')
    return layer

def badge_layer():
    layer = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(layer); tw = d.textlength(BADGE, font=F_BADGE)
    d.rounded_rectangle((40, 40, 40 + tw + 32, 92), 26, fill=INK + (190,)); d.text((56, 66), BADGE, font=F_BADGE, fill=SAND, anchor='lm')
    return layer

def punch(img, t, amount=.08, dur=.28):
    """quick zoom-in settle on every cut: a small pattern interrupt that keeps the eye"""
    if t >= dur: return img
    z = 1 + amount * (1 - t / dur) ** 2; w, h = img.size; cw, ch = int(w / z), int(h / z)
    return img.crop(((w - cw) // 2, (h - ch) // 2, (w - cw) // 2 + cw, (h - ch) // 2 + ch)).resize((w, h), Image.BILINEAR)

def compose(s, t, base):
    if s.get('lift'): g = 1 / s['lift']; base = base.point([int(255 * (v / 255) ** g) for v in range(256)] * 3)
    if s.get('punch', True) and not s.get('undian'): base = punch(base, t)
    img = base.convert('RGBA')
    if 'hook' in s: img.alpha_composite(hook_layer(*s['hook'][:2], t, *s['hook'][2:]))
    if 'title' in s: img.alpha_composite(title_fit(*s['title'][:2], t, *s['title'][2:]))
    if 'stat' in s: img.alpha_composite(B.stat_layer(*s['stat'][:2], t, *s['stat'][2:]))
    if 'decree' in s: img.alpha_composite(decree_card(t, *s['decree']))
    if 'banner' in s: img.alpha_composite(B.banner_layer(*s['banner'][:2], t, *s['banner'][2:]))
    if 'place' in s: img.alpha_composite(B.place_layer(*s['place'][:2], t, *s['place'][2:]))
    if 'mapcard' in s: img.alpha_composite(map_card(t, *s['mapcard']))
    if 'uicard' in s: img.alpha_composite(ui_card(t, *s['uicard']))
    if 'letter' in s: img.alpha_composite(paper_card('letter', 'Untuk Aru', ['Pemimpin pulau', 'harus dipilih warga,', 'bukan ditunjuk.', '', '— Penjaga Mercusuar'], t, *s['letter']))
    if 'usulan' in s: img.alpha_composite(paper_card('usulan', 'Kotak Usulan', ['- BENGKEL  <- !!!', '- hotel', '- apartemen'], t, *s['usulan'], ink=(30, 40, 60), rot=3))
    if 'notes' in s: img.alpha_composite(paper_card('notes', 'Catatan Warga', ['- ambil gorengan (ep 9)', '- tidur waktu ronda (ep 10)', '- makan mangga (ep 11)'], t, *s['notes'], ink=(30, 40, 60), rot=3))
    active = [(t0, l) for t0, l in s.get('lines', []) if t0 <= t]
    ec = s.get('endcard')
    if active and not (ec and t >= ec):
        t0, l = active[-1]; r = RES[l]; tl = t - t0
        if CAPTIONS == 'pop': img.alpha_composite(pop_caption(l, tl, r['who'], s.get('capy', 1250)))
        elif r['who'] == 'narrator':
            if tl < r['duration'] + .8: img.alpha_composite(narrator_caption(r['text'], shown_chars(l, tl), tl, r['duration']))
        else:
            img.alpha_composite(speaker_box(NAME[r['who']], r['text'], shown_chars(l, tl), tl))
    if ec: img.alpha_composite(end_layer(t, ec))
    if not ec or t < ec: img.alpha_composite(_BADGE.setdefault('b', badge_layer()))
    out = img.convert('RGB')
    L = seg_len(s); fi = s.get('fade_in', 0); fo = s.get('fade_out', 0); k = 1.0
    if fi and t < fi: k = t / fi
    if fo and t > L - fo: k = min(k, (L - t) / fo)
    if k < 1: out = Image.eval(out, lambda v: int(v * max(0, k)))
    return out

def base_frame(s, f):
    if s.get('undian'): return undian_frame(s, f / FPS)
    fs = frames_in(s)[s.get('from', 0):]
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

def knock(d=.35):
    """a hollow wooden 'tok' (kentongan)"""
    tt = S.t_axis(d); env = np.exp(-tt / .045)
    y = (np.sin(2 * np.pi * 520 * tt) * .8 + np.sin(2 * np.pi * 1180 * tt) * .3) * env + S.band_noise(d, 800, 3000, seed=7) * np.exp(-tt / .01) * .4
    return y * .9

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
        if 'uicard' in s: sfx.add(S.sfx_whoosh(.8), t + s['uicard'][0], .6); sfx.add(S.sfx_chime([72, 79]), t + s['uicard'][0] + .3, .5)
        if 'mapcard' in s: sfx.add(S.sfx_chime([64, 71]), t + s['mapcard'][0], .5)
        for key in ('letter', 'notes', 'usulan'):
            if key in s: sfx.add(S.sfx_whoosh(.6), t + s[key][0], .6); sfx.add(S.sfx_chime([62, 69]), t + s[key][0] + .3, .45)
        if 'decree' in s: sfx.add(S.sfx_whoosh(.6), t + s['decree'][0], .6); sfx.add(S.sfx_chime([60, 67]), t + s['decree'][0] + 1.2, .6)
        if s.get('market'): sfx.add(murmur(seg_len(s)), t, 1.0)
        for k0 in s.get('kentongan', ()):
            sfx.add(knock(), t + k0, .9)
        if s.get('undian'):
            for _, _, w in s['cards']: sfx.add(S.sfx_chime([76, 81, 84]), t + card_t(s, w), .55)
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
    return [CARD_T[k] if k in CARD_T else .4 + (word_time('n1', k) or 3.0) for k in COMMENTS]

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
        os.replace(f'{OUT}/final.tmp.mp4', f'{OUT}/pulau-netizen-ep{EP}-hook.mp4'); print('done')
