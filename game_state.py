# Owner: Emma, Arpa
# Shared game state that any screen or component can read and change.

import random

# Screen names — use these instead of typing the strings directly.
MENU = "menu"
INSTRUCTIONS = "instructions"
SETTINGS = "settings"
AVATAR_SELECT = "avatar_select"
STORE = "store"
AISLE = "aisle"


class GameState:
    ORDER_DURATION = 60.0

    def __init__(self):
        self.screen = MENU
        self.avatar_id = None
        self.current_aisle_id = None
        self.volume = 50  # 0–100
        self.running = True
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
        self.reset_order()
        self._order_started = True
        self.change_screen(AVATAR_SELECT)

    def play_again(self):
        """Start a fresh order while preserving the selected avatar."""
        avatar_id = self.avatar_id
        previous_items = set(self.required_items)
        self.reset_order()
        self.avatar_id = avatar_id
        self.generate_grocery_list(previous_items)
        self._order_started = True
        self.change_screen(STORE)

    def generate_grocery_list(self, previous_items=None):
        """Generate a new randomized shopping list for the next order."""
        available_items = (
            "milk", "eggs", "bread", "cheese", "chicken",
            "beef", "apples", "lettuce", "flour", "sugar",
        )
        previous_items = set(previous_items or ())
        item_count = random.randint(3, 5)

        for _ in range(20):
            items = set(random.sample(available_items, item_count))
            if items != previous_items:
                break
        self.set_grocery_list(items)

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

    def set_grocery_list(self, items):
        self.required_items = set(items)
        self.clear_collected_items()

    def add_collected_item(self, item):
        if item in self.required_items:
            self.extra_items.discard(item)
            self.collected_items.add(item)
        else:
            self.add_extra_item(item)

    def remove_collected_item(self, item):
        self.collected_items.discard(item)
        self.extra_items.discard(item)

    def add_extra_item(self, item):
        self.extra_items.add(item)

    def clear_collected_items(self):
        self.collected_items.clear()
        self.extra_items.clear()

    def calculate_accuracy(self):
        return bool(self.required_items) and (
            self.collected_items == self.required_items and not self.extra_items
        )

    @property
    def tip(self):
        return 5 if self.calculate_accuracy() else 0

    @property
    def missing_items(self):
        return self.required_items - self.collected_items

    @property
    def penalty(self):
        incorrect_item_count = len(self.missing_items) + len(self.extra_items)
        return incorrect_item_count * 5

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
        self.required_items = set()
        self.collected_items = set()
        self.extra_items = set()
        self._elapsed = 0.0
        self._order_started = False
        self._order_expired = False
        self._order_settled = False
        self.settled_earnings = None

    def quit(self):
        self.running = False
