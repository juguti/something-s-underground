from conf import *
import pyxel

class Explo:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.delay_anim = 30
        self.timer = 0

    def est_fini(self):
        if self.timer >= self.delay_anim:
            return True
        return False

    def draw(self):
        self.timer += 1
        x = self.x
        y = self.y
        if self.timer <= self.delay_anim // 2:
            pyxel.blt(x, y, 0, 56, 16, 8, 8, colkey=0)
        if self.timer >= self.delay_anim // 2:
            pyxel.blt(x, y, 0, 56, 8, 8, 8, colkey=0)