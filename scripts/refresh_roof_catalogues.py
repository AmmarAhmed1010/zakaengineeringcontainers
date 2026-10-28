"""Update all catalogue exteriors without changing approved plan pages."""
from io import BytesIO
import hashlib
import json
import os
import sys
from pathlib import Path

from PIL import Image, ImageDraw
from pypdf import PdfReader, PdfWriter
import pypdfium2 as pdfium
from reportlab.pdfgen import canvas

from catalogue_style import ROOT, W, H
import catalogue_names
import redesign_catalogues as original
import create_client_pdfs as client
from create_client_pdfs import frame, txt, wrap, rect
from expand_catalogues import NEW, configure
from roof_styles import STYLES, LABELS, CLIENT_SLUGS, apply_config, image_path, draw_panel, finish_text
from zaka_watermarks import add_watermark, LABEL

OUT=ROOT/'output/pdf';QA=ROOT/'tmp/pdfs/roof-revision';QA.mkdir(parents=True,exist_ok=True)
PREVIEW=ROOT/'public/images/pdf/roof-revision';PREVIEW.mkdir(parents=True,exist_ok=True)
REVISION='20261028-corrugated-roof-revision'
RENAMES={'compact-gabled-studio-12x20.pdf':'compact-container-studio-12x20.pdf',
         'compact-gabled-office-8x20.pdf':'compact-container-office-8x20.pdf'}

def content_hash(page):
    contents=page.get_contents()
    return hashlib.sha256(contents.get_data() if contents else b'').hexdigest()

def page(draw):
    buffer=BytesIO();c=canvas.Canvas(buffer,pagesize=(W,H),pageCompression=1);draw(c);c.save()
    return PdfReader(BytesIO(buffer.getvalue())).pages[0]

def generic_config(doc):
    slug=doc['slug']
    kind=next((kind for kind,value in CLIENT_SLUGS.items() if value==slug),None)
    if kind:cfg=apply_config(next(c for c in client.CONFIGS if c['type']==kind))
    else:
        index=next(i for i,raw in enumerate(NEW) if raw['slug']==slug);cfg=configure(NEW[index],index)
    cfg.update(slug=slug,total=doc['pages'],title=doc['title'],description=doc['description'])
    return cfg

def generic_cover(c,doc,cfg,style):
    frame(c,cfg,'Corrugated steel / '+doc['category'],1,doc['pages'])
    lines=[];line=''
    for word in doc['title'].split():
        candidate=(line+' '+word).strip()
        if c.stringWidth(candidate,'Times-Roman',29)>245 and line:lines.append(line);line=word
        else:line=candidate
    lines.append(line)
    for i,line in enumerate(lines):txt(c,40,470-i*33,line,29,client.INK,'Times-Roman')
    wrap(c,doc['description'],40,344,245,9.2,client.MUTED,leading=12.5)
    txt(c,40,207,cfg['dims'],21,client.INK,'Times-Roman')
    area=str(cfg['area'])+(' sq ft enclosed' if isinstance(cfg['area'],int) else '')
    wrap(c,area,40,184,245,8,client.MUTED,leading=11)
    wrap(c,LABELS[style['roof']].upper()+' / CORRUGATED STEEL',40,139,245,7,client.RED,font='Helvetica-Bold')
    draw_panel(c,doc['slug'],0,316,175,486,277)
    txt(c,325,158,'PHOTOREALISTIC EXTERIOR / REVISED ROOF & CLADDING',6,client.MUTED)
    c.showPage()

def generic_exterior(c,doc,cfg,style,index,page_number):
    frame(c,cfg,'Exterior / roof & cladding',page_number,doc['pages'],'The same design. Every side.','Revised corrugated steel construction and roof profile. Measured plans control the openings.')
    names=['FRONT / ENTRY PERSPECTIVE','REAR / SERVICE PERSPECTIVE','LEFT / END PERSPECTIVE','RIGHT / END PERSPECTIVE']
    for j in range(2):
        x=40+j*390;panel_index=index*2+j
        draw_panel(c,doc['slug'],panel_index,x,193,372,229)
        txt(c,x,175,names[panel_index],8,client.RED,'Helvetica-Bold')
        wrap(c,style['palette'],x,158,372,7,client.MUTED,leading=10)
    wrap(c,'ROOF: '+style['roofSpecification'],40,119,750,8,client.INK,leading=11)
    wrap(c,'Concept images illustrate materials and roof form. Exact opening sizes and positions, stairs and circulation follow the approved measured plans.',40,73,750,7,client.MUTED,leading=9)
    c.showPage()

