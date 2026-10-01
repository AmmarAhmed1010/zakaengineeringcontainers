import json, hashlib, re, concurrent.futures
from collections import defaultdict
from pathlib import Path
from urllib.parse import urlparse
import requests
root=Path(__file__).resolve().parents[1]
manifest=root/'content/source/assets.json'
assets=json.loads(manifest.read_text())
groups=defaultdict(list)
for a in assets:
    if 'local' in a:groups[a['local']].append(a)
jobs=[]
for local,group in groups.items():
    normalized={re.sub(r'(?<!:)//+','/',a['url']) for a in group}
    if len(normalized)<2:continue
    for a in group:
        p=Path(local)
        a['local']=str(p.with_name(p.stem+'-'+hashlib.sha1(a['url'].encode()).hexdigest()[:8]+p.suffix)).replace('\\','/')
        jobs.append(a)
def fetch(a):
    r=requests.get(a['url'],timeout=30);r.raise_for_status();p=root/'public'/a['local'].lstrip('/');p.write_bytes(r.content);a['bytes']=len(r.content)
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:list(pool.map(fetch,jobs))
manifest.write_text(json.dumps(assets,ensure_ascii=False,indent=2),encoding='utf8')
print('Resolved',len(jobs),'media URL filename collisions.')
