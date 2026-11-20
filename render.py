"""Render the original editorial page. Pillow and fonts are development only."""
from functools import cache
import json
import math
import os
from pathlib import Path
import sys
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
S = 2
PAPER = '#F4EFE4'
INK = '#172F34'
MUTED = '#496162'
RED = '#AD3D2D'
LINE = '#B9BDB0'
DENIM = '#163638'
DUSK = '#234A4C'
CREAM = '#FFF2D7'
TANGERINE = '#F0A563'
FONT_DIR = Path(os.environ.get('DIGEST_FONT_DIR', Path(os.environ.get('WINDIR', 'C:/Windows')) / 'Fonts'))
STORIES = json.loads((ROOT / 'stories.json').read_text(encoding='utf-8'))

@cache
def font(face, size):
    names = {'display':'georgia.ttf','bold':'georgiab.ttf','sans':'segoeui.ttf','strong':'segoeuib.ttf','mono':'consolab.ttf'}
    return ImageFont.truetype(FONT_DIR / names[face], size*S)

class Canvas:
    def __init__(self, size, bg):
        self.im = Image.new('RGB', tuple(v*S for v in size), bg)
        self.d = ImageDraw.Draw(self.im)
        self.log = []

    def rect(self, box, fill, outline=None, w=1):
        self.d.rectangle(tuple(round(v*S) for v in box), fill=fill, outline=outline, width=w*S)

    def ell(self, box, fill, outline=None, w=1):
        self.d.ellipse(tuple(round(v*S) for v in box), fill=fill, outline=outline, width=w*S)

    def arc(self, box, a, b, color, w):
        self.d.arc(tuple(round(v*S) for v in box), a, b, fill=color, width=w*S)

    def poly(self, pts, fill):
        self.d.polygon([(round(x*S), round(y*S)) for x,y in pts], fill=fill)

    def line(self, pts, color, w=1):
        self.d.line([(round(x*S),round(y*S)) for x,y in pts], fill=color, width=w*S, joint='curve')

    def type(self, x, y, content, face, size, color, right=982, anchor='lt'):
        f = font(face, size)
        a,b,c,d = self.d.textbbox((x*S,y*S),content,font=f,anchor=anchor)
        if a < 0 or b < 0 or c > right*S or d > self.im.height:
            raise ValueError(f'Text outside its column: {content!r} at {(a/S,b/S,c/S,d/S)}, limit {right}')
        self.d.text((x*S,y*S),content,font=f,fill=color,anchor=anchor)
        self.log.append((content, (a/S,b/S,c/S,d/S)))

    def paste(self, art, x, y):
        self.im.paste(art.im,(x*S,y*S))


def leader(c, x, base, skin, tie, variant):
    body = '#102728'
    y = base
    c.ell((x-39,y-56,x+39,y+34), '#4A6463')
    c.poly([(x-51,y+17),(x-46,y-15),(x-20,y-28),(x+19,y-28),(x+43,y-14),(x+52,y+17)],body)
    c.rect((x-9,y-39,x+9,y-22),skin)
    c.poly([(x-14,y-28),(x,y-18),(x+14,y-28),(x+6,y+16),(x-6,y+16)],CREAM)
    c.poly([(x,y-19),(x+4,y-14),(x+3,y+10),(x-2,y+15),(x-5,y+8),(x-3,y-14)],tie)
    c.line([(x-24,y-21),(x-19,y-8),(x-22,y-2),(x-12,y+14)],'#395454',2)
    c.line([(x+23,y-21),(x+17,y-8),(x+21,y-1),(x+11,y+14)],'#395454',2)
    c.ell((x-16,y-78,x+16,y-35),skin)
    c.ell((x-18,y-59,x-10,y-49),skin)
    c.ell((x+10,y-59,x+18,y-49),skin)
    if variant == 0:
        c.poly([(x-17,y-62),(x-19,y-71),(x-13,y-80),(x+11,y-82),(x+20,y-76),(x+18,y-68),(x+13,y-72),(x-10,y-69)],'#F3C376')
    elif variant == 1:
        c.poly([(x-16,y-57),(x-19,y-70),(x-12,y-79),(x-2,y-83),(x+11,y-81),(x+17,y-74),(x+16,y-59),(x+12,y-70),(x+1,y-73),(x-10,y-70)],'#172A29')
    else:
        c.poly([(x-16,y-60),(x-17,y-71),(x-12,y-78),(x-3,y-80),(x+10,y-79),(x+16,y-72),(x+15,y-64),(x+11,y-72),(x-9,y-73)],'#C2AF86')
    c.line([(x-10,y-59),(x-4,y-60)],body,1)
    c.line([(x+4,y-60),(x+10,y-59)],body,1)
    c.line([(x,y-57),(x-1,y-52),(x+2,y-51)],'#935841',1)
    c.line([(x-4,y-44),(x+4,y-44)],'#834F3D',1)