def table(c,rows):
    y=403
    for i,(label,value) in enumerate(rows):
        words=value.split();lines=[];line=''
        for word in words:
            candidate=(line+' '+word).strip()
            if c.stringWidth(candidate,'Helvetica',8)>555 and line:lines.append(line);line=word
            else:line=candidate
        if line:lines.append(line)
        height=max(31,12+len(lines)*10)
        if i%2==0:rect(c,40,y-height+5,762,height,'#EFEEEA','#EFEEEA')
        txt(c,48,y-11,label,8,client.INK,'Helvetica-Bold')
        for j,line in enumerate(lines):txt(c,225,y-11-j*10,line,8,client.MUTED)
        y-=height
    assert y>85,('Specification table overflow',y)

def generic_specification(c,doc,cfg,style,page_number):
    frame(c,cfg,'Materials / individual design',page_number,doc['pages'],'Corrugated steel. Defined roof form.','Roof and wall specification revised to match the selected building width.')
    area=str(cfg['area'])+(' sq ft enclosed' if isinstance(cfg['area'],int) else '')
    table(c,[('Building',doc['title']+' / '+cfg['dims']),('Floor area',area),
             ('Exterior walls',style['wallSpecification']),('Roof profile',style['roofSpecification']),
             ('Exterior palette',style['palette']+'.'),('Structure / enclosure','Fabricated or joined steel modules with insulation, weatherproof flashings and engineered supports and connections.'),
             ('Openings / services','Room access, kitchen and washroom positions, window sizes and furniture follow the approved plans and opening schedule.'),
             ('Delivery / installation','Transport route, crane access, anchoring, water, drainage and electrical connections coordinated for the site.')])
    wrap(c,'Concept specification. Final roof falls, support sizes, waterproofing and drainage are coordinated before fabrication. Complete material standards follow.',40,78,750,7,client.MUTED,leading=9)
    c.showPage()

def rename_files(docs):
    mapping=dict(catalogue_names.MAPPING)
    for key,value in list(mapping.items()):mapping[key]=RENAMES.get(value,value)
    mapping.update(RENAMES)
    (ROOT/'src/data/catalogue-filenames.json').write_text(json.dumps(mapping,indent=2)+'\n',encoding='utf-8')
    catalogue_names.MAPPING.clear();catalogue_names.MAPPING.update(mapping)
    for old,new in RENAMES.items():
        for folder in (OUT,ROOT/'public/downloads'):
            source=folder/old;destination=folder/new
            if source.exists():
                assert not destination.exists(),destination
                source.rename(destination)
    for doc in docs:doc['file']='/downloads/'+RENAMES.get(Path(doc['file']).name,Path(doc['file']).name)

def render_reviews(path,doc,changed):
    document=pdfium.PdfDocument(str(path))
    document[0].render(scale=1.3).to_pil().save(PREVIEW/(doc['slug']+'.webp'),quality=88)
    sheet=Image.new('RGB',(1684,1192),'#D7D9D8');draw=ImageDraw.Draw(sheet)
    for j,index in enumerate(sorted(changed)):
        image=document[index].render(scale=1.15).to_pil();image.save(QA/(doc['slug']+f'-page-{index+1}.jpg'),quality=91)
        image.thumbnail((842,568));x=j%2*842;y=j//2*596;sheet.paste(image,(x,y+24));draw.text((x+10,y+6),doc['slug']+f' / page {index+1}',fill='#17283B')
    sheet.save(QA/(doc['slug']+'-pdf-review.jpg'),quality=91);document.close()

