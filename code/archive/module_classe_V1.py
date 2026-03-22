#ici on s'occupe des classes
from LVL_UP import lvl_up


class Personnage :
    def __init__ (self, nom, niv , force, defence, pointDeVie, pointDeVieMax, agi, chance, sac = [], nbObjet = 0, nbObjet_max = 0, exp = 0, etat_potion =[]):
        self.nom = nom
        self.niv = niv
        self.force = force
        self.defence = defence
        self.pointDeVie = pointDeVie
        self.pointDeVieMax = pointDeVieMax
        self.agi = agi
        self.luk = chance
        
        self.exp = exp
        self.etat_potion = etat_potion

    def afficherStats(self):
        """affiche les atributs du personnage"""
        print("Name :", self.nom)
        print("Level :", self.niv)
        print('HP :', self.pointDeVie, '/', self.pointDeVieMax)
        print('STR :', self.force)
        print('DEF :', self.defence)
        print('AGI :', self.agi)
        print('LUK :', self.luk)

    def estVivant(self):
        """renvoie True ou False en fonction de l’état des points de vie du personnage"""
        if self.pointDeVie > 0 :
            return True
        else : return False


#    def attaquer(self, perso):
        """effectue une attaque sur un autre personnage
        (une attaque ne peut être effectuée que par et sur un personnage vivant
        et ôte sur un nombre de points de vie égal à la valeur de force de l’attaquant)."""
        if self.estVivant and perso.estVivant  :
            self.pointDeVie -= perso.force
        return print(self.nom, ":", self.pointDeVie)


    def consommePotion (self):
        self.pointDeVie = self.pointDeVieMax
        return


    def supprimerObjet (self, objet):
        for i in range (self.nbObjet) :
            if self.sac[i][0] == objet :
                self.sac.pop(i)
                self.nbObjet -= 1
                self.poidSac -= self.sac[i][1]
                return
        return objet, "n'est pas dans le sac"


    def ajouterObjet_poid(self, objet) :

        """permet d’ajouter soit une Potion, soit du materiel dans le sac du personnage, si c’est du materiel, il
        modifie les attributs du personnage, attention le poids ne peut dépasser le poids du sac.
        Si un objet doit être ajouté et que le poids max est atteint, la liste des objets du sac (avec
        leurs masses) et l’objet à ajouter seront listés et le joueur aura le droit d’en supprimer un ou
        plusieurs pour libérer de l’espace. (voir fonction supprimer objet)"""

        if self.poidSac + objet.poids > self.taille :

            print("ATTENTION : Le poids max est atteint. Vous ne pouvez pas rajouter l'objet." \
            " Vous pouvez supprimer un ou plusieurs objets du sac pour pouvoir le ranger.")

            if input("Voulez vous nettoyer le sac ? ") == "oui" :
                print("Le poids actuel du sac est de :", self.poidSac)
                print("Le poids à libérer pour l'objet est de :", self.poidSac - (self.taille-objet.poids))
                print("SAC : ")
                for i in range(self.nbObjet):
                    print("-", self.sac[i])

                for i in range(self.nbObjet) :
                    self.supprimerObjet (input("Nom de l'objet a supprimer : "))
                    rep = input("Voulez vous supprimer d'autres objets ? ")
                    if rep == 'non':
                        return None
            return None
        if type(objet) == Materiel :
            self.pointDeVieMax += objet.nbBonusVie
            self.force += objet.nbBonusForce


        self.sac.append((objet, objet.nom , objet.poids))
        self.poidSac += objet.poids
        self.nbObjet += 1


    def ajouterObjet(self, objet) :

        """permet d’ajouter du materiel dans le sac du personnage, attention la taille ne peut dépasser la taille du sac.
        Si un objet doit être ajouté et que la taille max est atteinte, la liste des objets du sac
        et l’objet à ajouter seront listés et le joueur aura le droit d’en supprimer un ou
        plusieurs pour libérer de l’espace. (voir fonction supprimer objet)"""

        if self.poidSac + objet.poids > self.taille :

            print("ATTENTION : Le poids max est atteint. Vous ne pouvez pas rajouter l'objet." \
            " Vous pouvez supprimer un ou plusieurs objets du sac pour pouvoir le ranger.")

            if input("Voulez vous nettoyer le sac ? ") == "oui" :
                print("Le poids actuel du sac est de :", self.poidSac)
                print("Le poids à libérer pour l'objet est de :", self.poidSac - (self.taille-objet.poids))
                print("SAC : ")
                for i in range(self.nbObjet):
                    print("-", self.sac[i])

                for i in range(self.nbObjet) :
                    self.supprimerObjet (input("Nom de l'objet a supprimer : "))
                    rep = input("Voulez vous supprimer d'autres objets ? ")
                    if rep == 'non':
                        return None
            return None
        if type(objet) == Materiel :
            self.pointDeVieMax += objet.nbBonusVie
            self.force += objet.nbBonusForce


        self.sac.append((objet, objet.nom , objet.poids))
        self.poidSac += objet.poids
        self.nbObjet += 1


    def boirePotion(self):
        """propose un menu montrant toutes les potions du Personnage
        et qui permet d’en boire une et de regagner le
        nombre de point de vie correspondant."""
        print("Menu de potions : ")
        for obj in self.sacPotion :
            print("-", obj[1], "bonus", obj[0].pointDeSoin)
        nbPotion = len(self.sacPotion)
        for i in range(nbPotion):
            rep = input("Voulez vous boire une potion ?")
            if rep == "non":
                return None
            return self.consommePotion(input("Quelle potion veux tu boires ?"))

    def gain_niv(self):
        lim = 30*self.niv
        if self.exp >= lim :
            self.exp = self.exp - lim
            self.niv += 1
            self.pointDeVieMax += 2
            self.pointDeVie += 2


