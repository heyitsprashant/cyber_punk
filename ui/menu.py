import pygame
from settings import (
    COLOR_BG,
    COLOR_NEON_BLUE,
    COLOR_NEON_GREEN,
    COLOR_NEON_PINK,
    COLOR_PANEL,
    COLOR_WHITE,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
)


class MainMenu:
    def __init__(self):
        cx = SCREEN_WIDTH // 2
        cy = SCREEN_HEIGHT // 2
        self.buttons = {
            "start": pygame.Rect(cx - 140, cy - 40, 280, 58),
            "level_select": pygame.Rect(cx - 140, cy + 34, 280, 58),
            "quit": pygame.Rect(cx - 140, cy + 108, 280, 58),
        }

        # Optional artwork: if you drop files into an assets/ folder they will be used.
        self.bg_image: pygame.Surface | None = None
        self.logo_image: pygame.Surface | None = None
        try:
            self.bg_image = pygame.image.load("assets/menu_background.png").convert()
        except Exception:
            self.bg_image = None
        try:
            self.logo_image = pygame.image.load("assets/logo.png").convert_alpha()
        except Exception:
            self.logo_image = None

    def handle_event(self, event: pygame.event.Event) -> str | None:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for name, rect in self.buttons.items():
                if rect.collidepoint(event.pos):
                    return name
        return None

    def draw(self, surface: pygame.Surface, title_font: pygame.font.Font, body_font: pygame.font.Font) -> None:
        if self.bg_image:
            bg = pygame.transform.smoothscale(self.bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
            surface.blit(bg, (0, 0))
        else:
            surface.fill(COLOR_BG)

            # Neon stripe background for a space-punk vibe.
            for i in range(0, SCREEN_WIDTH, 40):
                color = (20 + (i // 2) % 90, 10, 40 + i % 140)
                pygame.draw.line(surface, color, (i, 0), (i - 200, SCREEN_HEIGHT), 1)

        if self.logo_image:
            logo = self.logo_image
            logo_rect = logo.get_rect()
            logo_rect.centerx = SCREEN_WIDTH // 2
            logo_rect.top = 80
            surface.blit(logo, logo_rect)
            subtitle_y = logo_rect.bottom + 20
        else:
            title = title_font.render("SPACE-PUNK", True, COLOR_NEON_PINK)
            subtitle_y = 200
            surface.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 130))

        subtitle = body_font.render("Launch planets. Build a neon solar system.", True, COLOR_WHITE)
        surface.blit(subtitle, (SCREEN_WIDTH // 2 - subtitle.get_width() // 2, subtitle_y))

        for label, rect in self.buttons.items():
            pygame.draw.rect(surface, COLOR_PANEL, rect, border_radius=12)
            pygame.draw.rect(surface, COLOR_NEON_BLUE, rect, 2, border_radius=12)
            text = body_font.render(label.replace("_", " ").title(), True, COLOR_NEON_GREEN)
            surface.blit(text, (rect.centerx - text.get_width() // 2, rect.centery - text.get_height() // 2))
