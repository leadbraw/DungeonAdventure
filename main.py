import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, get_fonts, SPRITE_PATHS
from controller.splash_screen import SplashScreen
from controller.main_screen import MainScreen
from controller.character_screen import CharacterScreen
from controller.game_controller import GameController
from controller.game_setup import GameSetup
from model.managers.sprite_manager import SpriteManager

def main():
    """Entry point for the game."""
    # Initialize pygame
    pygame.init()

    # Load fonts after pygame.init()
    fonts = get_fonts()
    font_large = fonts["large"]

    # Create the screen and set up window properties
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Dungeon Adventure")

    # Use SpriteManager to preload images
    sprite_manager = SpriteManager.get_instance()
    sprite_manager.preload_sprites({
        "hero": SPRITE_PATHS["hero"],
        "dice": SPRITE_PATHS["dice"]
    })
    hero_image = sprite_manager.get_sprite("hero")
    dungeon_icon = sprite_manager.get_sprite("dice")

    # Set window icon
    pygame.display.set_icon(dungeon_icon)

    # Initialize GameSetup
    game_setup = GameSetup()

    # Show splash screen with hero image and text
    splash_screen = SplashScreen(screen, font_large)
    splash_screen.display("TEAM 5", setup_function=game_setup.setup, image=hero_image, image_size=(256, 256))

    # Define game states
    state = "MAIN_MENU"
    selected_hero = None

    while state != "QUIT":
        if state == "MAIN_MENU":
            # Launch the main menu
            main_menu = MainScreen(screen, fonts)
            choice = main_menu.run()

            if choice == "new_game":
                state = "CHARACTER_SELECTION"
            elif choice == "load_game":
                # TODO: Implement load game logic
                print("Load game functionality is not yet implemented.")
                state = "MAIN_MENU"

        elif state == "CHARACTER_SELECTION":
            # Run character selection
            character_screen = CharacterScreen(screen, fonts)
            result = character_screen.run()

            if isinstance(result, str):
                # Hero selected and confirmed
                selected_hero = result
                state = "GAMEPLAY"

            elif result is None:
                # Player returned to main menu
                state = "MAIN_MENU"


        elif state == "GAMEPLAY":
            # Initialize and start the game
            if selected_hero:
                game_controller = GameController(screen, selected_hero)
                game_controller.set_active_adventurer(selected_hero)

                # Dungeon is already initialized when DungeonManager is instantiated
                print("[Main] Dungeon is already initialized through DungeonManager.")
                game_controller.display_game()
                state = "QUIT"  # Exit game after gameplay finishes

    # Quit pygame when the game exits
    pygame.quit()

if __name__ == "__main__":
    main()