import unittest
from unittest.mock import patch

from game_state import AVATAR_SELECT, STORE, GameState

MILK = {"item_id": 1, "item_name": "milk"}
EGGS = {"item_id": 2, "item_name": "eggs"}
BREAD = {"item_id": 3, "item_name": "bread"}
CHEESE = {"item_id": 4, "item_name": "cheese"}
CANDY = {"item_id": 99, "item_name": "candy"}
PRODUCTS = [MILK, EGGS, BREAD, CHEESE, {"item_id": 5, "item_name": "flour"}]


def _order(state, *pairs):
    """Give the state a fixed order: _order(state, (MILK, 2), (EGGS, 1))."""
    state.set_order(list(pairs))


class GameStateOrderTests(unittest.TestCase):
    def setUp(self):
        # Keep unit tests off the real database (no restock, fixed product list).
        for target, value in (("_restock", None), ("_available_items", PRODUCTS)):
            p = patch.object(GameState, target, return_value=value)
            p.start()
            self.addCleanup(p.stop)

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
        _order(state, (MILK, 1))
        state.add_to_cart(MILK)

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

        _order(state, (MILK, 1), (EGGS, 1))
        state.add_to_cart(MILK)
        self.assertFalse(state.calculate_accuracy())
        self.assertEqual(state.tip, 0)

        state.add_to_cart(EGGS)
        self.assertTrue(state.calculate_accuracy())
        self.assertEqual(state.tip, 5)

        state.add_to_cart(CANDY)
        self.assertFalse(state.calculate_accuracy())
        self.assertEqual(state.tip, 0)
        state.remove_from_cart(CANDY["item_id"])
        self.assertTrue(state.calculate_accuracy())

    def test_accuracy_requires_exact_quantities(self):
        state = GameState()
        _order(state, (MILK, 2))
        state.add_to_cart(MILK)
        self.assertFalse(state.calculate_accuracy())      # under
        state.add_to_cart(MILK)
        self.assertTrue(state.calculate_accuracy())       # exact
        state.add_to_cart(MILK)
        self.assertFalse(state.calculate_accuracy())      # over
        self.assertEqual(state.penalty, 5)

    def test_missing_and_incorrect_items_each_reduce_earnings_by_five(self):
        state = GameState()
        state.start_game()
        _order(state, (MILK, 1), (EGGS, 1), (BREAD, 1))
        state.add_to_cart(MILK)
        state.add_to_cart(CANDY)

        state.update(60)

        self.assertEqual(state.missing_items, {"eggs", "bread"})
        self.assertIn("candy", state.extra_items)
        self.assertEqual(state.penalty, 15)
        self.assertEqual(state.earnings, 5)

    def test_earnings_never_go_below_zero(self):
        state = GameState()
        state.start_game()
        _order(state, (MILK, 1), (EGGS, 1), (BREAD, 1), (CHEESE, 1))
        state.add_to_cart(CANDY)

        state.update(60)

        self.assertEqual(state.penalty, 25)
        self.assertEqual(state.earnings, 0)

    def test_play_again_preserves_avatar_resets_timer_and_generates_list(self):
        state = GameState()
        state.choose_avatar("ava")
        state.start_game()
        first_order_id = state.order_id
        state.update(60)

        state.play_again()

        self.assertEqual(state.avatar_id, "ava")
        self.assertEqual(state.screen, STORE)
        self.assertEqual(state.elapsed, 0)
        self.assertEqual(state.remaining, 60)
        self.assertFalse(state.order_expired)
        self.assertTrue(state.required_items)
        self.assertTrue(state.order_items)
        self.assertNotEqual(state.order_id, first_order_id)

    def test_expiration_returns_to_store_for_popup(self):
        state = GameState()
        state.start_game()
        state.change_screen(STORE)

        state.update(60)

        self.assertEqual(state.screen, STORE)
        self.assertTrue(state.order_expired)

    def test_non_required_collected_item_counts_as_extra(self):
        state = GameState()
        _order(state, (MILK, 1))
        state.add_to_cart(MILK)
        state.add_to_cart(CANDY)

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
        state.set_order([(self._item(1, "bananas"), 1)])
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