def summit_art():
    c = Canvas((482,264), DENIM)
    c.ell((139,-54,346,150),'#D26A47')
    for y in range(9,153,6):
        for x in range(12 + (y%4)*2,481,7):
            if (x-242)**2+(y-48)**2 >= 107**2:
                c.ell((x,y,x+1.3,y+1.3),'#3B5D5B')
    c.line([(0,126),(88,126),(126,139),(165,139),(200,129),(324,129),(359,137),(482,137)],'#627871',1)
    skyline = [(4,26,55),(31,24,39),(60,15,56),(82,20,69),(115,23,33),(153,13,75),(402,20,51),(431,18,76),(456,26,41)]
    for x,w,h in skyline:
        c.poly([(x,152),(x,151-h),(x+w*.75,151-h-10),(x+w,151-h),(x+w,152)],'#35595A')
        for yy in range(155-h,149,7):
            c.line([(x+4,yy),(x+w-4,yy)],'#53736C')
    # The stepped central tower and its spire evoke the Shenzhen skyline.
    c.poly([(366,150),(372,49),(383,23),(393,49),(397,150)],'#456A65')
    c.line([(383,25),(383,7)],'#6E8B80',2)
    c.line([(383,48),(383,126)],'#839A89',1)
    c.rect((0,151,481,263),'#123032')
    leader(c,96,159,'#D69565','#D56148',0)
    leader(c,243,145,'#CB8B64','#C86449',1)
    leader(c,390,159,'#E4AB7E','#6E9D9A',2)
    # A shared table connects the three places; the paper is their declaration.
    c.ell((12,181,474,262),'#0B2325')
    c.ell((19,169,463,245),'#A24E37')
    c.ell((19,165,463,233),'#D38D55',outline='#EBB477',w=2)
    c.ell((46,171,436,224),None,'#B4734A',1)
    # Desk microphones and water glasses, not flags or party emblems.
    for x,y in [(104,190),(242,175),(376,190)]:
        c.ell((x-16,y-1,x+1,y+4),'#6F4C3A')
        c.line([(x-7,y+1),(x-7,y-11),(x-2,y-16)],INK,2)
        c.ell((x-3,y-18,x+4,y-14),INK)
        c.rect((x+13,y-9,x+20,y), '#A9B5A0', '#5A6959')
        c.line([(x+14,y-7),(x+14,y-2)],CREAM)
    c.poly([(220,200),(252,195),(267,209),(232,215)],'#B97046')
    c.poly([(220,196),(252,191),(267,205),(232,211)],CREAM)
    for n in range(3):
        c.line([(232+n*3,197+n*3),(248+n*3,195+n*3)],'#9B7056',1)
    c.line([(52,239),(114,250),(180,255),(301,255),(371,248),(430,236)],'#395453')
    return c


