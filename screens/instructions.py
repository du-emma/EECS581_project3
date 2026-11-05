# Owner: Arpa
# Explains how to play: shopping, clicking aisles, the timer, and deliveries.
# Has a Back button to return to the main menu.

import pygame

import config
import game_state
from screens.base_screen import BaseScreen, MenuButton, draw_text

STEPS = [
    "1. You're a grocery shopper with a customer's order to fill.",
    "2. Pick your avatar, then head into the store.",
    "3. Click an aisle on the store map to walk into it.",
    "4. Find the items on the grocery list and add them to your cart.",
    "5. Check out, then drive to the customer's house to deliver.",
    "6. Watch the timer! Faster deliveries earn bigger tips.",
    "7. Spend your earnings on power-ups to shop even faster.",
]


class Instructions(BaseScreen):
    def __init__(self, state):
        super().__init__(state)
        self.back = MenuButton(
            "Back",
            (config.WIDTH // 2, config.HEIGHT - 70),
            lambda: state.change_screen(game_state.MENU),
        )

    def handle_event(self, event):
        self.back.handle_event(event)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.state.change_screen(game_state.MENU)

    def draw(self, surface):
        surface.fill(config.BACKGROUND)
        draw_text(surface, "How to Play", config.HEADING_SIZE, (config.WIDTH // 2, 80), config.ACCENT)
        font = pygame.font.Font(None, config.BODY_SIZE)
        for i, line in enumerate(STEPS):
            surface.blit(font.render(line, True, config.TEXT), (130, 150 + i * 50))
        self.back.draw(surface)
