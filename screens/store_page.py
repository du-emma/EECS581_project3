# Owner: Megan
# The main store screen. Lays out:
#   - the player's avatar (Arpa's Avatar)
#   - placeholders for the timer, grocery list, and earnings (HudPlaceholders)

import os

import config
import game_state
import pygame
from screens.base_screen import BaseScreen, draw_text


class StorePage(BaseScreen):
    def __init__(self, state):
        super().__init__(state)
        bg_path = os.path.join(config.STORE_DIR, "Store_Background.png")
        bg_image = pygame.image.load(bg_path).convert()
        self.bg_image = pygame.transform.smoothscale(
            bg_image, (config.WIDTH, config.HEIGHT)
        )
        cx = config.WIDTH // 2
        self.buttons = [
            #MenuButton("Start", (cx, 300), lambda: state.change_screen(game_state.AVATAR_SELECT)),
            #MenuButton("Instructions", (cx, 380), lambda: state.change_screen(game_state.INSTRUCTIONS)),
            #MenuButton("Settings", (cx, 460), lambda: state.change_screen(game_state.SETTINGS)),
            #MenuButton("Quit", (cx, 540), state.quit),
        ]

    def handle_event(self, event):
        for button in self.buttons:
            button.handle_event(event)

    def draw(self, surface):
        surface.blit(self.bg_image, (0, 0))
        for button in self.buttons:
            button.draw(surface)