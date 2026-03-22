import pygame

class AnimateSprite (pygame.sprite.Sprite):
    def __init__(self, name):
        super().__init__()
        self.sprite_sheet = pygame.image.load('anomalia_player/' + name + '.png')
        self.animations = { "base" : [], "droite" : [], "gauche": [], "haut" : [], "bas" : [], "attaque_haut" : [], "attaque_bas" : [], "attaque_gauche" : [], "attaque_droite" : []}
        self.anim_pnj = {"RAR" : []}
        self.remplit_player_anim()
        

    def remplit_player_anim (self):  
        """ 
        Récupère les sprites sheets du joueur et les ranges dans un dictiononaire de 
        clée : nom de l'action ; et de valeur : une liste des images
        """   
        self.animations["base"].append(self.get_image(240+1*550,240))
        self.animations["base"][0].set_colorkey([196,196,187])
        self.animations["base"].append(self.get_image(240,240))
        self.animations["base"][1].set_colorkey([196,196,187])

        for i in range (7):
            self.animations["droite"].append(self.get_image(240 + i*580, 1110))   
            self.animations["droite"][i].set_colorkey([196,196,187]) 
            
        for i in range (7):
            self.animations["gauche"].append(self.get_image(240 + i*580, 1980))   
            self.animations["gauche"][i].set_colorkey([196,196,187]) 

        for i in range (4):
            self.animations["haut"].append(self.get_image(240 + i*580, 2850))   
            self.animations["haut"][i].set_colorkey([196,196,187]) 

        for i in range (4):
            self.animations["bas"].append(self.get_image(240 + i*580, 3720))   
            self.animations["bas"][i].set_colorkey([196,196,187]) 
        
        for i in range (5):
            self.animations["attaque_droite"].append(self.get_image(200 + i*870, 5460, 700, 670))   
            self.animations["attaque_droite"][i].set_colorkey([196,196,187]) 
            
        for i in range (4):
            self.animations["attaque_gauche"].append(self.get_image(120 + i*870, 6330, 700, 670))   
            self.animations["attaque_gauche"][i].set_colorkey([196,196,187]) 

        for i in range (5):
            self.animations["attaque_haut"].append(self.get_image(1540 + i*870, 240, 800, 670))   
            self.animations["attaque_haut"][i].set_colorkey([196,196,187]) 

        for i in range (7):
            self.animations["attaque_bas"].append(self.get_image(160 + i*870, 4590, 770, 770))   
            self.animations["attaque_bas"][i].set_colorkey([196,196,187]) 
          
        
        self.current_frame = 0
        self.image = self.animations["base"][self.current_frame]
        self.rect = self.image.get_rect()  
        

        self.ani_counter = 0


    def animate (self, nom_direc, loop = True):
        """Permet de timer l'enchainement des images des animations de déplacement du joueur"""
        self.ani_counter +=1

        if self.ani_counter >= 50:  
            self.ani_counter = 0
            self.current_frame += 1

            if self.current_frame >= len(self.animations[nom_direc]):
                if loop :
                    self.current_frame = 0
                else:
                    self.current_frame = len(self.animations[nom_direc]) - 1
                    return True 

        self.image = self.animations[nom_direc][self.current_frame]
        return False
        
    def animate_atk (self, nom_direc, loop = True):
        """Permet de timer l'enchainement des images des animations de l'attaque"""
        self.ani_counter +=1

        if self.ani_counter >= 25:  
            self.ani_counter = 0
            self.current_frame += 1

            if self.current_frame >= len(self.animations[nom_direc]):
                if loop :
                    self.current_frame = 0
                else:
                    self.current_frame = len(self.animations[nom_direc]) - 1
                    return True 

        self.image = self.animations[nom_direc][self.current_frame]
        return False 
        
        