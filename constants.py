import pygame

# Colors
DARK_GREY = (60, 60, 60)
PASTEL_RED = (250, 145, 147)
LIGHT_BLUE = (85, 176, 230)
OFF_WHITE = (226, 226, 226)
BACKGROUND_COLOR = (24, 24, 24)

# Screen Dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Pillar Names (used in game_controller)
PILLAR_NAMES = ["Pillar of Abstraction", "Pillar of Polymorphism", "Pillar of Inheritance", "Pillar of Encapsulation"]

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
    }