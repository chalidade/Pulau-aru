#!/usr/bin/env python3
"""Shared helpers for Pulau Aru videos: fonts, title/banner/stat layers, music moods, synth sfx.
(Originally the episode 3 editor; its own clip list is unused by the daily episodes.)
usage: build.py preview <seconds,...>   |   build.py render
"""
import sys, os, json, math, subprocess, shutil, wave
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

A = '/mnt/user-data/attachments/d8a8f54d-3261-580a-b176-410c1c3e68e9/'
CLIP = {
    'c01': '27182166-1000458335', 'c02': '986d29b1-1000458336', 'c03': '8865eba6-1000458337',
    'c04': 'c52856e6-1000458338', 'c05': 'b579ac9a-1000458339', 'c06': 'd25bff33-1000458340',
    'c07': '42c8a91c-1000458341', 'c08': '7e7c2338-1000458342', 'c09': '6d4a70a2-1000458343',
    'c10': 'f8139407-1000458344', 'c11': 'c2d7ff67-1000458345', 'c12': '1e62c5c2-1000458346',
    'c13': '7e345503-1000458347',
}
W, H, FPS = 1080, 1920, 30
OUT = os.environ.get('STUDIO_WORK', '/tmp/studio') + '/out-ep3'
F = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'fonts') + '/'
def font(name, size): return ImageFont.truetype(F + name, size)
PIX = 'pixelify-latin-700-normal.ttf'; BODY = 'rethink-latin-500-normal.ttf'; BOLD = 'rethink-latin-700-normal.ttf'; ITAL = 'rethink-latin-400-italic.ttf'

INK = (15, 42, 49); SAND = (244, 230, 198); LAMP = (255, 201, 74); CORAL = (255, 138, 114)

