from pathlib import Path
from io import BytesIO
import math
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, Color, white
from reportlab.lib.utils import ImageReader
from pypdf import PdfReader, PdfWriter
import pypdfium2 as pdfium
from PIL import Image, ImageDraw
from bed_furniture import draw_bed, audit_beds
from catalogue_names import filename
from roof_styles import apply_config, image_path as roof_image_path, draw_panel as roof_panel

REPO=Path(__file__).resolve().parents[1]
ROOT=REPO/'output'/'pdf'
TMP=REPO/'tmp'/'pdfs'/'client-revision-04'; TMP.mkdir(parents=True,exist_ok=True)
ASSETS=REPO/'public'/'images'/'generated'/'client-revision-04'
W,H=841.89,595.28
REF=PdfReader(ROOT/filename('zaka-two-bedroom-residence.pdf'))
LOGO=Image.open(REPO/'public/images/original/Zaka-logo-transparent.png').convert('RGBA')
INK='#17283B'; MUTED='#657079'; RED='#8D302D'

def txt(c,x,y,s,size=9,color=INK,font='Helvetica',align='left'):
    c.setFillColor(HexColor(color)); c.setFont(font,size)
    getattr(c,{'left':'drawString','center':'drawCentredString','right':'drawRightString'}[align])(x,y,s)

def wrap(c,s,x,y,width,size=9,color=INK,leading=None,font='Helvetica'):
    leading=leading or size*1.45; line=''
    for word in s.split():
        test=(line+' '+word).strip()
        if c.stringWidth(test,font,size)>width and line:
            txt(c,x,y,line,size,color,font); y-=leading; line=word
        else: line=test
    if line: txt(c,x,y,line,size,color,font); y-=leading
    return y

def rect(c,x,y,w,h,fill=None,stroke=INK,lw=1):
    c.setLineWidth(lw); c.setStrokeColor(HexColor(stroke)); c.setFillColor(HexColor(fill or '#FFFFFF'))
    c.rect(x,y,w,h,stroke=bool(stroke),fill=bool(fill))

def border(c,cfg):
    a=cfg['accent']; c.setStrokeColor(HexColor(a)); c.setLineWidth(1)
    if cfg['border']==0:
        c.rect(14,14,W-28,H-28,stroke=1,fill=0); c.setLineWidth(.3); c.rect(19,19,W-38,H-38,stroke=1,fill=0)
    elif cfg['border']==1:
        for x,y,dx,dy in [(15,15,1,1),(W-15,15,-1,1),(15,H-15,1,-1),(W-15,H-15,-1,-1)]:
            c.setLineWidth(2.5); c.line(x,y,x+dx*54,y); c.line(x,y,x,y+dy*54)
    elif cfg['border']==2:
        rect(c,14,14,5,H-28,a,a); rect(c,W-19,14,5,H-28,a,a)
    else:
        c.setDash(6,3); c.roundRect(15,15,W-30,H-30,9,stroke=1,fill=0); c.setDash()

def frame(c,cfg,section,page,total,title=None,sub=None):
    rect(c,0,0,W,H,'#FAF9F6','#FAF9F6')
    border(c,cfg)
    c.drawImage(ImageReader(LOGO),40,520,110,64,mask='auto')
    txt(c,400,559,'THE ZAKA DESIGN COLLECTION',8,RED,'Helvetica-Bold')
    txt(c,400,544,section.upper(),6.4,MUTED)
    txt(c,718,559,cfg['code']+' / 04',8,INK,'Helvetica-Bold')
    txt(c,718,544,'OCTOBER 2026',6.5,MUTED)
    c.setStrokeColor(HexColor('#CBD0D1')); c.setLineWidth(.6); c.line(40,513,802,513); c.line(40,42,802,42)
    txt(c,40,29,'ZAKA ENGINEERING CONTAINERS & PREFAB (PVT. LTD.)',6,INK,'Helvetica-Bold')
    txt(c,350,29,'CONCEPT DESIGN / NOMINAL FEET / FOR CLIENT DISCUSSION',5.8,MUTED)
    txt(c,775,29,f'{page:02d} / {total:02d}',6,INK)
    if title:
        txt(c,40,488,section.upper(),7,RED,'Helvetica-Bold'); txt(c,40,460,title,25,INK,'Times-Roman')
        if sub: wrap(c,sub,40,440,750,8.5,MUTED)

