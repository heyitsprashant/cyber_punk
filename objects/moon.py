import pygame
from game.physics import projectile_step
from settings import COLOR_WHITE, GRAVITY, SCREEN_HEIGHT, SCREEN_WIDTH


class Moon:
    def __init__(self, position: pygame.Vector2):
        self.position = pygame.Vector2(position)
        self.velocity = pygame.Vector2()
        self.radius = 10
        self.state = "ready"  # ready, launched, locked, destroyed
        self.anchor_planet_index = None

    @property
    def rect(self) -> pygame.Rect:
        return pygame.Rect(self.position.x - self.radius, self.position.y - self.radius, self.radius * 2, self.radius * 2)

    def launch(self, velocity: pygame.Vector2) -> None:
        self.velocity = pygame.Vector2(velocity)
        self.state = "launched"

    def destroy(self) -> None:
        self.state = "destroyed"

    def lock_to_planet(self, planet_index: int, orbit_pos: pygame.Vector2) -> None:
        self.state = "locked"
        self.anchor_planet_index = planet_index
        self.position = pygame.Vector2(orbit_pos)
        self.velocity = pygame.Vector2()

    def update(self) -> None:
        if self.state != "launched":
            return
        self.position, self.velocity = projectile_step(self.position, self.velocity, GRAVITY * 0.6)
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
        pygame.draw.circle(surface, COLOR_WHITE, (int(self.position.x), int(self.position.y)), self.radius)
