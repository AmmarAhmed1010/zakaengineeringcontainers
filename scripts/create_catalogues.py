"""Reproducible, original architectural concept catalogues inspired by supplied references."""
from pathlib import Path
import math, json, shutil
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, Color
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import ImageReader
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from PIL import Image, ImageOps, ImageDraw
import pymupdf

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'output/pdf'; OUT.mkdir(parents=True,exist_ok=True)
PUBLIC=ROOT/'public/downloads'; PUBLIC.mkdir(parents=True,exist_ok=True)
PREVIEW=ROOT/'public/images/pdf'; PREVIEW.mkdir(parents=True,exist_ok=True)
QA=ROOT/'tmp/pdfs'; QA.mkdir(parents=True,exist_ok=True)
W,H=841.89,595.28
NAVY=HexColor('#091d35'); RED=HexColor('#851c1d'); PAPER=HexColor('#faf9f6'); MUTED=HexColor('#626a72'); LINE=HexColor('#d8dbd8'); SAND=HexColor('#efede7')
font_path=Path('C:/Windows/Fonts')
pdfmetrics.registerFont(TTFont('Body',str(font_path/'arial.ttf')))
pdfmetrics.registerFont(TTFont('Bold',str(font_path/'arialbd.ttf')))
pdfmetrics.registerFont(TTFont('Display',str(font_path/'georgia.ttf')))
pdfmetrics.registerFont(TTFont('Italic',str(font_path/'georgiai.ttf')))
logo=Image.open(ROOT/'public/images/original/LOGO-ZAKA-ENGINEERING-1.png').convert('RGB')
logo=logo.crop((15,85,487,360));logo.save(QA/'logo.png')

catalogues=[
 {'slug':'single-cabin-office','title':'Single Cabin Office','code':'ZE-C01','subtitle':'One focused workspace. Everything you need.','length':20,'width':8,'height':8.5,'area':160,'image':'office','type':'office','use':'Compact office / 2-3 workstations','description':'A compact container office with one main workspace, an entry lobby, and an attached washroom. A simple arrangement for a site office or a small business workspace.','rooms':[('Office cabin',16,8),('Entry lobby',4,4),('Washroom',4,4)],'inspiration':'Single-cabin 8 x 20 office catalogue (zaka.pdf).'},
 {'slug':'two-cabin-office','title':'Two Cabin Office','code':'ZE-C02','subtitle':'Private workspaces. A shared footprint.','length':20,'width':8,'height':8.5,'area':160,'image':'office','type':'two-office','use':'Two private cabins / 2-4 workstations','description':'Two private office cabins are connected through a central shared entry zone with a compact washroom. A practical concept for teams that need privacy within a small footprint.','rooms':[('Cabin 01',8,8),('Cabin 02',8,8),('Entry lobby',4,4),('Washroom',4,4)],'inspiration':'Two-cabin 8 x 20 office catalogue (zaka1.pdf).'},
 {'slug':'two-bedroom-residence','title':'Two Bedroom Residence','code':'ZE-C03','subtitle':'A little more room for everyday life.','length':40,'width':16,'height':9.5,'area':640,'image':'hero','type':'residence','use':'Two bedrooms / living / kitchen / two baths','description':'A two-bedroom container residence with a central living room and kitchen. Each bedroom zone incorporates a bathroom and storage, keeping shared spaces at the heart of the home.','rooms':[('Bedroom zone 01',14,16),('Bedroom zone 02',14,16),('Living room',12,9),('Kitchen',12,7)],'inspiration':'ZE-2501-02, 16 x 40 x 9 ft 6 in residential proposal, supplied reference.'},
 {'slug':'compact-container-home','title':'Compact Container Home','code':'ZE-C04','subtitle':'Live comfortably. Make every metre count.','length':40,'width':12,'height':8.5,'area':480,'image':'hero','type':'compact','use':'One bedroom / open living / dining / kitchen','description':'A compact residential concept with a private bedroom, bathroom, and an open living and dining area. The kitchen occupies the far end of the shared zone, with an alternate two-bedroom concept available.','rooms':[('Bedroom / bath zone',14,12),('Living / dining',18,12),('Kitchen',8,12)],'inspiration':'PK-2411-01 proposals 02 and 03, 12 x 40 residential layouts, supplied references.'},
 {'slug':'industrial-field-office','title':'Industrial Field Office','code':'ZE-C05','subtitle':'A clear base for site operations.','length':20,'width':8,'height':8.5,'area':160,'image':'office','type':'field','use':'Plan review / communications / equipment storage','description':'A compact site operations office with a central plan-review workspace, a communications zone, and equipment storage. This concept keeps operational tasks together in a relocatable footprint.','rooms':[('Plan review',12,8),('Communications',4,8),('Gear / pantry',4,8)],'inspiration':'Industrial Field Office & Site Operations Command, supplied six-page reference.'},
]