# ---------------------------------------------------------------- the edit
# seg: clip, in, out, speed, mood (music), lines [(start, who, text, opts)], extras
# who: 'aru' dialog box, 'warga:<name>' chat bubble. opts: slow, top, shout
SEGS = [
    dict(id='01-pagi', clip='c01', a=0.0, b=9.0, speed=1.0, mood='cheer', fade_in=.4,
         title=('HARI KE-3', 'Pulau Netizen', .2, 3.4),
         lines=[(3.2, 'aru', 'Hari ketiga! Aru, penjaga pulau, melapor dari puncak piramida.', {}),
                (6.6, 'aru', '…yang tingginya sepuluh meter. Siapa yang minta ini, @VANZwlee?!', {'shout': True})]),
    dict(id='02-kampung', clip='c04', a=0.0, b=6.0, speed=1.0, mood='cheer',
         stat=('1.932', 'WARGA', .1, 3.0),
         lines=[(2.6, 'aru', 'Kemarin aku masih hafal nama kalian satu-satu.', {})]),
    dict(id='03-kampung2', clip='c06', a=0.0, b=6.1, speed=1.0, mood='cheer',
         lines=[(0.1, 'aru', 'Sekarang? Seribu sembilan ratus tiga puluh dua.', {}),
                (3.0, 'aru', 'Aku bahkan lupa jalan pulang ke tendaku sendiri.', {}),
                (5.2, 'warga:@warga', 'Aru nyasar di pulau sendiri wkwk', {})]),
    dict(id='04-rumah', clip='c05', a=0.0, b=4.43, speed=1.0, mood='cheer',
         lines=[(0.2, 'aru', 'Mereka lagi bikin rumah buat warga baru. Aku bantu… nonton.', {})]),
    dict(id='05-mancing', clip='c07', a=0.0, b=8.4, speed=0.85, mood='cheer',
         lines=[(0.3, 'aru', 'Itu warga lagi mancing. Aku? Kemarin nombak ikan, meleset dua belas kali.', {}),
                (4.6, 'warga:@warga', 'Aru kalah sama ikan', {}),
                (6.4, 'aru', 'HEI. Aku lihat komentar itu.', {'shout': True}),
                (8.6, 'aru', 'Tapi @Akai, tombakmu bagus kok. Yang jelek tanganku.', {})]),
    # ---- sisipan: request warga (32 s) ----
    dict(id='r1-request', seq='/tmp/claude-0/cap/A', mood='cheer',
         banner=('DARI KOMENTAR KALIAN', 'REQUEST WARGA', .2, 2.6),
         lines=[(1.4, 'aru', 'Ngomong-ngomong soal ikan… kemarin kalian kirim request!', {})]),
    dict(id='r2-undian', undian=True, dur=5.3, mood='cheer',
         lines=[(3.5, 'aru', 'Dua sekaligus? Oke, oke. Aku kerjain.', {})]),
    dict(id='r3-perahu', seq='/tmp/claude-0/cap/C', mood='cheer',
         place=('PERAHU NELAYAN', 'usulan @Pinjam seratus', .3, 4.6),
         lines=[(0.4, 'aru', 'Perahu nelayan sudah siap. Warga bisa cari ikan sampai ke tengah laut, atau jalan-jalan ke pulau seberang.', {}),
                (5.6, 'aru', 'Aku? Aku tetap di darat. Ikannya masih dendam sama aku.', {})]),
    dict(id='r4-lahan', seq='/tmp/claude-0/cap/D', mood='hype', rumble=1.33,
         title=('+ LAHAN BARU', 'usulan @riski', 5.0, 8.8),
         lines=[(0.3, 'aru', 'Dan pulaunya… kita perluas!', {'shout': True}),
                (3.0, 'aru', 'Lahan baru buat rumah kalian. Soalnya kemarin aku nggak kebagian tempat tidur.', {})]),
    dict(id='r5-makasih', seq='/tmp/claude-0/cap/E', mood='cheer', fade_out=.5,
         lines=[(0.2, 'aru', 'Makasih @Pinjam seratus dan @riski. Request kalian jadi kenyataan.', {})]),
    dict(id='06-senja', clip='c03', a=0.0, b=7.0, speed=0.8, mood='dusk', fade_in=.5,
         lines=[(1.4, 'aru', 'Kalian tahu nggak… malam pertama di sini, aku nggak tidur.', {'slow': True})]),
    dict(id='07-kilas', clip='c02', a=0.0, b=2.8, speed=0.6, mood='sad', gray=True, fade_in=.6, fade_out=.6,
         tag='Malam pertama',
         lines=[(0.6, 'aru', 'Gelap. Cuma aku, ombak, dan batu yang masih kosong.', {'slow': True})]),
    dict(id='08-lampu', clip='c02', a=7.4, b=14.9, speed=0.62, mood='sad', fade_in=.6, fade_out=.8,
         lines=[(0.8, 'aru', 'Sekarang lihat. Tiap lampu itu satu orang.', {'slow': True}),
                (4.4, 'aru', 'Satu dari kalian.', {'slow': True}),
                (7.0, 'aru', 'Jadi kalau ada yang nanya aku masih kesepian atau nggak…', {'slow': True}),
                (11.0, 'aru', '…nggak. Udah nggak.', {'slow': True})]),
    dict(id='09-kapal', clip='c07', a=8.4, b=16.9, speed=1.0, mood='hype', horn=0.25,
         banner=('MILESTONE 1.000 WARGA', 'KAPAL PERTAMA DATANG', 1.1, 5.2),
         lines=[(1.0, 'aru', 'EH?! KAPAL?! Sejak kapan?!', {'shout': True}),
                (4.6, 'aru', 'Siapa yang pesan?!', {'shout': True})]),
    dict(id='10-naik', clip='c08', a=0.0, b=10.6, speed=1.0, mood='hype',
         lines=[(0.3, 'aru', 'Aku nggak tahu cara nyetir kapal.', {}),
                (2.9, 'aru', 'Tapi aku penjaga pulau. Jadi… AYO BERLAYAR!', {'shout': True}),
                (8.1, 'aru', 'Sengaja. Itu manuver.', {})]),
    dict(id='11-laut', clip='c08', a=10.8, b=20.4, speed=1.0, mood='sail',
         lines=[(1.2, 'aru', 'Dari sini pulau kita kelihatan kecil banget, ya.', {}),
                (5.0, 'aru', 'Padahal semua yang ada di sana… kalian yang bikin.', {})]),
    dict(id='12-malam', clip='c10', a=0.0, b=20.4, speed=2.0, mood='sail',
         lines=[(2.0, 'aru', 'Eh… itu apa?', {}), (6.2, 'aru', 'Daratan? Ada pulau lain?!', {'shout': True})],
         place=('PULAU SEBERANG', 'belum bernama', 8.0, 10.2)),
    dict(id='13-dermaga', clip='c11', a=0.0, b=12.6, speed=1.6, mood='mystery',
         lines=[(0.6, 'aru', 'Dermaganya tua. Berarti… dulu ada orang di sini.', {'slow': True})]),
    dict(id='14-peti', clip='c11', a=13.0, b=17.4, speed=1.0, mood='mystery', fade_out=.5,
         lines=[(0.3, 'aru', 'Peta. Pulau kita dilingkari merah. Dan ada tulisan…', {'slow': True, 'top': True})]),
    dict(id='15-pesan', card=True, dur=5.4, mood='cliff', fade_in=.3,
         card_lines=[(0.5, '"Untuk Aru, kalau aku tidak kembali."', 'quote'), (3.4, '…Siapa yang tahu namaku?', 'small')]),
    dict(id='16-bukit', clip='c12', a=0.0, b=12.2, speed=1.0, mood='ending', fade_in=.6,
         lines=[(0.6, 'aru', 'Oke. Aku butuh bantuan kalian.', {}),
                (3.2, 'aru', 'Pulau ini belum punya nama.', {}),
                (5.7, 'aru', "Kalau aku yang namain, jadinya 'Pulau Aru 2'. Jelek banget.", {}),
                (9.5, 'aru', 'Kapalnya ada di dermaga. Siapa pun boleh naik.', {})]),
    dict(id='17-akhir', clip='c13', a=0.0, b=11.3, speed=1.0, mood='ending', fade_out=1.0,
         lines=[(0.2, 'aru', 'Tulis di komentar: namanya apa, dan kita bangun apa pertama.', {}),
                (4.1, 'aru', 'Sampai ketemu, warga. Dan jangan ketawain caraku nangkap ikan.', {})],
         endcard=(7.0,)),
]

