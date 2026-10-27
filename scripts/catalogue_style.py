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
QA=ROOT/'tmp/pdfs/collection-2026'; QA.mkdir(parents=True,exist_ok=True)
W,H=841.89,595.28
NAVY=HexColor('#091d35'); RED=HexColor('#851c1d'); PAPER=HexColor('#faf9f6'); MUTED=HexColor('#626a72'); LINE=HexColor('#d8dbd8'); SAND=HexColor('#efede7')
font_path=Path('C:/Windows/Fonts')
pdfmetrics.registerFont(TTFont('Body',str(font_path/'arial.ttf')))
pdfmetrics.registerFont(TTFont('Bold',str(font_path/'arialbd.ttf')))
pdfmetrics.registerFont(TTFont('Display',str(font_path/'georgia.ttf')))
pdfmetrics.registerFont(TTFont('Italic',str(font_path/'georgiai.ttf')))
logo=Image.open(ROOT/'public/images/original/Zaka-logo-transparent.png').convert('RGBA')
logo.save(QA/'logo.png')



def text(c,x,y,value,size=11,font='Body',color=NAVY):
    c.setFillColor(color);c.setFont(font,size);c.drawString(x,y,value)

def para(c,x,y,value,width=300,size=11,color=MUTED,leading=None,font='Body'):
    style=ParagraphStyle('p',fontName=font,fontSize=size,leading=leading or size*1.6,textColor=color)
    p=Paragraph(value.replace('&amp;','&').replace('&','&amp;'),style);_,h=p.wrap(width,500);p.drawOn(c,x,y-h);return y-h

def rect(c,x,y,w,h,fill=SAND,stroke=None):
    c.setFillColor(fill);c.setStrokeColor(stroke or fill);c.rect(x,y,w,h,fill=1,stroke=bool(stroke))

def line(c,x1,y1,x2,y2,color=LINE,lw=.6):
    c.setStrokeColor(color);c.setLineWidth(lw);c.line(x1,y1,x2,y2)

def header(c,d,page,section):
    rect(c,0,0,W,H,PAPER)
    c.drawImage(str(QA/'logo.png'),40,H-74,width=110,height=64,mask='auto',preserveAspectRatio=True,anchor='c')
    text(c,400,H-38,'THE ZAKA DESIGN COLLECTION',9,'Bold',RED)
    text(c,400,H-54,section.upper(),8,'Body',MUTED)
    text(c,W-123,H-38,d['code']+' / '+d.get('revision','01'),9,'Bold')
    text(c,W-123,H-54,'OCTOBER 2026',8,'Body',MUTED)
    line(c,40,H-82,W-40,H-82)
    line(c,40,43,W-40,43)
    text(c,40,27,'ZAKA ENGINEERING CONTAINERS & PREFAB (PVT. LTD.)',7,'Bold')
    text(c,350,27,'CONCEPT DESIGN / NOT TO SCALE / FOR CLIENT DISCUSSION',6.5,'Body',MUTED)
    text(c,W-92,27,f"{page:02d} / {d.get('pages',6):02d}",8,'Bold')
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

def spec_page(c,d):
    header(c,d,d.get('pages',6)-1,'Outline specifications')
    heading(c,'04 / Materials & systems','The details make the difference.','An outline schedule for client discussion. Material grades, thicknesses, capacity, and performance are confirmed in the project quotation.')
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
    header(c,d,d.get('pages',6),'Your project brief')
    heading(c,'05 / Make it yours','A clear plan for your next step.','Bring us your site and requirements. We will help develop the layout, scope, and quotation for your project.')
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
