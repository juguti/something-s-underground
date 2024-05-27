import pyxel
from conf import *
from class_map import Map
from class_player import Player
from class_chest import Cheste
from class_les_entite import Les_entite
from class_les_projectile import Les_projectile
from class_selection import Selection

class Game:
    def __init__(self):
        pyxel.init(WIDTH, HEIGHT)
        pyxel.load("theme2.pyxres")
        self.map = Map()
        self.les_entite = Les_entite()
        self.les_entite.spawn_mob(self.map)
        self.player = Player(self.map.spawn)
        self.chest = Cheste(self.map.chest[0], self.map.chest[1])
        self.les_proj = Les_projectile()
        self.debut = True
        self.dial_niv_5 = False
        self.animation_coffre = False
        self.etape_aniamtion_tresort = 0
        self.timer = 0
        self.select = Selection(self.map.max_niv)
        self.timer_jeu = None
        pyxel.playm(1, loop=True)
        pyxel.run(self.update, self.draw)

    def reset(self,tmp):
        if self.select.mode == "level":
            self.timer_jeu = pyxel.frame_count
            self.map.niv = tmp - 1
        else:
            self.map.niv = -1
            self.timer_jeu = None

        self.player.mun = self.player.mun_max
        self.map.next_level()
        self.player.message = None
        self.player.spawn = self.map.spawn
        self.player.revie()
        self.player.retourne_spawn()
        self.les_entite.spawn_mob(self.map)
        self.chest = Cheste(self.map.chest[0], self.map.chest[1])
        self.les_entite.mon_explo = None



    def update(self):
        if self.select.in_menu:
            tmp = self.select.update()
            if tmp is not None:
                self.reset(tmp)

        else:
            if not self.animation_coffre and self.les_entite.mon_explo is None:
                if self.map.fin:
                    pass
                elif self.map.niv == 4 and not self.dial_niv_5:
                    if pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A):
                        self.dial_niv_5 = True
                elif not self.debut:
                    self.player.update(self.map)
                    if self.player.mun >=1:
                        if pyxel.btnp(pyxel.KEY_S) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_Y):
                            pyxel.play(3,3)
                            self.les_proj.add(self.player)
                            self.player.mun -= 1
                    self.map.afficher_l_eau(self.player.est_sous_l_eau)
                    if self.player.dead:
                        self.select.mode = None
                        self.select.curseur = 0
                        self.select.in_menu = True
                        self.timer_jeu = None

                    self.les_proj.update(self.les_entite,self.collision,self.player.est_sous_l_eau,self.map)
                    if (self.player.x, self.player.y) == (self.chest.x, self.chest.y) and (
                            pyxel.btnp(pyxel.KEY_D) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_X)):
                        self.animation_coffre = True

                    self.les_entite.update(self.player, self.collision)

                else:
                    if pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A):
                        pyxel.playm(1, loop=True)
                        self.debut = False
            elif self.animation_coffre :
                self.timer += 1
                if self.timer % 15 == 0:
                    self.etape_aniamtion_tresort += 1
                if self.etape_aniamtion_tresort == 4:
                    self.etape_aniamtion_tresort = 0
                    self.timer = 0
                    self.animation_coffre = False
                    if self.select.mode != "level":
                        self.map.next_level()
                        self.player.spawn = self.map.spawn
                        self.player.retourne_spawn()
                        self.les_entite.spawn_mob(self.map)
                        self.chest = Cheste(self.map.chest[0], self.map.chest[1])
                    else:
                        self.select.retour_au_menu()
                        self.timer_jeu = None

            elif self.les_entite.mon_explo is not None:
                if self.les_entite.mon_explo.est_fini():
                    self.les_entite.mon_explo = None
                    self.player.dead = True

    def collision(self, obj1, obj2) -> bool:
        """
        Detect la collision entre l'objet1 et l'objet2
        """
        if obj2.x <= obj1.x <= obj2.x + obj2.W - 1 or obj2.x <= obj1.x + obj1.W - 1 <= obj2.x + obj2.W - 1:
            if obj2.y <= obj1.y <= obj2.y + obj2.H - 1 or obj2.y <= obj1.y + obj1.H - 1 <= obj2.y + obj2.H - 1:
                return True
        return False

    def draw(self):
        if self.select.in_menu:
            self.select.draw()

        else:
            if self.animation_coffre:
                if self.etape_aniamtion_tresort < 3:
                    self.player.draw()
                    self.chest.draw(self.etape_aniamtion_tresort,self.player.orientation)
                else:
                    pyxel.cls(0)
                    pyxel.text(32,62,"niv: "+str(self.map.niv+1),7)

            else:
                if self.map.fin:
                    pyxel.cls(0)
                    pyxel.text(8, 8, "Merci d'avoir joue", 7)
                elif self.map.niv == 4 and not self.dial_niv_5:
                    pyxel.cls(0)
                    pyxel.text(8, 8, "Prends garde aux mines.", 7)
                    pyxel.text(8, 16, "Elles ne sont visibles que", 7)
                    pyxel.text(8, 24, "sous l'eau, mais peuvent", 7)
                    pyxel.text(8, 32, "exploser dans les deux", 7),
                    pyxel.text(8, 40, "mondes. Bonne chance !", 7)
                elif not self.debut:
                    pyxel.cls(0)
                    self.map.draw()

                    self.les_entite.draw(self.player)
                    self.les_proj.draw(self.player.est_sous_l_eau)
                    self.player.draw()

                    if self.les_entite.mon_explo is not None:
                        self.les_entite.mon_explo.draw()

                    self.player.draw_barre_oxygene()
                    self.player.affiche_pv()
                    self.player.proj_count()
                    distance = pyxel.sqrt((self.player.x - self.chest.x) ** 2 + (self.player.y - self.chest.y) ** 2)
                    pyxel.text(0, 6, "Distance: " + str(int(distance)), 0)
                    pyxel.text(100, 4, 'niv:' + str(self.map.niv), 0)
                    if self.timer_jeu != None:
                        pyxel.text(0, 12, 'Temps: ' + self.format_temps(), 0)


                    if self.player.message is not None:
                        if pyxel.frame_count % 6 != 0 :
                            pyxel.text(32,62,self.player.message[0],8)
                        self.player.message[1] += 1
                        if self.player.message[1] > 30:
                            self.player.message = None

                else:
                    pyxel.cls(0)
                    pyxel.text(8, 8, "Bonjour pirate. Tu es pret", 7)
                    pyxel.text(8, 16, "pour une chasse au tresor ?", 7)
                    pyxel.text(8, 24, "Le tresor est enfoui quelque", 7)
                    pyxel.text(8, 32, "part. Appuie sur D pour le", 7)
                    pyxel.text(8, 40, "deterrer. En appuyant sur C", 7)
                    pyxel.text(8, 48, "tu peux passer sous l'eau en", 7)
                    pyxel.text(8, 56, "2D. Certains elements", 7)
                    pyxel.text(8, 64, "disparaissent sous l'eau.", 7)
                    pyxel.text(8, 72, "profites-en pour passer .", 7)
                    pyxel.text(8, 80, "Bonne chance !", 7)


    def format_temps(self):
        temps_ecoule = pyxel.frame_count - self.timer_jeu
        min = temps_ecoule // 60 // 30
        temps_ecoule -= min * 1800
        return str(min)+":"+str(temps_ecoule//30)


        

 




Game()
