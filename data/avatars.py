# Owner: Arpa
# The list of avatars the player can choose from — one for each person on the team.
# Each avatar has: id, name, skin, hair (color), hair_style, glasses, shirt (color).
# Everyone wears the same green apron over their shirt.
#   hair_style can be: "long", "bob", "ponytail", or "bun"
# For now avatars are drawn with simple shapes. Later, Megan's images can go in
# assets/avatars/ and be added here as an "image" field.

BLACK_HAIR = (30, 26, 28)
DARK_BROWN_HAIR = (58, 38, 28)
BROWN_HAIR = (112, 74, 44)

AVATARS = [
    {"id": "arpa", "name": "Arpa", "skin": (176, 120, 84), "hair": BLACK_HAIR,
     "hair_style": "long", "glasses": False, "shirt": (214, 92, 120)},
    {"id": "emma_r", "name": "Emma R", "skin": (192, 136, 96), "hair": DARK_BROWN_HAIR,
     "hair_style": "ponytail", "glasses": False, "shirt": (62, 150, 140)},
    {"id": "sneha", "name": "Sneha", "skin": (156, 102, 68), "hair": BLACK_HAIR,
     "hair_style": "bun", "glasses": False, "shirt": (236, 150, 60)},
    {"id": "serom", "name": "Serom", "skin": (241, 206, 172), "hair": BLACK_HAIR,
     "hair_style": "bob", "glasses": True, "shirt": (90, 130, 200)},
    {"id": "ellie", "name": "Ellie", "skin": (236, 198, 162), "hair": DARK_BROWN_HAIR,
     "hair_style": "long", "glasses": True, "shirt": (150, 110, 190)},
    {"id": "emma_d", "name": "Emma D", "skin": (244, 212, 180), "hair": BLACK_HAIR,
     "hair_style": "ponytail", "glasses": False, "shirt": (238, 200, 70)},
    {"id": "jana", "name": "Jana", "skin": (232, 192, 154), "hair": BLACK_HAIR,
     "hair_style": "long", "glasses": False, "shirt": (220, 110, 80)},
    {"id": "megan", "name": "Megan", "skin": (250, 222, 198), "hair": BROWN_HAIR,
     "hair_style": "bob", "glasses": True, "shirt": (70, 160, 200)},
]


def get_avatar(avatar_id):
    # Returns the avatar with this id, or None if there isn't one.
    for avatar in AVATARS:
        if avatar["id"] == avatar_id:
            return avatar
    return None