class Plan:
    def __init__(self,c,length,width,x,y,s,cfg):
        self.c=c; self.L=length; self.B=width; self.x=x; self.y=y; self.s=s; self.cfg=cfg
        self.beds=[];self.windows=[];self.doors=[];self.obstacles=[]
    def pt(self,x,y): return self.x+x*self.s,self.y+y*self.s
    def box(self,x,y,w,h,fill='#E2E3E2',lw=1):
        X,Y=self.pt(x,y); rect(self.c,X,Y,w*self.s,h*self.s,fill,INK,lw)
    def line(self,x1,y1,x2,y2,color=INK,lw=1):
        a,b=self.pt(x1,y1); d,e=self.pt(x2,y2); self.c.setLineWidth(lw); self.c.setStrokeColor(HexColor(color)); self.c.line(a,b,d,e)
    def label(self,x,y,s,size=8):
        X,Y=self.pt(x,y)
        for i,line in enumerate(s.split('\n')): txt(self.c,X,Y-i*(size+2),line,size,INK,'Helvetica-Bold' if i==0 else 'Helvetica',align='center')
    def win(self,x,y,length,vert=False,tag='W1'):
        self.windows.append(dict(x=x,y=y,size=length,vertical=vert,tag=tag))
        dx,dy=(0,length) if vert else (length,0); self.line(x,y,x+dx,y+dy,'#FAF9F6',5)
        for off in [-.12,.12]: self.line(x+off if vert else x,y if vert else y+off,x+off+dx if vert else x+dx,y+dy if vert else y+off,'#607C8C',1)
        X,Y=self.pt(x+dx/2,y+dy/2); txt(self.c,X+7 if vert else X,Y-3 if vert else Y+7,tag,6.5,'#3C6374',align='left' if vert else 'center')
    def door(self,x,y,width=3,vert=False,tag='D1',sign=1,reverse=False):
        self.doors.append(dict(x=x,y=y,size=width,vertical=vert,sign=sign,reverse=reverse,tag=tag))
        c=self.c; X,Y=self.pt(x,y); v=width*self.s
        self.line(x,y,x+(0 if vert else width),y+(width if vert else 0),'#FAF9F6',5)
        if reverse:
            if vert:Y+=v
            else:X+=v
        direction=-1 if reverse else 1
        dx,dy=(0,direction*v) if vert else (direction*v,0);ex,ey=(sign*v,0) if vert else (0,sign*v)
        c.setStrokeColor(HexColor(self.cfg['accent']));c.setLineWidth(.9);c.line(X,Y,X+ex,Y+ey)
        k=.5522848;path=c.beginPath();path.moveTo(X+dx,Y+dy)
        path.curveTo(X+dx+k*ex,Y+dy+k*ey,X+ex+k*dx,Y+ey+k*dy,X+ex,Y+ey)
        c.setLineWidth(.5);c.drawPath(path)
        if vert:
            txt(c,X+sign*10,Y+direction*v/2,tag,6,self.cfg['accent'],align='center')
        else:
            txt(c,X+v/2,Y-11 if sign>0 else Y+8,tag,6,self.cfg['accent'],align='center')
    def cupboard(self,x,y,w=6,h=2):
        self.obstacles.append((x,y,w,h))
        self.box(x,y,w,h,'#B8B4AC',.6); self.line(x,y,x+w,y+h,'#87857E',.4); self.line(x+w,y,x,y+h,'#87857E',.4)
        if h>w:
            X,Y=self.pt(x+w/2,y+h/2);self.c.saveState();self.c.translate(X,Y);self.c.rotate(90)
            txt(self.c,0,0,'CUPBOARD / 2 ft deep',5.4,align='center');self.c.restoreState()
        else:self.label(x+w/2,y+h/2-.1,'CUPBOARD',5.7)
    def bed(self,x,y,w,h,head,room):
        self.beds.append(dict(x=x,y=y,width=w,height=h,head=head,room=room,name='Bedroom / sleeping zone'))
        draw_bed(self.c,x,y,w,h,head,self.s,(self.x,self.y))
    def bath(self,x,y,w,h,tag='WC',door='east'):
        self.obstacles.append((x,y,w,h))
        self.box(x,y,w,h,'#DCE6E7'); self.label(x+w/2,y+h/2+.2,tag+f'\n{w:g} x {h:g} ft',6.5)
        X,Y=self.pt(x+.7,y+h-.7); self.c.setStrokeColor(HexColor('#71858B')); self.c.ellipse(X-3,Y-5,X+3,Y+4,stroke=1,fill=0)
        if door=='none': return
        if door=='east': self.door(x+w,y+.7,2.5,True,'D3',-1)
        elif door=='west': self.door(x,y+.7,2.5,True,'D3',1)
        else: self.door(x+.5,y,2.5,False,'D3')
    def kitchen(self,x,y,w=8,h=2):
        self.box(x,y,w,h,'#BBBDB7',.6); self.label(x+w/2,y+h/2-.1,'OPEN KITCHEN',5.9)
        X,Y=self.pt(x+.5,y+.4); self.c.setStrokeColor(HexColor('#707773')); self.c.rect(X,Y,self.s*1.2,self.s*.9,stroke=1,fill=0)
    def sofa_l(self,x,y):
        self.box(x,y,2,7,'#AEB8B5',.65);self.box(x,y,6,2,'#AEB8B5',.65)
        for offset in (2.2,4.4):self.line(x,y+offset,x+2,y+offset,'#7F8D88',.45)
        self.line(x+3.5,y,x+3.5,y+2,'#7F8D88',.45)
        self.label(x+4.2,y+3,'L-SOFA',5.6)
    def dimensions(self):
        audit_beds(self.beds,self.windows,self.doors,self.obstacles,self.cfg['file']+f' / page {self.c.getPageNumber()}')
        c=self.c; x,y=self.x,self.y; s=self.s
        c.setLineWidth(.5); c.setStrokeColor(HexColor(MUTED)); c.line(x,y+self.B*s+18,x+self.L*s,y+self.B*s+18)
        for a in [x,x+self.L*s]: c.line(a,y+self.B*s+12,a,y+self.B*s+24)
        txt(c,x+self.L*s/2,y+self.B*s+25,f'{self.L:g} ft overall',8,INK,align='center')
        c.line(x-24,y,x-24,y+self.B*s)
        for b in [y,y+self.B*s]: c.line(x-29,b,x-19,b)
        c.saveState(); c.translate(x-31,y+self.B*s/2); c.rotate(90); txt(c,0,0,f'{self.B:g} ft',8,INK,align='center'); c.restoreState()

