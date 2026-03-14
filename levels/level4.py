import pygame
from game.level_manager import BaseLevel
from objects.blackhole import BlackHole
from settings import COLOR_NEON_BLUE, COLOR_NEON_GREEN, COLOR_NEON_PINK, COLOR_RED, SCREEN_HEIGHT


class Level4(BaseLevel):
    level_number = 4
    title = "Black Hole Galaxy Transfer"

    def __init__(self):
        super().__init__()
        self.total_planets = 15
        self.planets_left_to_spawn = self.total_planets - 1
        self.blackholes = [
            BlackHole(pygame.Vector2(580, 220), pull_radius=200, event_horizon=34, pull_strength=0.55),
            BlackHole(pygame.Vector2(730, 510), pull_radius=180, event_horizon=32, pull_strength=0.5),
        ]
        self.portal_entry = pygame.Rect(380, SCREEN_HEIGHT // 2 - 60, 26, 120)
        self.portal_exit = pygame.Rect(980, SCREEN_HEIGHT // 2 - 60, 26, 120)
        self.status_message = "Use portals and avoid black hole event horizons"

    def update(self, dt: float) -> None:
        if self.active_planet and self.active_planet.state == "launched":
            for blackhole in self.blackholes:
                if blackhole.apply_gravity(self.active_planet):
                    self.active_planet.destroy()

            if self.portal_entry.colliderect(self.active_planet.rect):
                already_teleported = getattr(self.active_planet, "teleported", False)
                if not already_teleported:
                    self.active_planet.position = pygame.Vector2(self.portal_exit.center)
                    self.active_planet.velocity *= 1.15
                    setattr(self.active_planet, "teleported", True)

        super().update(dt)

    def draw(self, surface: pygame.Surface, font: pygame.font.Font) -> None:
        super().draw(surface, font)

        for blackhole in self.blackholes:
            blackhole.draw(surface)

        pygame.draw.rect(surface, COLOR_NEON_PINK, self.portal_entry, 2, border_radius=8)
        pygame.draw.rect(surface, COLOR_NEON_GREEN, self.portal_exit, 2, border_radius=8)
        pygame.draw.circle(surface, COLOR_NEON_PINK, self.portal_entry.center, 18, 2)
        pygame.draw.circle(surface, COLOR_NEON_GREEN, self.portal_exit.center, 18, 2)

        warn_text = font.render("BLACK HOLE GRAVITY ACTIVE", True, COLOR_RED)
        surface.blit(warn_text, (34, 96))