def combat(perso1, perso2) :
    """lançant un combat entre deux personnages qui attaquent à tour de rôle jusqu’à ce
    que les points de vie de l’un des deux atteigne zéro."""
    perso2.attaquer(perso1)
    if perso1.estVivant() and perso2.estVivant() :
        perso1.attaquer(perso2)
        return combat(perso1, perso2)
    elif perso1.pointDeVie <= 0 :
        perso1.pointDeVie = 0
    else :
        perso2.pointDeVie = 0
    return None


class Objet:
    def __init__ (self, nom):
        self.nom = nom.lower()

class Potion (Objet) :
    def __init__(self, nom, pointDeSoin):
        Objet.__init__(self, nom)
        self.pointDeSoin = pointDeSoin

class Materiel (Objet):
    def __init__(self, nom, nbBonusVie, nbBonusForce):
        Objet.__init__(self, nom)
        self.nbBonusVie = nbBonusVie
        self.nbBonusForce = nbBonusForce

class Armure (Materiel) :
    def __init__(self, nom, nbBonusVie, nbBonusForce):
        Materiel.__init__(self, nom)

class Monstre (Personnage):
    def __init__ (self, nom, race, niv , force, defence, pointDeVie, pointDeVieMax, agi, luk, exp, player) :
        Personnage.__init__(self, nom, niv , force, defence, pointDeVie, pointDeVieMax, agi, luk)
        self.race = race
        self.player = player
        self.exp = exp
        
        self.fc = self.facteur_de_puissance()

        

    def facteur_de_puissance (self):
        """Donne une coukeurs : vert, jaune, rouge. en fonction de la dangerosité du monstre pour le player.
        Un niveau inférieur au player: vert. Niveau égal : jaune. Plus de 10 niveau supérieur : rouge"""
        if self.niv < self.player.stat.niv-3 :
            return "vert"
        elif self.niv-3 > self.player.stat.niv :
            return "rouge"
        else :
            return "jaune"

    def afficherStats1(self):
        """affiche les atributs d'un monstre"""
        print("_______________________________________________________")
        print('Race :', self.race)
        self.afficherStats()
        print('FC :', self.fc)
        print("_______________________________________________________")

    def gain_exp (self):
        self.player.stat.exp += self.exp
        self.player.stat.gain_niv()

class Compétence_mg :
    def __init__ (self, consomation_mp, taux_chance_reussite, degat, perso):
        self.conso_mp = consomation_mp
        self.perso = perso
        self.tChance = self.perso.luk/100







