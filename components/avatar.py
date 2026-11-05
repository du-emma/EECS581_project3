# Owner: Arpa
# Draws the avatar the player chose. Shown on the store page, positioned at the current aisle.
#
# Usage (e.g. from store_page.py):
#     from components.avatar import draw_avatar
#     from data.avatars import get_avatar
#     draw_avatar(surface, get_avatar(state.avatar_id), (x, y))

import pygame

from config import OUTLINE

EYES = (30, 25, 35)
SMILE = (120, 50, 60)
GLASSES = (40, 40, 60)


def draw_avatar(surface, avatar, center, size=60):
    # Draws a simple shopper: shirt, hair, face, and optional glasses.
    # `center` is the middle of the avatar; `size` is its total height in pixels.
    if avatar is None:
        return
    x, y = center
    r = size // 5                      # head radius
    line = max(1, size // 40)          # outline thickness
    hair = avatar["hair"]
    style = avatar["hair_style"]

    # Body (shirt)
    body = pygame.Rect(0, 0, size // 2, size // 2)
    body.midbottom = (x, y + size // 2)
    head = (x, body.top - r + size // 20)

    # Hair behind the back — drawn first so the shirt and face go on top of it
    if style == "long":
        back = pygame.Rect(0, 0, int(r * 2.8), int(r * 3.2))
        back.midtop = (x, head[1] - r // 2)
        pygame.draw.rect(surface, hair, back, border_radius=r // 2)
    elif style == "bob":
        back = pygame.Rect(0, 0, int(r * 2.5), int(r * 1.6))
        back.midtop = (x, head[1] - r // 2)
        pygame.draw.rect(surface, hair, back, border_radius=r // 2)
    elif style == "ponytail":
        tail = pygame.Rect(0, 0, int(r * 0.6), int(r * 1.5))
        tail.midtop = (x + int(r * 1.05), head[1] - r // 3)
        pygame.draw.rect(surface, hair, tail, border_radius=r // 3)
        pygame.draw.circle(surface, hair, (x + int(r * 0.9), head[1] - r // 3), int(r * 0.5))
    elif style == "bun":
        pygame.draw.circle(surface, hair, (x, head[1] - r), int(r * 0.5))

    # Shirt
    pygame.draw.rect(surface, avatar["shirt"], body, border_radius=size // 8)
    pygame.draw.rect(surface, OUTLINE, body, width=line, border_radius=size // 8)

    # Hair on top of the head, then the face slightly lower so a hairline shows
    pygame.draw.circle(surface, hair, head, r + line + 1)
    face = (x, head[1] + r // 5)
    pygame.draw.circle(surface, avatar["skin"], face, r - r // 8)
    # Side-swept bangs
    bangs = pygame.Rect(0, 0, int(r * 1.3), int(r * 0.7))
    bangs.midtop = (x - r // 5, head[1] - r + line)
    pygame.draw.ellipse(surface, hair, bangs)

    # Eyes
    eye_y = face[1] + r // 8
    eye_dx = int(r * 0.4)
    eye_r = max(2, r // 7)
    pygame.draw.circle(surface, EYES, (x - eye_dx, eye_y), eye_r)
    pygame.draw.circle(surface, EYES, (x + eye_dx, eye_y), eye_r)

    # Glasses: a ring around each eye plus a bridge
    if avatar["glasses"]:
        lens_r = max(3, int(r * 0.3))
        glass_line = max(1, size // 55)
        for side in (-1, 1):
            pygame.draw.circle(surface, GLASSES, (x + side * eye_dx, eye_y), lens_r, width=glass_line)
        pygame.draw.line(surface, GLASSES, (x - eye_dx + lens_r, eye_y), (x + eye_dx - lens_r, eye_y), glass_line)

    # Smile
    smile = pygame.Rect(0, 0, int(r * 0.55), int(r * 0.35))
    smile.midtop = (x, eye_y + r // 4)
    pygame.draw.arc(surface, SMILE, smile, 3.5, 5.9, max(1, size // 70))
