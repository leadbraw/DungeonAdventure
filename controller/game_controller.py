import sys
import pygame
from constants import BACKGROUND_COLOR, DARK_GREY, PILLAR_NAMES, get_fonts, OFF_WHITE, LIGHT_BLUE
from controller.gui_elements import Button
from controller.inventory_overlay import InventoryOverlay
from model.entities.inventory import Inventory
from model.factories.adventurer_factory import AdventurerFactory
from model.factories.monster_factory import MonsterFactory
from model.factories.item_factory import ItemFactory
from model.managers.room_manager import RoomManager
from model.managers.monster_manager import MonsterManager
from model.managers.adventurer_manager import AdventurerManager
from model.managers.item_manager import ItemManager
from model.dungeon.dungeon import Dungeon
from model.managers.sprite_manager import SpriteManager  # Import SpriteManager

class GameController:
    def __init__(self, screen, hero_name):
        self.screen = screen
        self.hero_name = hero_name
        self.room_manager = RoomManager.get_instance()
        self.monster_manager = MonsterManager.get_instance()
        self.item_manager = ItemManager.get_instance()
        self.adventurer_manager = AdventurerManager.get_instance()
        self.sprite_manager = SpriteManager.get_instance()
        self.dungeon = []  # List of floors
        self.current_floor = 1
        self.position = None
        self.active_adventurer = None
        self.current_message = None
        self.fonts = get_fonts()  # Dictionary of fonts

        self.set_active_adventurer(hero_name)


    def initialize_dungeon(self):
        """Creates all four floors of the dungeon."""
        '''Create and populate the dungeon.'''
        self.dungeon = [Dungeon(1), Dungeon(2), Dungeon(3), Dungeon(4)]  # Updated reference
        print("Dungeon Generated:")
        print(self.dungeon[0])

        for i in range(4):
            # Populate rooms with monsters and items
            all_rooms = self.dungeon[i].get_room_list()  # List of room coordinates
            monster_rooms = [
                coords
                for coords in all_rooms
                if self.dungeon[i].fetch_room(coords[0], coords[1]).type == 'MONSTER'
            ]
            elite_rooms = [
                coords
                for coords in all_rooms
                if self.dungeon[i].fetch_room(coords[0], coords[1]).type == 'ELITE'
            ]
            item_rooms = [
                coords
                for coords in all_rooms
                if self.dungeon[i].fetch_room(coords[0], coords[1]).type == 'ITEM'
            ]

            # Place monsters in designated MONSTER rooms
            for room_coords in monster_rooms:
                raw_data = self.monster_manager.get_monster_data(monster_type="Normal")
                if raw_data:
                    raw_data_sliced = raw_data[1:]  # Skip the entry ID
                    try:
                        monster = MonsterFactory.get_instance().make_monster(raw_data_sliced)
                        if monster:
                            self.dungeon[i].fetch_room(room_coords[0], room_coords[1]).set_monster(monster)
                            print(f"Placed {monster.name} in a MONSTER room at {room_coords}.")
                        else:
                            print(f"Failed to place monster in room at {room_coords}: Monster creation failed.")
                    except ValueError as e:
                        print(f"Error creating monster: {e}")
                else:
                    print(f"No monster data available for room at {room_coords}.")

            # Place elite monsters in designated ELITE rooms
            for room_coords in elite_rooms:
                raw_data = self.monster_manager.get_monster_data(monster_type="Elite")
                if raw_data:
                    raw_data_sliced = raw_data[1:]  # Skip the entry ID
                    try:
                        elite_monster = MonsterFactory.get_instance().make_monster(raw_data_sliced)
                        if elite_monster:
                            self.dungeon[i].fetch_room(room_coords[0], room_coords[1]).set_monster(elite_monster)
                            print(f"Placed {elite_monster.name} in an ELITE room at {room_coords}.")
                        else:
                            print(f"Failed to place elite monster in room at {room_coords}: Monster creation failed.")
                    except ValueError as e:
                        print(f"Error creating elite monster: {e}")
                else:
                    print(f"No elite monster data available for room at {room_coords}.")

            # Place items in designated ITEM rooms
            for room_coords in item_rooms:
                raw_data = self.item_manager.get_random_consumable_item_data()
                if raw_data:
                    item = ItemFactory.get_instance().create_item_from_raw(raw_data)
                    if item:
                        self.dungeon[i].fetch_room(room_coords[0], room_coords[1]).set_item(item)
                        print(f"Placed {item.get_name()} in an ITEM room at {room_coords}.")
                    else:
                        print(f"Failed to place item in room at {room_coords}: Item creation failed.")

            # Place a unique pillar in a designated room
            pillar_coords = all_rooms[2]  # Pillar room is always the third room in the floor's room_list
            raw_data = self.item_manager.get_unique_item_data()
            if raw_data:
                pillar_item = ItemFactory.get_instance().create_unique_item(raw_data)
                self.dungeon[i].fetch_room(pillar_coords[0], pillar_coords[1]).set_item(pillar_item)
                print(f"Placed {pillar_item.get_name()} in a PILLAR room at {pillar_coords}.")
            else:
                print(f"Failed to place pillar in room at {pillar_coords}: No pillar available.")

        # Set the initial player position
        self.position = self.dungeon[0].entrance_loc
        # Use of asterisk is to unpack the self.position tuple and treat each member as a different arg.
        self.dungeon[0].fetch_room(*self.position).set_visited(True)
        print(f"Player starting position: {self.position}")

    def display_game(self):
        """Main gameplay loop."""
        while True:
            self.screen.fill(DARK_GREY)

            # Fetch the current room's sprite
            current_room = self.dungeon[self.current_floor - 1].fetch_room(self.position[0], self.position[1])
            room_doors = current_room.valid_directions  # List of four booleans (top, right, bottom, left)
            sprite_config = self.room_manager.get_room_by_doors(
                room_doors)  # Get room sprite and rotation from RoomManager

            # Render the current room's sprite
            if sprite_config and "sprite_name" in sprite_config and "rotation" in sprite_config:
                sprite_name, rotation = sprite_config["sprite_name"], sprite_config["rotation"]
                room_sprite = self.sprite_manager.get_transformed_sprite(sprite_name, rotate=rotation)

                if room_sprite:
                    x = (650 - room_sprite.get_width()) // 2  # Center within 650px
                    y = 0  # Top of the screen
                    self.screen.blit(room_sprite, (x, y))
                else:
                    print(f"[GameController] Failed to render sprite '{sprite_name}' with rotation {rotation}.")
            else:
                print(f"[GameController] Invalid sprite config for room doors {room_doors}: {sprite_config}")

            # Draw game UI and map
            self.draw_ui()
            map = pygame.transform.scale(self.dungeon[self.current_floor - 1].create_map(), (150, 150))
            self.screen.blit(map, (650, 0))

            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    self.player_movement(event.key)

            pygame.display.flip()

    def player_movement(self, key):
        """Handles player movement based on arrow key input."""
        # Map keys to movement directions and their corresponding indices in valid_directions
        direction_map = {
            pygame.K_UP: (-1, 0),  # Up
            pygame.K_RIGHT: (0, 1),  # Right
            pygame.K_DOWN: (1, 0),  # Down
            pygame.K_LEFT: (0, -1)  # Left
        }
        direction_indices = {
            pygame.K_UP: 0,  # Up corresponds to index 0
            pygame.K_RIGHT: 1,  # Right corresponds to index 1
            pygame.K_DOWN: 2,  # Down corresponds to index 2
            pygame.K_LEFT: 3  # Left corresponds to index 3
        }

        if key in direction_map:
            dx, dy = direction_map[key]
            direction_index = direction_indices[key]

            # Get the current room and check valid directions
            current_room = self.dungeon[self.current_floor - 1].fetch_room(self.position[0], self.position[1])
            if current_room.valid_directions[direction_index]:
                # Update the position if the direction is valid
                new_position = (self.position[0] + dx, self.position[1] + dy)
                self.position = new_position
                self.room_interaction()
            else:

                message = "Invalid move: No valid path in that direction."
                self.draw_ui(message)
                pygame.display.flip()
                pygame.time.delay(1000)

    def room_interaction(self):
        """Interact with the current room."""
        current_room = self.dungeon[self.current_floor - 1].fetch_room(self.position[0], self.position[1])
        message = f"Entered the {current_room.type} room at {self.position}"

        if current_room.type == "MONSTER" and current_room.has_monster():
            monster = current_room.get_monster()
            message = f"Oh no! A wild {monster.name} appears! Prepare for battle!"
            current_room.set_visited(True)
            self.draw_ui(message)
            pygame.display.flip()
            pygame.time.delay(2000)
            self.start_battle(monster)  # Start the battle

        elif current_room.type == "ITEM" and current_room.has_item():
            item = current_room.get_item()
            message = f"You found a {item.get_name()}!"

            # Special handling for Pillar items
            if item.get_name().startswith("Pillar"):
                message += f" The {item.get_name()} grants you its power!"
                self.active_adventurer.inventory._apply_effect_to_adventurer(
                    {
                        "name": item.get_name(),
                        "buff_type": item.get_buff_type(),
                        "effect_min": item.get_effect_min(),
                        "effect_max": item.get_effect_max(),
                    },
                    self.active_adventurer,
                    item.get_effect_min(),
                    item.get_effect_max(),
                )
                current_room.item = None
            else:
                # Add the item to the inventory if it's not a Pillar
                if self.active_adventurer.inventory.add_item(item):
                    message += f" {item.get_name()} added to your inventory."
                    current_room.item = None
                else:
                    message += f" Your inventory is full! Unable to pick up {item.get_name()}."

            self.draw_ui(message)
            pygame.display.flip()

        elif current_room.type == "EXIT":
            current_room.set_visited(True)
            if self.current_floor == len(self.dungeon):
                message = "You found the exit! Congratulations!"
                self.draw_ui(message)
                pygame.display.flip()
                pygame.time.delay(3000)
                pygame.quit()
                sys.exit()
            else:
                message = f"You have completed floor {self.current_floor}! Proceeding to the next floor."
                self.draw_ui(message)
                pygame.display.flip()
                pygame.time.delay(2000)
                self.current_floor += 1
                self.position = self.dungeon[self.current_floor - 1].entrance_loc
                self.dungeon[self.current_floor - 1].fetch_room(*self.position).set_visited(True)
                message = f"Entering floor {self.current_floor} at position {self.position}."
                self.draw_ui(message)
                pygame.display.flip()

        elif current_room.type == "ENTRANCE":
            message = "You are back at the entrance."
            self.draw_ui(message)
            pygame.display.flip()

        elif current_room.type == "PILLAR" and current_room.has_item():
            pillar = current_room.get_item()
            message = f"You've found the {pillar.get_name()}! Wow!"
            current_room.item = None
            self.draw_ui(message)
            pygame.display.flip()

        elif current_room.type == "EMPTY":
            message = "You've found an empty room. It smells in here."
            self.draw_ui(message)
            pygame.display.flip()

        # Mark the room as visited and display the final interaction message
        current_room.set_visited(True)
        self.draw_ui(message)
        pygame.display.flip()

    def start_battle(self, monster):
        """Starts and Handles battle action with player vs monster in the Room section."""

        adventurer = self.active_adventurer
        inventory_overlay = InventoryOverlay(self.screen, self.fonts, adventurer.inventory)

        # Define fight and item buttons
        fight_button = Button(color=LIGHT_BLUE, x=150, y=540, width=100, height=30,
                              font=self.fonts["small"], text_color=(255, 255, 255), text="Fight")
        item_button = Button(color=LIGHT_BLUE, x=350, y=540, width=100, height=30,
                             font=self.fonts["small"], text_color=(255, 255, 255), text="Use Item")

        running = True
        while running and monster.hp > 0 and adventurer.hp > 0:
            # Draw UI background
            bottom_rect = pygame.Rect(0, 450, 800, 150)
            pygame.draw.rect(self.screen, (0, 0, 0), bottom_rect)
            pygame.draw.rect(self.screen, BACKGROUND_COLOR, bottom_rect)

            portrait = self.get_hero_portrait()
            self.screen.blit(portrait, (650, 450))

            monster_text = self.fonts["small"].render(f"Monster HP: {monster.hp}", True, OFF_WHITE)
            adventurer_text = self.fonts["small"].render(f"Your HP: {adventurer.hp}", True, OFF_WHITE)
            self.screen.blit(monster_text, (50, 490))
            self.screen.blit(adventurer_text, (50, 510))

            # Draw buttons for battle actions
            fight_button.draw(self.screen)
            item_button.draw(self.screen)

            pygame.display.flip()

            # Handle player input through button clicks
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()

                    if fight_button.is_hovered(mouse_pos):
                        self.execute_fight(monster, adventurer)
                    elif item_button.is_hovered(mouse_pos):
                        # Open inventory overlay
                        inventory_overlay.display()

                        # Use the selected item if one was chosen
                        selected_item = inventory_overlay.selected_item
                        if selected_item:
                            if adventurer.inventory.use_item(selected_item, adventurer,
                                                             self.dungeon[self.current_floor - 1]):
                                print(f"You used {selected_item}.")
                                # End the turn after item use
                                continue
                            else:
                                print(f"Failed to use {selected_item}.")
                        else:
                            print("No item was selected. Returning to battle options.")

            # Exit battle if monster or adventurer is defeated
            if monster.hp <= 0 or not adventurer.is_alive():
                running = False

        # Post-battle logic
        if monster.hp <= 0:
            message = f"You defeated {monster.name}, well done!"
            self.draw_ui(message)
            pygame.display.flip()
            pygame.time.delay(2000)
            current_room = self.dungeon[self.current_floor - 1].fetch_room(self.position[0], self.position[1])
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
                            return  # Return to main menu logic
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
                self.draw_ui(message)
                pygame.display.flip()
                pygame.time.delay(2000)
            else:
                break

        if monster.hp > 0:
            message = f"{monster.name} is attacking!"
            self.draw_ui(message)
            pygame.display.flip()
            pygame.time.delay(2000)
            damage = monster.attack(adventurer)
            message = f"{monster.name} dealt {damage} damage to you."
            self.draw_ui(message)
            pygame.display.flip()
            pygame.time.delay(2000)

    def set_active_adventurer(self, adventurer_name):
        raw_data = self.adventurer_manager.get_adventurer_data(name=adventurer_name)[1:]  # Ignore entry number!
        if raw_data:
            self.active_adventurer = AdventurerFactory.get_instance().make_adventurer(raw_data)
        else:
            print(f"Adventurer '{adventurer_name}' not found.")

    def draw_ui(self, message=None):
        """Draws the game's user interface, updating the room message permanently."""
        # Draw the UI background
        bottom_rect = pygame.Rect(0, 450, 800, 150)
        right_rect = pygame.Rect(650, 0, 150, 450)
        pygame.draw.rect(self.screen, BACKGROUND_COLOR, bottom_rect)
        pygame.draw.rect(self.screen, BACKGROUND_COLOR, right_rect)

        # Draw the adventurer's portrait
        portrait = self.get_hero_portrait()
        self.screen.blit(portrait, (650, 450))

        # Draw adventurer's HP
        current_hp, max_hp = self.active_adventurer.hp, self.active_adventurer.max_hp
        hp_text = self.fonts["small"].render(f"{current_hp} / {max_hp}", True, OFF_WHITE)
        self.screen.blit(hp_text, (660, 420)) # TODO: Add hp bar, also display hp during battle as well.

        # If an interaction message is provided, update the message state
        if message:
            self.current_message = message

        # Display the current message (either room type or interaction message)
        if hasattr(self, 'current_message') and self.current_message:
            message_text = self.fonts["small"].render(self.current_message, True, OFF_WHITE)
            self.screen.blit(message_text, (50, 500))

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