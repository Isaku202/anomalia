import pygame, pytmx, pyscroll, os

#importation d'autres classes d'autres fichiers
import monstre as m  
from pnj import Pnj
from dino_scr import dino
from drop_monster import Drop_slime
from musique import EffetSonore, Musique
from Timer import Timer
from LVL_UP import lvl_up
import coffre as c

class Portail : 
    """Classe pour gérer les informations liées à un portail"""
    def __init__(self, monde_origine, point_origine, monde_cible, point_teleportation):
        self.monde_origine = monde_origine
        self.point_origine = point_origine
        self.monde_cible = monde_cible
        self.point_teleportation = point_teleportation


class Map:
    """Classe pour gérer les informations liées à une map"""
    def __init__(self, name, col, group, tmx_data, portails, musique, coffres = [], pnjs = [], monstres = [] ):
        self.name = name
        self.col = col
        self.group = group
        self.tmx_data = tmx_data
        self.portails = portails
        self.pnjs = pnjs
        self.monstres = monstres
        self.coffres = coffres
        self.musiques = Musique()
        self.musique = musique
            

    def joue_musique(self):
        """Lance la musique de la map en boucle"""
        self.musiques.arreter()
        self.musiques.charger(self.musique)  
        self.musiques.jouer(loops=-1)  
        self.musiques.set_volume(0.5)

class MapManger : 
    """Gère les maps : 
        - affichage 
        - objects 
        - interaction
    """
    def __init__(self, screen, player):
        self.maps = {}
        self.screen  = screen
        self.player = player
        self.current_map = None  
        self.ancienne_map = None

        self.cron = Timer(700)
        
        m1 = [Portail("Map1", "sortie_Monde", "Terre", "entrée_terre"), Portail("Map1", "entrée_grotte_monde", "grotte", "entrée2_grotte") ]
        t = [Portail("Terre", "sortie_terre", "Map1", "entrée_Monde"), Portail("Terre", "entrée_grotte", "grotte", "entrée1_grotte")  ]
        g = [Portail("grotte", "sortie2_grotte", "Map1", "sortie_grotte_monde"), Portail("grotte", "sortie1_grotte","Terre" , "sortie_grotte")  ]

        self.enregistrer_map("Map1",  m1, "fond_prairie.mp3") 
        self.enregistrer_map("Terre", t)
        self.enregistrer_map("grotte", g, "dongeon.mp3")
        
        self.effets = EffetSonore()

        self.effets.charger("dégat", "coup_sur_player.mp3")
        self.effets.charger("s1", "son_slime_1.mp3")
        self.effets.charger("ms", "mort_slime.mp3")
        self.effets.charger("s3", "son_slime_3.mp3")

        
        self.current_map = "Map1"
        self.teleport_player("player")
        self.maps[self.current_map].joue_musique()
        self.ancienne_map = self.current_map

    def enregistrer_map (self, name, portails = [], musique = None,  pnjs = []):
        if musique != None :
            pygame.init()

        tmx_data = pytmx.util_pygame.load_pygame(os.path.join(os.path.dirname(__file__), "..", "Map_graph", f"{name}.tmx"))
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 0.25

        #Récupère les objets dans le calque objects de la map TILED
        col = []
        spawn_monstre = {}        
        spawn_pnj = {}
        dic_coffre = {}
        for obj in tmx_data.objects:
            if obj.type == "collision":
                col.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
            elif obj.type == "monstre":
                spawn_monstre[obj.name] = obj
            elif obj.type == "pnj":
                spawn_pnj[obj.name] = obj
            elif obj.type == "coffre" :
                dic_coffre[obj.name] = obj

        #dessiner le groupe de calques 
        group = pyscroll.PyscrollGroup(map_layer = map_layer, default_layer = 5)
        group.add(self.player)

        #Ajoute les Slimes aux endroits indiqué sur Tiled
        liste_monstre = self.ajoute_slime(spawn_monstre, group)
        #Ajoute les Pnj 
        liste_pnjs = self.ajoute_pnj (spawn_pnj, group)
        #Ajoute les coffres 
        liste_coffre = self.ajoute_coffre (dic_coffre, group)

        # Créer et ajouter la map 
        self.maps[name] = Map(name, col, group, tmx_data, portails, musique, liste_coffre, liste_pnjs, liste_monstre)
        
        # charger les points en passant le nom de la map
