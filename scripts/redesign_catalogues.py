"""Revision 02: seventeen distinct designs, explicit floor geometry and exterior sets."""
from catalogue_style import *
from create_collection import panel_bounds
from watermark_catalogues import add_watermark
from client_floor_plans import REVISIONS, draw_plan
from client_materials import MATERIAL_PAGES, draw_materials
import hashlib

DESIGNS=json.loads((ROOT/'scripts/catalogue_redesigns.json').read_text())
ASSETS=ROOT/'public/images/catalogues/revision-02'
PREVIEW=ROOT/'public/images/pdf/revision-03';PREVIEW.mkdir(parents=True,exist_ok=True)
QA=ROOT/'tmp/pdfs/revision-03';QA.mkdir(parents=True,exist_ok=True)

def room(name,x,y,l,w,kind='living'):
    return dict(name=name,x=x,y=y,length=l,width=w,kind=kind)

def service(d,upper=False):
    w=d['width']
    if d['category']=='Workspace':
        return [room('Washroom',0,w-4,6,4,'bath'),room('Kitchen' if d['slug']=='office-10x20' else 'Entry / pantry',0,0,6,w-4,'kitchen')]
    return [room('Bathroom',0,6,6,w-6,'bath'),room('Landing' if upper else 'Kitchenette',0,0,6,6,'landing' if upper else 'kitchen')]

def rooms_for(d):
    l,w=d['length'],d['width'];slug=d['slug']
    if slug=='compact-container-home':
        return [[room('Bedroom 1',0,0,10,12,'bed'),room('Bedroom 2',0,12,10,12,'bed'),room('Living / dining',10,12,20,12),room('Bedroom 3',30,0,10,12,'bed'),room('Kitchen',30,12,5,12,'kitchen'),room('Bathroom',35,12,5,12,'bath')]]
    if slug=='two-cabin-office':
        return [[room('Private office 1',0,0,7,8,'office'),room('Entrance',7,0,6,4,'landing'),room('Washroom',7,4,6,4,'bath'),room('Private office 2',13,0,7,8,'office')]]
    if slug=='single-cabin-office':
        return [[room('Entrance',0,0,4,4,'landing'),room('Washroom',0,4,4,4,'bath'),room('Private office',4,0,16,8,'office')]]
    if slug=='industrial-field-office':
        return [[room('Review / briefing',0,0,12,8,'office'),room('Comms / desk',12,0,4,8,'office'),room('Equipment / pantry',16,0,4,8,'kitchen')]]
    if d['category']=='Workspace':
        floors=[service(d)+[room('Team workspace',6,0,l-6,w,'office')]]
        if d['storeys']==2:
            end=14 if w==10 else 12
            floors.append([room('Stair landing',0,0,6,3,'landing'),room('Washroom',0,w-4,6,4,'bath'),room('Pantry',0,3,6,w-7,'kitchen'),room('Meeting / studio',6,3,l-6-end,w-3,'office'),room('Private office',l-end,3,end,w-3,'office'),room('Shared corridor',6,0,l-6,3,'hall')])
        return floors
    b=d['bedrooms']
    if d['storeys']==2:
        return [service(d)+[room('Living / dining',6,0,23,w),room('Bedroom 1',29,3,16,w-3,'bed'),room('Bedroom access',29,0,16,3,'hall')],service(d,True)+[room('Bedroom 2',6,3,16,w-3,'bed'),room('Bedroom 3',22,3,23,w-3,'bed'),room('Shared corridor',6,0,39,3,'hall')]]
    if b==0:return [service(d)+[room('Open studio',6,0,l-6,w,'studio')]]
    bedlength=12 if slug in ('studio-12x30','two-bedroom-residence') else 10
    living=l-6-b*bedlength
    rs=service(d)+[room('Living / dining',6,0,living,w)]
    for i in range(b):rs.append(room(f'Bedroom {i+1}',6+living+i*bedlength,3,bedlength,w-3,'bed'))
    rs.append(room('Bedroom corridor',6+living,0,b*bedlength,3,'hall'))
    return [rs]

