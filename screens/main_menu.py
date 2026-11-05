# Owner: Arpa
# The first screen when the game opens.
# Buttons: Start (goes to avatar select), Instructions, and Settings.

import config
import game_state
from components.avatar import draw_avatar
from data.avatars import AVATARS
from screens.base_screen import BaseScreen, MenuButton, draw_text


class MainMenu(BaseScreen):
    def __init__(self, state):
        super().__init__(state)
        cx = config.WIDTH // 2
        self.buttons = [
            MenuButton("Start", (cx, 300), lambda: state.change_screen(game_state.AVATAR_SELECT)),
            MenuButton("Instructions", (cx, 380), lambda: state.change_screen(game_state.INSTRUCTIONS)),
            MenuButton("Settings", (cx, 460), lambda: state.change_screen(game_state.SETTINGS)),
            MenuButton("Quit", (cx, 540), state.quit),
        ]

    def handle_event(self, event):
        for button in self.buttons:
            button.handle_event(event)

    def draw(self, surface):
        surface.fill(config.BACKGROUND)
        draw_text(surface, config.TITLE, config.TITLE_SIZE, (config.WIDTH // 2, 130), config.ACCENT)
        draw_text(
            surface,
            "Shop fast. Deliver faster.",
            config.BODY_SIZE,
            (config.WIDTH // 2, 195),
            config.TEXT_MUTED,
        )
        # A couple of shoppers on either side of the buttons for decoration
        draw_avatar(surface, AVATARS[0], (220, 420), size=140)
        draw_avatar(surface, AVATARS[1], (config.WIDTH - 220, 420), size=140)
        for button in self.buttons:
            button.draw(surface)