CPS_NORMAL, CPS_SLOW = 30, 19
def type_dur(text, o): return len(text) / (CPS_SLOW if o.get('slow') else CPS_NORMAL)

def seg_len(s):
    if s.get('card') or s.get('undian'): return s['dur']
    if s.get('seq'): base = len([f for f in os.listdir(s['seq']) if f.endswith('.jpg')]) / FPS if os.path.isdir(s['seq']) else 9.0
    else: base = (s['b'] - s['a']) / s['speed']
    need = 0
    for (t, who, text, o) in s.get('lines', []):
        need = max(need, t + type_dur(text, o) + (1.8 if o.get('slow') else 1.25))
    if s.get('endcard'): need = max(need, s['endcard'][0] + 3.6)
    return round(max(base, need) * FPS) / FPS

# ---------------------------------------------------------------- drawing helpers
def wrap(draw, text, fnt, maxw):
    words, lines, cur = text.split(' '), [], ''
    for w_ in words:
        t = (cur + ' ' + w_).strip()
        if draw.textlength(t, font=fnt) <= maxw: cur = t
        else: lines.append(cur); cur = w_
    if cur: lines.append(cur)
    return lines

def ease_out_back(x):
    x = min(1, max(0, x)); c1 = 1.70158; c3 = c1 + 1
    return 1 + c3 * (x - 1) ** 3 + c1 * (x - 1) ** 2

def ease(x): x = min(1, max(0, x)); return 1 - (1 - x) ** 3

