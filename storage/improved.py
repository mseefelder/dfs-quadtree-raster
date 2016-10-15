def rotVec(v, a):
    c = cos(a)
    s = sin(a)
    return ( (c*v[0])-(s*v[1]), (s*v[0])+(c*v[1]) )

def angleDir(u, v):
    #angle from u to v
    return atan2(v[1], v[0]) - atan2(u[1], u[0])

def dist2(u, v):
    return (u[0]-v[0])*(u[0]-v[0])+(u[1]-v[1])*(u[1]-v[1])

def shade(o, p, r, a, ul, ur, bigAngle):
    l = dist2(o, p)
    theta = acos( 1-( (r*r)/(2*l) ) )
    pl = rotVec(p, theta)
    pr = rotVec(p, -theta)
    opl = (pl[0]-o[0], pl[1]-o[1])
    opl = opl/sqrt(dist2(opl, (0,0)))
    opr = (pr[0]-o[0], pr[1]-o[1])
    opr = opl/sqrt(dist2(opr, (0,0)))
    offset = angleDir(ur,opr)/bigAngle
    shade = angleDir(ur,opl)/bigAngle
    return offset, shade

def percentIn(o, s, b):
    so = s-o
    r = 0 + \
        (o  < 0 and s  > 1)*(b/so) + \
        (o  < 0 and s <= 1)*(s/so) + \
        (o >= 0 and s  > 1)*((b-o)/so)
    return r + (r==0)*1

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
            
            offset, shade = shade(origin, (x,y), levelradiuses[l], angle, ul, ur, , bigAngle)
            percent = percentIn(offset, shade, bigAngle)

            if percent > 0.9:
                selected.append((x,y,l))
            else:
                if l>0:
                    stack.append((((2*y)*leveldimensions[l-1][0])+(x*2),l-1))

        self.selected = selected

        return selected