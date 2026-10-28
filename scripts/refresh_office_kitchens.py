"""Revise office floor-plan pages while retaining exterior and material pages."""
from io import BytesIO
import hashlib
import json
import os
from pathlib import Path

from PIL import Image, ImageDraw
from pypdf import PdfReader, PdfWriter
import pypdfium2 as pdfium
from reportlab.pdfgen import canvas

from redesign_catalogues import DESIGNS, enrich
from client_floor_plans import draw_plan
from catalogue_style import ROOT, W, H
from catalogue_names import original_filename
from office_kitchens import AUDIT
from zaka_watermarks import add_watermark

QA=ROOT/'tmp/pdfs/office-kitchens';QA.mkdir(parents=True,exist_ok=True)
REVISION='20261028-open-office-kitchens'

def main():
    AUDIT.clear();updated={};reviews=[]
    for raw in DESIGNS:
        d=enrich(raw)
        if d['category']!='Workspace':continue
        path=ROOT/'output/pdf'/original_filename(d['slug']);source=PdfReader(path);pages={}
        for index in range(len(d['floors'])):
            buf=BytesIO();c=canvas.Canvas(buf,pagesize=(W,H));draw_plan(c,d,index,index+2);c.save()
            page=PdfReader(BytesIO(buf.getvalue())).pages[0]
            text=page.extract_text()
            assert 'Kitchen' in text and 'pantry' not in text.lower(),(path.name,index)
            pages[index+1]=page
        writer=PdfWriter()
        if source.metadata:writer.add_metadata(dict(source.metadata))
        for i,page in enumerate(source.pages):writer.add_page(pages.get(i,page))
        tmp=QA/(path.name+'.tmp');writer.write(tmp);os.replace(tmp,path);add_watermark(path,path)
        document=pdfium.PdfDocument(str(path))
        for index in pages:
            img=document[index].render(scale=1.4).to_pil();img.save(QA/(d['slug']+f'-floor-{index}.png'))
            reviews.append((d['slug'],index,img.copy()))
        document.close();updated[d['slug']]=d
        print('Updated',path.name,len(pages),'floor plan(s)',flush=True)
    data_path=ROOT/'src/data/documents.json';docs=json.loads(data_path.read_text(encoding='utf-8'))
    for doc in docs:
        if doc['slug'] in updated:doc['revision']=REVISION
    data_path.write_text(json.dumps(docs,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    manifest_path=ROOT/'output/pdf/catalogue-manifest.json';manifest=json.loads(manifest_path.read_text(encoding='utf-8'))
    for item in manifest:
        if item['slug'] not in updated:continue
        path=ROOT/'output/pdf'/item['file'];item.update(bytes=path.stat().st_size,sha256=hashlib.sha256(path.read_bytes()).hexdigest(),revision=REVISION,floorZones=updated[item['slug']]['floors'],kitchenCirculation=[r for r in AUDIT if r['slug']==item['slug']])
    manifest_path.write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
    for name in ['watermark-manifest.json','collection-review.json']:
        records_path=ROOT/'output/pdf'/name;records=json.loads(records_path.read_text(encoding='utf-8'))
        by_file={item['file']:item for item in manifest}
        for item in records:
            source=by_file.get(item.get('file'))
            if source:
                for key in ('bytes','sha256'):
                    if key in item:item[key]=source[key]
        records_path.write_text(json.dumps(records,indent=2)+'\n',encoding='utf-8')
    (ROOT/'output/pdf/office-kitchen-audit.json').write_text(json.dumps(AUDIT,indent=2)+'\n',encoding='utf-8')
    for start in range(0,len(reviews),4):
        sheet=Image.new('RGB',(1684,1192),'#D7D9D8');draw=ImageDraw.Draw(sheet)
        for j,(slug,index,img) in enumerate(reviews[start:start+4]):
            img.thumbnail((842,568));x=j%2*842;y=j//2*596
            sheet.paste(img,(x,y+24));draw.text((x+10,y+7),slug+f' / floor {index-1}',fill='#17283B')
        sheet.save(QA/f'review-{start//4+1}.png')
    print('Verified',len(AUDIT),'office floor plans; all kitchen counters clear of entrance and internal door swings.',flush=True)

if __name__=='__main__':main()