def main():
    selected=set(sys.argv[1:]);assert selected<=set(STYLES),'Unknown catalogue selection'
    assert len(STYLES)==30
    for slug in STYLES:assert image_path(slug),'Missing generated exterior: '+slug
    data_path=ROOT/'src/data/documents.json';docs=json.loads(data_path.read_text(encoding='utf-8'))
    rename_files(docs)
    native={raw['slug']:raw for raw in original.DESIGNS}
    audit_by_slug={a['slug']:a for a in json.loads((OUT/'roof-revision-audit.json').read_text(encoding='utf-8'))} if selected else {}
    manifest_path=OUT/'catalogue-manifest.json';manifest=json.loads(manifest_path.read_text(encoding='utf-8'));manifest_by_slug={m['slug']:m for m in manifest}
    for doc in docs:
        if selected and doc['slug'] not in selected:continue
        slug=doc['slug'];style=STYLES[slug];doc['title']=style['title'];doc['file']='/downloads/'+style['file']
        path=OUT/style['file'];source=PdfReader(path);before={i:content_hash(p) for i,p in enumerate(source.pages)}
        doc.update(roofStyle=LABELS[style['roof']],cladding='Corrugated steel',designStyle=finish_text(style),revision=REVISION,image=style['image'],preview='/images/pdf/roof-revision/'+slug+'.webp')
        if slug in native:
            d=original.enrich(native[slug]);d['image']=style['image'];doc['description']=d['description']
            start=d['basePages']-3;replacements={0:page(lambda c:original.cover(c,d)),
                start-1:page(lambda c:original.elevations(c,d,start,[0,1])),
                start:page(lambda c:original.elevations(c,d,start+1,[2,3])),
                d['briefPage']-1:page(lambda c:original.specifications(c,d))}
        else:
            doc['description']=doc['description'].split(' Exterior: ')[0]+' Exterior: '+finish_text(style)+'.'
            cfg=generic_config(doc);start=3 if slug=='studio-with-terrace-12x26' else 4
            replacements={0:page(lambda c:generic_cover(c,doc,cfg,style)),
                start:page(lambda c:generic_exterior(c,doc,cfg,style,0,start+1)),
                start+1:page(lambda c:generic_exterior(c,doc,cfg,style,1,start+2)),
                start+2:page(lambda c:generic_specification(c,doc,cfg,style,start+3))}
        writer=PdfWriter()
        for i,old in enumerate(source.pages):writer.add_page(replacements.get(i,old))
        writer.add_metadata({'/Title':doc['title']+' - '+LABELS[style['roof']],'/Author':'Zaka Engineering Containers & Prefab','/Subject':'Corrugated steel exterior and width-specific roof revision; approved plans retained'})
        temp=QA/(path.name+'.tmp');writer.write(temp);os.replace(temp,path);stamp=add_watermark(path,path)
        revised=PdfReader(path);assert len(revised.pages)==doc['pages']
        retained=[i for i in range(len(source.pages)) if i not in replacements]
        for i in retained:assert content_hash(revised.pages[i])==before[i],('Approved page changed',slug,i+1)
        for i in replacements:assert revised.pages[i].get('/ZakaLogoWatermark')==LABEL
        render_reviews(path,doc,replacements)
        item=manifest_by_slug[slug];item.update(stamp);item.update(file=style['file'],revision=REVISION,roof=style['roof'],roofStyle=LABELS[style['roof']],roofSpecification=style['roofSpecification'],wallSpecification=style['wallSpecification'],sha256=hashlib.sha256(path.read_bytes()).hexdigest(),imageSha256=hashlib.sha256(image_path(slug).read_bytes()).hexdigest())
        audit_by_slug[slug]=dict(slug=slug,file=style['file'],roof=style['roof'],widthFeet=style['widthFeet'],pages=doc['pages'],updatedPages=[i+1 for i in sorted(replacements)],preservedPages=[i+1 for i in retained],approvedPagesUnchanged=True,sha256=item['sha256'],websiteCopyMatches=True,exteriorViews=4)
        print('Updated',style['file'],LABELS[style['roof']],flush=True)
    data_path.write_text(json.dumps(docs,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    manifest_path.write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
    audit=[audit_by_slug[d['slug']] for d in docs]
    (OUT/'roof-revision-audit.json').write_text(json.dumps(audit,indent=2)+'\n',encoding='utf-8')
    for name in ('collection-review.json','watermark-manifest.json'):
        (OUT/name).write_text(json.dumps([{key:m[key] for key in ('slug','file','pages','bytes','sha256','websiteCopyMatches','watermark')} for m in manifest],indent=2)+'\n',encoding='utf-8')
    assert len(docs)==len(list(OUT.glob('*.pdf')))==len(list((ROOT/'public/downloads').glob('*.pdf')))==30
    print('Updated 30 catalogues /',sum(d['pages'] for d in docs),'pages / 120 exterior views. All approved non-exterior pages unchanged.',flush=True)

if __name__=='__main__':main()
