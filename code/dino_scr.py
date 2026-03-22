import pygame, os, sys
from Timer import Timer
from musique import EffetSonore
import Game_over_dino

def dino():
    """Affiche le screamer du dinosaure"""
    pygame.init()
    effets = EffetSonore()
    effets.charger("dino","dino.mp3")
    effets.set_volume(1)
    effets.jouer("dino")
    # Constantes
    LARGEUR, HAUTEUR = 800, 600
    FPS = 60

    # Chargement de l'image de fond
    chemin_script = os.path.dirname(os.path.abspath(__file__))
    chemin_image = os.path.join(chemin_script, "../objets/dino.jpg")
    fond_image = pygame.image.load(chemin_image)
    fond_image = pygame.transform.scale(fond_image, (LARGEUR, HAUTEUR))

    # Création de la fenêtre
    ecran = pygame.display.set_mode((LARGEUR, HAUTEUR))
    pygame.display.set_caption("Des fois... mieux vaux la mort")
    horloge = pygame.time.Clock()

    timer = Timer(500)
    en_cours = True
    timer.demarrer()
    
    while en_cours:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                en_cours = False
        
        if timer.est_fini():
            en_cours = False
        
        ecran.blit(fond_image, (0, 0))
        pygame.display.flip() 
        horloge.tick(FPS)  

    Game_over_dino.game_over()
    pygame.quit()
    sys.exit()
#Execute pour tester 
if __name__ == "__main__":
    dino()
    