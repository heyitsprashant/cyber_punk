import pygame
from settings import BASE_POWER_FACTOR, COLOR_NEON_BLUE, COLOR_NEON_PINK, MAX_DRAG_DISTANCE
from game.physics import clamp_vector_length


class Slingshot:
    def __init__(self, anchor: pygame.Vector2):
        self.anchor = pygame.Vector2(anchor)
        self.dragging = False
        self.current_mouse = pygame.Vector2(anchor)

    def begin_drag(self, mouse_pos: tuple[int, int]) -> None:
        self.dragging = True
        self.current_mouse = pygame.Vector2(mouse_pos)

    def update_drag(self, mouse_pos: tuple[int, int]) -> None:
        if self.dragging:
            self.current_mouse = pygame.Vector2(mouse_pos)

    def release(self) -> None:
        self.dragging = False

    def get_launch_velocity(self) -> pygame.Vector2:
        drag_vec = self.anchor - self.current_mouse
        drag_vec = clamp_vector_length(drag_vec, MAX_DRAG_DISTANCE)
        return drag_vec * BASE_POWER_FACTOR

    def draw(self, surface: pygame.Surface) -> None:
        # Draw base post
        pygame.draw.rect(surface, COLOR_NEON_BLUE, (self.anchor.x - 10, self.anchor.y - 45, 20, 70), border_radius=8)

        # Draw elastic bands while aiming
        if self.dragging:
            pull = self.anchor - self.current_mouse
            pull = clamp_vector_length(pull, MAX_DRAG_DISTANCE)
            draw_point = self.anchor - pull
            pygame.draw.line(surface, COLOR_NEON_PINK, (self.anchor.x - 14, self.anchor.y - 20), draw_point, 4)
            pygame.draw.line(surface, COLOR_NEON_PINK, (self.anchor.x + 14, self.anchor.y - 20), draw_point, 4)
            pygame.draw.circle(surface, COLOR_NEON_BLUE, (int(draw_point.x), int(draw_point.y)), 12)
