import pygame
import os

# Colors
RED = (255, 0, 0)
PASTEL_RED = (250, 145, 147)
DARK_RED = (139, 0, 0)

BLACK = (0, 0, 0)
GOLD = (255, 165, 0)
BROWN = (210, 105, 30)
WHITE = (255, 255, 255)

VIOLET = (238, 130, 238)
DARK_VIOLET = (199, 21, 133)

BACKGROUND_COLOR = (24, 24, 24)
DARK_GREY = (60, 60, 60)
MEDIUM_GREY = (80, 80, 80)
FADED_GRAY = (169, 169, 169)
OFF_WHITE = (226, 226, 226)

LIGHT_BLUE = (85, 176, 230)
FADED_BLUE = (100, 149, 237)

# Screen Dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Pillar Names (used in game_controller)
PILLAR_NAMES = [
    "Pillar of Abstraction",
    "Pillar of Polymorphism",
    "Pillar of Inheritance",
    "Pillar of Encapsulation"
]

# Button Sizes
MENU_BUTTON_WIDTH = 140
MENU_BUTTON_HEIGHT = 40


# Fonts (initialize after pygame.init())
def get_fonts():
    """Returns a dictionary of fonts."""
    return {
        "large": pygame.font.Font(None, 85),
        "small": pygame.font.Font(None, 30),
        "medium": pygame.font.Font(None, 50),
        "extra_small": pygame.font.Font(None, 25)
    }


# Sprite Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "assets", "images")

SPRITE_PATHS = {
    # dungeon sprites, will rotate
    "dungeon_one": os.path.join(ASSETS_DIR, "dungeon_one.png"),
    "dungeon_two": os.path.join(ASSETS_DIR, "dungeon_two.png"),
    "dungeon_two_op_a": os.path.join(ASSETS_DIR, "dungeon_two_op_a.png"),
    "dungeon_two_op_b": os.path.join(ASSETS_DIR, "dungeon_two_op_b.png"),
    "dungeon_three": os.path.join(ASSETS_DIR, "dungeon_three.png"),
    "dungeon_four": os.path.join(ASSETS_DIR, "dungeon_four.png"),

    # enemy sprites, may flip
    "gremlin_one": os.path.join(ASSETS_DIR, "gremlin_one.png"),
    "gremlin_two": os.path.join(ASSETS_DIR, "gremlin_two.png"),
    "ogre_one": os.path.join(ASSETS_DIR, "ogre_one.png"),
    "ogre_two": os.path.join(ASSETS_DIR, "ogre_two.png"),
    "skeleton_one": os.path.join(ASSETS_DIR, "skeleton_one.png"),
    "skeleton_two": os.path.join(ASSETS_DIR, "skeleton_two.png"),
    "tom": os.path.join(ASSETS_DIR, "tom.png"),

    # STATIC IMAGES
    # character and portraits sprites
    "jayne": os.path.join(ASSETS_DIR, "jayne.png"),
    "jayne_portrait": os.path.join(ASSETS_DIR, "jayne_portrait.png"),
    "mark": os.path.join(ASSETS_DIR, "mark.png"),
    "mark_portrait": os.path.join(ASSETS_DIR, "mark_portrait.png"),
    "noah": os.path.join(ASSETS_DIR, "noah.png"),
    "noah_portrait": os.path.join(ASSETS_DIR, "noah_portrait.png"),
    "sean": os.path.join(ASSETS_DIR, "sean.png"),
    "sean_portrait": os.path.join(ASSETS_DIR, "sean_portrait.png"),

    # default backups sprites
    "dice": os.path.join(ASSETS_DIR, "dice.png"),
    "hero": os.path.join(ASSETS_DIR, "hero.png"),

    # item sprites
    "abstraction_pillar": os.path.join(ASSETS_DIR, "abstraction_pillar.png"),
    "code_spike": os.path.join(ASSETS_DIR, "code_spike.png"),
    "encapsulation_pillar": os.path.join(ASSETS_DIR, "encapsulation_pillar.png"),
    "energy_drink": os.path.join(ASSETS_DIR, "energy_drink.png"),
    "inheritance_pillar": os.path.join(ASSETS_DIR, "inheritance_pillar.png"),
    "polymorphism_pillar": os.path.join(ASSETS_DIR, "polymorphism_pillar.png"),
    "white_box": os.path.join(ASSETS_DIR, "white_box.png"),
}

# Probabilities for room types
ENTITY_CHANCE = 0.4
EVENT_CHANCE = 0.4
EMPTY_CHANCE = 0.2

MONSTER_CHANCE = 0.8
ELITE_CHANCE = 0.2
TRAP_CHANCE = 0.5
ITEM_CHANCE = 0.5

# For position marker on minimap
MAP_CELL_WIDTH = 19

# For constructing minimap surface
MAP_SURFACE_TILE_SIZE = 64
