import os
import sqlite3

class DatabaseInitializer:
    def __init__(self, db_path='data/dungeon_game.db'):
        """
        Initializes the DatabaseInitializer with the given database path.
        Ensures the `data` directory exists.
        :param db_path: Path to the SQLite database file.
        """
        os.makedirs(os.path.dirname(db_path), exist_ok=True)  # Ensure the 'data' directory exists
        self.db_path = db_path

    def database_exists(self):
        """
        Check if the database file exists.
        :return: True if the database file exists, False otherwise.
        """
        return os.path.exists(self.db_path)

    def initialize_database(self):
        """
        Initializes the database only if it doesn't already exist.
        """
        if not self.database_exists():
            print("Database not found. Creating and initializing...")
            self.create_tables()
            print("Database initialized successfully.")
        else:
            print("Database already exists. Skipping initialization.")

    def create_tables(self):
        """Creates all necessary tables in the database."""
        table_commands = {
            "heroes": """
                CREATE TABLE IF NOT EXISTS heroes (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    type TEXT,
                    max_HP INTEGER,
                    attack_speed INTEGER,
                    chance_to_hit REAL,
                    attack_damage_min INTEGER,
                    attack_damage_max INTEGER,
                    chance_to_block REAL,
                    special_attack TEXT
                );
            """,
            "monsters": """
                CREATE TABLE IF NOT EXISTS monsters (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    type TEXT,
                    HP INTEGER,
                    attack_speed INTEGER,
                    chance_to_hit REAL,
                    attack_min INTEGER,
                    attack_max INTEGER,
                    chance_to_heal REAL,
                    heal_range_min INTEGER,
                    heal_range_max INTEGER
                );
            """,
            "items": """
                CREATE TABLE IF NOT EXISTS items (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    description TEXT,
                    ability TEXT,
                    temporary INTEGER, -- Use INTEGER instead of BOOLEAN
                    unique_item INTEGER -- Use INTEGER instead of BOOLEAN
                );
            """,
            "rooms": """
                CREATE TABLE IF NOT EXISTS rooms (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    doors TEXT NOT NULL,
                    image_path TEXT NOT NULL,
                    rotation INTEGER NOT NULL,
                    UNIQUE(doors)
                );
            """,
            "game_saves": """
                CREATE TABLE IF NOT EXISTS game_saves (
                    id INTEGER PRIMARY KEY,
                    slot_number INTEGER UNIQUE,
                    save_name TEXT,
                    level INTEGER,
                    hero_state TEXT,
                    items_state TEXT,
                    monsters_state TEXT,
                    save_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """
        }

        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                for table, command in table_commands.items():
                    cursor.execute(command)
                conn.commit()
                print("All tables created successfully.")
        except sqlite3.Error as e:
            print(f"Error creating tables: {e}")

    def reset_database(self):
        """
        Drops and recreates all tables in the database. Useful for testing and debugging.
        """
        if self.database_exists():
            print("Resetting the database...")
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("DROP TABLE IF EXISTS heroes")
                cursor.execute("DROP TABLE IF EXISTS monsters")
                cursor.execute("DROP TABLE IF EXISTS items")
                cursor.execute("DROP TABLE IF EXISTS rooms")
                cursor.execute("DROP TABLE IF EXISTS game_saves")
            self.create_tables()
            print("Database reset successfully.")
        else:
            print("No database to reset. Creating a new one...")
            self.create_tables()


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "reset":
        print("Resetting the database...")
        db_initializer = DatabaseInitializer()
        db_initializer.reset_database()
    else:
        print("Initializing the database if it doesn't exist...")
        db_initializer = DatabaseInitializer()
        db_initializer.initialize_database()