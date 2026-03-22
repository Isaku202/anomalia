import pygame, os 

class Musique:
    """Classe pour gérer la musique de fond"""
    def __init__(self):
        pygame.mixer.init()
        self.volume = 0.5
        self.is_playing = False
        self.current_track = None
        pygame.mixer.music.set_volume(self.volume)
        
    def charger(self, chemin):
        """Charge une musique de fond"""
        chemin_complet = os.path.join(os.path.dirname(__file__), "..", "sons", str(chemin))
        pygame.mixer.music.load(chemin_complet)
        self.current_track = chemin

    
    def jouer(self, loops=-1):
        """Lance la lecture de la musique"""
        pygame.mixer.music.play(loops=loops)
        self.is_playing = True
    
    def pause(self):
        """Met la musique en pause"""
        pygame.mixer.music.pause()
        self.is_playing = False
    
    def reprendre(self):
        """Reprend la musique après une pause"""
        pygame.mixer.music.unpause()
        self.is_playing = True
    
    def arreter(self):
        """Arrête complètement la musique"""
        pygame.mixer.music.stop()
        self.is_playing = False
    
    def set_volume(self, volume):
        """Définit le volume (0.0 à 1.0)"""
        self.volume = max(0.0, min(1.0, volume))
        pygame.mixer.music.set_volume(self.volume)
    
    def est_en_cours(self):
        """Vérifie si la musique est en cours de lecture"""
        return pygame.mixer.music.get_busy()


class EffetSonore:
    """Classe pour gérer les effets sonores"""
    def __init__(self, canaux=8):
        """Initialise le gestionnaire d'effets sonores
        canaux: nombre de sons pouvant être joués simultanément"""
        pygame.mixer.init()
        pygame.mixer.set_num_channels(canaux)
        self.sons = {}
        self.volume = 0.7
    
    def charger(self, nom, chemin):
        """Charge un effet sonore avec un nom"""
        son = pygame.mixer.Sound(os.path.join(os.path.dirname(__file__), "..", "sons", str(chemin)))
        son.set_volume(self.volume)
        self.sons[nom] = son
    
    def jouer(self, nom):
        """Joue un effet sonore par son nom"""
        if nom in self.sons:
            self.sons[nom].play()
    
    def set_volume(self, volume):
        """Définit le volume de tous les effets (0.0 à 1.0)"""
        self.volume = max(0.0, min(1.0, volume))
        for son in self.sons.values():
            son.set_volume(self.volume)
    
    def arreter(self, nom):
        """Arrête un effet sonore spécifique"""
        if nom in self.sons:
            self.sons[nom].stop()
    
    def arreter_tous(self):
        """Arrête tous les effets sonores"""
        pygame.mixer.stop()