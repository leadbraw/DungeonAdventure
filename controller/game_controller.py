import sys
import pygame
from constants import BACKGROUND_COLOR, DARK_GREY, PILLAR_NAMES, get_fonts, OFF_WHITE
from controller.gui_elements import Button
from model.factories.adventurer_factory import AdventurerFactory
from model.factories.monster_factory import MonsterFactory
from model.factories.item_factory import ItemFactory
from model.managers.room_manager import RoomManager
from model.managers.monster_manager import MonsterManager
from model.managers.adventurer_manager import AdventurerManager
from model.managers.item_manager import ItemManager
from model.dungeon.Dungeon import Dungeon


class GameController:
    def __init__(self, screen, hero_name):
        self.screen = screen
        self.hero_name = hero_name
        self.room_manager = RoomManager.get_instance()
        self.monster_manager = MonsterManager.get_instance()
        self.item_manager = ItemManager.get_instance()
        # print(f"Adventurers data passed to AdventurerManager: {adventurers_data}")
        self.adventurer_manager = AdventurerManager.get_instance()
        self.dungeon = []  # List of floors
        self.current_floor = 1
        self.position = None
        self.active_adventurer = None
        self.fonts = get_fonts() # dict of fonts

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
                raw_data = self.monster_manager.get_monster_data(monster_type="Normal")[1:] # Ignore entry ID!
                monster = MonsterFactory.get_instance().make_monster(raw_data)
                if monster:
                    self.dungeon[i].fetch_room(room_coords[0], room_coords[1]).set_monster(monster)
                    print(f"Placed {monster.name} in a MONSTER room at {room_coords}.")
                else:
                    print(f"Failed to place monster in room at {room_coords}: No monster available.")

            # Place elite monsters in designated ELITE rooms
            for room_coords in elite_rooms:
                raw_data = self.monster_manager.get_monster_data(monster_type="Elite")[1:] # Ignore entry ID!
                elite_monster = MonsterFactory.get_instance().make_monster(raw_data)
                if elite_monster:
                    self.dungeon[i].fetch_room(room_coords[0], room_coords[1]).set_monster(elite_monster)
                    print(f"Placed {elite_monster.name} in an ELITE room at {room_coords}.")
                else:
                    print(f"Failed to place elite monster in room at {room_coords}: No monster available.")

            # Place items in designated ITEM rooms
            for room_coords in item_rooms:
                raw_data = self.item_manager.get_random_consumable_item_data()[1:]
                item = ItemFactory.get_instance().create_item_from_raw(raw_data)
                if item:
                    self.dungeon[i].fetch_room(room_coords[0], room_coords[1]).set_item(item)
                    print(f"Placed {item.get_name()} in an ITEM room at {room_coords}.")
                else:
                    print(f"Failed to place item in room at {room_coords}: No item available.")
            pillar = PILLAR_NAMES[i]
            pillar_coords = all_rooms[2]  # Pillar room is always the third room in the floor's room_list
            raw_data = self.item_manager.get_unique_item_data(item_name=pillar)[1:] # Ignore entry ID!
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

            # Draw game UI
            self.draw_ui()

            # Draw map
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
                print(f"Moved to new position: {self.position}")
                self.draw_ui()
                self.room_interaction()
            else:
                print("Invalid move: No valid path in that direction.")

    def room_interaction(self):
        """Interact with the current room."""
        current_room = self.dungeon[self.current_floor - 1].fetch_room(self.position[0], self.position[1])
        print(f"Entered room at {self.position}: {current_room.type}")

        if current_room.type == "MONSTER" and current_room.has_monster():
            monster = current_room.get_monster()
            current_room.set_visited(True)
            self.start_battle(current_room.get_monster())

        elif current_room.type == "ITEM" and current_room.has_item():
            item = current_room.get_item()
            print(f"You found a {item.get_name()}!")
            current_room.item = None

        elif current_room.type == "EXIT":
            current_room.set_visited(True)
            if self.current_floor == len(self.dungeon):
                print("You found the exit! Congratulations!")
                pygame.quit()
                sys.exit()
            else:
                print(f"You have completed floor {self.current_floor}! Proceeding to the next floor.")
                self.current_floor += 1
                self.position = self.dungeon[self.current_floor - 1].entrance_loc
                self.dungeon[self.current_floor - 1].fetch_room(*self.position).set_visited(True)
                print(f"Entering floor {self.current_floor} at position {self.position}.")

        elif current_room.type == "ENTRANCE":
            print("You are back at the entrance.")

        elif current_room.type == "PILLAR" and current_room.has_item():
            pillar = current_room.get_item()
            print(f"You've found the {pillar.get_name()}! Wow!")
            current_room.item = None

        elif current_room.type == "EMPTY":
            print("You've found an empty room. It smells in here.")

        current_room.set_visited(True)

    def start_battle(self, monster):
        """Starts and Handles battle action with player vs monster in the Room section."""
        print(f"A wild {monster.name} appears! Prepare for battle!")

        adventurer = self.active_adventurer

        # Define the black section coordinates (adjust these based on your layout)
        room_section_x = 0
        room_section_y = 450
        room_section_width = 800
        room_section_height = 150

        # Define fight and item buttons in the room section
        fight_button = Button(color=(0, 255, 0), x=150, y=room_section_y + 70, width=100, height=30,
                              font=self.fonts["small"], text_color=(255, 255, 255), text="Fight")
        item_button = Button(color=(0, 0, 255), x=350, y=room_section_y + 70, width=100, height=30,
                             font=self.fonts["small"], text_color=(255, 255, 255), text="Use Item")

        running = True
        while running and monster.hp > 0 and adventurer.hp > 0:
            # Clear screen
            self.screen.fill(DARK_GREY)

            # Restore the mini-map
            map = pygame.transform.scale(self.dungeon[self.current_floor - 1].create_map(), (150, 150))
            self.screen.blit(map, (650, 0))

            # Restore the adventurer portrait
            portrait = self.get_hero_portrait()
            portrait_position = (650, 450)  # Fixed position for the portrait
            self.screen.blit(portrait, portrait_position)

            # Draw the black section as the battle UI
            room_rect = pygame.Rect(room_section_x, room_section_y, room_section_width, room_section_height)
            pygame.draw.rect(self.screen, (0, 0, 0), room_rect)  # True black background

            # Update "Room:" text to reflect the monster room
            room_text = self.fonts["small"].render(f"Room: MONSTER", True, OFF_WHITE)
            self.screen.blit(room_text, (10, room_section_y + 10))

            # Draw monster and adventurer stats in the black section
            monster_text = self.fonts["small"].render(f"Monster HP: {monster.hp}", True, OFF_WHITE)
            adventurer_text = self.fonts["small"].render(f"Your HP: {adventurer.hp}", True, OFF_WHITE)
            self.screen.blit(monster_text, (10, room_section_y + 40))
            self.screen.blit(adventurer_text, (10, room_section_y + 60))

            # Draw buttons in the black section
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
                        self.use_item(adventurer)

                # Exit battle if monster or adventurer is defeated
                if monster.hp <= 0 or adventurer.hp <= 0:
                    running = False

        # Check battle outcome
        if monster.hp <= 0:
            print(f"You defeated {monster.name}, Well done!")
            current_room = self.dungeon[self.current_floor - 1].fetch_room(self.position[0], self.position[1])
            current_room.set_monster(None)  # Clear monster from the room
        elif adventurer.hp <= 0:
            print("You were defeated, GAME OVER :(")
            pygame.quit()
            sys.exit()

    def execute_fight(self, monster, adventurer):
        """Handle the fight action."""
        player_turns = max(1, adventurer.attack_speed // monster.attack_speed)

        for _ in range(player_turns):
            if monster.hp > 0:
                damage = adventurer.attack(monster)
                print(f"You attacked and dealt {damage} damage to {monster.name}.")
            else:
                break

        if monster.hp > 0:
            print(f"{monster.name} is attacking!")
            damage = monster.attack(adventurer)
            print(f"{monster.name} dealt {damage} damage to you.")

    def use_item(self, adventurer):
        """Handle the use item action."""
        item = adventurer.use_item()
        if item:
            print(f"You used {item.get_name()}.")
        else:
            print("You don't have any usable items, bummer.")

    def set_active_adventurer(self, adventurer_name):
        """Switches the active adventurer."""
        raw_data = self.adventurer_manager.get_adventurer_data(name=adventurer_name)[1:] # Ignore entry number!
        if raw_data:
            self.active_adventurer = AdventurerFactory.get_instance().make_adventurer(raw_data)
        else:
            print(f"Adventurer '{adventurer_name}' not found.")

    def draw_ui(self):
        """Draws the game's user interface."""
        bottom_rect = pygame.Rect(0, 450, 800, 150)
        right_rect = pygame.Rect(650, 0, 150, 450)
        pygame.draw.rect(self.screen, BACKGROUND_COLOR, bottom_rect)
        pygame.draw.rect(self.screen, BACKGROUND_COLOR, right_rect)

        portrait = self.get_hero_portrait()
        self.screen.blit(portrait, (650, 450))

        # Display the current room type
        current_room = self.dungeon[self.current_floor - 1].fetch_room(self.position[0], self.position[1])
        room_text = self.fonts["small"].render(
            f"Room: {current_room.type}", True, OFF_WHITE
        )
        self.screen.blit(room_text, (50, 500))

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