import re, os, json, math, zipfile, hashlib
from PIL import Image, ImageDraw
REAL=["ZEUS", "POSEIDON", "HADES", "ATHENA", "ARES", "APOLLO", "HEPHAESTUS", "HERMES", "DIONYSUS"]
abil={k:[(None,t) for t in v] for k,v in {"ZEUS": ["AOE", "LEAP", "CHAIN", "STORM", "GUARD", "STORM"], "POSEIDON": ["BUFF", "AOE", "DASH", "TRAP", "BUFF", "AOE"], "HADES": ["BUFF", "BLINK", "GUARD", "SUMMON", "DRAIN", "AOE"], "ATHENA": ["REVEAL", "MARK", "GUARD", "BUFF", "REVEAL", "AOE"], "ARES": ["AOE", "BUFF", "AOE", "GUARD", "BUFF", "AOE"], "APOLLO": ["PROJECTILE", "HEAL", "BEAM", "AOE", "PROJECTILE", "PROJECTILE"], "HEPHAESTUS": ["BUFF", "BUFF", "AOE", "TRAP", "GUARD", "SUMMON"], "HERMES": ["BUFF", "LEAP", "BUFF", "DASH", "BLINK", "FLIGHT"], "DIONYSUS": ["TRAP", "BUFF", "TRAP", "HEAL", "BUFF", "TRAP"]}.items()}
COL={'ZEUS':(250,215,60),'POSEIDON':(50,130,235),'HADES':(150,70,200),'ATHENA':(225,225,235),'ARES':(220,50,50),
     'APOLLO':(255,150,40),'HEPHAESTUS':(130,130,140),'HERMES':(110,220,70),'DIONYSUS':(220,70,200)}
OUT='rp'
T=OUT+'/assets/olympian/textures/item'; M=OUT+'/assets/olympian/models/item'; I=OUT+'/assets/olympian/items'
for d in (T,M,I): os.makedirs(d,exist_ok=True)
S=32
def shade(c,f): return tuple(max(0,min(255,int(v*f))) for v in c)
def glyph(d,t,c,cx,cy):
    w=shade(c,1.15); k=(255,255,255)
    def poly(p,col=k): d.polygon([(cx+x,cy+y) for x,y in p],fill=col)
    if t=='AOE':
        for r in (10,6,2): d.ellipse([cx-r,cy-r,cx+r,cy+r],outline=k,width=2)
    elif t=='LEAP': poly([(0,-10),(8,2),(3,2),(3,10),(-3,10),(-3,2),(-8,2)])
    elif t=='CHAIN': poly([(3,-11),(-5,1),(0,1),(-3,11),(6,-2),(1,-2)])
    elif t=='DASH':
        for i in (-6,0,6): d.line([cx-10,cy+i,cx+4,cy+i],fill=k,width=2)
        poly([(4,-9),(12,0),(4,9)])
    elif t=='HEAL': d.rectangle([cx-3,cy-10,cx+3,cy+10],fill=k); d.rectangle([cx-10,cy-3,cx+10,cy+3],fill=k)
    elif t=='BUFF': poly([(0,-11),(3,-3),(11,-3),(5,3),(7,11),(0,6),(-7,11),(-5,3),(-11,-3),(-3,-3)])
    elif t=='GUARD': poly([(-9,-9),(9,-9),(9,2),(0,11),(-9,2)])
    elif t=='PROJECTILE': d.line([cx-10,cy+10,cx+8,cy-8],fill=k,width=3); poly([(12,-12),(2,-10),(10,-2)])
    elif t=='DRAIN': d.ellipse([cx-9,cy-9,cx+9,cy+9],outline=k,width=2); d.ellipse([cx-3,cy-3,cx+3,cy+3],fill=k)
    elif t=='TRAP':
        for i in range(-9,10,6): d.line([cx+i,cy-10,cx+i,cy+10],fill=k,width=2)
        for i in range(-9,10,6): d.line([cx-10,cy+i,cx+10,cy+i],fill=k,width=2)
    elif t=='SUMMON': d.ellipse([cx-4,cy-10,cx+4,cy-2],fill=k); poly([(-8,10),(0,-1),(8,10)])
    elif t=='BEAM': d.rectangle([cx-11,cy-3,cx+11,cy+3],fill=k); d.rectangle([cx-11,cy-1,cx+11,cy+1],fill=(255,255,200))
    elif t=='BLINK': poly([(0,-11),(8,0),(0,11),(-8,0)]); d.ellipse([cx-3,cy-3,cx+3,cy+3],fill=shade(c,0.6))
    elif t=='FLIGHT': poly([(0,-4),(12,-10),(6,2),(0,10),(-6,2),(-12,-10)])
    elif t=='STORM':
        d.ellipse([cx-11,cy-9,cx+3,cy+1],fill=k); d.ellipse([cx-3,cy-11,cx+11,cy+1],fill=k); poly([(2,0),(-3,10),(1,10),(-1,15),(6,4),(2,4)],(255,230,80))
    elif t=='REVEAL': d.ellipse([cx-11,cy-6,cx+11,cy+6],outline=k,width=2); d.ellipse([cx-4,cy-4,cx+4,cy+4],fill=k)
    elif t=='MARK':
        d.ellipse([cx-9,cy-9,cx+9,cy+9],outline=k,width=2); d.line([cx-12,cy,cx+12,cy],fill=k,width=2); d.line([cx,cy-12,cx,cy+12],fill=k,width=2)
    else: d.ellipse([cx-6,cy-6,cx+6,cy+6],fill=k)
