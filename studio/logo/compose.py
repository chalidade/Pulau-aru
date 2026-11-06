from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math
F='/home/claude/pulau-aru/studio/fonts/pixelify-latin-700-normal.ttf'
S=1080
def grad(top,bot,sea=None):
    im=Image.new('RGB',(S,S)); d=ImageDraw.Draw(im)
    t=[int(top[i:i+2],16) for i in (1,3,5)]; b=[int(bot[i:i+2],16) for i in (1,3,5)]
    for y in range(S):
        k=y/S; d.line([(0,y),(S,y)],fill=tuple(int(t[j]+(b[j]-t[j])*k) for j in range(3)))
    if sea:
        for y in range(sea,S):
            k=(y-sea)/(S-sea); d.line([(0,y),(S,y)],fill=(int(70-30*k),int(170-50*k),int(210-40*k)))
    return im
def clouds(im,pts):
    l=Image.new('RGBA',(S,S)); d=ImageDraw.Draw(l)
    for x,y,s in pts:
        for dx,dy,r in [(0,0,1),(-.9,.25,.7),(.9,.25,.75),(.4,-.35,.7)]:
            d.ellipse([x+dx*s*60-r*s*60,y+dy*s*60-r*s*60,x+dx*s*60+r*s*60,y+dy*s*60+r*s*60],fill=(255,255,255,215))
    im.paste(l,(0,0),l.filter(ImageFilter.GaussianBlur(2)))
def put(im,src,scale,cx,cy):
    a=Image.open(src); a=a.resize((int(1024*scale),)*2,Image.LANCZOS)
    sh=a.split()[3]
    im.paste(a,(int(cx-a.width/2),int(cy-a.height/2)),a)
def text(im,s,y,size,fill='#ffffff',stroke='#20314a'):
    d=ImageDraw.Draw(im); f=ImageFont.truetype(F,size)
    w=d.textlength(s,font=f); d.text(((S-w)/2,y),s,font=f,fill=fill,stroke_width=max(4,size//10),stroke_fill=stroke)
# A: floating island, no text
a=grad('#5fb8ec','#d8f0ff'); clouds(a,[(200,250,1.1),(860,330,.9),(760,860,.8)])
put(a,'island.png',1.16,540,565); a.save('A-pulau.png')
# B: Aru portrait with sea
b=grad('#ffb36b','#ffe2b0',sea=760); 
d=ImageDraw.Draw(b); d.ellipse([300,170,780,650],fill='#fff3c4')
b=b.convert('RGBA'); b2=Image.new('RGB',(S,S)); 
b=b.convert('RGB'); put(b,'portrait.png',1.05,540,585); b.save('B-aru.png')
# C: badge island + PULAU ARU
c=grad('#5fb8ec','#d8f0ff'); clouds(c,[(230,230,.9),(850,280,.8)])
put(c,'island.png',.9,540,500); text(c,'PULAU ARU',770,118,'#ffd25a'); c.save('C-badge.png')
# sheet with circle previews
sheet=Image.new('RGB',(3*560+40,640),'#1f2430'); dd=ImageDraw.Draw(sheet)
for i,(n,lab) in enumerate([('A-pulau.png','A · Pulau melayang'),('B-aru.png','B · Aru melambai'),('C-badge.png','C · Pulau + nama')]):
    im=Image.open(n).resize((520,520)); m=Image.new('L',(520,520),0); ImageDraw.Draw(m).ellipse([0,0,519,519],fill=255)
    sheet.paste(im,(20+i*560+20,30),m)
    small=Image.open(n).resize((96,96)); m2=Image.new('L',(96,96),0); ImageDraw.Draw(m2).ellipse([0,0,95,95],fill=255)
    sheet.paste(small,(20+i*560+20,540),m2)
    dd.text((20+i*560+130,575),lab,font=ImageFont.truetype(F,34),fill='#ffffff')
sheet.save('pilihan-profil.jpg',quality=92)
