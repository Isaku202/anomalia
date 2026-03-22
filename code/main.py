import pygame  # type: ignore
from game import Game # type: ignore

if __name__ == '__main__':
    pygame.init()
    game = Game()
    game.run()