def text(c,x,y,value,size=11,font='Body',color=NAVY):
    c.setFillColor(color);c.setFont(font,size);c.drawString(x,y,value)
def para(c,x,y,value,width=300,size=11,color=MUTED,leading=None,font='Body'):
    style=ParagraphStyle('p',fontName=font,fontSize=size,leading=leading or size*1.6,textColor=color)
    p=Paragraph(value.replace('&amp;','&').replace('&','&amp;'),style);_,h=p.wrap(width,500);p.drawOn(c,x,y-h);return y-h
def rect(c,x,y,w,h,fill=SAND,stroke=None):
    c.setFillColor(fill);c.setStrokeColor(stroke or fill);c.rect(x,y,w,h,fill=1,stroke=bool(stroke))
def line(c,x1,y1,x2,y2,color=LINE,lw=.6):
    c.setStrokeColor(color);c.setLineWidth(lw);c.line(x1,y1,x2,y2)
def image(c,path,x,y,w,h):
    im=Image.open(path).convert('RGB');im=ImageOps.fit(im,(int(w*2),int(h*2)))
    c.drawImage(ImageReader(im),x,y,width=w,height=h)
def header(c,d,page,section):
    rect(c,0,0,W,H,PAPER)
    c.drawImage(str(QA/'logo.png'),40,H-74,width=110,height=64,mask='auto',preserveAspectRatio=True,anchor='c')
    text(c,400,H-38,'THE ZAKA DESIGN COLLECTION',9,'Bold',RED)
    text(c,400,H-54,section.upper(),8,'Body',MUTED)
    text(c,W-123,H-38,d['code']+' / 01',9,'Bold')
    text(c,W-123,H-54,'OCTOBER 2026',8,'Body',MUTED)
    line(c,40,H-82,W-40,H-82)
    line(c,40,43,W-40,43)
    text(c,40,27,'ZAKA ENGINEERING CONTAINERS & PREFAB (PVT. LTD.)',7,'Bold')
    text(c,350,27,'CONCEPT DESIGN / NOT TO SCALE / FOR CLIENT DISCUSSION',6.5,'Body',MUTED)
    text(c,W-92,27,f'{page:02d} / 05',8,'Bold')
    c.setTitle(d['title']+' | Zaka Engineering Concept Catalogue')
    c.setAuthor('Zaka Engineering Containers & Prefab (Pvt. Ltd.)')
    c.setSubject('Illustrative container design catalogue with concept floor plan, elevations and outline specifications')
def heading(c,kicker,title,subtitle=None):
    text(c,40,H-111,kicker.upper(),8,'Bold',RED)
    text(c,40,H-149,title,30,'Display')
    if subtitle: para(c,40,H-166,subtitle,W-80,10)
