import random
import pygame
from game.level_manager import BaseLevel
from objects.meteor import Meteor
from settings import COLOR_RED


class Level2(BaseLevel):
    level_number = 2
    title = "Meteor Attack"

    def __init__(self):
        super().__init__()
        self.total_planets = 8
        self.required_planets = 5
        self.planets_left_to_spawn = self.total_planets - 1  # one is already active from base init
        self.meteors: list[Meteor] = []
        self.meteor_spawn_timer = 0.0
        self.meteor_spawn_interval = 1.1
        self.status_message = "Place 5 planets in orbit. Meteors can destroy planets! Learn about space hazards."

    def _meteor_hits_planet(self, meteor: Meteor, planet) -> bool:
        return meteor.position.distance_to(planet.position) <= meteor.radius + planet.radius

    def update(self, dt: float) -> None:
        super().update(dt)
        if self.is_complete or self.is_failed:
            return

        self.meteor_spawn_timer += dt
        if self.meteor_spawn_timer >= self.meteor_spawn_interval:
            self.meteor_spawn_timer = 0.0
            self.meteors.append(Meteor())

        for meteor in self.meteors:
            meteor.update()

            if self.active_planet and self.active_planet.state in {"ready", "launched"}:
                if self._meteor_hits_planet(meteor, self.active_planet):
                    self.active_planet.destroy()
                    meteor.alive = False

            for planet in self.locked_planets:
                if planet.state == "locked" and self._meteor_hits_planet(meteor, planet):
                    planet.destroy()
                    meteor.alive = False

        self.locked_planets = [p for p in self.locked_planets if p.state == "locked"]
        self.meteors = [m for m in self.meteors if m.alive]
        self._check_end_state()

    def draw(self, surface: pygame.Surface, font: pygame.font.Font) -> None:
        super().draw(surface, font)
        for meteor in self.meteors:
            meteor.draw(surface)

        warn_text = font.render("WARNING: METEOR SHOWER", True, COLOR_RED)
        surface.blit(warn_text, (34, 96))