def icon(name,c,t=None,emblem=False):
    im=Image.new('RGBA',(S,S),(0,0,0,0)); d=ImageDraw.Draw(im)
    for y in range(S):
        f=1.15-0.55*y/S
        d.line([2,y,S-3,y],fill=shade(c,f)+(255,))
    d.rectangle([0,0,S-1,S-1],outline=shade(c,0.45)+(255,),width=2)
    d.rectangle([2,2,S-3,S-3],outline=shade(c,1.3)+(255,),width=1)
    for x,y in ((0,0),(S-1,0),(0,S-1),(S-1,S-1)): d.point((x,y),fill=(0,0,0,0))
    if emblem:
        cx=cy=S//2
        for r,col in ((12,(255,255,255)),(9,shade(c,0.6)),(5,(255,255,255))): d.ellipse([cx-r,cy-r,cx+r,cy+r],fill=col+(255,))
        d.polygon([(cx,cy-14),(cx+3,cy-6),(cx-3,cy-6)],fill=(255,255,255,255))
    else: glyph(d,t,c,S//2,S//2)
    im.save(f'{T}/{name}.png')
    json.dump({"parent":"minecraft:item/generated","textures":{"layer0":f"olympian:item/{name}"}},open(f'{M}/{name}.json','w'))
    json.dump({"model":{"type":"minecraft:model","model":f"olympian:item/{name}"}},open(f'{I}/{name}.json','w'))
n=0
for g in REAL:
    c=COL.get(g,(200,200,200)); icon('god_'+g.lower(),c,emblem=True); n+=1
    for i,(an,t) in enumerate(abil[g]): icon(f'a_{g.lower()}_{i}',c,t); n+=1
ui={'train':((220,60,60),'MARK'),'board':((90,200,90),'REVEAL'),'shop':((60,200,140),'BUFF'),'legacy':((190,110,230),'SUMMON'),
    'abilities':((70,200,240),'CHAIN'),'warp':((240,240,240),'BLINK'),'keys':((250,190,50),'DASH'),'back':((170,170,170),'DASH'),
    'ascend':((255,215,60),'FLIGHT'),'boss':((150,20,40),'DRAIN'),'elite':((255,150,40),'GUARD'),'combat':((200,70,70),'AOE')}
for k,(c,t) in ui.items(): icon('ui_'+k,c,t); n+=1
json.dump({"pack":{"description":"Olympian Trials - Camp Aegis","min_format":[75,0],"max_format":[200,0]}},open(OUT+'/pack.mcmeta','w'))
# wide pack icon
Image.new('RGB',(64,64),(250,215,60)).save(OUT+'/pack.png')

# ---------- v2: weapons, armor, orbs, extra UI ----------
import sys
sys.path.insert(0,'.')
from sprites import T as TPL
def sprite(tmpl, god_col, name, metal=None, trim=(255,215,80), handheld=True):
    rows=[r.ljust(16,'.') for r in tmpl.strip('\n').split('\n')]
    assert len(rows)==16, (name,len(rows))
    im=Image.new('RGBA',(16,16),(0,0,0,0))
    met=metal or (210,212,222)
    pal={'K':(35,28,30),'H':(255,255,255),'M':met,'m':shade(met,0.65),
         'W':(130,85,45),'w':(90,55,30),'G':god_col,'g':shade(god_col,0.6),'Y':(240,200,60),'T':trim}
    for y,r in enumerate(rows):
        for x,ch in enumerate(r[:16]):
            if ch in pal: im.putpixel((x,y),pal[ch]+(255,))
    im.save(f'{T}/{name}.png')
    json.dump({"parent":"minecraft:item/handheld" if handheld else "minecraft:item/generated","textures":{"layer0":f"olympian:item/{name}"}},open(f'{M}/{name}.json','w'))
    json.dump({"model":{"type":"minecraft:model","model":f"olympian:item/{name}"}},open(f'{I}/{name}.json','w'))

WEAP={'ZEUS':('trident',(255,230,90)),'POSEIDON':('trident',(120,230,255)),'HADES':('scythe',(120,110,140)),
      'ATHENA':('sword',(225,230,245)),'ARES':('axe',(200,200,205)),'APOLLO':('bow',None),'HEPHAESTUS':('hammer',(150,150,160)),
      'HERMES':('dagger',(250,215,90)),'DIONYSUS':('staff',None)}
TRIM={'ZEUS':(255,240,150),'POSEIDON':(180,250,255),'HADES':(200,150,255),'ATHENA':(245,215,110),'ARES':(255,90,60),
      'APOLLO':(255,240,150),'HEPHAESTUS':(255,140,40),'HERMES':(230,255,200),'DIONYSUS':(160,240,90)}
for g in REAL:
    c=COL[g]; tp,metal=WEAP[g]
    sprite(TPL[tp], c, 'w_'+g.lower(), metal=metal); n+=1
    for pc in ('helmet','chest','legs','boots'):
        sprite(TPL[pc], c, f'ar_{g.lower()}_{pc}', trim=TRIM[g], handheld=False); n+=1
    # orb
    im=Image.new('RGBA',(16,16),(0,0,0,0))
    for y in range(16):
        for x in range(16):
            d=math.hypot(x-7.5,y-7.5)
            if d<7.2:
                f=1-d/7.2
                col=tuple(int(min(255,v*(0.6+0.8*f)+255*f*f*0.7)) for v in c)
                im.putpixel((x,y),col+(int(255*min(1,0.35+f*1.4)),))
    im.save(f'{T}/orb_{g.lower()}.png')
    json.dump({"parent":"minecraft:item/generated","textures":{"layer0":f"olympian:item/orb_{g.lower()}"}},open(f'{M}/orb_{g.lower()}.json','w'))
    json.dump({"model":{"type":"minecraft:model","model":f"olympian:item/orb_{g.lower()}"}},open(f'{I}/orb_{g.lower()}.json','w'))
    n+=1
more={'armory':((230,160,40),'GUARD'),'quests':((240,220,90),'REVEAL'),'quest':((235,235,235),'MARK'),'done':((90,210,90),'HEAL'),
      'cabins':((80,200,230),'SUMMON'),'events':((200,90,230),'STORM'),'upgrade':((90,220,120),'LEAP'),'titles':((240,190,50),'BUFF'),'ult':((255,120,40),'STORM'),'locked':((90,90,95),'GUARD')}
for k,(c,t) in more.items(): icon('ui_'+k,c,t); n+=1
bosses={'lionheart':((230,170,40),'AOE'),'broodqueen':((70,150,50),'TRAP'),'tempest':((80,190,240),'STORM'),'kronar':((200,60,50),'GUARD'),'hollowking':((110,30,60),'DRAIN')}
for k,(c,t) in bosses.items(): icon('boss_'+k,c,t); n+=1
import glob
for f in glob.glob(T+'/*.png'):
    im=Image.open(f).convert('RGBA'); im.quantize(colors=48,method=Image.Quantize.FASTOCTREE).save(f,optimize=True)
for f in glob.glob(OUT+'/**/*.json',recursive=True)+[OUT+'/pack.mcmeta']:
    j=json.load(open(f)); json.dump(j,open(f,'w'),separators=(',',':'))
Image.new('RGB',(16,16),(250,215,60)).save(OUT+'/pack.png',optimize=True)
z='OlympianTrials-Pack.zip'
if os.path.exists(z): os.remove(z)
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as zf:
    for r,_,fs in os.walk(OUT):
        for f in fs:
            p=os.path.join(r,f); zf.write(p,os.path.relpath(p,OUT))
print(n,'icons', hashlib.sha1(open(z,'rb').read()).hexdigest(), os.path.getsize(z))