def table(c,rows,x,y,width=762,col=185,rowh=29,size=8):
    for i,(a,b) in enumerate(rows):
        if i%2==0: rect(c,x,y-rowh+6,width,rowh,'#EFEEEA','#EFEEEA')
        txt(c,x+8,y-10,a,size,INK,'Helvetica-Bold'); wrap(c,b,x+col,y-10,width-col-12,size,MUTED,leading=size+2); y-=rowh
    return y

def notes(c,rows,y=153):
    txt(c,40,y,'ROOM SCHEDULE / NOMINAL FEET',7,RED,'Helvetica-Bold')
    table(c,rows,40,y-13,rowh=22,size=7.4)
    txt(c,40,52,'Beds: 5 x 6.5 ft; solid-wall headboards; minimum 2.5 ft access at both long sides and the foot.',6.4,MUTED)

def ground(c,cfg):
    p=Plan(c,40,24,215,175,9,cfg); p.box(0,0,40,24,'#F0EFEB',2)
    p.box(0,0,12,24,'#D9DADB'); p.box(28,0,12,24,'#D9DADB')
    p.bath(0,19,6,5,'ENSUITE 1'); p.bath(34,19,6,5,'ENSUITE 2','west')
    p.cupboard(6,22,6,2); p.cupboard(28,22,6,2)
    p.bed(5.5,9,6.5,5,'east',(0,0,12,18));p.bed(28,9,6.5,5,'west',(28,0,12,18))
    p.label(6,16,'BEDROOM 1\n12 x 18 ft sleeping zone'); p.label(34,16,'BEDROOM 2\n12 x 18 ft sleeping zone')
    p.label(20,8,'LIVING / DINING\n16 x 24 ft central space'); p.kitchen(14,22,12,2)
    p.box(26,17,2,7,'#BBBDB7',.6);p.label(25,16,'L-KITCHEN',6)
    p.sofa_l(12.5,12)
    p.door(12,3.5,3.5,True,'D2',-1); p.door(28,3.5,3.5,True,'D2',1); p.door(18,0,4,False,'D1')
    for x in [2,30]: p.win(x,0,8,False,'W1')
    p.win(0,5,8,True,'W1'); p.win(40,5,8,True,'W1'); p.win(15,24,6,False,'W3')
    p.win(1.5,24,2,False,'V1'); p.win(36.5,24,2,False,'V1'); p.dimensions()
    notes(c,[('Two side modules','12 x 24 ft each; beds face inward from solid room partitions, clear of front/side windows and dressing access.'),('Shared centre','L-shaped kitchen in the same rear position; L-shaped sofa against the side partition near the washroom/dressing zone.'),('Overall / circulation','40 x 24 ft = 960 sq ft; 16 x 24 ft living/dining, with clear entry and bedroom access.')],140)

def first(c,cfg):
    p=Plan(c,40,24,215,175,9,cfg); p.box(0,0,40,12,'#EAE8E2',1.3); p.label(20,5.5,'OPEN TERRACE\n40 x 12 ft / 480 sq ft')
    for a,b,d,e in [(0,0,40,0),(0,0,0,12),(40,0,40,12)]:
        p.line(a,b,d,e,cfg['accent'],2); p.line(a+.15,b+.25,d-.15 if d else d+.15,e+.25,cfg['accent'],.5)
    p.box(0,12,15,12,'#D9DADB'); p.box(15,12,10,12,'#F2F1ED'); p.box(25,12,15,12,'#D9DADB')
    p.bath(0,18,4,6,'ENSUITE 3'); p.bath(36,18,4,6,'ENSUITE 4','west')
    p.cupboard(0,12,2,6); p.cupboard(38,12,2,6)
    p.bed(7,17.5,5,6.5,'north',(0,12,15,12));p.bed(28,17.5,5,6.5,'north',(25,12,15,12))
    p.label(8.5,15.5,'BEDROOM 3\n15 x 12 ft gross',7); p.label(31.5,15.5,'BEDROOM 4\n15 x 12 ft gross',7)
    p.label(20,20,'LIVING\n9 x 12 ft clear',7); p.door(18,12,4,False,'D1'); p.door(15,13,3.5,True,'D2',-1); p.door(25,13,3.5,True,'D2',1)
    p.win(3,12,8,False,'W1'); p.win(29,12,8,False,'W1'); p.win(17,24,6,False,'W2'); p.win(1,24,2,False,'V1'); p.win(37,24,2,False,'V1'); p.dimensions()
    notes(c,[('Enclosed unit / terrace','40 x 12 ft enclosed unit + parallel 40 x 12 ft front terrace. Ensuites rotated to 4 ft along length x 6 ft along 12 ft end.'),('Length reconciliation','15 ft bedroom + 9 ft clear living + 15 ft bedroom + 1 ft combined partition allowance = 40 ft.'),('Access / railing','2 ft deep cupboards below the ensuites on the outer end walls. Living entry faces terrace; railing on exposed edges.')],140)

