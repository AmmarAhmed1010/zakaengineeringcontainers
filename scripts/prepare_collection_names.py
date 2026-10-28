"""One-time migration: remove brand/client prefixes while preserving old links."""
import json
import re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

def main():
    docs=json.loads((ROOT/'src/data/documents.json').read_text(encoding='utf-8'))
    mapping={}
    for doc in docs:
        old=Path(doc['file']).name
        if not old.startswith('zaka-'):continue
        title=re.sub(r'[^a-z0-9]+','-',doc['title'].lower()).strip('-')
        dims=re.search(r'(\d+)[^\d]+(\d+)',doc['subtitle'])
        suffix=f'-{dims[1]}x{dims[2]}' if dims else ''
        mapping[old]=title+suffix+'.pdf'
    mapping.update({
        'zaka-client-01-family-home-two-floors.pdf':'family-home-two-floors-40x24.pdf',
        'zaka-client-02-two-bedroom-12x40-and-12x44.pdf':'two-bedroom-living-12x40-and-12x44.pdf',
        'zaka-client-03-office-12x40-and-12x44.pdf':'executive-office-suite-12x40-and-12x44.pdf',
        'zaka-client-04-studio-12x26-with-terrace.pdf':'studio-with-terrace-12x26.pdf'})
    target=ROOT/'src/data/catalogue-filenames.json'
    if target.exists():mapping={**json.loads(target.read_text(encoding='utf-8')),**mapping}
    target.write_text(json.dumps(mapping,indent=2)+'\n',encoding='utf-8')
    for folder in ('output/pdf','public/downloads'):
        for old,new in mapping.items():
            source=ROOT/folder/old;dest=ROOT/folder/new
            if source.exists():
                if dest.exists():raise RuntimeError('Refusing to overwrite '+str(dest))
                source.rename(dest)
    for file in [ROOT/'src/data/documents.json',*list((ROOT/'output/pdf').glob('*.json'))]:
        contents=file.read_text(encoding='utf-8')
        for old,new in mapping.items():contents=contents.replace(old,new)
        file.write_text(contents,encoding='utf-8')
    print('Readable names applied to',len(mapping),'catalogues.')

if __name__=='__main__':main()
