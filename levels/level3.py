import random
import pygame
from game.level_manager import BaseLevel
from objects.asteroid import Asteroid
from objects.moon import Moon
from settings import COLOR_NEON_BLUE, COLOR_NEON_GREEN, COLOR_WHITE, SCORE_MOON_PLACED


class Level3(BaseLevel):
    level_number = 3
    title = "Asteroid Field - Moon Phase"

    def __init__(self):
        super().__init__()
        self.phase = "planets"
        self.required_moons = 8
        self.total_moons = 12
        self.moons_left_to_spawn = self.total_moons
        self.active_moon: Moon | None = None
        self.locked_moons: list[Moon] = []
        self.asteroids: list[Asteroid] = []
        self.asteroid_timer = 0.0
        self.asteroid_interval = 0.9
        self.status_message = "Phase 1: Place 8 planets, then place moons"

    def _spawn_next_moon(self) -> None:
        if self.moons_left_to_spawn <= 0:
            self.active_moon = None
            return
        self.moons_left_to_spawn -= 1
        self.active_moon = Moon(self.slingshot.anchor)

    def _moon_orbit_targets(self) -> list[tuple[int, pygame.Vector2]]:
        targets = []
        for i, planet in enumerate(self.locked_planets):
            if planet.state != "locked":
                continue
            angle = (i * 0.8) + 0.6
            offset = pygame.Vector2(42, 0).rotate_rad(angle)
            targets.append((i, planet.position + offset))
        return targets

    def _try_lock_active_moon(self) -> bool:
        if not self.active_moon or self.active_moon.state != "launched":
            return False

        for planet_index, orbit_pos in self._moon_orbit_targets():
            already_taken = any(m.anchor_planet_index == planet_index and m.state == "locked" for m in self.locked_moons)
            if already_taken:
                continue

            if self.active_moon.position.distance_to(orbit_pos) <= 14:
                self.active_moon.lock_to_planet(planet_index, orbit_pos)
                self.locked_moons.append(self.active_moon)
                self.score += SCORE_MOON_PLACED
                self.active_moon = None
                self._spawn_next_moon()
                return True

        return False

    def handle_event(self, event: pygame.event.Event) -> None:
        if self.phase == "planets":
            super().handle_event(event)
            return

        if self.is_complete or self.is_failed or not self.active_moon:
            return

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.active_moon.state == "ready":
            if self.active_moon.position.distance_to(pygame.Vector2(event.pos)) <= self.active_moon.radius + 18:
                self.slingshot.begin_drag(event.pos)
                self.active_moon.position = pygame.Vector2(event.pos)

        elif event.type == pygame.MOUSEMOTION and self.slingshot.dragging and self.active_moon.state == "ready":
            self.slingshot.update_drag(event.pos)
            pull = self.slingshot.anchor - pygame.Vector2(event.pos)
            if pull.length() > 0:
                pull.scale_to_length(min(pull.length(), 180))
            self.active_moon.position = self.slingshot.anchor - pull

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1 and self.slingshot.dragging and self.active_moon.state == "ready":
            vel = self.slingshot.get_launch_velocity()
            self.slingshot.release()
            self.active_moon.position = pygame.Vector2(self.slingshot.anchor)
            self.active_moon.launch(vel)

    def _update_asteroids(self, dt: float) -> None:
        self.asteroid_timer += dt
        if self.asteroid_timer >= self.asteroid_interval:
            self.asteroid_timer = 0.0
            self.asteroids.append(Asteroid())

        for asteroid in self.asteroids:
            asteroid.update()

            if self.active_moon and self.active_moon.state in {"ready", "launched"}:
                if asteroid.position.distance_to(self.active_moon.position) <= asteroid.radius + self.active_moon.radius:
                    self.active_moon.destroy()
                    asteroid.alive = False

            for moon in self.locked_moons:
                if moon.state == "locked" and asteroid.position.distance_to(moon.position) <= asteroid.radius + moon.radius:
                    moon.destroy()
                    asteroid.alive = False

        self.asteroids = [a for a in self.asteroids if a.alive]
        self.locked_moons = [m for m in self.locked_moons if m.state == "locked"]

    def update(self, dt: float) -> None:
        if self.phase == "planets":
            super().update(dt)
            if len(self.locked_planets) >= self.required_planets:
                self.phase = "moons"
                self.status_message = "Phase 2: Place moons while dodging asteroids"
                self.is_complete = False
                self.is_failed = False
                self._spawn_next_moon()
            return

        if self.is_complete or self.is_failed:
            return

        if self.active_moon:
            self.active_moon.update()
            self._try_lock_active_moon()
            if self.active_moon and self.active_moon.state == "destroyed":
                self.active_moon = None
                self._spawn_next_moon()

        self._update_asteroids(dt)

        if len(self.locked_moons) >= self.required_moons:
            self.is_complete = True
            self.status_message = "Complete solar system built"
            return

        no_moons_left = self.active_moon is None and self.moons_left_to_spawn <= 0
        if no_moons_left and len(self.locked_moons) < self.required_moons:
            self.is_failed = True
            self.status_message = "Moon phase failed"

    def draw(self, surface: pygame.Surface, font: pygame.font.Font) -> None:
        super().draw(surface, font)

        if self.phase == "moons":
            targets = self._moon_orbit_targets()
            for _, target in targets:
                pygame.draw.circle(surface, COLOR_NEON_BLUE, (int(target.x), int(target.y)), 10, 1)

            for moon in self.locked_moons:
                moon.draw(surface)
            if self.active_moon:
                self.active_moon.draw(surface)
            for asteroid in self.asteroids:
                asteroid.draw(surface)

            text = font.render("ASTEROID FIELD ACTIVE", True, COLOR_WHITE)
            phase = font.render("MOON PHASE", True, COLOR_NEON_GREEN)
            surface.blit(text, (34, 96))
            surface.blit(phase, (34, 126))
        else:
            hint = font.render("PHASE 1 / 2", True, COLOR_NEON_GREEN)
            surface.blit(hint, (34, 96))
