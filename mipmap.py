def vecLen(vec):
    result = 0
    for i in vec:
        result += i**2
    return sqrt(result)

def vecLen2(vec):
    result = 0
    for i in vec:
        result += i**2
    return result

def rotVec(v, a):
    c = cos(a)
    s = sin(a)
    return ( (c*v[0])-(s*v[1]), (s*v[0])+(c*v[1]) )

def angleDir(u, v):
    #angle from u to v
    return atan2(v[1], v[0]) - atan2(u[1], u[0])

def dist2(u, v):
    return 1.0*(u[0]-v[0])*(u[0]-v[0])+1.0*(u[1]-v[1])*(u[1]-v[1])

def shadeCalc(o, p, r, a, ul, ur, bigAngle):
    op = (p[0]-o[0], p[1]-o[1])
    l2 = vecLen2(op)
    l = sqrt(l2)
    op = (op[0]/l, op[1]/l)
    #theta = acos( 1 - ( (r*r)/(2*l*1.0) ) )
    theta = acos( sqrt( (l2-(r*r))/l2 ) )
    opl = rotVec(op, theta)
    opr = rotVec(op, -theta)
    #print(o, p, op, opr, opl, r, theta, l)
    #l = sqrt(l)
    #opl = ((pl[0]-o[0])/l, (pl[1]-o[1])/l)
    #opr = ((pr[0]-o[0])/l, (pr[1]-o[1])/l)
    offset = angleDir(ur,opr)
    shade = angleDir(ur,opl)
    return offset, shade

def nodeIn(o, s, b):
    #print (o, s, b)
    if(b<0):
        b = -b
        o = -o
        s = -s

    return (o >= 0) and (o < b) and (s <= b) and (s > 0)

def nodeOut(o, s, b):
    if(b<0):
        b = -b
        o = -o
        s = -s
    return ((o <= 0) and (s < 0)) or ((o > b) and (s >= b))

def addShade(o, s, b, c, v):
    if(b<0):
        b = -b
        o = -o
        s = -s
    res = len(v) #resolution of vector
    tempvec = [0.0]*res
    o = o/b
    s = s/b
    b = b/b
    x = 0.0
    step = (1.0/res)
    for i in xrange(res):
        l = (i)*step
        r = (i+1)*step
        #percentage = (abs(max(o-x, -x))+min(s-x, 0))/step
        #percentage = ( min(step, step-min(o-x, step) ) - abs(min(s-x, 0.0)))/step
        percentage = ( step - min(max(o-l, 0),step) + max(min(s-r, 0),-step) )/step
        #if percentage>1.0:
        #    print "SOMETHING'S WRONG", b, s, o, x, percentage
        tempvec[i] = min(percentage * c + v[i], 1.0)
    return tuple(tempvec)

