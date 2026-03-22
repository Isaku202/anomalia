import pygame, pytmx, pyscroll
import os
import monstre as m  
from pnj import Pnj
from musique import Musique


class Portail : 
    """Classe pour gérer les informations liées à un portail"""
    def __init__(self, monde_origine, point_origine, monde_cible, point_teleportation):
        self.monde_origine = monde_origine
        self.point_origine = point_origine
        self.monde_cible = monde_cible
        self.point_teleportation = point_teleportation


class Map:
    """Classe pour gérer les informations liées à une map"""
    def __init__(self, name, col, group, tmx_data, portails, musique, pnjs = [], monstres = [] ):
        self.name = name
        self.col = col
        self.group = group
        self.tmx_data = tmx_data
        self.portails = portails
        self.pnjs = pnjs
        self.monstres = monstres
        self.musiques = Musique()
        self.musique = musique
            

    def joue_musique(self):
        """Lance la musique de la map en boucle"""
        self.musiques.arreter()
        self.musiques.charger(self.musique)  
        self.musiques.jouer(loops=-1)  
        self.musiques.set_volume(0.5)

class MapManger : 
    def __init__(self, screen, player):
        self.maps = {}
        self.screen  = screen
        self.player = player
        self.current_map = None  
        self.ancienne_map = None
        
        m1 = [Portail("Map1", "sortie_Monde", "Terre", "entrée_terre"), Portail("Map1", "entrée_grotte_monde", "grotte", "entrée2_grotte") ]
        t = [Portail("Terre", "sortie_terre", "Map1", "entrée_Monde"), Portail("Terre", "entrée_grotte", "grotte", "entrée1_grotte")  ]
        g = [Portail("grotte", "sortie2_grotte", "Map1", "sortie_grotte_monde"), Portail("grotte", "sortie1_grotte","Terre" , "sortie_grotte")  ]

        self.enregistrer_map("Map1",  m1, "fond_prairie.mp3") 
        self.enregistrer_map("Terre", t)
        self.enregistrer_map("grotte", g, "dongeon.mp3")
        
        
        self.current_map = "Map1"
        self.teleport_player("player")
        self.maps[self.current_map].joue_musique()
        self.ancienne_map = self.current_map

    def enregistrer_map (self, name, portails = [], musique = None,  pnjs = []):
        if musique != None :
            #print(musique)
            pygame.init()

        tmx_data = pytmx.util_pygame.load_pygame(os.path.join(os.path.dirname(__file__), "..", "Map_graph", f"{name}.tmx"))
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 0.25

        col = []
        spawn_monstre = {}        
        spawn_pnj = {}
        for obj in tmx_data.objects:
            if obj.type == "collision":
                col.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
            elif obj.type == "monstre":
                spawn_monstre[obj.name] = obj
            elif obj.type == "pnj":
                spawn_pnj[obj.name] = obj

        #dessiner le groupe de calques 
        group = pyscroll.PyscrollGroup(map_layer = map_layer, default_layer = 5)
        group.add(self.player)

        #Ajoute les Slimes aux endroits indiqué sur Tiled
        liste_monstre = []
        for name_monstre, point_spawn in spawn_monstre.items():
            #print(name_monstre)
            slime = m.Monstre(name_monstre, point_spawn.x, point_spawn.y, 1, 2, 6, 6, 1, 1,  self.player) 
            #print("ajoute au groupe")
            #print("pnj :" + str(slime.name))
            group.add(slime)
            #print("ajouté au groupe")
            liste_monstre.append(slime)
            #print(slime.name)
            #print("liste monstre remplit")

        #Ajoute les Pnj 
        liste_pnjs = []
        #print("liste pnj créer")
        for nom_pnj, point_spawn in spawn_pnj.items():
            #print(nom_pnj)
            pnj = Pnj(nom_pnj, point_spawn.x, point_spawn.y ) 
            #print("ajoute au groupe")
            #print("pnj :" + str(pnj.name))
            group.add(pnj)
            #print("ajouté au groupe")
            liste_pnjs.append (pnj)
            #print(pnj.name)
            #print("liste pnj remplit")
        
        # Créer et ajouter la map 
        #print("map créer")
        self.maps[name] = Map(name, col, group, tmx_data, portails, musique, liste_pnjs, liste_monstre)
        
        # charger les points en passant le nom de la map
        for slime in liste_monstre:
            slime.charger_points(self, name)

        #print("remplit groupe pnj")
        for pnj in liste_pnjs :
            pnj.charger_points(self, name) ###        
        

    def get_map (self) :
        return self.maps[self.current_map]
    
    def get_group (self):
        return self.get_map().group
    
    def get_col (self):
        return self.get_map().col 
    
    def get_object (self, name ):
        return self.get_map().tmx_data.get_object_by_name(name)

    def check_collision(self, dialog_box):
        # Gestion des portails
        for portail in self.get_map().portails:
            if portail.monde_origine == self.current_map:
                point = self.get_object(portail.point_origine)
                rect = pygame.Rect(point.x, point.y, point.width, point.height)
                if self.player.feet.colliderect(rect):
                    copie_portail = portail
                    self.current_map = portail.monde_cible
                    self.teleport_player(copie_portail.point_teleportation)

        collision_pnj = False

        # Gestion des collisions pour tous les sprites
        for sprite in self.get_group().sprites():
            # Collision avec les MURS
            if sprite.feet.collidelist(self.get_col()) > -1:
                if isinstance(sprite, m.Monstre):
                    sprite.gerer_collision()  
                else:
                    sprite.move_back()
            
            # Collision MONSTRE 
            elif isinstance(sprite, m.Monstre):
                # Le player TOUCHE le monstre (collision corps)
                if self.player.feet.colliderect(sprite.feet):
                    self.player.move_back()
                    sprite.gerer_collision() 
                
                # Le player ATTAQUE le monstre 
                if self.player.is_attacking and self.player.current_frame >= 2 and not self.player.has_hit and self.player.hit_box.colliderect(sprite.hit_box):
                    #print(f"Le joueur frappe {sprite.name} !")
                    sprite.stat.pointDeVie -= self.player.stat.force
                    self.player.has_hit = True
                    if not sprite.stat.estVivant():
                        sprite.kill()
                        sprite.gain_exp()
                        #print(self.player.stat.exp)
                        #print(self.player.stat.niv)

                # Le monstre ATTAQUE le player
                if sprite.is_attacking and not sprite.has_hit and sprite.hit_box.colliderect(self.player.hit_box):
                    #print(f"{sprite.name} frappe le joueur!")
                    self.player.stat.pointDeVie -= sprite.stat.force
                    sprite.has_hit = True

            # Collision PNJ
            elif isinstance(sprite, Pnj):
                if self.player.feet.colliderect(sprite.feet):
                    self.player.move_back()
                    sprite.move_back()
                    collision_pnj = True
                    sprite.is_colliding = True
                    
                    dialog_box.start_dialogue()
                else:
                    sprite.is_colliding = False
        
        if not collision_pnj:
            dialog_box.reset_dialogue()

    def dessiner_barres_vie(self):
        """Dessine les barres de vie au-dessus des monstres"""
        zoom = self.get_group()._map_layer.zoom  
        
        for sprite in self.get_group().sprites():
            if isinstance(sprite, m.Monstre):
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
        