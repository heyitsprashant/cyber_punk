import pygame
from settings import COLOR_NEON_BLUE, COLOR_NEON_GREEN, COLOR_PANEL, COLOR_WHITE


class HUD:
    def draw(self, surface: pygame.Surface, font: pygame.font.Font, level_number: int, score: int, remaining: int) -> None:
        rect = pygame.Rect(surface.get_width() - 330, 20, 300, 118)
        pygame.draw.rect(surface, COLOR_PANEL, rect, border_radius=10)
        pygame.draw.rect(surface, COLOR_NEON_BLUE, rect, 2, border_radius=10)

        lines = [
            f"Level: {level_number}",
            f"Score: {score}",
            f"Remaining Planets: {remaining}",
            "R: Restart   ESC: Pause/Menu",
        ]

        for i, line in enumerate(lines):
            color = COLOR_NEON_GREEN if i < 3 else COLOR_WHITE
            text = font.render(line, True, color)
            surface.blit(text, (rect.x + 14, rect.y + 12 + i * 24))
