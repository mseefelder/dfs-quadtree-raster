from mipmap import *

tex = []
p1 = (2,2)
p2 = (100,240)
p3 = (240,2)

starting = (126.0, 126.0)
counter = 0
saveit = True
mode = 1

origin = (31.0,62.0)
uvec = (-0.5,-1.0)
angle = 0.50
distance = 200.0

def setup():
    
    size(128, 128)
    
    counter = 0  
    starting = (126.0, 126.0)  
    
    l0 = loadImage("t0.png")#128
    l1 = loadImage("t1.png")#64
    l2 = loadImage("t2.png")#32
    l3 = loadImage("t3.png")#16
    l4 = loadImage("t4.png")#8
    l5 = loadImage("t5.png")#4
    l6 = loadImage("t6.png")#2
    print("Image get", red(l0.get(64, 64)))
    
    tex.append(Mipmap(1,width,height,[l0,l1,l2,l3,l4,l5,l6]))

def mouseClicked():
    global saveit
    global mode
    if mode==0 or mode==1:
        print mode
        tex[0].setlight(mouseX, mouseY)
        saveit = True

#def keyPressed():
    #tex[0].trace(origin, uvec, angle, distance, 5)
    #print(len(tex[0].selected))
        
def draw():
    global counter
    global starting
    global mode
    global saveit
    if tex[0]:
        if mode == 0:
            tex[0].displayWithBackground()
            if saveit==True:
                saveFrame()
                saveit = False
        elif mode==1:
            tex[0].render()
            if saveit==True:
                saveFrame()
                saveit = False
        elif mode==2:
            if counter<63:
                print(counter)
                starting = (starting[0], starting[1]-2)
                tex[0].setlight(starting[0], starting[1])
                counter = counter+1
            else:
                saveit = False
            tex[0].render()
            if saveit==True:
                saveFrame()