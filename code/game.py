import pygame # type: ignore
import interface as inter # type: ignore
import map, asyncio
from dialogue import BoiteDialogue
from player import Player # type: ignore
from musique import EffetSonore
from page_game_over import game_over


class Game : 
    def __init__(self):
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Interface RPG")
        self.effets = EffetSonore()
        self.player = Player(0,0)
        self.map_manger = map.MapManger(self.screen, self.player)
        self.dialog_box = BoiteDialogue()
        self.effets.charger("épée","epee_joueur.ogg")
        self.effets.charger("dégat", "coup_sur_player.ogg")
        self.effets.charger("s1", "son_slime_1.ogg")
        self.effets.charger("s2", "son_slime_2.ogg")
        self.effets.charger("s3", "son_slime_3.ogg")

    def handle_input (self):
        if self.dialog_box.reading or self.player.bloque:
            return

        if self.player.is_attacking:
            return 
    
        pressed = pygame.key.get_pressed()

        if pressed[pygame.K_UP]:
            self.player.move_up()

        elif pressed[pygame.K_DOWN]:
            self.player.move_down()
        
        elif pressed[pygame.K_LEFT]:
            self.player.move_left()
        
        elif pressed[pygame.K_RIGHT]:
            self.player.move_right()

        else : 
            self.player.stop()
                
    def update(self):
        self.map_manger.update(self.dialog_box)
        

    def affichage_coeur(self, x_depart=20, y_depart=20):
        taille_pixel = 2  
        espace = 6
    
        nombre_coeurs = self.player.stat.pointDeVieMax // 2
    
        for i in range(nombre_coeurs):
            vie_du_coeur = self.player.stat.pointDeVie - i * 2
            if vie_du_coeur >= 2:
                couleur = (220, 40, 60)     
            elif vie_du_coeur == 1:
                couleur = (220, 120, 140)    
            else:
                couleur = (60, 60, 60)       
        
            x = x_depart + i * (13 * taille_pixel + espace)
            inter.dessiner_coeur(x, y_depart, taille_pixel, couleur)


    def affichage_potions(self, x_depart=20, y_depart=60):
        
        taille_potion = 0.85  
        espace = 30 
    
        nombre_potions = 3
        
        for i in range(nombre_potions):
            #print("ah")
            x = x_depart + i * espace
            if self.player.etat_postion[nombre_potions-1-i] == False :
                
                inter.dessiner_potion(x, y_depart, (60, 60, 60), (0, 0, 0),(60, 60, 60),(60, 60, 60),(0, 0, 0),(0, 0, 0),(80, 80, 80), taille=taille_potion)
            else : 
                inter.dessiner_potion(x, y_depart,(170, 220, 255), (80, 120, 160), (220, 60, 140), (170, 40, 110), (150, 95, 45), (110, 70, 35), (235, 250, 255),taille=taille_potion)



    async def run (self):
        #boucle du jeu

        self.running = True
        while self.running:
            self.player.save_location()
            self.handle_input()
            self.update()
            self.map_manger.draw()
            self.dialog_box.render(self.screen)
            self.affichage_coeur()
            self.affichage_potions()
            self.player.inventaire.render(self.screen)
            pygame.display.flip()

            if not self.player.estVivant():
                self.running = False
                await game_over()

            if self.map_manger.dino_ending:
                self.running = False
                from dino_scr import dino
                await dino()
                

            for event in pygame.event.get():        
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    if self.dialog_box.reading:
                        self.dialog_box.next_text()
                    else:
                        self.effets.jouer("épée")
                        self.player.attaque()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_RSHIFT:
                    self.player.sprint()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_LSHIFT:
                    self.player.sprint_dev()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_EQUALS:
                    self.player.retour_normal()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_z:
                    #son POP
                    self.player.stat.consommePotion()
                    self.player.change_etat_potion()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_e:
                    #son POP
                    if self.player.inventaire.est_ouvert():
                        self.player.inventaire.ferme_inventaire()
                    else :
                        self.player.inventaire.ouvre_inventaire()

            await asyncio.sleep(0)