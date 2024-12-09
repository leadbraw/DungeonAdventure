from src.model.dungeon.dungeon import Dungeon
from src.model.factories.monster_factory import MonsterFactory
from src.model.factories.item_factory import ItemFactory
from src.model.managers.monster_manager import MonsterManager
from src.model.managers.item_manager import ItemManager


class DungeonManager:
    _instance = None

    @staticmethod
    def get_instance():
        """
        Retrieve the singleton instance of DungeonManager.
        :return current instance of DungeonManager (a new instance if none existed prior to the get_instance() call).
        """
        if DungeonManager._instance is None:
            DungeonManager._instance = DungeonManager()
        return DungeonManager._instance

    def __init__(self):
        if DungeonManager._instance is not None:
            raise Exception("This class is a singleton! Use get_instance().")
        self.dungeon = []
        self.monster_manager = MonsterManager.get_instance()
        self.item_manager = ItemManager.get_instance()
        # print("[DungeonManager] Initialized. Ready to generate the dungeon.")
        # Note that __init__ does NOT call initialize_dungeon(), that is the game controller's responsibility!

    def initialize_dungeon(self):
        """
        Creates and populates all floors of the dungeon.
        :return The newly created dungeon.
        """
        print("[DungeonManager] Initializing the dungeon...")
        self.dungeon = [Dungeon(1), Dungeon(2), Dungeon(3), Dungeon(4)]  # Four floors
        # print(f"[DungeonManager] Dungeon generated with {len(self.dungeon)} floors.")

        for floor_index, floor in enumerate(self.dungeon):
            print(f"[DungeonManager] Floor {floor_index + 1} initialized:")
            print(floor)

        for i in range(4):
            all_rooms = self.dungeon[i].get_room_list()
            print(f"[DungeonManager] Floor {i + 1} contains {len(all_rooms)} rooms.")

            monster_rooms = [
                coords for coords in all_rooms if self.dungeon[i].fetch_room(coords[0],
                                                                             coords[1]).get_type() == 'MONSTER'
            ]
            elite_rooms = [
                coords for coords in all_rooms if self.dungeon[i].fetch_room(coords[0], coords[1]).get_type() == 'ELITE'
            ]
            item_rooms = [
                coords for coords in all_rooms if self.dungeon[i].fetch_room(coords[0], coords[1]).get_type() == 'ITEM'
            ]

            self.populate_rooms(i, monster_rooms, elite_rooms, item_rooms, all_rooms)

        return self.dungeon

    def populate_rooms(self, floor, monster_rooms, elite_rooms, item_rooms, all_rooms):
        """
        Populates the given floor with monsters, items, and pillars.
        :param floor The floor on which the rooms will be populated.
        :param monster_rooms A list of tuples (row, column) which denote the location of MONSTER rooms.
        :param elite_rooms A list of tuples (row, column) which denote the location of ELITE rooms.
        :param item_rooms A list of tuples (row, column) which denote the location of ITEM rooms.
        :param all_rooms A list of tuples (row, column) which denote the location of all rooms.
        """
        print(f"[DungeonManager] Populating rooms for Floor {floor + 1}...")
        for room_coords in monster_rooms:
            self.place_monster(floor, room_coords, monster_type="Normal")

        for room_coords in elite_rooms:
            self.place_monster(floor, room_coords, monster_type="Elite")

        for room_coords in item_rooms:
            self.place_item(floor, room_coords)

        pillar_coords = all_rooms[2]  # Third room for the pillar
        self.place_pillar(floor, pillar_coords)

    def place_monster(self, floor, room_coords, monster_type):
        """
        Places a monster in the specified room.
        :param floor The floor number (0-indexed).
        :param room_coords The coordinates where the monster will be placed (row, column).
        :param monster_type The type of the monster.
        """
        raw_data = self.monster_manager.get_monster_data(monster_type=monster_type)
        if raw_data:
            raw_data_sliced = raw_data[1:]
            try:
                monster = MonsterFactory.get_instance().make_monster(raw_data_sliced)
                if monster:
                    self.dungeon[floor].fetch_room(room_coords[0], room_coords[1]).set_monster(monster)
                    print(f"[DungeonManager] Placed {monster.name} in a {monster_type.upper()} room at {room_coords}.")
            except ValueError as e:
                print(f"[DungeonManager] Error creating {monster_type.lower()} monster: {e}")

    def place_item(self, floor, room_coords):
        """
        Places a consumable item in the specified room.
        :param floor: The floor number (0-indexed).
        :param room_coords: The coordinates of the room where the item will be placed (row, column).
        """
        # Attempt to get raw item data and create the item
        raw_data = self.item_manager.get_random_consumable_item_data()
        if raw_data:
            item = ItemFactory.get_instance().create_item_from_raw(raw_data)
            if item:
                self.dungeon[floor].fetch_room(room_coords[0], room_coords[1]).set_item(item)
                print(f"[DungeonManager] Placed {item.name} in an ITEM room at {room_coords}.")

    def place_pillar(self, floor_index, pillar_coords):
        """
        Places a unique pillar item in the specified room.
        :param floor_index: The floor number (0-indexed).
        :param pillar_coords: The coordinates of the room where the pillar shall be placed (row, column).
        """
        # Attempt to retrieve unique item data and place the pillar
        raw_data = self.item_manager.get_unique_item_data(floor_index=floor_index)
        if raw_data:
            pillar_item = ItemFactory.get_instance().create_unique_item(raw_data)
            if pillar_item:
                self.dungeon[floor_index].fetch_room(pillar_coords[0], pillar_coords[1]).set_item(pillar_item)
                print(f"[DungeonManager] Placed {pillar_item.name} in a PILLAR room at {pillar_coords}.")
            else:
                print(f"[DungeonManager] Failed to create a unique pillar item for Floor {floor_index + 1}.")
        else:
            print(f"[DungeonManager] No unique item data found for Floor {floor_index + 1}.")

    def get_floor_entrance(self, floor):
        """
        Returns the entrance position for the specified floor.
        :param floor The number of the floor to be checked.
        :return The location of the entrance (row, column).
        """
        if floor < 1 or floor > len(self.dungeon):
            print(f"[DungeonManager] Error: Invalid floor number {floor}.")
            raise ValueError(f"Invalid floor number: {floor}")
        entrance = self.dungeon[floor - 1].get_entrance_coords()
        print(f"[DungeonManager] Entrance for Floor {floor}: {entrance}")
        return entrance

    def get_room(self, floor, position):
        """
        Fetch a room based on floor and position.
        :param floor The floor number (1-indexed).
        :param position The coordinates of the room to be grabbed (row, column).
        :return The room at the specified position.
        """
        # print(f"[DungeonManager] Fetching room at Floor {floor}, Position {position}.")
        return self.dungeon[floor - 1].fetch_room(position[0], position[1])

    def mark_room_visited(self, floor, position):
        """
        Mark a room as visited.
        :param floor The floor number (1-indexed).
        :param position The coordinates of the room to be marked visited (row, column).
        """
        print(f"[DungeonManager] Marking room as visited: Floor {floor}, Position {position}.")
        self.get_room(floor, position).set_visited(True)

    def get_floor_map(self, floor, reveal_all=False):
        """
        Returns the map for the specified floor.
        :param floor The floor number (1-indexed).
        :param reveal_all Reveals all rooms
        :return The map of the floor as a pygame Surface.
        """
        if floor < 1 or floor > len(self.dungeon):
            print(f"[DungeonManager] Error: Invalid floor number {floor}.")
            raise ValueError(f"Invalid floor number: {floor}")

        floor_map = self.dungeon[floor - 1].create_map(reveal_all)
        # print(f"[DungeonManager] Retrieved map for Floor {floor}.")
        return floor_map

    def get_monster_in_room(self, floor, position):
        """
        Returns the monster in the specified room on the given floor.
        :param floor The floor number (1-indexed).
        :param position The (row, column) tuple for the room's position.
        :return The monster in the room, or None if there is no monster.
        """
        print(f"[DungeonManager] Fetching monster in room at Floor {floor}, Position {position}.")
        room = self.get_room(floor, position)
        if room.has_monster():
            monster = room.get_monster()
            return monster
        else:
            return None

    def get_item_in_room(self, floor, position):
        """
        Returns the item in the specified room on the given floor.
        :param floor The floor number (1-indexed).
        :param position The (row, column) tuple for the room's position.
        :return The item in the room, or None if there is no item.
        """
        print(f"[DungeonManager] Fetching item in room at Floor {floor}, Position {position}.")
        room = self.get_room(floor, position)
        if room.has_item():
            item = room.get_item()
            return item
        else:
            return None

    def clear_item_in_room(self, floor, position):
        """
        Clears (removes) the item in the specified room on the given floor.
        :param floor The floor number (1-indexed).
        :param position The (row, column) tuple for the room's position.
        """
        room = self.get_room(floor, position)
        if room.has_item():
            room.set_item(None)

# Method to define what gets pickled
    def __getstate__(self):
        # Return a dictionary of the object's state
        return {'dungeon': self.dungeon}

    # Method to define how the object is restored
    def __setstate__(self, state):
        # Restore the object's state from the dictionary
        self.dungeon = state['dungeon']
