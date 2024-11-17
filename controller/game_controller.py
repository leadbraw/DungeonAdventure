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
        # self.item_manager = ItemManager.get_instance()
        self.dungeon = None

    def initialize_dungeon(self):
        """Create and populate the dungeon."""
        self.dungeon = Dungeon(floor_number=1)  # Updated reference
        print(self.dungeon)

        # Populate rooms with monsters and items
        # all_rooms = [room for row in self.dungeon.map for room in row]
        # monster_rooms = [room for room in all_rooms if room.type == 'MONSTER']
        # item_rooms = [room for room in all_rooms if room.type == 'ITEM']
        #
        # for room in monster_rooms:
        #     monster = self.monster_manager.get_random_monster()
        #     print(f"Placed {monster.get_name()} in a MONSTER room.")
        #
        # for room in item_rooms:
        #     item = self.item_manager.get_random_non_unique_item()
        #     print(f"Placed {item.get_name()} in an ITEM room.")

        # Find entrance position
        self.position = next(
            ((r_idx, c_idx) for r_idx, row in enumerate(self.dungeon.map)
             for c_idx, room in enumerate(row) if room.type == 'ENTRANCE'), None
        )

    def display_game(self):
        """Main gameplay loop."""
        while True:
            self.screen.fill(DARK_GREY)

            # Draw game UI
            bottom_rect = pygame.Rect(0, 450, 800, 150)
            right_rect = pygame.Rect(650, 0, 150, 450)
            pygame.draw.rect(self.screen, BACKGROUND_COLOR, bottom_rect)
            pygame.draw.rect(self.screen, BACKGROUND_COLOR, right_rect)

            portrait = self.get_hero_portrait()
            self.screen.blit(portrait, (650, 450))

            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.flip()

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