def spot(kind):
    colors={'court':('#DECCC3','#8D594D'),'market':('#D6E2D1','#356F57'),
            'climate':('#EDDCB9','#976433'),'energy':('#CEDDDA','#337175')}
    bg,accent=colors[kind]
    c=Canvas((117,133),bg)
    c.ell((14,21,102,110),None,accent)
    for y in range(9,126,6):
        for x in range(6+(y%4),115,6):
            if (x-58)**2 + (y-65)**2 > 47**2:
                c.ell((x,y,x+1,y+1),accent)
    if kind == 'court':
        c.poly([(16,54),(57,32),(101,54)],accent)
        c.poly([(26,51),(57,38),(89,51)],CREAM)
        c.rect((20,55,97,60),INK)
        c.rect((25,63,91,97),'#C5A99D')
        for x in (30,46,63,79): c.rect((x,63,x+7,96),CREAM)
        c.rect((20,96,97,100),INK)
        c.rect((15,101,102,105),accent)
        c.rect((52,75,63,95),INK)
    elif kind == 'market':
        c.rect((20,33,96,102), '#E7EDE1',accent)
        for y in (51,66,81): c.line([(22,y),(95,y)],'#ACBFAB')
        for x,h in [(29,14),(44,24),(59,19),(74,36)]: c.rect((x,92-h,x+8,92),'#82A38C')
        c.line([(26,76),(45,65),(59,70),(87,43)],accent,4)
        c.poly([(77,44),(91,39),(89,53)],accent)
        c.line([(25,94),(91,94)],INK,2)
    elif kind == 'climate':
        c.poly([(30,28),(69,28),(89,47),(89,106),(30,106)],'#B69266')
        c.poly([(25,23),(69,23),(87,41),(87,102),(25,102)],CREAM)
        c.poly([(69,23),(69,42),(87,42)],'#DDB988')
        for y in (50,59,68,77,86): c.line([(34,y),(75,y)],'#A48761',2)
        c.rect((31,64,80,74),'#AD523B')
        c.line([(35,69),(76,69)],CREAM,2)
        c.line([(31,74),(81,64)],'#7C3628',2)
    else:
        c.poly([(0,31),(27,30),(43,49),(49,57),(42,69),(27,78),(17,99),(0,100)],'#8EAFA4')
        c.poly([(117,31),(98,35),(83,53),(80,82),(91,94),(117,99)],'#8EAFA4')
        c.line([(18,110),(31,98),(43,92),(56,84),(61,70),(65,52),(76,34)],accent,2)
        c.poly([(42,81),(83,68),(84,80),(72,88),(47,95)],INK)
        c.poly([(50,79),(66,74),(69,80),(53,86)],'#E0A368')
        c.poly([(68,73),(78,69),(82,76),(72,79)],CREAM)
        c.line([(37,94),(22,99)],CREAM,2)
        c.line([(43,100),(32,103)],CREAM,2)
    return c


def brief_art(kind):
    c=Canvas((72,43),PAPER)
    if kind == 'space':
        c.ell((2,19,22,39),'#3D746F')
        c.arc((6,22,18,36),85,270,CREAM,1)
        c.line([(3,29),(20,29)],CREAM)
        for x in (27,32,37,42): c.ell((x,25,x+1,26),MUTED)
        c.arc((46,7,67,32),102,264,RED,3)
        c.line([(53,18),(69,13),(69,31),(53,24)],INK,2)
        c.rect((54,17,62,24),'#DFA56C')
        c.line([(60,24),(64,36)],INK,2)
    elif kind == 'storm':
        path=[]
        for i in range(75):
            ang=i/74*math.pi*3.3
            r=1+i/74*18
            path.append((21+math.cos(ang)*r,21+math.sin(ang)*r))
        c.line(path,'#407F7C',3)
        c.line([(42,23),(51,23),(56,18)],RED,2)
        c.poly([(47,22),(59,12),(71,22)],INK)
        c.rect((50,23,68,36), '#BD6D52')
        c.rect((57,27,61,36),CREAM)
    else:
        c.ell((23,0,53,29),'#DC8C65')
        c.line([(32,33),(48,26),(70,27)],'#4D837F',2)
        c.poly([(10,16),(22,13),(29,17),(40,17),(48,13),(58,17),(62,34),(59,39),(52,39),(44,31),(26,31),(19,39),(11,39),(6,34)],INK)
        c.line([(17,24),(25,24)],CREAM,2)
        c.line([(21,20),(21,28)],CREAM,2)
        c.ell((49,21,52,24),TANGERINE)
        c.ell((54,25,57,28),TANGERINE)
    return c


