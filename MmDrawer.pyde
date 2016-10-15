from mipmap import *

tex = []
p1 = (2,2)
p2 = (100,240)
p3 = (240,2)

origin = (128,256)
uvec = (0,-1)
angle = 0.50
distance = 200

def setup():
    size(256, 256)
    tex.append(Mipmap(4,width,height))
    #tex[0].trace(p1,p2,p3, 4)
    tex[0].trace(origin, uvec, angle, distance, 5)
    print(len(tex[0].selected))
    
        
def draw():
    if tex[0]:
        #angle = angle+0.1
        #tex[0].trace(origin, uvec, angle, distance, 4)
        tex[0].display()
    #with pushStyle():
    #    noFill()
    #    stroke('#00FF00')
    #    with beginShape(TRIANGLES):
    #        vertex(p1)
    #        vertex(p2)
    #        vertex(p3)