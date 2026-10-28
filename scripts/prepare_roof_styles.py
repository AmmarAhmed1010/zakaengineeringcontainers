"""Record one exterior/roof specification per website catalogue."""
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
TITLES={'portable-12x20':'Compact Container Studio','single-cabin-office':'Compact Container Office'}
FILES={'portable-12x20':'compact-container-studio-12x20.pdf','single-cabin-office':'compact-container-office-8x20.pdf'}
DETAILS=[
('studio-12x30',12,30,'flat','Sand-brown corrugated steel, cedar entrance trim, graphite rails, black frames'),
('studio-12x21-terrace',12,21,'flat','Sage corrugated steel, white frames, charcoal rails and cedar pergola'),
('portable-12x40',12,40,'flat','Charcoal corrugated steel, white fascia, timber entrance recess, black frames'),
('portable-12x45',12,45,'flat','Ivory corrugated steel on two fully enclosed stacked floors, charcoal rails, timber entrance accents'),
('portable-12x24',12,24,'flat','White corrugated steel on two fully enclosed stacked floors, black frames and charcoal rails'),
('portable-12x20',12,20,'flat','Cream corrugated steel, brick-red perimeter rails and black windows'),
('office-8x20',8,20,'flat','Mint-green corrugated steel, white frames and dark grey horizontal roof rails'),
('office-10x20',10,20,'flat','Cedar-brown painted corrugated steel, graphite rails and tall black front glazing'),
('office-12x20',12,20,'flat','White corrugated steel, burgundy entrance portal and broad black-framed glazing'),
('office-8x40',8,40,'flat','Olive corrugated steel, black flat entrance canopy and linear windows'),
('office-10x40',10,40,'flat','Navy lower and white upper corrugated steel, black frames, two full enclosed floors'),
('office-12x40',12,40,'flat','Charcoal corrugated steel, grey and white trim, black frames, two full enclosed floors'),
('single-cabin-office',8,20,'flat','Powder-blue corrugated steel, white trim and window frames'),
('two-cabin-office',8,20,'flat','Mustard corrugated steel, graphite horizontal roof rails and two office windows'),
('industrial-field-office',8,20,'flat','Forest-green heavy corrugated steel, protected black windows and low-mounted rooftop solar'),
('two-bedroom-residence',16,40,'mono-pitch','Cream corrugated steel, cedar entry trim and terracotta single-slope metal roof'),
('compact-container-home',24,40,'mono-pitch','Charcoal corrugated steel, sand-coloured steel trim and charcoal roof frames'),
('family-home-two-floors-40x24',24,40,'mono-pitch','Grey corrugated steel, charcoal frames and white soffits'),
('two-bedroom-living-12x40-and-12x44',12,44,'flat','Charcoal corrugated steel, white frames and grey horizontal roof rails'),
('executive-office-suite-12x40-and-12x44',12,44,'flat','White corrugated steel, charcoal frames and grey accents'),
('studio-with-terrace-12x26',12,21,'flat','Warm-grey corrugated steel, white fascia and charcoal frame'),
('courtyard-cafe-12x40',12,40,'flat','Charcoal corrugated steel, ivory trim, black glazing and flat cedar entrance canopy'),
('cedar-bistro-24x40',24,40,'gable','Ivory corrugated steel, cedar entrance trim and charcoal A-shaped gable metal roof over joined modules'),
('charcoal-takeaway-12x20',12,20,'flat','Charcoal corrugated steel, white horizontal roof fascia and grey trim; preserve serving hatch'),
('slate-team-office-12x32',12,32,'flat','Silver-grey corrugated steel, charcoal frames and white horizontal roof fascia'),
('ivory-meeting-office-24x32',24,32,'mono-pitch','Ivory corrugated steel, charcoal frames and white fascia under a visible single-slope metal roof'),
('silver-one-bedroom-home-12x32',12,32,'flat','Light-grey corrugated steel, white fascia and charcoal window frames'),
('charcoal-two-bedroom-home-24x32',24,32,'gable','Charcoal corrugated steel, ivory frames and a grey A-shaped gable metal roof'),
('ivory-portable-clinic-12x40',12,40,'flat','White corrugated steel, charcoal frames and light-grey horizontal roof rails'),
('grey-learning-studio-12x40',12,40,'flat','Warm-grey corrugated steel, white fascia and charcoal frames'),
]

def main():
    docs=json.loads((ROOT/'src/data/documents.json').read_text(encoding='utf-8'))
    by_slug={d['slug']:d for d in docs};items=[]
    client_sources=['family','residence','office','studio']
    for index,(slug,width,length,roof,palette) in enumerate(DETAILS):
        doc=by_slug[slug]
        if index<17:source='public'+doc['image']
        elif index<21:source='public/images/generated/client-revision-04/'+client_sources[index-17]+'.png'
        else:source='public/images/generated/collection-30/'+slug+'.png'
        roof_spec={'flat':'Flat container-style corrugated steel roof with level perimeter rails; concealed drainage falls coordinated during detailing.',
                   'gable':'A-shaped gable steel roof over the joined 24 ft width, with corrugated metal roof sheets and coordinated ridge/drainage.',
                   'mono-pitch':'Single-slope steel roof with corrugated metal sheets; supports and drainage coordinated for the joined building.'}[roof]
        if slug=='compact-container-home':roof_spec+=' Sloping roofs cover occupied U-shaped wings only; the central courtyard stays open to sky.'
        if slug=='family-home-two-floors-40x24':roof_spec+=' A single-slope canopy spans the upper container and open-sided front terrace; the upper enclosed module remains 12 ft wide.'
        items.append(dict(slug=slug,title=TITLES.get(slug,doc['title']),file=FILES.get(slug,doc['file'].split('/')[-1]),widthFeet=width,lengthFeet=length,storeys=doc['storeys'],roof=roof,roofSpecification=roof_spec,palette=palette,wallSpecification='Deep vertical shipping-container-style corrugated steel cladding with visible steel corner posts and top/bottom perimeter rails.',sourceImage=source,image='/images/catalogues/roof-revision/'+slug+'.jpg'))
    assert len(items)==30
    (ROOT/'scripts/roof_style_revisions.json').write_text(json.dumps(items,indent=2)+'\n',encoding='utf-8')
    print('Prepared 30 roof and corrugation specifications.')

if __name__=='__main__':main()
