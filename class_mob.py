from conf import *
import pyxel


class Mob:
    def __init__(self, x, y, version):
        self.x = x
        self.y = y
        self.W = 8
        self.H = 8
        self.version = version
        self.u = 0 if version == 0 else 16
        self.v = 24 if version == 0 else 40
        self.spawn = (x, y)

    def draw(self, dans_leau):
        if self.version == dans_leau:
            pyxel.blt(self.x, self.y, 0, self.u, self.v, self.W, self.H, colkey=0)

    def update(self):
        if pyxel.frame_count % 5 == 0:
            self.x += pyxel.rndi(-1, 1)
            self.y += pyxel.rndi(-1, 1)

            if self.x > self.spawn[X] + 3 * 8:
                self.x = self.spawn[X] + 3 * 8

            if self.x < self.spawn[X] - 3 * 8:
                self.x = self.spawn[X] - 3 * 8

            if self.y > self.spawn[Y] + 3 * 8:
                self.y = self.spawn[Y] + 3 * 8

            if self.y < self.spawn[Y] - 3 * 8:
                self.y = self.spawn[Y] - 3 * 8