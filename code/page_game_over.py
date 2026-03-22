from Timer import Timer
import pygame
import sys, asyncio
from musique import EffetSonore
from utils import dessiner_texte_contour



async def game_over ():
    pygame.init()
    effets = EffetSonore()
    effets.charger("ah","oh_non.ogg")
    effets.jouer("ah")

    # Constantes
    LARGEUR, HAUTEUR = 800, 600
    FPS = 60

    # Couleurs
    NOIR = (0, 0, 0)
    BLANC = (255, 255, 255)
    ROUGE = (200, 50, 50)


    # Création de la fenêtre
    ecran = pygame.display.set_mode((LARGEUR, HAUTEUR))
    pygame.display.set_caption("Menu Principal - Anomalia")
    horloge = pygame.time.Clock()

    # Polices
    font_titre = pygame.font.Font(None, 130)
    font_petit = pygame.font.Font(None, 40)


    def dessiner_fond():
        """Dessine le fond en affichant un fond noir"""
        ecran.fill(NOIR)

    # Boucle principale
    timer = Timer(5000)
    en_cours = True
    timer.demarrer()
    while en_cours:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                en_cours = False
        if timer.est_fini() : 
            en_cours = False

        # Dessin
        dessiner_fond()

        # Titre du jeu avec contour
        dessiner_texte_contour(ecran, "GAME OVER", font_titre, ROUGE, BLANC,(LARGEUR // 2, 200), epaisseur=3)

        # Sous-titre avec contour
        dessiner_texte_contour(ecran, "Je t'attendrai... de L'autre côté...", font_petit, BLANC, NOIR,(LARGEUR // 2, 280), epaisseur=2)

        # Mise à jour de l'écran
        pygame.display.flip()
        horloge.tick(FPS)

        await asyncio.sleep(0)