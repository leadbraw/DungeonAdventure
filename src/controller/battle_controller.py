import sys
import pygame
from constants import BACKGROUND_COLOR, BLACK, LIGHT_BLUE, OFF_WHITE, WHITE
from src.view.gui_elements import Button


class BattleController:
    """Singleton class. Called by GameController to handle battle logic."""

    _instance = None

    @staticmethod
    def get_instance(screen=None, fonts=None, draw_ui=None):
        """
        Instantiates (or resets) a/the singleton instance of BattleController.
        :return current instance of DungeonManager (a new instance if none existed prior to the get_instance() call).
        """
        if not all([screen, fonts, draw_ui]):
            raise ValueError("Missing arguments for initializing or resetting BattleController.")
        if BattleController._instance is None:
            BattleController._instance = BattleController(screen, fonts, draw_ui)
        else:
            # There is an existing instance, let's reset it.
            BattleController._instance.reset(screen, fonts, draw_ui)
        return BattleController._instance

    def __init__(self, screen, fonts, draw_ui):
        """
        Constructor, initializes all fields.

        :param screen: The display (Surface)
        :param fonts: Dict of fonts (see constants.py)
        :param draw_ui Passed draw_ui function from GameController
        """
        if BattleController._instance is not None:
            raise Exception("This class is a singleton! Use get_instance() to access it.")
        self.screen = screen
        self.fonts = fonts
        self.draw_ui = draw_ui
        self.inventory_overlay = None

    def reset(self, screen, fonts, draw_ui):
        """
        Overrides all fields of the BattleController instance with new values.

        :param screen: The new display Surface
        :param fonts: The new fonts dict
        :param draw_ui: The new draw_ui function from GameController (now with a new referencing environment!)
        """
        self.screen = screen
        self.fonts = fonts
        self.draw_ui = draw_ui

    def start_battle(self, adventurer, monster, dungeon, current_floor, position, get_adventurer_portrait, minimap,
                     inventory_overlay):
        """
        Handles the main battle loop.

        :param adventurer: The adventurer in the battle.
        :param monster: The current monster in the battle.
        :param dungeon: The dungeon object (list of floors).
        :param current_floor: The current floor (1-indexed).
        :param position: The current position of the adventurer as a tuple (x, y).
        :param inventory_overlay: The InventoryOverlay instance.
        :param get_adventurer_portrait: The get_adventurer_portrait function from GameController.
        :param minimap: The current minimap.
        :return: True if the battle continues, False otherwise.
        """
        self.inventory_overlay = inventory_overlay  # Store the passed InventoryOverlay instance

        fight_button = Button(color=LIGHT_BLUE, x=200, y=540, width=100, height=30,
                              font=self.fonts["small"], text_color=WHITE, text="Fight")
        item_button = Button(color=LIGHT_BLUE, x=325, y=540, width=100, height=30,
                             font=self.fonts["small"], text_color=WHITE, text="Use Item")
        special_button = Button(color=LIGHT_BLUE, x=450, y=540, width=100, height=30,
                                font=self.fonts["small"], text_color=WHITE, text="Special")

        running = True
        while running and monster.hp > 0 and adventurer.hp > 0:
            # Pass `get_adventurer_portrait` as a callable
            self.draw_battle_ui(monster, adventurer, fight_button, item_button, special_button,
                                get_adventurer_portrait, minimap)
            running = self.handle_battle_event(
                monster, adventurer, self.inventory_overlay, dungeon, current_floor, position,
                fight_button, item_button, special_button
            )

        if self.post_battle_logic(monster, adventurer, dungeon, current_floor, position) == 1:
            # Triggers a restart in the game controller and main
            return 1

    def draw_battle_ui(self, monster, adventurer, fight_button, item_button, special_button,
                       get_adventurer_portrait, minimap):
        """
        Draw the battle UI components.

        :param monster: The current monster in the battle.
        :param adventurer: The adventurer in the battle.
        :param fight_button: The button for fight actions.
        :param item_button: The button for using items.
        :param special_button: The button for using special ability
        :param get_adventurer_portrait: The get_adventurer_portrait function from GameController.
        :param minimap: The current minimap.
        """
        bottom_rect = pygame.Rect(0, 450, 800, 150)
        pygame.draw.rect(self.screen, BACKGROUND_COLOR, bottom_rect)

        portrait_outline_top = pygame.Rect(650, 450, 150, 4)
        portrait_outline_left = pygame.Rect(650, 450, 4, 150)
        portrait_outline_bottom = pygame.Rect(650, 596, 150, 4)
        portrait_outline_right = pygame.Rect(796, 450, 4, 150)

        # Use the callable to fetch the hero portrait, then draw outline
        portrait = get_adventurer_portrait()
        self.screen.blit(portrait, (650, 450))
        pygame.draw.rect(self.screen, BLACK, portrait_outline_top)
        pygame.draw.rect(self.screen, BLACK, portrait_outline_left)
        pygame.draw.rect(self.screen, BLACK, portrait_outline_bottom)
        pygame.draw.rect(self.screen, BLACK, portrait_outline_right)

        monster_text = self.fonts["small"].render(f"Monster HP: {monster.hp}", True, OFF_WHITE)
        adventurer_text = self.fonts["small"].render(f"Your HP: {adventurer.hp}", True, OFF_WHITE)
        self.screen.blit(monster_text, (50, 490))
        self.screen.blit(adventurer_text, (50, 510))
        self.screen.blit(minimap, (650, 0))

        fight_button.draw(self.screen, True)
        item_button.draw(self.screen, True)
        special_button.draw(self.screen, True)

        pygame.display.flip()

    def handle_battle_event(self, monster, adventurer, inventory_overlay, dungeon, current_floor, position,
                            fight_button, item_button, special_button):
        """
        Handle player input during the battle.

        :param monster: The current monster in the battle.
        :param adventurer: The adventurer in the battle.
        :param inventory_overlay: The InventoryOverlay instance.
        :param dungeon: The dungeon object (list of floors).
        :param current_floor: The current floor (1-indexed).
        :param position: The current position of the adventurer as a tuple (x, y).
        :param fight_button: The button for fight actions.
        :param item_button: The button for using items.
        :param special_button: The button for using special ability
        :return: True if the battle continues, False otherwise.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                # Fight button logic
                if fight_button.is_hovered(mouse_pos):
                    self.execute_fight(monster, adventurer)

                # Special Attack Logic
                elif special_button.is_hovered(mouse_pos):
                    self.execute_special(monster, adventurer)

                # Item button logic
                elif item_button.is_hovered(mouse_pos):
                    inventory_overlay.display(target=adventurer)

                    selected_item = inventory_overlay.selected_item
                    if selected_item:
                        # Handle target logic for item types
                        if selected_item.name == "White Box":
                            actual_target = (
                                position, dungeon[current_floor])
                        elif selected_item.name == "Code Spike":
                            actual_target = monster
                        else:
                            actual_target = adventurer
                        if adventurer.inventory.use_item(selected_item.name, actual_target):
                            # Continue the battle
                            return True
                    else:
                        pass

        # Continue the battle as long as both monster and adventurer are alive
        return monster.hp > 0 and adventurer.hp > 0

    def post_battle_logic(self, monster, adventurer, dungeon, current_floor, position):
        """
        Handle the aftermath of the battle.

        :param monster: The current monster in the battle.
        :param adventurer: The adventurer in the battle.
        :param dungeon: The dungeon object (list of floors).
        :param current_floor: The current floor (1-indexed).
        :param position: The current position of the adventurer as a tuple (x, y).
        """
        if monster.hp <= 0:
            message = f"You defeated {monster.name}, well done!"
            self.draw_ui(message)
            pygame.display.flip()
            pygame.time.delay(2000)
            current_room = dungeon[current_floor - 1].fetch_room(position[0], position[1])
            current_room.set_monster(None)

        elif adventurer.hp <= 0:
            # Display game-over options
            menu_text = self.fonts["medium"].render("Return to Menu or Quit?", True, OFF_WHITE)
            bottom_rect = pygame.Rect(0, 450, 800, 150)
            menu_button = Button(color=LIGHT_BLUE, x=150, y=540, width=100, height=30,
                                 font=self.fonts["small"], text_color=(255, 255, 255), text="Menu")
            quit_button = Button(color=LIGHT_BLUE, x=350, y=540, width=100, height=30,
                                 font=self.fonts["small"], text_color=(255, 255, 255), text="Quit")
            while True:
                pygame.draw.rect(self.screen, (0, 0, 0), bottom_rect)

                self.screen.blit(menu_text, (200, 470))

                menu_button.draw(self.screen)
                quit_button.draw(self.screen)
                pygame.display.flip()

                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_pos = pygame.mouse.get_pos()

                        if menu_button.is_hovered(mouse_pos):
                            '''This method only returns a value if user chose to replay. This will be sent back
                            to start_battle(), to game controller, and then to main, triggering a restart.'''
                            return 1
                        elif quit_button.is_hovered(mouse_pos):
                            pygame.quit()
                            sys.exit()

    def execute_fight(self, monster, adventurer):
        """
        Handle the 'fight' action.

        :param monster: The current monster in the battle.
        :param adventurer: The adventurer in the battle.
        """
        if monster.hp > 0:
            outcomes = adventurer.attack(monster).split(".")
            for i in range(len(outcomes)):
                # Call the passed draw_ui method (and add period back in)
                self.draw_ui(outcomes[i] + ".", in_battle=True)
                pygame.display.flip()
                pygame.time.delay(1000)

        if monster.hp > 0:
            message = f"{monster.name} is attacking!"
            # Call the passed draw_ui method
            self.draw_ui(message)
            outcomes = monster.attack(adventurer).split(".")
            for i in range(len(outcomes)):
                # Call the passed draw_ui method (and add period back in)
                self.draw_ui(outcomes[i] + ".", in_battle=True)
                pygame.display.flip()
                pygame.time.delay(1000)

    def execute_special(self, monster, adventurer):
        """
        Handle the 'special' action.

        :param monster: The current monster in the battle.
        :param adventurer: The adventurer in the battle.
        """
        if monster.hp > 0:
            # Call the special_action method to get the full message
            outcomes = adventurer.special_action(monster).split(".")
            for i in range(len(outcomes)):
                if outcomes[i].strip():
                    # Call the passed draw_ui method
                    self.draw_ui(outcomes[i] + ".", in_battle=True)
                    pygame.display.flip()
                    pygame.time.delay(1000)

        if monster.hp > 0:
            message = f"{monster.name} is attacking!"
            # Call the passed draw_ui method
            self.draw_ui(message, in_battle=True)
            outcomes = monster.attack(adventurer).split(".")
            for i in range(len(outcomes)):
                # Call the passed draw_ui method (and add period back in)
                self.draw_ui(outcomes[i] + ".", in_battle=True)
                pygame.display.flip()
                pygame.time.delay(1000)