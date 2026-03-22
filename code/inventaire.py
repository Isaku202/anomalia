import random, pygame, os

def convertisseur_en_Item(item_tuple):
    """Convertit un tuple (nom, quantité) en objet Items"""
    return Items(item_tuple[0], item_tuple[1])

class Affichage_Items : 
    def __init__(self):
        self.font = pygame.font.Font(os.path.join(os.path.dirname(__file__), "..", "objets/Mistral.ttf"), 24)

        self.items = {
            "sang étrange" : None,
            "sang étrange bleu" : None,

            "livre vert" : None,
            "livre rouge" : None,
            "livre bleu" : None,
            "clef étrange" : None,

            "cailloux" : None,
            "lettre" : None,
            "plume" : None,
            "caca" : None,

            "eau" : None,
            "feu" : None,
            "poulet" : None,
            "pomme" : None,
            "viande" : None,
            "carrote" : None
        }
        self.img_ref = pygame.image.load(os.path.join(os.path.dirname(__file__), "..", "objets/items.png"))
        self.tout_charger()
    
    def tout_charger(self):   
        #ligne 1 sprite 
        self.charger_items("sang étrange", 60, 155)
        self.charger_items("sang étrange bleu", 105*3 + 60, 155)

        #ligne 2 sprite 
        self.charger_items("livre vert", 60, 105*1+155)
        self.charger_items("livre rouge", 165, 105*1+155)
        self.charger_items("livre bleu", 105*2 + 60, 105*1+155)
        self.charger_items("clef étrange", 105*5 + 60, 105*1+155)
        
        #ligne 3 sprite 
        self.charger_items("cailloux", 60, 105*2+155)
        self.charger_items("lettre", 165, 105*2+155)
        self.charger_items("plume", 105*4 + 60, 105*2+155)
        self.charger_items("caca", 105*5 + 60, 105*2+155)

        #ligne 4 sprite 
        self.charger_items("eau", 60, 105*3+155)
        self.charger_items("feu", 165, 105*3+155)
        self.charger_items("poulet", 105*2 + 60, 105*3+155)
        self.charger_items("pomme", 105*3 + 60, 105*3+155)
        self.charger_items("viande", 105*4 + 60, 105*3+155)
        self.charger_items("carrote", 105*5 + 60, 105*3+155)
    
    
    def charger_items (self, name, x, y):
        self.items[name] = [self.get_image(x, y, 100, 100), 0]
        self.items[name][0].set_colorkey([255, 255, 255])

    def get_image(self, x, y, x_rec, y_rec):
        """Extrait une portion de l'image"""
        image = pygame.Surface([x_rec, y_rec])
        image.blit(self.img_ref, (0, 0), (x, y, x_rec, y_rec))
        return image

    def transfert_items  (self):
        return self.items

    def render(self, screen, name, x, y):
        x = 75*x+95
        y = 75*y +100
        img = pygame.transform.scale(self.items[name][0], (80, 80))
        screen.blit(img, (x, y))

        text = self.font.render("X" + str(self.items[name][1]), False, (255,255,255))
        screen.blit(text, (x + 50, y + 50))

class Items :
    affichage_partagee = None
    def __init__(self, name, quantité):
        self.name = name
        self.quantity = quantité
        if Items.affichage_partagee is None:
            Items.affichage_partagee = Affichage_Items()
        self.img = Items.affichage_partagee

class Affichage_Inventaire  :
    def __init__(self):
        self.items = Affichage_Items().transfert_items()
        self.inv_box = pygame.image.load(os.path.join(os.path.dirname(__file__), "..", "inventaire/inventaire_case.png"))
        self.inv_box = pygame.transform.scale(self.inv_box, (800, 550))
        self.inv_box.set_colorkey([255, 255, 255])
        self.en_cours = False
        self.matrice = [[None for i in range(8)] for j in range(4)]

        

    def recherche_prochain_emplacement(self):
        for j in range(4):
            for i in range(8):
                if self.matrice[j][i] is None:
                    return i, j
        return None

    def ajout_matrice(self, item):
        result = self.recherche_prochain_emplacement()
        if result is None:
            return False
        
        i, j = result
        self.matrice[j][i] = item
        return True
    
    def retire_matrice(self, name):
        for j in range(4):
            for i in range(8):
                if self.matrice[j][i] is not None and self.matrice[j][i].name == name:
                    self.matrice[j][i] = None
                    return

    def est_ouvert(self):
        """verifie si l'inventaire est ouvert"""
        return self.en_cours

    def ouvre_inventaire(self):
        """affiche l'inventaire à l'écran"""
        self.en_cours = True 

    def ferme_inventaire(self):
        """ferme l'inventaire à l'écran"""
        self.en_cours = False

    def get_image(self, x, y, x_rec, y_rec):
        """Extrait une portion de l'image"""
        image = pygame.Surface([x_rec, y_rec])
        image.blit(self.inv_box, (0, 0), (x, y, x_rec, y_rec))
        return image

    def render(self, screen):
        if self.en_cours: 
            screen.blit(self.inv_box, (0, 0))
            
            for j in range(4):
                for i in range(8):
                    item = self.matrice[j][i]
                    if item is not None:
                        x = 75*i+95
                        y = 75*j +100
                        img = pygame.transform.scale(item.img.items[item.name][0], (80, 80))
                        screen.blit(img, (x, y))
                        
                        text = item.img.font.render("X" + str(self.items[item.name][1]), False, (255,255,255))
                        screen.blit(text, (x + 50, y + 50))

                        


class Inventaire(Affichage_Inventaire): 
    def __init__(self, items=[]):
        super().__init__()
        self.items_liste = items
        self.charge_items()

    def charge_items(self):
        for item in self.items_liste:
            self.ajoute_item(item)

    def convertisseur_en_Item (self, item):
        """On sait jamais."""
        return Items(item[0], item[1])


    def ajoute_item(self, item):
        """ajoute l'item dans l'inventaire"""
        if item.name not in self.items.keys():
            return
        
        if self.items[item.name][1] == 0:
            self.items[item.name][1] = item.quantity
            self.ajout_matrice(item)
        else:
            self.items[item.name][1] += item.quantity
    
    def retire_item(self, name, nb):
        self.items[name][1] -= nb
        if self.items[name][1] == 0:
            self.retire_matrice(name)


    def drop_items(self, liste_obj, maxi):
        """drop un item aléatoire au sein d'une liste d'objet et l'ajoute à l'inventaire"""
        nouvel_item = Items(random.choice(liste_obj), random.randint(1, maxi))
        self.ajoute_item(nouvel_item)
        return nouvel_item