class Mipmap():
    
    def __init__(self, tilesize, w, h, levels):
        self.ts = tilesize
        self.s = (w/tilesize, h/tilesize)
        self.selected = []
        self.base = levels[0]
        self.light = (self.s[0]/2, self.s[1]/2)#(0.0,0.0)#
        self.origin = (0,0)
        self.lightDiameter = self.s[0]/8
        self.lightChanged = False #True
        self.frame = createImage(self.s[0], self.s[1], RGB)
        self.maps = levels
        self.maxLevel = len(self.maps)-1
     
    def setlight(self, x, y):
        self.light = (x, y)
        self.lightChanged = True

        s = self.s
        self.updateShadow(s[0]/2, 2*s[1]/3)

        return 0          
    
    def render(self):
        ts = self.ts
        base = self.base
        lgt = self.light
        lgtdiam = self.lightDiameter
        frame = self.frame
        
        if (self.lightChanged):
            #render ground
            for x in range(self.s[0]):
                for y in range(self.s[1]):
                    c = color(255.0-red(base.get(x, y)), 120.0, 120.0)
                    frame.set(x, y, c)
        
            #calculate shadows for ground not in obstacles
            for x in range(self.s[0]):
                #print x
                for y in range(self.s[1]):
                    #print(x,y)
                    if (red(base.get(x, y)) != 0) and (dist2((x,y), lgt) > 1e-12):
                        self.updateShadow(x, y)
            
            #set as updated
            self.lightChanged = False
            #print("Updated frame!")
        
        image(frame, 0, 0)
        
        #render light
        with pushStyle():
            noStroke()
            fill('#FDFDAA')
            ellipse(lgt[0], lgt[1], lgtdiam, lgtdiam)
            
    def display(self):       
        ts = self.ts
        base = self.base

        with beginShape(QUADS):
            for x in range(self.s[0]):
                for y in range(self.s[1]):
                    vertex (ts*x,    ts*y)
                    vertex (ts*x,    ts*y+ts)
                    vertex (ts*x+ts, ts*y+ts)
                    vertex (ts*x+ts, ts*y)
        
        for i in self.selected:
            ax = i[0]
            ay = i[1]
            al = i[2]
            lts = ts*(2**(al))
            with pushStyle():
                stroke('#FF0000')
                fill('#F2F3F4')
                with beginShape(QUADS):
                    vertex (lts*ax,    lts*ay)
                    vertex (lts*ax,    lts*ay+lts)
                    vertex (lts*ax+lts, lts*ay+lts)
                    vertex (lts*ax+lts, lts*ay)

    def displayWithBackground(self):       
        ts = self.ts
        base = self.base
        lgt = self.light
        lgtdiam = self.lightDiameter
        frame = self.frame

        for x in range(self.s[0]):
            for y in range(self.s[1]):
                c = color(255.0-red(base.get(x, y)), 120.0, 120.0)
                frame.set(x, y, c)

        image(frame, 0, 0)

        with pushStyle():
            noFill()
            stroke('#FF0000')
            with beginShape(QUADS):
                for i in self.selected:
                    ax = i[0]
                    ay = i[1]
                    al = i[2]
                    lts = ts*(2**(al))
                    vertex (lts*ax,    lts*ay)
                    vertex (lts*ax,    lts*ay+lts)
                    vertex (lts*ax+lts, lts*ay+lts)
                    vertex (lts*ax+lts, lts*ay)

         #render light
        with pushStyle():
            noStroke()
            fill('#FDFDFD')
            ellipse(lgt[0], lgt[1], lgtdiam, lgtdiam)  

        #render origin
        if self.origin:
            with pushStyle():
                noStroke()
                fill('#BBAAFD')
                ellipse(self.origin[0], self.origin[1], 4, 4)      
                           
    def displayWithoutBackground(self):       
        ts = self.ts
        lgt = self.light
        lgtdiam = self.lightDiameter

        background(125, 125, 125)

        with pushStyle():
            noFill()
            stroke('#FF0000')
            with beginShape(QUADS):
                for i in self.selected:
                    ax = i[0]
                    ay = i[1]
                    al = i[2]
                    lts = ts*(2**(al))
                    vertex (lts*ax,    lts*ay)
                    vertex (lts*ax,    lts*ay+lts)
                    vertex (lts*ax+lts, lts*ay+lts)
                    vertex (lts*ax+lts, lts*ay)

         #render light
        with pushStyle():
            noStroke()
            fill('#FDFDFD')
            ellipse(lgt[0], lgt[1], lgtdiam, lgtdiam)  

        #render origin
        if self.origin:
            with pushStyle():
                noStroke()
                fill('#BBAAFD')
                ellipse(self.origin[0], self.origin[1], 4, 4)
                           
    def updateShadow(self, x, y):
        lgt = self.light
        lrad = self.lightDiameter/2.0
        
        #point of calculation
        origin = (x*1.0,y*1.0)
        
        #compute vector to light
        u = (lgt[0]-x, lgt[1]-y)
        
        #compute opening angle
        ul2 = vecLen2(u)
        theta = acos( sqrt( (ul2-(lrad*lrad))/ul2 ) )
        
        #compute calculation distance
        ul = sqrt(ul2)
        
        c = self.calcShadow(origin, u, theta, ul, self.maxLevel)
        self.frame.set(x, y, color(255.0*c))
        #self.traceDist(origin, u, theta, ul, self.maxLevel)
        
        return 0
   
    def calcShadow(self, origin, u, angle, distance, l=2):
        
        mm = self.maps
        s = 0.0
        sv = (0.0,0.0,0.0,0.0)

        if (len(u) != 2) or (len(origin) != 2):
            return
        
        #convert all to float
        distance = distance*1.0
        angle = angle*1.0
        origin = (origin[0]*1.0, origin[1]*1.0)
        
        #Normalize u
        u = (1.0*u[0], 1.0*u[1])
        ulen = vecLen(u)
        u = (u[0]/ulen, u[1]/ulen)
        
        v = (-u[1], u[0])
        ul = rotVec(u, angle)
        ur = rotVec(u, -angle)
        bigAngle = angleDir(ur, ul)

        #Convert to drawing space
        ts = self.ts
        hts = 0.5*ts
        
        self.origin = (origin[0]*ts+hts, origin[1]*ts+hts)
        #self.origin = (origin[0]*ts, origin[1]*ts)
        self.ur = ur
        self.ul = ul
        self.distance = distance
        
        leveldimensions = [( (self.s[0])/(2**i), (self.s[1])/(2**i) ) for i in range(l+1)]

        levelsizes = [leveldimensions[i][0]*leveldimensions[i][1] for i in range(l+1)]

        levelradiuses = [(1.4142135623730951*(2**(i)))/2.0 for i in range(l+1)]
        
        #starting nodes
        stack = []
        for i in xrange(leveldimensions[l][0]):
            for j in xrange(leveldimensions[l][1]):
                if i%2==0 and j%2==0:
                    stack.append((i, j, l))#((j*leveldimensions[l][0]+i,l))
                
        lts = ts*(2**l)
        t = (0,0,0)
        x = 0
        y = 0
        l = 0
        isin = 0
        isout = 0
        intersects = 0
        while stack!=[]:        
            t = stack.pop()
            l = t[2]
            lns = (2**l) #level node size
            
            x = t[0]
            y = t[1]
            
            #centers
            cx = (lns*x)+(lns/2.0)
            cy = (lns*y)+(lns/2.0)
            
            if not ( ( (x%2==1) and (y%2==1) ) or (x >= leveldimensions[l][0]) or  (y >= leveldimensions[l][1]) or (leveldimensions[l][0] == 1)):
                lx = x + (t[0]+1)%2 - t[0]%2
                ly = y + t[0]%2
                stack.append((lx, ly, l))
            
            # if node is obstacle, don't bother rendering
            if (255.0-red(mm[l].get(x,y)))<1e-12:
                continue
            obstacle = ( 255.0-red(mm[l].get(x,y)) )/255.0 #1.0 is full blocking obstacle
            if obstacle>1.0:
                print "SOMETHING'S WRONG"

            # if cone origin is inside node, break it
            if dist2((cx, cy), origin)<1e-12:
                if l>0:
                    stack.append((2*x, 2*y, l-1))
                continue
                   
            offset, shade = shadeCalc(origin, (cx,cy), levelradiuses[l], angle, ul, ur, bigAngle)
            
            nodeDist = sqrt(dist2(origin, (cx,cy)))

            if nodeIn(offset, shade, bigAngle):
                if nodeDist+levelradiuses[l] <= distance:
                    sv = addShade(offset, shade, bigAngle, obstacle, sv)
                    isin = isin+1
            elif nodeOut(offset, shade, bigAngle):
                isout = isout+1
                continue
            elif l>0:
                intersects = intersects+1
                stack.append((2*x, 2*y, l-1))

        #print(vecLen(sv))
        #s = min(vecLen(sv), 1.0)
        s = min((sv[0]+sv[1]+sv[2]+sv[3])/4.0, 1.0)
        s = 1.0 - s
        #print(s, sv, counter)
        return s
                                                                              
    def traceDist(self, origin, u, angle, distance, l=2):
        
        mm = self.maps
        s = 0.0
        sv = (0.0,0.0,0.0,0.0)

        if (len(u) != 2) or (len(origin) != 2):
            return
        
        #convert all to float
        distance = distance*1.0
        angle = angle*1.0
        origin = (origin[0]*1.0, origin[1]*1.0)
        
        #Normalize u
        u = (1.0*u[0], 1.0*u[1])
        ulen = vecLen(u)
        u = (u[0]/ulen, u[1]/ulen)
        
        v = (-u[1], u[0])
        ul = rotVec(u, angle)
        ur = rotVec(u, -angle)
        bigAngle = angleDir(ur, ul)

        #Convert to drawing space
        ts = self.ts
        hts = 0.5*ts
        
        self.origin = (origin[0]*ts+hts, origin[1]*ts+hts)
        #self.origin = (origin[0]*ts, origin[1]*ts)
        self.ur = ur
        self.ul = ul
        self.distance = distance
        
        leveldimensions = [( (self.s[0])/(2**i), (self.s[1])/(2**i) ) for i in range(l+1)]

        levelsizes = [leveldimensions[i][0]*leveldimensions[i][1] for i in range(l+1)]

        levelradiuses = [(2**(i))/2.0 for i in range(l+1)]
        
        #starting nodes
        stack = []
        for i in xrange(leveldimensions[l][0]):
            for j in xrange(leveldimensions[l][1]):
                if i%2==0 and j%2==0:
                    stack.append((i, j, l))#((j*leveldimensions[l][0]+i,l))
        
        selected = []  
        lts = ts*(2**l)
        t = (0,0,0)
        x = 0
        y = 0
        l = 0        
        while stack!=[]:
            #print stack
            t = stack.pop()
            l = t[2]
            lns = (2**l) #level node size
            
            x = t[0]
            y = t[1]
            
            #centers
            cx = (lns*x)+(lns/2.0)
            cy = (lns*y)+(lns/2.0)
            
            if not ( ( (x%2==1) and (y%2==1) ) or (x >= leveldimensions[l][0]) or  (y >= leveldimensions[l][1]) or (leveldimensions[l][0] == 1)):
                lx = x + (t[0]+1)%2 - t[0]%2
                ly = y + t[0]%2
                stack.append((lx, ly, l))
            
            # if node is obstacle, don't bother rendering
            if (255.0-red(mm[l].get(x,y)))<1e-12:
                continue
            #obstacle = ( 255.0-red(mm[l].get(x,y)) )/255.0 #1.0 is full blocking obstacle

            # if cone origin is inside node, break it
            if dist2((cx, cy), origin)<1e-12:
                if l>0:
                    stack.append((2*x, 2*y, l-1))
                continue
                   
            offset, shade = shadeCalc(origin, (cx,cy), levelradiuses[l], angle, ul, ur, bigAngle)
            
            nodeDist = sqrt(dist2(origin, (cx,cy)))
            
            if nodeIn(offset, shade, bigAngle):
                if nodeDist+levelradiuses[l] <= distance:
                    selected.append((x,y,l))
            elif l>0:
                stack.append((2*x, 2*y, l-1))

            print "------"

        self.selected = selected
        print("Selected: ",len(selected))
        return s

    def trace(self, origin, u, angle, distance, l=2):
        
        if (len(u) != 2) or (len(origin) != 2):
            return
        
        #convert all to float
        distance = distance*1.0
        angle = angle*1.0
        origin = (origin[0]*1.0, origin[1]*1.0)
        
        #Normalize u
        u = (1.0*u[0], 1.0*u[1])
        ulen = vecLen(u)
        u = (u[0]/ulen, u[1]/ulen)
        
        v = (-u[1], u[0])
        ul = rotVec(u, angle)
        ur = rotVec(u, -angle)
        bigAngle = angleDir(ur, ul)

        #Convert to drawing space
        ts = self.ts
        hts = 0.5*ts
        
        self.origin = (origin[0]*ts+hts, origin[1]*ts+hts)
        #self.origin = (origin[0]*ts, origin[1]*ts)
        self.ur = ur
        self.ul = ul
        self.distance = distance
        
        leveldimensions = [( (self.s[0])/(2**i), (self.s[1])/(2**i) ) for i in range(l+1)]

        levelsizes = [leveldimensions[i][0]*leveldimensions[i][1] for i in range(l+1)]

        levelradiuses = [(2**(i))/2.0 for i in range(l+1)]
        
        #starting nodes
        stack = []
        for i in xrange(leveldimensions[l][0]):
            for j in xrange(leveldimensions[l][1]):
                if i%2==0 and j%2==0:
                    stack.append((i, j, l))#((j*leveldimensions[l][0]+i,l))
                
        selected = []
        lts = ts*(2**l)
        t = (0,0,0)
        x = 0
        y = 0
        l = 0
        while stack!=[]: 
            #print(stack)           
            t = stack.pop()
            l = t[2]
            lns = (2**l) #level node size
            
            x = t[0]#t[0]%leveldimensions[l][0]
            y = t[1]#(t[0]-x)/leveldimensions[l][0]
            
            #centers
            cx = (lns*x)+(lns/2.0)
            cy = (lns*y)+(lns/2.0)
            
            if not ( ( (x%2==1) and (y%2==1) ) or (x >= leveldimensions[l][0]) or  (y >= leveldimensions[l][1]) or (leveldimensions[l][0] == 1)):
                lx = x + (t[0]+1)%2 - t[0]%2
                ly = y + t[0]%2
                stack.append((lx, ly, l))#((ly*leveldimensions[l][0]+lx,l))
            
            if dist2((cx, cy), origin)<1e-12:
                if l>0:
                    stack.append((2*x, 2*y, l-1))
                continue
                   
            offset, shade = shadeCalc(origin, (cx,cy), levelradiuses[l], angle, ul, ur, bigAngle)
            # percent = percentIn(offset, shade, bigAngle) 
                    
            if nodeIn(offset, shade, bigAngle):#percent > 0.8:
                selected.append((x,y,l))
            elif l>0:
                stack.append((2*x, 2*y, l-1))#((((2*y)*leveldimensions[l-1][0])+(x*2),l-1))

        self.selected = selected
        #print(selected)
        return selected