def enrich(d):
    d={**d,**REVISIONS.get(d['slug'],{}).get('changes',{})}
    d['revision']='03';d['floors']=[f['rooms'] for f in REVISIONS[d['slug']]['floors']] if d['slug'] in REVISIONS else rooms_for(d)
    d['basePages']=7 if d['storeys']==2 or d['roofTerrace'] else 6
    d['pages']=d['basePages']+MATERIAL_PAGES;d['briefPage']=d['basePages']-1
    d['floorArea']=sum(r['length']*r['width'] for r in d['floors'][0]);d['area']=d['floorArea']*d['storeys'];d['type']='redesign'
    assert d['floorArea']==(720 if d['slug']=='compact-container-home' else d['width']*d['length'])
    for floor in d['floors']:
        assert sum(r['length']*r['width'] for r in floor)==d['floorArea']
        for i,r in enumerate(floor):
            assert r['x']>=0 and r['y']>=0 and r['x']+r['length']<=d['length'] and r['y']+r['width']<=d['width']
            for t in floor[i+1:]:assert min(r['x']+r['length'],t['x']+t['length'])<=max(r['x'],t['x']) or min(r['y']+r['width'],t['y']+t['width'])<=max(r['y'],t['y'])
    program=f"{d['bedrooms']}-bedroom home" if d['bedrooms'] else ('open studio' if d['category']=='Living' else 'portable office')
    d['subtitle']=f"{d['storeys']}-storey {program} / {d['area']} sq ft enclosed"
    article='An' if d['width']==8 else 'A'
    d['description']=f"{article} {d['width']} x {d['length']} ft {program} with {d['finish']}."
    if d['storeys']==2:d['description']+=' Kitchen and washroom on both floors; right-end stairs connect to the upper front access balcony.'
    if d['terrace']:d['description']+=' An additional 12 x 5 ft terrace extends from the right end.'
    if d['roofTerrace']:d['description']+=' A 12 x 24 ft roof deck adds an outdoor lounge above the enclosed floor.'
    if d['slug']=='compact-container-home':d['description']+=' A 20 x 12 ft open courtyard connects the three bedrooms and living wing via outdoor access.'
    d['inspiration']='Architecture direction informed by client-assets references, then developed as an original concept. All measurements are nominal feet; wall thicknesses are not deducted. Wider modules require fabricated or joined frames.'
    if d['storeys']==2:d['inspiration']+=' Right-end external stairs: 4 x 16 ft, plus a 3 ft deep upper front access balcony, both outside the enclosed footprint. Final stair geometry, structure and clearances require detailed design.'
    return d

def panel(c,d,index,x,y,w,h):
    source=ROOT/'public'/d['image'].lstrip('/');im=Image.open(source).convert('RGB');iw,ih=im.size
    jpeg=QA/(d['slug']+'.jpg');im.save(jpeg,quality=92,optimize=True)
    lx,ty,rx,by=panel_bounds(im,d['slug'])[index];s=min(w/(rx-lx),h/(by-ty));pw,ph=(rx-lx)*s,(by-ty)*s;left=x+(w-pw)/2;bottom=y+(h-ph)/2
    c.saveState();clip=c.beginPath();clip.rect(left,bottom,pw,ph);c.clipPath(clip,stroke=0,fill=0);c.drawImage(str(jpeg),left-lx*s,bottom-(ih-by)*s,width=iw*s,height=ih*s);c.restoreState()

def cover(c,d):
    header(c,d,1,'Revision 03 / '+d['category'])
    text(c,40,479,'INDIVIDUAL DESIGN / '+d['code'],8,'Bold',RED)
    titlebottom=para(c,40,456,d['title'],245,28,NAVY,32,'Display')
    para(c,40,titlebottom-14,d['subtitle'],242,11,RED,16,'Bold')
    para(c,40,316,d['description'],240,9,MUTED,14)
    line(c,40,169,277,169);text(c,40,143,f"{d['width']}' x {d['length']}'",24,'Display')
    text(c,40,124,f"{d['area']} SQ FT ENCLOSED / {d['storeys']} STOREY",8,'Bold',MUTED)
    text(c,40,103,'FLOOR PLANS + FOUR EXTERIOR VIEWS',7.5,'Bold',RED)
    rect(c,303,110,497,374,SAND);panel(c,d,0,310,165,483,298)
    rect(c,303,110,497,38,NAVY);text(c,320,125,'ORIGINAL EXTERIOR CONCEPT / CLIENT REFERENCE INSPIRED',7,'Body',PAPER)
    text(c,303,85,'ISLAMABAD / DESIGN COLLECTION 2026',8,'Bold',RED);c.showPage()