def dim(c,x1,y1,x2,y2,label):
    line(c,x1,y1,x2,y2,MUTED,.5)
    if y1==y2:
        line(c,x1,y1-5,x1,y1+5,MUTED,.5);line(c,x2,y2-5,x2,y2+5,MUTED,.5)
        c.setFont('Body',8);tw=pdfmetrics.stringWidth(label,'Body',8);rect(c,(x1+x2)/2-tw/2-6,y1-4,tw+12,13,PAPER);text(c,(x1+x2)/2-tw/2,y1,label,8)
    else:
        line(c,x1-5,y1,x1+5,y1,MUTED,.5);line(c,x2-5,y2,x2+5,y2,MUTED,.5)
        c.saveState();c.translate(x1-8,(y1+y2)/2);c.rotate(90);text(c,-pdfmetrics.stringWidth(label,'Body',8)/2,0,label,8);c.restoreState()
def plan(c,d,x,y,w):
    scale=w/d['length'];h=d['width']*scale
    def r(a,b,l,k,fill=SAND): rect(c,x+a*scale,y+b*scale,l*scale,k*scale,fill,NAVY)
    def wall(a,b,aa,bb): line(c,x+a*scale,y+b*scale,x+aa*scale,y+bb*scale,NAVY,1.3)
    def label(a,b,title,sub=''):
        cx=x+a*scale;cy=y+b*scale;c.setFont('Bold',9);c.setFillColor(NAVY);c.drawCentredString(cx,cy,title.upper())
        if sub:c.setFont('Body',8);c.setFillColor(MUTED);c.drawCentredString(cx,cy-14,sub)
    def window(a,b,l,vertical=False):
        xx=x+a*scale;yy=y+b*scale
        if vertical:line(c,xx,yy,xx,yy+l*scale,HexColor('#57879a'),3)
        else:line(c,xx,yy,xx+l*scale,yy,HexColor('#57879a'),3)
    def door(a,b,l=3):
        xx=x+a*scale;yy=y+b*scale
        line(c,xx,yy,xx+l*scale,yy,PAPER,3);line(c,xx,yy,xx,yy+l*scale,RED,.7);c.setStrokeColor(RED);c.setLineWidth(.5);c.arc(xx-l*scale,yy-l*scale,xx+l*scale,yy+l*scale,0,90)
    def desk(a,b,l=3,k=1.5):r(a,b,l,k,HexColor('#e0d6c7'))
    def vdoor(a,b,l=2.5):
        xx=x+a*scale;yy=y+b*scale
        line(c,xx,yy,xx,yy+l*scale,PAPER,3);line(c,xx,yy,xx+l*scale,yy,RED,.7)
        c.setStrokeColor(RED);c.setLineWidth(.5);c.arc(xx-l*scale,yy-l*scale,xx+l*scale,yy+l*scale,0,90)
    def bed(a,b,l=5,k=6):
        r(a,b,l,k,HexColor('#e4ded5'));r(a+.2,b+k-1.4,l-.4,1,HexColor('#faf9f6'))
    def wc(a,b):
        c.setStrokeColor(MUTED);c.setFillColor(PAPER);c.ellipse(x+a*scale,y+b*scale,x+(a+1)*scale,y+(b+1.5)*scale,fill=1,stroke=1)
    r(0,0,d['length'],d['width'],HexColor('#f6f4ee'))
    t=d['type']
    if t=='office':
        wall(4,0,4,8);wall(0,4,4,4);label(12,4,'Office cabin',"16' x 8' / nominal zone");label(2,5.3,'Washroom');label(2,1.5,'Entry');wc(1,6.5);desk(7,6);desk(12,6);door(1,0,2.5);vdoor(4,1);door(.7,4,2.5);window(7,8,4);window(13,0,4)
    elif t=='two-office':
        wall(8,0,8,8);wall(12,0,12,8);wall(8,4,12,4);label(4,4,'Cabin 01',"8' x 8'");label(16,4,'Cabin 02',"8' x 8'");label(10,5.3,'Washroom');label(10,1.5,'Entry');wc(9,6.5);desk(2,6);desk(15,6);door(8.5,0);vdoor(8,1);vdoor(12,1);door(8.7,4,2.5);window(2,8,4);window(14,8,4)
    elif t=='residence':
        wall(14,0,14,16);wall(26,0,26,16);wall(14,9,26,9);wall(4,10,4,16);wall(0,10,4,10);wall(36,10,36,16);wall(36,10,40,10)
        label(7,8.5,'Bedroom zone 01',"14' x 16' incl. bath");label(33,8.5,'Bedroom zone 02',"14' x 16' incl. bath");label(20,5.5,'Living room',"12' x 9'");label(20,12,'Kitchen',"12' x 7'");label(2,12.5,'Bath');label(38,12.5,'Bath');wc(1,14);wc(37,14);bed(1,1);bed(33,1);desk(15,14,10,1.5);desk(22,1,3,1.5);door(18,0,4);vdoor(14,2);vdoor(26,2);vdoor(4,11);vdoor(36,11);door(18,9);window(4,0,5);window(30,0,5);window(17,16,6)
    elif t=='two-home':
        wall(14,0,14,12);wall(26,0,26,12);wall(4,6,4,12);wall(0,6,4,6);wall(36,6,36,12);wall(36,6,40,6)
        label(7,3.5,'Bedroom zone 01',"14' x 12' incl. bath");label(33,3.5,'Bedroom zone 02',"14' x 12' incl. bath");label(20,5,'Living / kitchen',"12' x 12' shared zone");label(2,8,'Bath');label(38,8,'Bath');wc(1,10);wc(37,10);bed(8,6,5,5);bed(27,6,5,5);desk(15,10,10,1.5);door(18,0,4);vdoor(14,1);vdoor(26,1);vdoor(4,7);vdoor(36,7);window(4,0,5);window(30,0,5);window(17,12,6)
    elif t=='compact':
        wall(14,0,14,12);wall(8,6,8,12);wall(0,6,8,6);label(7,3,'Bedroom zone',"14' x 12' incl. bath");label(4,9,'Bathroom',"8' x 6'");label(23,6,'Living / dining',"18' x 12'");label(36,6,'Kitchen',"8' x 12'");wc(1,10);bed(8.5,5,4.5,6);desk(33,10,6,1.3);desk(23,2,5,2);door(24,0);vdoor(14,1);vdoor(8,7);window(3,0,5);window(19,12,5);window(33,0,4)
    else:
        wall(12,0,12,8);wall(16,0,16,8);label(6,3.5,'Plan review',"12' x 8' / 96 sq ft");label(14,3.5,'Comms',"32 sq ft");label(18,3.5,'Gear / pantry',"32 sq ft");desk(1,6,9,1.3);desk(13,6,2,1.2);desk(17,6,2,1.2);door(6,0);vdoor(12,.5);vdoor(16,.5);window(2,8,6);window(13,8,2)
    dim(c,x,y+h+24,x+w,y+h+24,f"{d['length']}' / {round(d['length']*304.8):,} mm nominal")
    dim(c,x-25,y,x-25,y+h,f"{d['width']}' / {round(d['width']*304.8):,} mm")
    text(c,x,y-24,'CONCEPT FLOOR PLAN',8,'Bold',RED)
    text(c,x+w-154,y-24,'Dimensions in feet / NTS',7,'Body',MUTED)
    return h

