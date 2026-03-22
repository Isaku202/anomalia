import pygame, os

class BoiteDialogue:
    """Class pour gérer la création du texte et des boites de dialogues"""
    def __init__(self):
        self.X_position = 60
        self.Y_position = 436

        self.img_box = pygame.image.load(os.path.join(os.path.dirname(__file__), "..", "objets/boite_dialogue.png"))
        
        self.box = self.get_image(65, 160, 380, 135)
        self.box.set_colorkey([0, 0, 0])  
        self.box = pygame.transform.scale(self.box, (700, 125))

        self.texts = []
        self.text_index = 0
        self.letter_index = 0
        self.font = pygame.font.Font(os.path.join(os.path.dirname(__file__), "..", "objets/Mistral.ttf"), 24)

        self.reading = False
        self.letter_speed = 2
        self.dialogue_finished = False  

    def start_dialogue(self, dialoge = []):
        """Démarre un nouveau dialogue"""
        if not self.reading and not self.dialogue_finished and len(dialoge) > 0:
            self.reading = True
            self.text_index = 0
            self.letter_index = 0
            self.texts = dialoge
        

    def reset_dialogue(self):
        """Réinitialise le dialogue pour permettre une nouvelle interaction"""
        self.dialogue_finished = False
        self.reading = False
        self.text_index = 0
        self.letter_index = 0
        self.texts = []

    def next_text(self):
        """Passe au texte suivant"""
        if not self.reading or len(self.texts) == 0:
            return
            
        if self.letter_index < len(self.texts[self.text_index]):
            self.letter_index = len(self.texts[self.text_index])
        else:
            self.text_index += 1
            self.letter_index = 0
            
            if self.text_index >= len(self.texts):
                self.reading = False
                self.dialogue_finished = True 

    def get_image(self, x, y, x_rec, y_rec):
        """Extrait une portion de l'image"""
        image = pygame.Surface([x_rec, y_rec])
        image.blit(self.img_box, (0, 0), (x, y, x_rec, y_rec))
        return image

    def render(self, screen):
        """Gère l'affichage des boites dialogues et des lettres une par une"""
        if self.reading and len(self.texts) > 0 and self.text_index < len(self.texts):
            if self.letter_index < len(self.texts[self.text_index]):
                self.letter_index += self.letter_speed

            current_length = min(self.letter_index, len(self.texts[self.text_index]))

            screen.blit(self.box, (self.X_position, self.Y_position)) 
            
            text = self.font.render(self.texts[self.text_index][0:current_length], False, (0, 0, 0))
            screen.blit(text, (self.X_position + 25, self.Y_position + 15))