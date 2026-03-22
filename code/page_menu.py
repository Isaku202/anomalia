# Créé par nsi, le 01/12/2025 en Python 3.7
from game import Game # type: ignore
from musique import Musique # type: ignore
import pygame, sys, os, asyncio

async def menu():
    pygame.init()
    try:
        mus = Musique()
        mus.charger("guitar_chelou.ogg")
        mus.set_volume(0.7)
        mus.jouer()
    except Exception:
        pass

    # Constante
    LARGEUR, HAUTEUR = 800, 600
    FPS = 60

    # Couleurs
    NOIR = (0, 0, 0)
    BLANC = (255, 255, 255)
    GRIS = (150, 150, 150)
    ROUGE = (200, 50, 50)
    OR = (255, 215, 0)

    # Chargement de l'image de fond
    chemin_script = os.path.dirname(os.path.abspath(__file__))
    chemin_image = os.path.join(chemin_script, "page_acceuil.png")

    fond_image = pygame.image.load(chemin_image)
    fond_image = pygame.transform.scale(fond_image, (LARGEUR, HAUTEUR))

    # Création de la fenêtre
    ecran = pygame.display.set_mode((LARGEUR, HAUTEUR))
    pygame.display.set_caption("Menu Principal - Anomalia")
    horloge = pygame.time.Clock()

    # Polices
    font_titre = pygame.font.Font(None, 80)
    font_menu = pygame.font.Font(None, 50)
    font_petit = pygame.font.Font(None, 30)

    class Bouton: #IA
        def __init__(self, x, y, texte, largeur=300, hauteur=60):
            self.rect = pygame.Rect(x, y, largeur, hauteur)
            self.texte = texte
            self.couleur = GRIS
            self.survol = False

        def dessiner(self, surface):
            couleur = OR if self.survol else self.couleur
            pygame.draw.rect(surface, couleur, self.rect)
            pygame.draw.rect(surface, BLANC, self.rect, 3)
            texte_surface = font_menu.render(self.texte, True, NOIR if self.survol else BLANC)
            texte_rect = texte_surface.get_rect(center=self.rect.center)
            surface.blit(texte_surface, texte_rect)

        def verifier_survol(self, pos_souris):
            self.survol = self.rect.collidepoint(pos_souris)
            return self.survol

        def est_clique(self, pos_souris, event):
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                return self.rect.collidepoint(pos_souris)
            return False

    # Création des boutons
    boutons = [
        Bouton(LARGEUR // 3.5 - 150, 350, "Commencer"),
    ]

    def dessiner_texte_contour(surface, texte, font, couleur_texte, couleur_contour, centre, epaisseur=2): #IA
        """Dessine un texte avec un contour pour une meilleure lisibilité"""
        for dx in range(-epaisseur, epaisseur + 1):
            for dy in range(-epaisseur, epaisseur + 1):
                if dx != 0 or dy != 0:
                    texte_contour = font.render(texte, True, couleur_contour)
                    rect_contour = texte_contour.get_rect(center=(centre[0] + dx, centre[1] + dy))
                    surface.blit(texte_contour, rect_contour)
        texte_surface = font.render(texte, True, couleur_texte)
        texte_rect = texte_surface.get_rect(center=centre)
        surface.blit(texte_surface, texte_rect)

    def dessiner_fond():
        """Dessine le fond en usant de l'image
        importée et si erreur alors affiche un fond noir"""
        if fond_image:
            ecran.blit(fond_image, (0, 0))
        else:
            ecran.fill(NOIR)

    # Boucle principale
    en_cours = True
    while en_cours:
        pos_souris = pygame.mouse.get_pos() #IA

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                en_cours = False

            # Vérification des clics sur les boutons (IA)
            for i, bouton in enumerate(boutons):
                if bouton.est_clique(pos_souris, event):
                    #MOI
                    if i == 0:
                        pygame.mixer.music.stop()
                        pygame.mixer.stop()
                        pygame.mixer.quit()
                        await asyncio.sleep(0.3)
                        pygame.mixer.init()
                        pygame.init()
                        game = Game()
                        await game.run()
                    elif i == 3:
                        en_cours = False
                    #FIN MOI

        # Dessin
        dessiner_fond()

        # Titre du jeu avec contour
        dessiner_texte_contour(ecran, "Anomalia", font_titre, OR, GRIS,(LARGEUR // 3.75, 100), epaisseur=3)

        # Sous-titre avec contour
        dessiner_texte_contour(ecran, "Je t'attendrai... de L'autre côté", font_petit, BLANC, GRIS,(LARGEUR // 3.75, 170), epaisseur=2)

        # Dessin des boutons
        for bouton in boutons:
            bouton.verifier_survol(pos_souris)
            bouton.dessiner(ecran)

        # Mise à jour de l'écran
        pygame.display.flip()
        horloge.tick(FPS)

        await asyncio.sleep(0)

    pygame.quit()
