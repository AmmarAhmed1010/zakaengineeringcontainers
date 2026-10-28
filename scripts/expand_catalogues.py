"""Build nine detailed catalogues and publish the full thirty-design collection.

Run after create_catalogues.py / create_client_pdfs.py when rebuilding everything.
Existing plans are preserved. Every website entry is backed by one canonical PDF.
"""
from io import BytesIO
import hashlib
import json
from pathlib import Path
import shutil
import sys

from PIL import Image, ImageDraw
from pypdf import PdfReader, PdfWriter
import pypdfium2 as pdfium
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

import create_client_pdfs as base
from create_client_pdfs import Plan, W, H, txt, wrap, rect, table, frame, border
from catalogue_names import filename
from bed_furniture import AUDIT
from zaka_watermarks import add_watermark, LABEL

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'output/pdf'
ASSETS=ROOT/'public/images/generated/collection-30'
PREVIEW=ROOT/'public/images/pdf/collection-30'
QA=ROOT/'tmp/pdfs/collection-30'
REVISION='20261028-collection-30'

# Each room description is also printed on the dedicated room-schedule page.
NEW=[
 dict(slug='courtyard-cafe-12x40',title='Courtyard Cafe',category='Hospitality',L=40,B=12,
      description='A 12 x 40 ft cafe with a 12 x 16 ft kitchen, an internal serving hatch and 12 x 24 ft seating area. Reception sits beside the centred front entrance.',
      rooms=[('Kitchen','16 x 12 ft / 192 sq ft; preparation island, sink, cooking and storage counters.'),('Seating / reception','24 x 12 ft / 288 sq ft; four cafe tables with eight seats, reception and entry circulation.'),('Service connection','5 ft wide internal serving hatch; separate staff door in the kitchen partition.')]),
 dict(slug='cedar-bistro-24x40',title='Cedar Bistro',category='Hospitality',L=40,B=24,
      description='A joined-module restaurant with a 12 x 24 ft kitchen, generous dining room, reception and a separate customer washroom.',
      rooms=[('Kitchen','12 x 24 ft / 288 sq ft; preparation, cooking, wash-up and storage counters.'),('Dining / reception','28 x 24 ft gross / 672 sq ft; six four-seat tables, entry and washroom circulation.'),('Customer washroom','6 x 6 ft within the rear dining corner; entered from dining, separated from food preparation.')]),
 dict(slug='charcoal-takeaway-12x20',title='Charcoal Takeaway',category='Hospitality',L=20,B=12,
      description='A compact takeaway kitchen with an 8 ft serving hatch, separate staff entrance, preparation benches and a 4 x 6 ft staff washroom.',
      rooms=[('Kitchen / service','16 x 12 ft gross / 192 sq ft; cooking and preparation behind the front serving counter.'),('Staff washroom','4 x 6 ft / 24 sq ft; enclosed rear corner.'),('Storage','4 x 6 ft / 24 sq ft; dedicated dry-goods storage with kitchen access.')]),
 dict(slug='slate-team-office-12x32',title='Slate Team Office',category='Workspace',L=32,B=12,
      description='A single-storey office with reception, four workstations, a private executive room, an enclosed kitchen and a washroom.',
      rooms=[('Team / reception','14 x 12 ft / 168 sq ft; four workstations and reception beside front entry.'),('Executive office','12 x 12 ft / 144 sq ft; private desk and visitor seating, front and end windows.'),('Services','6 x 12 ft / 72 sq ft; separate 6 x 6 ft kitchen and 6 x 6 ft washroom.')]),
 dict(slug='ivory-meeting-office-24x32',title='Ivory Meeting Office',category='Workspace',L=32,B=24,
      description='A 24 x 32 ft office pavilion with a meeting room, team workspace, executive room, reception, enclosed kitchen and washroom.',
      rooms=[('Front meeting room','12 x 12 ft / 144 sq ft; six-place conference table.'),('Reception / circulation','8 x 12 ft front zone / 96 sq ft; centred entrance and open rear connection.'),('Team office','12 x 12 ft / 144 sq ft; four workstations.'),('Rear executive / lounge','20 x 12 ft / 240 sq ft; two desks and visitor/lounge seating.'),('Kitchen / washroom','Two 6 x 9 ft service rooms with a shared 12 x 3 ft passage from reception.')]),
 dict(slug='silver-one-bedroom-home-12x32',title='Silver One Bedroom Home',category='Living',L=32,B=12,bedrooms=1,
      description='A one-bedroom home with a separate service bay, kitchen, washroom and storage, opening into a bright living and dining room.',
      rooms=[('Bedroom','12 x 12 ft / 144 sq ft; double bed with solid-wall headboard and wardrobe.'),('Service bay','8 x 12 ft / 96 sq ft; kitchen 8 x 4 ft, passage 8 x 3 ft, washroom 5 x 5 ft and store 3 x 5 ft.'),('Living / dining','12 x 12 ft / 144 sq ft; main entrance and end-wall kitchen-side glazing.')]),
 dict(slug='charcoal-two-bedroom-home-24x32',title='Charcoal Two Bedroom Home',category='Living',L=32,B=24,bedrooms=2,
      description='A two-bedroom joined-module home with rear bedroom suites, two attached washrooms, cupboards and an open kitchen facing shared front living space.',
      rooms=[('Bedroom suites','Two 16 x 12 ft gross zones / 192 sq ft each, including a 5 x 6 ft ensuite and 2 ft deep wardrobe.'),('Living / dining','24 x 12 ft / 288 sq ft; centred front entrance and lounge furniture.'),('Open kitchen','8 x 12 ft / 96 sq ft; L-shaped counter in the front right corner.')]),
 dict(slug='ivory-portable-clinic-12x40',title='Ivory Portable Clinic',category='Portable',L=40,B=12,
      description='A consultation and treatment space with central waiting and reception, staff kitchen and washroom. Doors, privacy glazing and furniture are shown.',
      rooms=[('Consultation','10 x 12 ft / 120 sq ft; consultation desk, examination couch and handwash sink.'),('Service bay','6 x 12 ft / 72 sq ft; separate 6 x 6 ft kitchen and washroom.'),('Reception / waiting','12 x 12 ft / 144 sq ft; centred exterior entrance and internal circulation.'),('Treatment','12 x 12 ft / 144 sq ft; treatment couch, desk, storage and handwash sink.')]),
 dict(slug='grey-learning-studio-12x40',title='Grey Learning Studio',category='Portable',L=40,B=12,
      description='A portable learning space with twelve student desks, a teaching zone, a storage room, staff kitchen and washroom.',
      rooms=[('Classroom','28 x 12 ft / 336 sq ft; twelve seats, central aisle and front teaching area.'),('Service / storage','12 x 12 ft / 144 sq ft; kitchen 6 x 6 ft, washroom 6 x 6 ft and store 6 x 12 ft.'),('Openings','Centred main entrance, classroom end exit, wide teaching windows and high-level washroom vent.')]),
]

