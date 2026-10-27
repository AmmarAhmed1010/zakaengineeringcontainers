"""Refresh sleeping-room plans and executive glazing without changing other pages."""
from pathlib import Path
from io import BytesIO
import json
import os
from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
import pypdfium2 as pdfium
from PIL import Image, ImageDraw

from redesign_catalogues import DESIGNS, enrich
from client_floor_plans import draw_plan
from catalogue_style import ROOT, W, H
from bed_furniture import AUDIT
from zaka_watermarks import add_watermark, main as update_watermarks

QA=ROOT/'tmp/pdfs/bed-layout-review';QA.mkdir(parents=True,exist_ok=True)

def main():
    AUDIT.clear();reviews=[];changed=[]
    for raw in DESIGNS:
        d=enrich(raw);pages={}
        for floor,rooms in enumerate(d['floors']):
            if not any(r['kind'] in ('bed','studio') for r in rooms) and d['slug']!='office-10x20':continue
            buffer=BytesIO();c=canvas.Canvas(buffer,pagesize=(W,H));draw_plan(c,d,floor,floor+2);c.save()
            pages[floor+1]=PdfReader(BytesIO(buffer.getvalue())).pages[0]
        if not pages:continue
        path=ROOT/'output/pdf'/('zaka-'+d['slug']+'.pdf');original=PdfReader(path);writer=PdfWriter()
        if original.metadata:writer.add_metadata(dict(original.metadata))
        for i,page in enumerate(original.pages):writer.add_page(pages.get(i,page))
        temp=QA/(path.name+'.tmp');writer.write(temp);os.replace(temp,path);add_watermark(path,path)
        reviews.extend((path,i) for i in pages);changed.append(d['slug'])
        print('Revised',path.name,'plan pages:',[i+1 for i in pages],flush=True)

    from create_client_pdfs import CONFIGS,author
    for cfg in CONFIGS:
        path=author(cfg);reviews.extend((path,i) for i in range(1,2 if cfg['type']=='studio' else 3))
        print('Revised',path.name,flush=True)

    (ROOT/'output/pdf/bed-layout-audit.json').write_text(json.dumps(AUDIT,indent=2)+'\n',encoding='utf-8')
    update_watermarks()
    data_path=ROOT/'src/data/documents.json';data=json.loads(data_path.read_text(encoding='utf-8'))
    for doc in data:
        if doc['slug'] in changed:doc['revision']='20261027-bed-layouts-front-window'
    data_path.write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    manifest_path=ROOT/'output/pdf/catalogue-manifest.json';manifest=json.loads(manifest_path.read_text(encoding='utf-8'))
    for item in manifest:
        item['bytes']=(ROOT/'output/pdf'/item['file']).stat().st_size
        beds=[entry for entry in AUDIT if entry['context'].split(' / ')[0]==item['slug']]
        if beds:item['bedFurniture']=beds
        if item['slug']=='office-10x20':
            from client_floor_plans import REVISIONS
            item['windows']=REVISIONS['office-10x20']['floors'][0]['windows']
    manifest_path.write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')

    thumbnails=[]
    for path,i in reviews:
        doc=pdfium.PdfDocument(str(path));img=doc[i].render(scale=1.3).to_pil()
        img.save(QA/(path.stem+f'-page-{i+1}.png'))
        crop=img.crop((40,int((H-435)*1.3),int((W-30)*1.3),int((H-165)*1.3)))
        crop.thumbnail((780,270));thumb=Image.new('RGB',(800,305),'#FAF9F6')
        thumb.paste(crop,((800-crop.width)//2,27));ImageDraw.Draw(thumb).text((12,7),path.stem+f' / page {i+1}',fill='#17283B')
        thumbnails.append(thumb)
    for start in range(0,len(thumbnails),6):
        sheet=Image.new('RGB',(1600,915),'#D7D9D8')
        for j,img in enumerate(thumbnails[start:start+6]):sheet.paste(img,((j%2)*800,(j//2)*305))
        sheet.save(QA/f'review-{start//6+1}.png')
    print('Validated',len(AUDIT),'beds across',len(reviews),'floor-plan pages.',flush=True)
    print('Minimum side/foot access:',min(min(v['sideClearancesFeet']+[v['footClearanceFeet']]) for v in AUDIT),'ft.',flush=True)

if __name__=='__main__':main()
