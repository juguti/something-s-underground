from conf import *
import pyxel

class Coeur:
    def __init__(self, pos):
        self.x = pos[0]
        self.y = pos[1]
        self.W = 8
        self.H = 8
        self.U = 32
        self.V = 32

    def draw(self):
        pyxel.blt(self.x, self.y, 0, self.U, self.V, self.W, self.H, colkey=0)