def elevation(c,d,x,y,w,front=True,dimension=True):
    s=w/d['length'];h=d['height']*s
    rect(c,x,y,w,h,HexColor('#f0eee7'),NAVY)
    for a in range(1,int(d['length']*3)):
        line(c,x+a*s/3,y,x+a*s/3,y+h,HexColor('#c6ccc9'),.25)
    line(c,x,y+h,x+w,y+h,NAVY,3);line(c,x,y,x+w,y,NAVY,2)
    for a in [2,d['length']-6]:rect(c,x+a*s,y+h*.4,4*s,h*.38,HexColor('#c7d7d8'),NAVY)
    if front:rect(c,x+(d['length']/2-1.5)*s,y,3*s,h*.8,PAPER,NAVY)
    rect(c,x-3,y-10,w+6,6,LINE)
    if dimension: dim(c,x,y+h+18,x+w,y+h+18,f"{d['length']}' nominal")
    dim(c,x-20,y,x-20,y+h,f"{d['height']}' nominal")
    text(c,x,y-30,'A-A / FRONT ELEVATION' if front else 'B-B / REAR ELEVATION',8,'Bold',RED)

def cover(c,d):
    header(c,d,1,'Concept catalogue')
    text(c,40,475,'SPACES THAT GO FURTHER',8,'Bold',RED)
    words=d['title'].split();title1=' '.join(words[:-1]);title2=words[-1]
    if d['slug']=='two-bedroom-residence':title1='Two Bedroom';title2='Residence'
    text(c,40,430,title1,30,'Display');text(c,40,392,title2,34,'Italic',RED)
    para(c,40,365,d['subtitle'],240,13,NAVY,19)
    para(c,40,303,d['description'],236,10,MUTED,16)
    line(c,40,192,273,192)
    text(c,40,173,f"{d['width']}' x {d['length']}'",22,'Display')
    text(c,40,153,f"{d['area']} SQ FT / NOMINAL FOOTPRINT",8,'Bold',MUTED)
    text(c,40,123,'A CONCEPT. YOUR STARTING POINT.',7,'Bold',RED)
    para(c,40,110,'Final design, scope and quotation are developed around your site and requirements.',235,8)
    image(c,ROOT/f"public/images/generated/{d['image']}.webp",310,110,490,375)
    rect(c,310,110,490,32,NAVY)
    text(c,327,122,'ARCHITECTURAL VISUALIZATION / ILLUSTRATIVE CONCEPT',7,'Body',PAPER)
    text(c,310,86,'ISLAMABAD, PAKISTAN',8,'Bold',RED)
    text(c,627,86,'DESIGN / FABRICATE / DELIVER',8,'Body',MUTED)
    c.showPage()

