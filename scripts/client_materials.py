"""Preserve the complete client-supplied specification in readable flowing columns."""
import re
from xml.sax.saxutils import escape
from catalogue_style import *

SOURCE=ROOT/'content/specifications/client-standard-materials.txt'
CONTENT=SOURCE.read_text(encoding='utf-8').replace('\u2013','-').replace('\u2011','-').replace('\u00d7','x')
STARTS=list(re.finditer(r'^\d{2}\. .+$',CONTENT,re.M))
SECTIONS=[]
for i,match in enumerate(STARTS):
    end=STARTS[i+1].start() if i+1<len(STARTS) else CONTENT.index('QUALITY & CUSTOMIZATION')
    SECTIONS.append((match.group().strip(),CONTENT[match.end():end].strip()))
SECTIONS.append(('QUALITY & CUSTOMIZATION',CONTENT[CONTENT.index('QUALITY & CUSTOMIZATION')+len('QUALITY & CUSTOMIZATION'):].strip()))
assert len(SECTIONS)==21

def paragraphs(title,body):
    title_style=ParagraphStyle('material-title',fontName='Bold',fontSize=9.5,leading=13,textColor=RED,spaceAfter=6)
    body_style=ParagraphStyle('material-body',fontName='Body',fontSize=8.5,leading=11,textColor=NAVY)
    # Every field and qualifier is preserved. Soft wraps are introduced by the PDF renderer.
    lines=[escape(v.strip()) for v in body.splitlines() if v.strip()]
    return Paragraph(escape(title),title_style),Paragraph('<br/>'.join(lines),body_style)

def placement():
    placed=[];page=0;column=0;y=384;cw=365
    for title,body in SECTIONS:
        h1=paragraphs(title,body)[0].wrap(cw,1000)[1];h2=paragraphs(title,body)[1].wrap(cw,1000)[1];height=h1+6+h2+16
        if y-height<73:
            column+=1;y=384
            if column==2:column=0;page+=1
        assert y-height>=73,(title,height)
        placed.append((page,column,y,title,body,height));y-=height
    return placed,page+1

PLACED,MATERIAL_PAGES=placement()

def draw_materials(c,d,start):
    for i in range(MATERIAL_PAGES):
        header(c,d,start+i,'Standard material & technical specifications')
        heading(c,'04 / Client material standard','Materials. As specified by Zaka.',f'Complete client-supplied specification / part {i+1} of {MATERIAL_PAGES}. Selection and inclusion follow the approved quotation.')
        line(c,W/2,74,W/2,389,LINE,.6)
        for page,column,y,title,body,height in PLACED:
            if page!=i:continue
            xx=40+column*397;p1,p2=paragraphs(title,body);_,h1=p1.wrap(365,1000);p1.drawOn(c,xx,y-h1);_,h2=p2.wrap(365,1000);p2.drawOn(c,xx,y-h1-6-h2)
        c.showPage()
