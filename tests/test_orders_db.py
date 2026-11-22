# Integration tests: R9/R10 against the real SQLite schema and seed data
# (using a temporary copy of the database, never data/grocery.db).
# Run from the project root:  python -m unittest discover -s tests -t .

import os
import tempfile
import unittest
from pathlib import Path

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")

from data import db, items
from game_state import GameState
from components.checklist import checklist_rows


class RealDbTestCase(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self._orig_path = db.DB_PATH
        db.DB_PATH = Path(self._tmp.name) / "test.db"
        self.state = GameState()

    def tearDown(self):
        db.DB_PATH = self._orig_path
        self._tmp.cleanup()

    def by_id(self):
        return {r["item_id"]: r for r in items.get_all_items()}


class TestOrdersAgainstDb(RealDbTestCase):
    def test_every_ordered_item_exists_with_valid_quantity(self):
        catalog = self.by_id()
        for _ in range(100):
            self.state.start_game()
            self.assertGreaterEqual(len(self.state.order_items), 3)
            for o in self.state.order_items:
                row = catalog[o["item_id"]]
                self.assertEqual(row["item_name"], o["item_name"])
                self.assertGreaterEqual(o["required_quantity"], 1)
                self.assertLessEqual(o["required_quantity"], row["stock_quantity"])

    def test_new_session_restocks_drained_shelves(self):
        for row in items.get_all_items():
            db.execute("UPDATE items SET stock_quantity = 0 WHERE item_id = ?",
                       (row["item_id"],))
        self.state.start_game()
        catalog = self.by_id()
        self.assertTrue(all(r["stock_quantity"] > 0 for r in catalog.values()))
        self.assertGreaterEqual(len(self.state.order_items), 3)

    def test_full_shopping_flow(self):
        self.state.start_game()
        catalog = self.by_id()
        for o in self.state.order_items:                     # shop like aisle_view does
            for _ in range(o["required_quantity"]):
                items.decrement_stock(o["item_id"])
                self.state.add_to_cart(catalog[o["item_id"]])
        rows = checklist_rows(self.state)
        self.assertTrue(all(r["complete"] for r in rows))
        self.assertTrue(self.state.calculate_accuracy())
        self.assertEqual(self.state.penalty, 0)

        first = self.state.order_items[0]                    # remove one, like the cart panel
        self.state.remove_from_cart(first["item_id"])
        items.increment_stock(first["item_id"], 1)
        row = next(r for r in checklist_rows(self.state) if r["item_id"] == first["item_id"])
        self.assertEqual(row["collected"], first["required_quantity"] - 1)
        self.assertFalse(row["complete"])


if __name__ == "__main__":
    unittest.main()