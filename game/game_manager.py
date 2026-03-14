import pygame
from game.level_manager import get_level
from settings import COLOR_BG, COLOR_NEON_BLUE, COLOR_NEON_GREEN, COLOR_WHITE, FPS
from ui.gameover import GameOverScreen
from ui.hud import HUD
from ui.menu import MainMenu


class GameManager:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.running = True

        self.state = "menu"  # menu, level_select, playing, paused, gameover
        self.selected_level = 1
        self.level = None
        self.last_result_won = False

        self.menu = MainMenu()
        self.hud = HUD()
        self.gameover = GameOverScreen()

        self.title_font = pygame.font.SysFont("impact", 78)
        self.body_font = pygame.font.SysFont("consolas", 28)
        self.hud_font = pygame.font.SysFont("consolas", 22)

    def _start_level(self, level_number: int) -> None:
        self.selected_level = max(1, min(4, level_number))
        self.level = get_level(self.selected_level)
        self.state = "playing"

    def _draw_level_select(self) -> None:
        self.screen.fill(COLOR_BG)
        title = self.title_font.render("SELECT LEVEL", True, COLOR_NEON_BLUE)
        self.screen.blit(title, (self.screen.get_width() // 2 - title.get_width() // 2, 120))

        for i in range(1, 5):
            active = i == self.selected_level
            text = self.body_font.render(f"[{i}] Level {i}", True, COLOR_NEON_GREEN if active else COLOR_WHITE)
            self.screen.blit(text, (self.screen.get_width() // 2 - 110, 220 + i * 60))

        hint = self.hud_font.render("Press 1-4 then ENTER to start. ESC to menu.", True, COLOR_WHITE)
        self.screen.blit(hint, (self.screen.get_width() // 2 - hint.get_width() // 2, self.screen.get_height() - 80))

    def _draw_pause_overlay(self) -> None:
        overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 120))
        self.screen.blit(overlay, (0, 0))
        text = self.title_font.render("PAUSED", True, COLOR_NEON_BLUE)
        hint = self.hud_font.render("ESC resume | M menu", True, COLOR_WHITE)
        self.screen.blit(text, (self.screen.get_width() // 2 - text.get_width() // 2, 200))
        self.screen.blit(hint, (self.screen.get_width() // 2 - hint.get_width() // 2, 320))

    def _handle_menu_event(self, event: pygame.event.Event) -> None:
        action = self.menu.handle_event(event)
        if action == "start":
            self._start_level(1)
        elif action == "level_select":
            self.state = "level_select"
        elif action == "quit":
            self.running = False

    def _handle_level_select_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_1, pygame.K_KP1):
                self.selected_level = 1
            elif event.key in (pygame.K_2, pygame.K_KP2):
                self.selected_level = 2
            elif event.key in (pygame.K_3, pygame.K_KP3):
                self.selected_level = 3
            elif event.key in (pygame.K_4, pygame.K_KP4):
                self.selected_level = 4
            elif event.key == pygame.K_RETURN:
                self._start_level(self.selected_level)
            elif event.key == pygame.K_ESCAPE:
                self.state = "menu"

    def _handle_playing_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and self.level:
                self._start_level(self.selected_level)
                return
            if event.key == pygame.K_ESCAPE:
                self.state = "paused"
                return

        if self.level:
            self.level.handle_event(event)

    def _handle_paused_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.state = "playing"
            elif event.key == pygame.K_m:
                self.state = "menu"

    def _handle_gameover_event(self, event: pygame.event.Event) -> None:
        action = self.gameover.handle_event(event)
        if action == "retry":
            if self.last_result_won and self.selected_level < 4:
                self._start_level(self.selected_level + 1)
            else:
                self._start_level(self.selected_level)
        elif action == "menu":
            self.state = "menu"

    def _update_playing(self, dt: float) -> None:
        if not self.level:
            return
        self.level.update(dt)

        if self.level.is_complete:
            self.last_result_won = True
            self.state = "gameover"
        elif self.level.is_failed:
            self.last_result_won = False
            self.state = "gameover"

    def _draw_playing(self) -> None:
        if not self.level:
            return

        self.level.draw(self.screen, self.hud_font)
        remaining = self.level.planets_left_to_spawn + (1 if self.level.active_planet is not None else 0)
        self.hud.draw(self.screen, self.hud_font, self.selected_level, self.level.score, remaining)

    def run(self) -> None:
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    continue

                if self.state == "menu":
                    self._handle_menu_event(event)
                elif self.state == "level_select":
                    self._handle_level_select_event(event)
                elif self.state == "playing":
                    self._handle_playing_event(event)
                elif self.state == "paused":
                    self._handle_paused_event(event)
                elif self.state == "gameover":
                    self._handle_gameover_event(event)

            if self.state == "playing":
                self._update_playing(dt)

            if self.state == "menu":
                self.menu.draw(self.screen, self.title_font, self.body_font)
            elif self.state == "level_select":
                self._draw_level_select()
            elif self.state in {"playing", "paused"}:
                self._draw_playing()
                if self.state == "paused":
                    self._draw_pause_overlay()
            elif self.state == "gameover" and self.level:
                self.gameover.draw(self.screen, self.title_font, self.body_font, self.last_result_won, self.level.score)

            pygame.display.flip()
