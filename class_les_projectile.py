from conf import *
from class_proj import Proj
import pyxel

class Les_projectile:
    def __init__(self):
        self.les_proj = []

    def update(self,les_entite,collide,est_dans_l_eau,map):
        index = 0
        a_sup = []
        for i in self.les_proj:
            i.move()
            if les_entite.kill_mob(i,collide):
                a_sup.append(index)
            if i.x < 0 or i.x > WIDTH or i.y <0 or i.y >HEIGHT:
                a_sup.append(index)

            if not i.est_sous_l_eau:
                if map.in_bloc_calque_2(i.x,i.y,MUR_CASSABLE_T):
                    map.cache.pset((i.x+map.niv*128)//8,i.y//8,SOL)
                    a_sup.append(index)

                if map.in_bloc(i.x, i.y, MUR) or map.in_bloc(i.x, i.y, MUR2):
                    a_sup.append(index)
            else:
                if map.in_bloc_sous_l_eau_calque2(i.x,i.y,MUR_CASSABLE_A):
                    map.cache.pset((i.x+map.niv*128)//8,(i.y+128)//8,EAU)
                    a_sup.append(index)

                if map.in_bloc_sous_l_eau(i.x, i.y, MUR_EAU):
                    a_sup.append(index)


            index+=1

        a_sup = list(set(a_sup))
        for pro in a_sup[::-1]:
            self.les_proj.pop(pro)
    def draw(self,est_sous_l_eau):
        for i in self.les_proj:
            i.draw(est_sous_l_eau)
    def add(self,player):
        self.les_proj.append(Proj(player))