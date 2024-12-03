import sys
import pygame
from constants import BACKGROUND_COLOR, DARK_GREY, get_fonts, OFF_WHITE
from controller.battle_manager import BattleManager
from controller.dungeon_manager import DungeonManager
from model.managers.room_manager import RoomManager
from model.managers.adventurer_manager import AdventurerManager
from model.managers.sprite_manager import SpriteManager
from model.factories.adventurer_factory import AdventurerFactory

class GameController:
    def __init__(self, screen, hero_name):
        self.screen = screen
        self.hero_name = hero_name
        self.fonts = get_fonts()  # Dictionary of fonts
        self.room_manager = RoomManager.get_instance()
        self.sprite_manager = SpriteManager.get_instance()
        self.battle_manager = BattleManager.get_instance(self.screen, self.fonts, self.draw_ui)
        self.dungeon_manager = DungeonManager.get_instance()
        self.adventurer_manager = AdventurerManager.get_instance()
        self.minimap = None

        # Attributes for game state
        self.current_floor = 1
        self.position = self.dungeon_manager.get_floor_entrance(self.current_floor)  # Fetch entrance position
        self.active_adventurer = None
        self.current_message = None

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
                elif event.type == pygame.KEYDOWN:
                    self.player_movement(event.key)

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
        self.dungeon_manager.mark_room_visited(self.current_floor, self.position)

        # Handle MONSTER and ELITE rooms
        if current_room.type == "MONSTER" and current_room.has_monster():
            monster = self.dungeon_manager.get_monster_in_room(self.current_floor, self.position)
            self.display_message(f"A wild {monster.name} appears! Prepare for battle!", 2000)
            self.battle_manager.start_battle(
                adventurer=self.active_adventurer,
                monster=monster,
                dungeon=self.dungeon_manager.dungeon,  # Assuming this is the correct dungeon reference
                current_floor=self.current_floor,
                position=self.position,
                get_hero_portrait=self.get_hero_portrait, # Pass the callable here
                minimap=self.minimap
            )

        elif current_room.type == "ELITE" and current_room.has_monster():
            monster = self.dungeon_manager.get_monster_in_room(self.current_floor, self.position)
            self.display_message(f"An ELITE {monster.name} stands before you! Prepare for a tougher fight!", 2000)
            self.battle_manager.start_battle(
                adventurer=self.active_adventurer,
                monster=monster,
                dungeon=self.dungeon_manager.dungeon,  # Assuming this is the correct dungeon reference
                current_floor=self.current_floor,
                position=self.position,
                get_hero_portrait=self.get_hero_portrait,
                minimap=self.minimap # Pass the callable here
            )

        # Handle ITEM rooms
        elif current_room.type == "ITEM" and current_room.has_item():
            item = self.dungeon_manager.get_item_in_room(self.current_floor, self.position)
            if item.get_name().startswith("Pillar"):
                self.handle_pillar_item(item)
            else:
                self.handle_regular_item(item)

        # Handle EXIT rooms
        elif current_room.type == "EXIT":
            self.handle_exit_room()

        # Handle ENTRANCE rooms
        elif current_room.type == "ENTRANCE":
            self.display_message("You are back at the entrance.")

        # Handle PILLAR rooms
        elif current_room.type == "PILLAR" and current_room.has_item():
            item = self.dungeon_manager.get_item_in_room(self.current_floor, self.position)
            self.display_message(f"You've found the {item.get_name()}! Wow!")
            self.dungeon_manager.clear_item_in_room(self.current_floor, self.position)

        # Handle EMPTY rooms
        elif current_room.type == "EMPTY":
            self.display_message("You've found an empty room. It smells in here.")

    def handle_pillar_item(self, item):
        """Handles interaction with Pillar items."""
        self.display_message(f"The {item.get_name()} grants you its power!")

        # Use the existing public apply_effect method
        self.active_adventurer.inventory.apply_effect(
            {
                "name": item.get_name(),
                "buff_type": item.get_buff_type(),
                "effect_min": item.get_effect_min(),
                "effect_max": item.get_effect_max(),
                "target": "adventurer",  # Explicitly specify the target
            },
            self.active_adventurer,
            item.get_effect_min(),
            item.get_effect_max(),
        )

        self.dungeon_manager.clear_item_in_room(self.current_floor, self.position)

    def handle_regular_item(self, item):
        """Handles interaction with regular items."""
        if self.active_adventurer.inventory.add_item(item):
            self.display_message(f"{item.get_name()} added to your inventory.")
            self.dungeon_manager.clear_item_in_room(self.current_floor, self.position)
        else:
            self.display_message(f"Your inventory is full! Unable to pick up {item.get_name()}.")

    def handle_exit_room(self):
        """Handles interaction with the Exit room."""
        if self.current_floor == len(self.dungeon_manager.dungeon):
            self.display_message("You found the exit! Congratulations!", 3000)
            pygame.quit()
            sys.exit()
        else:
            self.current_floor += 1
            self.position = self.dungeon_manager.get_floor_entrance(self.current_floor)
            self.dungeon_manager.mark_room_visited(self.current_floor, self.position)
            self.display_message(f"Entering floor {self.current_floor} at position {self.position}.")

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

    def draw_ui(self, message=None):
        """Draws the game's user interface."""
        bottom_rect = pygame.Rect(0, 450, 800, 150)
        right_rect = pygame.Rect(650, 0, 150, 450)
        pygame.draw.rect(self.screen, BACKGROUND_COLOR, bottom_rect)
        pygame.draw.rect(self.screen, BACKGROUND_COLOR, right_rect)

        # Draw adventurer portrait
        portrait = self.get_hero_portrait()
        self.screen.blit(portrait, (650, 450))

        # Display adventurer HP
        current_hp, max_hp = self.active_adventurer.hp, self.active_adventurer.max_hp
        hp_text = self.fonts["small"].render(f"{current_hp} / {max_hp}", True, OFF_WHITE)
        self.screen.blit(hp_text, (660, 420))

        # Display room message
        if message:
            self.current_message = message
        if self.current_message:
            message_text = self.fonts["small"].render(self.current_message, True, OFF_WHITE)
            self.screen.blit(message_text, (50, 500))

        # Draw minimap
        self.screen.blit(self.minimap, (650, 0))

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