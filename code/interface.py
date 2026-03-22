import pygame

def dessiner_coeur( x, y, taille, couleur): #généré par IA 
    """
    Dessine un cœur en style pixel art (comme Minecraft/Terraria)
    x, y = coin haut-gauche
    taille = taille d'un pixel du cœur
    couleur = couleur RGB du cœur
    """
    surface = pygame.display.get_surface()

    # Couleur noire pour le contour
    contour = (0, 0, 0)

    # Couleur plus claire pour le reflet (blanc)
    reflet = (255, 255, 255)

        # Matrice du cœur pixel art (1 = pixel plein, 0 = vide, 2 = reflet)
        # Format 15x13 pixels pour un beau cœur
    pixel_map = [
        [0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0],  # Ligne 0
        [0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0],  # Ligne 1
        [1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1],  # Ligne 2 (avec reflet)
        [1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],  # Ligne 3 (avec reflet)
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],  # Ligne 4
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],  # Ligne 5
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],  # Ligne 6
        [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],  # Ligne 7
        [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0],  # Ligne 8
        [0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0],  # Ligne 9
        [0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0],  # Ligne 10
        [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],  # Ligne 11
    ]

        # Dessiner d'abord le contour noir (décalé de 1 pixel dans toutes les directions)
    for ligne_idx, ligne in enumerate(pixel_map):
        for col_idx, pixel in enumerate(ligne):
            if pixel > 0:  # Si c'est un pixel plein
                px = x + col_idx * taille
                py = y + ligne_idx * taille
                # Dessiner le contour noir autour
                # Vérifier les pixels adjacents pour dessiner le contour uniquement sur les bords
                # Haut
                if ligne_idx == 0 or pixel_map[ligne_idx - 1][col_idx] == 0:
                    pygame.draw.rect(surface, contour, (px, py - taille, taille, taille))
                # Bas
                if ligne_idx == len(pixel_map) - 1 or pixel_map[ligne_idx + 1][col_idx] == 0:
                    pygame.draw.rect(surface, contour, (px, py + taille, taille, taille))
                # Gauche
                if col_idx == 0 or pixel_map[ligne_idx][col_idx - 1] == 0:
                    pygame.draw.rect(surface, contour, (px - taille, py, taille, taille))
                # Droite
                if col_idx == len(ligne) - 1 or pixel_map[ligne_idx][col_idx + 1] == 0:
                    pygame.draw.rect(surface, contour, (px + taille, py, taille, taille))
                # Coins
                if ligne_idx > 0 and col_idx > 0 and pixel_map[ligne_idx - 1][col_idx] == 0 and pixel_map[ligne_idx][col_idx - 1] == 0:
                    pygame.draw.rect(surface, contour, (px - taille, py - taille, taille, taille))
                if ligne_idx > 0 and col_idx < len(ligne) - 1 and pixel_map[ligne_idx - 1][col_idx] == 0 and pixel_map[ligne_idx][col_idx + 1] == 0:
                    pygame.draw.rect(surface, contour, (px + taille, py - taille, taille, taille))
                if ligne_idx < len(pixel_map) - 1 and col_idx > 0 and pixel_map[ligne_idx + 1][col_idx] == 0 and pixel_map[ligne_idx][col_idx - 1] == 0:
                    pygame.draw.rect(surface, contour, (px - taille, py + taille, taille, taille))
                if ligne_idx < len(pixel_map) - 1 and col_idx < len(ligne) - 1 and pixel_map[ligne_idx + 1][col_idx] == 0 and pixel_map[ligne_idx][col_idx + 1] == 0:
                    pygame.draw.rect(surface, contour, (px + taille, py + taille, taille, taille))
        # Dessiner le cœur principal
    for ligne_idx, ligne in enumerate(pixel_map):
        for col_idx, pixel in enumerate(ligne):
            if pixel > 0:  # Si c'est un pixel plein
                px = x + col_idx * taille
                py = y + ligne_idx * taille
                # Choisir la couleur (reflet blanc ou couleur normale)
                couleur_pixel = reflet if pixel == 2 else couleur
                # Dessiner le pixel
                pygame.draw.rect(surface, couleur_pixel, (px, py, taille, taille))

def dessiner_potion( x, y, verre,verre_contour,liquide,liquide_ombre, bouchon, bouchon_ombre,reflet,taille=1): #généré par IA puis modifié a la main
    
        """
        Dessine une potion stylisée (style simple, liquide bien contenu).
        (x, y) = coin haut-gauche du dessin
            taille = scale (1, 2, 0.5, etc.)
     """
        surface = pygame.display.get_surface()
    
        t = taille


        # Dimensions de base
        largeur = int(40 * t)
        hauteur = int(55 * t)

        # === CORPS (bouteille) D'ABORD ===
        corps = pygame.Rect(x + int(6*t), y + int(16*t), int(28*t), int(34*t))
        pygame.draw.rect(surface, verre, corps, border_radius=int(10*t))

        # === LIQUIDE PAR-DESSUS (dans le corps) ===
        # Liquide dans le corps - BIEN À L'INTÉRIEUR et ne déborde pas en bas
        liquide_rect = pygame.Rect(
            corps.x + int(3*t),
            corps.y + int(14*t),
            corps.w - int(6*t),
            corps.h - int(17*t)  # Réduit pour ne pas dépasser en bas
        )
        pygame.draw.rect(surface, liquide, liquide_rect, border_radius=int(8*t))

    # Partie foncée en haut (pour l'effet de profondeur)
        ombre_h = int(liquide_rect.h * 0.4)  # 40% du haut
        ombre_rect = pygame.Rect(
            liquide_rect.x, 
            liquide_rect.y, 
            liquide_rect.w, 
            ombre_h
        )
        pygame.draw.rect(surface, liquide_ombre, ombre_rect, border_radius=int(8*t))

        # === CONTOUR DU CORPS (par-dessus tout) ===
        pygame.draw.rect(surface, verre_contour, corps, width=max(1, int(2*t)), border_radius=int(10*t))

        # === COL (goulot) ===
        col = pygame.Rect(x + int(14*t), y + int(6*t), int(12*t), int(16*t))
        pygame.draw.rect(surface, verre, col, border_radius=int(5*t))
        pygame.draw.rect(surface, verre_contour, col, width=max(1, int(2*t)), border_radius=int(5*t))
        
    # === BOUCHON ===
        b = pygame.Rect(x + int(12*t), y + int(0*t), int(16*t), int(10*t))
        pygame.draw.rect(surface, bouchon, b, border_radius=int(4*t))
        pygame.draw.rect(surface, bouchon_ombre, b, width=max(1, int(2*t)), border_radius=int(4*t))

        # === REFLETS ===
        # Reflet principal (sur le verre)
        reflet_rect = pygame.Rect(corps.x + int(5*t), corps.y + int(6*t), int(5*t), int(18*t))
        pygame.draw.rect(surface, reflet, reflet_rect, border_radius=int(4*t))

        # Petit highlight sur le col
        pygame.draw.line(
            surface, reflet,
            (col.x + int(3*t), col.y + int(3*t)),
            (col.x + int(3*t), col.y + int(12*t)),
            max(1, int(2*t))
        )





        