def story(c, idx, x, y, right, title_size=29):
    s=STORIES[idx]
    c.type(x,y,s['label'],'mono',13,RED,right)
    for j,line in enumerate(s['head']):
        c.type(x,y+23+j*33,line,'bold',title_size,INK,right)
    body_top=y+62+33*(len(s['head'])-1)
    for j,line in enumerate(s['body']):
        c.type(x,body_top+j*22,line,'sans',18,INK,right)
    c.type(x,body_top+22*len(s['body'])+3,s['source'],'mono',12,MUTED,right)


def render(path):
    c=Canvas((1024,1024),PAPER)
    c.rect((0,0,1023,7),DENIM)
    c.type(44,27,'THE WORLD / ONE DAY','mono',16,RED)
    c.type(980,27,'THURSDAY  /  GLOBAL EDITION','mono',15,MUTED,anchor='rt')
    c.type(40,50,'19 November 2026','display',86,INK)
    c.line([(44,139),(980,139)],INK,2)
    c.line([(44,144),(980,144)],LINE)
    c.rect((44,157,980,420),DENIM)
    c.paste(summit_art(),44,157)
    c.line([(525,169),(525,407)],'#54726A')
    hero=STORIES[0]
    c.type(549,178,hero['label'],'mono',15,TANGERINE)
    for j,line in enumerate(hero['head']):
        c.type(545,202+j*49,line,'bold',48,CREAM)
    for j,line in enumerate(hero['body']):
        c.type(549,310+j*21,line,'sans',19,'#F7EEE0')
    c.type(549,400,hero['source'],'mono',12,'#C9D9C9')
    c.type(44,441,'THE DAY’S OTHER LEAD STORIES','mono',14,RED)
    c.line([(304,448),(980,448)],LINE)
    for idx,x,y in [(1,44,474),(2,530,474),(3,44,648),(4,530,648)]:
        c.paste(spot(STORIES[idx]['id']),x,y+1)
        story(c,idx,x+131,y,510 if x==44 else 981,26)
    c.line([(44,630),(980,630)],LINE)
    c.line([(512,472),(512,790)],LINE)
    c.line([(44,805),(980,805)],INK,2)
    for idx,x,right in [(5,44,344),(6,363,665),(7,684,980)]:
        s=STORIES[idx]
        c.paste(brief_art(s['id']),x+221,819)
        c.type(x,829,s['label'],'mono',13,RED,right)
        c.type(x,857,s['head'][0],'bold',26,INK,right)
        for j,line in enumerate(s['body']): c.type(x,894+j*21,line,'sans',18,INK,right)
        c.type(x,960,s['source'],'mono',12,MUTED,right)
    for x in (347,669): c.line([(x,823),(x,971)],LINE)
    c.line([(44,985),(980,985)],LINE)
    c.type(44,997,'EIGHT STORIES / ONE DAY','mono',12,MUTED)
    c.type(980,997,'19 NOV 2026','mono',12,MUTED,anchor='rt')
    # As well as per-column limits, reject any text-to-text box overlaps.
    for i,(text,(a,b,d,e)) in enumerate(c.log):
        for other,(f,g,h,k) in c.log[:i]:
            if max(a,f)<min(d,h) and max(b,g)<min(e,k):
                raise ValueError(f'Overlapping text: {text!r} and {other!r}')
    for s in STORIES:
        if not all(line in {text for text,_ in c.log} for line in [s['label'],*s['head'],*s['body'],s['source']]):
            raise ValueError(f'Missing editorial copy: {s["id"]}')
    c.im.resize((1024,1024),Image.Resampling.LANCZOS).save(path,format='PNG',optimize=True)

if __name__ == '__main__':
    render(Path(sys.argv[1]) if len(sys.argv)>1 else ROOT/'entry.png')
