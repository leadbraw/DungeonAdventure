import sys
import pygame
from constants import BACKGROUND_COLOR, DARK_GREY, PILLAR_NAMES
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
                raw_data = self.monster_manager.get_monster_data(monster_type="Normal")[1:] # Ignore entry number!
                monster = MonsterFactory.get_instance().make_monster(raw_data)
                if monster:
                    self.dungeon[i].fetch_room(room_coords[0], room_coords[1]).set_monster(monster)
                    print(f"Placed {monster.name} in a MONSTER room at {room_coords}.")
                else:
                    print(f"Failed to place monster in room at {room_coords}: No monster available.")

            # Place elite monsters in designated ELITE rooms
            for room_coords in elite_rooms:
                raw_data = self.monster_manager.get_monster_data(monster_type="Elite")[1:] # Ignore entry number!
                elite_monster = MonsterFactory.get_instance().make_monster(raw_data)
                if elite_monster:
                    self.dungeon[i].fetch_room(room_coords[0], room_coords[1]).set_monster(elite_monster)
                    print(f"Placed {elite_monster.name} in an ELITE room at {room_coords}.")
                else:
                    print(f"Failed to place elite monster in room at {room_coords}: No monster available.")

            # Place items in designated ITEM rooms
            for room_coords in item_rooms:
                raw_data = self.item_manager.get_item_data()
                item = ItemFactory.get_instance().create_item_from_raw(raw_data)
                if item:
                    self.dungeon[i].fetch_room(room_coords[0], room_coords[1]).set_item(item)
                    print(f"Placed {item.get_name()} in an ITEM room at {room_coords}.")
                else:
                    print(f"Failed to place item in room at {room_coords}: No item available.")
            pillar = PILLAR_NAMES[i]
            pillar_coords = all_rooms[2]  # Pillar room is always the third room in the floor's room_list
            raw_data = self.item_manager.get_item_data(item_name=pillar)
            if raw_data:
                pillar_item = ItemFactory.get_instance().create_unique_item(raw_data)
                self.dungeon[i].fetch_room(pillar_coords[0], pillar_coords[1]).set_item(pillar_item)
                print(f"Placed {pillar_item.get_name()} in a PILLAR room at {pillar_coords}.")
            else:
                print(f"Failed to place pillar in room at {pillar_coords}: No pillar available.")
        # Set the initial player position
        self.position = self.dungeon[0].entrance_loc
        print(f"Player starting position: {self.position}")

    def display_game(self):
        """Main gameplay loop."""
        while True:
            self.screen.fill(DARK_GREY)

            # Draw game UI
            self.draw_ui()

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
                self.room_interaction()
            else:
                print("Invalid move: No valid path in that direction.")

    def room_interaction(self):
        """Interact with the current room."""
        current_room = self.dungeon[self.current_floor - 1].fetch_room(self.position[0], self.position[1])
        print(f"Entered room at {self.position}: {current_room.type}")

        if current_room.type == "MONSTER" and current_room.has_monster():
            monster = current_room.get_monster()
            self.start_battle(current_room.get_monster())

        elif current_room.type == "ITEM" and current_room.has_item():
            item = current_room.get_item()
            print(f"You found a {item.get_name()}!")
            current_room.item = None

        elif current_room.type == "EXIT":

            if self.current_floor == len(self.dungeon):
                print("You found the exit! Congratulations!")
                pygame.quit()
                sys.exit()
            else:
                print(f"You have completed floor {self.current_floor}! Proceeding to the next floor.")
                self.current_floor += 1
                self.position = self.dungeon[self.current_floor - 1].entrance_loc
                print(f"Entering floor {self.current_floor} at position {self.position}.")

        elif current_room.type == "ENTRANCE":
            print("You are back at the entrance.")

        elif current_room.type == "PILLAR" and current_room.has_item():
            pillar = current_room.get_item()
            print(f"You've found the {pillar}! Wow!")
            current_room.item = None

        elif current_room.type == "EMPTY":
            print("You've found an empty room. It smells in here.")

    def start_battle(self, monster):
        """Starts and Handles battle action with player vs monster"""
        print(f"A wild {monster.name} appears! Prepare for battle!")

        if not self.active_adventurer:
            print("No adventurer is active. Please select one.")
            return

        adventurer = self.active_adventurer
        while monster.hp > 0 and adventurer.hp > 0:
            print(f"Monster HP: {monster.hp}")
            print(f"Your HP: {adventurer.hp}")
            print("What are you going to do?:")
            print("1. Are you going to Fight")
            print("2. Are you going to use Item")
            # TODO: Get user choice/print info to GUI, not console
            # get the player input
            action = input("Enter 1 to Fight or 2 to use Item: ").strip()

            if action == "1": # player chooses to fight the monster
                # TODO: attack() in adventurer handles the attack speed calculations itself.
                player_turns = adventurer.attack_speed // monster.attack_speed
                #Ensure at least 1 attack
                if player_turns == 0:
                    player_turns = 1

                for turn in range(player_turns):
                    # if monster still alive
                    # TODO: use .is_alive() for clarity
                    if monster.hp > 0:
                        damage = adventurer.attack(monster)
                        print(f"You attacked and dealt {damage} damage to {monster.name}.")

                    else:
                        break

                #Use item
            elif action == "2":
                # TODO: Implement item uses/effects
                if adventurer.use_item():
                    print(f"You used {adventurer.use_item.get_name}.")
                else:
                    print("You don't have any usable items, Bummer.")

            else:
                print("Invalid action, please choose again.")
                # retry
                continue

            # now the monster turn
            if monster.hp > 0:
                print(f"{monster.name} is attacking!")
                damage = monster.attack(adventurer)
                print(f"{monster.name} dealt {damage} damage to you.")

        #check outcome of battle
        if monster.hp <= 0:
            print(f"You defeated {monster.name}, Well done!")
            current_room = self.dungeon[self.current_floor - 1].fetch_room(self.position[0], self.position[1])
            #clear monster from room
            current_room.set_monster(None)

        elif adventurer.hp <= 0:
            print("Your were defeated, GAME OVER:(")
            pygame.quit()
            sys.exit()

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
        room_text = pygame.font.Font(None, 30).render(
            f"Room: {current_room.type}", True, (255, 255, 255)
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