def residence(c,cfg,L):
    s=14;p=Plan(c,L,12,(W-L*s)/2,229,s,cfg);p.box(0,0,L,12,'#F1F0EC',2)
    if L==40:
        p.box(0,0,14,12,'#D9DADB');p.box(14,0,14,12,'#D9DADB')
        p.bath(0,8,6,4,'ENSUITE 1');p.bath(22,8,6,4,'ENSUITE 2','west')
        p.cupboard(0,0,2,6);p.cupboard(26,0,2,4)
        p.bed(7.5,2.5,6.5,5,'east',(0,0,14,12));p.bed(14,2.5,6.5,5,'west',(14,0,14,12))
        p.label(8,1.8,'BEDROOM 1\n14 x 12 ft suite',7.2);p.label(21,1.8,'BEDROOM 2\n14 x 12 ft suite',7.2)
        p.kitchen(29,10,10,2);p.label(34,6,'LIVING / OPEN KITCHEN\n12 x 12 ft',7.5)
        p.door(14,8.5,3,True,'D7',-1);p.door(28,4.5,3.5,True,'D2',-1);p.door(29,0,3.5,False,'D1')
        for x in (4,16):p.win(x,0,6,False,'W2')
        p.win(7,12,6,False,'W2');p.win(15,12,6,False,'W2');p.win(40,3,6,True,'W2');p.win(32,12,4,False,'W4')
        p.win(2,12,2,False,'V1');p.win(24,12,2,False,'V1')
        rows=[('Long-wall ensuites','Two 6 x 4 ft ensuites on the rear 40 ft side, each entered only from its bedroom.'),('Internal bedroom access','Living opens into bedroom 2; a 3 ft connecting door leads from bedroom 2 to bedroom 1. No outside bedroom entry is needed.'),('Building area','12 x 40 ft = 480 sq ft; two 14 x 12 ft gross bedroom suites plus 12 x 12 ft end living/open kitchen.')]
    else:
        p.box(0,0,14,12,'#D9DADB');p.box(30,0,14,12,'#D9DADB')
        p.bath(0,6,4,6,'ENSUITE 1','south');p.bath(40,6,4,6,'ENSUITE 2','south')
        p.cupboard(0,0,2,6);p.cupboard(42,0,2,6)
        p.bed(7.5,4.5,6.5,5,'east',(0,0,14,12));p.bed(30,4.5,6.5,5,'west',(30,0,14,12))
        p.label(8,2.7,'BEDROOM 1\n14 x 12 ft suite',7.2);p.label(36,2.7,'BEDROOM 2\n14 x 12 ft suite',7.2)
        p.kitchen(15,10,14,2);p.label(22,6,'LIVING / OPEN KITCHEN\n12 x 16 ft',8)
        p.door(14,.5,3,True,'D2',-1);p.door(30,.5,3,True,'D2',1);p.door(20.25,0,3.5,False,'D1')
        for x in (5,33):p.win(x,0,6,False,'W2')
        for x in (6,32):p.win(x,12,6,False,'W2')
        p.win(20,12,4,False,'W4')
        p.win(1,12,2,False,'V1');p.win(41,12,2,False,'V1')
        rows=[('Rear-corner washrooms','4 x 6 ft ensuites relocated to the two outside rear corners, along the 12 ft bedroom ends, away from living entry.'),('Central living / kitchen','12 x 16 ft shared living/open-kitchen bay. Both bedrooms open directly into living; cupboards are 2 ft deep.'),('Building area','12 x 44 ft = 528 sq ft; two 14 x 12 ft gross suites include attached washrooms and cupboards.')]
    p.dimensions();notes(c,rows,180)

def office(c,cfg,L):
    rec=L-30; e=16+rec; s=14; p=Plan(c,L,12,(W-L*s)/2,229,s,cfg); p.box(0,0,L,12,'#F1F0EC',2)
    p.box(0,0,10,12,'#D9DADB');p.box(10,0,6,4.5,'#EBE8E0');p.box(10,4.5,6,2.5,'#FAF9F6');p.bath(10,7,6,5,'WASHROOM','none')
    p.box(10.3,.3,5.4,1.7,'#BBBDB7',.6);p.box(10.7,.6,1.2,.8,'#F6F5F1',.4)
    p.label(14,3.1,'KITCHEN\n6 x 4.5 ft',6.3);p.label(13,5.55,'2.5 ft PASSAGE',6)
    p.door(10.5,4.5,2.5,False,'D6',-1);p.door(13,7,2.5,False,'D3',1)
    p.box(e,0,14,12,'#D5D7D8')
    p.bed(2.5,0,5,6.5,'south',(0,0,10,12));p.cupboard(8,8,2,4);p.label(4,10.5,'BEDROOM\n10 x 12 ft',7.5)
    p.label(16+rec/2,8,'RECEPTION\n'+str(rec)+' x 12 ft',8); p.label(e+7,9,'EXECUTIVE OFFICE\n14 x 12 ft',8)
    p.box(e+5,3,6,3,'#B8B7B0',.6); p.box(17,4,4,2,'#C6C2B8',.5)
    p.door(10,4.5,2.5,True,'D2',-1,reverse=True);p.line(16,4.5,16,7,'#FAF9F6',5)
    p.door(e,1,3.5,True,'D4',1); p.door(17,0,3.5,False,'D1')
    p.line(e,5,e,12,'#71919E',1.5); p.label(e+.6,7,'GLASS',5.3)
    p.win(1,12,4,False,'W5'); p.win(0,3,4,True,'W5'); p.win(17,12,6,False,'W2'); p.win(e+4,0,6,False,'W2'); p.win(L,3,6,True,'W2'); p.win(12,12,2,False,'V1');p.win(11,0,4,False,'W4'); p.dimensions()
    notes(c,[('Rooms / service bay',f'Bedroom 10 x 12 ft; service bay 6 x 12 ft; reception {rec} x 12 ft; executive office 14 x 12 ft.'),('Passage / room widths','12 ft width = 4.5 ft kitchen + 2.5 ft passage + 5 ft washroom. Both services are entered from the passage.'),('Access / glazing','Executive office: front and right-end windows; rear window removed. Bedroom headboard uses the solid front wall.')],180)

