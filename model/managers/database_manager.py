import sqlite3

class DatabaseManager:
    _instance = None  # Singleton instance

    @staticmethod
    def get_instance(db_path='data/dungeon_game.db'):
        if DatabaseManager._instance is None:
            DatabaseManager._instance = DatabaseManager(db_path)
        return DatabaseManager._instance

    def __init__(self, db_path):
        if DatabaseManager._instance is not None:
            raise Exception("This class is a singleton!")
        self.db_path = db_path
        self.connection = None
        self.cursor = None

    def connect(self):
        """Establishes a connection to the database if not already connected."""
        if not self.connection:
            self.connection = sqlite3.connect(self.db_path)
            self.cursor = self.connection.cursor()

    def execute_query(self, query, params=()):
        """Executes a SELECT query and returns the results."""
        self.connect()
        try:
            self.cursor.execute(query, params)
            result = self.cursor.fetchall()
            return result
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return []
        finally:
            self.close_connection()

    def close_connection(self):
        """Closes the database connection if open."""
        if self.connection:
            self.cursor.close()
            self.connection.close()
            self.connection = None
            self.cursor = None

    def fetch_items(self):
        """Fetches all items from the items table."""
        query = """
        SELECT id, name, description, ability, one_time_item
        FROM items
        """
        return self.execute_query(query)

    def fetch_rooms(self):
        """Fetches all room configurations from the rooms table."""
        query = """
        SELECT doors, image_path, rotation
        FROM rooms
        """
        return self.execute_query(query)

    def fetch_monsters(self):
        query = """
        SELECT id, name, type, max_HP, attack_speed, chance_to_hit, 
               attack_damage_min, attack_damage_max, chance_to_heal,
               heal_range_min, heal_range_max
        FROM monsters
        """
        monsters = self.execute_query(query)
        print(f"DatabaseManager: Fetched {len(monsters)} monsters.")
        return monsters

    def fetch_adventurers(self):
        """Fetches all adventurers from the adventurers table."""
        query = """
        SELECT id, name, type, max_hp, attack_speed, chance_to_hit,
                attack_damage_min, attack_damage_max, chance_to_block
        FROM adventurers
        """
        return self.execute_query(query)