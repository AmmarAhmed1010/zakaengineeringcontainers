"""Rebuild the four requested home revisions and synchronize the website."""
from io import BytesIO
import hashlib
import json
import os

from PIL import Image, ImageDraw
from pypdf import PdfReader, PdfWriter
import pypdfium2 as pdfium
from reportlab.pdfgen import canvas

from catalogue_style import ROOT, W, H
from catalogue_names import original_filename, filename
from redesign_catalogues import DESIGNS, enrich, cover
from client_floor_plans import draw_plan
from create_client_pdfs import CONFIGS, author as client_author
from expand_catalogues import NEW, configure, author as new_author, previews, PREVIEW
from bed_furniture import AUDIT
from zaka_watermarks import add_watermark

QA=ROOT/'tmp/pdfs/home-access';QA.mkdir(parents=True,exist_ok=True)
REVISION='20261028-home-access'
TARGETS={'portable-12x24','compact-container-home','two-bedroom-living-12x40-and-12x44','silver-one-bedroom-home-12x32'}

def rendered_page(draw):
    buf=BytesIO();c=canvas.Canvas(buf,pagesize=(W,H));draw(c);c.save()
    return PdfReader(BytesIO(buf.getvalue())).pages[0]

def main():
    AUDIT.clear();PREVIEW.mkdir(parents=True,exist_ok=True)
    path=ROOT/'src/data/documents.json';docs=json.loads(path.read_text(encoding='utf-8'));by_slug={d['slug']:d for d in docs}
    designs={};review=[]
    for slug,floor in [('portable-12x24',1),('compact-container-home',0)]:
        d=enrich(next(raw for raw in DESIGNS if raw['slug']==slug));d['image']=by_slug[slug]['image'];designs[slug]=d
        pdf=ROOT/'output/pdf'/original_filename(slug);source=PdfReader(pdf);writer=PdfWriter()
        replacements={floor+1:rendered_page(lambda c:draw_plan(c,d,floor,floor+2))}
        if slug=='portable-12x24':replacements[0]=rendered_page(lambda c:cover(c,d))
        if source.metadata:writer.add_metadata(dict(source.metadata))
        for i,page in enumerate(source.pages):writer.add_page(replacements.get(i,page))
        temp=QA/(pdf.name+'.tmp');writer.write(temp);os.replace(temp,pdf);add_watermark(pdf,pdf)
        document=pdfium.PdfDocument(str(pdf));document[0].render(scale=1.3).to_pil().save(ROOT/'public'/by_slug[slug]['preview'].lstrip('/'),quality=88);document.close()
        by_slug[slug]['description']=d['description']
        review.append((slug,pdf,floor+1));print('Updated',pdf.name,flush=True)
    cfg=next(cfg for cfg in CONFIGS if cfg['type']=='residence')
    pdf=client_author(cfg);slug='two-bedroom-living-12x40-and-12x44';previews(pdf,slug)
    by_slug[slug]['description']=cfg['desc'];review.append((slug,pdf,1));print('Updated',pdf.name,flush=True)
    index=next(i for i,raw in enumerate(NEW) if raw['slug']=='silver-one-bedroom-home-12x32')
    cfg=configure(NEW[index],index);pdf,plan=new_author(cfg);previews(pdf,cfg['slug']);review.append((cfg['slug'],pdf,1));print('Updated',pdf.name,flush=True)
    for doc in docs:
        if doc['slug'] in TARGETS:doc['revision']=REVISION
    path.write_text(json.dumps(docs,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    # Preserve bed records for untouched floors, replacing only revised contexts.
    bed_contexts={}
    for records in [json.loads((ROOT/'output/pdf/bed-layout-audit.json').read_text(encoding='utf-8')),
                    json.loads((ROOT/'output/pdf/collection-30-bed-audit.json').read_text(encoding='utf-8')),AUDIT]:
        grouped={}
        for bed in records:grouped.setdefault(bed['context'],[]).append(bed)
        bed_contexts.update(grouped)
    all_beds=[bed for records in bed_contexts.values() for bed in records]
    (ROOT/'output/pdf/bed-layout-audit.json').write_text(json.dumps(all_beds,indent=2)+'\n',encoding='utf-8')
    path=ROOT/'output/pdf/catalogue-manifest.json';manifest=json.loads(path.read_text(encoding='utf-8'))
    for item in manifest:
        slug=item['slug']
        if slug not in TARGETS:continue
        pdf=ROOT/'output/pdf'/item['file'];item.update(bytes=pdf.stat().st_size,sha256=hashlib.sha256(pdf.read_bytes()).hexdigest(),revision=REVISION)
        if slug in designs:item['floorZones']=designs[slug]['floors']
        if slug==cfg['slug']:item.update(rooms=cfg['rooms'],windows=plan.windows,doors=plan.doors,bedFurniture=plan.beds)
        beds=[b for b in all_beds if b['context'].split(' / ')[0] in (slug,item['file'])]
        if beds:item['bedFurniture']=beds
    path.write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8');by_file={m['file']:m for m in manifest}
    for name in ('collection-review.json','watermark-manifest.json'):
        path=ROOT/'output/pdf'/name;records=json.loads(path.read_text(encoding='utf-8'))
        for item in records:
            current=by_file.get(item.get('file'))
            if current:
                for key in ('bytes','sha256'):
                    if key in item:item[key]=current[key]
        path.write_text(json.dumps(records,indent=2)+'\n',encoding='utf-8')
    (ROOT/'output/pdf/home-access-bed-audit.json').write_text(json.dumps(AUDIT,indent=2)+'\n',encoding='utf-8')
    sheet=Image.new('RGB',(1684,1192),'#D7D9D8');draw=ImageDraw.Draw(sheet)
    for i,(slug,pdf,index) in enumerate(review):
        document=pdfium.PdfDocument(str(pdf));image=document[index].render(scale=1.5).to_pil();image.save(QA/(slug+'.png'))
        image.thumbnail((842,568));x=i%2*842;y=i//2*596;sheet.paste(image,(x,y+24));draw.text((x+10,y+6),slug,fill='#17283B');document.close()
    sheet.save(QA/'four-layouts.png')
    # The upper lobby must contain no kitchen, and the residence has an internal
    # bedroom connection instead of an outside-only entrance.
    duplex=PdfReader(ROOT/'output/pdf'/original_filename('portable-12x24')).pages[2].extract_text()
    assert 'Kitchen / entry' not in duplex and 'Entrance / lobby' in duplex and 'FIRST-FLOOR ENTRANCE' in duplex
    residence=PdfReader(ROOT/'output/pdf'/filename(next(c['file'] for c in CONFIGS if c['type']=='residence')))
    assert 'D7' in residence.pages[1].extract_text() and 'D5' not in residence.pages[1].extract_text()
    print('Revised four PDFs; validated',len(AUDIT),'bed placements; canonical and website copies synchronized.',flush=True)

if __name__=='__main__':main()
