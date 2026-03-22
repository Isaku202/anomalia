import random, pygame, os

class Affichage_Items : 
    def __init__(self):
        self.items = {}
        self.img_ref = pygame.image.load(os.path.join(os.path.dirname(__file__), "..", "objets/items.png"))
        #self.img_ref = pygame.transform.scale(self.img_ref, (800, 550))
        #self.img_ref.set_colorkey([255, 255, 255])
        self.charger_items("sang étrange", 60, 155)
        self.charger_items("sang étrange bleu", 165, 155)
    
    def charger_items (self, name, x, y):
        self.items[name] = self.get_image(x, y, 100, 100)
        self.items[name].set_colorkey([255, 255, 255])

    def get_image(self, x, y, x_rec, y_rec):
        """Extrait une portion de l'image"""
        image = pygame.Surface([x_rec, y_rec])
        image.blit(self.img_ref, (0, 0), (x, y, x_rec, y_rec))
        return image

    def render(self, screen, name, x, y):
        screen.blit(self.items[name], (150*x+65, 10*y +85))

class Items :
    def __init__(self, name, quantité):
        self.name = name
        self.quantity = quantité
        self.img = Affichage_Items()

class Affichage_Inventaire :
    def __init__(self):
        self.inv_box = pygame.image.load(os.path.join(os.path.dirname(__file__), "..", "inventaire/inventaire_case.png"))
        self.inv_box = pygame.transform.scale(self.inv_box, (800, 550))
        self.inv_box.set_colorkey([255, 255, 255])
        self.en_cours = False
        self.items = Affichage_Items()
        self.matrice = [[None for i in range (8)],
                        [None for i in range (8)], 
                        [None for i in range (8)], 
                        [None for i in range (8)]]
        
        for i in range (4):
            print (self.matrice[i])

    def recherche_prochain_emplacement(self):
        current = self.matrice[0][0]
        i = 0
        j = 0
        while current != None :
            if i >= 8 : 
                if j >= 4 : 
                    return "plein mais ça arrive jamais"
                else : 
                    i = 0
                    j += 1
            else : 
                i += 1
            current = self.matrice[i][j]
        print(i, j)
        return i, j

    def ajout_matrice (self, item):
        print ("entre dans ajout matrice")
        i, j  = self.recherche_prochain_emplacement()
        self.matrice[i][j] = item
        print("Objet ajouté")

            
    def est_ouvert(self):
        """verifie si l'inventaire est ouvert"""
        return self.en_cours

    def ouvre_inventaire (self):
        """affiche l'inventaire à l'écran"""
        print("ouvert")
        self.en_cours = True 

    def ferme_inventaire (self):
        """ferme l'inventaire à l'écran"""
        print("fermé")
        self.en_cours = False

    def get_image(self, x, y, x_rec, y_rec):
        """Extrait une portion de l'image"""
        image = pygame.Surface([x_rec, y_rec])
        image.blit(self.inv_box, (0, 0), (x, y, x_rec, y_rec))
        return image

    def render(self, screen):
        if self.en_cours: 
            screen.blit(self.inv_box, (0, 0))
            current = self.matrice[0][0]
            i = 0
            j = 0
            while current != None :
                if i >= 8 : 
                    if j >= 4 : 
                        return "plein mais ça arrive jamais"
                    else : 
                        i = 0
                        j += 1
                else : 
                    i += 1
                current.img.render(screen, current.name, i, j)
                current = self.matrice[i][j]



class Inventaire (Affichage_Inventaire) : 
    def __init__(self, items = []):
        super().__init__()
        self.inventaire = {}
        self.items = items
        print(items)
        self.charge_items()
        print(items)
        for i in range (4):
            print (self.matrice[i])

    def charge_items (self):
        for item in self.items :
            self.ajoute_item(item)
            
#Items("sang étrange", 1)

    def ajoute_item (self, item):
        """ajoute l'item dans l'inventaire"""
        print("ajoute l'item à la matrice et au dico")
        if item.name not in self.inventaire.keys():
            self.inventaire[item.name] = item.quantity
            self.ajout_matrice(item)
        else :
            self.inventaire[item.name] += self.quantity
        print("ajout fini")
    
    def drop_items (self, liste_obj, maxi ):
        """drop un item aléatoire au sein d'une liste d'objet et l'ajoute à l'inventaire"""
        self.ajoute_item(Items(random.choice(liste_obj), random.randint(1, maxi)))
        return 


