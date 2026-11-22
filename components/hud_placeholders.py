# Owner: Emma, Megan
# HUD display for the order timer, grocery list, and earnings.

import math
import os

import pygame

import config
from components.shopping_cart import ShoppingCart
from components.checklist import Checklist 
from screens.base_screen import draw_text


class HudPlaceholders:
    def __init__(self, state, show_clipboard=True, on_stock_changed=None):
        self.state = state
        self.show_clipboard = show_clipboard
        self.timer_rect = pygame.Rect(24, 24, 180, 118)
        clipboard_path = os.path.join(config.STORE_DIR, "Clipboard.png")
        self.clipboard_image = pygame.image.load(clipboard_path).convert_alpha()
        self.clipboard_rect = self.clipboard_image.get_rect(
            topright=(config.WIDTH - 24, 128)
        )
        self.earnings_rect = pygame.Rect(
            config.WIDTH - 214, 24, 190, 86
        )
        self.cart = ShoppingCart(state, self.earnings_rect, on_stock_changed)
        self.checklist = Checklist()

    def draw(self, surface):
        self._draw_panel(surface, self.timer_rect)
        draw_text(
            surface,
            "TIMER",
            config.BODY_SIZE,
            (self.timer_rect.centerx, 47),
            config.ACCENT,
        )
        seconds = math.ceil(self.state.remaining)
        timer_text = f"{seconds // 60:02d}:{seconds % 60:02d}"
        draw_text(
            surface,
            timer_text,
            config.HEADING_SIZE,
            (self.timer_rect.centerx, 84),
            config.TEXT,
        )
        if self.state.order_expired:
            draw_text(
                surface,
                "ORDER EXPIRED",
                21,
                (self.timer_rect.centerx, 124),
                config.SELECTED,
            )

        if self.show_clipboard:
            surface.blit(self.clipboard_image, self.clipboard_rect)
            self.checklist.draw_in_rect(surface, self.state, self.clipboard_rect)

        self._draw_panel(surface, self.earnings_rect)
        draw_text(
            surface, "EARNINGS", 26,
            (self.earnings_rect.centerx, self.earnings_rect.top + 24),
            config.ACCENT,
        )
        draw_text(
            surface,
            f"${self.state.earnings:.2f}",
            config.BODY_SIZE,
            (self.earnings_rect.centerx, self.earnings_rect.top + 60),
            config.TEXT,
        )
        self.cart.draw(surface)

    def handle_event(self, event):
        return self.cart.handle_event(event)

    @staticmethod
    def _draw_panel(surface, rect):
        pygame.draw.rect(surface, config.CARD, rect, border_radius=12)
        pygame.draw.rect(
            surface, config.CARD_BORDER, rect, width=2, border_radius=12
        )
