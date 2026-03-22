#C'est ici le corps du code
import module_classe as c

perso1 = c.Personnage("Pierre", 12, 40, 36, 67, 67, 0, 21, 10)
perso2 = c.Personnage("Marc", 12, 32, 40, 90, 90, 0, 28, 10)
print("stat origine :")
perso1.afficherStats()
perso2.afficherStats()

c.combat(perso1,perso2)

print (" ")
print (" ")
print("stat nouvelle :")
perso1.afficherStats()
perso2.afficherStats()
potion_de_soins = c.Potion("potion de soins", 10, 0.03)
epee = c.Materiel("Épée de chevalier", 0, 25, 5)
for i in range (1):
    perso1.ajouterObjet(epee)
    perso1.ajouterObjet(potion_de_soins)

#perso1.afficherStats()

print(perso1.sacPotion)

print("")
perso2.pointDeVie = 10
perso2.boirePotion()

print("")

perso2.afficherStats()

print("_______________________________________________________")

slime = c.Monstre("Slime ordinaire", "Slime basique", 3 , 15, 30, 30, 30, 0, 2, 51, perso1)
slime.afficherStats1()

print("")

c.combat(perso1, slime)
slime.gain_exp()
slime.afficherStats1()
perso1.afficherStats()








