from conf import *
import pyxel

class Selection:
    def __init__(self, niv):
        self.n_niv = niv
        self.curseur = 0
        self.in_menu = True
        self.mode = None

    def update(self):
        if self.mode == "level":
            if pyxel.btnp(pyxel.KEY_UP) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_UP):
                pyxel.play(3,4)
                self.curseur -= 4

            if pyxel.btnp(pyxel.KEY_DOWN)or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN):
                pyxel.play(3,4)
                self.curseur += 4

            if pyxel.btnp(pyxel.KEY_RIGHT)or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT):
                pyxel.play(3,4)
                self.curseur += 1

            if pyxel.btnp(pyxel.KEY_LEFT)or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT):
                pyxel.play(3,4)
                self.curseur -= 1

            if self.curseur < 0: self.curseur = 0
            if self.curseur >= self.n_niv: self.curseur = self.n_niv

            if pyxel.btnp(pyxel.KEY_B) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_B):
                self.mode = None
                self.curseur = 0
                pass

            if pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A):
                pyxel.stop()
                pyxel.play(3, 5)

                self.in_menu = False
                return self.curseur

            return None
        else:
            if pyxel.btnp(pyxel.KEY_UP) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_UP) or pyxel.btnp(pyxel.KEY_DOWN) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN):
                pyxel.play(3, 4)
                self.curseur = (self.curseur + 1)%2

            if pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A):
                if self.curseur == 0:
                    pyxel.stop()
                    pyxel.play(3, 5)
                    self.in_menu = False
                    self.mode = "normal"
                    self.in_menu = False
                    return 0
                else:
                    self.mode = "level"
                    self.curseur = 0

    def draw(self):
        pyxel.cls(5)

        if self.mode == "level":
            x = 16
            y = 16
            ecartement =  16
            taille = 12
            for i in range(self.n_niv+1):
                if self.curseur == i:
                    pyxel.rect(x-1,y-1,taille+2,taille+2,2)

                pyxel.rect(x,y,taille,taille,1)
                pyxel.text(3+x,2+y,str(i),0)

                x += ecartement + taille
                if x > 128-ecartement:
                    x = 16
                    y += ecartement + taille

        else:
            pyxel.rect(32,21,64,32,3 if self.curseur == 0 else 1)
            pyxel.text(52,35,'Normal',0)
            pyxel.rect(32, 74, 64, 32, 3 if self.curseur == 1 else 1)
            pyxel.text(52,88,'Choisir',0)


    def retour_au_menu(self):
        self.in_menu = True
        self.curseur = 0
        pyxel.stop()
        pyxel.playm(1,loop=True)