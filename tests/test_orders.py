# Tests for R9 (order generation) and R10 (checklist progress).
# Run from the project root:  python -m unittest discover -s tests -t .

import os
import unittest

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")

import game_state
from game_state import GameState
from components.checklist import checklist_rows, checklist_summary

PRODUCTS = [{"item_id": i, "item_name": n} for i, n in enumerate(
    ["milk", "eggs", "apples", "flour", "cheese", "sugar", "carrots", "beef"], start=1)]
DB_IDS = {p["item_id"] for p in PRODUCTS}


class OrderTestCase(unittest.TestCase):
    def setUp(self):
        self._orig = GameState._available_items
        self._orig_restock = GameState._restock
        GameState._available_items = staticmethod(lambda: list(PRODUCTS))
        GameState._restock = staticmethod(lambda: None)
        self.state = GameState()

    def tearDown(self):
        GameState._available_items = staticmethod(self._orig)
        GameState._restock = staticmethod(self._orig_restock)

    def product(self, item_id):
        return next(p for p in PRODUCTS if p["item_id"] == item_id)


class TestR9(OrderTestCase):
    def test_new_session_generates_order(self):
        self.state.start_game()
        self.assertIsNotNone(self.state.order_id)
        self.assertTrue(self.state.order_items)

    def test_multiple_items_valid_ids_positive_int_quantities(self):
        for _ in range(200):
            self.state.start_game()
            items = self.state.order_items
            self.assertGreaterEqual(len(items), game_state.MIN_ORDER_ITEMS)
            ids = [o["item_id"] for o in items]
            self.assertEqual(len(ids), len(set(ids)))        # no duplicate rows
            for o in items:
                self.assertIn(o["item_id"], DB_IDS)
                self.assertIsInstance(o["required_quantity"], int)
                self.assertGreater(o["required_quantity"], 0)
                self.assertEqual(o["order_id"], self.state.order_id)

    def test_orders_vary_across_sessions(self):
        sigs = set()
        for _ in range(30):
            self.state.start_game()
            sigs.add(self.state.order_signature())
        self.assertGreater(len(sigs), 5)

    def test_play_again_changes_order_and_keeps_avatar(self):
        self.state.start_game()
        self.state.choose_avatar("a2")
        for _ in range(50):
            before = self.state.order_signature()
            self.state.play_again()
            self.assertNotEqual(before, self.state.order_signature())
            self.assertEqual(self.state.avatar_id, "a2")

    def test_order_stable_while_shopping(self):
        self.state.start_game()
        self.state.change_screen(game_state.STORE)
        snapshot = [dict(o) for o in self.state.order_items]
        self.state.select_aisle(2)
        self.state.add_to_cart(PRODUCTS[0])
        self.state.update(1.0)
        self.state.change_screen(game_state.STORE)
        self.state.select_aisle(3)
        self.state.remove_from_cart(PRODUCTS[0]["item_id"])
        self.state.toggle_cart()
        self.assertEqual(snapshot, self.state.order_items)


class TestStock(OrderTestCase):
    def test_orders_respect_stock(self):
        stocked = [
            {"item_id": 1, "item_name": "milk", "stock_quantity": 0},
            {"item_id": 2, "item_name": "eggs", "stock_quantity": 1},
            {"item_id": 3, "item_name": "apples", "stock_quantity": 2},
            {"item_id": 4, "item_name": "flour", "stock_quantity": 10},
            {"item_id": 5, "item_name": "sugar", "stock_quantity": 10},
            {"item_id": 6, "item_name": "beef", "stock_quantity": 10},
        ]
        GameState._available_items = staticmethod(lambda: list(stocked))
        limits = {p["item_id"]: p["stock_quantity"] for p in stocked}
        for _ in range(200):
            self.state.start_game()
            for o in self.state.order_items:
                self.assertNotEqual(o["item_id"], 1)           # out of stock
                self.assertLessEqual(o["required_quantity"], limits[o["item_id"]])


class TestR10(OrderTestCase):
    def setUp(self):
        super().setUp()
        self.state.set_order([
            (self.product(1), 2), (self.product(2), 1),
            (self.product(3), 3), (self.product(4), 1),
        ])

    def row(self, item_id):
        return next(r for r in checklist_rows(self.state) if r["item_id"] == item_id)

    def test_rows_show_required_and_collected(self):
        rows = checklist_rows(self.state)
        self.assertEqual([r["required"] for r in rows], [2, 1, 3, 1])
        self.assertTrue(all(r["collected"] == 0 and not r["complete"] for r in rows))

    def test_progress_below_then_exactly_at_required(self):
        milk = self.product(1)
        self.state.add_to_cart(milk)
        self.assertEqual((self.row(1)["collected"], self.row(1)["complete"]), (1, False))
        self.state.add_to_cart(milk)
        self.assertEqual((self.row(1)["collected"], self.row(1)["complete"]), (2, True))

    def test_removing_reverts_completion(self):
        eggs = self.product(2)
        self.state.add_to_cart(eggs)
        self.assertTrue(self.row(2)["complete"])
        self.state.remove_from_cart(2)
        self.assertEqual((self.row(2)["collected"], self.row(2)["complete"]), (0, False))

    def test_checklist_matches_cart(self):
        for pid in (1, 1, 3, 5):
            self.state.add_to_cart(self.product(pid))
        self.state.remove_from_cart(1)
        for r in checklist_rows(self.state):
            self.assertEqual(r["collected"], self.state.collected_quantity(r["item_id"]))
        self.assertEqual(self.state.collected_quantity(1), 1)

    def test_summary(self):
        self.assertEqual(checklist_summary(self.state), "0 of 4 items complete")
        self.state.add_to_cart(self.product(2))
        self.state.add_to_cart(self.product(4))
        self.assertEqual(checklist_summary(self.state), "2 of 4 items complete")

    def test_scoring_still_works(self):
        for pid, n in ((1, 2), (2, 1), (3, 3), (4, 1)):
            for _ in range(n):
                self.state.add_to_cart(self.product(pid))
        self.assertTrue(self.state.calculate_accuracy())
        self.assertEqual(self.state.penalty, 0)
        self.state.add_to_cart(self.product(5))          # off-list item
        self.assertFalse(self.state.calculate_accuracy())
        self.assertEqual(self.state.penalty, 5)


class TestDraw(unittest.TestCase):
    def test_checklist_draws(self):
        import pygame
        from components.checklist import Checklist
        pygame.init()
        surf = pygame.display.set_mode((400, 400))
        orig, orig_r = GameState._available_items, GameState._restock
        GameState._available_items = staticmethod(lambda: list(PRODUCTS))
        GameState._restock = staticmethod(lambda: None)
        try:
            st = GameState(); st.start_game()
            st.add_to_cart(PRODUCTS[0])
            Checklist().draw(surf, st, (10, 10))
            import pygame as pg
            Checklist().draw_in_rect(surf, st, pg.Rect(200, 10, 180, 250))
        finally:
            GameState._available_items = staticmethod(orig)
            GameState._restock = staticmethod(orig_r)


if __name__ == "__main__":
    unittest.main()