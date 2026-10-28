"""Client-marked layouts: explicit openings, continuous living zones and end stairs."""
from catalogue_style import *
from bed_furniture import draw_bed, default_bed, audit_beds
from office_kitchens import openings as kitchen_openings, counter as kitchen_counter

REVISIONS=json.loads((ROOT/'scripts/client_plan_revisions.json').read_text())

def groups(rs):
    result={}
    for r in rs:
        key=r.get('group',r['name'])
        if key not in result:result[key]={'name':key,'area':0,'rooms':[],'dimensions':r.get('schedule',f"{r['length']}' x {r['width']}'")}
        result[key]['area']+=r['length']*r['width'];result[key]['rooms'].append(r)
    return list(result.values())

def default_openings(d,rs,index):
    doors=[];opens=[];slug=d['slug'];w=d['width']
    for r in rs:
        a,b,ll,ww,kind=(r[k] for k in ('x','y','length','width','kind'))
        entry=dict(x=a+.6,y=b,vertical=False,sign=1,size=2.5)
        if kind=='bath':
            if index==1 or slug=='two-cabin-office':doors.append(entry)
            elif slug=='compact-container-home':doors.append(dict(x=a,y=b+3,vertical=True,sign=1,size=2.5))
            else:doors.append(dict(x=a+ll,y=b+.4,vertical=True,sign=-1,size=2.5))
        elif kind in ('kitchen','landing'):
            if slug=='compact-container-home':doors.append(dict(x=a,y=b+3,vertical=True,sign=1,size=2.5))
            elif slug!='industrial-field-office':doors.append(dict(x=a+ll,y=b+.3,vertical=True,sign=-1,size=min(2.5,ww-.6)))
        elif kind=='bed':
            if slug=='compact-container-home':doors.append(dict(x=a+ll if a==0 else a,y=b+1,vertical=True,sign=-1 if a==0 else 1,size=3))
            else:doors.append(entry)
        elif kind=='office' and index==1:doors.append(entry)
        elif kind=='office' and slug in ('two-cabin-office','industrial-field-office'):
            if a>0 or slug=='two-cabin-office':doors.append(dict(x=a if a else a+ll,y=b+.3,vertical=True,sign=1 if a else -1,size=2.5))
        elif kind=='hall':doors.append(dict(x=a,y=b+.2,vertical=True,sign=1,size=2.5))
    if slug=='compact-container-home':doors.append(dict(x=18,y=12,vertical=False,sign=1,size=3))
    else:doors.append(dict(x=8.5 if slug=='two-cabin-office' else .6 if index else 8,y=0,vertical=False,sign=1,size=3))
    return doors,opens

