# Owner: Megan
# Placeholder boxes for the timer, grocery list, and earnings.
# These just reserve space on the store page for now; they get real values in later sprints.

import os

import pygame

import config
from screens.base_screen import draw_text


class HudPlaceholders:
    def __init__(self):
        self.timer_rect = pygame.Rect(24, 24, 150, 88)
        clipboard_path = os.path.join(config.STORE_DIR, "Clipboard.png")
        self.clipboard_image = pygame.image.load(clipboard_path).convert_alpha()
        self.clipboard_rect = self.clipboard_image.get_rect(
            topright=(config.WIDTH - 24, 24)
        )
        self.earnings_rect = pygame.Rect(
            config.WIDTH - 214, config.HEIGHT - 110, 190, 86
        )

    def draw(self, surface):
        self._draw_panel(surface, self.timer_rect)
        draw_text(
            surface,
            "TIMER",
            config.BODY_SIZE,
            (self.timer_rect.centerx, 47),
            config.ACCENT,
        )
        draw_text(
            surface,
            "--:--",
            config.HEADING_SIZE,
            (self.timer_rect.centerx, 84),
            config.TEXT,
        )

        surface.blit(self.clipboard_image, self.clipboard_rect)

        self._draw_panel(surface, self.earnings_rect)
        draw_text(
            surface, "EARNINGS", 26,
            (self.earnings_rect.centerx, self.earnings_rect.top + 24),
            config.ACCENT,
        )
        draw_text(
            surface,
            "$0.00",
            config.BODY_SIZE,
            (self.earnings_rect.centerx, self.earnings_rect.top + 60),
            config.TEXT,
        )

    @staticmethod
    def _draw_panel(surface, rect):
        pygame.draw.rect(surface, config.CARD, rect, border_radius=12)
        pygame.draw.rect(
            surface, config.CARD_BORDER, rect, width=2, border_radius=12
        )
