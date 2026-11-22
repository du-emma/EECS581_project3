# Owner: Emma, Arpa
# Shared game state that any screen or component can read and change.

import itertools
import random

# Screen names — use these instead of typing the strings directly.
MENU = "menu"
INSTRUCTIONS = "instructions"
SETTINGS = "settings"
AVATAR_SELECT = "avatar_select"
STORE = "store"
AISLE = "aisle"

# R9 order generation settings
MIN_ORDER_ITEMS = 3      # distinct products per order (acceptance: "multiple items")
MAX_ORDER_ITEMS = 5
QUANTITY_CHOICES = (1, 2, 3)
QUANTITY_WEIGHTS = (5, 3, 2)   # small quantities are more common

_order_ids = itertools.count(1)


class GameState:
    ORDER_DURATION = 60.0

    def __init__(self):
        self.screen = MENU
        self.avatar_id = None
        self.current_aisle_id = None
        self.volume = 50  # 0–100
        self.running = True
        self.cart_open = False
        self.reset_order()

    def change_screen(self, screen_name):
        self.screen = screen_name

    def choose_avatar(self, avatar_id):
        self.avatar_id = avatar_id

    def select_aisle(self, aisle_id):
        # Moves the avatar to the clicked aisle and opens the aisle view.
        self.current_aisle_id = aisle_id
        self.change_screen(AISLE)

    def start_game(self):
        # A new shopping session: build a fresh order, then it stays fixed.
        self.reset_order()
        self._restock()
        self.generate_order()
        self._order_started = True
        self.change_screen(AVATAR_SELECT)

    def play_again(self):
        """Start a fresh order while preserving the selected avatar."""
        avatar_id = self.avatar_id
        previous = self.order_signature()
        self.reset_order()
        self.avatar_id = avatar_id
        self._restock()
        self.generate_order(previous)
        self._order_started = True
        self.change_screen(STORE)

    # ----- R9: randomized order generation -----

    def generate_order(self, previous_signature=None):
        """Pick random products from the database with positive quantities.

        Called once per session (start_game / play_again). Nothing else
        regenerates the order, so it cannot change while the player shops.
        Tries to avoid repeating the previous order exactly.
        """
        pool = self._available_items()
        # Only order things the player can actually pick up (stock > 0).
        in_stock = [p for p in pool if (p.get("stock_quantity") is None
                                        or p["stock_quantity"] > 0)]
        pool = in_stock or pool
        count = min(random.randint(MIN_ORDER_ITEMS, MAX_ORDER_ITEMS), len(pool))

        def roll():
            picks = random.sample(pool, count)
            return [(p, self._roll_quantity(p)) for p in picks]

        rolled = roll()
        for _ in range(19):
            sig = frozenset((p["item_id"], q) for p, q in rolled)
            if sig != previous_signature:
                break
            rolled = roll()
        self.set_order(rolled)

    @staticmethod
    def _restock():
        """Refill shelf stock so every new order can be completed."""
        try:
            from data.items import restock_all

            restock_all()
        except Exception:
            pass

    @staticmethod
    def _roll_quantity(product):
        """Positive quantity, never more than the shelf stock."""
        stock = product.get("stock_quantity")
        cap = max(QUANTITY_CHOICES) if stock is None else min(stock, max(QUANTITY_CHOICES))
        pairs = [(q, w) for q, w in zip(QUANTITY_CHOICES, QUANTITY_WEIGHTS) if q <= cap]
        if not pairs:
            return 1
        return random.choices([q for q, _ in pairs], [w for _, w in pairs])[0]

    def set_order(self, rolled):
        """rolled: iterable of ({"item_id", "item_name"}, required_quantity)."""
        self.order_id = next(_order_ids)
        self.order_items = [
            {
                "order_id": self.order_id,
                "item_id": product["item_id"],
                "item_name": product["item_name"],
                "required_quantity": int(quantity),
            }
            for product, quantity in rolled
        ]
        self.clear_cart()

    def order_signature(self):
        return frozenset(
            (o["item_id"], o["required_quantity"]) for o in self.order_items
        )

    @staticmethod
    def _available_items():
        """Products from the store database as [{"item_id", "item_name"}].

        Falls back to a small hardcoded list only if the database can't be
        read, so the game doesn't crash (those ids won't match real shelves).
        """
        try:
            from data.items import get_all_items

            items = []
            for row in get_all_items():
                row = dict(row)
                items.append({
                    "item_id": row["item_id"],
                    "item_name": row["item_name"],
                    "stock_quantity": row.get("stock_quantity"),
                })
            if items:
                return items
        except Exception:
            pass
        fallback = (
            "milk", "eggs", "cheese", "chicken", "beef",
            "apples", "lettuce", "flour", "sugar", "carrots",
        )
        return [{"item_id": n, "item_name": n} for n in fallback]

    # ----- R10: checklist progress (derived from the cart) -----

    def collected_quantity(self, item_id):
        entry = self.cart.get(item_id)
        return entry["quantity"] if entry else 0

    def order_progress(self):
        """One dict per ordered item: required/collected quantity + complete flag."""
        rows = []
        for o in self.order_items:
            collected = self.collected_quantity(o["item_id"])
            rows.append({
                **o,
                "collected_quantity": collected,
                "complete": collected >= o["required_quantity"],
            })
        return rows

    def completed_count(self):
        return sum(1 for row in self.order_progress() if row["complete"])

    def update(self, dt):
        if not self._order_started or self._order_settled:
            return

        self._elapsed = min(self._elapsed + max(0.0, dt), self.ORDER_DURATION)
        if self._elapsed >= self.ORDER_DURATION:
            self._order_expired = True
            self.settle_order()
            self.change_screen(STORE)

    @property
    def elapsed(self):
        return self._elapsed

    @property
    def remaining(self):
        return max(0.0, self.ORDER_DURATION - self._elapsed)

    @property
    def order_expired(self):
        return self._order_expired

    @property
    def is_expired(self):
        return self._order_expired

    @property
    def speed_payout(self):
        if self.elapsed <= 10:
            return 60
        if self.elapsed <= 20:
            return 50
        if self.elapsed <= 30:
            return 40
        if self.elapsed <= 40:
            return 30
        return 20

    # Name-set views kept for screens/HUD code written against the old API.
    @property
    def required_items(self):
        return {o["item_name"] for o in self.order_items}

    @property
    def collected_items(self):
        ordered = {o["item_id"] for o in self.order_items}
        return {e["item_name"] for i, e in self.cart.items() if i in ordered}

    @property
    def extra_items(self):
        ordered = {o["item_id"] for o in self.order_items}
        return {e["item_name"] for i, e in self.cart.items() if i not in ordered}

    @property
    def incorrect_items(self):
        """Names of off-list cart items and over-collected order items."""
        return {entry["item_name"] for entry in self.validate_cart()["incorrect"]}

    def add_to_cart(self, item):
        """Add one unit of a shelf item. Stacks quantity for the same product."""
        item_id = item["item_id"]
        name = item["item_name"]
        if item_id in self.cart:
            self.cart[item_id]["quantity"] += 1
        else:
            self.cart[item_id] = {
                "item_id": item_id,
                "item_name": name,
                "quantity": 1,
            }
        return self.cart[item_id]

    def remove_from_cart(self, item_id):
        """Remove one unit. Drops the product when its quantity hits zero."""
        entry = self.cart.get(item_id)
        if entry is None:
            return None
        entry["quantity"] -= 1
        snapshot = dict(entry)
        if entry["quantity"] <= 0:
            del self.cart[item_id]
            snapshot["quantity"] = 0
        return snapshot

    def clear_cart(self):
        """Remove every product from the cart. Returns the entries that were cleared."""
        removed = [dict(entry) for entry in self.cart.values()]
        self.cart.clear()
        return removed

    def cart_items(self):
        return list(self.cart.values())

    def cart_count(self):
        return sum(entry["quantity"] for entry in self.cart.values())

    def toggle_cart(self):
        self.cart_open = not self.cart_open

    def close_cart(self):
        self.cart_open = False

    def validate_cart(self):
        """Compare the cart to the order and list missing vs incorrect items.

        Missing: ordered products the cart is short on (including qty 0).
        Incorrect: off-list products, or extra units beyond what the order asked for.
        """
        ordered = {o["item_id"]: o for o in self.order_items}
        missing = []
        for o in self.order_items:
            collected = self.collected_quantity(o["item_id"])
            required = o["required_quantity"]
            if collected < required:
                missing.append({
                    "item_id": o["item_id"],
                    "item_name": o["item_name"],
                    "required": required,
                    "collected": collected,
                    "shortfall": required - collected,
                })

        incorrect = []
        for item_id, entry in self.cart.items():
            required = ordered[item_id]["required_quantity"] if item_id in ordered else 0
            extra = entry["quantity"] - required
            if extra > 0:
                incorrect.append({
                    "item_id": item_id,
                    "item_name": entry["item_name"],
                    "quantity": entry["quantity"],
                    "extra": extra,
                    "on_order": item_id in ordered,
                })

        return {
            "matches": bool(self.order_items) and not missing and not incorrect,
            "missing": missing,
            "incorrect": incorrect,
        }

    def calculate_accuracy(self):
        """True when the cart matches the order exactly (no missing, no extra)."""
        return self.validate_cart()["matches"]

    @property
    def tip(self):
        return 5 if self.calculate_accuracy() else 0

    @property
    def missing_units(self):
        return sum(
            max(0, r["required_quantity"] - r["collected_quantity"])
            for r in self.order_progress()
        )

    @property
    def extra_units(self):
        """Units in the cart beyond the order (off-list items or over-collecting)."""
        ordered = {o["item_id"]: o["required_quantity"] for o in self.order_items}
        return sum(
            max(0, e["quantity"] - ordered.get(i, 0)) for i, e in self.cart.items()
        )

    @property
    def wrong_unit_count(self):
        return self.missing_units + self.extra_units

    @property
    def missing_items(self):
        return {r["item_name"] for r in self.order_progress() if not r["complete"]}

    @property
    def penalty(self):
        return self.wrong_unit_count * 5

    @property
    def earnings(self):
        if self._order_settled:
            return self.settled_earnings
        return max(0, self.speed_payout + self.tip - self.penalty)

    def settle_order(self):
        if not self._order_settled:
            self.settled_earnings = max(
                0, self.speed_payout + self.tip - self.penalty
            )
            self._order_settled = True
        return self.settled_earnings

    def reset_order(self):
        self.order_id = None
        self.order_items = []
        self.cart = {}
        self.cart_open = False
        self._elapsed = 0.0
        self._order_started = False
        self._order_expired = False
        self._order_settled = False
        self.settled_earnings = None

    def quit(self):
        self.running = False