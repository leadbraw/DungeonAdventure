import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, SPRITE_PATHS, get_fonts
from src.model.managers.adventurer_manager import AdventurerManager
from src.model.managers.sprite_manager import SpriteManager
from src.model.managers.game_state_manager import GameStateManager
from src.controller.game_controller import GameController
from src.controller.game_setup import GameSetup
from src.view.splash_screen import SplashScreen
from src.view.main_screen import MainScreen
from src.view.character_screen import CharacterScreen


class MainController:
    """Handles the main menu and state transitions to/from it (to character selection, gameplay, etcetera)."""

    def __init__(self):
        """Constructor. Initializes pygame, the window, and fields."""
        pygame.init()
        self.fonts = get_fonts()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Dungeon Adventure")

        # Preload sprite and set icon
        sprite_manager = SpriteManager.get_instance()
        sprite_manager.preload_sprites({
            "dice": SPRITE_PATHS["dice"]
        })
        dungeon_icon = sprite_manager.get_sprite("dice")
        pygame.display.set_icon(dungeon_icon)

        self.game_setup = GameSetup()
        self.state = "MAIN_MENU"
        self.selected_hero = None
        self.debug = False
        self.loading = False
        self.game_controller = None

    def run(self):
        """Main game loop."""
        splash_screen = SplashScreen(self.screen, self.fonts["large"])
        splash_screen.display("TEAM 5", setup_function=self.game_setup.setup)

        while self.state != "QUIT":
            if self.state == "MAIN_MENU":
                self.main_menu()
            elif self.state == "CHARACTER_SELECTION":
                self.character_selection()
            elif self.state == "GAMEPLAY":
                self.gameplay()

        pygame.quit()

    def main_menu(self):
        """Handles the main menu and state transitions from it."""
        main_menu = MainScreen(self.screen, self.fonts)
        choice = main_menu.run()
        if choice == "new_game":
            self.state = "CHARACTER_SELECTION"
        elif choice == "load_game":
            self.loading = True
            try:
                self.game_controller = GameStateManager.load_game_state()
                self.game_controller.set_up_from_load(self.screen, self.fonts)
                self.state = "GAMEPLAY"
            except FileNotFoundError:
                print("No saved game file found. Try saving a game before loading.")
                self.loading = False
                self.state = "MAIN_MENU"
            except Exception as e:
                print(f"An unexpected error occurred: {e}")
                self.loading = False
                self.state = "MAIN_MENU"

    def character_selection(self):
        """Handles the character selection screen(s) and state transitions from them."""
        adventurer_manager = AdventurerManager.get_instance()
        adventurer_data = adventurer_manager.get_adventurer_data()

        character_screen = CharacterScreen(self.screen, self.fonts, adventurer_data)
        result = character_screen.run()
        if isinstance(result, tuple):
            if result[1] == "debug":
                self.debug = True
            self.selected_hero = result[0]
            self.state = "GAMEPLAY"
        elif result is None:
            self.state = "MAIN_MENU"

    def gameplay(self):
        """Handles gameplay and state transitions from it."""
        if self.selected_hero or self.loading:
            if not self.loading:
                self.game_controller = GameController(self.screen, self.selected_hero, self.debug)
                self.game_controller.set_active_adventurer(self.selected_hero)
            self.loading = False
            if self.game_controller.display_game() == 1:
                self.state = "MAIN_MENU"
            else:
                self.state = "QUIT"