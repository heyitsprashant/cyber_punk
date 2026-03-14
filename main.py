import pygame
from game.game_manager import GameManager
from settings import SCREEN_HEIGHT, SCREEN_WIDTH


def main() -> None:
    pygame.init()
    pygame.display.set_caption("Space-Punk")
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    manager = GameManager(screen)
    manager.run()

    pygame.quit()


if __name__ == "__main__":
    main()
