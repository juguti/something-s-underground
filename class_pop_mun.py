from conf import *
import pyxel


class Pop_mun:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.W = 8
        self.H = 8
        self.u = 40
        self.v = 24

    def draw(self):
        pyxel.blt(self.x, self.y, 0, self.u, self.v, self.W, self.H, colkey=0)