PALETTES=[('#454A4E','#ECEDEA','#9B7254'),('#EBECE8','#41474D','#71836A'),('#454A4E','#ECEDEA','#A77C5B'),
          ('#B9BEC1','#33383B','#526E72'),('#EBECE8','#41474D','#596C88'),('#C9CAC8','#484B50','#815D6A'),
          ('#454A4E','#ECEDEA','#8A7760'),('#EBECE8','#41474D','#4D8086'),('#B9BEC1','#33383B','#6B7550')]

def configure(raw,i):
    body,trim,accent=PALETTES[i]
    return {**raw,'code':f'ZE-{22+i:02d}','file':raw['slug']+'.pdf','body':body,'trim':trim,'accent':accent,
            'border':i%4,'finish':('Charcoal' if body=='#454A4E' else 'Ivory' if body=='#EBECE8' else 'Grey')+' steel / contrasting trim',
            'palette':'Grey, charcoal and white steel surfaces; '+accent+' border accent.',
            'bedrooms':raw.get('bedrooms',0),'dims':f"{raw['B']} x {raw['L']} ft",'area':raw['B']*raw['L']}

def furniture(p,x,y,w,h,label='',fill='#B9B8B0'):
    p.box(x,y,w,h,fill,.55)
    if label:p.label(x+w/2,y+h/2+.1,label,5.4)

