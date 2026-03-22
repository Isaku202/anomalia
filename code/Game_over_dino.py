from Timer import Timer
import pygame
import sys


def game_over ():
    """Affiche la fenetre de game over lié au dino"""
    pygame.init()
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


    def dessiner_texte_contour(surface, texte, font, couleur_texte, couleur_contour, centre, epaisseur=2):
        """Dessine un texte avec un contour pour une meilleure lisibilité"""
        # Dessiner le contour (en décalant le texte dans toutes les directions)
        for dx in range(-epaisseur, epaisseur + 1):
            for dy in range(-epaisseur, epaisseur + 1):
                if dx != 0 or dy != 0:  # Ne pas dessiner au centre
                    texte_contour = font.render(texte, True, couleur_contour)
                    rect_contour = texte_contour.get_rect(center=(centre[0] + dx, centre[1] + dy))
                    surface.blit(texte_contour, rect_contour)

        #Dessiner le texte principal par-dessus
        texte_surface = font.render(texte, True, couleur_texte)
        texte_rect = texte_surface.get_rect(center=centre)
        surface.blit(texte_surface, texte_rect)

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
        dessiner_texte_contour(ecran, "Des fois... mieux vaut la mort.", font_petit, BLANC, NOIR,(LARGEUR // 2, 280), epaisseur=2)

        # Mise à jour de l'écran
        pygame.display.flip()
        horloge.tick(FPS)

    pygame.quit()
    sys.exit()