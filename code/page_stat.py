import pygame 

import os


LARGEUR, HAUTEUR = 400, 600
FPS = 60

# Chargement de l'image de fond
chemin_script = os.path.dirname(os.path.abspath(__file__))
chemin_image = os.path.join(chemin_script, "fenetre_stat_fond.png")

fond_image = pygame.image.load(chemin_image)
fond_image = pygame.transform.scale(fond_image, (LARGEUR, HAUTEUR))

font_petit = pygame.font.Font(None, 30)






