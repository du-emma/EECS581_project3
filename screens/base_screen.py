# Owner: Arpa
# The template every screen follows, so main.py can treat them all the same way.
# Each screen should have: handle_event(event), update(dt), and draw(surface).
# Also has a simple MenuButton used by the menu screens.

import pygame

import config


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


class MenuButton:
    # A simple clickable rectangle with text. Calls on_click() when clicked.

    def __init__(self, text, center, on_click, size=(260, 60)):
        self.text = text
        self.rect = pygame.Rect(0, 0, *size)
        self.rect.center = center
        self.on_click = on_click
        self.enabled = True

    def handle_event(self, event):
        if (
            self.enabled
            and event.type == pygame.MOUSEBUTTONDOWN
            and event.button == 1
            and self.rect.collidepoint(event.pos)
        ):
            self.on_click()

    def draw(self, surface):
        if not self.enabled:
            color = config.CARD_BORDER
        elif self.rect.collidepoint(pygame.mouse.get_pos()):
            color = config.BUTTON_HOVER
        else:
            color = config.BUTTON
        pygame.draw.rect(surface, color, self.rect, border_radius=12)
        draw_text(surface, self.text, config.BUTTON_SIZE, self.rect.center, config.BUTTON_TEXT)
