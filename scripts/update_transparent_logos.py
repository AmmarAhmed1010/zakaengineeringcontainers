"""Replace embedded logo images without altering the catalogue layouts."""
from pathlib import Path
import os
import json
import shutil
from PIL import Image
from pypdf import PdfReader, PdfWriter
import pypdfium2 as pdfium
from io import BytesIO
from reportlab.pdfgen import canvas
from catalogue_names import filename

ROOT=Path(__file__).resolve().parents[1]
QA=ROOT/'tmp/pdfs/transparent-logo-review';QA.mkdir(parents=True,exist_ok=True)
ASSETS=ROOT/'public/images/original'
REPLACEMENTS={(472,275):ASSETS/'Zaka-logo-transparent.png',
              (1200,480):ASSETS/'Containers-Prefab-watermark.png'}

def main():
    templates={}
    for size,asset in REPLACEMENTS.items():
        buffer=BytesIO();page=canvas.Canvas(buffer,pagesize=size)
        page.drawImage(str(asset),0,0,width=size[0],height=size[1],mask='auto');page.save()
        holder=PdfReader(BytesIO(buffer.getvalue()))
        templates[size]=next(iter(holder.pages[0]['/Resources']['/XObject'].values())).get_object()
    results=[]
    for source in sorted((ROOT/'output/pdf').glob('*.pdf')):
        writer=PdfWriter(clone_from=PdfReader(source));replaced=set()
        for page in writer.pages:
            for image in list(page.images):
                ref=image.indirect_reference
                if ref is None or ref.idnum in replaced:continue
                obj=ref.get_object();size=(obj.get('/Width'),obj.get('/Height'))
                if size not in REPLACEMENTS:continue
                replacement=templates[size].clone(writer)
                obj.clear();obj.update(replacement);obj._data=replacement._data
                obj.decoded_self=None
                if '/SMask' not in ref.get_object():raise RuntimeError('Logo lost its transparency')
                replaced.add(ref.idnum)
        if not replaced:raise RuntimeError('No logo images found in '+source.name)
        temp=QA/(source.name+'.tmp');writer.write(temp);os.replace(temp,source)
        shutil.copy2(source,ROOT/'public/downloads'/source.name)
        results.append((source.name,len(writer.pages),len(replaced)))
        print(source.name,'transparent logo objects:',len(replaced),flush=True)

    data_path=ROOT/'src/data/documents.json';data=json.loads(data_path.read_text(encoding='utf-8'))
    for doc in data:
        doc['revision']='20261027-transparent-logo'
        d=pdfium.PdfDocument(str(ROOT/'public'/doc['file'].lstrip('/')))
        preview=ROOT/'public'/doc['preview'].lstrip('/')
        d[0].render(scale=1.25).to_pil().save(preview,quality=90)
    data_path.write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    for name in ['zaka-office-10x20.pdf','zaka-client-01-family-home-two-floors.pdf']:
        name=filename(name)
        d=pdfium.PdfDocument(str(ROOT/'output/pdf'/name))
        for i in [0,1]:d[i].render(scale=1.25).to_pil().save(QA/(Path(name).stem+f'-{i+1}.png'))
    print('Updated',len(results),'catalogues with transparent header and watermark logos.',flush=True)

if __name__=='__main__':main()
