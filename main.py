import asyncio
import sys, os

# Ajouter le dossier code/ au path pour que les imports fonctionnent
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "code"))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))

async def main():
    try:
        from page_menu import menu
        await menu()
    except Exception as e:
        # Affiche l'erreur sur l'écran si le jeu crash
        import traceback
        error_text = traceback.format_exc()
        print(error_text)

        font = pygame.font.Font(None, 24)
        screen.fill((0, 0, 0))
        y = 20
        for line in error_text.split('\n'):
            text = font.render(line, True, (255, 50, 50))
            screen.blit(text, (20, y))
            y += 25
        pygame.display.flip()

        # Garde l'écran d'erreur visible
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
            await asyncio.sleep(0)

asyncio.run(main())
