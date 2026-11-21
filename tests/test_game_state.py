import unittest

from game_state import AVATAR_SELECT, STORE, GameState


class GameStateOrderTests(unittest.TestCase):
    def test_start_game_starts_timer_and_selects_avatar(self):
        state = GameState()

        state.start_game()

        self.assertEqual(state.screen, AVATAR_SELECT)
        self.assertEqual(state.elapsed, 0)
        self.assertEqual(state.remaining, 60)
        state.update(2.5)
        self.assertEqual(state.elapsed, 2.5)

    def test_speed_payout_boundaries(self):
        tiers = ((10, 60), (20, 50), (30, 40), (40, 30), (50, 20), (60, 20))
        for elapsed, expected in tiers:
            with self.subTest(elapsed=elapsed):
                state = GameState()
                state.start_game()
                state.update(elapsed)
                self.assertEqual(state.speed_payout, expected)

    def test_timer_expires_freezes_and_settles_without_reset(self):
        state = GameState()
        state.start_game()
        state.set_grocery_list(["milk"])
        state.add_collected_item("milk")

        state.update(60)
        self.assertEqual(state.elapsed, 60)
        self.assertEqual(state.remaining, 0)
        self.assertTrue(state.order_expired)
        self.assertEqual(state.earnings, 25)
        state.update(10)
        self.assertEqual(state.elapsed, 60)
        self.assertEqual(state.earnings, 25)

    def test_accuracy_tip_requires_complete_list_and_no_extras(self):
        state = GameState()
        self.assertFalse(state.calculate_accuracy())
        self.assertEqual(state.tip, 0)

        state.set_grocery_list(["milk", "eggs"])
        state.add_collected_item("milk")
        self.assertFalse(state.calculate_accuracy())
        self.assertEqual(state.tip, 0)

        state.add_collected_item("eggs")
        self.assertTrue(state.calculate_accuracy())
        self.assertEqual(state.tip, 5)

        state.add_extra_item("candy")
        self.assertFalse(state.calculate_accuracy())
        self.assertEqual(state.tip, 0)
        state.remove_collected_item("candy")
        self.assertTrue(state.calculate_accuracy())

    def test_missing_and_incorrect_items_each_reduce_earnings_by_five(self):
        state = GameState()
        state.start_game()
        state.set_grocery_list(["milk", "eggs", "bread"])
        state.add_collected_item("milk")
        state.add_collected_item("candy")

        state.update(60)

        self.assertEqual(state.missing_items, {"eggs", "bread"})
        self.assertIn("candy", state.extra_items)
        self.assertEqual(state.penalty, 15)
        self.assertEqual(state.earnings, 5)

    def test_earnings_never_go_below_zero(self):
        state = GameState()
        state.start_game()
        state.set_grocery_list(["milk", "eggs", "bread", "cheese"])
        state.add_collected_item("candy")

        state.update(60)

        self.assertEqual(state.penalty, 25)
        self.assertEqual(state.earnings, 0)

    def test_play_again_preserves_avatar_resets_timer_and_generates_list(self):
        state = GameState()
        state.choose_avatar("ava")
        state.set_grocery_list(["milk", "eggs"])
        state.start_game()
        state.update(60)

        state.play_again()

        self.assertEqual(state.avatar_id, "ava")
        self.assertEqual(state.screen, STORE)
        self.assertEqual(state.elapsed, 0)
        self.assertEqual(state.remaining, 60)
        self.assertFalse(state.order_expired)
        self.assertTrue(state.required_items)

    def test_expiration_returns_to_store_for_popup(self):
        state = GameState()
        state.start_game()
        state.change_screen(STORE)

        state.update(60)

        self.assertEqual(state.screen, STORE)
        self.assertTrue(state.order_expired)

    def test_non_required_collected_item_counts_as_extra(self):
        state = GameState()
        state.set_grocery_list(["milk"])
        state.add_collected_item("milk")
        state.add_collected_item("candy")

        self.assertFalse(state.calculate_accuracy())
        self.assertIn("candy", state.extra_items)


class GameStateCartTests(unittest.TestCase):
    def _item(self, item_id, name):
        return {"item_id": item_id, "item_name": name}

    def test_add_to_cart_stacks_quantity_for_the_same_product(self):
        state = GameState()
        bananas = self._item(1, "bananas")
        state.add_to_cart(bananas)
        state.add_to_cart(bananas)
        state.add_to_cart(bananas)

        items = state.cart_items()
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]["item_name"], "bananas")
        self.assertEqual(items[0]["quantity"], 3)
        self.assertEqual(state.cart_count(), 3)

    def test_different_products_are_listed_separately(self):
        state = GameState()
        state.add_to_cart(self._item(1, "bananas"))
        state.add_to_cart(self._item(2, "milk"))
        state.add_to_cart(self._item(1, "bananas"))

        items = {entry["item_name"]: entry["quantity"] for entry in state.cart_items()}
        self.assertEqual(items, {"bananas": 2, "milk": 1})

    def test_remove_decreases_quantity_by_one(self):
        state = GameState()
        bananas = self._item(1, "bananas")
        state.add_to_cart(bananas)
        state.add_to_cart(bananas)
        state.add_to_cart(bananas)

        state.remove_from_cart(1)
        self.assertEqual(state.cart[1]["quantity"], 2)
        state.remove_from_cart(1)
        self.assertEqual(state.cart[1]["quantity"], 1)

    def test_remove_last_unit_drops_the_product(self):
        state = GameState()
        state.add_to_cart(self._item(1, "bananas"))

        removed = state.remove_from_cart(1)
        self.assertEqual(removed["quantity"], 0)
        self.assertEqual(state.cart_items(), [])
        self.assertEqual(state.cart_count(), 0)

    def test_clear_cart_removes_every_product(self):
        state = GameState()
        state.add_to_cart(self._item(1, "bananas"))
        state.add_to_cart(self._item(2, "milk"))
        state.add_to_cart(self._item(1, "bananas"))

        cleared = state.clear_cart()
        self.assertEqual(len(cleared), 2)
        self.assertEqual(state.cart_items(), [])
        self.assertEqual(state.cart_count(), 0)

    def test_cart_contents_survive_opening_and_closing(self):
        state = GameState()
        state.add_to_cart(self._item(1, "bananas"))
        state.toggle_cart()
        self.assertTrue(state.cart_open)
        state.toggle_cart()
        self.assertFalse(state.cart_open)
        self.assertEqual(state.cart_items()[0]["quantity"], 1)

    def test_cart_cleared_when_a_new_order_starts(self):
        state = GameState()
        state.add_to_cart(self._item(1, "bananas"))
        state.toggle_cart()
        state.reset_order()
        self.assertEqual(state.cart_count(), 0)
        self.assertFalse(state.cart_open)

    def test_cart_stays_in_sync_with_collected_items(self):
        state = GameState()
        state.set_grocery_list(["bananas"])
        state.add_to_cart(self._item(1, "bananas"))
        state.add_to_cart(self._item(2, "candy"))
        self.assertIn("bananas", state.collected_items)
        self.assertIn("candy", state.extra_items)

        state.remove_from_cart(2)
        self.assertNotIn("candy", state.extra_items)
        state.remove_from_cart(1)
        self.assertNotIn("bananas", state.collected_items)


if __name__ == "__main__":
    unittest.main()
