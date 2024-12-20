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
            # Convert JSON string of directions back to a list
            doors = json.loads(row[0])
            self.rooms[tuple(doors)] = {
                "image_path": row[1],
                "rotation": row[2]
            }

    def get_room_by_doors(self, doors):
        """
        Retrieves the sprite configuration for the given door configuration.
        :param doors: List of four booleans representing the door states (top, right, bottom, left).
        :return: A dictionary containing 'sprite_name' and 'rotation', or None if not found.
        """
        room_config = self.rooms.get(tuple(doors))
        if room_config:
            # Normalize the sprite name from image_path
            image_path = room_config["image_path"]
            # Handle both forward (/) and backward (\) slashes
            sprite_name = image_path.replace("\\", "/").split("/")[-1].split(".")[0]
            return {"sprite_name": sprite_name, "rotation": room_config["rotation"]}
        else:
            print(f"[RoomManager] No room config found for doors: {doors}")
            return None

    def get_all_rooms(self):
        return self.rooms

    def __getstate__(self):
        """ Stores the object's state in a pickled dictionary.
        :return: dictionary of states to be stored.
        """
        return {'rooms': self.rooms}

    # Method to define how the object is restored
    def __setstate__(self, state):
        """ Restores the object's state from the pickled dictionary.
        :param state: dictionary of restored states.
        """
        self.rooms = state['rooms']