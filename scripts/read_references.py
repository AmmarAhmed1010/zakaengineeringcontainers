from pathlib import Path
import fitz, json

root=Path(__file__).resolve().parents[1]
out=root/'content/references'
out.mkdir(parents=True,exist_ok=True)
files=["ZE-2501-02 CONTAINER ROOM 16'X40'X9'-6''  PROPOSAL 04.pdf","PK-2411-01 CONTAINER ROOM PROPOSAL 02.pdf","PK-2411-01 CONTAINER ROOM PROPOSAL 03.pdf","CONTAINER_XALAMA_Industrial_Field_Office___Site_Operations_Command_1790864474848.pdf","zaka.pdf","zaka1.pdf"]
summary=[]
for idx,name in enumerate(files):
    p=Path.home()/'Downloads'/name
    doc=fitz.open(p)
    pages=[]
    for n,page in enumerate(doc):
        txt=page.get_text()
        pages.append({'page':n+1,'text':txt,'width':page.rect.width,'height':page.rect.height})
        pix=page.get_pixmap(matrix=fitz.Matrix(1.2,1.2))
        pix.save(str(out/f'ref-{idx+1}-page-{n+1}.png'))
    (out/f'ref-{idx+1}.txt').write_text('\n\n'.join('PAGE '+str(p['page'])+'\n'+p['text'] for p in pages),encoding='utf-8')
    summary.append({'file':name,'pages':pages})
    print(name,'PAGES',len(doc),flush=True)
(out/'references.json').write_text(json.dumps(summary,indent=2,ensure_ascii=False),encoding='utf-8')
