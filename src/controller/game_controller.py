import random
import sys
import pygame
from constants import (BACKGROUND_COLOR, DARK_GREY, get_fonts, OFF_WHITE, LIGHT_BLUE, MAP_CELL_WIDTH,
                       MENU_BUTTON_HEIGHT, MENU_BUTTON_WIDTH, GOLD, SCREEN_WIDTH, SCREEN_HEIGHT, DARK_RED, RED, BROWN,
                       FADED_GRAY, MEDIUM_GREY, VIOLET, DARK_VIOLET)
from src.controller.battle_manager import BattleManager
from src.controller.dungeon_manager import DungeonManager
from src.view.gui_elements import Button
from src.view.inventory_overlay import InventoryOverlay
from src.model.managers.room_manager import RoomManager
from src.model.managers.adventurer_manager import AdventurerManager
from src.model.managers.sprite_manager import SpriteManager
from src.model.factories.adventurer_factory import AdventurerFactory

from src.model.managers.game_state_manager import GameStateManager


class GameController:
    def __init__(self, screen, hero_name, debug):
        self.screen = screen
        self.hero_name = hero_name
        self.debug = debug
        self.fonts = get_fonts()  # Dictionary of fonts
        self.room_manager = RoomManager.get_instance()
        self.sprite_manager = SpriteManager.get_instance()
        self.battle_manager = BattleManager.get_instance(self.screen, self.fonts, self.draw_ui)
        self.dungeon_manager = DungeonManager.get_instance()
        self.dungeon_manager.initialize_dungeon()
        self.adventurer_manager = AdventurerManager.get_instance()
        self.minimap = None
        self.full_maps = []
        for i in range(4):  # Collect all fully revealed maps for display upon game completion
            self.full_maps.append(self.dungeon_manager.get_floor_map(i + 1, reveal_all=True))
        # Attributes for game state
        self.current_floor = 1
        self.position = self.dungeon_manager.get_floor_entrance(self.current_floor)  # Fetch entrance position
        self.active_adventurer = None
        self.current_message = None
        self.pillars_found = 0
        self.return_to_menu = False  # Flag for if user chose to return to menu. Only set to True upon losing a battle.

        self.inventory_button = Button(color=LIGHT_BLUE, x=670, y=160, width=110, height=30,
                                       font=self.fonts["small"], text_color=(255, 255, 255), text="Inventory")
        self.save_button = Button(color=LIGHT_BLUE, x=670, y=200, width=110, height=30,
                                  font=self.fonts["extra_small"], text_color=(255, 255, 255), text="Save Game")

        # Mark the starting room as visited and initialize the adventurer
        self.dungeon_manager.mark_room_visited(self.current_floor, self.position)
        self.set_active_adventurer(hero_name)

    def display_game(self):
        """Main gameplay loop."""
        if self.debug:
            self.minimap = pygame.transform.scale(self.dungeon_manager.get_floor_map(self.current_floor, self.debug),
                                                  (150, 150))
        while True:
            self.screen.fill(DARK_GREY)

            # Render the current room's sprite
            current_room = self.dungeon_manager.get_room(self.current_floor, self.position)
            room_doors = current_room.valid_directions
            sprite_config = self.room_manager.get_room_by_doors(room_doors)
            self.render_room_sprite(sprite_config)
            if not self.debug:  # Don't fetch map every frame if not needed.
                self.minimap = pygame.transform.scale(self.dungeon_manager.get_floor_map(self.current_floor),
                                                      (150, 150))
            self.draw_ui()  # Draw UI draws map as well

            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if self.inventory_button.is_hovered(mouse_pos):
                        # Pass the current position and dungeon explicitly
                        inventory_overlay = InventoryOverlay(
                            self.screen,
                            self.fonts,
                            self.active_adventurer.inventory,
                            current_monster=None,  # No monster when out of combat
                            current_room=self.position,  # Use current position
                            dungeon=self.dungeon_manager.dungeon  # Pass the entire dungeon
                        )

                        # Provide position and the current dungeon floor to the display method
                        inventory_overlay.display(
                            target=self.active_adventurer,
                            position=self.position,
                            dungeon=self.dungeon_manager.dungeon[self.current_floor - 1]  # Specific dungeon floor
                        )
                    elif self.save_button.is_hovered(mouse_pos):
                        GameStateManager.save_game_state(self)
                        self.display_message("Game saved!", 500)

                elif event.type == pygame.KEYDOWN:
                    self.player_movement(event.key)

            if self.return_to_menu:
                return 1  # This will be seen by main.py and trigger a return to the main menu.
            pygame.display.flip()

    def player_movement(self, key):
        """Handles player movement based on arrow key input."""
        direction_map = {
            pygame.K_UP: (-1, 0),
            pygame.K_RIGHT: (0, 1),
            pygame.K_DOWN: (1, 0),
            pygame.K_LEFT: (0, -1)
        }
        direction_indices = {
            pygame.K_UP: 0,
            pygame.K_RIGHT: 1,
            pygame.K_DOWN: 2,
            pygame.K_LEFT: 3
        }

        if key in direction_map:
            dx, dy = direction_map[key]
            direction_index = direction_indices[key]
            current_room = self.dungeon_manager.get_room(self.current_floor, self.position)

            if current_room.valid_directions[direction_index]:
                self.position = (self.position[0] + dx, self.position[1] + dy)
                self.room_interaction()
            else:
                self.display_message("Invalid move: No valid path in that direction.", 250)

    def room_interaction(self):
        """Interact with the current room."""
        current_room = self.dungeon_manager.get_room(self.current_floor, self.position)

        if current_room.type in ["MONSTER", "ELITE"] and current_room.has_monster():
            self.handle_monster_room(current_room)
        elif current_room.type == "ITEM" and current_room.has_item():
            self.handle_item_room()
        elif current_room.type == "EXIT":
            self.handle_exit_room()
        elif current_room.type == "ENTRANCE":
            self.display_message("You are back at the entrance.")
        elif current_room.type == "PILLAR" and current_room.has_item():
            self.handle_pillar_room()
        elif current_room.type == "TRAP" and not current_room.visited:
            self.handle_trap_room()
        elif current_room.type == "EMPTY":
            self.dungeon_manager.mark_room_visited(self.current_floor, self.position)
            self.display_message("You've found an empty room. It smells in here.")

    def handle_monster_room(self, room):
        """Handles interactions in MONSTER and ELITE rooms."""
        monster = self.dungeon_manager.get_monster_in_room(self.current_floor, self.position)
        if not monster:
            return

        message = (
            f"A wild {monster.name} appears! Prepare for battle!" if room.type == "MONSTER"
            else f"An ELITE {monster.name} stands before you! Prepare for a tough fight!"
        )
        self.render_monster_sprite(monster.name)
        self.display_message(message, delay=2000, in_battle=True)
        self.dungeon_manager.mark_room_visited(self.current_floor, self.position)
        battle_result = self.battle_manager.start_battle(
            adventurer=self.active_adventurer,
            monster=monster,
            dungeon=self.dungeon_manager.dungeon,
            current_floor=self.current_floor,
            position=self.position,
            get_hero_portrait=self.get_hero_portrait,
            minimap=self.minimap
        )

        if battle_result == 1:
            self.return_to_menu = True

    def handle_item_room(self):
        """Handles interactions in ITEM rooms."""
        item = self.dungeon_manager.get_item_in_room(self.current_floor, self.position)
        if not item:
            self.display_message("There's no item here.")
            return
        if item.name.startswith("Pillar"):
            self.handle_pillar_item(item)
        else:
            self.handle_regular_item(item)
        self.dungeon_manager.mark_room_visited(self.current_floor, self.position)

    def handle_pillar_room(self):
        """Handles interactions in PILLAR rooms."""
        item = self.dungeon_manager.get_item_in_room(self.current_floor, self.position)
        if not item:
            self.display_message("There's no pillar here. Strange...")
            return
        self.handle_pillar_item(item)
        self.pillars_found += 1
        self.dungeon_manager.mark_room_visited(self.current_floor, self.position)

    def handle_trap_room(self):
        """Handles interactions in TRAP rooms."""
        trap_dmg = min(random.randint(1, 10), self.active_adventurer.hp - 1)  # Ensure player can't die to trap.
        self.active_adventurer._update_hp(trap_dmg)
        self.display_message(f"It's a trap! You take {trap_dmg} damage.")
        self.dungeon_manager.mark_room_visited(self.current_floor, self.position)

    def handle_pillar_item(self, item):
        """Handles interaction with Pillar items."""
        self.display_message(f"The {item.name} grants you its power!")

        # Use the existing public apply_effect method
        self.active_adventurer.inventory.apply_effect(
            item,
            self.active_adventurer,
            item.effect_min,
            item.effect_max,
        )

        self.dungeon_manager.clear_item_in_room(self.current_floor, self.position)

    def handle_regular_item(self, item):
        """Handles interaction with regular items."""
        if self.active_adventurer.inventory.add_item(item):
            self.display_message(f"{item.name} added to your inventory.")
            self.dungeon_manager.clear_item_in_room(self.current_floor, self.position)
        else:
            self.display_message(f"Your inventory is full! Unable to pick up {item.name}.")

    def handle_exit_room(self):
        """Handles interaction with the Exit room."""
        if self.current_floor == len(self.dungeon_manager.dungeon) and self.pillars_found == self.current_floor:
            self.display_message("You found the exit! Congratulations!", 2000)
            if self.end_message() == 1:  # User chose to return to main menu.
                self.return_to_menu = True
        elif self.pillars_found == self.current_floor:
            self.current_floor += 1
            self.position = self.dungeon_manager.get_floor_entrance(self.current_floor)
            self.dungeon_manager.mark_room_visited(self.current_floor, self.position)
            if self.debug:
                self.minimap = pygame.transform.scale(
                    self.dungeon_manager.get_floor_map(self.current_floor, self.debug),
                    (150, 150))
            self.display_message(f"You've now entered floor {self.current_floor}.")
        else:
            self.dungeon_manager.mark_room_visited(self.current_floor, self.position)
            self.display_message(f"You must find the Pillar of O.O. before proceeding!")

    def end_message(self):
        end_running = True
        end_menu_button = Button(DARK_GREY, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
        end_title = self.fonts["large"].render("CONGRATULATIONS", True, GOLD)
        end_body = self.fonts["medium"].render("You have proven yourself an excellent hero",
                                               True, OFF_WHITE)
        end_body2 = self.fonts["medium"].render("who will surely go down in history as one",
                                                True, OFF_WHITE)
        end_body3 = self.fonts["medium"].render("of the best to ever go adventuring. You",
                                                True, OFF_WHITE)
        end_body4 = self.fonts["medium"].render("vanquished countless monsters, obtained all",
                                                True, OFF_WHITE)
        end_body5 = self.fonts["medium"].render("pillars, and escaped with your life. Well done!",
                                                True, OFF_WHITE)
        end_body6 = self.fonts["medium"].render("Hit \"NEXT\" to view the complete map!",
                                                True, OFF_WHITE)
        next_button = Button(OFF_WHITE, 635, 520, MENU_BUTTON_WIDTH, MENU_BUTTON_HEIGHT, self.fonts["small"],
                             DARK_GREY, "NEXT")
        prev_button = Button(OFF_WHITE, 25, 520, MENU_BUTTON_WIDTH, MENU_BUTTON_HEIGHT, self.fonts["small"],
                             DARK_GREY, "PREVIOUS")
        main_menu_button = Button(OFF_WHITE, 330, 520, MENU_BUTTON_WIDTH, MENU_BUTTON_HEIGHT, self.fonts["small"],
                                  DARK_GREY, "MAIN MENU")

        monster_text = self.fonts["small"].render("Monster", True, OFF_WHITE)
        elite_text = self.fonts["small"].render("Elite", True, OFF_WHITE)
        item_text = self.fonts["small"].render("Item", True, OFF_WHITE)
        trap_text = self.fonts["small"].render("Trap", True, OFF_WHITE)
        pillar_text = self.fonts["small"].render("Pillar", True, OFF_WHITE)
        empty_text = self.fonts["small"].render("Empty", True, OFF_WHITE)
        entrance_text = self.fonts["small"].render("Entrance", True, OFF_WHITE)
        exit_text = self.fonts["small"].render("Exit", True, OFF_WHITE)

        monster_rect = pygame.Rect(540, 30, 35, 35)
        elite_rect = pygame.Rect(540, 80, 35, 35)
        item_rect = pygame.Rect(540, 130, 35, 35)
        trap_rect = pygame.Rect(540, 180, 35, 35)
        pillar_rect = pygame.Rect(540, 230, 35, 35)
        empty_rect = pygame.Rect(540, 280, 35, 35)
        entrance_rect = pygame.Rect(540, 330, 35, 35)
        exit_rect = pygame.Rect(540, 380, 35, 35)

        position = 0
        while end_running:
            clicked = False
            mouse_pos = pygame.mouse.get_pos()
            end_menu_button.draw(self.screen, outline=True)
            main_menu_button.draw(self.screen, outline=True)
            if position == 0:
                self.screen.blit(end_title, (SCREEN_WIDTH / 2 - end_title.get_width() / 2,
                                             SCREEN_HEIGHT / 8 - end_title.get_height() / 2))
                self.screen.blit(end_body, (SCREEN_WIDTH / 2 - end_body.get_width() / 2,
                                            SCREEN_HEIGHT / 5 - end_body.get_height() / 2 + 50))
                self.screen.blit(end_body2, (SCREEN_WIDTH / 2 - end_body.get_width() / 2,
                                             SCREEN_HEIGHT / 5 - end_body.get_height() / 2 + 103))
                self.screen.blit(end_body3, (SCREEN_WIDTH / 2 - end_body.get_width() / 2,
                                             SCREEN_HEIGHT / 5 - end_body.get_height() / 2 + 156))
                self.screen.blit(end_body4, (SCREEN_WIDTH / 2 - end_body.get_width() / 2,
                                             SCREEN_HEIGHT / 5 - end_body.get_height() / 2 + 209))
                self.screen.blit(end_body5, (SCREEN_WIDTH / 2 - end_body.get_width() / 2,
                                             SCREEN_HEIGHT / 5 - end_body.get_height() / 2 + 262))
                self.screen.blit(end_body6, (SCREEN_WIDTH / 2 - end_body.get_width() / 2,
                                             SCREEN_HEIGHT / 5 - end_body.get_height() / 2 + 315))
                next_button.draw(self.screen, True)

            elif 0 < position < 5:
                # Messy, don't care! Too bad!
                pygame.draw.rect(self.screen, DARK_RED, elite_rect)
                pygame.draw.rect(self.screen, RED, monster_rect)
                pygame.draw.rect(self.screen, BROWN, trap_rect)
                pygame.draw.rect(self.screen, GOLD, item_rect)
                pygame.draw.rect(self.screen, FADED_GRAY, pillar_rect)
                pygame.draw.rect(self.screen, MEDIUM_GREY, empty_rect)
                pygame.draw.rect(self.screen, VIOLET, entrance_rect)
                pygame.draw.rect(self.screen, DARK_VIOLET, exit_rect)
                self.screen.blit(monster_text, (590, 30 + elite_text.get_height() / 2 - 3))
                self.screen.blit(elite_text, (590, 80 + elite_text.get_height() / 2 - 3))
                self.screen.blit(item_text, (590, 130 + elite_text.get_height() / 2 - 3))
                self.screen.blit(trap_text, (590, 180 + elite_text.get_height() / 2 - 3))
                self.screen.blit(pillar_text, (590, 230 + elite_text.get_height() / 2 - 3))
                self.screen.blit(empty_text, (590, 280 + elite_text.get_height() / 2 - 3))
                self.screen.blit(entrance_text, (590, 330 + elite_text.get_height() / 2 - 3))
                self.screen.blit(exit_text, (590, 380 + elite_text.get_height() / 2 - 3))
                map_surface = pygame.transform.scale(self.full_maps[position - 1], (400, 400))
                self.screen.blit(map_surface, (130, 25))
                floor_text = self.fonts["large"].render(f"Floor {position}", True, OFF_WHITE)
                self.screen.blit(floor_text, (SCREEN_WIDTH / 2 - floor_text.get_width() / 2, 430))
                prev_button.draw(self.screen, True)
                if position != 4:
                    next_button.draw(self.screen, True)

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # left click
                    clicked = True
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            if clicked:
                if next_button.is_hovered(mouse_pos) and position < 4:
                    position += 1
                elif prev_button.is_hovered(mouse_pos) and position > 0:
                    position -= 1
                elif main_menu_button.is_hovered(mouse_pos):
                    return 1  # Will be seen by handle_exit_room, which will set the return_to_menu field to True

            pygame.display.flip()

    def render_room_sprite(self, sprite_config):
        """Renders the sprite for the current room."""
        if sprite_config and "sprite_name" in sprite_config and "rotation" in sprite_config:
            sprite_name, rotation = sprite_config["sprite_name"], sprite_config["rotation"]
            room_sprite = self.sprite_manager.get_transformed_sprite(sprite_name, rotate=rotation)

            if room_sprite:
                x = (650 - room_sprite.get_width()) // 2
                y = 0
                self.screen.blit(room_sprite, (x, y))
            else:
                print(f"Failed to render sprite '{sprite_name}' with rotation {rotation}.")
        else:
            print(f"Invalid sprite config: {sprite_config}")

    def render_monster_sprite(self, monster_name):
        choice = random.choice(("_one", "_two"))
        if monster_name == "Tom":
            sprite = self.sprite_manager.get_sprite("tom")
        else:
            sprite = self.sprite_manager.get_sprite(monster_name.lower() + choice)
        sprite_scaled = pygame.transform.scale(sprite, (450, 450))
        self.screen.blit(sprite_scaled, (100, 0))

    def display_message(self, message, delay=0, in_battle=False):
        """Displays a message and optionally delays for a specified duration."""
        self.draw_ui(message, in_battle=in_battle)
        pygame.display.flip()
        if delay > 0:
            pygame.time.delay(delay)

    def set_active_adventurer(self, adventurer_name):
        """Sets the active adventurer."""
        raw_data = self.adventurer_manager.get_adventurer_data(name=adventurer_name)[1:]
        if raw_data:
            self.active_adventurer = AdventurerFactory.get_instance().make_adventurer(raw_data)
            if self.debug:
                self.active_adventurer.apply_buff(999 - self.active_adventurer.max_hp, "max_hp")  # sets value to 999
                self.active_adventurer.apply_buff(100, "block_chance")
                self.active_adventurer.apply_buff(500, "attack_damage")
                self.active_adventurer.apply_buff(50, "attack_speed")
                self.active_adventurer.apply_buff(1, "hit_chance")
        else:
            print(f"Adventurer '{adventurer_name}' not found.")
        self.adventurer_manager.active_adventurer = self.active_adventurer

    def draw_ui(self, message=None, in_battle=False):
        """Draws the game's user interface."""
        bottom_rect = pygame.Rect(0, 450, 800, 150)
        right_rect = pygame.Rect(650, 0, 150, 450)
        pygame.draw.rect(self.screen, BACKGROUND_COLOR, bottom_rect)
        pygame.draw.rect(self.screen, BACKGROUND_COLOR, right_rect)

        # Draw adventurer portrait
        portrait = self.get_hero_portrait()
        self.screen.blit(portrait, (650, 450))

        # Display adventurer stats
        current_hp, max_hp = self.active_adventurer.hp, self.active_adventurer.max_hp
        block_chance, attack_speed = self.active_adventurer.block_chance, self.active_adventurer.attack_speed
        damage_range, hit_chance = self.active_adventurer.damage_range, self.active_adventurer.hit_chance
        hp_text = self.fonts["small"].render(f"HP: {current_hp} / {max_hp}", True, OFF_WHITE)
        block_text = self.fonts["extra_small"].render(f"Block %: {block_chance * 100:.0f}%", True, OFF_WHITE)
        speed_text = self.fonts["extra_small"].render(f"Speed: {attack_speed}", True, OFF_WHITE)
        range_text = self.fonts["extra_small"].render(f"Attack: {damage_range[0]}-{damage_range[1]}", True, OFF_WHITE)
        hit_text = self.fonts["extra_small"].render(f"Hit %: {hit_chance * 100:.0f}%", True, OFF_WHITE)
        self.screen.blit(block_text, (660, 385))
        self.screen.blit(speed_text, (660, 350))
        self.screen.blit(range_text, (660, 315))
        self.screen.blit(hit_text, (660, 280))
        self.screen.blit(hp_text, (660, 420))

        # Display room message
        if message:
            self.current_message = message
        if self.current_message:
            message_text = self.fonts["small"].render(self.current_message, True, OFF_WHITE)
            self.screen.blit(message_text, (50, 500))

        # Draw minimap
        self.screen.blit(self.minimap, (650, 0))

        # Draw current position on minimap
        dim = MAP_CELL_WIDTH
        pygame.draw.circle(self.screen, (255, 255, 255),
                           (650 + self.position[1] * dim + dim / 2, 5 + self.position[0] * dim + 3), 5)
        if not in_battle:
            # Draw save and inventory buttons
            self.save_button.draw(self.screen)
            self.inventory_button.draw(self.screen)

    def get_hero_portrait(self):
        """Returns the portrait for the selected hero."""
        portrait_paths = {
            "Noah": "assets/images/noah_portrait.png",
            "Sean": "assets/images/sean_portrait.png",
            "Jayne": "assets/images/jayne_portrait.png",
            "Mark": "assets/images/mark_portrait.png"
        }
        portrait_path = portrait_paths.get(self.hero_name, "assets/images/hero.png")
        portrait = pygame.image.load(portrait_path).convert_alpha()
        return pygame.transform.scale(portrait, (150, 150))

    def set_up_from_load(self, the_screen, the_fonts):
        self.screen = the_screen
        self.fonts = the_fonts
        self.battle_manager = BattleManager.get_instance(self.screen, self.fonts, self.draw_ui)
        self.sprite_manager = SpriteManager.get_instance()
        self.full_maps = []
        for i in range(4):  # mirror constructor
            self.full_maps.append(self.dungeon_manager.get_floor_map(i + 1, reveal_all=True))
        self.inventory_button = Button(color=LIGHT_BLUE, x=670, y=160, width=110, height=30,
                                       font=self.fonts["small"], text_color=(255, 255, 255), text="Inventory")
        self.save_button = Button(color=LIGHT_BLUE, x=670, y=200, width=110, height=30,
                                  font=self.fonts["extra_small"], text_color=(255, 255, 255), text="Save Game")

    # Method to define what gets pickled
    def __getstate__(self):
        # Return a dictionary of the object's state
        print("Game Controller state saved.")
        return {
            'hero_name': self.hero_name,  # string
            'room_manager': self.room_manager,  # pickled
            'dungeon_manager': self.dungeon_manager,
            # 'adventurer_manager': self.adventurer_manager,  # to be pickled
            'current_floor': self.current_floor,  # int
            'position': self.position,  # tuple
            'active_adventurer': self.active_adventurer,
            'current_message': self.current_message,  # string
            'pillars_found': self.pillars_found,  # int
            'return_to_menu': self.return_to_menu,  # boolean
            'debug': self.debug  # boolean
        }

    # Method to define how the object is restored
    def __setstate__(self, state):
        # Restore the object's state from the dictionary
        self.hero_name = state['hero_name']
        self.room_manager = state['room_manager']
        self.dungeon_manager = state['dungeon_manager']
        # self.adventurer_manager = state['adventurer_manager']
        self.current_floor = state['current_floor']
        self.position = state['position']
        self.active_adventurer = state['active_adventurer']
        self.current_message = state['current_message']
        self.pillars_found = state['pillars_found']
        self.return_to_menu = state['return_to_menu']
        self.debug = state['debug']
        print("Loaded save for: " + self.hero_name)
