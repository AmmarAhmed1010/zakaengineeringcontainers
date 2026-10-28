"""Generate twelve six-page catalogues with measured plans and four exterior renders."""
from catalogue_style import *

ASSETS=ROOT/'public/images/catalogues'
catalogues=json.loads((ROOT/'scripts/catalogue_layouts.json').read_text())
PANEL_BOUNDS={}

def panel_bounds(im,slug):
    if slug in PANEL_BOUNDS:return PANEL_BOUNDS[slug]
    iw,ih=im.size;px=im.load()
    def white(pixel):return min(pixel)>225 and max(pixel)-min(pixel)<18
    rows=[y for y in range(int(ih*.3),int(ih*.7)) if sum(white(px[x,y]) for x in range(0,iw,8))/(len(range(0,iw,8)))>.9]
    cols=[x for x in range(int(iw*.3),int(iw*.7)) if sum(white(px[x,y]) for y in range(0,ih,8))/(len(range(0,ih,8)))>.9]
    if not rows or not cols:raise ValueError(f'No clean four-panel divider found: {slug}')
    def longest_run(values):
        groups=[];run=[]
        for value in values:
            if run and value!=run[-1]+1:groups.append(run);run=[]
            run.append(value)
        groups.append(run)
        return max(groups,key=len)
    rows=longest_run(rows);cols=longest_run(cols)
    bounds=[(0,0,min(cols),min(rows)),(max(cols)+1,0,iw,min(rows)),(0,max(rows)+1,min(cols),ih),(max(cols)+1,max(rows)+1,iw,ih)]
    PANEL_BOUNDS[slug]=bounds;return bounds

def render_panel(c,d,panel,x,y,w,h):
    # Clip at PDF composition time; generated source images stay intact.
    source=ASSETS/(d['slug']+'.webp')
    im=Image.open(source).convert('RGB');iw,ih=im.size
    compressed=QA/(d['slug']+'.jpg')
    if not compressed.exists() or source.stat().st_mtime>compressed.stat().st_mtime:
        im.save(compressed,quality=92,optimize=True)
    lx,ty,rx,by=panel_bounds(im,d['slug'])[panel]
    s=min(w/(rx-lx),h/(by-ty))
    pw,ph=(rx-lx)*s,(by-ty)*s;left=x+(w-pw)/2;bottom=y+(h-ph)/2
    c.saveState();clip=c.beginPath();clip.rect(left,bottom,pw,ph);c.clipPath(clip,stroke=0,fill=0)
    c.drawImage(str(compressed),left-lx*s,bottom-(ih-by)*s,width=iw*s,height=ih*s)
    c.restoreState()

def enrich(d,i):
    d.update(code=f'ZE-{i+1:02d}',area=d['width']*d['length'],type=d['kind'])
    width,length=d['width'],d['length']
    if d['kind']=='office':
        main=length-6
        d['description']=f'A {width} x {length} ft portable workspace with a dedicated {main} x {width} ft office zone, a compact washroom and an entrance/pantry bay. Perimeter furniture leaves a central path for daily circulation.'
        d['subtitle']='A focused place to work. Ready for your next site.'
        d['rooms']=[('Office workspace',main,width),('Washroom',6,4),('Kitchen' if d['slug']=='office-10x20' else 'Entry / pantry',6,width-4)]
    elif d['kind']=='home':
        d['description']=f'A {width} x {length} ft portable residence with a private bedroom, a central living and dining space, a kitchenette and bathroom. The longer footprint gives each activity a dedicated zone.'
        d['subtitle']='Room to settle in. Freedom to move.'
        d['rooms']=[('Bedroom',12,width),('Living / dining',length-18,width),('Kitchenette',6,6),('Bathroom',6,6)]
    else:
        d['description']=f'A {width} x {length} ft open studio combining sleeping, sitting and everyday dining, with a kitchenette and separate bathroom in a compact service bay.'
        d['subtitle']='One thoughtful room. A complete everyday space.'
        d['rooms']=[('Studio / living',length-6,width),('Kitchenette',6,6),('Bathroom',6,6)]
        if d.get('terrace'):
            d['description']+=' A 12 x 5 ft terrace extends from the right short end, giving a 12 x 26 ft overall footprint.'
            d['subtitle']='A compact studio. An outdoor room of your own.'
            d['rooms'].append(('Additional terrace',5,12))
    d['inspiration']='Client size brief and supplied container-room and office reference proposals. Widths above a standard shipping container require a fabricated or joined-module solution.'
    if d.get('terrace'):d['inspiration']+=' Terrace assumed additional to the 12 x 21 ft enclosed studio.'
    return d

