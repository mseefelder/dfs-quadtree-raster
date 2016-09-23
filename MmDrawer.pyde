from mipmap import *

tex = []

def setup():
    size(256, 256)
    tex.append(Mipmap(4,width,height))
    tex[0].trace((2,2),(240,240),(240,2), 2)
    
        
def draw():
    if tex[0]:
        tex[0].display()
    with pushStyle():
        noFill()
        stroke('#00FF00')
        with beginShape(TRIANGLES):
            vertex(2,2)
            vertex(240,240)
            vertex(240,2)