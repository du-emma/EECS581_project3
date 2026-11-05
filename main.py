# Owner: Arpa
# Starts the game: sets up pygame and the window, then runs the main game loop.
# Each frame it passes events to the current screen, updates it, and draws it.
# Switches screens when game_state says the screen has changed.

import pygame

import config
import game_state
from game_state import GameState
from screens import aisle_view, store_page
from screens.avatar_select import AvatarSelect
from screens.base_screen import BaseScreen, draw_text
from screens.instructions import Instructions
from screens.main_menu import MainMenu
from screens.settings_screen import SettingsScreen


class NotBuiltYet(BaseScreen):
    # Stand-in for screens that haven't been written yet. Esc goes back to the menu.

    def __init__(self, state, name):
        super().__init__(state)
        self.name = name

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.state.change_screen(game_state.MENU)

    def draw(self, surface):
        surface.fill(config.BACKGROUND)
        draw_text(surface, f"{self.name} - not built yet", config.HEADING_SIZE,
                  (config.WIDTH // 2, config.HEIGHT // 2 - 20))
        draw_text(surface, "Press Esc to return to the menu", config.BODY_SIZE,
                  (config.WIDTH // 2, config.HEIGHT // 2 + 40), config.TEXT_MUTED)


# Screen name -> screen class. Megan's StorePage and Ellie's AisleView are picked up
# automatically once those classes exist in screens/store_page.py and screens/aisle_view.py.
SCREENS = {
    game_state.MENU: MainMenu,
    game_state.INSTRUCTIONS: Instructions,
    game_state.SETTINGS: SettingsScreen,
    game_state.AVATAR_SELECT: AvatarSelect,
    game_state.STORE: getattr(store_page, "StorePage", None),
    game_state.AISLE: getattr(aisle_view, "AisleView", None),
}


def make_screen(state):
    screen_class = SCREENS.get(state.screen)
    if screen_class is None:
        return NotBuiltYet(state, state.screen.replace("_", " ").title())
    return screen_class(state)


def main():
    pygame.init()
    window = pygame.display.set_mode((config.WIDTH, config.HEIGHT))
    pygame.display.set_caption(config.TITLE)
    clock = pygame.time.Clock()

    state = GameState()
    current_name = state.screen
    current = make_screen(state)

    while state.running:
        dt = clock.tick(config.FPS) / 1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                state.quit()
            else:
                current.handle_event(event)
            # Switch right away so the rest of this frame's events go to the new screen
            if state.screen != current_name:
                current_name = state.screen
                current = make_screen(state)

        current.update(dt)
        current.draw(window)
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