def cover_v2(c,d):
    header(c,d,1,'Concept catalogue')
    text(c,40,477,d['category'].upper()+' / PORTABLE SPACES',8,'Bold',RED)
    titles={'Studio with Terrace':['Studio with','Terrace'],'Portable Residence':['Portable','Residence'],'Portable Studio':['Portable','Studio'],'Portable Office':['Portable','Office'],'Studio Room':['Studio','Room']}
    a,b=titles[d['title']]
    text(c,40,433,a,29,'Display');text(c,40,394,b,35,'Italic',RED)
    para(c,40,368,d['subtitle'],235,12,NAVY,18)
    para(c,40,310,d['description'],235,9,MUTED,14)
    line(c,40,174,275,174)
    text(c,40,151,f"{d['width']}' x {d['length']}'",23,'Display')
    text(c,40,130,f"{d['area']} SQ FT / ENCLOSED NOMINAL AREA",7.5,'Bold',MUTED)
    text(c,40,110,"PLUS 12' x 5' TERRACE / 60 SQ FT" if d.get('terrace') else 'DESIGN / FABRICATE / DELIVER',7.5,'Bold',RED)
    rect(c,305,105,495,380,SAND);render_panel(c,d,0,310,158,485,300)
    rect(c,305,105,495,43,NAVY)
    text(c,323,123,'FINISHED EXTERIOR / ILLUSTRATIVE ARCHITECTURAL RENDER',7,'Body',PAPER)
    text(c,305,83,'ISLAMABAD, PAKISTAN',8,'Bold',RED)
    text(c,650,83,'DESIGN COLLECTION 2026',7.5,'Body',MUTED)
    c.showPage()

