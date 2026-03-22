#ici on s'occupe des classes
from LVL_UP import lvl_up


class Personnage :
    def __init__ (self, nom, niv , force, defence, pointDeVie, pointDeVieMax, agi, chance, sac = None, nbObjet = 0, nbObjet_max = 0, exp = 0, etat_potion = None):
        self.nom = nom
        self.niv = niv
        self.force = force
        self.defence = defence
        self.pointDeVie = pointDeVie
        self.pointDeVieMax = pointDeVieMax
        self.agi = agi
        self.luk = chance

        self.exp = exp
        # Chaque instance a sa propre liste (pas de partage mémoire)
        self.sac = sac if sac is not None else []
        self.etat_potion = etat_potion if etat_potion is not None else []

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

    def consommePotion (self):
        self.pointDeVie = self.pointDeVieMax
        return

    def gain_niv(self):
        lim = 30*self.niv
        if self.exp >= lim :
            self.exp = self.exp - lim
            self.niv += 1
            self.pointDeVieMax += 2
            self.pointDeVie += 2

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









