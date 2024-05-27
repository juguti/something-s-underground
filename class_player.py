from conf import *
import pyxel

class Player:
    def __init__(self, spawn):
        self.x = 0
        self.y = 0
        self.spawn = spawn
        self.retourne_spawn()
        self.u = PLAYER_POS[X]
        self.v = PLAYER_POS[Y]
        self.W = 8
        self.H = 8
        self.speed = 8
        self.oxygene_max = 60 * 5
        self.oxygene = self.oxygene_max
        self.est_sous_l_eau = False
        self.G = 0.5
        self.f = 0
        self.dead = False
        self.pvmax = 60 * 3
        self.pv = self.pvmax
        self.orientation = HAUT
        self.mun = 3
        self.mun_max = 3
        self.message = None

    def proj_count(self):
        munx = 4
        muny = HEIGHT - 11
        for mun in range(self.mun_max):
            pyxel.blt(munx, muny, 0, MUN_U, MUN_V + 8, 4, 7,0 )
            munx += 5
        munx = 4
        for mun in range(self.mun):
            pyxel.blt(munx, muny, 0, MUN_U, MUN_V, 4, 7, 0 )
            munx += 5



    def retourne_a_la_surface(self, map):
        if self.collide(map):
            self.message = ["Mur au dessu", 0]
        else:
            self.est_sous_l_eau = False
            pyxel.stop()
            pyxel.playm(1, loop=True)
            self.u, self.v = 16, 0
            self.x = self.x // 8*8
            self.y = self.y // 8*8

    def take_dammage(self, cmb):
        self.pv -= int(cmb)
        if self.pv < 0:
            self.dead = True
            self.pv = 0

    def affiche_pv(self):
        pour = int(self.pv / self.pvmax * 100)
        pyxel.text(0, 0, "pv: " + str(pour) + "%", 0)

    def revie(self):
        self.pv = self.pvmax
        self.retourne_spawn()
        self.oxygene = self.oxygene_max
        self.est_sous_l_eau = False
        self.u, self.v = 16, 0
        self.dead = False
        pyxel.stop()
        pyxel.playm(1, loop=True)

    def retourne_spawn(self):
        self.x = self.spawn[X]
        self.y = self.spawn[Y]

    def draw(self):
        pyxel.blt(self.x, self.y, 0, self.u, self.v, self.W, self.H, colkey=0)

    def collide(self, map):
        # pos = [(self.x,self.y),(self.x + self.W-1,self.y),(self.x,self.y+self.H),(self.x+self.W-1,self.y+self.H-1)]
        if map.in_bloc(self.x, self.y, MUR):
            return True
        if map.in_bloc(self.x, self.y, MUR2):
            return True
        if map.in_bloc_calque_2(self.x,self.y,MUR_CASSABLE_T):
            return True
        return False

    def collide_eau(self, map):
        pos = [(self.x, self.y), (self.x + self.W - 1, self.y), (self.x, self.y + self.H - 1),
               (self.x + self.W - 1, self.y + self.H - 1)]
        for i in pos:
            if map.in_bloc_sous_l_eau(i[0], i[1], PLAT):
                return True
            if map.in_bloc_sous_l_eau(i[0], i[1], MUR_EAU):
                return True
            if map.in_bloc_sous_l_eau_calque2(i[0], i[1], MUR_CASSABLE_A):
                return True
        return False

    def update(self, map):
        self.move(map)
        self.vas_sous_l_eau(map)
        self.respire()
        if self.oxygene<=0:
            self.take_dammage(5)
        if self.oxygene <= 0:
            self.retourne_a_la_surface(map)

        if self.y > 128:
            self.dead = True

    def draw_barre_oxygene(self):
        if self.est_sous_l_eau or self.oxygene < self.oxygene_max:
            pourcentage = self.oxygene / self.oxygene_max
            largeur_barre = 4
            position_barre = ((WIDTH - largeur_barre),4)
            HAUTEUR_BARRE = HEIGHT - largeur_barre*2
            size = int((HAUTEUR_BARRE-2) * pourcentage)
            pyxel.rect(position_barre[X],position_barre[Y], largeur_barre, HAUTEUR_BARRE, 13)
            y = (largeur_barre+1+HAUTEUR_BARRE-2) - size
            pyxel.rect(position_barre[X]+1, y, largeur_barre-2, size, 5)

    def respire(self):
        if self.est_sous_l_eau:
            self.oxygene -= 1
            if self.oxygene < 0: self.oxygene = 0
        else:
            if self.oxygene < self.oxygene_max:
                self.oxygene += 2
                if self.oxygene > self.oxygene_max:
                    self.oxygene = self.oxygene_max

    def move(self, map):
        if (pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_B)) and self.est_sous_l_eau:
            self.f = -4
        if not self.est_sous_l_eau:

            dx = 0
            dy = 0
            if pyxel.btnp(pyxel.KEY_LEFT) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT):
                self.u, self.v = 32, 8
                self.orientation = GAUCHE
                dx = - self.speed
                dy = 0
            if pyxel.btnp(pyxel.KEY_RIGHT) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT):
                self.u, self.v = 32, 0
                self.orientation = DROITE
                dx = self.speed
                dy = 0
            if pyxel.btnp(pyxel.KEY_UP) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_UP):
                self.orientation = HAUT
                self.u, self.v = 16, 0
                dx = 0
                dy = - self.speed
            if pyxel.btnp(pyxel.KEY_DOWN) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN):
                self.orientation = BAS
                self.u, self.v = 16, 8
                dx = 0
                dy = self.speed

            self.x += dx
            self.y += dy

            if self.collide(map):
                self.x -= dx
                self.y -= dy

            if self.x >= WIDTH: self.x = self.x - self.W

        else:
            if pyxel.frame_count % 2 == 0:
                self.f += self.G
                for dy in range(abs(int(self.f))):
                    self.y += (self.f / abs(self.f))
                    if self.collide_eau(map):
                        self.y -= (self.f / abs(self.f))
                        self.f = 0
                        break
                self.y = int(self.y)

            dx = 0
            if pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT):
                dx = 1
                self.u, self.v = 0, 32
                self.orientation = DROITE

            if pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT):
                self.u, self.v = 0, 40
                dx = -1
                self.orientation = GAUCHE

            self.x += dx
            if self.collide_eau(map):
                self.x -= dx

        if self.x <= 0: self.x = 0
        if self.y - self.H >= HEIGHT: self.y = self.y - self.H
        if self.y <= 0: self.y = 0

    def vas_sous_l_eau(self, map):
        if (pyxel.btnp(pyxel.KEY_C) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A)):
            if self.est_sous_l_eau:
                self.retourne_a_la_surface(map)
            else:
                if self.collide_eau(map):
                    self.message = ["Sol trop dur", 0]
                else:
                    self.est_sous_l_eau = True
                    pyxel.stop()
                    pyxel.playm(0, loop=True)
                    self.u, self.v = 0, 32
                    self.orientation = DROITE
