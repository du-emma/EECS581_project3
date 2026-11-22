import os
import unittest
from unittest.mock import patch

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")

import pygame

import config
from components.hud_placeholders import HudPlaceholders
from components.shopping_cart import ShoppingCart
from game_state import GameState
from screens.aisle_view import AisleView


def _click(pos):
    return pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"button": 1, "pos": pos})


class ShoppingCartUITests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pygame.init()
        pygame.display.set_mode((config.WIDTH, config.HEIGHT))

    def setUp(self):
        self.state = GameState()
        self.anchor = pygame.Rect(config.WIDTH - 214, 24, 190, 86)
        self.cart = ShoppingCart(self.state, self.anchor)

    def test_icon_sits_just_left_of_the_earnings_box(self):
        self.assertLess(self.cart.icon_rect.right, self.anchor.left)
        self.assertEqual(self.cart.icon_rect.centery, self.anchor.centery)

    def test_clicking_the_icon_opens_and_closes_the_panel(self):
        self.assertFalse(self.state.cart_open)
        self.assertTrue(self.cart.handle_event(_click(self.cart.icon_rect.center)))
        self.assertTrue(self.state.cart_open)
        self.assertTrue(self.cart.handle_event(_click(self.cart.icon_rect.center)))
        self.assertFalse(self.state.cart_open)

    def test_remove_decreases_quantity_and_clear_empties_the_cart(self):
        bananas = {"item_id": 9001, "item_name": "bananas"}
        milk = {"item_id": 9002, "item_name": "milk"}
        self.state.add_to_cart(bananas)
        self.state.add_to_cart(bananas)
        self.state.add_to_cart(bananas)
        self.state.add_to_cart(milk)
        self.state.toggle_cart()
        self.cart._layout_panel()

        labels = [
            f"{entry['item_name'].title()} ({entry['quantity']})"
            for entry in self.state.cart_items()
        ]
        self.assertEqual(labels, ["Bananas (3)", "Milk (1)"])

        self.cart._remove_buttons[0].on_click()
        self.assertEqual(self.state.cart[9001]["quantity"], 2)

        self.cart._layout_panel()
        self.cart.clear_button.on_click()
        self.assertEqual(self.state.cart_items(), [])

    def test_hud_and_aisle_view_draw_with_an_open_cart(self):
        self.state.current_aisle_id = "produce"
        self.state.add_to_cart({"item_id": 9001, "item_name": "bananas"})
        self.state.toggle_cart()
        surface = pygame.Surface((config.WIDTH, config.HEIGHT))

        hud = HudPlaceholders(self.state, show_clipboard=False)
        hud.draw(surface)
        self.assertTrue(hud.cart.icon_rect.collidepoint(hud.cart.icon_rect.center))

        view = AisleView(self.state)
        view.draw(surface)
        self.assertTrue(view.hud.handle_event(_click(view.hud.cart.icon_rect.center)))
        self.assertFalse(self.state.cart_open)

    def _first_shelf_item(self, view):
        for shelf in view.shelves:
            for index, item in enumerate(shelf.items):
                if item is not None:
                    return shelf, index, item
        self.fail("aisle had no products to click")

    def test_cart_panel_identifies_missing_and_incorrect_items(self):
        self.state.set_order([
            ({"item_id": 1, "item_name": "bananas"}, 2),
            ({"item_id": 2, "item_name": "milk"}, 1),
        ])
        self.state.add_to_cart({"item_id": 1, "item_name": "bananas"})
        self.state.add_to_cart({"item_id": 3, "item_name": "candy"})
        self.state.toggle_cart()
        self.cart._layout_panel()

        lines = [text for text, _color in self.cart._validation_lines()]
        self.assertFalse(any("Missing:" in t for t in lines))
        self.assertTrue(any(t.startswith("Incorrect:") and "Candy" in t for t in lines))

        surface = pygame.Surface((config.WIDTH, config.HEIGHT))
        self.cart.draw(surface)

    def test_clicking_a_product_adds_one_unit_each_time(self):
        self.state.current_aisle_id = "produce"
        view = AisleView(self.state)
        shelf, index, item = self._first_shelf_item(view)
        pos = shelf.slot_rect(index).center
        updated = dict(item)
        updated["stock_quantity"] = max(0, item["stock_quantity"] - 1)

        with patch("screens.aisle_view.decrement_stock", return_value=updated):
            view.handle_event(_click(pos))
            view.handle_event(_click(pos))
            view.handle_event(_click(pos))

        cart_item = self.state.cart_items()[0]
        self.assertEqual(cart_item["item_name"], item["item_name"])
        self.assertEqual(cart_item["quantity"], 3)
        self.assertEqual(
            f"{cart_item['item_name'].title()} ({cart_item['quantity']})",
            f"{item['item_name'].title()} (3)",
        )


if __name__ == "__main__":
    unittest.main()
