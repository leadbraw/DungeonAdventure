import pygame
from constants import (SCREEN_WIDTH, SCREEN_HEIGHT, get_fonts)
from controller.splash_screen import SplashScreen
from controller.main_screen import MainScreen
from controller.character_screen import CharacterScreen
from controller.game_controller import GameController
from controller.game_setup import GameSetup

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
    dungeon_icon = pygame.image.load('assets/images/dice.png')
    pygame.display.set_icon(dungeon_icon)

    # Initialize GameSetup
    game_setup = GameSetup()

    # Define adventurers data
    adventurers_data = [
        (1, "Warrior", "Warrior", 100, 10, 0.8, 15, 25, 0.3),
        (2, "Priest", "Priest", 80, 8, 0.6, 10, 20, 0.4),
        (3, "Thief", "Thief", 70, 12, 0.7, 8, 16, 0.2),
        (4, "Bard", "Bard", 75, 9, 0.65, 10, 18, 0.3),
    ]

    # Show splash screen while running the game setup
    splash_screen = SplashScreen(screen, font_large)
    splash_screen.display("TEAM 5", game_setup.setup)

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
                game_controller = GameController(screen, adventurers_data)
                game_controller.set_active_adventurer(selected_hero)
                game_controller.initialize_dungeon()
                game_controller.display_game()
                state = "QUIT"  # Exit game after gameplay finishes

    # Quit pygame when the game exits
    pygame.quit()

if __name__ == "__main__":
    main()