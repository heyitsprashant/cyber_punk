import random
import pygame
from settings import COLOR_RED, SCREEN_HEIGHT, SCREEN_WIDTH


class Meteor:
    def __init__(self):
        side = random.choice(["left", "right", "top"])
        if side == "left":
            self.position = pygame.Vector2(-40, random.randint(100, SCREEN_HEIGHT - 100))
            self.velocity = pygame.Vector2(random.uniform(4, 8), random.uniform(-1.5, 1.5))
        elif side == "right":
            self.position = pygame.Vector2(SCREEN_WIDTH + 40, random.randint(100, SCREEN_HEIGHT - 100))
            self.velocity = pygame.Vector2(random.uniform(-8, -4), random.uniform(-1.5, 1.5))
        else:
            self.position = pygame.Vector2(random.randint(150, SCREEN_WIDTH - 150), -40)
            self.velocity = pygame.Vector2(random.uniform(-2, 2), random.uniform(4, 7))
        self.radius = random.randint(12, 20)
        self.alive = True

    @property
    def rect(self) -> pygame.Rect:
        return pygame.Rect(self.position.x - self.radius, self.position.y - self.radius, self.radius * 2, self.radius * 2)

    def update(self) -> None:
        self.position += self.velocity
        if (
            self.position.x < -100
            or self.position.x > SCREEN_WIDTH + 100
            or self.position.y < -100
            or self.position.y > SCREEN_HEIGHT + 100
        ):
            self.alive = False

    def draw(self, surface: pygame.Surface) -> None:
        pygame.draw.circle(surface, COLOR_RED, (int(self.position.x), int(self.position.y)), self.radius)
        pygame.draw.circle(surface, (255, 180, 90), (int(self.position.x), int(self.position.y)), self.radius - 5)
