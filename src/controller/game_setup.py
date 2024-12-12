from src.controller.database_init import DatabaseInitializer
from src.model.managers.item_manager import ItemManager
from src.model.managers.room_manager import RoomManager
from src.model.managers.monster_manager import MonsterManager
from src.model.managers.adventurer_manager import AdventurerManager
from src.model.managers.sprite_manager import SpriteManager
from assets.seeders.adventurer_seeder import AdventurerSeeder
from assets.seeders.item_seeder import ItemSeeder
from assets.seeders.monster_seeder import MonsterSeeder
from assets.seeders.room_seeder import RoomSeeder
from src.model.managers.database_manager import DatabaseManager
from constants import SPRITE_PATHS


class GameSetup:
    """Responsible for setting up the game."""

    def __init__(self):
        """Constructor. Instantiates fields (does not assign values)."""
        self.item_manager = None
        self.room_manager = None
        self.monster_manager = None
        self.adventurer_manager = None
        self.sprite_manager = None

    def setup(self):
        """
        Sets up the game. Responsible for calling the database initializer,
        fetching data, and instantiating all managers.

        :return: A tuple containing (in order) The item, room, monster, adventurer, and sprite managers.
        """
        # Step 1: Initialize the DatabaseInitializer
        db_initializer = DatabaseInitializer()

        # Step 2: Check if the database exists
        if not db_initializer.database_exists():
            db_initializer.initialize_database()
        else:
            db_initializer.reset_database()

        # Step 3: Run seeders to populate the database
        AdventurerSeeder().populate_adventurers()
        ItemSeeder().populate_items()
        MonsterSeeder().populate_monsters()
        RoomSeeder().populate_rooms()

        # Step 4: Fetch data from the database
        db_manager = DatabaseManager.get_instance()
        db_manager.connect()
        items_data = db_manager.fetch_items()
        rooms_data = db_manager.fetch_rooms()
        monsters_data = db_manager.fetch_monsters()
        adventurers_data = db_manager.fetch_adventurers()
        db_manager.close_connection()

        # Step 5: Initialize managers with the fetched data
        self.item_manager = ItemManager.get_instance(items_data)
        self.room_manager = RoomManager.get_instance(rooms_data)
        self.monster_manager = MonsterManager.get_instance(monsters_data)
        self.adventurer_manager = AdventurerManager.get_instance(adventurers_data)

        # Step 6: Initialize SpriteManager and preload sprites
        self.sprite_manager = SpriteManager.get_instance()
        self.sprite_manager.preload_sprites(SPRITE_PATHS)

        return (
            self.item_manager,
            self.room_manager,
            self.monster_manager,
            self.adventurer_manager,
            self.sprite_manager,
        )
