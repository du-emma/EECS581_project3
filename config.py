# Shared by everyone. Agree on changes as a team before editing.
# Game-wide constants: window width/height, frames per second, colors, font sizes,
# and paths to the assets folders.

import os

# Window — same shape as Megan's store art (2360x1640), scaled to 40%
WIDTH = 1180
HEIGHT = 720
FPS = 60
TITLE = "Grocery Rush"

# Colors (R, G, B) — matched to Megan's store background
WALL = (230, 230, 253)          # pale lavender wall
FLOOR = (107, 107, 159)         # dusty purple floor tiles
OUTLINE = (85, 85, 135)         # deep purple tile lines / outlines
DOOR = (176, 176, 222)          # soft periwinkle door frame

BACKGROUND = WALL
TEXT = (60, 60, 100)
TEXT_MUTED = (120, 120, 165)
ACCENT = OUTLINE
BUTTON = FLOOR
BUTTON_HOVER = OUTLINE
BUTTON_TEXT = (255, 255, 255)
CARD = (255, 255, 255)
CARD_BORDER = DOOR
SELECTED = (240, 170, 40)       # gold, so the picked avatar stands out against the purples

# Font sizes
TITLE_SIZE = 84
HEADING_SIZE = 48
BODY_SIZE = 30
BUTTON_SIZE = 32

# Asset folders
ASSETS_DIR = os.path.join(os.path.dirname(__file__), "assets")
AVATAR_DIR = os.path.join(ASSETS_DIR, "avatars")
STORE_DIR = os.path.join(ASSETS_DIR, "store")
UI_DIR = os.path.join(ASSETS_DIR, "ui")
FONT_DIR = os.path.join(ASSETS_DIR, "fonts")
