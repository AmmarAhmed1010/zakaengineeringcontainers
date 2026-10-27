"""Shared bed symbols and geometric checks for usable sleeping layouts."""
from reportlab.lib.colors import HexColor

AUDIT=[]

def draw_bed(c,x,y,width,height,head,scale,origin):
    """Coordinates are nominal feet. A double bed is 5 x 6.5 ft."""
    ox,oy=origin
    def box(a,b,w,h,fill,stroke='#777A76',lw=.45):
        c.setFillColor(HexColor(fill));c.setStrokeColor(HexColor(stroke));c.setLineWidth(lw)
        c.rect(ox+a*scale,oy+b*scale,w*scale,h*scale,stroke=1,fill=1)
    box(x,y,width,height,'#D2CEC6')
    if head in ('north','south'):
        hy=y+height-.18 if head=='north' else y
        py=y+height-1.2 if head=='north' else y+.3
        box(x,hy,width,.18,'#687472')
        for px in (x+.25,x+width/2+.1):box(px,py,width/2-.35,.85,'#FAF9F6',lw=.3)
        fold=y+1.6 if head=='north' else y+height-1.6
        c.line(ox+x*scale,oy+fold*scale,ox+(x+width)*scale,oy+fold*scale)
    else:
        hx=x+width-.18 if head=='east' else x
        px=x+width-1.2 if head=='east' else x+.3
        box(hx,y,.18,height,'#687472')
        for py in (y+.25,y+height/2+.1):box(px,py,.85,height/2-.35,'#FAF9F6',lw=.3)
        fold=x+1.6 if head=='east' else x+width-1.6
        c.line(ox+fold*scale,oy+y*scale,ox+fold*scale,oy+(y+height)*scale)

def default_bed(room):
    a,b,l,w=(room[k] for k in ('x','y','length','width'))
    if room['kind']=='studio':
        return dict(x=a+6,y=b,width=5,height=6.5,head='south',room=(a,b,l,w),name=room['name'])
    head='west' if a==0 else 'east'
    return dict(x=a if head=='west' else a+l-6.5,y=b+(w-5)/2,width=6.5,height=5,
                head=head,room=(a,b,l,w),name=room['name'])

def overlap(a,b):
    return min(a[0]+a[2],b[0]+b[2])-max(a[0],b[0])>1e-5 and min(a[1]+a[3],b[1]+b[3])-max(a[1],b[1])>1e-5

def door_hits_bed(door,bed):
    radius=door.get('size',door.get('width',3));hx,hy=door['x'],door['y']
    vertical=door.get('vertical',False);reverse=door.get('reverse',False)
    if reverse:
        if vertical:hy+=radius
        else:hx+=radius
    sx=door.get('sign',1) if vertical else (-1 if reverse else 1)
    sy=(-1 if reverse else 1) if vertical else door.get('sign',1)
    x,y,w,h=(bed[k] for k in ('x','y','width','height'))
    xx=sorted(((x-hx)*sx,(x+w-hx)*sx));yy=sorted(((y-hy)*sy,(y+h-hy)*sy))
    if xx[1]<=1e-5 or yy[1]<=1e-5:return False
    return max(0,xx[0])**2+max(0,yy[0])**2 < (radius-1e-4)**2

def audit_beds(beds,windows,doors,obstacles,context):
    for bed in beds:
        x,y,w,h=(bed[k] for k in ('x','y','width','height'));rx,ry,rw,rh=bed['room'];head=bed['head']
        assert x>=rx-1e-5 and y>=ry-1e-5 and x+w<=rx+rw+1e-5 and y+h<=ry+rh+1e-5,(context,'bed outside room',bed)
        edge={'west':x-rx,'east':rx+rw-x-w,'north':ry+rh-y-h,'south':y-ry}[head]
        assert abs(edge)<.02,(context,'headboard not on wall',bed)
        if head in ('east','west'):clear=[y-ry,ry+rh-y-h,x-rx if head=='east' else rx+rw-x-w]
        else:clear=[x-rx,rx+rw-x-w,y-ry if head=='north' else ry+rh-y-h]
        for obstacle in obstacles:
            if not overlap(obstacle,(rx,ry,rw,rh)):continue
            assert not overlap((x,y,w,h),obstacle),(context,'bed collides with fixture',bed,obstacle)
            a,b,l,d=obstacle
            if head in ('east','west'):
                if min(x+w,a+l)>max(x,a):
                    if b+d<=y:clear[0]=min(clear[0],y-b-d)
                    if b>=y+h:clear[1]=min(clear[1],b-y-h)
                if min(y+h,b+d)>max(y,b):
                    if head=='east' and a+l<=x:clear[2]=min(clear[2],x-a-l)
                    if head=='west' and a>=x+w:clear[2]=min(clear[2],a-x-w)
            else:
                if min(y+h,b+d)>max(y,b):
                    if a+l<=x:clear[0]=min(clear[0],x-a-l)
                    if a>=x+w:clear[1]=min(clear[1],a-x-w)
                if min(x+w,a+l)>max(x,a):
                    if head=='north' and b+d<=y:clear[2]=min(clear[2],y-b-d)
                    if head=='south' and b>=y+h:clear[2]=min(clear[2],b-y-h)
        assert min(clear)>=2.5-1e-5,(context,'insufficient bedside/foot access',clear,bed)
        for window in windows:
            a,b,size=window['x'],window['y'],window['size'];vertical=window.get('vertical',False)
            if head in ('east','west') and vertical:
                hx=x+w if head=='east' else x
                assert abs(hx-a)>.02 or min(y+h,b+size)<=max(y,b),(context,'headboard under window',bed)
            elif head in ('north','south') and not vertical:
                hy=y+h if head=='north' else y
                assert abs(hy-b)>.02 or min(x+w,a+size)<=max(x,a),(context,'headboard under window',bed)
        for door in doors:assert not door_hits_bed(door,bed),(context,'bed intersects door swing',bed,door)
        AUDIT.append(dict(context=context,**bed,sideClearancesFeet=clear[:2],footClearanceFeet=clear[2],headboardOnSolidWall=True))
