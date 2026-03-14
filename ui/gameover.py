import pygame
from settings import COLOR_BG, COLOR_NEON_BLUE, COLOR_NEON_PINK, COLOR_PANEL, COLOR_RED, COLOR_WHITE, SCREEN_HEIGHT, SCREEN_WIDTH


class GameOverScreen:
    def __init__(self):
        cx = SCREEN_WIDTH // 2
        cy = SCREEN_HEIGHT // 2
        self.retry_btn = pygame.Rect(cx - 130, cy + 30, 260, 56)
        self.menu_btn = pygame.Rect(cx - 130, cy + 100, 260, 56)

    def handle_event(self, event: pygame.event.Event) -> str | None:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.retry_btn.collidepoint(event.pos):
                return "retry"
            if self.menu_btn.collidepoint(event.pos):
                return "menu"
        return None

    def draw(self, surface: pygame.Surface, title_font: pygame.font.Font, body_font: pygame.font.Font, won: bool, score: int) -> None:
        surface.fill(COLOR_BG)
        title_color = COLOR_NEON_PINK if won else COLOR_RED
        title_text = "LEVEL COMPLETE" if won else "GAME OVER"

        title = title_font.render(title_text, True, title_color)
        subtitle = body_font.render(f"Score: {score}", True, COLOR_WHITE)
        surface.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 180))
        surface.blit(subtitle, (SCREEN_WIDTH // 2 - subtitle.get_width() // 2, 260))

        for rect, label in ((self.retry_btn, "Retry"), (self.menu_btn, "Main Menu")):
            pygame.draw.rect(surface, COLOR_PANEL, rect, border_radius=12)
            pygame.draw.rect(surface, COLOR_NEON_BLUE, rect, 2, border_radius=12)
            text = body_font.render(label, True, COLOR_WHITE)
            surface.blit(text, (rect.centerx - text.get_width() // 2, rect.centery - text.get_height() // 2))
