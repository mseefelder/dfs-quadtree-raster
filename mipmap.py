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
        
    def shade():
        shArr = (0,0,0,0,0,0,0,0)
        
        
        
        return shArr            
                            
    #def trace(self, p1, p2, p3, l=2):
    def trace(self, origin, uvec, angle, distance, l=2):
        
        p1 = origin
        p2 = (cos(angle)*uvec[0]-sin(angle)*uvec[1], sin(angle)*uvec[0]+cos(angle)*uvec[1]) 
        dp = vecLen(p2)
        p2 = ((p2[0]/dp)*distance, (p2[1]/dp)*distance)
        p2 = (p2[0]+p1[0], p2[1]+p1[1])
        
        p3 = (cos(angle)*uvec[0]+sin(angle)*uvec[1], -sin(angle)*uvec[0]+cos(angle)*uvec[1])
        p3 = ((p3[0]/dp)*distance, (p3[1]/dp)*distance)
        p3 = (p3[0]+p1[0], p3[1]+p1[1])
        
        print(p1, p2, p3)
        
        levelsizes = [(self.size[0]*self.size[1])/(4**i) for i in range(l+1)]
        leveldimensions = [((self.size[0])/(2**i), (self.size[1])/(2**i)) for i in range(l+1)]
        #print(leveldimensions)
        
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
            #print("==========")
            #print "stack:", stack
            #print "selected:", selected
            
            t = stack.pop()
            l = t[1]
            lts = ts*(2**l)
            
            x = t[0]%leveldimensions[l][0]
            y = (t[0]-x)/leveldimensions[l][0]
            
            #if (t[0]+1) < levelsizes[l]:
            if not ( ( (x%2==1) and (y%2==1) ) or (x >= leveldimensions[l][0]) or  (y >= leveldimensions[l][1])):
                lx = x + (t[0]+1)%2 - t[0]%2
                ly = y + t[0]%2
                stack.append((ly*leveldimensions[l][0]+lx,l))
            
            #print((x,y))
            #This order matters for ptInSq and ptInTri
            sq1 = (lts*x,     lts*y)
            sq2 = (lts*x+lts, lts*y+lts)
            sq3 = (lts*x,     lts*y+lts)
            sq4 = (lts*x+lts, lts*y)
            #print(sq1, sq2, sq3, sq4)
            count = 0
            count = count + int(ptInTri(sq1,p1,p2,p3))
            count = count + int(ptInTri(sq2,p1,p2,p3))
            count = count + int(ptInTri(sq3,p1,p2,p3))
            count = count + int(ptInTri(sq4,p1,p2,p3))
            #print("Sq points in tri:", count)
            if count == 4:
                selected.append((x,y,l))
                continue
            if count > 0:
                if l>0:
                    stack.append((((2*y)*leveldimensions[l-1][0])+(x*2),l-1))
                continue
            if count == 0:
                count = 0
                count = count + int(ptInSq(p1,sq1,sq2,sq3,sq4))
                count = count + int(ptInSq(p2,sq1,sq2,sq3,sq4))
                count = count + int(ptInSq(p3,sq1,sq2,sq3,sq4))
                #print("Tri points in sq:", count)
                if count > 0:
                    if l>0:
                        stack.append((((2*y)*leveldimensions[l-1][0])+(x*2),l-1))
                continue
        self.selected = selected
        return selected
            