def studio(c,cfg):
    p=Plan(c,26,12,200,195,17,cfg); p.box(0,0,21,12,'#F0EFEB',2); p.box(21,0,5,12,'#E5E2DB',1.2)
    p.bath(0,6,5,6,'WASHROOM','south'); p.kitchen(0,0,5,2); p.cupboard(5,6,2,6)
    p.bed(9.5,5.5,5,6.5,'north',(0,0,21,12))
    p.label(16.9,7.6,'OPEN STUDIO\n21 x 12 ft gross',7.3); p.label(23.5,7,'TERRACE\n5 x 12 ft',7)
    p.door(21,1,3.5,True,'D1',-1); p.win(21,6,5,True,'W6'); p.win(8,0,4,False,'W4'); p.win(17,12,4,False,'W4'); p.win(1,12,2,False,'V1')
    p.line(26,0,26,12,cfg['accent'],2); p.line(21,12,26,12,cfg['accent'],2); p.dimensions()
    notes(c,[('External footprint','12 x 26 ft = 312 sq ft including terrace.'),('Enclosed studio','12 x 21 ft gross; 5 x 6 ft washroom. Wardrobe moved beside its side wall: 2 ft deep x 6 ft long.'),('Outdoor / openings','12 x 5 ft terrace = 60 sq ft. Washroom door moved to the studio-facing wall to keep wardrobe access clear.')],175)

