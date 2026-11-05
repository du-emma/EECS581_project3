# Grocery Rush

A shopping and delivery game: navigate a grocery store, collect the items on a customer's list, and deliver them before time runs out. Built with Python and pygame.

## Running the game

```
pip install -r requirements.txt
python main.py
```

## Sprint 1 ownership

| Person | Files |
|---|---|
| Arpa | `main.py`, `game_state.py`, `data/avatars.py`, `screens/base_screen.py`, `main_menu.py`, `instructions.py`, `settings_screen.py`, `avatar_select.py`, `components/avatar.py` |
| Megan | `assets/`, `screens/store_page.py`, `components/button.py`, `components/hud_placeholders.py` |
| Ellie | `data/aisles.py`, `screens/aisle_view.py`, `components/store_map.py`, `components/aisle.py`, `components/shelf.py` |
| Serom | `docs/` |

`config.py` is shared — agree on changes as a team.

## Folders

- `screens/` — full pages (main menu, store page, aisle view, ...)
- `components/` — smaller pieces drawn inside screens (buttons, aisles, avatar, ...)
- `data/` — lists of avatars and aisles
- `assets/` — images and fonts

## Screen flow

Main menu → Avatar select → Store page → click an aisle → Aisle view (empty shelves) → back to store

Each file has a comment at the top describing what goes in it and who owns it.

## Workflow

Make a branch for your work (e.g. `git checkout -b ellie-aisles`), push it, and open a pull request into `main`.
