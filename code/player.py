import pygame  # type: ignore
import module_classe as m # type: ignore 
import animation as animation  # type: ignore
import inventaire


class Player (animation.AnimateSprite):
    def __init__ (self, x , y):
        super().__init__('player_complet')
        self.stat = m.Personnage("Léon", 1, 1, 1, 10, 10, 1, 1)
        self.current_direction = "base"
        self.position = [x, y]
        self.feet = pygame.Rect(0,0, self.rect.width * 0.5, 130)
        self.old_position = self.position.copy()
        self.speed = 5

        self.is_attacking = False
        self.has_hit = False

        self.etat_postion = [True, True, True]

        self.inventaire = inventaire.Inventaire([])
        self.inventaire.ajoute_item(inventaire.Items("sang étrange bleu", 4))
        self.inventaire.ajoute_item(inventaire.Items("viande", 4))
        self.inventaire.ajoute_item(inventaire.Items("carrote", 2))
        marge = 80
        self.hit_box = pygame.Rect(
            0, 0,
            self.rect.width + marge * 2,
            self.rect.height + marge * 2
        )
        self.hit_box.center = self.rect.center
        self.bloque = False  

    def ajoute_item(self, item):
        self.inventaire.ajoute_item(item)

    def drop_items(self, liste_obj, maxi):
        self.inventaire.drop_items(liste_obj, maxi)


    def estVivant (self):
        return self.stat.estVivant()
    
    def change_etat_potion (self):
        """
        Retire une potion consommée de la liste de potion.
        """
        for i in range (3):
            if self.etat_postion[i] == True :
                self.etat_postion[i] = False 
                return self.etat_postion

 #   def atk (self, perso):
        #self.stat.attaquer(perso)

    def save_location (self):
        self.old_position = self.position.copy()

    def sprint_dev (self):
        self.speed += 1.5

    def sprint(self):
        self.speed = 7.0

    def retour_normal(self):
        self.speed = 5

    def move_right (self) :
        self.change_ani ("droite")
        self.position[0] += self.speed
        self.animate("droite")

    def move_left (self) : 
        self.change_ani ("gauche")
        self.position[0] -= self.speed
        self.animate("gauche")

    def move_up (self) : 
        self.change_ani ("haut")
        self.position[1] -= self.speed
        self.animate("haut")

    def move_down (self) : 
        self.change_ani ("bas")
        self.position[1] += self.speed
        self.animate("bas")

#attaqque
    def attaque(self):
        if self.is_attacking:
            return  
    
        self.is_attacking = True
        self.has_hit = False
        self.current_frame = 0
        self.ani_counter = 0
   
        if self.current_direction == "droite":
            self.current_direction = "attaque_droite"

        elif self.current_direction == "gauche":
            self.current_direction = "attaque_gauche"

        elif self.current_direction == "haut":
            self.current_direction = "attaque_haut"
        else: 
            self.current_direction = "attaque_bas"
    


    def update(self):
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom
        
        if hasattr(self, 'hit_box'):
            self.hit_box.center = self.rect.center

        if self.is_attacking:
            finished = self.animate_atk(self.current_direction, loop=False)

            if finished:
                self.is_attacking = False
                self.stop() 

    def move_back (self):
        self.position = self.old_position
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom

    def get_image (self, x , y, x_rec = 215, y_rec = 320):
        from config import SPRITE_SCALE
        image = pygame.Surface([x_rec, y_rec])
        image.blit(self.sprite_sheet, (0,0), (x,y, x_rec, y_rec))
        image = pygame.transform.scale(image, (int(x_rec * SPRITE_SCALE), int(y_rec * SPRITE_SCALE)))
        return image
    
    def stop (self):
        if self.current_direction != "base":
            self.current_frame = 0
            self.current_direction = "base"
            self.image = self.animations["base"][0]

    def change_ani (self, nv_direction):
        if self.current_direction != nv_direction:
            self.current_frame = 0
            self.ani_counter = 0
            self.current_direction = nv_direction