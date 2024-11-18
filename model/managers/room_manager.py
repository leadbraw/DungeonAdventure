import json

class RoomManager:
    _instance = None  # Singleton instance

    @staticmethod
    def get_instance(rooms_data=None):
        if RoomManager._instance is None:
            if rooms_data is None:
                raise ValueError("RoomManager requires 'rooms_data' for initialization.")
            RoomManager._instance = RoomManager(rooms_data)
        return RoomManager._instance

    def __init__(self, rooms_data):
        if RoomManager._instance is not None:
            raise Exception("This class is a singleton! Use get_instance() to access the instance.")
        self.rooms = {}
        for row in rooms_data:
            doors = json.loads(row[0])  # Convert JSON string back to a list
            self.rooms[tuple(doors)] = {
                "image_path": row[1],
                "rotation": row[2]
            }

    def get_room_by_doors(self, doors):
        return self.rooms.get(tuple(doors))

    def get_all_rooms(self):
        return self.rooms