def floor_v2(c,d):
    header(c,d,2,'Floor plan & measurements')
    heading(c,'01 / The layout','Every foot has a purpose.','Overall and room-zone measurements are in feet. Zones are nominal; wall thicknesses are not deducted.')
    length,width=d['length'],d['width'];total=length+d.get('terrace',0)
    s=min(630/total,190/width);x=(W-total*s)/2;y=172;w=length*s;h=width*s
    def wall(a,b,aa,bb):line(c,x+a*s,y+b*s,x+aa*s,y+bb*s,NAVY,1.2)
    def box(a,b,l,k,fill=SAND):rect(c,x+a*s,y+b*s,l*s,k*s,fill,NAVY)
    def label(a,b,value,sub):
        tw=max(pdfmetrics.stringWidth(value.upper(),'Bold',8),pdfmetrics.stringWidth(sub,'Body',7.5))
        rect(c,x+a*s-tw/2-3,y+b*s-16,tw+6,27,HexColor('#f6f4ee'))
        c.setFillColor(NAVY);c.setFont('Bold',8);c.drawCentredString(x+a*s,y+b*s,value.upper())
        c.setFillColor(MUTED);c.setFont('Body',7.5);c.drawCentredString(x+a*s,y+b*s-13,sub)
    def window(a,b,l,vertical=False):
        line(c,x+a*s,y+b*s,x+(a if vertical else a+l)*s,y+(b+l if vertical else b)*s,HexColor('#57879a'),3)
    def door(a,b,l=3,vertical=False):
        xx,yy=x+a*s,y+b*s
        line(c,xx,yy,xx+(0 if vertical else l*s),yy+(l*s if vertical else 0),PAPER,3.5)
        inward=vertical and a==6
        line(c,xx,yy,xx+((-l if inward else l)*s if vertical else 0),yy+(0 if vertical else l*s),RED,.7)
        c.setStrokeColor(RED);c.setLineWidth(.5);c.arc(xx-l*s,yy-l*s,xx+l*s,yy+l*s,90 if inward else 0,90)
    def bed(a,b):box(a,b,5,6,HexColor('#e0d6c7'));box(a+.2,b+4.5,4.6,1.1,PAPER)
    box(0,0,length,width,HexColor('#f6f4ee'))
    bathwidth=4 if d['kind']=='office' else 6;split=width-bathwidth
    wall(6,0 if d['kind']=='office' else split,6,width)
    wall(0,split,6,split)
    label(2.8,split+bathwidth/2-.5,'Bath',f"6' x {bathwidth}'")
    c.setStrokeColor(MUTED);c.setFillColor(PAPER)
    c.ellipse(x+.7*s,y+(width-2.2)*s,x+1.9*s,y+(width-.5)*s,fill=1,stroke=1)
    box(4.1,width-1.6,1.2,1,PAPER);door(6,split+.6,2.5,True)
    if d['kind']=='office':
        label(3.6,split-.8,'Entry',f"6' x {split}'")
        box(.4,.5,1.5,max(1,split-1),HexColor('#e0d6c7'));door(6,.5,min(2.5,split-.6),True)
        main=length-6;label(6+main/2,width/2-.5,'Office workspace',f"{main}' x {width}'")
        for a in range(8,length-3,6):
            box(a,width-2.2,3.5,1.6,HexColor('#e0d6c7'));box(a+1,width-3.2,1.3,.7,PAPER)
        if width>=10:
            for a in range(8,length-3,8):
                if a<length/2+4 and a+3.5>length/2-3:continue
                box(a,.5,3.5,1.6,HexColor('#e0d6c7'))
    else:
        label(3.6,2.1,'Kitchenette',"6' x 6'")
        box(.3,.3,1.5,5.4,HexColor('#e0d6c7'));box(2,4.3,3.7,1.4,HexColor('#e0d6c7'))
        end=length-12 if d['kind']=='home' else length
        if d['kind']=='home':
            wall(end,0,end,width);door(end,1,3,True);bed(length-6.5,5);label(end+6,3,'Bedroom',"12' x 12'")
        else:bed(length-6.5,5)
        main=end-6
        # Position the open-zone label away from the sleeping furniture.
        label(6+main*.35,5,'Living / dining' if d['kind']=='home' else 'Studio / living',f"{main}' x {width}'")
        box(8,8,4,2,HexColor('#e0d6c7')) if main>=18 else box(7,width-2,3,1.4,HexColor('#e0d6c7'))
    door(length/2-1.5,0,3)
    first=max(1,length*.2-2);last=length*.8-1
    window(first,0,3);window(last,0,3);window(first,width,3);window(last,width,3);window(0,width-2,1.5,True)
    if d.get('terrace'):
        box(length,0,5,width,HexColor('#e0d6c7'))
        for t in range(1,10):wall(length+t*.5,0,length+t*.5,width)
        label(length+2.5,6,'Terrace',"5' x 12'");window(length,4,4,True)
        dim(c,x+w,y+h+18,x+total*s,y+h+18,"5' terrace")
        dim(c,x,y+h+40,x+total*s,y+h+40,"26' overall footprint")
    else:window(length,width/2-2,4,True)
    dim(c,x,y+h+18,x+w,y+h+18,f"{length}' enclosed length")
    dim(c,x-25,y,x-25,y+h,f"{width}' enclosed width")
    spans=[6,length-18,12] if d['kind']=='home' else [6,length-6];offset=0
    for span in spans:
        dim(c,x+offset*s,y-20,x+(offset+span)*s,y-20,f"{span}'");offset+=span
    text(c,40,125,'NOMINAL SPACE SCHEDULE',8,'Bold',RED)
    for i,(name,l,k) in enumerate(d['rooms']):
        xx=40+i*190;text(c,xx,105,name,9,'Bold');text(c,xx,89,f"{l}' x {k}' / {l*k} sq ft",8,'Body',MUTED)
    para(c,40,71,'Blue: glazing. Red arcs: indicative door swings. Furniture is illustrative. Zone areas sum to the enclosed gross footprint; terrace area is additional. Final clearances and openings are developed with the client.',W-80,7,leading=9)
    c.showPage()

