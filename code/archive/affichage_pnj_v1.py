import pygame

class SpritePnj (pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.anim_pnj = {}
        self.ajoute_pnj("Léon", 270, 90, [196,196,187])
        self.ajoute_pnj("Paul", 0, 90, [255, 255, 255])

    def ajoute_pnj(self, name, x, y, color):
        # Charger un sprite_sheet UNIQUE pour chaque PNJ
        sprite_sheet_pnj = pygame.image.load("PNJ/" + name + ".png")

        self.anim_pnj[name] = []
        # Utiliser le sprite_sheet spécifique au PNJ
        self.anim_pnj[name].append(self.get_image(sprite_sheet_pnj, x, y))
        self.anim_pnj[name][0].set_colorkey(color) 

        # Initialiser l'image avec Léon par défaut (le premier ajouté)
        if not hasattr(self, 'image'):
            self.image = self.anim_pnj[name][0]
            self.rect = self.image.get_rect()  

    def get_image(self, sprite_sheet, x, y, x_rec=400, y_rec=770): 
        image = pygame.Surface([x_rec, y_rec])
        image.blit(sprite_sheet, (0,0), (x, y, x_rec, y_rec))
        return image