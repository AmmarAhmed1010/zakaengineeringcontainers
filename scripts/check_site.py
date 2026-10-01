import json,concurrent.futures
from pathlib import Path
import requests,pymupdf
root=Path(__file__).resolve().parents[1]
archive=json.loads((root/'src/data/archive.json').read_text(encoding='utf8'))
projects=json.loads((root/'src/data/projects.json').read_text(encoding='utf8'))
routes={'/','/downloads','/source-content','/robots.txt','/sitemap.xml'}
routes.update('/'+p['slug'] for p in archive)
routes.update('/source-content/'+p['slug'] for p in archive)
routes.update('/services/'+s for s in ['portable-prefab-cabins','modified-shipping-units','customized-containers','aluminum-fabrication','ms-iron-fabrication','ss-steel-fabrication'])
routes.update('/downloads/'+s for s in ['single-cabin-office','two-cabin-office','two-bedroom-residence','compact-container-home','industrial-field-office'])
routes.update(p for project in projects for p in project['images'])
routes.update('/images/generated/'+s+'.webp' for s in ['hero','office','interior','workshop'])
def fetch(path):
    try:
        r=requests.get('http://127.0.0.1:3000'+path,timeout=60)
        return {'path':path,'status':r.status_code}
    except Exception as e:return {'path':path,'error':str(e)}
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    responses=list(pool.map(fetch,sorted(routes)))
pdfs=[]
for p in sorted((root/'public/downloads').glob('*.pdf')):
    r=requests.get('http://127.0.0.1:3000/downloads/'+p.name,timeout=30)
    doc=pymupdf.open(p)
    clipped=[]
    for i,page in enumerate(doc):
        for block in page.get_text('dict')['blocks']:
            for line in block.get('lines',[]):
                b=line['bbox']
                if b[0]<0 or b[1]<0 or b[2]>page.rect.width or b[3]>page.rect.height:clipped.append({'page':i+1,'bbox':b})
    pdfs.append({'file':p.name,'pages':len(doc),'response':r.status_code,'mime':r.headers.get('Content-Type'),'validSignature':r.content.startswith(b'%PDF'),'textOutsidePage':clipped})
report={'checkedRoutesAndImages':len(responses),'failedResponses':[r for r in responses if r.get('status')!=200],'pdfs':pdfs,'allResponses':responses}
(root/'output/playwright/http-audit.json').write_text(json.dumps(report,indent=2))
print(json.dumps({k:v for k,v in report.items() if k!='allResponses'},indent=2))
if report['failedResponses'] or any(p['pages']!=5 or p['response']!=200 or not p['validSignature'] or p['textOutsidePage'] for p in pdfs):raise SystemExit(1)
