# Owner: Arpa
# The list of avatars the player can choose from (id, name, colors).
# For now avatars are drawn with simple shapes. Later, Megan's images can go in
# assets/avatars/ and be added here as an "image" field.

AVATARS = [
    {"id": "green", "name": "Gus", "shirt": (52, 140, 82), "skin": (241, 194, 150)},
    {"id": "blue", "name": "Bea", "shirt": (58, 110, 190), "skin": (198, 134, 90)},
    {"id": "red", "name": "Rae", "shirt": (200, 70, 60), "skin": (255, 219, 172)},
    {"id": "purple", "name": "Pip", "shirt": (130, 80, 170), "skin": (141, 85, 36)},
]


def get_avatar(avatar_id):
    # Returns the avatar with this id, or None if there isn't one.
    for avatar in AVATARS:
        if avatar["id"] == avatar_id:
            return avatar
    return None
