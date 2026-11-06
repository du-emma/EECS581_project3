# Owner: Ellie
# The list of store aisles (e.g. Dairy, Produce, Powders) and where each one sits on the store map.
# Each aisle has an id (e.g. "dairy", becomes the database key in Sprint 2), a name, and a position/size.
# Coordinate with Megan so positions match the store page layout.

AISLES = [
    {"id": "dairy",  "name": "Dairy & Eggs", "rect": (0.07, 0.22, 0.102, 0.583)},
    {"id": "meat", "name": "Meat", "rect": (0.27, 0.22, 0.102, 0.583)},
    {"id": "baking",   "name": "Baking", "rect": (0.47, 0.22, 0.102, 0.583)},
    {"id": "produce",  "name": "Produce", "rect": (0.67, 0.22, 0.102, 0.583)},
]
 
def get_aisle(aisle_id):
    """Return the aisle dict with this id, or None."""
    for aisle in AISLES:
        if aisle["id"] == aisle_id:
            return aisle
    return None