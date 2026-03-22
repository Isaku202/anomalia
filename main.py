import asyncio
import sys, os

# Ajouter le dossier code/ au path pour que les imports fonctionnent
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "code"))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pygame
pygame.init()

from page_menu import menu

asyncio.run(menu())
