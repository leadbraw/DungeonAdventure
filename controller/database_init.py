import os
import sqlite3

class DatabaseInitializer:
    def __init__(self, db_path='data/dungeon_game.db'):
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.db_path = db_path

    def create_tables(self):
        """Creates all necessary tables in the database with error handling."""
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
                    temporary BOOLEAN,
                    unique BOOLEAN
                );
            """,
            "door_configurations": """
                CREATE TABLE IF NOT EXISTS door_configurations (
                    id INTEGER PRIMARY KEY,
                    door_north BOOLEAN NOT NULL,
                    door_east BOOLEAN NOT NULL,
                    door_south BOOLEAN NOT NULL,
                    door_west BOOLEAN NOT NULL
                );
            """,
            "room_types": """
                CREATE TABLE IF NOT EXISTS room_types (
                    id INTEGER PRIMARY KEY,
                    room_type TEXT NOT NULL
                );
            """,
            "room_configurations": """
                CREATE TABLE IF NOT EXISTS room_configurations (
                    id INTEGER PRIMARY KEY,
                    room_type_id INTEGER,
                    door_configuration_id INTEGER,
                    sprite_path TEXT NOT NULL,
                    FOREIGN KEY (room_type_id) REFERENCES room_types(id),
                    FOREIGN KEY (door_configuration_id) REFERENCES door_configurations(id)
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
                    try:
                        print(f"Creating table: {table}")
                        cursor.execute(command)
                    except sqlite3.Error as e:
                        print(f"Error creating table {table}: {e}")
                conn.commit()
            print("All tables created successfully.")
        except sqlite3.Error as e:
            print(f"Database connection error: {e}")

    def initialize_database(self):
        """Run the database initialization process with error handling."""
        print("Starting database initialization...")
        try:
            self.create_tables()
            print("Database setup complete.")
        except Exception as e:
            print(f"Error during database initialization: {e}")

if __name__ == "__main__":
    initializer = DatabaseInitializer()
    initializer.initialize_database()