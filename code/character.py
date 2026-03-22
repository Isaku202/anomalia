import pygame 

class Character:  
    """Classe pour les fonctionnalités communes entre PNJ et monstres"""
    
    def init_character(self, name, x, y, feet_height, nb_points, speed=3):
        """Initialise les attributs du character"""
        self.name = name
        self.position = [x, y]
        self.old_position = self.position.copy()
        
        self.feet = pygame.Rect(0, 0, self.rect.width * 1, feet_height)
        self.feet.midbottom = self.rect.midbottom 
        
        self._layer = 5
        self.nb_points = nb_points
        self.points = []
        self.current_point = 0
        self.speed = speed
        self.current_direction = "base"
        self.current_frame = 0
        self.ani_counter = 0
    
    def move(self):
        """déplace le personnage"""
        if len(self.points) == 0:
            return
        
        rect_cible = self.points[self.current_point]
        distance_x = rect_cible.centerx - self.rect.centerx
        distance_y = rect_cible.centery - self.rect.centery

        if abs(distance_y) > abs(distance_x):
            if distance_y < -5: 
                self.move_up()
            elif distance_y > 5: 
                self.move_down()
        else:
            if distance_x < -5:  
                self.move_left()
            elif distance_x > 5: 
                self.move_right()

        if abs(distance_x) < 10 and abs(distance_y) < 10:
            self.current_point += 1
            if self.current_point >= len(self.points):
                self.current_point = 0

    def move_right(self):
        """deplace le personnage vers la droite"""
        self.save_location()
        self.change_ani("droite")
        self.position[0] += self.speed

    def move_left(self):
        """deplace le personnage vers la gauche"""
        self.save_location()
        self.change_ani("gauche")
        self.position[0] -= self.speed

    def move_up(self):
        """deplace le personnage vers le haut"""
        self.save_location()
        self.change_ani("haut")
        self.position[1] -= self.speed

    def move_down(self):
        """deplace le personnage vers le bas"""
        self.save_location()
        self.change_ani("bas")
        self.position[1] += self.speed
    
    def charger_points(self, map_manager, map_name):
        """Charge les points de déplacement depuis Tiled"""
        for i in range(1, self.nb_points + 1):
            point_name = f"{self.name}_point_{i}"
            try:
                point = map_manager.maps[map_name].tmx_data.get_object_by_name(point_name)
                rect = pygame.Rect(point.x, point.y, point.width, point.height)
                self.points.append(rect)
                print(f"  ✓ {self.name} - Point {i} chargé: ({point.x}, {point.y})")
            except KeyError:
                print(f"  ✗ {self.name} - Point '{point_name}' non trouvé")

    def update(self):
        """Met à jour la position du character"""
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom

    def move_back(self):
        """Retour à l'ancienne position en cas de collision"""
        self.position = self.old_position.copy()
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom

    def save_location(self):
        """Sauvegarde la position actuelle"""
        self.old_position = self.position.copy()

    def change_ani(self, nv_direction):
        """met a jour les images d'animations"""
        if self.current_direction != nv_direction:
            self.current_frame = 0
            self.ani_counter = 0
            self.current_direction = nv_direction