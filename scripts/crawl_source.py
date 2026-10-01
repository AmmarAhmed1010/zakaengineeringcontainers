"""Archive public site content and media for the redesign."""
import json, re, hashlib, concurrent.futures
from collections import Counter
from xml.etree import ElementTree as ET
from pathlib import Path
from urllib.parse import urljoin, urlparse, unquote
import requests
from bs4 import BeautifulSoup

BASE = 'https://zakaengineeringcontainers.com/'
ROOT = Path(__file__).resolve().parents[1]
ARCHIVE = ROOT / 'content/source'
ASSETS = ROOT / 'public/images/original'
ARCHIVE.mkdir(parents=True, exist_ok=True)
ASSETS.mkdir(parents=True, exist_ok=True)
session = requests.Session()
session.headers['User-Agent'] = 'Mozilla/5.0 (Website content migration)'
pages, failures, media, endpoints = [], [], set(), []
queue, seen = [BASE], set()

def get(url):
    r = session.get(url, timeout=40)
    r.raise_for_status()
    return r

# Discover all public sitemap URLs as well as navigation links.
for sitemap in ['wp-sitemap.xml', 'sitemap_index.xml', 'sitemap.xml']:
    try:
        xml = ET.fromstring(get(urljoin(BASE,sitemap)).content)
        for loc in [n.text for n in xml.iter() if n.tag.endswith('}loc') or n.tag=='loc']:
            if loc.endswith('.xml'):
                try:
                    nested = ET.fromstring(get(loc).content)
                    queue += [n.text for n in nested.iter() if n.tag.endswith('}loc') or n.tag=='loc']
                except Exception as e: failures.append({'url':loc,'error':str(e)})
            else: queue.append(loc)
    except Exception: pass

while queue:
    url = queue.pop(0).split('#')[0].split('?')[0]
    if url in seen or urlparse(url).netloc != urlparse(BASE).netloc: continue
    if re.search(r'\.(jpg|png|webp|svg|pdf|gif|xml|zip)$',url,re.I):
        media.add(url); continue
    seen.add(url)
    try:
        r = get(url)
        if 'html' not in r.headers.get('Content-Type',''): continue
        soup = BeautifulSoup(r.text,'html.parser')
        slug = urlparse(url).path.strip('/') or 'home'
        safe = slug.replace('/','__')
        (ARCHIVE / (safe+'.html')).write_text(r.text,encoding='utf-8')
        images=[]
        for img in soup.find_all('img'):
            for attr in ['src','data-src','data-lazy-src']:
                if img.get(attr) and not img[attr].startswith('data:'):
                    u=urljoin(url,img[attr]); media.add(u); images.append({'url':u,'alt':img.get('alt','')})
            for attr in ['srcset','data-srcset']:
                for candidate in img.get(attr,'').split(','):
                    if candidate.strip(): media.add(urljoin(url,candidate.strip().split()[0]))
        for match in re.findall(r'url\([\"\']?([^\)\"\']+)',r.text):
            if not match.startswith('data:'): media.add(urljoin(url,match))
        links=[]
        for a in soup.find_all('a',href=True):
            u=urljoin(url,a['href']); links.append({'text':a.get_text(' ',strip=True),'url':u})
            if urlparse(u).netloc==urlparse(BASE).netloc:
                if '/wp-content/uploads/' in u: media.add(u)
                elif not any(x in u for x in ['/wp-json/','/feed/','wp-login','wp-admin','replytocom']): queue.append(u)
        for tag in soup(['script','style','noscript']): tag.decompose()
        text=soup.get_text('\n',strip=True)
        (ARCHIVE / (safe+'.txt')).write_text(text,encoding='utf-8')
        content=soup.find('main') or soup.find(class_='site-main') or soup.body
        pages.append({'url':url,'slug':slug,'title':soup.title.get_text(strip=True) if soup.title else slug,'text':text,'mainText':content.get_text('\n',strip=True) if content else text,'images':images,'links':links})
        print('PAGE',slug, len(images),flush=True)
    except Exception as e: failures.append({'url':url,'error':str(e)})

# The WordPress media index includes original files beyond displayed thumbnails.
try:
    for page in range(1,20):
        r=session.get(BASE+'wp-json/wp/v2/media',params={'per_page':100,'page':page},timeout=40)
        if r.status_code!=200: break
        data=r.json()
        (ARCHIVE / f'wp-media-{page}.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
        for item in data:
            media.add(item['source_url'])
            for size in item.get('media_details',{}).get('sizes',{}).values():
                if size.get('source_url'): media.add(size['source_url'])
        if len(data)<100: break
except Exception as e: failures.append({'url':'wp-json/media','error':str(e)})

media={re.sub(r'(?<!:)//+','/',u) for u in media}
name_counts=Counter(Path(urlparse(u).path).name for u in media)

def download(u):
    try:
        parsed=urlparse(u)
        name=unquote(Path(parsed.path).name)
        if not name or len(name)>170: name=hashlib.sha1(u.encode()).hexdigest()+'.bin'
        name=re.sub(r'[^a-zA-Z0-9_.-]','-',name)
        if name_counts[Path(parsed.path).name]>1:
            p=Path(name);name=p.stem+'-'+hashlib.sha1(u.encode()).hexdigest()[:8]+p.suffix
        target=ASSETS/name
        r=requests.get(u,timeout=45)
        r.raise_for_status()
        target.write_bytes(r.content)
        return {'url':u,'local':'/images/original/'+name,'bytes':len(r.content),'type':r.headers.get('Content-Type','')}
    except Exception as e: return {'url':u,'error':str(e)}

with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
    assets=list(pool.map(download,sorted(media)))
(ARCHIVE/'pages.json').write_text(json.dumps(pages,ensure_ascii=False,indent=2),encoding='utf-8')
(ARCHIVE/'assets.json').write_text(json.dumps(assets,ensure_ascii=False,indent=2),encoding='utf-8')
(ARCHIVE/'failures.json').write_text(json.dumps(failures,indent=2),encoding='utf-8')
print(json.dumps({'pages':len(pages),'assets':len(assets),'failures':failures,'downloadFailures':[a for a in assets if 'error' in a]},indent=2))
