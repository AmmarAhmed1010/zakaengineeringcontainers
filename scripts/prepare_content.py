import json,re
from pathlib import Path
from PIL import Image,ImageOps,ImageDraw
from bs4 import BeautifulSoup
ROOT=Path(__file__).resolve().parents[1]
pages=json.loads((ROOT/'content/source/pages.json').read_text(encoding='utf-8'))
assets=json.loads((ROOT/'content/source/assets.json').read_text(encoding='utf-8'))
mapping={a['url']:a['local'] for a in assets if 'local' in a}
projects=[]
category={'pak-dream-hotel-restaurant':'Hospitality','noor-kitchen':'Hospitality','mosque-project':'Community'}
for p in pages:
    if not p['slug'].startswith('projects/'): continue
    slug=p['slug'].split('/')[-1]
    lines=p['text'].splitlines()
    def field(label):
        for i,line in enumerate(lines):
            if line.strip().startswith(label): return lines[i+1]
        return ''
    images=list(dict.fromkeys(mapping[i['url']] for i in p['images'] if 'Containers-Prefab' not in i['url'] and i['url'] in mapping))
    soup=BeautifulSoup((ROOT/'content/source'/ (p['slug'].replace('/','__')+'.html')).read_text(encoding='utf8'),'html.parser')
    paragraphs=list(dict.fromkeys(tag.get_text(' ',strip=True) for tag in soup.find_all('p') if len(tag.get_text(' ',strip=True))>150))
    projects.append({'slug':slug,'title':p['title'].split(' – ')[0],'category':category.get(slug,'Workspaces'),'location':field('Location :'),'client':field('Client :'),'startDate':field('Starting Date :'),'endDate':field('Ending Date :'),'images':images,'paragraphs':paragraphs,'sourceUrl':p['url']})
(ROOT/'src/data').mkdir(parents=True,exist_ok=True)
(ROOT/'src/data/projects.json').write_text(json.dumps(projects,ensure_ascii=False,indent=2),encoding='utf-8')
unique={p['slug']:p for p in pages}
archive=[]
for slug,p in unique.items():
    txt=p['text']
    body=txt.split('About Us\n',2)[-1] if 'About Us\n' in txt else txt
    body=body.split('Custom Container Solutions')[0].strip()
    archive.append({'slug':slug,'title':p['title'].split(' – ')[0],'body':body,'text':txt,'sourceUrl':p['url']})
(ROOT/'src/data/archive.json').write_text(json.dumps(archive,ensure_ascii=False,indent=2),encoding='utf-8')
report={'capturedPages':len(pages),'uniquePages':len(unique),'projects':len(projects),'downloadedAssets':sum('local' in a for a in assets),'assetBytes':sum(a.get('bytes',0) for a in assets),'failedDownloads':[a for a in assets if 'error' in a],'brokenLinks':json.loads((ROOT/'content/source/failures.json').read_text()),'notes':['All source HTML and extracted text retained in content/source.','Source project descriptions include copied text and one conflicting client name; retained as supplied, recorded for client review.','Demo team, pricing and testimonial text archived rather than promoted as verified company information.','New architectural images are concepts and are not used as completed project photography.']}
(ROOT/'content/migration-report.json').write_text(json.dumps(report,indent=2),encoding='utf8')
sheet=Image.new('RGB',(1200,900),'#eeeeee');draw=ImageDraw.Draw(sheet)
for i,p in enumerate(projects):
    img=Image.open(ROOT/'public'/p['images'][0].lstrip('/')).convert('RGB')
    sheet.paste(ImageOps.fit(img,(390,250)),((i%3)*400,(i//3)*300+30))
    draw.text(((i%3)*400+5,(i//3)*300+6),p['title'],fill='black')
sheet.save(ROOT/'content/project-contact-sheet.jpg')
print(json.dumps(report,indent=2)[:3000])
