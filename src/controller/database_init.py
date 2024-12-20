import os
import sqlite3


class DatabaseInitializer:
    """Responsible for initializing the database."""

    def __init__(self, db_name='dungeon_game.db'):
        """
        Initializes the DatabaseInitializer with the given database name.
        Ensures the `data` directory exists and uses an absolute path for compatibility.
        :param db_name: Name of the SQLite database file.
        """
        # Define an absolute path for the database in the 'data' directory
        project_root = os.path.dirname(os.path.abspath(__file__))
        data_dir = os.path.join(project_root, '../../../data')
        os.makedirs(data_dir, exist_ok=True)
        self.db_path = os.path.join(data_dir, db_name)

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
            self.create_tables()
        else:
            pass

    def create_tables(self):
        """Creates all necessary tables in the database."""
        table_commands = {
            "adventurers": """
                CREATE TABLE IF NOT EXISTS adventurers (
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
                    max_HP INTEGER,
                    attack_speed INTEGER,
                    chance_to_hit REAL,
                    attack_damage_min INTEGER,
                    attack_damage_max INTEGER,
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
                    target TEXT NOT NULL,
                    one_time_item INTEGER, -- Need to use INTEGER instead of BOOLEAN
                    effect_min INTEGER,
                    effect_max INTEGER,
                    buff_type TEXT
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
            """
        }

        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                for table, command in table_commands.items():
                    cursor.execute(command)
                conn.commit()
        except sqlite3.Error as e:
            print(f"Error creating tables: {e}")

    def reset_database(self):
        """
        Drops and recreates all tables in the database. Useful for testing and debugging.
        """
        if self.database_exists():
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("DROP TABLE IF EXISTS adventurers")
                cursor.execute("DROP TABLE IF EXISTS monsters")
                cursor.execute("DROP TABLE IF EXISTS items")
                cursor.execute("DROP TABLE IF EXISTS rooms")
            self.create_tables()
        else:
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