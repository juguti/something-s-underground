from conf import *
import pyxel


class Map:
    def __init__(self):
        self.niv = 0
        self.u = 0 + 128 * self.niv
        self.v = 0
        self.tilemap = pyxel.tilemap(0)
        self.cache = pyxel.tilemap(1)
        self.spawn = None
        self.chest = None
        self.fin = False
        self.max_niv = 15
        self.pos_les_mobs_terrestre = []
        self.pos_les_mobs_aquatique = []
        self.pos_les_coeur_terrestre = []
        self.pos_les_coeur_aqua = []
        self.pos_les_algues = []



        self.pos_les_mines = []
        self.pos_les_mun = []

        self.parcour()

    def draw(self):
        pyxel.bltm(0, 0, 0, self.u, self.v, WIDTH, HEIGHT)
        pyxel.bltm(0, 0, 1, self.u, self.v, WIDTH, HEIGHT, colkey=0)

    def in_bloc(self, x, y, bloc):
        x += self.niv * 128
        if self.tilemap.pget(x // 8, y // 8) == bloc:
            return True
        return False

    def in_bloc_calque_2(self,x,y,bloc):
        x += self.niv * 128
        if self.cache.pget(x // 8, y // 8) == bloc:
            return True
        return False


    def in_bloc_sous_l_eau(self, x, y, bloc):
        x += self.niv * 128
        if self.tilemap.pget(x // 8, (y + 128) // 8) == bloc:
            return True
        return False

    def in_bloc_sous_l_eau_calque2(self, x, y, bloc):
        x += self.niv * 128
        if self.cache.pget(x // 8, (y + 128) // 8) == bloc:
            return True
        return False


    def afficher_l_eau(self, vrai):
        if vrai:
            self.v = 128
        else:
            self.v = 0

    def get_bloc(self, x, y, bloc):
        if self.tilemap.pget(x, y) == bloc:
            return True
        return False

    def parcour(self):
        self.pos_les_mobs_terrestre.clear()
        self.pos_les_mobs_aquatique.clear()
        self.pos_les_mines.clear()
        self.pos_les_mun.clear()
        self.pos_les_coeur_terrestre = []
        self.pos_les_coeur_aqua = []
        self.pos_les_algues = []

        for dx in range(WIDTH // 8):
            for dy in range(HEIGHT // 8):
                ddx = dx + self.niv * 16
                if self.get_bloc(ddx, dy, SPAWN):
                    self.spawn = (dx * 8, dy * 8)
                    self.cache.pset(ddx, dy, SOL)
                if self.get_bloc(ddx, dy, CHEST):
                    self.chest = (dx * 8, dy * 8)
                    self.cache.pset(ddx, dy, SOL)
                if self.get_bloc(ddx, dy, MOB_POS):
                    self.pos_les_mobs_terrestre.append((dx * 8, dy * 8))
                    self.cache.pset(ddx, dy, SOL)
                if self.get_bloc(ddx, dy + 16, MOB_POS):
                    self.pos_les_mobs_aquatique.append((dx * 8, dy * 8))
                    self.cache.pset(ddx, dy + 16, EAU)
                if self.get_bloc(ddx, dy, MINE):
                    self.pos_les_mines.append((dx * 8, dy * 8))
                    self.cache.pset(ddx, dy, SOL)

                if self.get_bloc(ddx, dy + 16, MUR_CASSABLE_A):
                    self.cache.pset(ddx, dy + 16, MUR_CASSABLE_A)
                if self.get_bloc(ddx, dy, MUR_CASSABLE_T):
                    self.cache.pset(ddx, dy, MUR_CASSABLE_T)

                if self.get_bloc(ddx, dy, COEUR):
                    self.pos_les_coeur_terrestre.append((dx * 8, dy * 8))
                    self.cache.pset(ddx, dy, SOL)

                if self.get_bloc(ddx, dy + 16, COEUR):
                    self.pos_les_coeur_aqua.append((dx * 8, dy * 8))
                    self.cache.pset(ddx, dy + 16, EAU)

                if self.get_bloc(ddx, dy + 16, ALGUE):
                    self.pos_les_algues.append((dx * 8, dy * 8))
                    self.cache.pset(ddx, dy + 16, EAU)

                if self.get_bloc(ddx, dy, MUNITION):
                    self.pos_les_mun.append((dx * 8, dy * 8))
                    self.cache.pset(ddx, dy, SOL)



    def next_level(self):
        self.niv += 1
        self.u = 128 *self.niv
        if self.niv == self.max_niv+1:
            self.fin = True
        else:
            self.parcour()