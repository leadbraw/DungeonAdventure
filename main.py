import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, get_fonts, SPRITE_PATHS
from view.splash_screen import SplashScreen
from view.main_screen import MainScreen
from view.character_screen import CharacterScreen
from controller.game_controller import GameController
from controller.game_setup import GameSetup
from model.managers.sprite_manager import SpriteManager
from model.managers.game_state_manager import GameStateManager

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
        "dice": SPRITE_PATHS["dice"]
    })
    dungeon_icon = sprite_manager.get_sprite("dice")

    # Set window icon
    pygame.display.set_icon(dungeon_icon)

    # Initialize GameSetup
    game_setup = GameSetup()

    # Show splash screen with hero image and text
    splash_screen = SplashScreen(screen, font_large)
    splash_screen.display("TEAM 5", setup_function=game_setup.setup)

    # Define game states
    state = "MAIN_MENU"
    selected_hero = None
    game_controller = None

    while state != "QUIT":
        if state == "MAIN_MENU":
            # Launch the main menu
            main_menu = MainScreen(screen, fonts)
            choice = main_menu.run()

            if choice == "new_game":
                state = "CHARACTER_SELECTION"
            elif choice == "load_game":
                game_controller = GameStateManager.load_game_state()
                # might cause a bug due to surface variables
                game_controller.screen = screen
                state = "GAMEPLAY"

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
                # if game_controller:
                # TODO uncomment if statement above once load is implemented
                game_controller = GameController(screen, selected_hero)
                game_controller.set_active_adventurer(selected_hero)

                # TODO: implement a save button and call the line below
                # GameStateManager.save_game_state(game_controller)

                # Dungeon is already initialized when DungeonManager is instantiated
                print("[Main] Dungeon is already initialized through DungeonManager.")
                if game_controller.display_game() == 1: # If it returns a value, means user has died and chose to replay
                    state = "MAIN_MENU"
                else:
                    state = "QUIT"  # Exit game after gameplay finishes

    # Quit pygame when the game exits
    pygame.quit()

if __name__ == "__main__":
    main()