# Owner: Arpa
# The list of avatars the player can choose from — one for each person on the team.
# Each avatar has: id, name, skin, hair (color), hair_style, glasses.
# Everyone wears the same green cap + apron uniform (colors are in components/avatar.py).
#   hair_style can be: "long", "bob", "ponytail", or "bun"
# For now avatars are drawn with simple shapes. Later, Megan's images can go in
# assets/avatars/ and be added here as an "image" field.

BLACK_HAIR = (30, 26, 28)
DARK_BROWN_HAIR = (58, 38, 28)
BROWN_HAIR = (112, 74, 44)

AVATARS = [
    {"id": "arpa", "name": "Arpa", "skin": (176, 120, 84), "hair": BLACK_HAIR,
     "hair_style": "long", "glasses": False},
    {"id": "emma_r", "name": "Emma R", "skin": (192, 136, 96), "hair": DARK_BROWN_HAIR,
     "hair_style": "ponytail", "glasses": False},
    {"id": "sneha", "name": "Sneha", "skin": (156, 102, 68), "hair": BLACK_HAIR,
     "hair_style": "bun", "glasses": False},
    {"id": "serom", "name": "Serom", "skin": (241, 206, 172), "hair": BLACK_HAIR,
     "hair_style": "bob", "glasses": True},
    {"id": "ellie", "name": "Ellie", "skin": (236, 198, 162), "hair": DARK_BROWN_HAIR,
     "hair_style": "long", "glasses": True},
    {"id": "emma_d", "name": "Emma D", "skin": (244, 212, 180), "hair": BLACK_HAIR,
     "hair_style": "ponytail", "glasses": False},
    {"id": "jana", "name": "Jana", "skin": (232, 192, 154), "hair": BLACK_HAIR,
     "hair_style": "long", "glasses": False},
    {"id": "megan", "name": "Megan", "skin": (250, 222, 198), "hair": BROWN_HAIR,
     "hair_style": "bob", "glasses": True},
]


def get_avatar(avatar_id):
    # Returns the avatar with this id, or None if there isn't one.
    for avatar in AVATARS:
        if avatar["id"] == avatar_id:
            return avatar
    return None
