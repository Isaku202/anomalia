import asyncio
import sys, os

# Ajouter le dossier code/ au path pour que les imports fonctionnent
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "code"))

from page_menu import menu

asyncio.run(menu())
