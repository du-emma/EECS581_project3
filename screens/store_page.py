# Owner: Megan
# The main store screen. Lays out:
#   - the player's avatar (Arpa's Avatar)
#   - placeholders for the timer, grocery list, and earnings (HudPlaceholders)

import os

import config
import game_state
import pygame
from components.avatar import draw_avatar
from components.button import Button
from components.hud_placeholders import HudPlaceholders
from data.avatars import get_avatar
from screens.base_screen import BaseScreen, draw_text


class StorePage(BaseScreen):
    def __init__(self, state):
        super().__init__(state)
        bg_path = os.path.join(config.STORE_DIR, "Store_Background.png")
        bg_image = pygame.image.load(bg_path).convert()
        self.bg_image = pygame.transform.smoothscale(
            bg_image, (config.WIDTH, config.HEIGHT)
        )
        self.hud = HudPlaceholders()
        self.paused = False
        center_x = config.WIDTH // 2
        self.continue_button = Button(
            "Continue",
            (center_x, config.HEIGHT // 2 + 35),
            lambda: setattr(self, "paused", False),
        )
        self.main_menu_button = Button(
            "Main Menu",
            (center_x, config.HEIGHT // 2 + 115),
            lambda: self.state.change_screen(game_state.MENU),
        )

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.paused = not self.paused
            return

        if self.paused:
            self.continue_button.handle_event(event)
            self.main_menu_button.handle_event(event)

    def draw(self, surface):
        surface.blit(self.bg_image, (0, 0))
        draw_avatar(
            surface,
            get_avatar(self.state.avatar_id),
            (config.WIDTH // 2, config.HEIGHT - 170),
            size=100,
        )
        self.hud.draw(surface)

        if self.paused:
            overlay = pygame.Surface((config.WIDTH, config.HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 160))
            surface.blit(overlay, (0, 0))
            draw_text(
                surface,
                "Paused",
                config.TITLE_SIZE,
                (config.WIDTH // 2, config.HEIGHT // 2 - 60),
                config.BUTTON_TEXT,
            )
            self.continue_button.draw(surface)
            self.main_menu_button.draw(surface)