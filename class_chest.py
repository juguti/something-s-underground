from conf import *
import pyxel

class Cheste:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self,etape,orientation):
        co = {
            BAS:(0,8),
            HAUT: (0, -8),
            GAUCHE: (-8, 0),
            DROITE: (8, 0)
        }
        x = self.x + co[orientation][X]
        y = self.y + co[orientation][Y]
        if etape == 0:
            pyxel.blt(x,y,0,56,0,8,8,colkey=0)
        if etape == 1:
            pyxel.blt(x,y,0,48,8,8,8,colkey=0)
        if etape == 2:
            pyxel.blt(x,y,0,48,0,8,8,colkey=0)