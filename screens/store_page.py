# Owner: Emma, Megan
# The main store screen. Lays out the player's avatar, HUD, and aisles.

import os

import config
import game_state
import pygame
from components.aisle import Aisle
from components.avatar import draw_avatar
from components.button import Button
from components.hud_placeholders import HudPlaceholders
from data.aisles import AISLES
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
        self.aisles = [
            Aisle(aisle["id"], aisle["name"], aisle["rect"], state)
            for aisle in AISLES
        ]
        self.hud = HudPlaceholders(state)
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
        self.play_again_button = Button(
            "Play Again",
            (center_x, config.HEIGHT // 2 + 35),
            self.state.play_again,
        )
        self.expired_main_menu_button = Button(
            "Main Menu",
            (center_x, config.HEIGHT // 2 + 115),
            lambda: self.state.change_screen(game_state.MENU),
        )

    def handle_event(self, event):
        if self.state.order_expired:
            self.play_again_button.handle_event(event)
            self.expired_main_menu_button.handle_event(event)
            return

        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.paused = not self.paused
            return

        if self.paused:
            self.continue_button.handle_event(event)
            self.main_menu_button.handle_event(event)
            return

        for aisle in self.aisles:
            if aisle.handle_event(event):
                break

    def draw(self, surface):
        surface.blit(self.bg_image, (0, 0))
        for aisle in self.aisles:
            aisle.draw(surface)
        draw_avatar(
            surface,
            get_avatar(self.state.avatar_id),
            (config.WIDTH // 2, config.HEIGHT - 170),
            size=100,
        )
        self.hud.draw(surface)

        if self.state.order_expired:
            overlay = pygame.Surface((config.WIDTH, config.HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 170))
            surface.blit(overlay, (0, 0))

            popup_rect = pygame.Rect(0, 0, 420, 300)
            popup_rect.center = (config.WIDTH // 2, config.HEIGHT // 2)
            pygame.draw.rect(surface, config.CARD, popup_rect, border_radius=16)
            pygame.draw.rect(
                surface, config.CARD_BORDER, popup_rect, width=3, border_radius=16
            )
            draw_text(
                surface,
                "Time's Up!",
                config.HEADING_SIZE,
                (popup_rect.centerx, popup_rect.top + 55),
                config.ACCENT,
            )
            draw_text(
                surface,
                f"You earned ${self.state.earnings:.2f}",
                config.BODY_SIZE,
                (popup_rect.centerx, popup_rect.top + 105),
                config.TEXT,
            )
            self.play_again_button.draw(surface)
            self.expired_main_menu_button.draw(surface)
        elif self.paused:
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
