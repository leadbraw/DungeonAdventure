from model.dungeon.dungeon import Dungeon
from model.factories.monster_factory import MonsterFactory
from model.factories.item_factory import ItemFactory
from model.managers.monster_manager import MonsterManager
from model.managers.item_manager import ItemManager


class DungeonManager:
    _instance = None

    @staticmethod
    def get_instance():
        """Retrieve the singleton instance of DungeonManager."""
        if DungeonManager._instance is None:
            DungeonManager._instance = DungeonManager()
        return DungeonManager._instance

    def __init__(self):
        if DungeonManager._instance is not None:
            raise Exception("This class is a singleton! Use get_instance().")
        self.dungeon = []
        self.monster_manager = MonsterManager.get_instance()
        self.item_manager = ItemManager.get_instance()
        print("[DungeonManager] Initialized. Ready to generate the dungeon.")
        # Note that __init__ does NOT call initialize_dungeon(), that is the game controller's responsibility!

    def initialize_dungeon(self):
        """Creates and populates all floors of the dungeon."""
        print("[DungeonManager] Initializing the dungeon...")
        self.dungeon = [Dungeon(1), Dungeon(2), Dungeon(3), Dungeon(4)]  # Four floors
        print(f"[DungeonManager] Dungeon generated with {len(self.dungeon)} floors.")

        for floor_index, floor in enumerate(self.dungeon):
            print(f"[DungeonManager] Floor {floor_index + 1} initialized:")
            print(floor)

        for i in range(4):
            all_rooms = self.dungeon[i].get_room_list()
            print(f"[DungeonManager] Floor {i + 1} contains {len(all_rooms)} rooms.")

            monster_rooms = [
                coords for coords in all_rooms if self.dungeon[i].fetch_room(coords[0], coords[1]).type == 'MONSTER'
            ]
            elite_rooms = [
                coords for coords in all_rooms if self.dungeon[i].fetch_room(coords[0], coords[1]).type == 'ELITE'
            ]
            item_rooms = [
                coords for coords in all_rooms if self.dungeon[i].fetch_room(coords[0], coords[1]).type == 'ITEM'
            ]

            print(
                f"[DungeonManager] Floor {i + 1}: {len(monster_rooms)} MONSTER rooms, {len(elite_rooms)} ELITE rooms, {len(item_rooms)} ITEM rooms.")
            self.populate_rooms(i, monster_rooms, elite_rooms, item_rooms, all_rooms)

        return self.dungeon

    def populate_rooms(self, floor, monster_rooms, elite_rooms, item_rooms, all_rooms):
        """Populates the given floor with monsters, items, and pillars."""
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
        """Places a monster in the specified room."""
        print(f"[DungeonManager] Attempting to place {monster_type} monster in Floor {floor + 1}, Room {room_coords}.")
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
        """Places a consumable item in the specified room."""
        print(f"[DungeonManager] Attempting to place an ITEM in Floor {floor + 1}, Room {room_coords}.")
        raw_data = self.item_manager.get_random_consumable_item_data()
        if raw_data:
            item = ItemFactory.get_instance().create_item_from_raw(raw_data)
            if item:
                self.dungeon[floor].fetch_room(room_coords[0], room_coords[1]).set_item(item)
                print(f"[DungeonManager] Placed {item.get_name()} in an ITEM room at {room_coords}.")

    def place_pillar(self, floor_index, pillar_coords):
        """Places a unique pillar item in the specified room."""
        print(f"[DungeonManager] Attempting to place a PILLAR in Floor {floor_index + 1}, Room {pillar_coords}.")
        raw_data = self.item_manager.get_unique_item_data(floor_index=floor_index)
        if raw_data:
            pillar_item = ItemFactory.get_instance().create_unique_item(raw_data)
            self.dungeon[floor_index].fetch_room(pillar_coords[0], pillar_coords[1]).set_item(pillar_item)
            print(f"[DungeonManager] Placed {pillar_item.get_name()} in a PILLAR room at {pillar_coords}.")
        else:
            print(f"[DungeonManager] Failed to place pillar in a PILLAR room at {pillar_coords}.")

    def get_floor_entrance(self, floor):
        """Returns the entrance position for the specified floor."""
        if floor < 1 or floor > len(self.dungeon):
            print(f"[DungeonManager] Error: Invalid floor number {floor}.")
            raise ValueError(f"Invalid floor number: {floor}")
        entrance = self.dungeon[floor - 1].entrance_loc
        print(f"[DungeonManager] Entrance for Floor {floor}: {entrance}")
        return entrance

    def get_room(self, floor, position):
        """Fetch a room based on floor and position."""
        # print(f"[DungeonManager] Fetching room at Floor {floor}, Position {position}.")
        return self.dungeon[floor - 1].fetch_room(position[0], position[1])

    def mark_room_visited(self, floor, position):
        """Mark a room as visited."""
        print(f"[DungeonManager] Marking room as visited: Floor {floor}, Position {position}.")
        self.get_room(floor, position).set_visited(True)

    def get_floor_map(self, floor):
        """
        Returns the map for the specified floor.
        :param floor: The floor number (1-indexed).
        :return: The map of the floor as an image or object.
        """
        if floor < 1 or floor > len(self.dungeon):
            print(f"[DungeonManager] Error: Invalid floor number {floor}.")
            raise ValueError(f"Invalid floor number: {floor}")

        floor_map = self.dungeon[floor - 1].create_map()
        # print(f"[DungeonManager] Retrieved map for Floor {floor}.")
        return floor_map

    def get_monster_in_room(self, floor, position):
        """
        Returns the monster in the specified room on the given floor.
        :param floor: The floor number (1-indexed).
        :param position: The (row, column) tuple for the room's position.
        :return: The monster in the room, or None if there is no monster.
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
        :param floor: The floor number (1-indexed).
        :param position: The (row, column) tuple for the room's position.
        :return: The item in the room, or None if there is no item.
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
        :param floor: The floor number (1-indexed).
        :param position: The (row, column) tuple for the room's position.
        """
        room = self.get_room(floor, position)
        if room.has_item():
            room.set_item(None)
