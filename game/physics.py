import math
import pygame


def projectile_step(position: pygame.Vector2, velocity: pygame.Vector2, gravity: float) -> tuple[pygame.Vector2, pygame.Vector2]:
    """Basic projectile motion integrator used by moving objects."""
    position = position + velocity
    velocity = pygame.Vector2(velocity.x, velocity.y + gravity)
    return position, velocity


def clamp_vector_length(vec: pygame.Vector2, max_length: float) -> pygame.Vector2:
    if vec.length_squared() == 0:
        return pygame.Vector2()
    if vec.length() <= max_length:
        return vec
    return vec.normalize() * max_length


def launch_velocity(anchor: pygame.Vector2, mouse_pos: tuple[int, int], power_factor: float, max_drag: float) -> pygame.Vector2:
    drag_vec = anchor - pygame.Vector2(mouse_pos)
    drag_vec = clamp_vector_length(drag_vec, max_drag)
    return drag_vec * power_factor


def distance(a: pygame.Vector2, b: pygame.Vector2) -> float:
    return math.hypot(a.x - b.x, a.y - b.y)
