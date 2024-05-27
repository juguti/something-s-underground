from conf import *
import pyxel
from class_Explo import Explo
from class_mob import Mob
from class_mines import Mines
from class_algues import Algue
from class_coeur import Coeur
from class_pop_mun import Pop_mun


class Les_entite:
    def __init__(self):
        self.les_mobs_terre = []
        self.les_mobs_aqua = []
        self.les_mines = []
        self.les_coeur_terrestre = []
        self.les_coeur_aqua = []
        self.les_algues = []
        self.les_mun = []
        self.mon_explo = None

    def kill_mob(self, projectile, collide):
        index_a_sup = []
        index = 0
        if not projectile.est_sous_l_eau:
            for mob in self.les_mobs_terre:
                if collide(projectile, mob):
                    index_a_sup.append(index)
                index += 1
            for mob in index_a_sup[0::-1]:
                self.les_mobs_terre.pop(mob)
        else:
            for mob in self.les_mobs_aqua:
                if collide(projectile, mob):
                    index_a_sup.append(index)
                index += 1
            for mob in index_a_sup[0::-1]:
                self.les_mobs_aqua.pop(mob)
        return False if len(index_a_sup)<=0 else True
    def spawn_mob(self, tilemap) -> None:
        self.les_mobs_terre.clear()
        self.les_mobs_aqua.clear()
        self.les_coeur_aqua.clear()
        self.les_coeur_terrestre.clear()
        self.les_mines.clear()
        self.les_algues.clear()
        self.les_mun.clear()
        for i in tilemap.pos_les_mobs_terrestre:
            self.les_mobs_terre.append(Mob(i[X], i[Y], 0))
        for i in tilemap.pos_les_mobs_aquatique:
            self.les_mobs_aqua.append(Mob(i[X], i[Y], 1))
        for i in tilemap.pos_les_mines:
            self.les_mines.append(Mines(i[X], i[Y]))
        for i in tilemap.pos_les_coeur_terrestre:
            self.les_coeur_terrestre.append(Coeur((i[X], i[Y])))
        for i in tilemap.pos_les_coeur_aqua:
            self.les_coeur_aqua.append(Coeur((i[X], i[Y])))
        for i in tilemap.pos_les_algues:
            self.les_algues.append(Algue(i[X], i[Y]))
        for i in tilemap.pos_les_mun:
            self.les_mun.append(Pop_mun(i[X], i[Y]))

    def update(self, player, collision):
        for mo in self.les_mobs_terre:
            mo.update()
            if collision(mo, player) and not player.est_sous_l_eau:
                player.take_dammage(2)

        for mo in self.les_mobs_aqua:
            mo.update()

            if collision(mo, player) and player.est_sous_l_eau:
                player.take_dammage(2)

        m = 0
        for mun in self.les_mun:
            if not player.est_sous_l_eau:
                if collision(mun, player):
                    player.mun = 3
                    self.les_mun.pop(m)
                    break
            m  +=1
        for mi in self.les_mines:
            if collision(mi, player):
                self.mon_explo = Explo(mi.x, mi.y)
                pyxel.stop()
                pyxel.play(0,2)

        i = 0
        for co in self.les_coeur_terrestre:
            if collision(player, co):
                player.pv = player.pvmax
                self.les_coeur_terrestre.pop(i)
        i += 1
        i = 0
        for co in self.les_coeur_aqua:
            if collision(player, co):
                player.pv = player.pvmax
        i += 1

    def draw(self, player):
        for mo in self.les_mobs_terre:
            mo.draw(0 if not player.est_sous_l_eau else 1)
        for mo in self.les_mobs_aqua:
            mo.draw(0 if not player.est_sous_l_eau else 1)
        for mi in self.les_mines:
            mi.draw(player.est_sous_l_eau)
        for co in self.les_coeur_terrestre:
            if not player.est_sous_l_eau:
                co.draw()
        for co in self.les_coeur_aqua:
            if player.est_sous_l_eau:
                co.draw()
        for al in self.les_algues:
            al.draw(player.est_sous_l_eau)
        for mun in self.les_mun:
            if not player.est_sous_l_eau:
                mun.draw()
