import sqlite3
import json

class RoomSeeder:
    def __init__(self, db_path='data/dungeon_game.db'):
        """
        Initializes the RoomSeeder with the database path.
        :param db_path: Path to the SQLite database file.
        """
        self.db_path = db_path

    def populate_rooms(self):
        """
        Populates the rooms table with door configurations, associated images, and required rotations.
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            # Define the room data: (doors, image_path, rotation)
            room_data = [
                # Four doors open (1 configuration)
                ([True, True, True, True], "assets/images/dungeon_four.png", 0),

                # Three doors open (4 configurations)
                ([True, True, True, False], "assets/images/dungeon_three.png", 0),  # Top, right, bottom
                ([True, True, False, True], "assets/images/dungeon_three.png", 90),  # Top, right, left
                ([True, False, True, True], "assets/images/dungeon_three.png", 180),  # Top, bottom, left
                ([False, True, True, True], "assets/images/dungeon_three.png", 270),  # Right, bottom, left

                # Two doors open (6 configurations)
                ([True, True, False, False], "assets/images/dungeon_two.png", 0),  # Top, right
                ([True, False, True, False], "assets/images/dungeon_op_two_b.png", 0),  # Top, bottom
                ([True, False, False, True], "assets/images/dungeon_two.png", 90),  # Top, left
                ([False, True, True, False], "assets/images/dungeon_two.png", 270),  # Right, bottom
                ([False, True, False, True], "assets/images/dungeon_op_two_a.png", 90),  # Right, left
                ([False, False, True, True], "assets/images/dungeon_two.png", 180),  # Bottom, left

                # One door open (4 configurations)
                ([True, False, False, False], "assets/images/dungeon_one.png", 0),  # Top
                ([False, True, False, False], "assets/images/dungeon_one.png", 270),  # Right
                ([False, False, True, False], "assets/images/dungeon_one.png", 180),  # Bottom
                ([False, False, False, True], "assets/images/dungeon_one.png", 90),  # Left
            ]

            # Insert data into the database
            for doors, image_path, rotation in room_data:
                # Convert the doors list to a JSON string for database storage
                cursor.execute("""
                    INSERT OR IGNORE INTO rooms (doors, image_path, rotation)
                    VALUES (?, ?, ?)
                """, (json.dumps(doors), image_path, rotation))

            # Commit the transaction to save changes
            conn.commit()
            print(f"Inserted {len(room_data)} room configurations into the database.")


if __name__ == "__main__":
    seeder = RoomSeeder()
    seeder.populate_rooms()
