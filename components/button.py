# Owner: Megan
# A reusable clickable button (rectangle + text) so every screen's buttons look the same.
# Should detect when it is clicked.

import pygame

import config


class Button:
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
        font = pygame.font.Font(None, config.BUTTON_SIZE)
        image = font.render(self.text, True, config.BUTTON_TEXT)
        surface.blit(image, image.get_rect(center=self.rect.center))