def plan(c,d,index,page,roof=False):
    name='Roof terrace' if roof else ('Ground floor' if index==0 else 'Upper floor')
    header(c,d,page,name+' / measurements in feet')
    heading(c,'01 / Measured space',name+'. A distinct layout.','Nominal dimensions in feet. Floor-zone areas exclude wall deductions; furniture and openings are schematic.')
    l,w=d['length'],d['width'];total=l+d['terrace'];stairs=d['storeys']==2 or d['roofTerrace'];s=min(625/total,(140 if stairs else 185)/w);x=(W-total*s)/2;y=185
    palette={'bed':'#e4dacb','bath':'#dce8eb','kitchen':'#ece2d2','office':'#e0e6de','hall':'#faf9f6','landing':'#f0ece4','studio':'#e9dfd0','living':'#efede7'}
    def bx(a,b,ll,ww,fill,stroke=NAVY):rect(c,x+a*s,y+b*s,ll*s,ww*s,HexColor(fill),stroke)
    def door(a,b,vertical=False,size=2.5):
        xx,yy=x+a*s,y+b*s
        line(c,xx,yy,xx+(0 if vertical else size*s),yy+(size*s if vertical else 0),PAPER,3)
        line(c,xx,yy,xx+size*s,yy+(0 if vertical else size*s),RED,.65)
        c.setStrokeColor(RED);c.setLineWidth(.5);c.arc(xx-size*s,yy-size*s,xx+size*s,yy+size*s,0,90)
    rs=[room('Roof lounge',0,0,l,w,'living')] if roof else d['floors'][index]
    if d['slug']=='compact-container-home':
        bx(10,0,20,12,'#dedaca',None);text(c,x+12*s,y+5*s,'OPEN COURTYARD',9,'Bold',RED)
        text(c,x+12*s,y+5*s-13,"20' x 12' / 240 sq ft",8)
    for r in rs:bx(r['x'],r['y'],r['length'],r['width'],palette[r['kind']])
    for i,r in enumerate(rs):
        a,b,ll,ww=r['x'],r['y'],r['length'],r['width'];kind=r['kind']
        if kind in ('bed','studio') and ll>=7 and ww>=8:
            bx(a+ll-5.7,b+ww-6.7,5,6,'#cabba7',MUTED);bx(a+ll-5.5,b+ww-1.7,4.6,.8,'#faf9f6',MUTED)
        elif kind=='office':
            for xx in range(1,int(ll)-3,7):bx(a+xx,b+ww-2.2,3.5,1.5,'#cabba7',MUTED)
        elif kind=='kitchen':bx(a+.4,b+.4,1.5,max(1,ww-.8),'#cabba7',MUTED)
        elif kind=='living' and not roof:
            bx(a+1,b+ww-2.6,min(5,ll-2),2,'#cabba7',MUTED)
            if ll>=10:bx(a+ll-4,b+2,2.5,3,'#e4dacb',MUTED)
        elif kind=='bath':
            c.setFillColor(PAPER);c.setStrokeColor(MUTED);c.ellipse(x+(a+.6)*s,y+(b+.6)*s,x+(a+1.7)*s,y+(b+2.2)*s,fill=1,stroke=1)
        if kind not in ('hall','landing','bath','kitchen') and ll>=8 and ww>=7:
            label=r['name'] if ll*s>115 else f"ZONE {i+1:02d}"
            tw=pdfmetrics.stringWidth(label,'Bold',8);rect(c,x+(a+ll*.4)*s-tw/2-3,y+(b+ww*.4)*s-4,tw+6,15,PAPER);text(c,x+(a+ll*.4)*s-tw/2,y+(b+ww*.4)*s,label,8,'Bold')
        # Zone index connects the compact plan to the precise dimension schedule.
        rect(c,x+(a+.2)*s,y+(b+ww)*s-13,11,10,NAVY)
        text(c,x+(a+.2)*s+3,y+(b+ww)*s-10,str(i+1),7,'Bold',PAPER)
        if kind=='bed':
            if d['slug']=='compact-container-home':door(a+ll,b+1,True) if a==0 else door(a,b+1,True)
            else:door(a+.7,b,False)
        if kind=='bath':
            if d['slug']=='two-cabin-office' or index==1:door(a+.7,b)
            elif d['slug']=='compact-container-home':door(a,b+3,True)
            else:door(a+ll,b+.3,True)
        if kind in ('kitchen','landing') and d['slug'] not in ('industrial-field-office','compact-container-home'):
            door(a+ll,b+.3,True,min(2.5,ww-.6))
        if kind=='hall':door(a,b+.2,True,2.5)
        if d['slug']=='compact-container-home' and kind=='kitchen':door(a,b+3,True)
        if kind=='office' and index==1:door(a+.7,b)
        if kind=='office' and d['slug'] in ('two-cabin-office','industrial-field-office'):
            if a>0:door(a,b+.3,True)
            elif d['slug']=='two-cabin-office':door(a+ll,b+.3,True)
    if roof:
        for xx in range(2,int(l)-3,4):bx(xx,1.5,2.5,1.4,'#cabba7',MUTED)
        text(c,x+1*s,y+(w-1)*s,'GUARDING TO ALL OPEN EDGES',7,'Bold',RED)
    elif d['slug']=='compact-container-home':door(18,12,False,3)
    elif index==0:door(8 if d['slug']!='two-cabin-office' else 8.5,0,False,3)
    else:door(0,.3,True)
    # Windows shown on exposed facades; individual openings are schematic.
    if not roof:
        for r in rs:
            if r['kind'] not in ('bed','office','studio','living'):continue
            if r['y']+r['width']==w:line(c,x+(r['x']+1)*s,y+w*s,x+(r['x']+min(r['length']-1,4))*s,y+w*s,HexColor('#57879a'),3)
    if d['terrace']:
        bx(l,0,5,w,'#dedaca');text(c,x+(l+.7)*s,y+5*s,'TERRACE',7,'Bold');dim(c,x+l*s,y+w*s+18,x+total*s,y+w*s+18,"5' terrace")
    if stairs:
        bx(0,w+.3,16,4,'#e0e6de',MUTED)
        for t in range(1,16):line(c,x+t*s,y+(w+.3)*s,x+t*s,y+(w+4.3)*s,MUTED,.5)
        text(c,x+3*s,y+(w+1.8)*s,'EXTERNAL STAIR',6,'Bold',RED)
        dim(c,x,y+(w+4.3)*s+12,x+16*s,y+(w+4.3)*s+12,"16' stair allowance")
        dim(c,x-15,y+(w+.3)*s,x-15,y+(w+4.3)*s,"4'")
        dim(c,x,y-16,x+l*s,y-16,f"{l}' building length")
    else:dim(c,x,y+w*s+38,x+l*s,y+w*s+38,f"{l}' building length")
    dim(c,x-23,y,x-23,y+w*s,f"{w}' building width")
    if d['storeys']==2 or d['roofTerrace']:
        para(c,40,158,"EXTERNAL STAIR: 4' x 16' ALLOWANCE OUTSIDE FOOTPRINT. Arrival at left-end landing; final rise, run and support design by engineer.",W-80,7,RED,10)
    text(c,40,138,'ZONE SCHEDULE / DIMENSIONS IN FEET',8,'Bold',RED)
    for i,r in enumerate(rs):
        xx=40+(i%3)*257;yy=117-(i//3)*27
        text(c,xx,yy,f"{i+1:02d}  {r['name']}",8,'Bold')
        text(c,xx,yy-12,f"{r['length']}' x {r['width']}' / {r['length']*r['width']} sq ft",8,'Body',MUTED)
    note='Blue: glazing / Red: indicative doors. Coordinate room access and opening positions in the detailed design.'
    if d['slug']=='compact-container-home':note='Courtyard access serves the front bedrooms; rear bedroom connects to living. Courtyard is open air and excluded from enclosed area.'
    if roof:note='Roof deck: 288 sq ft additional outdoor area. Deck loads, waterproofing, guarding and stair access require engineered design.'
    if d['terrace']:note+=' Terrace: 60 sq ft additional; overall ground footprint 12 x 26 ft.'
    para(c,40,66,note,W-80,7,MUTED,9);c.showPage()

def elevations(c,d,page,panels):
    header(c,d,page,'Four side exterior / '+('front and rear' if panels[0]==0 else 'left and right'))
    heading(c,'02 / Exterior design','The same design. Every side.','Four original visualizations illustrate this individual concept. Openings and construction details remain schematic.')
    labels=['FRONT / ENTRY FACADE','REAR / SERVICE FACADE','LEFT / END VIEW','RIGHT / END VIEW']
    for i,p in enumerate(panels):
        xx=40+i*395;rect(c,xx,156,366,245,SAND);panel(c,d,p,xx+5,160,356,235)
        text(c,xx,135,labels[p],9,'Bold',RED)
        text(c,xx,115,f"{d['length'] if p<2 else d['width']}' nominal span / {d['storeys']} enclosed storey",9)
    para(c,40,93,'FINISH DIRECTION: '+d['finish'].capitalize()+'.',W-80,9,MUTED,13)
    para(c,40,65,'Images depict a concept finish. Exact window locations, heights, stairs and roof assemblies are coordinated with the measured layout before fabrication.',W-80,7,MUTED,9);c.showPage()

def specifications(c,d):
    # Individual finish and programme above the standard construction schedule.
    header(c,d,d['briefPage'],'Individual specification brief')
    heading(c,'03 / Materials & programme','Details for this design.','A defined visual direction and spatial brief for the project quotation.')
    rows=[('Building',f"{d['width']} x {d['length']} ft footprint; {d['storeys']} enclosed storey(s); {d['bedrooms']} bedroom(s)."),('Enclosed floor area',f"{d['floorArea']} sq ft per floor / {d['area']} sq ft total, before wall deductions."),('Exterior palette',d['finish'].capitalize()+'.'),('Roof & outdoor space','Guarded 12 x 24 ft accessible roof deck; stairs outside footprint.' if d['roofTerrace'] else ('Additional 12 x 5 ft terrace / 60 sq ft.' if d['terrace'] else ('20 x 12 ft open courtyard / 240 sq ft excluded from floor area.' if d['slug']=='compact-container-home' else 'Roof profile follows the exterior concept; structure and drainage to be designed.'))),('Structure','Fabricated or joined steel modules; foundation, openings, connections and lifting points engineered for site conditions.'),('Comfort & finish','Insulated walls and roof; selected internal linings and floor finish; washable wet-area surfaces.'),('Glazing & doors','Opening schedule coordinated with rooms, privacy, escape and ventilation; safety glass and hardware specified individually.'),('Electrical & services','Power, lighting, sockets and data developed to suit use. Plumbing, water supply and drainage coordinated with available site services.'),('Circulation & access','External stair allowance 4 x 16 ft; final rise, run, landing and support design required.' if d['storeys']==2 else 'Door swings and furniture are indicative; confirm finished clearances and accessible circulation.'),('Delivery & installation','Transport route, crane access, supports, anchoring and connections agreed before manufacture.')]
    yy=380
    for i,(label,value) in enumerate(rows):
        if label=='Circulation & access' and d['storeys']==2:value="Right-end stair: 4 x 16 ft. Upper front access balcony: 3 ft deep, outside enclosed footprint. Final stair geometry to be engineered."
        rh=29;rect(c,40,yy-rh,W-80,rh,SAND if i%2==0 else PAPER);text(c,51,yy-18,label,8,'Bold');para(c,222,yy-5,value,560,8,MUTED,10);yy-=rh
    para(c,40,72,'Concept proposal only. Final engineering, quantities, approvals and price are established for the selected design and site.',W-80,7,MUTED,9);c.showPage()

def main():
    manifest=[];site=[]
    for raw in DESIGNS:
        d=enrich(raw);path=OUT/('zaka-'+d['slug']+'.pdf')
        revision='03' if (ROOT/'public/images/catalogues/revision-03'/(d['slug']+'.webp')).exists() else '02'
        d['image']='/images/catalogues/revision-'+revision+'/'+d['slug']+'.webp'
        c=canvas.Canvas(str(path),pagesize=(W,H),pageCompression=1);cover(c,d);draw_plan(c,d,0,2)
        if d['storeys']==2:draw_plan(c,d,1,3)
        elif d['roofTerrace']:plan(c,d,0,3,True)
        start=d['basePages']-3;elevations(c,d,start,[0,1]);elevations(c,d,start+1,[2,3]);specifications(c,d);draw_materials(c,d,d['briefPage']+1);planning_page(c,d);c.save()
        watermark=add_watermark(path,path);doc=pymupdf.open(path);assert len(doc)==d['pages']
        for j,p in enumerate(doc):
            pix=p.get_pixmap(matrix=pymupdf.Matrix(1.25,1.25),alpha=False);pix.save(str(QA/f"{d['slug']}-{j+1}.png"))
            if j==0:Image.frombytes('RGB',[pix.width,pix.height],pix.samples).save(PREVIEW/(d['slug']+'.webp'),quality=90)
        sheet=Image.new('RGB',(1800,math.ceil(len(doc)/3)*240),'#deded9');draw=ImageDraw.Draw(sheet)
        for j in range(len(doc)):
            im=ImageOps.contain(Image.open(QA/f"{d['slug']}-{j+1}.png"),(590,209));xx=(j%3)*600;yy=(j//3)*240;sheet.paste(im,(xx,yy+22));draw.text((xx+5,yy+4),f"{d['slug']} / {j+1}",fill='black')
        sheet.save(QA/(d['slug']+'-review.jpg'))
        manifest.append({**watermark,'slug':d['slug'],'revision':'03','widthFeet':d['width'],'lengthFeet':d['length'],'storeys':d['storeys'],'bedrooms':d['bedrooms'],'areaSqFt':d['area'],'reference':d['reference'],'imageSha256':hashlib.sha256((ROOT/'public'/d['image'].lstrip('/')).read_bytes()).hexdigest(),'floorZones':d['floors'],'materialSpecificationSections':20})
        subtitle=f"{d['width']}′ × {d['length']}′ / {d['area']} sq ft enclosed"
        if d['terrace']:subtitle+=' + 60 sq ft terrace'
        if d['roofTerrace']:subtitle+=' + roof deck'
        site.append(dict(slug=d['slug'],code=d['code'],title=d['title'],subtitle=subtitle,description=d['description'],pages=d['pages'],revision='03',file='/downloads/'+path.name,image=d['image'],preview='/images/pdf/revision-03/'+d['slug']+'.webp',category=d['category'],storeys=d['storeys'],bedrooms=d['bedrooms'],designStyle=d['finish']))
        print(path.name,d['pages'],'pages',flush=True)
    (OUT/'catalogue-manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf8')
    review=[{k:d[k] for k in ('slug','pages','areaSqFt','imageSha256','websiteCopyMatches')}|{'roomGeometryValidated':True} for d in manifest]
    stamps=[{k:d[k] for k in ('file','pages','watermark','bytes','websiteCopyMatches')} for d in manifest]
    (OUT/'collection-review.json').write_text(json.dumps(review,indent=2),encoding='utf8')
    (OUT/'watermark-manifest.json').write_text(json.dumps(stamps,indent=2),encoding='utf8')
    (ROOT/'src/data/documents.json').write_text(json.dumps(site,indent=2,ensure_ascii=False),encoding='utf8')

if __name__=='__main__':main()
