# Owner: Arpa
# The template every screen follows, so main.py can treat them all the same way.
# Each screen should have: handle_event(event), update(dt), and draw(surface).
# Also has a simple MenuButton used by the menu screens.

import pygame

import config
from components.button import Button as MenuButton


class BaseScreen:
    def __init__(self, state):
        self.state = state  # the shared GameState

    def handle_event(self, event):
        pass

    def update(self, dt):
        # dt = seconds since the last frame
        pass

    def draw(self, surface):
        pass


def draw_text(surface, text, size, center, color=config.TEXT):
    font = pygame.font.Font(None, size)
    image = font.render(text, True, color)
    surface.blit(image, image.get_rect(center=center))
