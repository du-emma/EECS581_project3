# Owner: Ellie, Emma
# Store-map aisle layout + names/items loaded from the SQLite database.
# Coordinate with Megan so positions match the store page layout.

from data import items as items_db

# Fractional window positions for the store map (x, y, w, h).
_AISLE_LAYOUT = {
    "dairy":   (0.07, 0.22, 0.102, 0.583),
    "meat":    (0.27, 0.22, 0.102, 0.583),
    "baking":  (0.47, 0.22, 0.102, 0.583),
    "produce": (0.67, 0.22, 0.102, 0.583),
}


def load_aisles():
    """Combine DB aisle names with the fixed map layout."""
    aisles = []
    for row in items_db.get_all_aisles():
        aisle_id = row["aisle_id"]
        rect = _AISLE_LAYOUT.get(aisle_id)
        if rect is None:
            continue
        aisles.append({"id": aisle_id, "name": row["aisle_name"], "rect": rect})
    return aisles


AISLES = load_aisles()


def get_aisle(aisle_id):
    """Return the aisle dict with this id, or None."""
    for aisle in AISLES:
        if aisle["id"] == aisle_id:
            return aisle
    return None


def get_aisle_items(aisle_id):
    """Return item records for this aisle from the database."""
    return items_db.get_items_by_aisle(aisle_id)
