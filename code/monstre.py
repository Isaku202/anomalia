import pygame
import random
from Timer import Timer
from animation_monstre import AnimateSpriteMonstre
from character import Character
import module_classe as mc


class Monstre(AnimateSpriteMonstre, Character):
    def __init__(self, name, x, y, force, defence, pointDeVie, pointDeVieMax, agi, chance, player, nb_points=0, exp=10):
        AnimateSpriteMonstre.__init__(self)
        self.init_character(name, x, y, 400, nb_points, speed=2)  
        self.has_hit = False
        self.timer = Timer(3000)

        self.preparation_attaque = False

        self.spawn_x = x
        self.spawn_y = y
        self.timer_respawn = Timer(10000)  
        self.est_mort = False
        self.visible = True

        marge = 50  
        self.hit_box = pygame.Rect(
            0, 
            0, 
            self.rect.width + marge * 2, 
            self.rect.height + marge * 2   
        )
        self.hit_box.center = self.rect.center
        
        self.stat = mc.Monstre(
            nom=name,
            race="Slime Ordinaire",
            niv=1,
            force=force,
            defence=defence,
            pointDeVie=pointDeVie,
            pointDeVieMax=pointDeVieMax,
            agi=agi,
            luk=chance,
            exp=exp,
            player=player
        )

        self.force_init = force
        self.defence_init = defence
        self.pointDeVie_init = pointDeVie
        self.pointDeVieMax_init = pointDeVieMax
        #self.stat.afficherStats1()
        
        #Système de mouvement aléatoire
        self.direction_actuelle = random.choice(['up', 'down', 'left', 'right'])
        self.compteur_changement = 0
        self.duree_direction = random.randint(60, 180)  
        
        self.is_attacking = False
    
    def afficher_stats(self):
        return self.stat.afficherStats1()
    
    def attaquer(self, cible):
        return self.stat.attaquer(cible)
    
    def estVivant(self):
        return self.stat.estVivant()
    
    def gain_exp(self):
        return self.stat.gain_exp()

    def mourir(self):
        """Appelée quand le monstre meurt"""
        self.est_mort = True
        self.visible = False
        self.timer_respawn.demarrer()

    def respawn(self):
        """Réinitialise le monstre à son état initial"""
        self.position = [self.spawn_x, self.spawn_y]
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom
        
        self.stat.pointDeVie = self.pointDeVieMax_init
        self.stat.pointDeVieMax = self.pointDeVieMax_init
        self.stat.force = self.force_init
        self.stat.defence = self.defence_init
        
        self.est_mort = False
        self.visible = True
        self.is_attacking = False
        self.has_hit = False
        
        self.choisir_nouvelle_direction()



    def choisir_nouvelle_direction(self):
        """Choisit une nouvelle direction aléatoire"""
        self.direction_actuelle = random.choice(['up', 'down', 'left', 'right'])
        self.duree_direction = random.randint(60, 180)
        self.compteur_changement = 0

    def move(self):
        """Déplacement aléatoire du monstre"""
        self.compteur_changement += 1
        
        if self.compteur_changement >= self.duree_direction:
            self.choisir_nouvelle_direction()
        
        if self.direction_actuelle == 'up':
            self.move_up()
        elif self.direction_actuelle == 'down':
            self.move_down()
        elif self.direction_actuelle == 'left':
            self.move_left()
        elif self.direction_actuelle == 'right':
            self.move_right()

    def gerer_collision(self):
        """Appelé quand le monstre heurte quelque chose (mur ou joueur)"""
        self.move_back()  
        self.choisir_nouvelle_direction()  
    
    def tire_attaque (self):
        if self.is_attacking:
            return
        if self.preparation_attaque:
            if self.timer.est_fini():
                self.is_attacking = True
                self.preparation_attaque = False
            return
        rand = random.randint(0, 100)
        if rand == 1:  
            self.timer.demarrer()
            self.preparation_attaque = True

    # Méthodes mouvement 
    def move_right(self):
        """Déplacement vers la droite"""
        Character.move_right(self)

    def move_left(self):
        """Déplacement vers la gauche"""
        Character.move_left(self)

    def move_up(self):
        """Déplacement vers le haut"""
        Character.move_up(self)

    def move_down(self):
        """Déplacement vers le bas"""
        Character.move_down(self)

    def stop (self):
        self.image = self.anim_monstre["slime"]["mouvement"][0]

    def update(self):
        """Met à jour la position du monstre"""
        if self.est_mort:
            self.rect.x = -10000
            self.rect.y = -10000
            if self.timer_respawn.est_fini():
                self.respawn()
            return
        
        if self.visible:
            Character.update(self)
            self.hit_box.center = self.rect.center 
            self.animate("slime")
            self.tire_attaque()

            if self.is_attacking:
                finished = self.animate_atk(loop=False)
                if finished:
                    self.is_attacking = False
                    self.has_hit = False
                    self.stop()
                    
    def move_back(self):
        """Retour à l'ancienne position en cas de collision"""
        Character.move_back(self)

    def save_location(self):
        """Sauvegarde la position actuelle"""
        Character.save_location(self)

    def change_ani(self, nv_direction):
        Character.change_ani(self, nv_direction)