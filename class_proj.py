from conf import *
import pyxel

class Proj:
    def __init__(self,player):
        self.orientation = player.orientation
        self.W,self.H = (1,2) if self.orientation in (BAS,HAUT) else (2,1)
        self.x = player.x + player.W // 2
        self.y = player.y + player.H //2
        self.u, self.v = (3,22) if self.orientation in (BAS,HAUT) else (22,28)
        self.est_sous_l_eau = player.est_sous_l_eau

    def move(self):
        if self.orientation == GAUCHE:
            self.x -= 1
        if self.orientation == DROITE:
            self.x += 1
        if self.orientation == BAS:
            self.y += 1
        if self.orientation == HAUT:
            self.y -= 1

    def draw(self,est_sous_l_eau):
        if self.est_sous_l_eau and est_sous_l_eau:
            pyxel.blt(self.x,self.y,0,self.u,self.v,self.W,self.H,0)
        if not self.est_sous_l_eau and not est_sous_l_eau:
            pyxel.blt(self.x,self.y,0,self.u,self.v,self.W,self.H,0)
