# Owner: Ellie
# Shown after clicking an aisle. Loads that aisle's items from the DB and shows
# each item's name, price, and stock quantity on the shelves.

import pygame

import game_state
import config
from screens.base_screen import BaseScreen, MenuButton, draw_text
from components.checklist import Checklist
from components.hud_placeholders import HudPlaceholders
from components.shelf import Shelf
from data.aisles import get_aisle, get_aisle_items
from data.items import decrement_stock


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
        self._stock_shelves()
        # R10: the clipboard doesn't fit beside the shelves, so show a strip below them.
        self.checklist = Checklist()
        self.checklist_rect = pygame.Rect(0, 0, config.WIDTH - 196 - 24, 74)
        self.checklist_rect.topleft = (196, config.HEIGHT - 86)
        self.hud = HudPlaceholders(
            state,
            show_clipboard=False,
            on_stock_changed=self._sync_stock,
        )
        self.back_button = MenuButton(
            "Back", (24 + 75, config.HEIGHT - 49), self.go_back, size=(150, 50)
        )

    def _stock_shelves(self):
        """Pull this aisle's items from SQLite and lay them across the shelf rows."""
        items = get_aisle_items(self.state.current_aisle_id)
        slots_per_shelf = len(self.shelves[0].items) if self.shelves else 5
        for i, shelf in enumerate(self.shelves):
            start = i * slots_per_shelf
            shelf.place_items(items[start : start + slots_per_shelf])

    def go_back(self):
        self.state.close_cart()
        self.state.change_screen(game_state.STORE)

    def _sync_stock(self, item_id, stock_quantity):
        for shelf in self.shelves:
            for item in shelf.items:
                if item is not None and item.get("item_id") == item_id:
                    item["stock_quantity"] = stock_quantity

    def handle_event(self, event):
        if self.hud.handle_event(event):
            return
        self.back_button.handle_event(event)
        if event.type != pygame.MOUSEBUTTONDOWN or event.button != 1:
            return
        if self.back_button.rect.collidepoint(event.pos):
            return

        for shelf in self.shelves:
            item, slot = shelf.item_at_pos(event.pos)
            if item is None:
                continue
            if item.get("stock_quantity", 0) <= 0:
                return
            shelf.flash_slot(slot)
            updated = decrement_stock(item["item_id"])
            if updated is not None:
                item["stock_quantity"] = updated["stock_quantity"]
            self.state.add_to_cart(item)
            return

    def update(self, dt):
        for shelf in self.shelves:
            shelf.update(dt)

    def draw(self, surface):
        surface.fill(config.BACKGROUND)
        aisle = get_aisle(self.state.current_aisle_id)
        name = aisle["name"] if aisle else "Unknown"
        draw_text(
            surface,
            f"{name} Aisle",
            config.HEADING_SIZE,
            (config.WIDTH // 2, int(config.HEIGHT * 0.11)),
        )

        for shelf in self.shelves:
            shelf.draw(surface)
        self.back_button.draw(surface)
        self.checklist.draw_compact(surface, self.state, self.checklist_rect)
        self.hud.draw(surface)