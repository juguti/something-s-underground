from conf import *
import pyxel

class Algue:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.W = 8
        self.H = 8
        self.u = [16, 24]
        self.v = 32
        self.index = 0
        self.delay = 5

    def draw(self, est_sou_l_eau: bool) -> None:
        if est_sou_l_eau:
            if pyxel.frame_count % self.delay == 0:
                self.index = (self.index + 1) % len(self.u)
            pyxel.blt(self.x, self.y, 0, self.u[self.index], self.v, self.W, self.H, colkey=0)