def cafe_table(p,x,y,four=False):
    furniture(p,x,y,2.5,2,'TABLE','#D6C7B4')
    for a,b in [(x+.7,y-.8),(x+.7,y+2.1)]+([(x-.8,y+.55),(x+2.6,y+.55)] if four else []):furniture(p,a,b,.7,.7)

def kitchen(p,x,y,w,h,side='left'):
    p.box(x,y,w,h,'#E5E2D9')
    furniture(p,x,y+h-2,w,2,'SINK / PREP / HOB')
    if h>=10 and side:furniture(p,x if side=='left' else x+w-2,y,2,h-2,'STORAGE')
    p.label(x+w/2,y+(h-6 if h>=18 else h/2),'KITCHEN',6.8)

def office_desk(p,x,y):
    furniture(p,x,y,4,2,'DESK');furniture(p,x+1.6,y+2.3,.8,.8,'','#CCD0CA')

def floor_plan(c,cfg):
    L,B=cfg['L'],cfg['B'];s=min(17,650/L,215/B)
    p=Plan(c,L,B,(W-L*s)/2,178,s,cfg);p.box(0,0,L,B,'#F1F0EC',2)
    slug=cfg['slug']
    if slug=='courtyard-cafe-12x40':
        kitchen(p,0,0,16,12);furniture(p,6,4,6,2,'PREP ISLAND')
        p.box(16,0,24,12,'#E4E8E2');p.label(27,6.2,'SEATING / RECEPTION\n24 x 12 ft',7)
        furniture(p,23,1,4,2,'RECEPTION')
        for x in (29,35):
            for y in (2,8):cafe_table(p,x,y)
        p.door(18,0,4,tag='D1');p.door(16,.4,3,True,'D2',-1)
        p.win(16,5,5,True,'S1');p.win(4,0,6,tag='W2');p.win(4,12,6,tag='W2')
        for x in (28,35):p.win(x,0,4,tag='W1');p.win(x,12,4,tag='W1')
        p.win(40,4,4,True,'W1')
    elif slug=='cedar-bistro-24x40':
        kitchen(p,0,0,12,24);furniture(p,5,7,4,8,'PREP')
        p.line(12,0,12,24);p.door(12,3,3,True,'D2',-1);p.win(12,11,6,True,'S2')
        p.bath(34,18,6,6,door='south');p.win(36,24,2,tag='V1')
        p.door(18,0,4,tag='D1');p.door(4,0,3,tag='D5')
        furniture(p,23,2,5,2,'RECEPTION');p.label(24,11,'DINING / 24 SEATS',7)
        for x in (16,24,32):
            for y in (6,14):cafe_table(p,x,y,True)
        for x in (2,15,24):p.win(x,24,6,tag='W2')
        p.win(29,0,6,tag='W2');p.win(40,6,6,True,'W2');p.win(0,6,4,True,'W1')
    elif slug=='charcoal-takeaway-12x20':
        kitchen(p,0,0,16,12,side=None);p.bath(16,6,4,6,door='west');p.box(16,0,4,6,'#E2DED4');p.label(18,4,'DRY STORE',5.5)
        p.door(16,1,2.5,True,'D2',-1);p.door(0,1,3,True,'D1',1)
        furniture(p,4,0,9,2,'ORDER / PICKUP');furniture(p,6,5,6,2,'PREP')
        p.win(4,0,8,tag='S3');p.win(5,12,4,tag='W1');p.win(17,12,2,tag='V1')
    elif slug=='slate-team-office-12x32':
        kitchen(p,0,0,6,6);p.bath(0,6,6,6);p.door(6,.5,2.5,True,'D2',-1)
        p.box(20,0,12,12,'#DDE3E1');p.label(26,8,'EXECUTIVE\n12 x 12 ft',7);p.door(20,1,3,True,'D4')
        for x in (8,14):office_desk(p,x,8)
        office_desk(p,8,2);office_desk(p,15,4.5)
        office_desk(p,24,3);p.label(13,11.4,'TEAM / RECEPTION',6)
        p.door(14,0,4,tag='D1');p.win(1,12,2,tag='V1');p.win(1,0,4,tag='W1')
        p.win(8,12,6,tag='W2');p.win(24,0,6,tag='W2');p.win(32,5,4,True,'W1')
    elif slug=='ivory-meeting-office-24x32':
        p.box(0,0,12,12,'#DDE3E1');furniture(p,3,4,6,3,'MEETING / 6')
        for x in (3,5.5,8):furniture(p,x,2.8,.8,.8);furniture(p,x,7.4,.8,.8)
        p.door(12,1,3,True,'D2',-1);p.box(20,0,12,12,'#DDE3E1');p.door(20,1,3,True,'D2')
        for x in (21,27):
            for y in (4,8):office_desk(p,x,y)
        kitchen(p,0,15,6,9);p.bath(6,15,6,9,door='none');p.door(7,15,2.5,tag='D3')
        p.door(3,15,2.5,tag='D2');p.line(12,15,12,24);p.line(0,12,12,12);p.label(6,13,'PASSAGE / 3 ft',5)
        office_desk(p,17,20);office_desk(p,25,20);furniture(p,23,13,6,2,'LOUNGE');p.label(21,18,'EXECUTIVE / LOUNGE',6)
        p.door(14,0,4,tag='D1');furniture(p,14,8,4,2,'RECEPTION')
        p.win(3,0,6,tag='W2');p.win(23,0,6,tag='W2');p.win(18,24,6,tag='W2')
        p.win(0,17,4,True,'W1');p.win(8,24,2,tag='V1');p.win(32,15,6,True,'W2')
    elif slug=='silver-one-bedroom-home-12x32':
        p.box(0,0,12,12,'#D9DADB');p.bed(0,3.5,6.5,5,'west',(0,0,12,12));p.cupboard(10,8,2,4)
        p.label(6,10.8,'BEDROOM / 12 x 12 ft',6.2)
        kitchen(p,12,0,8,4);p.box(12,7,5,5,'#DCE6E7');p.label(14.5,9.7,'WC\n5 x 5 ft',6)
        p.box(17,7,3,5,'#E2DED4');p.label(18.5,10,'STORE',5.7)
        p.door(12.5,7,2.5,tag='D3');p.door(17.2,7,2.5,tag='D2');p.label(16,5.8,'PASSAGE / 3 ft',5.5)
        p.door(12,4.2,2.6,True,'D2',1);p.line(20,0,20,12);p.door(20,4.2,2.6,True,'D2')
        furniture(p,24,9,6,2,'SOFA');cafe_table(p,28,4,True);p.label(26,7.8,'LIVING / DINING',6.5)
        p.door(24,0,4,tag='D1');p.win(3,0,6,tag='W2');p.win(3,12,6,tag='W2')
        p.win(13,0,4,tag='W1');p.win(13.5,12,2,tag='V1');p.win(32,4,4,True,'W1')
    elif slug=='charcoal-two-bedroom-home-24x32':
        for x in (0,16):p.box(x,12,16,12,'#D9DADB')
        p.bath(0,18,5,6);p.bath(27,18,5,6,door='west');p.cupboard(0,12,2,6);p.cupboard(30,12,2,6)
        p.bed(8,17.5,5,6.5,'north',(0,12,16,12));p.bed(19,17.5,5,6.5,'north',(16,12,16,12))
        p.label(9,14.5,'BEDROOM 1 / 16 x 12 ft',6.2);p.label(23,14.5,'BEDROOM 2 / 16 x 12 ft',6.2)
        p.door(12,12,3,tag='D2');p.door(17,12,3,tag='D2')
        kitchen(p,24,0,8,12,side='right');p.line(24,0,24,12,'#F1F0EC',3)
        furniture(p,3,9,8,2,'SOFA');cafe_table(p,19,7,True);p.label(11,5.5,'LIVING / DINING',7)
        p.door(14,0,4,tag='D1');p.win(3,0,6,tag='W2');p.win(25,0,6,tag='W2')
        p.win(0,13,4,True,'W1');p.win(32,13,4,True,'W1');p.win(1.5,24,2,tag='V1');p.win(28.5,24,2,tag='V1')
    elif slug=='ivory-portable-clinic-12x40':
        p.box(0,0,10,12,'#DFE5E4');p.label(5,6.7,'CONSULTATION',6)
        office_desk(p,2,8);furniture(p,1,1,6,2.5,'EXAM');furniture(p,8,9,2,2,'SINK')
        kitchen(p,10,0,6,6);p.bath(10,6,6,6);p.door(16,.5,2.5,True,'D2',-1)
        p.door(10,3,3,True,'D2',-1);p.label(22,7,'WAITING / RECEPTION',6.3)
        furniture(p,23,9,4,2,'RECEPTION');furniture(p,18,9,4,2,'SEATS')
        p.box(28,0,12,12,'#DFE5E4');p.door(28,1,3,True,'D2');p.label(34,7,'TREATMENT',6.3)
        furniture(p,30,8,6,2.5,'COUCH');office_desk(p,34,2);furniture(p,38,9,2,2,'SINK')
        p.door(18,0,4,tag='D1');p.win(2,12,6,tag='F1');p.win(11,12,2,tag='V1')
        p.win(11,0,4,tag='W1');p.win(22,0,4,tag='W1');p.win(31,12,6,tag='F1')
    else:
        kitchen(p,0,0,6,6);p.bath(0,6,6,6);p.door(6,.5,2.5,True,'D2',-1)
        p.box(6,0,6,12,'#E2DED4');p.label(9,8,'STORE\n6 x 12 ft',6.5);furniture(p,6,10,6,2,'SHELVES')
        p.door(12,1,3,True,'D2',-1);p.label(25,6.3,'CLASSROOM / 12 SEATS',6.5)
        for y,xs in [(2,(14,23,26,29,32,35)),(8,(14,18,22,26,30,34))]:
            for x in xs:furniture(p,x,y,2,1.5,'DESK');furniture(p,x+.6,y+1.7,.7,.7)
        furniture(p,38,3,2,6,'BOARD');p.door(40,9,3,True,'D5',-1)
        p.door(18,0,4,tag='D1');p.win(1,0,4,tag='W1');p.win(1,12,2,tag='V1')
        for x in (13,23,32):p.win(x,12,6,tag='W2')
        for x in (24,32):p.win(x,0,6,tag='W2')
    p.dimensions()
    txt(c,40,147,'ROOMS / NOMINAL DIMENSIONS',7,base.RED,'Helvetica-Bold')
    text=' | '.join(a+': '+b.split(';')[0] for a,b in cfg['rooms'])
    wrap(c,text,40,129,755,8,leading=11)
    txt(c,40,65,'Front / main entrance is at the bottom of plan. A separate opening schedule follows.',7,base.MUTED)
    return p

