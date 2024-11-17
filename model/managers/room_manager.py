import os
import sqlite3
import json

class RoomManager:
    _instance = None  # Singleton instance

    @staticmethod
    def get_instance(db_path='data/dungeon_game.db'):
        """
        Get or create the singleton instance of RoomManager.
        :param db_path: Path to the SQLite database.
        """
        if RoomManager._instance is None:
            RoomManager._instance = RoomManager(db_path)
        return RoomManager._instance

    def __init__(self, db_path):
        """
        Initializes the RoomManager with the database path.
        :param db_path: Path to the SQLite database.
        """
        if RoomManager._instance is not None:
            raise Exception("This class is a singleton!")
        self.db_path = db_path

        # Debugging: Check the database path
        print(f"Initializing RoomManager with DB path: {self.db_path}")
        if not os.path.exists(self.db_path):
            raise FileNotFoundError(f"Database file not found: {self.db_path}")

        self.rooms = self.load_rooms()  # Load all room data from the database

    def load_rooms(self):
        """
        Loads all room configurations from the database.
        :return: Dictionary of room configurations keyed by door configuration (JSON-encoded list).
        """
        rooms = {}
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            query = "SELECT doors, image_path, rotation FROM rooms"
            cursor.execute(query)
            for row in cursor.fetchall():
                doors = json.loads(row[0])  # Convert JSON string back to a list
                image_path = row[1]
                rotation = row[2]
                rooms[tuple(doors)] = {
                    "image_path": image_path,
                    "rotation": rotation
                }
        return rooms

    def get_room_by_doors(self, doors):
        """
        Retrieves room configuration by door configuration.
        :param doors: List of booleans [up, right, down, left] representing door states.
        :return: Dictionary with image path and rotation, or None if not found.
        """
        return self.rooms.get(tuple(doors))

    def get_all_rooms(self):
        """
        Returns all available room configurations.
        :return: Dictionary of all room configurations.
        """
        return self.rooms