import sqlite3

class RoomSeeder:
    def __init__(self, db_path='data/dungeon_game.db'):
        self.db_path = db_path

    def populate_door_configurations(self):
        """Populates the door_configurations table with 24 unique entries."""
        door_data = [
            (True, True, True, True),
            (True, True, True, False),
            (True, True, False, True),
            (True, False, True, True),
            (False, True, True, True),
            (True, True, False, False),
            (True, False, True, False),
            (False, True, True, False),
            (True, False, False, True),
            (False, True, False, True),
            (False, False, True, True),
            (True, False, False, False),
            (False, True, False, False),
            (False, False, True, False),
            (False, False, False, True),
            (True, True, True, True),
            (True, True, True, False),
            (True, True, False, True),
            (True, False, True, True),
            (False, True, True, True),
            (True, False, False, False),
            (False, True, False, False),
            (False, False, True, False),
            (False, False, False, True)
        ]

        insert_query = """
            INSERT INTO door_configurations (door_north, door_east, door_south, door_west)
            VALUES (?, ?, ?, ?)
        """

        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.executemany(insert_query, door_data)
                conn.commit()
            print("Door configurations table populated.")
        except sqlite3.Error as e:
            print(f"Error populating door configurations: {e}")

    def populate_room_types(self):
        """Populates the room_types table with 10 unique room types."""
        room_types = [
            # Example room types
            ("Monster",),
            ("Boss",),
            ("Entry",),
            ("Exit Closed",),
            ("Exit Open",),
            ("Trap",),
            ("Item",),
            ("Pillar",),
            ("Solid",),
            ("Empty",)
        ]

        insert_query = "INSERT INTO room_types (room_type) VALUES (?)"

        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.executemany(insert_query, room_types)
                conn.commit()
            print("Room types table populated.")
        except sqlite3.Error as e:
            print(f"Error populating room types: {e}")

    def populate_room_configurations(self):
        """Populates the room_configurations table by combining room types and door configurations."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                # Fetch room types and door configurations
                cursor.execute("SELECT id, room_type FROM room_types")
                room_types = cursor.fetchall()

                cursor.execute("SELECT id FROM door_configurations")
                door_configs = cursor.fetchall()

                configurations_data = []
                for room_id, room_type in room_types:
                    for door_config_id in door_configs:
                        sprite_path = f"assets/sprites/{room_type}_{door_config_id[0]}.png"
                        configurations_data.append((room_id, door_config_id[0], sprite_path))

                insert_query = """
                    INSERT INTO room_configurations (room_type_id, door_configuration_id, sprite_path)
                    VALUES (?, ?, ?)
                """
                cursor.executemany(insert_query, configurations_data)
                conn.commit()
            print("Room configurations table populated.")
        except sqlite3.Error as e:
            print(f"Error populating room configurations: {e}")

    def seed_all(self):
        self.populate_door_configurations()
        self.populate_room_types()
        self.populate_room_configurations()


# Run the seeder
if __name__ == "__main__":
    seeder = RoomSeeder()
    seeder.seed_all()