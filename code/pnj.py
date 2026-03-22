import pygame
from affichage_pnj import SpritePnj 
from character import Character
from quete import Quete
from inventaire import convertisseur_en_Item, Items

class Pnj(SpritePnj, Character):
    def __init__(self, name, x, y, nb_points=0):
        SpritePnj.__init__(self, name)
        self.init_character(name, x, y, 400, nb_points, speed=3)
        self.texts = {}
        self.etat_quete_leon = "base"
        self.etat_quete_paul = "base"
        
        # Initialiser les objets Quete dès le début
        self.quete_de_leon = None
        self.quete_de_paul = None


#BLABLA de LEON
        self.ajoute_dialoge("Léon", [
            "Toi.", 
            "T'es qui ?",
            "Tu n'as rien a faire ici.", 
            "Est-ce que tu serais...",
            "Ne m'approche pas !", 
            "*soupire*",
            "Quoique...", 
            "Amène moi 4 viandes et 2 carrotes. Si tu le fais je te conseilerais... peut-être.",
            "Vas, surtout n'oublit pas... cdhvsqjK&Â§!Ã¨ @Ã¹$Ã´$kÃ¹p^$^@mlÃ¹ $^p$ $ok^@ $^@"], 
            
            "base")
        
        self.ajoute_dialoge("Léon", [
            "Amène moi 4 viandes et 2 carrotes. Si tu le fais je te conseilerais... peut-être.",
            "Vas, surtout n'oublit pas... cdhvsqjK&Â§!Ã¨ @Ã¹$Ã´$kÃ¹p^$^@mlÃ¹ $^p$ $ok^@ $^@"],
            
            "en cours")

        self.ajoute_dialoge("Léon", [
            "Ah, encore toi.",
            "Tu les as ?",
            "Bien. Donne. De suite.",
            "*crounch, crounch, crounch*", 
            "Tsk",
            "Mouais. Même si je ne devrais pas te le dire...",
            "Fais très attention aux autres anomalies. Elles pouraient te... arf", 
            "Au moins...", 
            "Sache que si tu dis 'Z' alors tu guériras.", 
            "Mais attention. Tu n'as que trois chances."], 
            
            "recu")

        self.ajoute_dialoge("Léon", [
            "Arf...", 
            "MAIS CASSES TOI !", 
            "FOUS MOI LA PAIX !"], 
        
            "apres")

#BLABLA de PAUL
        self.ajoute_dialoge("Paul", [
            "Toi.", 
            "T'es une anomalie aussi..?",
            "Tu n'as rien a faire ici.", 
            "Aide moi...", 
            "*hesitation*",
            "Dis... ", 
            "Si tu m'amenes 4 de ces especes de liquides bleus, je te dirais comment t'échapper.", 
            "Fais moi confiance.", 
            "Fais moi confiance..."], 
            
            "base")
        
        self.ajoute_dialoge("Paul", [
            "Si tu m'amenes 4 de ces especes de liquides bleus, je te dirais comment t'échapper.", 
            "Fais moi confiance."],
            
            "en cours")

        self.ajoute_dialoge("Paul", [
            "*surpris* Tu... Tu les as troués ?", 
            "*les recupÃ¨res*", 
            "Hah, merci anomalie.", 
            "*L'air est lourd*", 
            "*sourire tordu et bugé*", 
            "tsk.", 
            "Revient me voir avec du liquide rouge", 
            "*il boit l'étrange liquide bleu*"], 
        
            "recu")

        self.ajoute_dialoge("Paul", [
            "*Le sol tremble*", 
            "*son sourire est completement bugé et distordu*", 
            "*soudain il me saute à la gorge*",
            "RRRRROOOOOAAAAARRRRRRRRR"], 
            
            "apres")
        
    def ajoute_pnj (self, name):
        if name not in self.texts:
            self.texts[name] = {"base" : [], "en cours" : [], "recu" : [], "apres" : []}

    def ajoute_dialoge (self, name, text, etat_quete):
        self.ajoute_pnj(name)

        for i in range (len(text)):
            self.texts[name][etat_quete].append(text[i])
        return

    def dialoge (self, name, etat_quete):
        return self.texts[name][etat_quete]

    def quete_leon(self, player):
        conditions = {"viande": 4, "carrote": 2}
        recompense = ("clef étrange", 1)
        recompense_item = convertisseur_en_Item(recompense)

        if self.quete_de_leon is None:
            self.quete_de_leon = Quete(recompense, conditions)
        
        if self.quete_de_leon.remplit(player):
            self.quete_de_leon.recupere_recompense(player, recompense_item)
            return True
        return False


    def quete_paul(self, player):
        conditions = {"sang étrange bleu": 4}  
        recompense = ("plume", 1)
        recompense_item = convertisseur_en_Item(recompense)

        if self.quete_de_paul is None:
            self.quete_de_paul = Quete(recompense, conditions)
        
        if self.quete_de_paul.remplit(player):
            self.quete_de_paul.recupere_recompense(player, recompense_item)
            return True
        return False


    def move(self):
        Character.move(self)

    def move_right(self):
        Character.move_right(self)

    def move_left(self):
        Character.move_left(self)

    def move_up(self):
        Character.move_up(self)

    def move_down(self):
        Character.move_down(self)
    
    def charger_points(self, map_manager, map_name):
        Character.charger_points(self, map_manager, map_name)

    def update(self):
        """Met à jour la position du pnj"""
        Character.update(self)

    def move_back(self):
        """Retour à l'ancienne position en cas de collision"""
        Character.move_back(self)

    def save_location(self):
        """Sauvegarde la position actuelle"""
        Character.save_location(self)

    def change_ani(self, nv_direction):
        Character.change_ani(self, nv_direction)