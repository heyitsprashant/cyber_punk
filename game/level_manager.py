import math
import pygame
from settings import (
    COLOR_NEON_BLUE,
    COLOR_NEON_GREEN,
    COLOR_NEON_PURPLE,
    COLOR_PANEL,
    COLOR_WHITE,
    SCORE_PERFECT_ORBIT,
    SCORE_PLANET_PLACED,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    SLINGSHOT_POS,
    SOLAR_ZONE_CENTER,
)
from objects.planet import Planet
from objects.slingshot import Slingshot


class BaseLevel:
    level_number = 1
    title = "Normal Space"

    def __init__(self):
        self.slingshot = Slingshot(SLINGSHOT_POS)
        self.orbit_slots = self._build_orbit_slots(8, 170)
        self.total_planets = 12
        self.required_planets = 8
        self.planets_left_to_spawn = self.total_planets
        self.active_planet: Planet | None = None
        self.locked_planets: list[Planet] = []
        self.score = 0
        self.is_complete = False
        self.is_failed = False
        self.status_message = "Launch planets into orbit slots"
        # Optional level background artwork.
        self.bg_image: pygame.Surface | None = None
        try:
            self.bg_image = pygame.image.load("assets/space_background.png").convert()
        except Exception:
            self.bg_image = None
        self._spawn_next_planet()

    def _build_orbit_slots(self, count: int, radius: float) -> list[pygame.Vector2]:
        slots = []
        for i in range(count):
            angle = i * (2 * math.pi / count)
            pos = pygame.Vector2(
                SOLAR_ZONE_CENTER.x + math.cos(angle) * radius,
                SOLAR_ZONE_CENTER.y + math.sin(angle) * radius,
            )
            slots.append(pos)
        return slots

    def _spawn_next_planet(self) -> None:
        if self.planets_left_to_spawn <= 0:
            self.active_planet = None
            return
        self.planets_left_to_spawn -= 1
        self.active_planet = Planet(self.slingshot.anchor)

    def _available_slot_index(self, planet: Planet) -> int | None:
        for i, slot in enumerate(self.orbit_slots):
            slot_occupied = any(p.orbit_slot == i and p.state == "locked" for p in self.locked_planets)
            if slot_occupied:
                continue
            if planet.position.distance_to(slot) <= 24:
                return i
        return None

    def _try_lock_active_planet(self) -> bool:
        if not self.active_planet or self.active_planet.state != "launched":
            return False

        slot_index = self._available_slot_index(self.active_planet)
        if slot_index is None:
            return False

        speed = self.active_planet.velocity.length()
        self.active_planet.lock_in_orbit(self.orbit_slots[slot_index], slot_index)
        self.locked_planets.append(self.active_planet)
        self.score += SCORE_PLANET_PLACED
        if speed < 3.5:
            self.score += SCORE_PERFECT_ORBIT
        self.active_planet = None
        self._spawn_next_planet()
        return True

    def _check_end_state(self) -> None:
        if len(self.locked_planets) >= self.required_planets:
            self.is_complete = True
            self.status_message = "Level complete"
            return

        no_more_attempts = self.active_planet is None and self.planets_left_to_spawn <= 0
        if no_more_attempts and len(self.locked_planets) < self.required_planets:
            self.is_failed = True
            self.status_message = "All planets lost"

    def restart(self) -> None:
        self.__init__()

    def handle_event(self, event: pygame.event.Event) -> None:
        if self.is_complete or self.is_failed or not self.active_planet:
            return

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.active_planet.state == "ready":
            if self.active_planet.position.distance_to(pygame.Vector2(event.pos)) <= self.active_planet.radius + 20:
                self.slingshot.begin_drag(event.pos)
                self.active_planet.position = pygame.Vector2(event.pos)

        elif event.type == pygame.MOUSEMOTION and self.slingshot.dragging and self.active_planet.state == "ready":
            self.slingshot.update_drag(event.pos)
            pull = self.slingshot.anchor - pygame.Vector2(event.pos)
            if pull.length() > 0:
                pull.scale_to_length(min(pull.length(), 180))
            self.active_planet.position = self.slingshot.anchor - pull

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1 and self.slingshot.dragging and self.active_planet.state == "ready":
            velocity = self.slingshot.get_launch_velocity()
            self.slingshot.release()
            self.active_planet.position = pygame.Vector2(self.slingshot.anchor)
            self.active_planet.launch(velocity)

    def update(self, dt: float) -> None:
        if self.is_complete or self.is_failed:
            return

        if self.active_planet:
            self.active_planet.update()
            self._try_lock_active_planet()
            if self.active_planet and self.active_planet.state == "destroyed":
                self.active_planet = None
                self._spawn_next_planet()

        self._check_end_state()

    def draw_background(self, surface: pygame.Surface) -> None:
        if self.bg_image:
            bg = pygame.transform.smoothscale(self.bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
            surface.blit(bg, (0, 0))
        else:
            surface.fill((6, 6, 18))
            for i in range(35):
                x = (i * 211) % SCREEN_WIDTH
                y = (i * 127) % SCREEN_HEIGHT
                color = (20 + (i * 5) % 100, 20, 60 + (i * 4) % 160)
                pygame.draw.circle(surface, color, (x, y), 2)

    def draw(self, surface: pygame.Surface, font: pygame.font.Font) -> None:
        self.draw_background(surface)

        # Solar zone rings
        pygame.draw.circle(surface, COLOR_NEON_PURPLE, (int(SOLAR_ZONE_CENTER.x), int(SOLAR_ZONE_CENTER.y)), 220, 2)
        pygame.draw.circle(surface, COLOR_NEON_BLUE, (int(SOLAR_ZONE_CENTER.x), int(SOLAR_ZONE_CENTER.y)), 170, 2)

        for i, slot in enumerate(self.orbit_slots):
            occupied = any(p.orbit_slot == i and p.state == "locked" for p in self.locked_planets)
            slot_color = COLOR_NEON_GREEN if occupied else COLOR_WHITE
            pygame.draw.circle(surface, slot_color, (int(slot.x), int(slot.y)), 12, 2)

        self.slingshot.draw(surface)

        for planet in self.locked_planets:
            planet.draw(surface)

        if self.active_planet:
            self.active_planet.draw(surface)

        panel = pygame.Rect(20, 20, 420, 110)
        pygame.draw.rect(surface, COLOR_PANEL, panel, border_radius=10)
        pygame.draw.rect(surface, COLOR_NEON_BLUE, panel, 2, border_radius=10)

        title_text = font.render(f"LEVEL {self.level_number}: {self.title}", True, COLOR_WHITE)
        msg_text = font.render(self.status_message, True, COLOR_NEON_GREEN)
        surface.blit(title_text, (34, 34))
        surface.blit(msg_text, (34, 66))


def get_level(level_number: int) -> BaseLevel:
    if level_number == 1:
        from levels.level1 import Level1

        return Level1()
    if level_number == 2:
        from levels.level2 import Level2

        return Level2()
    if level_number == 3:
        from levels.level3 import Level3

        return Level3()
    from levels.level4 import Level4

    return Level4()
