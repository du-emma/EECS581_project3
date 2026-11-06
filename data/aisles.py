# Owner: Ellie
# The list of store aisles (e.g. Dairy, Produce, Powders) and where each one sits on the store map.
# Each aisle has an id (e.g. "dairy", becomes the database key in Sprint 2), a name, and a position/size.
# Coordinate with Megan so positions match the store page layout.

AISLES = [
    {"id": "baking",  "name": "Baking", "rect": (0.10, 0.22, 0.14, 0.70)},
    {"id": "produce", "name": "Produce", "rect": (0.30, 0.22, 0.14, 0.70)},
    {"id": "dairy",   "name": "Dairy & Eggs", "rect": (0.50, 0.22, 0.14, 0.70)},
]
 
def get_aisle(aisle_id):
    """Return the aisle dict with this id, or None."""
    for aisle in AISLES:
        if aisle["id"] == aisle_id:
            return aisle
    return None