def panel(c,cfg,index,x,y,w,h):
    path=ASSETS/(cfg['slug']+'.png');im=Image.open(path);iw,ih=im.size
    pw,ph=iw/2,ih/2;left=(index%2)*pw+3;top=(index//2)*ph+3;rw,rh=pw-6,ph-6
    scale=min(w/rw,h/rh);dx=x+(w-rw*scale)/2;dy=y+(h-rh*scale)/2
    c.saveState();clip=c.beginPath();clip.rect(dx,dy,rw*scale,rh*scale);c.clipPath(clip,stroke=0,fill=0)
    c.drawImage(str(path),dx-left*scale,dy-(ih-top-rh)*scale,iw*scale,ih*scale);c.restoreState()

def author(cfg):
    buf=BytesIO();c=canvas.Canvas(buf,pagesize=(W,H),pageCompression=1);total=13
    def page(n,section,title=None,sub=None):frame(c,cfg,section,n,total,title,sub)
    page(1,'Design collection / '+cfg['category'])
    title=cfg['title'].split();lines=[];line=''
    for word in title:
        if c.stringWidth((line+' '+word).strip(),'Times-Roman',29)>245:lines.append(line);line=word
        else:line=(line+' '+word).strip()
    lines.append(line)
    for j,line in enumerate(lines):txt(c,40,470-j*33,line,29,base.INK,'Times-Roman')
    wrap(c,cfg['description'],40,345,240,10,base.MUTED)
    txt(c,40,207,cfg['dims'],23,base.INK,'Times-Roman');txt(c,40,182,f"{cfg['area']} sq ft enclosed / single storey",8)
    txt(c,40,139,'MEASURED PLAN / FOUR EXTERIOR VIEWS',7,base.RED,'Helvetica-Bold')
    panel(c,cfg,0,319,171,483,280);c.showPage()
    page(2,'01 / ground floor',cfg['dims']+'. Planned for daily use.','Nominal feet before wall deductions. Furniture, door swings and opening tags are shown.')
    p=floor_plan(c,cfg);c.showPage()
    page(3,'02 / rooms & circulation','A place for every function.','Room sizes reconcile with the external footprint. Service rooms are included in their parent zones.')
    table(c,cfg['rooms']+[('Footprint',f"{cfg['L']} x {cfg['B']} ft = {cfg['area']} sq ft gross enclosed area."),('Entry / circulation','Main entry, service doors, partitions and furniture positions follow the dimensioned plan.'),('Finish direction',cfg['palette'])],40,402,rowh=44,size=9)
    if cfg['bedrooms']:wrap(c,'Sleeping furniture: double beds 5 x 6.5 ft, headboards against solid walls, minimum 2.5 ft bedside and foot access. Wardrobes are 2 ft deep.',40,91,750,8,base.MUTED)
    c.showPage()
    page(4,'03 / doors & windows','Every opening. Clearly scheduled.','Window and hatch sizes are width x height. Tags correspond to the floor plan; front is the bottom edge.')
    rows=[]
    descriptions={'D1':'Main entrance','D2':'Internal / staff door','D3':'Washroom door','D4':'Glazed executive door','D5':'Service / secondary exterior exit'}
    for tag in sorted({d['tag'] for d in p.doors}):
        doors=[d for d in p.doors if d['tag']==tag];sizes=sorted({d['size'] for d in doors})
        rows.append((tag+' / '+descriptions.get(tag,'Door'),', '.join(f'{v:g} ft wide' for v in sizes)+' x 7 ft high; '+str(len(doors))+' opening(s).'))
    for tag in sorted({d['tag'] for d in p.windows}):
        windows=[d for d in p.windows if d['tag']==tag];widths=sorted({d['size'] for d in windows})
        height=1.5 if tag=='V1' else 3 if tag.startswith('S') else 4
        title='Serving hatch' if tag.startswith('S') else 'Frosted privacy glazing' if tag=='F1' else 'High-level washroom vent' if tag=='V1' else 'Window'
        rows.append((tag+' / '+title,', '.join(f'{v:g} ft' for v in widths)+f' wide x {height:g} ft high; {len(windows)} opening(s).'))
    table(c,rows,40,403,rowh=30,size=8)
    wrap(c,'Glazing and door hardware, sill levels, safety glass, ventilation and clear openings require final coordination. Food-service fit-out and hygiene finishes follow the selected equipment and operating requirements.',40,91,750,8,base.MUTED);c.showPage()
    for k in range(2):
        page(5+k,'04 / exterior design','The same space. Four perspectives.','Photorealistic architectural concepts; floor plans and opening schedules control the design.')
        for j in range(2):
            x=40+j*390;panel(c,cfg,2*k+j,x,185,372,235)
            txt(c,x,168,['FRONT / ENTRY','REAR / SERVICE','LEFT / END','RIGHT / END'][2*k+j],8,base.RED,'Helvetica-Bold')
            txt(c,x,152,cfg['finish'],7,base.MUTED)
        wrap(c,'Exterior concepts illustrate finish and atmosphere. Openings and furniture are governed by the measured plan; generated views can contain small visual differences.',40,109,750,8,base.MUTED);c.showPage()
    page(7,'05 / materials & programme','A coordinated specification.','The complete material standards follow on the next five pages.')
    table(c,[('Building',cfg['title']+' / '+cfg['dims']),('Gross floor area',str(cfg['area'])+' sq ft before wall deductions.'),('Exterior finish',cfg['palette']),('Steel structure','Joined or fabricated modules; connections, supports and lifting points engineered for the selected site.'),('Roof / enclosure','Insulated roof and wall build-up, weatherproof flashings and coordinated rainwater discharge.'),('Interior / wet areas','Washable wall linings, durable flooring and slip-resistant wet-area surfaces.'),('Services','Lighting, sockets, ventilation, water supply and drainage coordinated with the site.'),('Installation','Transport, crane access, supports, anchoring and service connections agreed before fabrication.')],40,401,rowh=36,size=8)
    wrap(c,'Concept proposal for discussion. Final wall thicknesses, structure, fire strategy, access and equipment are confirmed in project-specific drawings and quotation.',40,83,750,8,base.MUTED);c.showPage();c.save()
    writer=PdfWriter();writer.append(PdfReader(BytesIO(buf.getvalue())))
    for source_index in [5,6,7,8,9,10]:
        source=base.REF.pages[source_index];overlay=BytesIO();oc=canvas.Canvas(overlay,pagesize=(W,H));border(oc,cfg)
        rect(oc,707,538,91,30,'#FAF9F6','#FAF9F6');txt(oc,718,559,cfg['code']+' / 04',8,base.INK,'Helvetica-Bold')
        txt(oc,718,544,'OCTOBER 2026',6.5,base.MUTED);rect(oc,742,22,59,15,'#FAF9F6','#FAF9F6')
        txt(oc,775,29,f'{len(writer.pages)+1:02d} / {total:02d}',6);oc.save()
        writer.add_page(source);writer.pages[-1].merge_page(PdfReader(BytesIO(overlay.getvalue())).pages[0])
    assert len(writer.pages)==total
    writer.add_metadata({'/Title':cfg['title']+' '+cfg['dims'],'/Author':'Zaka Engineering Containers & Prefab','/Subject':'Floor plan, room schedule, opening sizes, exterior concepts and material standards'})
    path=OUT/cfg['file'];writer.write(path);add_watermark(path,path)
    return path,p

def previews(path,slug):
    doc=pdfium.PdfDocument(str(path));cover=doc[0].render(scale=1.3).to_pil();cover.save(PREVIEW/(slug+'.webp'),quality=86)
    thumbs=[]
    for i in range(len(doc)):
        img=doc[i].render(scale=1).to_pil();img.save(QA/(slug+f'-{i+1:02d}.png'))
        img.thumbnail((421,298));thumbs.append(img)
    sheet=Image.new('RGB',(1263,((len(thumbs)+2)//3)*322),'#D7D9D8');draw=ImageDraw.Draw(sheet)
    for i,img in enumerate(thumbs):
        x,y=i%3*421,i//3*322;sheet.paste(img,(x,y+20));draw.text((x+9,y+4),str(i+1),fill='#17283B')
    sheet.save(QA/(slug+'-review.png'));doc.close()

def main():
    only=set(sys.argv[1:])
    PREVIEW.mkdir(parents=True,exist_ok=True);QA.mkdir(parents=True,exist_ok=True);AUDIT.clear()
    data_path=ROOT/'src/data/documents.json';docs=json.loads(data_path.read_text(encoding='utf-8'));docs_by_slug={d['slug']:d for d in docs}
    plans={}
    for i,raw in enumerate(NEW):
        if only and raw['slug'] not in only:continue
        cfg=configure(raw,i);path,plan=author(cfg);previews(path,cfg['slug'])
        docs_by_slug[cfg['slug']]=dict(slug=cfg['slug'],code=cfg['code'],title=cfg['title'],subtitle=f"{cfg['B']}′ × {cfg['L']}′ / {cfg['area']} sq ft enclosed",description=cfg['description'],pages=13,revision=REVISION,file='/downloads/'+path.name,image='/images/pdf/collection-30/'+cfg['slug']+'.webp',preview='/images/pdf/collection-30/'+cfg['slug']+'.webp',category=cfg['category'],storeys=1,bedrooms=cfg['bedrooms'],designStyle=cfg['finish'])
        plans[cfg['slug']]=dict(lengthFeet=cfg['L'],widthFeet=cfg['B'],areaSqFt=cfg['area'],rooms=cfg['rooms'],windows=plan.windows,doors=plan.doors,bedFurniture=plan.beds)
        print('Created',path.name,flush=True)
    # Make the four previously unlisted, fully revised catalogues visible too.
    for i,cfg in enumerate(base.CONFIGS):
        slug=['family-home-two-floors-40x24','two-bedroom-living-12x40-and-12x44','executive-office-suite-12x40-and-12x44','studio-with-terrace-12x26'][i]
        path=OUT/filename(cfg['file'])
        if not only:previews(path,slug)
        docs_by_slug[slug]=dict(slug=slug,code=f'ZE-{18+i:02d}',title=cfg['title'].replace('\n',' '),subtitle=cfg['dims']+' / '+cfg['area'],description=cfg['desc'],pages=len(PdfReader(path).pages),revision=REVISION,file='/downloads/'+path.name,image='/images/pdf/collection-30/'+slug+'.webp',preview='/images/pdf/collection-30/'+slug+'.webp',category='Workspace' if cfg['type']=='office' else 'Living',storeys=2 if cfg['type']=='duplex' else 1,bedrooms=[4,2,1,0][i],designStyle=cfg['finish'])
    docs=sorted(docs_by_slug.values(),key=lambda d:int(d['code'].split('-')[1]))
    assert len(docs)==30,len(docs)
    for d in docs:d['file']='/downloads/'+filename(Path(d['file']).name)
    assert len({d['file'] for d in docs})==30
    data_path.write_text(json.dumps(docs,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    previous=json.loads((OUT/'catalogue-manifest.json').read_text(encoding='utf-8'));previous={p['file']:p for p in previous}
    manifest=[]
    for d in docs:
        name=Path(d['file']).name;path=OUT/name;reader=PdfReader(path)
        assert len(reader.pages)==d['pages']
        assert not name.startswith('zaka-') and 'client-' not in name
        for page in reader.pages:assert page.get('/ZakaLogoWatermark')==LABEL
        shutil.copy2(path,ROOT/'public/downloads'/name)
        manifest.append({**previous.get(name,{}),**plans.get(d['slug'],{}),'file':name,'slug':d['slug'],'pages':len(reader.pages),'bytes':path.stat().st_size,'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'websiteCopyMatches':True,'watermark':LABEL,'revision':REVISION})
    assert len(list(OUT.glob('*.pdf')))==30
    assert len(list((ROOT/'public/downloads').glob('*.pdf')))==30
    (OUT/'catalogue-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
    (OUT/'collection-review.json').write_text(json.dumps([dict(slug=d['slug'],file=d['file'],pages=d['pages'],sha256=d['sha256'],websiteCopyMatches=True) for d in manifest],indent=2)+'\n',encoding='utf-8')
    audit_path=OUT/'collection-30-bed-audit.json'
    old_audit=json.loads(audit_path.read_text(encoding='utf-8')) if only and audit_path.exists() else []
    revised_files={entry['file'] for entry in manifest if entry['slug'] in plans}
    old_audit=[entry for entry in old_audit if entry['context'].split(' / ')[0] not in revised_files]
    audit_path.write_text(json.dumps(old_audit+AUDIT,indent=2)+'\n',encoding='utf-8')
    (OUT/'watermark-manifest.json').write_text(json.dumps([{k:d[k] for k in ('file','pages','bytes','sha256','websiteCopyMatches','watermark')} for d in manifest],indent=2)+'\n',encoding='utf-8')
    print('Verified 30 unique PDFs on website;',sum(d['pages'] for d in docs),'pages.',flush=True)

if __name__=='__main__':main()
