"""Replace legacy preview stamps with the actual website logo, idempotently."""
from io import BytesIO
import json
import os
from pathlib import Path
import shutil
import subprocess

from pypdf import PdfReader, PdfWriter
from pypdf.generic import NameObject, TextStringObject
from reportlab.pdfgen import canvas

ROOT=Path(__file__).resolve().parents[1]
OUTPUT=ROOT/'output/pdf'
DOWNLOADS=ROOT/'public/downloads'
QA=ROOT/'tmp/pdfs/watermark-review'
LOGO=ROOT/'public/images/original/Containers-Prefab-watermark.png'
LABEL='ZAKA WEBSITE LOGO v1'
LEGACY_LABEL='GRID AND LOGIC'

def ensure_logo():
    if not LOGO.exists():
        # Render the same SVG used by the website header; no new logo artwork.
        subprocess.run(['node',str(ROOT/'scripts/prepare_brand_logo.mjs')],cwd=ROOT,check=True)

def remove_legacy_watermark(page):
    stream=page.get_contents()
    if stream is None:return 0
    stack=[];enclosing={};ends={};hits=[]
    for i,(args,operator) in enumerate(stream.operations):
        if operator==b'q':stack.append(i)
        elif operator==b'Q' and stack:ends[stack.pop()]=i
        if operator in (b'Tj',b'TJ') and LEGACY_LABEL in str(args):
            hits.append(i);enclosing[i]=stack[-1] if stack else None
    remove=set()
    for hit in hits:
        start=enclosing[hit]
        remove.update(range(start,ends[start]+1) if start is not None and start in ends else [hit])
    if remove:
        stream.operations=[entry for i,entry in enumerate(stream.operations) if i not in remove]
        page.replace_contents(stream)
    return len(hits)

def make_overlay(width,height):
    ensure_logo();buffer=BytesIO();layer=canvas.Canvas(buffer,pagesize=(width,height),pageCompression=1)
    layer.saveState();layer.addLiteral('/ZakaLogoWatermark BMC');layer.setFillAlpha(.12)
    lw=min(width*.38,300);lh=lw*.4
    layer.drawImage(str(LOGO),(width-lw)/2,(height-lh)/2,width=lw,height=lh,mask='auto')
    layer.addLiteral('EMC');layer.restoreState();layer.save()
    return PdfReader(BytesIO(buffer.getvalue()))

def add_watermark(source,destination):
    source=Path(source);destination=Path(destination);QA.mkdir(parents=True,exist_ok=True)
    reader=PdfReader(source,strict=False)
    if not reader.pages:raise ValueError('PDF has no pages: '+source.name)
    writer=PdfWriter(clone_from=reader);removed=0;changed=False;overlays={}
    for page in writer.pages:
        n=remove_legacy_watermark(page);removed+=n;changed|=bool(n)
        if page.get('/ZakaLogoWatermark')==LABEL:continue
        dimensions=(float(page.mediabox.width),float(page.mediabox.height))
        if dimensions not in overlays:overlays[dimensions]=make_overlay(*dimensions)
        page.merge_page(overlays[dimensions].pages[0],over=True)
        page[NameObject('/ZakaLogoWatermark')]=TextStringObject(LABEL);changed=True
    if changed or source.resolve()!=destination.resolve():
        temp=QA/(source.name+'.tmp');writer.write(temp);os.replace(temp,destination)
    public=DOWNLOADS/destination.name
    if destination.resolve()!=public.resolve():shutil.copy2(destination,public)
    checked=PdfReader(destination)
    for i,page in enumerate(checked.pages):
        if LEGACY_LABEL in (page.extract_text() or ''):raise RuntimeError(f'Legacy stamp remains: {source.name}, page {i+1}')
        if page.get('/ZakaLogoWatermark')!=LABEL:raise RuntimeError(f'Logo missing: {source.name}, page {i+1}')
    return dict(file=source.name,pages=len(checked.pages),watermark=LABEL,bytes=destination.stat().st_size,
                legacyWatermarksRemoved=removed,websiteCopyMatches=destination.read_bytes()==public.read_bytes())

def main():
    sources=sorted(OUTPUT.glob('*.pdf'))
    if not sources:raise RuntimeError('No catalogue PDFs found')
    results=[]
    for path in sources:
        result=add_watermark(path,path);results.append(result);print(path.name,result['pages'],'pages',flush=True)
    (OUTPUT/'watermark-manifest.json').write_text(json.dumps(results,indent=2),encoding='utf-8')
    print('Updated',len(results),'catalogues /',sum(x['pages'] for x in results),'pages.',flush=True)

if __name__=='__main__':main()