def floor_page(c,d):
    header(c,d,2,'Space planning')
    heading(c,'01 / The layout','Designed around daily use.','Nominal planning zones; final clear dimensions depend on the approved wall build-up.')
    w=640 if d['type']=='compact' else 520
    y=175 if d['type']=='compact' else 160
    plan(c,d,110,y,w)
    bottom=90
    text(c,40,bottom+32,'THE SPACE SCHEDULE',8,'Bold',RED)
    x=40
    for name,l,k in d['rooms']:
        text(c,x,bottom+13,name,9,'Bold');text(c,x,bottom-3,f"{l}' x {k}' / {l*k} sq ft",8,'Body',MUTED);x+=185
    para(c,40,65,'Area figures are gross nominal zones, not clear usable areas. Bathrooms within residential bedroom zones are included, not added to the total.',W-80,7.5)
    c.showPage()

def elevation_page(c,d):
    header(c,d,3,'Exterior concept')
    heading(c,'02 / The envelope','A considered exterior.','Window and door arrangements illustrate the design language; positions and sizes are finalized with your layout.')
    w=300 if d['length']==20 else 540; x=100
    elevation(c,d,x,260,w,True)
    elevation(c,d,x,95,w,False,False)
    if d['length']==20:
        x2=545
        para(c,x2,430,'01 / Corrugated steel shell',240,13,NAVY,font='Bold')
        para(c,x2,400,'Durable steel construction with an exterior coating selected for the site and exposure.',230,10)
        para(c,x2,325,'02 / Natural light',240,13,NAVY,font='Bold')
        para(c,x2,295,'Aluminum-framed glazing and opening windows can be selected to suit daylight and ventilation needs.',230,10)
        para(c,x2,217,'03 / Your finish palette',240,13,NAVY,font='Bold')
        para(c,x2,187,'A restrained selection of light cladding, navy frames, warm timber accents, and brick-red brand details.',230,10)
    else:
        text(c,705,405,'STEEL',8,'Bold',RED);para(c,705,388,'A strong shell, finished for the site.',90,8)
        text(c,705,255,'GLAZING',8,'Bold',RED);para(c,705,238,'Light, ventilation and practical openings.',90,8)
        text(c,705,130,'DETAILS',8,'Bold',RED);para(c,705,113,'Roof drainage, seals and anchoring to be detailed.',90,8)
    c.showPage()

