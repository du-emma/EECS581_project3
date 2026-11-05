# Owner: Arpa
# Shared game state that any screen or component can read and change.
# Should hold: the current screen, the chosen avatar, the current aisle, and settings (e.g. volume).
# Should provide: a way to change screens, choose an avatar, and select_aisle(aisle_id),
# which Ellie's aisles call when clicked (moves the avatar there and opens the aisle view).

# Screen names — use these instead of typing the strings directly.
MENU = "menu"
INSTRUCTIONS = "instructions"
SETTINGS = "settings"
AVATAR_SELECT = "avatar_select"
STORE = "store"
AISLE = "aisle"


class GameState:
    def __init__(self):
        self.screen = MENU
        self.avatar_id = None
        self.current_aisle_id = None
        self.volume = 50  # 0–100
        self.running = True

    def change_screen(self, screen_name):
        self.screen = screen_name

    def choose_avatar(self, avatar_id):
        self.avatar_id = avatar_id

    def select_aisle(self, aisle_id):
        # Moves the avatar to the clicked aisle and opens the aisle view.
        self.current_aisle_id = aisle_id
        self.change_screen(AISLE)

    def quit(self):
        self.running = False
