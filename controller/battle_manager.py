import pygame
import sys
from controller.gui_elements import Button
from controller.inventory_overlay import InventoryOverlay
from constants import LIGHT_BLUE, OFF_WHITE, BACKGROUND_COLOR

class BattleManager:
    _instance = None

    @staticmethod
    def get_instance(screen=None, fonts=None, draw_ui=None):
        if BattleManager._instance is None:
            if not all([screen, fonts, draw_ui]):
                raise ValueError("Missing arguments for initializing BattleManager.")
            BattleManager._instance = BattleManager(screen, fonts, draw_ui)
        return BattleManager._instance

    def __init__(self, screen, fonts, draw_ui):
        if BattleManager._instance is not None:
            raise Exception("This class is a singleton! Use get_instance() to access it.")
        self.screen = screen
        self.fonts = fonts
        self.draw_ui = draw_ui

    def start_battle(self, adventurer, monster, dungeon, current_floor, position, get_hero_portrait, minimap):
        """Starts and Handles battle action with player vs monster in the Room section."""
        inventory_overlay = InventoryOverlay(self.screen, self.fonts, adventurer.inventory)

        fight_button = Button(color=LIGHT_BLUE, x=150, y=540, width=100, height=30,
                              font=self.fonts["small"], text_color=(255, 255, 255), text="Fight")
        item_button = Button(color=LIGHT_BLUE, x=350, y=540, width=100, height=30,
                             font=self.fonts["small"], text_color=(255, 255, 255), text="Use Item")
        running = True
        while running and monster.hp > 0 and adventurer.hp > 0:
            # Pass `get_hero_portrait` as a callable
            self.draw_battle_ui(monster, adventurer, fight_button, item_button, get_hero_portrait, minimap)
            running = self.handle_battle_event(
                monster, adventurer, inventory_overlay, dungeon, current_floor, fight_button, item_button
            )

        if self.post_battle_logic(monster, adventurer, dungeon, current_floor, position) == 1:
            return 1 # This will be seen by game controller and main and trigger a restart.

    def draw_battle_ui(self, monster, adventurer, fight_button, item_button, get_hero_portrait, minimap):
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

        pygame.display.flip()

    def handle_battle_event(self, monster, adventurer, inventory_overlay, dungeon, current_floor, fight_button, item_button):
        """Handle player input during the battle."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                if fight_button.is_hovered(mouse_pos):
                    self.execute_fight(monster, adventurer)
                elif item_button.is_hovered(mouse_pos):
                    inventory_overlay.display()

                    # Use the selected item if one was chosen
                    selected_item = inventory_overlay.selected_item
                    if selected_item:
                        if adventurer.inventory.use_item(selected_item, adventurer, dungeon[current_floor - 1]):
                            print(f"You used {selected_item}.")
                            return True  # Continue the battle
                        else:
                            print(f"Failed to use {selected_item}.")
                    else:
                        print("No item was selected. Returning to battle options.")
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
            while True:
                bottom_rect = pygame.Rect(0, 450, 800, 150)
                pygame.draw.rect(self.screen, (0, 0, 0), bottom_rect)
                pygame.display.flip()

                menu_text = self.fonts["medium"].render("Return to Menu or Quit?", True, OFF_WHITE)
                self.screen.blit(menu_text, (200, 470))

                menu_button = Button(color=LIGHT_BLUE, x=150, y=540, width=100, height=30,
                                     font=self.fonts["small"], text_color=(255, 255, 255), text="Menu")
                quit_button = Button(color=LIGHT_BLUE, x=350, y=540, width=100, height=30,
                                     font=self.fonts["small"], text_color=(255, 255, 255), text="Quit")

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
        player_turns = max(1, adventurer.attack_speed // monster.attack_speed)

        for _ in range(player_turns):
            if monster.hp > 0:
                damage = adventurer.attack(monster)
                message = f"You attacked and dealt {damage} damage to {monster.name}."
                self.draw_ui(message)  # Call the passed draw_ui method
                pygame.display.flip()
                pygame.time.delay(2000)
            else:
                break

        if monster.hp > 0:
            message = f"{monster.name} is attacking!"
            self.draw_ui(message)  # Call the passed draw_ui method
            pygame.display.flip()
            pygame.time.delay(2000)
            damage = monster.attack(adventurer)
            message = f"{monster.name} dealt {damage} damage to you."
            self.draw_ui(message)
            pygame.display.flip()
            pygame.time.delay(2000)