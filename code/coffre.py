import pygame, os


class Drop_Coffre :
    """Stuff possible dans un coffre"""
    def __init__(self):
        self.possible = ["livre vert",
                         "livre rouge",
                         "livre bleu" ,
                         "clef étrange" ,
                         "cailloux",
                         "lettre",
                         "plume",
                         "caca"]



class Coffre (pygame.sprite.Sprite):
    def __init__(self, coordonnées):
        super().__init__()
        self.type = None
        self.coord_x = coordonnées.x
        self.coord_y = coordonnées.y
        self.image = pygame.image.load(os.path.join(os.path.dirname(__file__), "..", "objets/coffre.png"))
        self.image = pygame.transform.scale(self.image, (int(coordonnées.width), int(coordonnées.height)))
        self.rect = self.image.get_rect()
        self.rect.x = coordonnées.x
        self.rect.y = coordonnées.y
        self.position = [coordonnées.x, coordonnées.y]
        self.feet = pygame.Rect(0, 0, self.rect.width, self.rect.height)
        self.feet.midbottom = self.rect.midbottom
        self.ouvert = False

    def ouvrir(self):
        """Ouvre le coffre et change son apparence"""
        self.ouvert = True
        self.image.set_alpha(100)
