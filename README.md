# Grocery Rush

A shopping and delivery game: navigate a grocery store, collect the items on a customer's list, and deliver them before time runs out.

## Running the game

```
cd client
npm install
npm run dev
```

Then open the URL Vite prints (usually http://localhost:5173).

## Sprint 1 ownership

| Person | Files |
|---|---|
| Arpa | `App.tsx`, `state/GameContext.tsx`, `data/avatars.ts`, `screens/MainMenu.tsx`, `Instructions.tsx`, `Settings.tsx`, `AvatarSelect.tsx`, `components/Avatar.tsx` |
| Megan | `public/assets/`, `styles/global.css`, `screens/StorePage.tsx`, `components/Button.tsx`, `components/store/HudPlaceholders.tsx` |
| Ellie | `data/aisles.ts`, `screens/AisleView.tsx`, `components/store/StoreMap.tsx`, `components/store/Aisle.tsx`, `components/aisle/Shelf.tsx` |
| Serom | `docs/` |

`types.ts` is shared — agree on changes as a team.

## Screen flow

Main menu → Avatar select → Store page → click an aisle → Aisle view (empty shelves) → back to store

Each file has a comment at the top describing what goes in it and who owns it.

## Workflow

Make a branch for your work (e.g. `git checkout -b ellie-aisles`), push it, and open a pull request into `main`.
