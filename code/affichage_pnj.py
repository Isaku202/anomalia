import pygame

class SpritePnj (pygame.sprite.Sprite):
    """Extrait les sprites des pnjs"""
    def __init__(self, name):
        super().__init__()
        pnjs = {"Léon": {"x": 270, "y": 90, "x_rect": 400, "y_rect": 770,"color": [196, 196, 187]}, 
                "Paul": {"x": 75, "y": 170, "x_rect": 860, "y_rect": 970,"color": [255, 255, 255]}}

        pnj = pnjs[name]
        
        self.sprite_sheet = pygame.image.load("PNJ/" + name + ".png")
        
        self.anim_pnj = []
        self.anim_pnj.append(self.get_image(pnj["x"], pnj["y"], pnj["x_rect"], pnj["y_rect"] ))
        self.anim_pnj[0].set_colorkey(pnj["color"])
        
        self.image = self.anim_pnj[0]
        self.rect = self.image.get_rect()

    def get_image(self, x, y, x_rec=400, y_rec=770): 
        image = pygame.Surface([x_rec, y_rec])
        image.blit(self.sprite_sheet, (0, 0), (x, y, x_rec, y_rec))
        return image