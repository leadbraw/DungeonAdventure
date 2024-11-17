import sqlite3
from itertools import product

class RoomManager:
    _instance = None  # Singleton instance

    @staticmethod
    def get_instance():
        if RoomManager._instance is None:
            RoomManager._instance = RoomManager()
        return RoomManager._instance

    def __init__(self, db_path='data/dungeon_game.db'):
        if RoomManager._instance is not None:
            raise Exception("This class is a singleton!")
        self.db_path = db_path
        self.door_configurations = self.load_door_configurations()
        self.room_types = self.load_room_types()
        self.room_variants = self.generate_room_variants()  # 238 possibilities

    def load_door_configurations(self):
        """Loads all door configurations from the database."""
        door_configs = {}
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        query = "SELECT id, door_north, door_east, door_south, door_west FROM door_configurations"
        cursor.execute(query)
        for row in cursor.fetchall():
            config_id = row[0]
            door_configs[config_id] = {
                "north": row[1], "east": row[2], "south": row[3], "west": row[4]
            }

        conn.close()
        return door_configs

    def load_room_types(self):
        """Loads all room types from the database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        query = "SELECT id, room_type FROM room_types"
        cursor.execute(query)
        room_types = {row[0]: row[1] for row in cursor.fetchall()}

        conn.close()
        return room_types

    def generate_room_variants(self):
        """Generates and stores all 238 possible room configurations."""
        room_variants = {}
        for room_type_id, door_config_id in product(self.room_types.keys(), self.door_configurations.keys()):
            key = (room_type_id, door_config_id)
            room_variants[key] = {
                "room_type": self.room_types[room_type_id],
                "door_config": self.door_configurations[door_config_id]
            }
        return room_variants

    def get_room_configuration(self, room_type_id, door_config_id):
        """Returns a room configuration by room type and door configuration."""
        key = (room_type_id, door_config_id)
        return self.room_variants.get(key)
