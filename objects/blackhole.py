import pygame
from settings import COLOR_NEON_PURPLE, COLOR_RED


class BlackHole:
    def __init__(self, position: pygame.Vector2, pull_radius: float = 220, event_horizon: float = 38, pull_strength: float = 0.45):
        self.position = pygame.Vector2(position)
        self.pull_radius = pull_radius
        self.event_horizon = event_horizon
        self.pull_strength = pull_strength

    def apply_gravity(self, obj) -> bool:
        """Returns True when the object is consumed by the event horizon."""
        if obj.state != "launched":
            return False

        delta = self.position - obj.position
        dist = delta.length() if delta.length_squared() > 0 else 0.0001

        if dist < self.event_horizon:
            return True

        if dist < self.pull_radius:
            direction = delta / dist
            strength = self.pull_strength * (1 - (dist / self.pull_radius))
            obj.velocity += direction * strength

        return False

    def draw(self, surface: pygame.Surface) -> None:
        pygame.draw.circle(surface, COLOR_NEON_PURPLE, (int(self.position.x), int(self.position.y)), int(self.pull_radius), 1)
        pygame.draw.circle(surface, (10, 10, 10), (int(self.position.x), int(self.position.y)), int(self.event_horizon))
        pygame.draw.circle(surface, COLOR_RED, (int(self.position.x), int(self.position.y)), int(self.event_horizon), 2)
