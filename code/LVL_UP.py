import pygame, os, asyncio
from Timer import Timer

async def lvl_up (screen):
    """Affiche la notification de montée de niveau"""
    en_cours = True
    time = Timer(1000)

    img = pygame.image.load(os.path.join(os.path.dirname(__file__), "..", "objets/lvl_up.png"))
    img = pygame.transform.scale(img, (330, 140))
    img.set_colorkey([255, 255, 255])

    time.demarrer()
    while en_cours:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                en_cours = False

        screen.blit(img, (240, 140))
        pygame.display.flip()

        if time.est_fini():
            en_cours = False

        await asyncio.sleep(0)  # laisse le navigateur respirer