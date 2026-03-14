import random
import pygame
from game.physics import projectile_step
from settings import (
    COLOR_NEON_BLUE,
    COLOR_NEON_GREEN,
    COLOR_NEON_PINK,
    COLOR_NEON_PURPLE,
    COLOR_RED,
    GRAVITY,
    PLANET_MAX_HEALTH,
    PLANET_RADIUS,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
)


PLANET_COLORS = [COLOR_NEON_BLUE, COLOR_NEON_PINK, COLOR_NEON_PURPLE, COLOR_NEON_GREEN]


class Planet:
    def __init__(self, position: pygame.Vector2, orbit_slot: int | None = None):
        self.position = pygame.Vector2(position)
        self.velocity = pygame.Vector2(0, 0)
        self.radius = PLANET_RADIUS + random.randint(-3, 4)
        self.health = PLANET_MAX_HEALTH
        self.mass = 1.0 + random.random() * 1.5
        self.orbit_slot = orbit_slot
        self.color = random.choice(PLANET_COLORS)
        self.state = "ready"  # ready, launched, locked, destroyed
        self.locked_position = pygame.Vector2(position)

    @property
    def rect(self) -> pygame.Rect:
        return pygame.Rect(
            self.position.x - self.radius,
            self.position.y - self.radius,
            self.radius * 2,
            self.radius * 2,
        )

    def launch(self, velocity: pygame.Vector2) -> None:
        self.velocity = pygame.Vector2(velocity)
        self.state = "launched"

    def destroy(self) -> None:
        self.state = "destroyed"
        self.health = 0

    def lock_in_orbit(self, position: pygame.Vector2, orbit_slot: int) -> None:
        self.state = "locked"
        self.velocity = pygame.Vector2(0, 0)
        self.position = pygame.Vector2(position)
        self.locked_position = pygame.Vector2(position)
        self.orbit_slot = orbit_slot

    def take_damage(self, amount: int) -> None:
        self.health -= amount
        if self.health <= 0:
            self.destroy()

    def update(self) -> None:
        if self.state == "launched":
            self.position, self.velocity = projectile_step(self.position, self.velocity, GRAVITY)
            out_of_bounds = (
                self.position.x < -100
                or self.position.x > SCREEN_WIDTH + 100
                or self.position.y < -100
                or self.position.y > SCREEN_HEIGHT + 120
            )
            if out_of_bounds:
                self.destroy()

    def draw(self, surface: pygame.Surface) -> None:
        if self.state == "destroyed":
            return

        pygame.draw.circle(surface, self.color, (int(self.position.x), int(self.position.y)), self.radius)
        pygame.draw.circle(surface, COLOR_RED, (int(self.position.x), int(self.position.y)), self.radius, 2)
