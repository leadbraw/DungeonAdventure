import pygame
import sys
from src.view.gui_elements import Button
from src.view.inventory_overlay import InventoryOverlay
from constants import LIGHT_BLUE, OFF_WHITE, BACKGROUND_COLOR

class BattleManager:
    _instance = None

    @staticmethod
    def get_instance(screen=None, fonts=None, draw_ui=None):
        if not all([screen, fonts, draw_ui]):
            raise ValueError("Missing arguments for initializing or resetting BattleManager.")
        if BattleManager._instance is None:
            BattleManager._instance = BattleManager(screen, fonts, draw_ui)
        else: # There is an existing instance, let's reset it.
            BattleManager._instance.reset(screen, fonts, draw_ui)
        return BattleManager._instance

    def __init__(self, screen, fonts, draw_ui):
        if BattleManager._instance is not None:
            raise Exception("This class is a singleton! Use get_instance() to access it.")
        self.screen = screen
        self.fonts = fonts
        self.draw_ui = draw_ui

    def reset(self, screen, fonts, draw_ui):
        self.screen = screen
        self.fonts = fonts
        self.draw_ui = draw_ui

    def start_battle(self, adventurer, monster, dungeon, current_floor, position, get_hero_portrait, minimap):
        """Starts and Handles battle action with player vs monster in the Room section."""
        inventory_overlay = InventoryOverlay(
            self.screen,
            self.fonts,
            adventurer.inventory,
            current_monster=monster,  # Pass current monster
            current_room=position,  # Pass current position
            dungeon=dungeon  # Pass dungeon
        )

        fight_button = Button(color=LIGHT_BLUE, x=200, y=540, width=100, height=30,
                              font=self.fonts["small"], text_color=(255, 255, 255), text="Fight")
        item_button = Button(color=LIGHT_BLUE, x=325, y=540, width=100, height=30,
                             font=self.fonts["small"], text_color=(255, 255, 255), text="Use Item")
        special_button = Button(color=LIGHT_BLUE, x=450, y=540, width=100, height=30,
                                font=self.fonts["small"], text_color=(255, 255, 255), text="Special")

        running = True
        while running and monster.hp > 0 and adventurer.hp > 0:
            # Pass `get_hero_portrait` as a callable
            self.draw_battle_ui(monster, adventurer, fight_button, item_button, special_button, get_hero_portrait, minimap)
            running = self.handle_battle_event(
                monster, adventurer, inventory_overlay, dungeon, current_floor, position,
                fight_button, item_button, special_button
            )

        if self.post_battle_logic(monster, adventurer, dungeon, current_floor, position) == 1:
            return 1  # Triggers a restart in the game controller and main

    def draw_battle_ui(self, monster, adventurer, fight_button, item_button, special_button, get_hero_portrait, minimap):
        """Draw the battle UI components."""
        bottom_rect = pygame.Rect(0, 450, 800, 150)
        pygame.draw.rect(self.screen, (0, 0, 0), bottom_rect)
        pygame.draw.rect(self.screen, BACKGROUND_COLOR, bottom_rect)

        # Use the callable to fetch the hero portrait
        portrait = get_hero_portrait()
        self.screen.blit(portrait, (650, 450))

        monster_text = self.fonts["small"].render(f"Monster HP: {monster.hp}", True, OFF_WHITE)
        adventurer_text = self.fonts["small"].render(f"Your HP: {adventurer.hp}", True, OFF_WHITE)
        self.screen.blit(monster_text, (50, 490))
        self.screen.blit(adventurer_text, (50, 510))
        self.screen.blit(minimap, (650, 0))

        fight_button.draw(self.screen)
        item_button.draw(self.screen)
        special_button.draw(self.screen)

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
                    print(f"[DEBUG] Selected item: {selected_item}")  # Debugging line
                    if selected_item:
                        # Handle target logic for item types
                        if selected_item.name == "White Box":
                            actual_target = (
                            position, dungeon[current_floor - 1])  # Use position and floor for room effects
                        elif selected_item.name == "Code Spike":
                            actual_target = monster  # Use monster for damage
                        else:
                            actual_target = adventurer  # Default target is the adventurer

                        if adventurer.inventory.use_item(selected_item.name, actual_target):
                            print(f"You used {selected_item.name}.")
                            return True  # Continue the battle
                        else:
                            print(f"Failed to use {selected_item.name}.")
                    else:
                        print("No item was selected. Returning to battle options.")



            # Continue the battle as long as both monster and adventurer are alive
        return monster.hp > 0 and adventurer.hp > 0

    def post_battle_logic(self, monster, adventurer, dungeon, current_floor, position):
        """Handle the aftermath of the battle."""
        if monster.hp <= 0:
            message = f"You defeated {monster.name}, well done!"
            self.draw_ui(message)
            pygame.display.flip()
            pygame.time.delay(2000)
            current_room = dungeon[current_floor - 1].fetch_room(position[0], position[1])
            current_room.set_monster(None)  # Clear monster from the room

        elif adventurer.hp <= 0:
            print("You were defeated, GAME OVER :(")

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
                            print("Returning to main menu...")
                            '''This method only returns a value if user chose to replay. This will be sent back
                            to start_battle(), to game controller, and then to main, triggering a restart.'''
                            return 1
                        elif quit_button.is_hovered(mouse_pos):
                            print("Exiting game...")
                            pygame.quit()
                            sys.exit()

    def execute_fight(self, monster, adventurer):
        """Handle the fight action."""
        if monster.hp > 0:
            outcomes = adventurer.attack(monster).split(".")
            for i in range(len(outcomes)):
                self.draw_ui(outcomes[i]+".")  # Call the passed draw_ui method (and add period back in)
                pygame.display.flip()
                pygame.time.delay(1000)

        if monster.hp > 0:
            message = f"{monster.name} is attacking!"
            self.draw_ui(message)  # Call the passed draw_ui method
            outcomes = monster.attack(adventurer).split(".")
            for i in range(len(outcomes)):
                self.draw_ui(outcomes[i] + ".")  # Call the passed draw_ui method (and add period back in)
                pygame.display.flip()
                pygame.time.delay(1000)

    def execute_special(self, monster, adventurer):
        """Handle the special action."""
        if monster.hp > 0:
            # Call the special_action method to get the full message
            outcomes = adventurer.special_action(monster).split(".")
            for i in range(len(outcomes)):
                if outcomes[i].strip():
                    self.draw_ui(outcomes[i] + ".")  # Call the passed draw_ui method
                    pygame.display.flip()
                    pygame.time.delay(2000)

        if monster.hp > 0:
            message = f"{monster.name} is attacking!"
            self.draw_ui(message)  # Call the passed draw_ui method
            outcomes = monster.attack(adventurer).split(".")
            for i in range(len(outcomes)):
                self.draw_ui(outcomes[i] + ".")  # Call the passed draw_ui method (and add period back in)
                pygame.display.flip()
                pygame.time.delay(1000)