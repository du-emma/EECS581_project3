# Owner: Arpa
# Draws the avatar the player chose. Shown on the store page, positioned at the current aisle.
#
# Usage (e.g. from store_page.py):
#     from components.avatar import draw_avatar
#     from data.avatars import get_avatar
#     draw_avatar(surface, get_avatar(state.avatar_id), (x, y))

import pygame

from config import OUTLINE

HAIR = (60, 40, 30)
EYES = (30, 25, 35)


def draw_avatar(surface, avatar, center, size=60):
    # Draws a simple shopper: body + head. `size` is the total height in pixels.
    if avatar is None:
        return
    x, y = center
    head_radius = size // 5
    body_w = size // 2
    body_h = size // 2

    # Body (shirt)
    body = pygame.Rect(0, 0, body_w, body_h)
    body.midbottom = (x, y + size // 2)
    pygame.draw.rect(surface, avatar["shirt"], body, border_radius=size // 8)
    pygame.draw.rect(surface, OUTLINE, body, width=2, border_radius=size // 8)

    # Head
    head_center = (x, body.top - head_radius + 2)
    pygame.draw.circle(surface, avatar["skin"], head_center, head_radius)
    # Hair on top half of the head
    hair_rect = pygame.Rect(0, 0, head_radius * 2, head_radius * 2)
    hair_rect.center = head_center
    pygame.draw.arc(surface, HAIR, hair_rect, 0.2, 2.94, max(2, head_radius // 2))
    pygame.draw.circle(surface, OUTLINE, head_center, head_radius, width=2)

    # Eyes
    eye_y = head_center[1] + head_radius // 6
    eye_dx = head_radius // 2
    eye_r = max(2, size // 30)
    pygame.draw.circle(surface, EYES, (x - eye_dx, eye_y), eye_r)
    pygame.draw.circle(surface, EYES, (x + eye_dx, eye_y), eye_r)