def photo_panel(c,cfg,index,x,y,w,h):
    slug=cfg.get('roofSlug')
    if slug and roof_image_path(slug):return roof_panel(c,slug,index,x,y,w,h)
    key='family' if cfg['type']=='duplex' else cfg['type']
    path=ASSETS/(key+'.png')
    im=Image.open(path); iw,ih=im.size
    # Select a contact-sheet panel by PDF clipping; source pixels stay unmodified.
    pw,ph=iw/2,ih/2; inset=3
    left=(index%2)*pw+inset; top=(index//2)*ph+inset
    rw,rh=pw-2*inset,ph-2*inset
    scale=min(w/rw,h/rh); dx=x+(w-rw*scale)/2; dy=y+(h-rh*scale)/2
    c.saveState(); clip=c.beginPath(); clip.rect(dx,dy,rw*scale,rh*scale); c.clipPath(clip,stroke=0,fill=0)
    c.drawImage(str(path),dx-left*scale,dy-(ih-top-rh)*scale,iw*scale,ih*scale)
    c.restoreState()

def elevations(c,cfg,kind):
    for i in range(2):
        x=40+i*390; index=kind*2+i
        rect(c,x,190,372,232,'#ECEBE6','#ECEBE6')
        photo_panel(c,cfg,index,x+8,198,356,216)
        labels=['FRONT / ENTRY PERSPECTIVE','EXTERIOR / OPPOSITE PERSPECTIVE','LEFT / SIDE PERSPECTIVE','RIGHT / SIDE PERSPECTIVE']
        txt(c,x,174,labels[index],8,RED,'Helvetica-Bold')
        wrap(c,cfg['finish'],x,159,372,7,MUTED,leading=10)
    wrap(c,'FINISH DIRECTION: '+cfg['palette'],40,128,750,9)
    note='AI-generated architectural concept images illustrate materials, lighting and landscape. The dimensioned floor plans and opening schedule control the layout.'
    if cfg['type']=='office': note+=' The 44 ft option is illustrated; the 40 ft option has a shorter reception bay.'
    elif cfg['type']=='residence': note+=' The 44 ft finish concept is illustrated. The 40 ft option has long-wall ensuites and an internal connecting door between the bedrooms.'
    wrap(c,note,40,94,750,8,MUTED)
    return

def vector_elevations(c,cfg,kind):
    sides=['FRONT / ENTRY FACADE','REAR / SERVICE FACADE'] if kind==0 else ['LEFT / END VIEW','RIGHT / END VIEW']
    for i,label in enumerate(sides):
        x=40+i*390; y=210; w=372; h=198
        rect(c,x,y,w,h,'#ECEBE6','#ECEBE6')
        length=40 if cfg['type']=='duplex' else (44 if cfg['type'] in ['residence','office'] else 26)
        span=length if kind==0 else (24 if cfg['type']=='duplex' else 12)
        sc=min(325/span,8); bw=span*sc; bh=(17 if cfg['type']=='duplex' else 9)*sc
        bx=x+(w-bw)/2; by=y+28
        rect(c,bx,by,bw,bh,cfg['body'],cfg['trim'],1.5)
        c.setStrokeColor(HexColor(cfg['trim'])); c.setLineWidth(.25)
        for u in range(1,int(span*2)): c.line(bx+u*sc/2,by,bx+u*sc/2,by+bh)
        rect(c,bx-3,by+bh,bw+6,5,cfg['trim'],cfg['trim'])
        if cfg['type']=='duplex':
            c.setLineWidth(2); c.line(bx,by+bh/2,bx+bw,by+bh/2)
            for z in range(0,int(bw),14): c.line(bx+z,by+bh/2,bx+z,by+bh/2+12)
            c.line(bx,by+bh/2+12,bx+bw,by+bh/2+12)
        for f in range(2 if cfg['type']=='duplex' else 1):
            yy=by+bh*(f+.23)/(2 if cfg['type']=='duplex' else 1)
            for q in [.18,.68]:
                ww=min(50,bw*.2); rect(c,bx+bw*q,yy,ww,25,'#B7C9CF',cfg['trim'],2)
                c.setStrokeColor(HexColor(cfg['trim'])); c.line(bx+bw*q+ww/2,yy,bx+bw*q+ww/2,yy+25)
        if kind==0 and i==0: rect(c,bx+bw*.45,by,18,min(42,bh*.6),'#7F9195',cfg['trim'],2)
        c.setStrokeColor(HexColor('#878E8D')); c.setLineWidth(1); c.line(x+15,by,x+w-15,by)
        txt(c,x,y-19,label,8,RED,'Helvetica-Bold'); txt(c,x,y-35,f'{span} ft nominal span / '+cfg['finish'],7,MUTED)
    wrap(c,'FINISH DIRECTION: '+cfg['palette'],40,141,750,9)
    wrap(c,'Newly drawn schematic elevations follow this proposal. Window tags, positions and sizes are controlled by the floor plans and opening schedule. The 40 ft and 44 ft alternatives share the same finish direction.',40,105,750,8,MUTED)

def hero(c,cfg):
    rect(c,315,156,487,277,'#EDECE7','#EDECE7')
    photo_panel(c,cfg,0,325,174,467,247)
    txt(c,330,164,'PHOTOREALISTIC ARCHITECTURAL CONCEPT',6.5,MUTED)
    return

def vector_hero(c,cfg):
    # Vector axonometric, keeping the cover visual tied to the actual module geometry.
    x,y=369,225; a=330; b=85; h=118 if cfg['type']=='duplex' else 83
    def poly(pts,fill):
        p=c.beginPath(); p.moveTo(*pts[0]); [p.lineTo(*v) for v in pts[1:]]; p.close(); c.setFillColor(HexColor(fill)); c.setStrokeColor(HexColor(cfg['trim'])); c.setLineWidth(1); c.drawPath(p,fill=1,stroke=1)
    rect(c,315,156,487,277,'#EDECE7','#EDECE7')
    poly([(x,y),(x+a,y),(x+a,y+h),(x,y+h)],cfg['body'])
    poly([(x+a,y),(x+a+b,y+49),(x+a+b,y+h+49),(x+a,y+h)],cfg['trim'])
    poly([(x,y+h),(x+b,y+h+49),(x+a+b,y+h+49),(x+a,y+h)],'#ECEDE9')
    for j in range(1,33):
        c.setStrokeColor(HexColor(cfg['trim'])); c.setLineWidth(.3); c.line(x+j*10,y,x+j*10,y+h)
    for f in range(2 if cfg['type']=='duplex' else 1):
        yy=y+18+f*58
        for xx in [x+22,x+234]: rect(c,xx,yy,58,33,'#B9CDD2',cfg['trim'],3)
        rect(c,x+139,yy-18,29,50,'#789198',cfg['trim'],2)
    if cfg['type']=='duplex':
        c.setStrokeColor(HexColor(cfg['trim'])); c.setLineWidth(2); c.line(x,y+58,x+a,y+58)
        for j in range(0,331,15): c.line(x+j,y+58,x+j,y+75)
        c.line(x,y+75,x+a,y+75)
    txt(c,330,171,'ORIGINAL VECTOR CONCEPT / FINISH STUDY',6.5,MUTED)

CONFIGS=[
dict(type='duplex',code='ZC-01',file='zaka-client-01-family-home-two-floors.pdf',title='Family Home\n& Terrace',short='Two-floor family home',dims='40 x 24 ft',body='#B9BEC1',trim='#33383B',accent='#526E72',border=0,finish='Grey body / charcoal frame / white soffits',palette='Light grey cladding, charcoal steel frame, white roof and soffits; muted teal double border.',desc='Four bedrooms across two floors: two on the ground floor and two upstairs. A full-length first-floor terrace extends the living space.',area='960 sq ft ground + 480 sq ft upper enclosed + 480 sq ft terrace'),
dict(type='residence',code='ZC-02',file='zaka-client-02-two-bedroom-12x40-and-12x44.pdf',title='Two Bedroom\nLiving',short='Two bedroom residence',dims='12 x 40 / 44 ft',body='#454A4E',trim='#ECEDEA',accent='#9B7254',border=1,finish='Charcoal body / white trim / grey roof',palette='Charcoal corrugated body, white window frames and light grey roof; copper corner border.',desc='Two alternative layouts, each with two bedrooms, attached washrooms and living with an open kitchen. The 40 ft option uses long-wall ensuites and an internal bedroom connection; the 44 ft option uses rear-corner washrooms.',area='480 sq ft / 528 sq ft enclosed'),
dict(type='office',code='ZC-03',file='zaka-client-03-office-12x40-and-12x44.pdf',title='Executive\nOffice Suite',short='Office with rest bedroom',dims='12 x 40 / 44 ft',body='#EBECE8',trim='#41474D',accent='#596C88',border=2,finish='White body / charcoal trim / grey accents',palette='White cladding, charcoal frames and grey service panels; slate-blue side border.',desc='Two office sizes with a bedroom, enclosed kitchen and washroom accessed from a 2.5 ft passage, reception and a separate executive office behind a glazed partition.',area='480 sq ft / 528 sq ft enclosed'),
dict(type='studio',code='ZC-04',file='zaka-client-04-studio-12x26-with-terrace.pdf',title='Studio\n& Terrace',short='Open studio with front terrace',dims='12 x 26 ft overall',body='#C9CAC8',trim='#484B50',accent='#815D6A',border=3,finish='Warm grey body / white fascia / charcoal frame',palette='Warm grey cladding, charcoal frame and white roof fascia; plum dashed round-corner border.',desc='A 12 x 21 ft enclosed studio with a 5 x 6 ft washroom, open kitchen and cupboard, opening onto a 12 x 5 ft terrace.',area='252 sq ft enclosed + 60 sq ft terrace')]

def author(cfg):
    cfg=apply_config({**cfg,'file':filename(cfg['file'])})
    plans=2 if cfg['type']!='studio' else 1; total=11+plans # adds dedicated opening schedule
    buf=BytesIO(); c=canvas.Canvas(buf,pagesize=(W,H)); c.setTitle(cfg['short']+' | Zaka client revision')
    n=0
    def page(section,title=None,sub=None):
        nonlocal n
        n+=1; frame(c,cfg,section,n,total,title,sub)
    page('Revision 04 / client sketch')
    txt(c,40,485,'INDIVIDUAL DESIGN / '+cfg['code'],7,RED,'Helvetica-Bold')
    for j,line in enumerate(cfg['title'].split('\n')): txt(c,40,448-j*32,line,29,INK,'Times-Roman')
    wrap(c,cfg['desc'],40,345,240,10,MUTED)
    txt(c,40,209,cfg['dims'],21,INK,'Times-Roman'); wrap(c,cfg['area'],40,186,245,8,MUTED)
    txt(c,40,141,'FLOOR PLANS + FOUR EXTERIOR VIEWS',7,RED,'Helvetica-Bold'); hero(c,cfg); c.showPage()
    sub='Nominal feet before wall deductions. Doors, windows, washrooms, cupboards and circulation are shown on plan.'
    if cfg['type']=='duplex':
        page('01 / ground floor','Two bedrooms. A shared centre.',sub); ground(c,cfg); c.showPage()
        page('01 / first floor','Two bedrooms. A full-length terrace.',sub); first(c,cfg); c.showPage()
    elif cfg['type']=='residence':
        for L in [40,44]: page(f'01 / 12 x {L} ft option',f'12 x {L} ft. Two bedroom suites.',sub); residence(c,cfg,L); c.showPage()
    elif cfg['type']=='office':
        for L in [40,44]: page(f'01 / 12 x {L} ft option',f'12 x {L} ft. Work and reception.',sub); office(c,cfg,L); c.showPage()
    else: page('01 / studio floor plan','21 ft inside. 5 ft terrace.',sub); studio(c,cfg); c.showPage()
    page('02 / doors, windows & finishes','Every opening. Clearly scheduled.','Window dimensions are width x height; locations follow the tags on the floor plans. All door sizes are clear nominal openings.')
    rows=[('D1 / main entrance',"4 ft x 6 ft 6 in (home); 3 ft 6 in x 6 ft 6 in (other units)."),('D2 / internal doors',"2 ft 6 in x 6 ft 6 in at office bedroom/passage; 3 ft 6 in x 6 ft 6 in for home/residence bedrooms."),('D3 / washroom doors',"2 ft 6 in x 6 ft 6 in; moisture-resistant finish."),('D4 / executive office',"3 ft 6 in x 7 ft glazed door within glazed reception partition."),('D5 / separate bedroom entry',"3 ft 6 in x 6 ft 6 in; outside entry to bedroom 1 in the 40 ft residence option."),('D6 / enclosed kitchen',"2 ft 6 in x 6 ft 6 in; entered only from office service passage."),('W1 / home bedrooms',"8 ft x 6 ft; front and outer side walls as drawn."),('W2 / living & offices',"6 ft x 4 ft; living, bedroom and executive-office walls where tagged."),('W3 / home kitchen',"6 ft x 4 ft; rear wall above kitchen counter."),('W4 / kitchen / studio',"4 ft x 4 ft; studio long walls, residence kitchen and office kitchen."),('W5 / office bedroom',"4 ft x 5 ft; bedroom end and rear walls."),('W6 / studio terrace',"5 ft x 4 ft; glazed opening beside terrace entrance."),('V1 / washroom vent',"2 ft x 1 ft 6 in, high-level frosted opening; mechanical extract provision.")]
    if cfg['type']=='residence':rows.append(('D7 / bedroom connection','3 ft x 6 ft 6 in; internal door between bedrooms 2 and 1 in the 40 ft option.'))
    used={'duplex':{'D1','D2','D3','W1','W2','W3','V1'},'residence':{'D1','D2','D3','D7','W2','W4','V1'},'office':{'D1','D2','D3','D4','D6','W2','W4','W5','V1'},'studio':{'D1','D3','W4','W6','V1'}}[cfg['type']]
    rows=[row for row in rows if row[0].split(' / ')[0] in used]
    if cfg['type']=='residence':rows=[(a,'3 ft clear in the 44 ft option; 3 ft 6 in in the 40 ft option. Door height 6 ft 6 in.' if a.startswith('D2 /') else b) for a,b in rows]
    rows.append(('Cupboard / wardrobe','2 ft deep x 6 ft long beside the studio washroom.' if cfg['type']=='studio' else '2 ft deep; positions and lengths follow the floor plan.'))
    rows.append(('Finish selection',cfg['palette']))
    table(c,rows,40,405,rowh=25,size=8)
    wrap(c,'Only the tags shown on each plan apply to that option. Typical cupboard depth is 2 ft. Window sill heights, opening direction, final wall build-up and stair connections require coordination before fabrication.',40,83,750,8,MUTED); c.showPage()
    for k in [0,1]: page('03 / exterior design','The same design. Brought to life.','Four photorealistic exterior perspectives. Grey, charcoal and white are arranged differently for each proposal.'); elevations(c,cfg,k); c.showPage()
    page('04 / materials & programme','Details for this design.','Spatial brief and finish direction for project quotation.')
    rows=[('Building',cfg['short']+' / '+cfg['dims']),('Floor area',cfg['area']),('Exterior palette',cfg['palette']),('Roof & terrace',cfg.get('roofSpecification','Flat roof concept; drainage and waterproofing coordinated with the final structural design.')),('Structure','Fabricated / joined steel modules; supports, connections and openings developed for the selected site.'),('Comfort & finish','Insulated walls and roof; washable internal linings; slip-resistant wet area finishes.'),('Glazing & doors','Opening sizes and positions follow the new plans and dedicated schedule.'),('Electrical & services','Power, lighting, sockets, kitchen supply and washroom plumbing coordinated with available site services.'),('Circulation & access','Door swings and furniture are indicative. External stair to first-floor terrace is additional to footprint.' if cfg['type']=='duplex' else 'Door swings and furniture are indicative; confirm clear circulation after wall deductions.'),('Delivery & installation','Transport route, crane access, supports and anchoring agreed before manufacture.')]
    table(c,rows,40,405,rowh=29,size=8); wrap(c,'Concept proposal: nominal dimensions are not fabrication dimensions. Original client material standards follow on the next five pages.',40,82,745,8,MUTED); c.showPage()
    # Preserve the complete five material-standard pages from the existing catalogue.
    # These pages are appended after this authored sequence and receive new page IDs.
    c.save(); new=PdfReader(BytesIO(buf.getvalue())); writer=PdfWriter()
    for p in new.pages: writer.add_page(p)
    for j in range(5,10):
        source=REF.pages[j]; overlay=BytesIO(); oc=canvas.Canvas(overlay,pagesize=(W,H)); border(oc,cfg)
        rect(oc,707,538,91,30,'#FAF9F6','#FAF9F6'); txt(oc,718,559,cfg['code']+' / 04',8,INK,'Helvetica-Bold'); txt(oc,718,544,'OCTOBER 2026',6.5,MUTED)
        rect(oc,742,22,59,15,'#FAF9F6','#FAF9F6'); txt(oc,775,29,f'{len(writer.pages)+1:02d} / {total:02d}',6,INK)
        oc.save(); writer.add_page(source); writer.pages[-1].merge_page(PdfReader(BytesIO(overlay.getvalue())).pages[0])
    # Retain the original contact / project-brief page with consistent identifiers.
    overlay=BytesIO(); oc=canvas.Canvas(overlay,pagesize=(W,H)); border(oc,cfg)
    rect(oc,707,538,91,30,'#FAF9F6','#FAF9F6'); txt(oc,718,559,cfg['code']+' / 04',8,INK,'Helvetica-Bold'); txt(oc,718,544,'OCTOBER 2026',6.5,MUTED)
    rect(oc,742,22,59,15,'#FAF9F6','#FAF9F6'); txt(oc,775,29,f'{total:02d} / {total:02d}',6,INK); oc.save()
    writer.add_page(REF.pages[10]); writer.pages[-1].merge_page(PdfReader(BytesIO(overlay.getvalue())).pages[0])
    assert len(writer.pages)==total,(len(writer.pages),total)
    writer.add_metadata({'/Title':cfg['short']+' - Client floor plan revision','/Author':'Zaka Engineering Containers & Prefab','/Subject':'Client sketch interpretation with nominal dimensions and opening schedules'})
    path=ROOT/cfg['file']; writer.write(path)
    from watermark_catalogues import add_watermark
    add_watermark(path,path)
    return path

if __name__=='__main__':
    for cfg in CONFIGS:
        path=author(cfg); d=pdfium.PdfDocument(str(path)); thumbs=[]
        for i in range(len(d)):
            img=d[i].render(scale=.8).to_pil(); img.save(TMP/(path.stem+f'-{i+1:02d}.png'))
            img.thumbnail((421,298)); thumbs.append(img)
        sheet=Image.new('RGB',(1263,math.ceil(len(thumbs)/3)*298),'#D8D9D9'); draw=ImageDraw.Draw(sheet)
        for i,img in enumerate(thumbs): sheet.paste(img,((i%3)*421,(i//3)*298)); draw.text(((i%3)*421+7,(i//3)*298+7),str(i+1),fill='#B00000')
        sheet.save(TMP/(path.stem+'-contact.png')); print(path.name,len(d),'pages')
