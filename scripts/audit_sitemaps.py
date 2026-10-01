import requests,xml.etree.ElementTree as ET,json
from pathlib import Path
root=Path(__file__).resolve().parents[1]
base='https://zakaengineeringcontainers.com/'
session=requests.Session();urls=[];errors=[];seen=set()
queue=[base+'wp-sitemap.xml',base+'sitemap_index.xml',base+'sitemap.xml']
while queue:
    u=queue.pop(0)
    if u in seen:continue
    seen.add(u)
    try:
        r=session.get(u,timeout=25);r.raise_for_status();xml=ET.fromstring(r.content)
        locs=[n.text for n in xml.iter() if n.tag.endswith('}loc') or n.tag=='loc']
        print(u,len(locs),flush=True)
        queue.extend(l for l in locs if l.endswith('.xml'))
        urls.extend(l for l in locs if not l.endswith('.xml'))
    except Exception as e:errors.append({'url':u,'error':str(e)})
existing={p['url'].rstrip('/') for p in json.loads((root/'content/source/pages.json').read_text(encoding='utf8'))}
missing=[u for u in urls if u.rstrip('/') not in existing]
report={'urls':urls,'uncaptured':missing,'errors':errors}
(root/'content/source/sitemap-audit.json').write_text(json.dumps(report,indent=2))
print(json.dumps({'uncaptured':missing,'errors':errors},indent=2))
