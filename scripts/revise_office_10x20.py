"""Apply the requested office correction and refresh branded catalogue previews."""
from io import BytesIO
import json
import os
from pathlib import Path
from pypdf import PdfReader, PdfWriter
import pypdfium2 as pdfium
from reportlab.pdfgen import canvas

from redesign_catalogues import DESIGNS, enrich
from client_floor_plans import draw_plan, REVISIONS
from catalogue_style import ROOT, W, H
from zaka_watermarks import main as update_watermarks, LABEL

def main():
    slug='office-10x20';d=enrich(next(v for v in DESIGNS if v['slug']==slug))
    source=ROOT/'output/pdf'/('zaka-'+slug+'.pdf')
    buf=BytesIO();c=canvas.Canvas(buf,pagesize=(W,H));draw_plan(c,d,0,2);c.save()
    replacement=PdfReader(BytesIO(buf.getvalue()));original=PdfReader(source);writer=PdfWriter()
    if original.metadata:writer.add_metadata(dict(original.metadata))
    for i,page in enumerate(original.pages):writer.add_page(replacement.pages[0] if i==1 else page)
    temp=ROOT/'tmp/pdfs/office-10x20-revised.pdf';temp.parent.mkdir(parents=True,exist_ok=True)
    writer.write(temp);os.replace(temp,source)
    update_watermarks()
    data_path=ROOT/'src/data/documents.json';data=json.loads(data_path.read_text(encoding='utf-8'))
    for doc in data:
        doc['revision']='20261027-kitchen-logo' if doc['slug']==slug else '20261027-zaka-logo'
        pdf=ROOT/'public'/doc['file'].lstrip('/');preview=ROOT/'public'/doc['preview'].lstrip('/')
        document=pdfium.PdfDocument(str(pdf));preview.parent.mkdir(parents=True,exist_ok=True)
        document[0].render(scale=1.25).to_pil().save(preview,quality=90)
    data_path.write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    manifest_path=ROOT/'output/pdf/catalogue-manifest.json'
    manifest=json.loads(manifest_path.read_text(encoding='utf-8'))
    for item in manifest:
        item['watermark']=LABEL
        item['bytes']=(ROOT/'output/pdf'/item['file']).stat().st_size
        if item['slug']==slug:
            item['floorZones']=d['floors'];item['windows']=REVISIONS[slug]['floors'][0]['windows']
    manifest_path.write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
    qa=ROOT/'tmp/pdfs/current-review';qa.mkdir(parents=True,exist_ok=True)
    for filename,indices in [('zaka-office-10x20.pdf',[0,1,5]),('zaka-client-01-family-home-two-floors.pdf',[1,7]),('zaka-studio-12x21-terrace.pdf',[1])]:
        document=pdfium.PdfDocument(str(ROOT/'output/pdf'/filename))
        for index in indices:document[index].render(scale=1.3).to_pil().save(qa/(Path(filename).stem+f'-{index+1:02d}.png'))
    print('Office plan, website copies and previews updated.',flush=True)

if __name__=='__main__':main()
