import pygame


def dessiner_texte_contour(surface, texte, font, couleur_texte, couleur_contour, centre, epaisseur=2):
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
