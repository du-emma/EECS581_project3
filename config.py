# Shared by everyone. Agree on changes as a team before editing.
# Game-wide constants: window width/height, frames per second, colors, font sizes,
# and paths to the assets folders.

import os

# Window
WIDTH = 960
HEIGHT = 640
FPS = 60
TITLE = "Grocery Rush"

# Colors (R, G, B)
BACKGROUND = (246, 241, 230)
TEXT = (40, 40, 40)
TEXT_MUTED = (110, 110, 110)
ACCENT = (52, 140, 82)          # grocery green
BUTTON = (52, 140, 82)
BUTTON_HOVER = (40, 112, 64)
BUTTON_TEXT = (255, 255, 255)
CARD = (255, 255, 255)
CARD_BORDER = (210, 204, 190)
SELECTED = (240, 170, 40)

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