def draw_plan(c,d,index,page,roof=False):
    rs=d['floors'][index];g=groups(rs);l,w=d['length'],d['width'];slug=d['slug']
    detail=REVISIONS.get(slug,{}).get('floors',[])
    detail=detail[index] if detail else {}
    doors,opens=(detail['doors'],detail.get('openEdges',[])) if detail else default_openings(d,rs,index)
    doors,opens=kitchen_openings(d,index,rs,doors,opens)
    stairs=d['storeys']==2;balcony=stairs and index==1
    name='Ground floor' if index==0 else 'First floor'
    header(c,d,page,name+' / measurements in feet')
    heading(c,'01 / Client layout revision',name+'. Planned around your brief.','Nominal feet, before wall deductions. Numbered spaces correspond to the room schedule below.')
    total=l+d.get('terrace',0)+(5 if stairs else 0);depth=max(w,16 if stairs else w)+(3 if balcony else 0)
    s=min(630/total,200/depth);x=(W-total*s)/2;y=(193 if stairs else 177)+(3*s if balcony else 0)
    palette={'bed':'#e4dacb','wardrobe':'#e4dacb','bath':'#dce8eb','kitchen':'#ece2d2','office':'#e0e6de','hall':'#faf9f6','landing':'#f0ece4','studio':'#e9dfd0','living':'#efede7'}
    def bx(a,b,ll,ww,fill,stroke=NAVY):
        c.setLineWidth(.65);rect(c,x+a*s,y+b*s,ll*s,ww*s,HexColor(fill),stroke)
    def opening(o):
        xx,yy=x+o['x']*s,y+o['y']*s;r=o['size']*s;v=o.get('vertical',False);sign=o.get('sign',1)
        dx,dy=(0,r) if v else (r,0);ex,ey=(sign*r,0) if v else (0,sign*r)
        line(c,xx,yy,xx+dx,yy+dy,PAPER,3.5);line(c,xx,yy,xx+ex,yy+ey,RED,.75)
        c.setStrokeColor(RED);c.setLineWidth(.5);p=c.beginPath();p.moveTo(xx+dx,yy+dy)
        k=.5522848;p.curveTo(xx+dx+k*ex,yy+dy+k*ey,xx+ex+k*dx,yy+ey+k*dy,xx+ex,yy+ey);c.drawPath(p)
    if slug=='compact-container-home':
        bx(10,0,20,12,'#dedaca',None);text(c,x+12*s,y+5*s,'OPEN COURTYARD',8,'Bold',RED);text(c,x+12*s,y+5*s-12,"20' x 12' / 240 sq ft",7)
    for r in rs:bx(r['x'],r['y'],r['length'],r['width'],palette[r['kind']])
    # Adjacent rectangles in the same group form one continuous L-shaped space.
    for o in opens:
        a,b=o['x'],o['y'];v=o.get('vertical',False);ll=o['length']
        line(c,x+a*s,y+b*s,x+(a if v else a+ll)*s,y+(b+ll if v else b)*s,HexColor('#efede7'),3)
    beds=[]
    for r in rs:
        a,b,ll,ww,kind=(r[k] for k in ('x','y','length','width','kind'))
        if kind in ('bed','studio') and ll>=7 and ww>=8:
            bed=default_bed(r);beds.append(bed)
            draw_bed(c,bed['x'],bed['y'],bed['width'],bed['height'],bed['head'],s,(x,y))
        elif kind=='wardrobe':bx(a+.2,b+.2,ll-.4,1.5,'#cabba7',MUTED)
        elif kind=='office' and r.get('furnish',True):
            for xx in range(1,int(ll)-3,7):bx(a+xx,b+ww-2.2,3.5,1.5,'#cabba7',MUTED)
        elif kind=='kitchen':
            if d['category']=='Workspace':
                ca,cb,cl,cw=kitchen_counter(r);bx(ca,cb,cl,cw,'#cabba7',MUTED)
                vertical=cl==2
                bx(ca+.35,cb+.2 if vertical else cb+.4,1.2,1.1,'#faf9f6',MUTED)
                hx,hy=(ca+.35,cb+cw-1.3) if vertical else (ca+cl-1.55,cb+.4)
                bx(hx,hy,1.2,1.1,'#626a72',MUTED)
                c.setStrokeColor(PAPER);c.setLineWidth(.5)
                for offset in (.3,.9):c.circle(x+(hx+offset)*s,y+(hy+.55)*s,.18*s,stroke=1,fill=0)
            else:
                bx(a+.4,b+ww-1.8,max(1,ll-.8),1.4,'#cabba7',MUTED)
                bx(a+.7,b+ww-1.5,.9,.8,'#faf9f6',MUTED)
        elif kind=='living' and ll>=6 and ww>=6:
            bx(a+1,b+ww-2.5,min(4,ll-2),1.7,'#cabba7',MUTED)
        elif kind=='bath':
            c.setFillColor(PAPER);c.setStrokeColor(MUTED);c.ellipse(x+(a+.6)*s,y+(b+ww-2.7)*s,x+(a+1.7)*s,y+(b+ww-1.1)*s,fill=1,stroke=1)
            bx(a+ll-1.5,b+ww-1.4,1.1,.8,'#faf9f6',MUTED)
    for i,zone in enumerate(g):
        main=max(zone['rooms'],key=lambda r:r['length']*r['width']);a,b,ll,ww=(main[k] for k in ('x','y','length','width'))
        rect(c,x+(a+.2)*s,y+(b+ww)*s-13,11,10,NAVY);text(c,x+(a+.2)*s+3,y+(b+ww)*s-10,str(i+1),7,'Bold',PAPER)
        label=zone['name'];size=7.5;natural=pdfmetrics.stringWidth(label,'Bold',size)
        size=max(6.2,min(size,size*(ll*s-8)/max(1,natural)))
        if pdfmetrics.stringWidth(label,'Bold',size)>ll*s-4:
            label='Kitchen' if 'Kitchen' in label else label.split(' / ')[0]
            size=min(size,(ll*s-8)/pdfmetrics.stringWidth(label,'Bold',1))
        tw=pdfmetrics.stringWidth(label,'Bold',size);cx=x+(a+ll*.45)*s;cy=y+(b+ww*.36)*s
        if main['kind'] in ('bed','studio'):cx=x+(a+ll*.5)*s;cy=y+(b+ww-1.5)*s
        rect(c,cx-tw/2-3,cy-3,tw+6,12,PAPER);text(c,cx-tw/2,cy,label,size,'Bold')
    if d.get('terrace'):
        bx(l,0,5,w,'#dedaca');text(c,x+(l+.6)*s,y+5*s,'TERRACE',7,'Bold')
        dim(c,x+l*s,y+w*s+18,x+(l+5)*s,y+w*s+18,"5' terrace")
    if 'windows' in detail:
        for window in detail['windows']:
            a,b,size=window['x'],window['y'],window['size'];vertical=window.get('vertical',False)
            xx,yy=x+a*s,y+b*s;dx,dy=(0,size*s) if vertical else (size*s,0)
            line(c,xx,yy,xx+dx,yy+dy,PAPER,4)
            line(c,xx,yy,xx+dx,yy+dy,HexColor('#57879a'),2.5)
            label=f"{window['tag']}  {size:g}' x {window['height']:g}'"
            c.saveState()
            if vertical:
                c.translate(xx+(-8 if a==0 else 11),yy+dy/2);c.rotate(90)
                text(c,-pdfmetrics.stringWidth(label,'Body',6.5)/2,0,label,6.5,'Body',HexColor('#3d6a7e'))
            else:
                tx=xx+dx/2-pdfmetrics.stringWidth(label,'Body',6.5)/2
                text(c,tx,yy+8 if b==w else yy-13,label,6.5,'Body',HexColor('#3d6a7e'))
            c.restoreState()
    else:
        for r in rs:
            if r['kind'] not in ('bed','office','studio','living'):continue
            if r['y']+r['width']==w:line(c,x+(r['x']+1)*s,y+w*s,x+(r['x']+min(r['length']-1,4))*s,y+w*s,HexColor('#57879a'),3)
    if stairs:
        start=-3 if balcony else 0
        bx(l+.5,start,4,16,'#e0e6de',MUTED)
        for t in range(1,16):line(c,x+(l+.5)*s,y+(start+t)*s,x+(l+4.5)*s,y+(start+t)*s,MUTED,.5)
        c.saveState();c.translate(x+(l+2.8)*s,y+(start+8)*s);c.rotate(90);text(c,-35,0,'EXTERNAL STAIR',6,'Bold',RED);c.restoreState()
        dim(c,x+(l+4.5)*s+15,y+start*s,x+(l+4.5)*s+15,y+(start+16)*s,"16' stair allowance")
        dim(c,x+(l+.5)*s,y+start*s-12,x+(l+4.5)*s,y+start*s-12,"4'")
        if balcony:
            bx(0,-3,l,3,'#e0e6de',MUTED);text(c,x+2*s,y-2*s,"UPPER ACCESS BALCONY / 3' DEEP",7,'Bold',RED)
            bx(l,-3,.5,3,'#e0e6de',MUTED)
            line(c,x+l*s,y-3*s,x+l*s,y,HexColor('#e0e6de'),3)
    for o in doors:opening(o)
    windows=detail.get('windows',[dict(x=r['x']+1,y=w,size=min(r['length']-1,4)-1,vertical=False) for r in rs if r['kind'] in ('bed','office','studio','living') and r['y']+r['width']==w])
    obstacles=[(r['x'],r['y'],r['length'],r['width']) for r in rs if r['kind'] in ('bath','kitchen','wardrobe')]
    audit_beds(beds,windows,doors,obstacles,f"{slug} / floor {index}")
    dim(c,x,y+w*s+20,x+l*s,y+w*s+20,f"{l}' building length")
    dim(c,x-23,y,x-23,y+w*s,f"{w}' building width")
    note=detail.get('note','Blue: glazing. Red arcs: indicative doors. All final openings and clearances are developed for the approved layout.')
    if d['category']=='Workspace':
        note=note.replace('Kitchen replaces entry/pantry.','Open kitchen with outer-wall counters and unobstructed entry.')
        note+=' Kitchen counters include a sink and hob. Open sides keep entrance, landing and corridor routes clear.'
    if stairs:para(c,40,160,"RIGHT-END STAIR: 4' x 16' outside footprint. Upper front access balcony: 3' deep, additional outdoor area. Stair geometry to be engineered.",W-80,7,RED,10)
    text(c,40,139,'ROOM SCHEDULE / DIMENSIONS IN FEET',8,'Bold',RED)
    for i,zone in enumerate(g):
        xx=40+(i%3)*257;yy=118-(i//3)*28
        text(c,xx,yy,f"{i+1:02d}  {zone['name']}",8,'Bold');para(c,xx,yy-5,f"{zone['dimensions']} / {zone['area']} sq ft",245,7.5,MUTED,10)
    if d.get('terrace'):note+=' Additional terrace: 60 sq ft; total ground footprint 12 x 26 ft.'
    para(c,40,65,note,W-80,7,MUTED,9);c.showPage()
