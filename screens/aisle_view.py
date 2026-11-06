# Owner: Ellie
# Shown after clicking an aisle. Displays the inside of the selected aisle with empty shelves
# (items get added in a later sprint). Has a Back button to return to the store page.

import config
from screens.base_screen import BaseScreen, MenuButton, draw_text
from components.shelf import Shelf
from data.aisles import get_aisle
 
 
class AisleView(BaseScreen):
    def __init__(self, state):
        super().__init__(state)
 
        margin = int(config.WIDTH * 0.1)
        shelf_w = config.WIDTH - 2 * margin
        slot_h = int(config.HEIGHT * 0.13)
        self.shelves = [
            Shelf(margin, int(config.HEIGHT * (0.24 + 0.22 * row)), shelf_w, slot_h=slot_h)
            for row in range(3)
        ]
        self.back_button = MenuButton(
            "Back", (24 + 75, config.HEIGHT - 49), self.go_back, size=(150, 50)
        )
 
    def go_back(self):
        self.state.change_screen("store_page")
 
    def handle_event(self, event):
        self.back_button.handle_event(event)
 
    def draw(self, surface):
        surface.fill(config.BACKGROUND)
        aisle = get_aisle(self.state.current_aisle)
        name = aisle["name"] if aisle else "Unknown"
        draw_text(surface, f"{name} Aisle", config.HEADING_SIZE,
                  (config.WIDTH // 2, int(config.HEIGHT * 0.11)))
 
        for shelf in self.shelves:
            shelf.draw(surface)
        self.back_button.draw(surface)
