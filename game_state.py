# Owner: Arpa
# Shared game state that any screen or component can read and change.
# Should hold: the current screen, the chosen avatar, the current aisle, and settings (e.g. volume).
# Should provide: a way to change screens, choose an avatar, and select_aisle(aisle_id),
# which Ellie's aisles call when clicked (moves the avatar there and opens the aisle view).
