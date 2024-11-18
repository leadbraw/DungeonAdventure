from controller.database_init import DatabaseInitializer
from model.managers.item_manager import ItemManager
from model.managers.room_manager import RoomManager
from model.managers.monster_manager import MonsterManager
from model.managers.adventurer_manager import AdventurerManager
from controller.seeders.hero_seeder import HeroSeeder
from controller.seeders.item_seeder import ItemSeeder
from controller.seeders.monster_seeder import MonsterSeeder
from controller.seeders.room_seeder import RoomSeeder
from model.managers.database_manager import DatabaseManager


class GameSetup:
    def __init__(self):
        self.item_manager = None
        self.room_manager = None
        self.monster_manager = None
        self.adventurer_manager = None

    def setup(self):
        # Step 1: Initialize the DatabaseInitializer
        db_initializer = DatabaseInitializer()

        # Step 2: Check if the database exists
        if not db_initializer.database_exists():
            print("Database does not exist. Initializing it...")
            db_initializer.initialize_database()
        else:
            print("Database exists. Resetting it...")
            db_initializer.reset_database()

        # Step 3: Run seeders to populate the database
        print("Populating the database with seeders...")
        HeroSeeder().populate_heroes()
        ItemSeeder().populate_items()
        MonsterSeeder().populate_monsters()
        RoomSeeder().populate_rooms()

        # Step 4: Fetch data from the database
        print("Fetching data for managers...")
        db_manager = DatabaseManager.get_instance()
        db_manager.connect()
        items_data = db_manager.fetch_items()
        rooms_data = db_manager.fetch_rooms()
        monsters_data = db_manager.fetch_monsters()
        adventurers_data = db_manager.fetch_adventurers()  # Fetch adventurer data
        db_manager.close_connection()

        # Step 5: Initialize managers with the fetched data
        print("Initializing managers...")
        self.item_manager = ItemManager.get_instance(items_data)
        self.room_manager = RoomManager.get_instance(rooms_data)
        self.monster_manager = MonsterManager.get_instance(monsters_data)
        self.adventurer_manager = AdventurerManager.get_instance(adventurers_data)

        print("Game setup complete!")
        return self.item_manager, self.room_manager, self.monster_manager, self.adventurer_manager
