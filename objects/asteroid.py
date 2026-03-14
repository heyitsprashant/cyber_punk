import random
import pygame
from settings import COLOR_YELLOW, SCREEN_HEIGHT, SCREEN_WIDTH


class Asteroid:
    def __init__(self):
        y = random.randint(120, SCREEN_HEIGHT - 120)
        self.position = pygame.Vector2(random.choice([-50, SCREEN_WIDTH + 50]), y)
        direction = 1 if self.position.x < 0 else -1
        self.velocity = pygame.Vector2(direction * random.uniform(5, 9), random.uniform(-1.2, 1.2))
        self.radius = random.randint(10, 16)
        self.alive = True

    @property
    def rect(self) -> pygame.Rect:
        return pygame.Rect(self.position.x - self.radius, self.position.y - self.radius, self.radius * 2, self.radius * 2)

    def update(self) -> None:
        self.position += self.velocity
        if (
            self.position.x < -120
            or self.position.x > SCREEN_WIDTH + 120
            or self.position.y < -120
            or self.position.y > SCREEN_HEIGHT + 120
        ):
            self.alive = False

    def draw(self, surface: pygame.Surface) -> None:
        pygame.draw.circle(surface, COLOR_YELLOW, (int(self.position.x), int(self.position.y)), self.radius)
        pygame.draw.circle(surface, (140, 90, 60), (int(self.position.x), int(self.position.y)), self.radius, 2)
