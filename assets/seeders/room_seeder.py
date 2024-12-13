import sqlite3
import json
from constants import SPRITE_PATHS  # Import SPRITE_PATHS from constants.py

class RoomSeeder:
    def __init__(self, db_path='data/dungeon_game.db'):
        self.db_path = db_path

    def populate_rooms(self):
        """Populates the rooms table with door configurations, images, and rotations."""
        room_data = [
            # Four doors open (1 configuration)
            ([True, True, True, True], SPRITE_PATHS["dungeon_four"], 0),

            # Three doors open (4 configurations)
            ([True, True, True, False], SPRITE_PATHS["dungeon_three"], 0),  # Top, right, bottom
            ([True, True, False, True], SPRITE_PATHS["dungeon_three"], 90),  # Top, right, left
            ([True, False, True, True], SPRITE_PATHS["dungeon_three"], 180),  # Top, bottom, left
            ([False, True, True, True], SPRITE_PATHS["dungeon_three"], 270),  # Right, bottom, left

            # Two doors open (6 configurations)
            ([True, True, False, False], SPRITE_PATHS["dungeon_two"], 0),  # Top, right
            ([True, False, True, False], SPRITE_PATHS["dungeon_two_op_b"], 0),  # Top, bottom
            ([True, False, False, True], SPRITE_PATHS["dungeon_two"], 90),  # Top, left
            ([False, True, True, False], SPRITE_PATHS["dungeon_two"], 270),  # Right, bottom
            ([False, True, False, True], SPRITE_PATHS["dungeon_two_op_a"], 90),  # Right, left
            ([False, False, True, True], SPRITE_PATHS["dungeon_two"], 180),  # Bottom, left

            # One door open (4 configurations)
            ([True, False, False, False], SPRITE_PATHS["dungeon_one"], 0),  # Top
            ([False, True, False, False], SPRITE_PATHS["dungeon_one"], 270),  # Right
            ([False, False, True, False], SPRITE_PATHS["dungeon_one"], 180),  # Bottom
            ([False, False, False, True], SPRITE_PATHS["dungeon_one"], 90),  # Left
        ]

        insert_query = """
                        INSERT OR IGNORE INTO rooms (doors, image_path, rotation)
                        VALUES (?, ?, ?)
                    """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                for doors, image_path, rotation in room_data:
                    cursor.execute(insert_query, (json.dumps(doors), image_path, rotation))
                conn.commit()
        except sqlite3.Error as e:
            print(f"Error populating rooms table: {e}")