"""Shared roof and corrugation rules for all thirty catalogue builders."""
import json
from pathlib import Path
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]
STYLES={r['slug']:r for r in json.loads((ROOT/'scripts/roof_style_revisions.json').read_text(encoding='utf-8'))}
LABELS={'flat':'Flat container roof','gable':'A-shaped gable roof','mono-pitch':'Single-slope roof'}
CLIENT_SLUGS={'duplex':'family-home-two-floors-40x24','residence':'two-bedroom-living-12x40-and-12x44','office':'executive-office-suite-12x40-and-12x44','studio':'studio-with-terrace-12x26'}

def finish_text(style):
    palette=style['palette'];terms={'flat':('flat roof','flat container'),'gable':('gable','a-shaped'),'mono-pitch':('single-slope','mono-pitch')}
    return palette if any(term in palette.lower() for term in terms[style['roof']]) else palette+'; '+LABELS[style['roof']].lower()

def apply_design(d):
    style=STYLES.get(d['slug'])
    if style:
        d.update(title=style['title'],finish=finish_text(style),roofSpecification=style['roofSpecification'],wallSpecification=style['wallSpecification'],roofStyle=LABELS[style['roof']])
    return d

def apply_config(cfg,slug=None):
    cfg=dict(cfg);slug=slug or cfg.get('slug') or CLIENT_SLUGS.get(cfg.get('type'))
    style=STYLES.get(slug)
    if style:
        cfg.update(roofSlug=slug,finish=style['palette']+' / '+LABELS[style['roof']],palette=style['palette']+'. Deep vertical corrugated steel / '+LABELS[style['roof']].lower()+'.',roofSpecification=style['roofSpecification'],wallSpecification=style['wallSpecification'],roofStyle=LABELS[style['roof']])
    return cfg

def image_path(slug):
    style=STYLES.get(slug)
    path=ROOT/'public'/style['image'].lstrip('/') if style else None
    return path if path and path.exists() else None

def draw_panel(c,slug,index,x,y,w,h):
    path=image_path(slug)
    if not path:raise FileNotFoundError('Missing revised exterior image for '+slug)
    with Image.open(path) as im:iw,ih=im.size
    pw,ph=iw/2,ih/2;inset=18 if slug=='ivory-meeting-office-24x32' else 4
    left=(index%2)*pw+inset;top=(index//2)*ph+inset;rw,rh=pw-2*inset,ph-2*inset
    scale=min(w/rw,h/rh);dx=x+(w-rw*scale)/2;dy=y+(h-rh*scale)/2
    c.saveState();clip=c.beginPath();clip.rect(dx,dy,rw*scale,rh*scale);c.clipPath(clip,stroke=0,fill=0)
    c.drawImage(str(path),dx-left*scale,dy-(ih-top-rh)*scale,iw*scale,ih*scale)
    c.restoreState()