def exterior_v2(c,d,page,panels):
    header(c,d,page,'Finished exterior / '+('front & rear' if page==3 else 'left & right'))
    heading(c,'02 / Exterior views' if page==3 else '03 / Exterior views','A finished view from every side.','Original architectural visualizations of the proposed finish. Rendered proportions and materials are illustrative.')
    labels=['FRONT / LONG FACADE','REAR / LONG FACADE','LEFT / SHORT END','RIGHT / SHORT END']
    notes=['Centered glazed entrance with daylight windows.','Window openings for daylight and cross ventilation.','High-level glazing at the bathroom service bay.','Glazed connection to the additional 12 x 5 ft terrace.' if d.get('terrace') else 'End glazing for additional daylight.']
    for i,p in enumerate(panels):
        xx=40+i*395;rect(c,xx,166,366,229,SAND);render_panel(c,d,p,xx+6,171,354,216)
        text(c,xx,145,labels[p],9,'Bold',RED)
        text(c,xx,126,f"{d['length'] if p<2 else d['width']}' nominal facade span",10)
        para(c,xx,109,notes[p],366,9,leading=13)
    para(c,40,69,'Finish direction: light corrugated steel, navy frames, dark aluminum glazing and a restrained brick-red roof detail. Final finish, roof build-up and opening sizes are agreed before fabrication.',W-80,7,leading=9)
    c.showPage()

def main():
    manifest=[];site=[]
    for i,raw in enumerate(catalogues):
        from catalogue_names import original_filename
        d=enrich(raw,i);path=OUT/original_filename(d['slug'])
        assert sum(l*k for name,l,k in d['rooms'] if name!='Additional terrace')==d['area']
        c=canvas.Canvas(str(path),pagesize=(W,H),pageCompression=1)
        cover_v2(c,d);floor_v2(c,d);exterior_v2(c,d,3,[0,1]);exterior_v2(c,d,4,[2,3]);spec_page(c,d);planning_page(c,d)
        c.setTitle(f"{d['title']} - {d['width']} x {d['length']} ft | Zaka Engineering")
        c.setSubject('Measured concept floor plan and four exterior views');c.save();shutil.copy2(path,PUBLIC/path.name)
        doc=pymupdf.open(path)
        for j,p in enumerate(doc):
            pix=p.get_pixmap(matrix=pymupdf.Matrix(1.3,1.3));pix.save(str(QA/f"{d['slug']}-{j+1}.png"))
            if j==0:Image.frombytes('RGB',[pix.width,pix.height],pix.samples).save(PREVIEW/(d['slug']+'.webp'),quality=90)
        manifest.append({'slug':d['slug'],'file':str(path),'pages':len(doc),'widthFeet':d['width'],'lengthFeet':d['length'],'terraceFeet':d.get('terrace',0),'bytes':path.stat().st_size})
        title=d['title']+f" {d['width']} × {d['length']}"
        subtitle=f"{d['width']}′ × {d['length']}′ / {d['area']} sq ft"+(' + 60 sq ft terrace' if d.get('terrace') else '')
        site.append({'slug':d['slug'],'code':d['code'],'title':title,'subtitle':subtitle,'description':d['description'],'pages':6,'file':'/downloads/'+path.name,'image':'/images/catalogues/'+d['slug']+'.webp','preview':'/images/pdf/'+d['slug']+'.webp','category':d['category']})
        sheet=Image.new('RGB',(1800,480),'#deded9');draw=ImageDraw.Draw(sheet)
        for j in range(6):
            im=ImageOps.contain(Image.open(QA/f"{d['slug']}-{j+1}.png"),(590,209));xx=(j%3)*600;yy=(j//3)*240
            sheet.paste(im,(xx,yy+22));draw.text((xx+5,yy+4),f"{d['slug']} / {j+1}",fill='black')
        sheet.save(QA/(d['slug']+'-review.jpg'));print(path.name,'6 pages',flush=True)
    (OUT/'catalogue-manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf8')
    (ROOT/'src/data/documents.json').write_text(json.dumps(site,indent=2,ensure_ascii=False),encoding='utf8')
    print('Built',len(manifest),'catalogues.')

if __name__=='__main__':main()
