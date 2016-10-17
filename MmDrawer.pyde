from mipmap import *

tex = []
p1 = (2,2)
p2 = (100,240)
p3 = (240,2)

origin = (31.0,62.0)
uvec = (-0.5,-1.0)
angle = 0.50
distance = 200.0

def setup():
    size(128, 128)
    
    l0 = loadImage("t0.png")
    l1 = loadImage("t1.png")
    l2 = loadImage("t2.png")
    l3 = loadImage("t3.png")
    l4 = loadImage("t4.png")
    l5 = loadImage("t5.png")
    l6 = loadImage("t6.png")
    print("Image get", red(l0.get(64, 64)))
    
    tex.append(Mipmap(1,width,height,[l0,l1,l2,l3,l4,l5,l6]))
    #tex[0].trace(p1,p2,p3, 4)
    #tex[0].trace(origin, uvec, angle, distance, 5)
    #print(len(tex[0].selected))

def mouseClicked():
    tex[0].setlight(mouseX, mouseY)

def keyPressed():
    tex[0].trace(origin, uvec, angle, distance, 5)
    print(len(tex[0].selected))
        
def draw():
    if tex[0]:
        #angle = angle+0.1
        #tex[0].trace(origin, uvec, angle, distance, 4)
        #tex[0].displayWithBackground()
        tex[0].render()
    #with pushStyle():
    #    noFill()
    #    stroke('#00FF00')
    #    with beginShape(TRIANGLES):
    #        vertex(p1)
    #        vertex(p2)
    #        vertex(p3)