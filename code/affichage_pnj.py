import pygame
from config import SPRITE_SCALE

S = 0.5  # facteur d'échelle des sprite sheets redimensionnées

class SpritePnj (pygame.sprite.Sprite):
    """Extrait les sprites des pnjs"""
    def __init__(self, name):
        super().__init__()
        # Léon a été redimensionné (S=0.5), Paul non (coordonnées originales)
        pnjs = {"Léon": {"x": int(270*S), "y": int(90*S), "x_rect": int(400*S), "y_rect": int(770*S),"color": [196, 196, 187]},
                "Paul": {"x": int(75*S), "y": int(170*S), "x_rect": int(860*S), "y_rect": int(970*S),"color": [255, 255, 255]}}

        pnj = pnjs[name]

        self.sprite_sheet = pygame.image.load("PNJ/" + name + ".png")

        self.anim_pnj = []
        self.anim_pnj.append(self.get_image(pnj["x"], pnj["y"], pnj["x_rect"], pnj["y_rect"] ))
        self.anim_pnj[0].set_colorkey(pnj["color"])

        self.image = self.anim_pnj[0]
        self.rect = self.image.get_rect()

    def get_image(self, x, y, x_rec=200, y_rec=385):
        image = pygame.Surface([x_rec, y_rec])
        image.blit(self.sprite_sheet, (0, 0), (x, y, x_rec, y_rec))
        image = pygame.transform.scale(image, (int(x_rec * SPRITE_SCALE), int(y_rec * SPRITE_SCALE)))
        return image
