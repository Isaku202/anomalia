import pygame


class Timer:
    def __init__(self, duree_ms):
        self.duree = duree_ms
        self.temps_debut = None
        self.actif = False
    
    def demarrer(self):
        """Démarre le timer"""
        self.temps_debut = pygame.time.get_ticks()
        self.actif = True
    
    def est_fini(self):
        """Vérifie si le timer est terminé"""
        if not self.actif:
            return False
        
        temps_actuel = pygame.time.get_ticks()
        if temps_actuel - self.temps_debut >= self.duree:
            self.actif = False
            return True
        return False
    