"""Open office kitchens with counters outside entrance and landing circulation."""
from copy import deepcopy
from bed_furniture import door_hits_bed

AUDIT=[]

def normalize_rooms(d):
    if d['category']!='Workspace':return
    d['floors']=deepcopy(d['floors'])
    for rooms in d['floors']:
        for r in rooms:
            if r['kind']=='kitchen' or r['name']=='Entrance':
                r.update(name='Kitchen',group='Kitchen',kind='kitchen')
    if d['slug']=='single-cabin-office':
        # The original 4 x 4 entrance bay is too narrow for a 2 ft counter and
        # a 3 ft approach. Borrow 2 ft from the adjacent office, preserving area.
        d['floors'][0]=[
            dict(name='Kitchen',group='Kitchen',kind='kitchen',x=0,y=0,length=6,width=4),
            dict(name='Washroom',kind='bath',x=0,y=4,length=4,width=4),
            dict(name='Private office',group='Private office',kind='office',x=6,y=0,length=14,width=4,furnish=False,schedule="14' x 4' + 16' x 4'"),
            dict(name='Private office',group='Private office',kind='office',x=4,y=4,length=16,width=4)]
    if d['slug']=='two-cabin-office':
        # A counter across the old middle entrance bay would sever access to
        # one private office. Put the compact service bank at the outer end.
        d['floors'][0]=[
            dict(name='Kitchen',group='Kitchen',kind='kitchen',x=0,y=0,length=6,width=4),
            dict(name='Washroom',kind='bath',x=0,y=4,length=4,width=4),
            dict(name='Private office 1',group='Private office 1',kind='office',x=6,y=0,length=7,width=4,furnish=False,schedule="7' x 4' + 9' x 4'"),
            dict(name='Private office 1',group='Private office 1',kind='office',x=4,y=4,length=9,width=4),
            dict(name='Private office 2',kind='office',x=13,y=0,length=7,width=8)]

def counter(r):
    a,b,l,w=(r[k] for k in ('x','y','length','width'))
    # The field-office service bay is narrow but deep; use its rear wall.
    return (a,b+w-2,l,2) if l<5 else (a,b,2,w)

def openings(d,index,rooms,doors,edges):
    doors=deepcopy(doors);edges=deepcopy(edges)
    if d['category']!='Workspace':return doors,edges
    kitchens=[r for r in rooms if r['kind']=='kitchen']
    if d['slug']=='two-cabin-office':
        doors=[dict(x=4,y=4.4,vertical=True,sign=-1,size=2.5),
               dict(x=13,y=.5,vertical=True,sign=1,size=2.5),
               dict(x=8,y=0,vertical=False,sign=1,size=3)]
        edges=[dict(x=6,y=4,vertical=False,length=7)]
    for r in kitchens:
        a,b,l,w=(r[k] for k in ('x','y','length','width'))
        sides=[a+l]
        if d['slug']=='industrial-field-office':sides=[a]
        doors=[door for door in doors if not (door.get('vertical') and door['x'] in sides and b<=door['y']<b+w)]
        for side in sides:
            size=w-2 if d['slug']=='industrial-field-office' else w
            edges.append(dict(x=side,y=b,vertical=True,length=size))
    if index==1:
        # Landing and shared corridor are one continuous entrance route.
        doors=[door for door in doors if not (door.get('vertical') and door['x']==6 and door['y']<3)]
        edges.append(dict(x=6,y=0,vertical=True,length=3))
        for door in doors:
            if not door.get('vertical') and door['y']==0:door['x']=2.5
    if d['slug']=='single-cabin-office':
        edges.append(dict(x=6,y=4,vertical=False,length=14))
    counters=[]
    for r in kitchens:
        x,y,w,h=counter(r)
        fixture=dict(x=x,y=y,width=w,height=h)
        for door in doors:
            assert not door_hits_bed(door,fixture),(d['slug'],index,'door/counter collision',door,fixture)
        clear=r['length']-w if w==2 else r['width']-h
        assert clear>=3,(d['slug'],index,'kitchen approach too narrow',clear)
        counters.append(dict(room=r['name'],counterFeet=[x,y,w,h],clearApproachFeet=clear))
    AUDIT.append(dict(slug=d['slug'],floor=index,counters=counters,doors=doors,openEdges=edges,doorSwingsClearOfCounters=True))
    return doors,edges
