import pygame


class AnimateSpriteMonstre (pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.sprite_sheet = pygame.image.load('monstre/slime.png')
        self.anim_monstre = {}
        self.ajoute_monstre("slime", 90)

    def ajoute_monstre(self, name, y):
        """Extrait les sprites des monstres et les ranges dans 
        le dictionnaire de liste en fonction de leurs utilité
        """

        self.anim_monstre[name] = {"mouvement" : [], "attaque" : []}
        for i in range (4):
            self.anim_monstre[name]["mouvement"].append(self.get_image(1150+i*580,y))
            self.anim_monstre[name]["mouvement"][i].set_colorkey([196,196,187]) 
        for i in range (4):
            self.anim_monstre[name]["mouvement"].append(self.get_image(1150+i*580,y+290))
            self.anim_monstre[name]["mouvement"][i+4].set_colorkey([196,196,187]) 
        for i in range (4):
            self.anim_monstre[name]["mouvement"].append(self.get_image(1150+i*580,y+570))
            self.anim_monstre[name]["mouvement"][i+8].set_colorkey([196,196,187]) 
        for i in range (3):
            self.anim_monstre[name]["mouvement"].append(self.get_image(1150+i*580,y+870))
            self.anim_monstre[name]["mouvement"][i+12].set_colorkey([196,196,187]) 
        
        self.anim_monstre[name]["attaque"].append(self.get_image(1150+3*580,y+870))
        self.anim_monstre[name]["attaque"][0].set_colorkey([196,196,187]) 
        self.current_frame = 0
        self.image = self.anim_monstre[name]["mouvement"][self.current_frame]
        self.rect = self.image.get_rect()  
        

        self.ani_counter = 0

    def animate (self, nom_monstre, loop = True):
        """Permet de timer l'enchainement des images des animations de déplacement"""
        self.ani_counter +=1

        if self.ani_counter >= 50:  
            self.ani_counter = 0
            self.current_frame += 1

            if self.current_frame >= len(self.anim_monstre[nom_monstre]):
                if loop :
                    self.current_frame = 0
                else:
                    self.current_frame = len(self.anim_monstre[nom_monstre]) - 1
                    return True 

        self.image = self.anim_monstre[nom_monstre]["mouvement"][self.current_frame]
        return False
      
    def animate_atk (self, loop = True, name = "slime"):
        """Permet de timer l'animation de l'attaque"""
        self.ani_counter +=1

        if self.ani_counter >= 45:  
            if not loop :
                return True
            
        self.image = self.anim_monstre[name]["attaque"][0]
        return False


    def get_image (self, x , y, x_rec = 370, y_rec = 220): 
        """renvoie l'image coupée"""
        image = pygame.Surface([x_rec, y_rec])
        image.blit(self.sprite_sheet, (0,0), (x,y, x_rec, y_rec))
        return image