def spec_page(c,d):
    header(c,d,4,'Outline specifications')
    heading(c,'03 / Materials & systems','The details make the difference.','An outline schedule for client discussion. Material grades, thicknesses, capacity, and performance are confirmed in the project quotation.')
    rows=[('Structure','Steel container or fabricated prefab frame; openings and reinforcement to be engineered for the approved layout.'),('Exterior finish','Protective primer and coating system selected for exposure, maintenance needs, and the agreed colour palette.'),('Insulation','Wall and roof insulation specification to be agreed for local climate, comfort, and budget.'),('Internal linings','Insulated panel or board lining; washable finishes in wet areas and an agreed finish in occupied spaces.'),('Floor assembly','Existing or fabricated base with a selected floor finish; wet-area waterproofing and thresholds to be detailed.'),('Doors & glazing','Aluminum-framed windows and selected entrance doors; safety glass and hardware specified by opening type.'),('Electrical & data','Lighting, socket and data-point schedule to be agreed; supply requirements and local earthing verified for the site.'),('Climate & ventilation','Ventilation and optional air conditioning sized for occupancy, heat gain, climate, and operating requirements.'),('Plumbing & drainage','Supply, waste, and sanitary connections coordinated with site services where included in the final scope.'),('Delivery & installation','Route access, lifting, support design, anchoring, and service connections agreed before dispatch.')]
    rect(c,40,360,W-80,27,NAVY);text(c,53,370,'SYSTEM',8,'Bold',PAPER);text(c,228,370,'OUTLINE REQUIREMENT',8,'Bold',PAPER)
    y=360
    for i,(label,value) in enumerate(rows):
        rh=27
        rect(c,40,y-rh,W-80,rh,PAPER if i%2 else SAND)
        text(c,53,y-17,label,8,'Bold')
        para(c,228,y-6,value,558,8,MUTED,10)
        y-=rh
    para(c,40,76,'No compliance certification, structural approval, acoustic rating, or fixed cost is asserted by this concept catalogue. Those items require project-specific verification.',W-80,7.5)
    c.showPage()

def planning_page(c,d):
    header(c,d,5,'Your project brief')
    heading(c,'04 / Make it yours','A clear plan for your next step.','Bring us your site and requirements. We will help develop the layout, scope, and quotation for your project.')
    text(c,40,365,'BEFORE WE DESIGN',9,'Bold',RED)
    prompts=['Intended use and number of occupants','City, site access and available footprint','Preferred room layout and finish palette','Available power, water and drainage','Budget range and desired delivery timeline']
    y=338
    for i,p in enumerate(prompts):
        text(c,40,y,f'0{i+1}',8,'Bold',RED);para(c,72,y+3,p,330,10,NAVY);line(c,72,y-22,397,y-22);y-=43
    rect(c,445,139,355,225,NAVY)
    text(c,465,338,'LET\'S BUILD YOUR SPACE.',18,'Display',PAPER)
    para(c,465,307,'Zaka Engineering Containers &amp; Prefab (Pvt. Ltd.)',315,11,PAPER,17)
    text(c,465,258,'+92 340 5221225',22,'Display',PAPER)
    text(c,465,232,'zakaurrehman3020@gmail.com',10,'Body',PAPER)
    text(c,465,213,'zakaengineeringcontainers.com',10,'Body',PAPER)
    para(c,465,188,'Main Jinnah Avenue, near Bukhari Chowk (Attock Petrol), New Mal, Islamabad',305,9,HexColor('#cbd2da'),14)
    c.linkURL('https://wa.me/923405221225',(465,249,755,277),relative=0)
    c.linkURL('https://zakaengineeringcontainers.com',(465,207,745,225),relative=0)
    text(c,40,94,'REFERENCE & DESIGN NOTES',7,'Bold',RED)
    note=d['inspiration']+' Original drawings in this catalogue are newly authored schematic interpretations, not reproductions of approved engineering drawings.'
    if d['type']=='compact':note+=' Alternate brief: two bedrooms can replace the open living arrangement; develop a fresh layout with the team.'
    para(c,40,82,note,W-80,7,MUTED,10)
    c.showPage()