F_DLG = font(BODY, 46); F_DLGB = font(BOLD, 48); F_NAME = font(PIX, 40)
def dialog_layer(text, shown, o, t_line, pos_top=False):
    """Game-style dialog box (matches the game's in-game box), text typed up to `shown` chars."""
    layer = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(layer)
    fnt = F_DLGB if o.get('shout') else F_DLG
    bx, bw = 56, W - 56 - 150          # keep clear of TikTok's right-side buttons
    lines = wrap(d, text, fnt, bw - 72)
    lh = 62; bh = 52 + lh * len(lines) + 22
    by = 300 if pos_top else 1480 - bh   # above TikTok's caption area
    pop = ease_out_back(t_line / .22); sc = .86 + .14 * pop
    # shadow + box
    box = Image.new('RGBA', (bw, bh), (0, 0, 0, 0)); bd = ImageDraw.Draw(box)
    bd.rounded_rectangle((0, 8, bw - 1, bh - 1), 14, fill=(0, 0, 0, 90))
    bd.rounded_rectangle((0, 0, bw - 1, bh - 9), 14, fill=SAND + (246,), outline=INK + (255,), width=5)
    y = 30
    left = shown
    for ln in lines:
        part = ln[:max(0, left)]; left -= len(ln) + 1
        bd.text((36, y), part, font=fnt, fill=INK)
        y += lh
    # blinking "next" arrow when fully typed
    if shown >= len(text) and int(t_line * 2.2) % 2 == 0:
        bd.polygon([(bw - 52, bh - 46), (bw - 30, bh - 46), (bw - 41, bh - 32)], fill=INK)
    if sc < .999:
        box = box.resize((max(1, int(bw * sc)), max(1, int(bh * sc))), Image.BICUBIC)
    layer.alpha_composite(box, (bx + (bw - box.width) // 2, by + (bh - box.height) // 2))
    # name tag
    tag = Image.new('RGBA', (170, 64), (0, 0, 0, 0)); td = ImageDraw.Draw(tag)
    td.rounded_rectangle((0, 0, 169, 63), 10, fill=INK + (255,))
    td.text((85, 31), 'ARU', font=F_NAME, fill=LAMP, anchor='mm')
    layer.alpha_composite(tag, (bx + 26, by - 40))
    return layer

F_BUB = font(BOLD, 40); F_BUBN = font(BODY, 30)
def bubble_layer(name, text, t_line, shown):
    layer = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(layer)
    tw = d.textlength(text, font=F_BUB); bw = int(tw + 64); bh = 120
    x = W - 150 - bw; y = 520
    pop = ease_out_back(t_line / .25); dy = int((1 - pop) * 40)
    a = int(255 * min(1, t_line / .15))
    d.rounded_rectangle((x, y + dy, x + bw, y + bh + dy), 22, fill=(255, 255, 255, a), outline=INK + (a,), width=4)
    d.polygon([(x + bw - 70, y + bh + dy - 2), (x + bw - 30, y + bh + dy - 2), (x + bw - 40, y + bh + 30 + dy)], fill=(255, 255, 255, a))
    d.text((x + 32, y + 18 + dy), name, font=F_BUBN, fill=(90, 110, 115, a))
    d.text((x + 32, y + 56 + dy), text[:shown], font=F_BUB, fill=INK + (a,))
    return layer

F_T1 = font(PIX, 150); F_T2 = font(BOLD, 48)
def title_layer(t1, t2, t, t0, t1end):
    layer = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(layer)
    k = t - t0; out = max(0, (t - (t1end - .35)) / .35)
    if k < 0 or out >= 1: return layer
    p = ease_out_back(k / .45); a = int(255 * (1 - out))
    txt = Image.new('RGBA', (W, 400), (0, 0, 0, 0)); td = ImageDraw.Draw(txt)
    td.text((W // 2 + 7, 167), t1, font=F_T1, fill=INK + (a,), anchor='mm')
    td.text((W // 2, 160), t1, font=F_T1, fill=LAMP + (a,), anchor='mm', stroke_width=6, stroke_fill=INK + (a,))
    if k > .3:
        a2 = int(a * min(1, (k - .3) / .3))
        tw = td.textlength(t2, font=F_T2)
        td.rounded_rectangle((W // 2 - tw / 2 - 26, 262, W // 2 + tw / 2 + 26, 336), 37, fill=INK + (int(a2 * .9),))
        td.text((W // 2, 299), t2, font=F_T2, fill=SAND + (a2,), anchor='mm')
    sc = .5 + .5 * p
    txt = txt.resize((int(W * sc), int(400 * sc)), Image.BICUBIC)
    layer.alpha_composite(txt, ((W - txt.width) // 2, 250 + (400 - txt.height) // 2))
    return layer

F_STAT = font(PIX, 220); F_STAT2 = font(PIX, 72)
def stat_layer(num, label, t, t0, t1end):
    layer = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(layer)
    k = t - t0; out = max(0, (t - (t1end - .3)) / .3)
    if k < 0 or out >= 1: return layer
    a = int(255 * (1 - out))
    # count-up on the number
    target = int(num.replace('.', '')); v = int(target * ease(k / .9))
    s = f'{v:,}'.replace(',', '.')
    p = ease_out_back(k / .4); y = 470 - int((1 - p) * 120)
    d.text((W // 2 + 9, y + 9), s, font=F_STAT, fill=INK + (a,), anchor='mm')
    d.text((W // 2, y), s, font=F_STAT, fill=LAMP + (a,), anchor='mm', stroke_width=8, stroke_fill=INK + (a,))
    d.text((W // 2, y + 150), label, font=F_STAT2, fill=SAND + (a,), anchor='mm', stroke_width=6, stroke_fill=INK + (a,))
    return layer

F_BAN1 = font(BOLD, 40); F_BAN2 = font(PIX, 76)
def banner_layer(l1, l2, t, t0, t1end):
    layer = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(layer)
    k = t - t0; out = max(0, (t - (t1end - .3)) / .3)
    if k < 0 or out >= 1: return layer
    a = int(255 * (1 - out)); slide = int((1 - ease(k / .35)) * W)
    y = 300
    d.rectangle((0 + slide, y, W + slide, y + 210), fill=INK + (int(a * .92),))
    d.rectangle((0 + slide, y, W + slide, y + 10), fill=LAMP + (a,)); d.rectangle((0 + slide, y + 200, W + slide, y + 210), fill=LAMP + (a,))
    d.text((W // 2 + slide, y + 62), l1, font=F_BAN1, fill=SAND + (a,), anchor='mm')
    sh = 0.5 + 0.5 * math.sin(k * 9)
    col = tuple(int(LAMP[i] * (1 - .25 * sh) + 255 * .25 * sh) for i in range(3))
    d.text((W // 2 + slide, y + 140), l2, font=F_BAN2, fill=col + (a,), anchor='mm')
    # sparkles
    for i in range(10):
        ang = i * 0.63 + k * 2; r = 470 + 30 * math.sin(k * 3 + i)
        sx = W // 2 + slide + math.cos(ang) * r; sy = y + 105 + math.sin(ang) * 140
        s = 6 + 5 * abs(math.sin(k * 6 + i))
        d.polygon([(sx, sy - s * 2), (sx + s / 2, sy), (sx, sy + s * 2), (sx - s / 2, sy)], fill=(255, 240, 180, int(a * .9)))
    return layer

F_PL1 = font(PIX, 64); F_PL2 = font(ITAL, 40)
def place_layer(l1, l2, t, t0, t1end):
    layer = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(layer)
    k = t - t0; out = max(0, (t - (t1end - .4)) / .4)
    if k < 0 or out >= 1: return layer
    a = int(255 * min(1, k / .4) * (1 - out))
    x = 70; y = 360
    d.rectangle((x, y, x + 8, y + 140), fill=LAMP + (a,))
    d.text((x + 34, y + 6), l1, font=F_PL1, fill=SAND + (a,), stroke_width=4, stroke_fill=INK + (a,))
    d.text((x + 36, y + 88), l2, font=F_PL2, fill=SAND + (a,), stroke_width=3, stroke_fill=INK + (a,))
    return layer

F_TAG = font(ITAL, 44)
def tag_layer(text, t):
    layer = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(layer)
    a = int(255 * min(1, t / .5))
    d.text((W // 2, 330), text, font=F_TAG, fill=(235, 235, 235, a), anchor='mm', stroke_width=3, stroke_fill=(0, 0, 0, a))
    return layer

F_URL = font(PIX, 92); F_URL2 = font(BOLD, 40); F_TBC = font(ITAL, 60)
def end_layer(t, t0):
    layer = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(layer)
    k = t - t0
    if k < 0: return layer
    a = int(255 * min(1, k / .5)); dim = int(150 * min(1, k / .5))
    d.rectangle((0, 0, W, H), fill=(5, 14, 18, dim))
    p = ease_out_back(k / .5); y = 640 + int((1 - p) * 60)
    d.text((W // 2, y), 'Naik kapalnya sendiri', font=F_URL2, fill=SAND + (a,), anchor='mm')
    d.rounded_rectangle((W // 2 - 420, y + 50, W // 2 + 420, y + 190), 26, fill=LAMP + (a,), outline=INK + (a,), width=6)
    d.text((W // 2, y + 120), 'pulau-aru.web.id', font=F_URL, fill=INK + (a,), anchor='mm')
    d.text((W // 2, y + 250), 'Komentar: nama pulau + bangunan pertama', font=F_URL2, fill=SAND + (a,), anchor='mm')
    if k > 1.2:
        a3 = int(255 * min(1, (k - 1.2) / .5))
        d.text((W // 2, 1180), 'Bersambung…', font=F_TBC, fill=(255, 255, 255, a3), anchor='mm', stroke_width=4, stroke_fill=INK + (a3,))
    return layer

F_Q = font(ITAL, 62); F_QS = font(BODY, 44)
COMMENTS = ['/mnt/user-data/attachments/d8a8f54d-3261-580a-b176-410c1c3e68e9/22cb3a6e-image.jpg', '/mnt/user-data/attachments/d8a8f54d-3261-580a-b176-410c1c3e68e9/99e44822-image.jpg']
_UND = {}
F_UT = font(PIX, 84); F_US = font(BOLD, 40); F_UN = font(PIX, 64)
SPIN = ['@yanzz7384', '@faaxyz79', '@perfume016', '@riski', '@zulfadlibil', '@gledek136', '@Pinjam seratus', '@rwd_god', '@adam.aee1', '@hariri3515']
def undian_frame(s, t):
    if 'bg' not in _UND:
        bg = Image.open('/tmp/claude-0/cap/A/0149.jpg').resize((W, H), Image.LANCZOS).filter(ImageFilter.GaussianBlur(14))
        _UND['bg'] = Image.blend(bg, Image.new('RGB', (W, H), INK), .55)
        cards = []
        for pth in COMMENTS:
            im = Image.open(pth).convert('RGB'); sc = 900 / im.width; im = im.resize((900, int(im.height * sc)), Image.LANCZOS)
            m = Image.new('L', im.size, 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, im.width - 1, im.height - 1), 26, fill=255)
            c = Image.new('RGBA', im.size); c.paste(im, (0, 0), m); cards.append(c)
        _UND['cards'] = cards
    img = _UND['bg'].copy().convert('RGBA'); d = ImageDraw.Draw(img)
    d.text((W // 2, 300), 'UNDIAN KOMENTAR', font=F_UT, fill=LAMP, anchor='mm', stroke_width=6, stroke_fill=INK)
    d.text((W // 2, 380), 'acak · tanpa hadiah', font=F_US, fill=SAND, anchor='mm')
    if t < 1.5:   # names spinning in a slot window
        k = int(t * 14)
        d.rounded_rectangle((140, 560, W - 140, 700), 28, fill=SAND + (255,), outline=INK + (255,), width=6)
        d.text((W // 2, 630), SPIN[k % len(SPIN)], font=F_UN, fill=INK, anchor='mm')
    y = 520
    for i, card in enumerate(_UND['cards']):
        t0 = 1.5 + i * 1.0
        if t < t0: break
        p = ease_out_back((t - t0) / .4); sc = .6 + .4 * p
        c = card.resize((max(1, int(card.width * sc)), max(1, int(card.height * sc))), Image.BICUBIC)
        sh = Image.new('RGBA', (c.width + 24, c.height + 24), (0, 0, 0, 0)); ImageDraw.Draw(sh).rounded_rectangle((12, 20, c.width + 12, c.height + 22), 26, fill=(0, 0, 0, 110))
        x0 = (W - c.width) // 2; img.alpha_composite(sh, (x0 - 12, y - 12)); img.alpha_composite(c, (x0, y))
        if t - t0 > .35:   # "terpilih" stamp
            tag = 'TERPILIH'; tw = d.textlength(tag, font=F_US) + 40
            d.rounded_rectangle((W - 120 - tw, y - 26, W - 120, y + 30), 28, fill=LAMP + (255,), outline=INK + (255,), width=4)
            d.text((W - 120 - tw / 2, y + 2), tag, font=F_US, fill=INK, anchor='mm')
        y += card.height + 70
    return img.convert('RGB')

def card_frame(s, t):
    img = Image.new('RGB', (W, H), (6, 10, 14)); d = ImageDraw.Draw(img)
    # faint vignette glow
    for (t0, text, kind) in s['card_lines']:
        k = t - t0
        if k < 0: continue
        if kind == 'quote':
            shown = int(k * 15)
            lines = wrap(d, text, F_Q, W - 200)
            y = 820; left = shown
            for ln in lines:
                d.text((W // 2, y), ln[:max(0, left)].ljust(0), font=F_Q, fill=(243, 231, 201), anchor='mm'); left -= len(ln) + 1; y += 86
        else:
            a = min(1, k / .8)
            c = tuple(int(v * a) for v in (170, 180, 185))
            d.text((W // 2, 1120), text, font=F_QS, fill=c, anchor='mm')
    return img

# ---------------------------------------------------------------- per-segment render
def clip_cmd(s, n_frames):
    src = A + CLIP[s['clip']] + '.mp4'
    vf = [f"trim=start={s['a']}:end={s['b']}", 'setpts=PTS-STARTPTS']
    if s['speed'] != 1: vf.append(f"setpts=PTS/{s['speed']}")
    vf += ['fps=30', 'crop=864:1536:0:192', 'delogo=x=640:y=1466:w=212:h=67', f'scale={W}:{H}:flags=lanczos']
    if s.get('gray'): vf += ['hue=s=0', 'eq=contrast=1.15:brightness=-0.04', 'vignette=PI/3.2']
    vf.append(f'tpad=stop_mode=clone:stop_duration=30')
    return ['ffmpeg', '-v', 'error', '-i', src, '-vf', ','.join(vf), '-frames:v', str(n_frames), '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-']

def overlays(s, t, base):
    img = base.convert('RGBA')
    if 'title' in s: img.alpha_composite(title_layer(*s['title'][:2], t, *s['title'][2:]))
    if 'stat' in s: img.alpha_composite(stat_layer(*s['stat'][:2], t, *s['stat'][2:]))
    if 'banner' in s: img.alpha_composite(banner_layer(*s['banner'][:2], t, *s['banner'][2:]))
    if 'place' in s: img.alpha_composite(place_layer(*s['place'][:2], t, *s['place'][2:]))
    if 'tag' in s: img.alpha_composite(tag_layer(s['tag'], t))
    # the active dialog line: the latest one that has started (each stays until the next)
    aru = [l for l in s.get('lines', []) if l[1] == 'aru' and l[0] <= t]
    if aru and not ('endcard' in s and t >= s['endcard'][0]):
        t0, _, text, o = aru[-1]
        shown = int((t - t0) * (CPS_SLOW if o.get('slow') else CPS_NORMAL))
        img.alpha_composite(dialog_layer(text, shown, o, t - t0, o.get('top')))
    for (t0, who, text, o) in s.get('lines', []):
        if who.startswith('warga') and t0 <= t < t0 + 2.6:
            img.alpha_composite(bubble_layer(who.split(':', 1)[1], text, t - t0, int((t - t0) * 32)))
    if 'endcard' in s: img.alpha_composite(end_layer(t, s['endcard'][0]))
    out = img.convert('RGB')
    L = seg_len(s); fi = s.get('fade_in', 0); fo = s.get('fade_out', 0)
    k = 1.0
    if fi and t < fi: k = t / fi
    if fo and t > L - fo: k = min(k, (L - t) / fo)
    if k < 1: out = Image.eval(out, lambda v: int(v * max(0, k)))
    return out

def render_seg(i, s):
    L = seg_len(s); n = int(round(L * FPS))
    dst = f'{OUT}/seg_{s["id"]}.mp4'; tmp = dst + '.tmp.mp4'
    enc = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', '30', '-i', '-',
                            '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '19', '-pix_fmt', 'yuv420p', '-r', '30', tmp], stdin=subprocess.PIPE)
    if s.get('card'):
        for f in range(n): enc.stdin.write(overlays(s, f / FPS, card_frame(s, f / FPS)).tobytes())
    elif s.get('undian'):
        for f in range(n): enc.stdin.write(overlays(s, f / FPS, undian_frame(s, f / FPS)).tobytes())
    elif s.get('seq'):
        files = sorted(f for f in os.listdir(s['seq']) if f.endswith('.jpg'))
        for f in range(n):
            im = Image.open(os.path.join(s['seq'], files[min(f, len(files) - 1)])).convert('RGB').resize((W, H), Image.LANCZOS)
            enc.stdin.write(overlays(s, f / FPS, im).tobytes())
    else:
        dec = subprocess.Popen(clip_cmd(s, n), stdout=subprocess.PIPE)
        fs = W * H * 3
        last = None
        for f in range(n):
            buf = dec.stdout.read(fs)
            if len(buf) == fs: last = Image.frombytes('RGB', (W, H), buf)
            enc.stdin.write(overlays(s, f / FPS, last).tobytes())
        dec.stdout.close(); dec.wait()
    enc.stdin.close(); assert enc.wait() == 0
    os.replace(tmp, dst)
    print(f'seg_{s["id"]} {L:.2f}s', flush=True)

def timeline():
    t = 0; out = []
    for s in SEGS: out.append((t, s)); t += seg_len(s)
    return out, t

# ---------------------------------------------------------------- audio
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import synth as S

def blip(freq, d=.045, vol=.18):
    t = S.t_axis(d); y = np.sign(np.sin(2 * np.pi * freq * t)) * .5 + np.sin(2 * np.pi * freq * t) * .5
    return y * S.env_ad(len(y), .002, d / 3) * vol

def horn(d=2.6):
    y = np.zeros(int(d * S.SR))
    for n, g in ((43, .6), (50, .4), (55, .3)):
        y += S.saw(S.midi(n), d, harm=10, bright=.6) * g
    t = S.t_axis(d); e = np.minimum(1, t / .25) * np.minimum(1, (d - t) / .6)
    return y * e * .5

def piano(note, d=2.4, v=1.0):
    f = S.midi(note); t = S.t_axis(d)
    y = (np.sin(2*np.pi*f*t) + .4*np.sin(4*np.pi*f*t) + .15*np.sin(6*np.pi*f*t)) * np.exp(-t * 2.2) * np.minimum(1, t / .004)
    return y * .32 * v

CH = {'C': [60, 64, 67], 'G': [55, 59, 62], 'Am': [57, 60, 64], 'F': [53, 57, 60], 'Em': [52, 55, 59], 'Dm': [50, 53, 57]}
def music(bus, mood, t0, t1, beat0=0):
    dur = t1 - t0
    if mood == 'cheer':
        bpm = 116; b = 60 / bpm; prog = ['C', 'G', 'Am', 'F']
        n = int(dur / b)
        for k in range(n):
            t = t0 + k * b; ch = CH[prog[(k // 4) % 4]]
            bus.add(S.pluck(ch[k % 3] + 12, .5, .7), t, .5, pan=-.3)
            bus.add(S.pluck(ch[(k + 1) % 3] + 24, .35, .5), t + b / 2, .28, pan=.3)
            if k % 4 == 0: bus.add(S.bass(ch[0] - 24, b * 3.6), t, .35)
            bus.add(S.kick(.5), t, .35) if k % 2 == 0 else bus.add(S.snare(.4), t, .18)
            bus.add(S.hat(), t + b / 2, .25)
    elif mood == 'dusk':
        prog = ['Am', 'F']; seg = dur / 2
        for k in range(2): bus.add(S.pad([n + 12 for n in CH[prog[k]]], seg + .6, .35), t0 + k * seg, .32)
        for k in range(int(dur / 1.1)): bus.add(piano(CH[prog[min(1, int(k * 1.1 / seg))]][k % 3] + 12, 2.0, .6), t0 + k * 1.1, .7)
    elif mood == 'sad':
        prog = ['Am', 'F', 'C', 'G', 'Am', 'F', 'C', 'G']; b = 60 / 66
        start = t0 + 1.4 if beat0 == 0 else t0
        for k in range(int((t1 - start) / b)):
            ch = CH[prog[(k // 4) % 8]]; t = start + k * b
            bus.add(piano(ch[[0, 1, 2, 1][k % 4]] + 12, 2.8, .9), t, .8)
            if k % 4 == 0: bus.add(piano(ch[0] - 12, 4, .7), t, .6)
        bus.add(S.pad([57, 64, 69], dur, .25), t0, .12)
    elif mood == 'hype':
        bpm = 132; b = 60 / bpm; prog = ['F', 'G', 'Em', 'Am', 'F', 'G', 'C', 'C']
        bus.add(S.crash(), t0 + .25, .5)
        for k in range(int(dur / b)):
            t = t0 + k * b; ch = CH[prog[(k // 4) % 8]]
            bus.add(S.kick(.9), t, .45)
            if k % 2 == 1: bus.add(S.snare(.8), t, .32)
            bus.add(S.hat(), t + b / 2, .3)
            if k % 2 == 0: bus.add(S.stab([n + 12 for n in ch], b * 1.6), t, .22)
            bus.add(S.bass(ch[0] - 24, b * .9), t, .3)
            bus.add(S.pluck(ch[k % 3] + 24, .3, .8), t + b / 2, .2, pan=.4)
    elif mood == 'sail':
        prog = ['C', 'G', 'Am', 'F']; seg = 3.2
        for k in range(int(dur / seg) + 1):
            bus.add(S.pad([n + 12 for n in CH[prog[k % 4]]], seg + .5, .45), t0 + k * seg, .3)
            for j in range(4): bus.add(S.pluck(CH[prog[k % 4]][j % 3] + 24, .9, .5), t0 + k * seg + j * .8, .2, pan=(-.4 if j % 2 else .4))
    elif mood == 'mystery':
        bus.add(S.pad([45, 52], dur, .3), t0, .3)
        for k in range(int(dur / 1.3)): bus.add(S.pluck([81, 84, 88, 76, 79][k % 5], 1.6, .3), t0 + .5 + k * 1.3, .2, pan=(k % 3 - 1) * .5)
    elif mood == 'cliff':
        bus.add(S.sfx_impact(), t0 + .2, .7)
        bus.add(piano(57, 4.5, 1.0), t0 + .45, .8)
    elif mood == 'ending':
        prog = ['F', 'C', 'G', 'Am']; b = 60 / 92
        for k in range(int(dur / b)):
            t = t0 + k * b; ch = CH[prog[(k // 4) % 4]]
            bus.add(piano(ch[[0, 1, 2, 1][k % 4]] + 12, 1.8, .7), t, .55)
            if k % 4 == 0: bus.add(S.pad([n + 12 for n in ch], b * 4 + .4, .35), t, .22)
            if k % 2 == 0: bus.add(S.kick(.35), t, .22)

def build_audio(path):
    tl, total = timeline()
    bus = S.Bus(total); sfx = S.Bus(total)
    # music: merge consecutive segments with the same mood into one run
    runs = []
    for (t, s) in tl:
        L = seg_len(s)
        if runs and runs[-1][0] == s['mood']: runs[-1][2] = t + L
        else: runs.append([s['mood'], t, t + L])
    for i, (mood, a, b) in enumerate(runs):
        m = S.Bus(b - a); music(m, mood, 0, b - a)
        # short fades at run edges so cuts between moods stay clean
        n = int((b - a) * S.SR); env = np.ones(n)
        fi = int(.12 * S.SR); fo = int((.5 if mood not in ('hype', 'cheer') else .25) * S.SR)
        env[:fi] = np.linspace(0, 1, fi); env[-fo:] = np.linspace(1, 0, fo)
        bus.add(m.L[:n] * env, a, 1.0, pan=-1); bus.add(m.R[:n] * env, a, 1.0, pan=1)
    # dialog blips, title whooshes, horn
    for (t, s) in tl:
        for (t0, who, text, o) in s.get('lines', []):
            cps = CPS_SLOW if o.get('slow') else CPS_NORMAL
            if who.startswith('warga'): cps = 32
            base = 560 if who == 'aru' else 820
            if o.get('slow'): base = 470
            if o.get('shout'): base = 640
            g = np.random.default_rng(len(text))
            for k, ch in enumerate(text):
                if ch in ' .,…?!\'"': continue
                if k % 2: continue   # every other letter keeps it from buzzing
                f = base * (1 + .12 * g.standard_normal() * .6)
                sfx.add(blip(f, vol=.13 if o.get('slow') else .16), t + t0 + k / cps)
            sfx.add(S.sfx_click(), t + t0, .25)
        for key in ('title', 'stat', 'banner', 'place'):
            if key in s: sfx.add(S.sfx_whoosh(1.0), t + s[key][2], .9); sfx.add(S.sfx_shimmer(), t + s[key][2] + .25, .6)
        if 'horn' in s: sfx.add(horn(), t + s['horn'], .9)
        if 'rumble' in s:
            d_ = 4.2; nz = S.band_noise(d_, 30, 260, seed=5); tt = S.t_axis(d_); env = np.sin(np.pi * tt / d_) ** .7
            sfx.add(nz * env * .55 + S.sweep(55, 38, d_, 1.0) * env * .35, t + s['rumble'], 1.0); sfx.add(S.sfx_impact(), t + s['rumble'] + 4.0, .5)
        if s.get('undian'):
            for k in range(21): sfx.add(S.sfx_tick(k), t + k / 14, .7)
            for i in range(2): sfx.add(S.sfx_chime([76, 81, 84]), t + 1.5 + i, .6)
        if 'endcard' in s: sfx.add(S.sfx_chime([72, 76, 79, 84]), t + s['endcard'][0], .8)
        if s.get('card'):
            for k in range(len(s['card_lines'][0][1])):
                if k % 2 == 0: sfx.add(blip(300 + (k % 5) * 12, .05, .07), t + s['card_lines'][0][0] + k / 15)
    L = bus.L * .7 + sfx.L; R = bus.R * .7 + sfx.R
    n = int(total * S.SR); st = np.stack([L[:n], R[:n]], 1)
    peak = np.max(np.abs(st)) + 1e-9; st = st / peak * .89
    with wave.open(path, 'wb') as wv:
        wv.setnchannels(2); wv.setsampwidth(2); wv.setframerate(S.SR)
        wv.writeframes((st * 32767).astype('<i2').tobytes())
    return total

# ---------------------------------------------------------------- main
if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    tl, total = timeline()
    if sys.argv[1] == 'plan':
        for (t, s) in tl: print(f'{t:7.2f}  {seg_len(s):5.2f}  {s["id"]}')
        print('total', round(total, 2))
    elif sys.argv[1] == 'preview':
        for ts in sys.argv[2].split(','):
            T = float(ts)
            for (t, s) in tl:
                if t <= T < t + seg_len(s): break
            lt = T - t
            if s.get('card'): base = card_frame(s, lt)
            elif s.get('undian'): base = undian_frame(s, lt)
            elif s.get('seq'):
                files = sorted(f for f in os.listdir(s['seq']) if f.endswith('.jpg'))
                base = Image.open(os.path.join(s['seq'], files[min(int(lt * FPS), len(files) - 1)])).convert('RGB').resize((W, H), Image.LANCZOS)
            else:
                cmd = clip_cmd(s, int(lt * FPS) + 1)
                raw = subprocess.run(cmd, capture_output=True).stdout
                fs = W * H * 3; base = Image.frombytes('RGB', (W, H), raw[-fs:])
            overlays(s, lt, base).save(f'{OUT}/prev_{T:06.2f}.jpg', quality=88)
            print('preview', T, s['id'])
    elif sys.argv[1] == 'render':
        only = sys.argv[2].split(',') if len(sys.argv) > 2 else None
        for i, sg in enumerate(SEGS):
            if only is None or sg['id'] in only: render_seg(i, sg)
    elif sys.argv[1] == 'audio':
        print('audio', build_audio(f'{OUT}/audio.wav'))