#        for slime in liste_monstre:
#            slime.charger_points(self, name)

#        for pnj in liste_pnjs :
#            pnj.charger_points(self, name)

    def ajoute_coffre (self, dic_coffre, group):
        liste_coffre = []
        for point_col in dic_coffre.values():
            coffre = c.Coffre(point_col)
            group.add(coffre)
            liste_coffre.append(coffre)
        return liste_coffre

    def ajoute_slime(self, spawn_monstre, group):
        """Ajoute les slimes au groupe"""
        liste_monstre = []
        for name_monstre, point_spawn in spawn_monstre.items():
            slime = m.Monstre(name_monstre, point_spawn.x, point_spawn.y, 1, 2, 6, 6, 1, 1,  self.player) 
            group.add(slime)
            liste_monstre.append(slime)
        return liste_monstre


    def ajoute_pnj (self, spawn_pnj, group):
        """Ajoute les PNJ au groupe"""
        liste_pnjs = []
        for nom_pnj, point_spawn in spawn_pnj.items():
            pnj = Pnj(nom_pnj, point_spawn.x, point_spawn.y ) 
            group.add(pnj)
            liste_pnjs.append (pnj)
        return liste_pnjs        

    def get_map (self) :
        return self.maps[self.current_map]
    
    def get_group (self):
        return self.get_map().group
    
    def get_col (self):
        return self.get_map().col 
    
    def get_object (self, name ):
        return self.get_map().tmx_data.get_object_by_name(name)

    def check_collision(self, dialog_box):
        """Gère toutes les collisions et leurs conséquences"""
        # Gestion des portails
        for portail in self.get_map().portails:
            if portail.monde_origine == self.current_map:
                point = self.get_object(portail.point_origine)
                rect = pygame.Rect(point.x, point.y, point.width, point.height)
                if self.player.feet.colliderect(rect):
                    copie_portail = portail
                    self.current_map = portail.monde_cible
                    self.teleport_player(copie_portail.point_teleportation)

        # Gestion des collisions pour tous les sprites
        for sprite in self.get_group().sprites():
            # Collision COFFRE (vérifier avant les murs)
            if isinstance(sprite, c.Coffre):
                if self.player.feet.colliderect(sprite.feet) and not sprite.ouvert:
                    sprite.ouvrir()
                    self.player.drop_items(c.Drop_Coffre().possible, 2)
                continue

            # Collision avec les MURS
            if sprite.feet.collidelist(self.get_col()) > -1:
                if isinstance(sprite, m.Monstre):
                    sprite.gerer_collision()
                else:
                    sprite.move_back()

            # Collision MONSTRE 
            elif isinstance(sprite, m.Monstre):
                if sprite.est_mort or not sprite.visible:
                    continue
                # Le player TOUCHE le monstre (collision corps)
                if self.player.feet.colliderect(sprite.feet):
                    self.player.move_back()
                    sprite.gerer_collision() 
                
                # Le player ATTAQUE le monstre 
                if self.player.is_attacking and self.player.current_frame >= 2 and not self.player.has_hit and self.player.hit_box.colliderect(sprite.hit_box):
                    sprite.stat.pointDeVie -= self.player.stat.force
                    self.player.has_hit = True

                    if not sprite.stat.estVivant(): #Si le monstre est MORT alors :
                        
                        #Le monstre disparait du champ visuel 
                        sprite.mourir() 
                        sprite.gain_exp() #en fonction des XP du monstre + gère la monté de niveau du monstre
                        
                        #joue sons de mort slime
                        self.effets.jouer("ms") 
                        
                        #Drop de l'item de classe Items et l'ajoute à l'inventaire du player 
                        self.player.drop_items(Drop_slime().possible, 1)

                # Le monstre ATTAQUE le player
                if sprite.is_attacking and not sprite.has_hit and sprite.hit_box.colliderect(self.player.hit_box):
                    self.player.stat.pointDeVie -= sprite.stat.force
                    sprite.has_hit = True
                    #self.effets.jouer("s2")

            # Collision PNJ
            elif isinstance(sprite, Pnj):
                self.collision_Pnj (sprite, dialog_box)
        
        if dialog_box.dialogue_finished:
            for sprite in self.get_group().sprites():
                if isinstance(sprite, Pnj):
                    # Gestion de Léon
                    if sprite.name == "Léon":
                        self.gestion_dialog_Léon (sprite)
                    
                    # Gestion de Popaul
                    elif sprite.name == "Paul":
                        self.gestion_dilog_Paul (sprite)
            
            self.player.bloque = False
            dialog_box.reset_dialogue()

    def collision_Pnj (self, sprite, dialog_box):
        """Gère les conséquences des collisions avec un pnj"""
        if self.player.feet.colliderect(sprite.feet):
            self.player.move_back()  
            sprite.move_back()
            sprite.is_colliding = True
                    
            if not dialog_box.reading and not dialog_box.dialogue_finished:
                self.player.bloque = True
                if sprite.name == "Léon":
                    dialog_box.start_dialogue(sprite.dialoge(sprite.name, sprite.etat_quete_leon))
                elif sprite.name == "Paul":
                    dialog_box.start_dialogue(sprite.dialoge(sprite.name, sprite.etat_quete_paul))
                   
        else:
            sprite.is_colliding = False

    def gestion_dialog_Léon (self, sprite):
        """Gère les changements de dialogue de Léon"""

        if sprite.etat_quete_leon == "base":
            sprite.etat_quete_leon = "en cours"
                        
        elif sprite.etat_quete_leon == "en cours" and sprite.quete_leon(self.player):
            sprite.etat_quete_leon = "recu"
                        
        elif sprite.etat_quete_leon == "recu":
            sprite.etat_quete_leon = "apres"
                                        
    def gestion_dilog_Paul (self, sprite):
        """Gère les changements de dialogue de Paul"""

        if sprite.etat_quete_paul == "base":
            sprite.etat_quete_paul = "en cours"
                        
        elif sprite.etat_quete_paul == "en cours":
            if sprite.quete_paul(self.player):
                sprite.etat_quete_paul = "recu"
                        
        elif sprite.etat_quete_paul == "recu":
            sprite.etat_quete_paul = "apres"
        elif sprite.etat_quete_paul == "apres":
            #gère une des fins possible du jeu (Bad ending)
            dino()
            self.running = False

    def dessiner_barres_vie(self): #Partie faite par IA encadré par "#_________________"
        """Dessine les barres de vie au-dessus des monstres"""
    #___________________________________________________________________________ 
        zoom = self.get_group()._map_layer.zoom  
    #___________________________________________________________________________ 
    
        for sprite in self.get_group().sprites():
            if isinstance(sprite, m.Monstre):
                if sprite.est_mort or not sprite.visible:
                    continue
                view_rect = self.get_group()._map_layer.view_rect
                
                x_ecran = (sprite.rect.centerx - view_rect.x) * zoom
                y_ecran = (sprite.rect.top - view_rect.y) * zoom
             
                barre_x = x_ecran - 25
                barre_y = y_ecran - 15
                
                # Dimensions
                largeur_totale = 50
                hauteur = 6
                
                # Calcule le pourcentage de vie
                pourcentage_vie = sprite.stat.pointDeVie / sprite.stat.pointDeVieMax
                largeur_vie = int(largeur_totale * pourcentage_vie)
    #___________________________________________________________________________            
                # Fond NOIR 
                pygame.draw.rect(self.screen, (0, 0, 0), 
                            (barre_x, barre_y, largeur_totale, hauteur))
                
                # Barre ROUGE 
                if largeur_vie > 0:
                    pygame.draw.rect(self.screen, (220, 40, 60), 
                                (barre_x, barre_y, largeur_vie, hauteur))
                
                # Contour blanc
                pygame.draw.rect(self.screen, (255, 255, 255), 
                            (barre_x - 1, barre_y - 1, largeur_totale + 2, hauteur + 2), 1)
    #___________________________________________________________________________ 

    def teleport_player (self, name):
        point = self.get_object(name)
        self.player.position[0] = point.x
        self.player.position[1] = point.y
        self.player.save_location()


    def draw (self):
        self.get_group().center(self.player.rect.center)
        self.get_group().draw(self.screen)
        self.dessiner_barres_vie()
        

    def update (self, dialog_box):
        self.get_group().update()
        self.check_collision(dialog_box)
        

        if self.current_map != self.ancienne_map :
            self.ancienne_map = self.current_map

            if self.maps[self.current_map].musique != None :
                self.maps[self.current_map].joue_musique()
            
        for pnj in self.get_map().pnjs : 
            pnj.move()
        for monstre in self.get_map().monstres:
            monstre.move()