def alternate_page(c,d):
    header(c,d,5,'Alternate residential concept')
    heading(c,'04 / A second possibility','An alternative way to live.','A two-bedroom zoning option within the same 12 x 40 ft footprint, inspired by the supplied Proposal 02.')
    alt=dict(d,type='two-home')
    plan(c,alt,105,165,640)
    para(c,40,112,'TWO BEDROOM ZONES / 168 SQ FT EACH',330,8,NAVY,font='Bold')
    para(c,40,95,'Each includes a compact bathroom. The central shared living and kitchen zone occupies 144 sq ft. Total nominal footprint: 480 sq ft.',335,8)
    text(c,445,104,'DEVELOP YOUR PROJECT WITH ZAKA ENGINEERING',8,'Bold',RED)
    text(c,445,84,'+92 340 5221225 / zakaengineeringcontainers.com',9,'Body')
    para(c,445,70,'New schematic interpretation of PK-2411-01 Proposal 02. Final wall build-ups, clearances and service connections require project design.',355,7,MUTED,10)
    c.linkURL('https://wa.me/923405221225',(445,79,790,99),relative=0)
    c.showPage()

qa=[]
for d in catalogues:
    path=OUT/f"zaka-{d['slug']}.pdf"
    c=canvas.Canvas(str(path),pagesize=(W,H),pageCompression=1)
    cover(c,d);floor_page(c,d);elevation_page(c,d);spec_page(c,d)
    if d['type']=='compact':alternate_page(c,d)
    else:planning_page(c,d)
    c.save()
    shutil.copy2(path,PUBLIC/path.name)
    doc=pymupdf.open(path)
    for i,p in enumerate(doc):
        pix=p.get_pixmap(matrix=pymupdf.Matrix(1.3,1.3));pix.save(str(QA/f"{d['slug']}-{i+1}.png"))
        if i==0:
            im=Image.frombytes('RGB',[pix.width,pix.height],pix.samples);im.save(PREVIEW/f"{d['slug']}.webp",quality=90)
    qa.append({'file':str(path),'pages':len(doc),'pageSize':[W,H],'characters':[len(p.get_text()) for p in doc],'bytes':path.stat().st_size})
    print(path.name,len(doc),'pages',flush=True)
(OUT/'catalogue-manifest.json').write_text(json.dumps(qa,indent=2),encoding='utf8')
files=sorted(QA.glob('*-[1-5].png'))
sheet=Image.new('RGB',(1500,5*245),'#deded9');draw=ImageDraw.Draw(sheet)
for i,p in enumerate(files):
    thumb=ImageOps.contain(Image.open(p),(292,208));sheet.paste(thumb,((i%5)*300,(i//5)*245+25));draw.text(((i%5)*300+4,(i//5)*245+7),p.stem,fill='black')
sheet.save(QA/'contact-sheet.jpg')
print(json.dumps(qa,indent=2))
