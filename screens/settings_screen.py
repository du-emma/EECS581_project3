# Owner: Arpa
# Basic adjustable options, such as volume.
# Has a Back button to return to the main menu.

import pygame

import config
import game_state
from screens.base_screen import BaseScreen, MenuButton, draw_text

VOLUME_STEP = 10


class SettingsScreen(BaseScreen):
    def __init__(self, state):
        super().__init__(state)
        cx = config.WIDTH // 2
        self.buttons = [
            MenuButton("-", (cx - 220, 270), self.volume_down, size=(60, 60)),
            MenuButton("+", (cx + 220, 270), self.volume_up, size=(60, 60)),
            MenuButton("Back", (cx, config.HEIGHT - 70), lambda: state.change_screen(game_state.MENU)),
        ]
        self.bar = pygame.Rect(0, 0, 320, 24)
        self.bar.center = (cx, 270)

    def volume_down(self):
        self.state.volume = max(0, self.state.volume - VOLUME_STEP)

    def volume_up(self):
        self.state.volume = min(100, self.state.volume + VOLUME_STEP)

    def handle_event(self, event):
        for button in self.buttons:
            button.handle_event(event)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.state.change_screen(game_state.MENU)

    def draw(self, surface):
        surface.fill(config.BACKGROUND)
        draw_text(surface, "Settings", config.HEADING_SIZE, (config.WIDTH // 2, 80), config.ACCENT)
        draw_text(surface, f"Volume: {self.state.volume}", config.BODY_SIZE, (config.WIDTH // 2, 210))

        # Volume bar
        pygame.draw.rect(surface, config.CARD_BORDER, self.bar, border_radius=12)
        filled = self.bar.copy()
        filled.width = int(self.bar.width * self.state.volume / 100)
        if filled.width > 0:
            pygame.draw.rect(surface, config.ACCENT, filled, border_radius=12)

        for button in self.buttons:
            button.draw(surface)
