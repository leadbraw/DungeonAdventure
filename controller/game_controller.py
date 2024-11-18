import sys
import pygame
from constants import BACKGROUND_COLOR, DARK_GREY
from model.managers.room_manager import RoomManager
from model.managers.monster_manager import MonsterManager
from model.managers.item_manager import ItemManager
from model.dungeon.Dungeon import Dungeon

class GameController:
    def __init__(self, screen, hero_name):
        self.screen = screen
        self.hero_name = hero_name
        self.room_manager = RoomManager.get_instance()
        self.monster_manager = MonsterManager.get_instance()
        #self.item_manager = ItemManager.get_instance()
        self.dungeon = None
        self.position = None

    def initialize_dungeon(self):
        """Create and populate the dungeon."""
        self.dungeon = Dungeon(floor_number=1)  # Updated reference
        print("Dungeon Generated:")
        print(self.dungeon)

        # Populate rooms with monsters and items
        all_rooms = self.dungeon.get_room_list() # get_room_list returns a list of tuples that are room coordinates
        monster_rooms = [
            coords
            for coords in all_rooms
            if self.dungeon.fetch_room(coords[0], coords[1]).type == 'MONSTER']

        item_rooms = [
            coords
            for coords in all_rooms
            if self.dungeon.fetch_room(coords[0], coords[1]).type == 'ITEM']
        #


        for room_coords in monster_rooms:
           monster = self.monster_manager.get_random_monster()
           if monster:
               self.dungeon.fetch_room(room_coords[0], room_coords[1]).set_monster(monster)
               print(f"Placed {monster.name()} in a MONSTER room at {room_coords}.") # TODO: fix error here!
           else:
               print(f"Failed to place monster in room at {room_coords}: No monster available.")



        #
        for room in item_rooms:
           item = self.item_manager.get_random_non_unique_item()
           self.dungeon.fetch_room(room_coords[0], room_coords[1]).set_item(item)
           print(f"Placed {item.get_name()} in an ITEM room at {room_coords}.")


        # get entrance position
        self.position = self.dungeon.entrance_loc
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
        """Handles player movement based on arrow key input"""
        direction_map = {
            pygame.K_UP: (-1, 0),
            pygame.K_DOWN: (1, 0),
            pygame.K_LEFT: (0, -1),
            pygame.K_RIGHT: (0, 1)
        }
        if key in direction_map:
            dx, dy = direction_map[key]
            new_position = (self.position[0] + dx, self.position[1] + dy)

            #Check if the new position is valid
            if self.dungeon.is_valid_room(new_position):
                self.position = new_position
                self.room_interaction()

    def room_interaction(self):
        """Interact with the current room"""
        current_room = self.dungeon.fetch_room(self.position[0], self.position[1])
        print(f"Entered room at {self.position}: {current_room.type}")

        if current_room.type == "MONSTER" and current_room.has_monster():
            monster = current_room.get_monster()
            print(f"A wild {monster.get_name()}appears! Prepare for battle!")
        elif current_room.type == "ITEM" and current_room.has_item():
            item = current_room.get_item()
            print(f"You found a {item.get_name}!")
        elif current_room.type == "EXIT":
            print("You found the exit! Congratulations!")
        elif current_room.type == "ENTRANCE":
            print("You are back at the entrance.")

    def draw_ui(self):
        """Draws the game's user interface"""
        bottom_rect = pygame.Rect(0, 450, 800, 150)
        right_rect = pygame.Rect(650, 0, 150, 450)
        pygame.draw.rect(self.screen, BACKGROUND_COLOR, bottom_rect)
        pygame.draw.rect(self.screen, BACKGROUND_COLOR, right_rect)

        portrait = self.get_hero_portrait()
        self.screen.blit(portrait, (650, 450))

        #Display the current room type
        current_room = self.dungeon.fetch_room(self.position[0], self.position[1])
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



