from conf import *
import pyxel

class Mines:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.W = 8
        self.H = 8
        self.u = 16
        self.v = 16

    def draw(self, vrai):
        if vrai:
            pyxel.blt(self.x, self.y, 0, self.u, self.v, self.W, self.H, colkey=0)