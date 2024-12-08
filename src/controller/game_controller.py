import random
import sys
import pygame
from constants import BACKGROUND_COLOR, DARK_GREY, get_fonts, OFF_WHITE, LIGHT_BLUE
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
        self.fonts = get_fonts()  # Dictionary of fonts
        self.room_manager = RoomManager.get_instance()
        self.sprite_manager = SpriteManager.get_instance()
        self.battle_manager = BattleManager.get_instance(self.screen, self.fonts, self.draw_ui)
        self.dungeon_manager = DungeonManager.get_instance()
        self.dungeon_manager.initialize_dungeon()
        self.adventurer_manager = AdventurerManager.get_instance()
        self.minimap = None
        self.inventory_button = None
        self.debug = debug

        # Attributes for game state
        self.current_floor = 1
        self.position = self.dungeon_manager.get_floor_entrance(self.current_floor)  # Fetch entrance position
        self.active_adventurer = None
        self.current_message = None
        self.pillars_found = 0
        self.return_to_menu = False # Flag for if user chose to return to menu. Only set to True upon losing a battle.

        self.inventory_button = Button(color=LIGHT_BLUE, x=670, y=160, width=110, height=30,
                                       font=self.fonts["small"], text_color=(255, 255, 255), text="Inventory")
        self.save_button = Button(color=LIGHT_BLUE, x=670, y=200, width=110, height=30,
                                  font=self.fonts["extra_small"], text_color=(255, 255, 255), text="Save Game")

        # Mark the starting room as visited and initialize the adventurer
        self.dungeon_manager.mark_room_visited(self.current_floor, self.position)
        self.set_active_adventurer(hero_name)

    def display_game(self):
        """Main gameplay loop."""
        while True:
            self.screen.fill(DARK_GREY)

            # Render the current room's sprite
            current_room = self.dungeon_manager.get_room(self.current_floor, self.position)
            room_doors = current_room.valid_directions
            sprite_config = self.room_manager.get_room_by_doors(room_doors)
            self.render_room_sprite(sprite_config)

            map_image = self.dungeon_manager.get_floor_map(self.current_floor)
            self.minimap = pygame.transform.scale(map_image, (150, 150))
            self.draw_ui() # Draw UI draws map as well

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

                elif event.type == pygame.KEYDOWN:
                    self.player_movement(event.key)

            if self.return_to_menu:
                return 1 # This will be seen by main.py and trigger a return to the main menu.
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
                self.display_message("Invalid move: No valid path in that direction.", 1000)

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
        self.display_message(message, 2000)
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
        if self.current_floor == len(self.dungeon_manager.dungeon):
            self.display_message("You found the exit! Congratulations!", 3000)
            pygame.quit()
            sys.exit()
        elif self.pillars_found == self.current_floor:
            self.current_floor += 1
            self.position = self.dungeon_manager.get_floor_entrance(self.current_floor)
            self.dungeon_manager.mark_room_visited(self.current_floor, self.position)
            self.display_message(f"You've now entered floor {self.current_floor}.")
        else:
            self.dungeon_manager.mark_room_visited(self.current_floor, self.position)
            self.display_message(f"You must find the Pillar of O.O. before proceeding!")

    def render_room_sprite(self, sprite_config):
        """Renders the sprite for the current room."""
        if sprite_config and "sprite_name" in sprite_config and "rotation" in sprite_config:
            sprite_name, rotation = sprite_config["sprite_name"], sprite_config["rotation"]
            room_sprite = self.sprite_manager.get_transformed_sprite(sprite_name, rotate=rotation)

            if room_sprite:
                test = room_sprite.get_width()
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


    def display_message(self, message, delay=0):
        """Displays a message and optionally delays for a specified duration."""
        self.draw_ui(message)
        pygame.display.flip()
        if delay > 0:
            pygame.time.delay(delay)

    def set_active_adventurer(self, adventurer_name):
        """Sets the active adventurer."""
        raw_data = self.adventurer_manager.get_adventurer_data(name=adventurer_name)[1:]
        if raw_data:
            self.active_adventurer = AdventurerFactory.get_instance().make_adventurer(raw_data)
        else:
            print(f"Adventurer '{adventurer_name}' not found.")
        self.adventurer_manager.active_adventurer = self.active_adventurer

    def draw_ui(self, message=None):
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
        if self.debug: # TODO: implement debug mode widely
            block_text = self.fonts["extra_small"].render(f"Block %: {block_chance * 100}%", True, OFF_WHITE)
            speed_text = self.fonts["extra_small"].render(f"Speed: {attack_speed}", True, OFF_WHITE)
            range_text = self.fonts["extra_small"].render(f"Attack: {damage_range[0]}-{damage_range[1]}", True, OFF_WHITE)
            hit_text = self.fonts["extra_small"].render(f"Hit %: {hit_chance * 100}%", True, OFF_WHITE)
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

    # Method to define what gets pickled
    def __getstate__(self):
        # Return a dictionary of the object's state
        print("Game Controller state saved.")
        return {
                'hero_name': self.hero_name,    # string
                'room_manager': self.room_manager,  # pickled
                # 'battle_manager': self.battle_manager,  # BattleManager ???
                # 'dungeon_manager': self.dungeon_manager,    # to be pickled
                # 'adventurer_manager': self.adventurer_manager,  # to be pickled
                # 'minimap':self.minimap, # ???
                'current_floor': self.current_floor,    # int
                'position': self.position, # tuple
                # 'active_adventurer': self.active_adventurer,    # Adventurer: to be pickled
                'current_message': self.current_message,    # string
                'pillars_found': self.pillars_found,    # int
                'return_to_menu': self.return_to_menu  # boolean
        }

    # Method to define how the object is restored
    def __setstate__(self, state):
        # Restore the object's state from the dictionary
        self.hero_name = state['hero_name']
        self.room_manager = state['room_manager']
        # self.battle_manager = state['battle_manager']
        # self.dungeon_manager = state['dungeon_manager']
        # self.adventurer_manager = state['adventurer_manager']
        # self.minimap = state['minimap']
        self.current_floor = state['current_floor']
        self.position = state['position']
        # self.active_adventurer = state['active_adventurer']
        self.current_message = state['current_message']
        self.pillars_found = state['pillars_found']
        self.return_to_menu = state['return_to_menu']
        print("Loaded save for: " + self.hero_name)
