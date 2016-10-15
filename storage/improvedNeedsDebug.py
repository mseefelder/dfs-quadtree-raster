#def ptInTri(p, p0, p1, p2):
#    A = 1/2 * (-p1[1] * p2[0] + p0[1] * (-p1[0] + p2[0]) + p0[0] * (p1[1] - p2[1]) + p1[0] * p2[1])
#    sign =  -1 if (A < 0) else 1
#    s = (p0[1] * p2[0] - p0[0] * p2[1] + (p2[1] - p0[1]) * p[0] + (p0[0] - p2[0]) * p[1]) * sign
#    t = (p0[0] * p1[1] - p0[1] * p1[0] + (p0[1] - p1[1]) * p[0] + (p1[0] - p0[0]) * p[1]) * sign
#    
#    return s > 0 and t > 0 and (s + t) < 2 * A * sign;

def sign (p1, p2, p3):
    return (p1[0] - p3[0]) * (p2[1] - p3[1]) - (p2[0] - p3[0]) * (p1[1] - p3[1])

def ptInTri(p, p0, p1, p2):

    b1 = sign(p, p0, p1) < 0.0
    b2 = sign(p, p1, p2) < 0.0
    b3 = sign(p, p2, p0) < 0.0

    return ((b1 == b2) and (b2 == b3))

def ptInSq(p, p0, p1, p2, p3):
    return ptInTri(p, p0, p1, p2) or ptInTri(p, p0, p2, p3)

def vecLen(vec):
    result = 0
    for i in vec:
        result += i**2
    return sqrt(result)

def rotVec(v, a):
    c = cos(a)
    s = sin(a)
    return ( (c*v[0])-(s*v[1]), (s*v[0])+(c*v[1]) )

def angleDir(u, v):
    #angle from u to v
    return atan2(v[1], v[0]) - atan2(u[1], u[0])

def dist2(u, v):
    return (u[0]-v[0])*(u[0]-v[0])+(u[1]-v[1])*(u[1]-v[1])

def shadeCalc(o, p, r, a, ul, ur, bigAngle):
    l = dist2(o, p)
    theta = acos( 1-( (r*r)/(2*l) ) )
    pl = rotVec(p, theta)
    pr = rotVec(p, -theta)
    l = sqrt(l)
    opl = ((pl[0]-o[0])/l, (pl[1]-o[1])/l)
    opr = ((pr[0]-o[0])/l, (pr[1]-o[1])/l)
    offset = angleDir(ur,opr)/bigAngle
    shade = angleDir(ur,opl)/bigAngle
    return offset, shade

def percentIn(o, s, b):
    so = s-o
    so = so - (so==0)*1
    r = 0 + (o  < 0 and s  > 1)*(b/so) + (o  < 0 and s <= 1)*(s/so) + (o >= 0 and s  > 1)*((b-o)/so)
    return r + (r<=0)*1

class Mipmap():
    
    def __init__(self, tilesize, w, h):
        self.tilesize = tilesize
        self.size = (w/tilesize, h/tilesize)
        #self.tile()
        self.selected = []
            
    def tile(self):
        #Divide window into tiles of size tS (= tile size)
        #Returns (width, height) in tiles
        ts = self.tilesize
        with beginShape(QUADS):
            for x in range(self.size[0]):
                for y in range(self.size[1]):
                    vertex (ts*x,    ts*y)
                    vertex (ts*x,    ts*y+ts)
                    vertex (ts*x+ts, ts*y+ts)
                    vertex (ts*x+ts, ts*y)
       
    # def drawtile(self,x,y,l=0,c='#FF0000'):
    #     #Draws tile on x,y in level l
    #     #Stes color c
    #     print("Drawing")
    #     ts = self.tilesize*(2**(l+1))
    #     with pushStyle():
    #         stroke(c)
    #         with beginShape(QUADS):
    #             vertex (ts*x,    ts*y)
    #             vertex (ts*x,    ts*y+ts)
    #             vertex (ts*x+ts, ts*y+ts)
    #             vertex (ts*x+ts, t    
    # def drawtileTuple(self,tile):
    #     print(tile)
    #     self.drawtile(tile[0], tile[1], tile[2])
                
    def display(self):       
        ts = self.tilesize
        with beginShape(QUADS):
            for x in range(self.size[0]):
                for y in range(self.size[1]):
                    vertex (ts*x,    ts*y)
                    vertex (ts*x,    ts*y+ts)
                    vertex (ts*x+ts, ts*y+ts)
                    vertex (ts*x+ts, ts*y)
        
        for i in self.selected:
            ax = i[0]
            ay = i[1]
            al = i[2]
            lts = self.tilesize*(2**(al))
            with pushStyle():
                stroke('#FF0000')
                with beginShape(QUADS):
                    vertex (lts*ax,    lts*ay)
                    vertex (lts*ax,    lts*ay+lts)
                    vertex (lts*ax+lts, lts*ay+lts)
                    vertex (lts*ax+lts, lts*ay)            
                            
    #def trace(self, p1, p2, p3, l=2):
    def trace(self, origin, u, angle, distance, l=2):
        
        v = (-u[1], u[0])
        ul = rotVec(u, angle)
        ur = rotVec(u, -angle)
        bigAngle = angleDir(ur, ul)
        
        levelsizes = [(self.size[0]*self.size[1])/(4**i) for i in range(l+1)]
        leveldimensions = [((self.size[0])/(2**i), (self.size[1])/(2**i)) for i in range(l+1)]
        levelradiuses = [0.5*(2**(i)) for i in range(l+1)]
        
        stack = []
        for i in xrange(leveldimensions[l][0]):
            for j in xrange(leveldimensions[l][1]):
                if i%2==0 and j%2==0:
                    stack.append((j*leveldimensions[l][0]+i,l))
                
        selected = []
        ts = self.tilesize
        lts = ts*(2**l)
        t = (0,0,0)
        x = 0
        y = 0
        l = 0
        while stack!=[]:            
            t = stack.pop()
            l = t[1]
            lts = ts*(2**l)
            
            x = t[0]%leveldimensions[l][0]
            y = (t[0]-x)/leveldimensions[l][0]
            
            if not ( ( (x%2==1) and (y%2==1) ) or (x >= leveldimensions[l][0]) or  (y >= leveldimensions[l][1])):
                lx = x + (t[0]+1)%2 - t[0]%2
                ly = y + t[0]%2
                stack.append((ly*leveldimensions[l][0]+lx,l))
            
            offset, shade = shadeCalc(origin, (x,y), levelradiuses[l], angle, ul, ur, bigAngle)
            percent = percentIn(offset, shade, bigAngle)

            if percent > 1:
                selected.append((x,y,l))
            else:
                if l>0:
                    stack.append((((2*y)*leveldimensions[l-1][0])+(x*2),l-1))

        self.selected = selected

        return selected
            