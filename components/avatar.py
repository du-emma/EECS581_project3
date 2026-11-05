# Owner: Arpa
# Draws the avatar the player chose. Shown on the store page, positioned at the current aisle.
# Style: chibi grocery worker — big head, thick dark outlines, green apron.
#
# Usage (e.g. from store_page.py):
#     from components.avatar import draw_avatar
#     from data.avatars import get_avatar
#     draw_avatar(surface, get_avatar(state.avatar_id), (x, y))

import pygame

# Avatars are designed on a 200 x 300 grid, drawn SCALE times bigger, then shrunk
# down to the size asked for — that keeps the edges smooth.
GRID_W, GRID_H = 200, 300
SCALE = 3
STROKE = 3.5  # outline thickness, in grid units

INK = (45, 38, 48)               # outlines + eyes
APRON = (52, 118, 62)            # green apron
APRON_DARK = (40, 96, 50)
TEE = (250, 250, 250)            # white t-shirt
PANTS = (38, 36, 42)
SHOES = (250, 250, 250)
SMILE = (150, 70, 70)
GLASSES = (45, 38, 48)

_cache = {}


def _u(v):
    return int(round(v * SCALE))


def _rect(x, y, w, h):
    return pygame.Rect(_u(x), _u(y), _u(w), _u(h))


def _shape(surf, kind, color, x, y, w, h, radius=0):
    # Draws a filled ellipse or rounded rectangle with a dark outline around it.
    outline = _rect(x - STROKE, y - STROKE, w + 2 * STROKE, h + 2 * STROKE)
    inner = _rect(x, y, w, h)
    if kind == "ellipse":
        pygame.draw.ellipse(surf, INK, outline)
        pygame.draw.ellipse(surf, color, inner)
    else:
        pygame.draw.rect(surf, INK, outline, border_radius=_u(radius + STROKE))
        pygame.draw.rect(surf, color, inner, border_radius=_u(radius))


def _line(surf, color, a, b, width):
    pygame.draw.line(surf, color, (_u(a[0]), _u(a[1])), (_u(b[0]), _u(b[1])), _u(width))


def _render(avatar):
    # Draws the avatar back-to-front on a big transparent canvas.
    surf = pygame.Surface((_u(GRID_W), _u(GRID_H)), pygame.SRCALPHA)
    skin, hair, style = avatar["skin"], avatar["hair"], avatar["hair_style"]

    # 1. Hair that hangs behind the head and back
    if style == "long":
        _shape(surf, "rect", hair, 30, 84, 140, 152, radius=44)
    elif style == "bob":
        _shape(surf, "rect", hair, 34, 84, 132, 100, radius=38)
    elif style == "ponytail":
        _shape(surf, "ellipse", hair, 18, 100, 46, 112)
    elif style == "bun":
        _shape(surf, "ellipse", hair, 54, 20, 50, 46)      # bun on top of the head

    # 2. Legs and shoes
    _shape(surf, "rect", PANTS, 70, 222, 60, 48, radius=6)
    _line(surf, INK, (100, 240), (100, 270), STROKE)
    _shape(surf, "ellipse", SHOES, 64, 262, 36, 18)
    _shape(surf, "ellipse", SHOES, 100, 262, 36, 18)

    # 3. Arms (skin), then t-shirt sleeves over the shoulders
    _shape(surf, "rect", skin, 50, 180, 20, 52, radius=10)
    _shape(surf, "rect", skin, 130, 180, 20, 52, radius=10)
    _shape(surf, "rect", TEE, 48, 160, 28, 32, radius=10)
    _shape(surf, "rect", TEE, 124, 160, 28, 32, radius=10)

    # 4. T-shirt body and apron with straps + pocket
    _shape(surf, "rect", TEE, 64, 156, 72, 74, radius=14)
    _shape(surf, "rect", APRON, 70, 172, 60, 60, radius=8)
    _line(surf, APRON, (78, 156), (78, 174), 8)
    _line(surf, APRON, (122, 156), (122, 174), 8)
    pygame.draw.rect(surf, APRON_DARK, _rect(88, 188, 24, 16), width=_u(2), border_radius=_u(3))

    # 5. Top of the hair (behind the head), then ears, then the head
    _shape(surf, "ellipse", hair, 32, 40, 136, 112)
    _shape(surf, "ellipse", skin, 30, 112, 24, 28)
    _shape(surf, "ellipse", skin, 146, 112, 24, 28)
    _shape(surf, "ellipse", skin, 40, 56, 120, 114)

    # 6. Hair around the face: side locks + side-swept bangs
    lock_h = 76 if style in ("long", "bob") else 40
    pygame.draw.rect(surf, hair, _rect(39, 70, 20, lock_h), border_radius=_u(10))
    pygame.draw.rect(surf, hair, _rect(141, 70, 20, lock_h), border_radius=_u(10))
    pygame.draw.ellipse(surf, hair, _rect(46, 50, 110, 44))
    pygame.draw.ellipse(surf, hair, _rect(40, 56, 62, 50))

    # 8. Face: tall oval eyes with a highlight and lash, then a small smile
    for ex, lash in ((78, -1), (122, 1)):
        pygame.draw.ellipse(surf, INK, _rect(ex - 10, 112, 20, 32))
        pygame.draw.ellipse(surf, (255, 255, 255), _rect(ex - 5, 117, 7, 9))
        _line(surf, INK, (ex + lash * 8, 115), (ex + lash * 15, 108), 3)
    smile = _rect(90, 148, 20, 10)
    pygame.draw.arc(surf, SMILE, smile, 3.5, 5.9, _u(2.2))

    # 9. Glasses: round frames around each eye + bridge
    if avatar["glasses"]:
        for ex in (78, 122):
            pygame.draw.ellipse(surf, GLASSES, _rect(ex - 19, 109, 38, 38), width=_u(3))
        _line(surf, GLASSES, (97, 128), (103, 128), 3)

    return surf


def draw_avatar(surface, avatar, center, size=60):
    # Draws the avatar centered at `center`. `size` is its total height in pixels.
    if avatar is None:
        return
    key = (avatar["id"], size)
    if key not in _cache:
        width = size * GRID_W // GRID_H
        _cache[key] = pygame.transform.smoothscale(_render(avatar), (width, size))
    image = _cache[key]
    surface.blit(image, image.get_rect(center=center))
