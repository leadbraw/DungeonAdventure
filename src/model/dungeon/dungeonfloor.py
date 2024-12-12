import random
import pygame
from colorama import Fore, Style
from copy import deepcopy
from pygame import Surface
from constants import BACKGROUND_COLOR, TRAP_CHANCE, ITEM_CHANCE, MONSTER_CHANCE, ELITE_CHANCE, EMPTY_CHANCE, \
    EVENT_CHANCE, ENTITY_CHANCE, MAP_SURFACE_TILE_SIZE, FADED_GRAY, RED, DARK_RED, GOLD, BROWN, \
    VIOLET, DARK_VIOLET, BLACK, MEDIUM_GREY

'''
MONSTER: Room with monster, battle begins upon entry
BOSS: Room with boss enemy, battle begins upon entry
EXIT: Allows exiting the dungeon
ENTRANCE: Starting room
ITEM: Room containing an item, picked up upon entry
TRAP: Room that does some amount of damage to the adventurer upon entry

BLOCKED: Inaccessible room

RANDOM: Passed to Room constructor to indicate a random accessible room
'''


class Room:
    """Represents a single room. Should never be instantiated outside the context of within a Dungeon class."""

    def __init__(self, room_type='BLOCKED'):
        """
        Constructor. Instantiates fields

        :param room_type: The room type of the room. Room types defined above.
        """
        if room_type == 'RANDOM':
            # First roll: Decide the major category
            main_category = random.choices(
                population=['ENTITY', 'EVENT', 'EMPTY'],
                weights=[ENTITY_CHANCE, EVENT_CHANCE, EMPTY_CHANCE],  # 40% entity, 40% event, 20% empty
                k=1
            )[0]

            if main_category == 'ENTITY':
                # 80% chance for 'MONSTER', 20% for 'ELITE'
                self.type = random.choices(
                    population=['MONSTER', 'ELITE'],
                    weights=[MONSTER_CHANCE, ELITE_CHANCE],
                    k=1
                )[0]

            elif main_category == 'EVENT':
                # 50% chance for 'TRAP', 50% for 'ITEM'
                self.type = random.choices(
                    population=['TRAP', 'ITEM'],
                    weights=[TRAP_CHANCE, ITEM_CHANCE],
                    k=1
                )[0]

            elif main_category == 'EMPTY':
                # Directly assign 'EMPTY'
                self.type = 'EMPTY'
        else:
            # Assign fixed room type for non-random cases
            self.type = room_type

        self.valid_directions = [False, False, False, False]  # Up, Right, Down, Left
        # Attributes
        self.monster = None
        self.item = None
        self.visited = False

    def __str__(self):
        """
        Prints out a string representation of the room in form 'TYPE' with a specific color for each time.

        :return: A string representation of the room.
        """
        colors = {
            'MONSTER': Fore.RED,
            'ELITE': Fore.MAGENTA,
            'ITEM': Fore.GREEN,
            'TRAP': Fore.YELLOW,
            'ENTRANCE': Fore.CYAN,
            'EXIT': Fore.BLUE,
            'PILLAR': Fore.LIGHTWHITE_EX,
            'BLOCKED': Fore.LIGHTBLACK_EX
        }
        color = colors.get(self.type, Fore.RESET)  # Default to no color
        return f"{color}{self.type:<8}{Style.RESET_ALL}"

    def set_monster(self, monster):
        """
        Sets the monster field of the room to a given monster.

        :param monster: The monster to 'place' in the room.
        """
        self.monster = monster

    def get_monster(self):
        """
        Returns the monster in the room.

        :return: The monster currently present in the room
        """
        return self.monster

    def has_monster(self):
        """
        Returns a boolean for if the room has a monster or not.

        :return: Whether the room has a monster or not.
        """
        return self.monster is not None

    # Item-related methods

    def set_item(self, item):
        """
        Setter for the item in the room.

        :param item: The item to place in the room
        """
        self.item = item

    def get_item(self):
        """
        Fetches the item in the room.

        :return: The item in the room.
        """
        return self.item

    def has_item(self):
        """
        Returns a boolean for if the room has an item or not.

        :return: Whether the room has an item or not.
        """
        return self.item is not None

    def set_type(self, new_type):
        """
        Setter for the room type.

        :param new_type: The new room type.
        """
        self.type = new_type

    def get_type(self):
        """
        Getter for the room type.

        :return: The room type.
        """
        return self.type

    def set_visited(self, new_visited):
        """
        Setter for visited field. Used when adventurer reaches room for the first time.

        :param new_visited: The new visited status of the room.
        """
        self.visited = new_visited

    def get_visited(self):
        """
        Getter for visited status.

        :return: The visited status of the room.
        """
        return self.visited

    def define_valid_directions(self, length, width, dungeon, x, y):
        """
        Sets the valid directions field of the room according to whether the adjacent rooms
        are traversable or not.

        :param length: The length of the floor the room is on.
        :param width: The width of the floor the room is on.
        :param dungeon: The entire dungeon.
        :param x: The row position.
        :param y: The column position.
        """
        directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]  # Up, Right, Down, Left
        count = 0
        for i in directions:
            if 0 <= x + i[0] < length and 0 <= y + i[1] < width and dungeon[x + i[0]][y + i[1]].type != 'BLOCKED':
                self.valid_directions[count] = True
            count += 1

    def __getstate__(self):
        """Stores the object's state in a pickled dictionary."""
        return {'type': self.type,
                'valid_directions': self.valid_directions,
                'monster': self.monster,
                'item': self.item,
                'visited': self.visited}

    def __setstate__(self, state):
        """Restores the object's state from the pickled dictionary."""
        self.type = state['type']
        self.valid_directions = state['valid_directions']
        self.monster = state['monster']
        self.item = state['item']
        self.visited = state['visited']


class DungeonFloor:
    """Represents one floor of a dungeon. Is made up of Rooms. A collection of these make up the whole dungeon."""

    def __init__(self, floor_number):
        """Constructor for Dungeon. Instantiates it."""
        # 5x5, 6x6, 7x7, 8x8
        self._length = floor_number + 4
        self._width = floor_number + 4
        # Rooms by default are blocked
        self._map = [[Room('BLOCKED') for _ in range(self._length)] for _ in range(self._width)]
        self._entrance_loc = None
        self._exit_loc = None
        self._pillar_loc = None
        self._room_list = []  # List to store non-blocked room coordinates
        '''Populates the map, in addition to instantiating the entrance_loc, exit_loc, and room_list fields'''
        self.__populate_map()

    def get_width(self) -> int:
        """
        Returns the width of the floor

        :return: The width.
        """
        return self._width

    def get_length(self) -> int:
        """
        Returns the length of the floor

        :return: The length.
        """
        return self._length

    def get_room_list(self) -> list[tuple[int, int]]:
        """
        Returns a deep copy of the room coordinate list.

        :return: A deep copy of the room coordinate list.
        """
        return deepcopy(self._room_list)

    def get_entrance_coords(self) -> tuple[int, int]:
        """
        Returns coordinates of entrance room.

        :return: The coordinates of the entrance room (row, column).
        """
        return self._entrance_loc

    def get_exit_coords(self) -> tuple[int, int]:
        """
        Returns coordinates of exit room.

        :return: The coordinates of the exit room (row, column).
        """
        return self._exit_loc

    def get_pillar_coords(self) -> tuple[int, int]:
        """
        Returns coordinates of the pillar room.

        :return: The coordinates of the pillar room (row, column).
        """
        return self._pillar_loc

    def fetch_room(self, x, y) -> Room:
        """
        Fetches room at given coordinates.

        :return: The room at the passed coordinates.
        """
        return self._map[x][y]

    def reveal_adjacent_rooms(self, x, y):
        """
        Marks adjacent rooms to a certain room as visited. For use in the minimap.

        :param x: The row coordinate of the room.
        :param y: The column coordinate of the room.
        """
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)]
        for pair in directions:
            next_x, next_y = x + pair[0], y + pair[1]
            if 0 <= next_x < self._length and 0 <= next_y < self._width:
                self._map[next_x][next_y].set_visited(True)

    def __str__(self):
        """
        Returns a string representation of this floor. Rows separated by a newline character.

        :return: A string representation of this floor.
        """
        result = ""
        for row in self._map:
            result += " ".join(str(item) for item in row) + "\n"
        return result

    @staticmethod
    def __distance(a_x, a_y, b_x, b_y):
        """
        Static method used for calculating the number of rooms that need to be traversed from room A to B.

        :param a_x: The row coordinate of room A.
        :param a_y: The column coordinate of room A.
        :param b_x: The row coordinate of room B.
        :param b_y: The column coordinate of room B.
        :return: The distance between the two rooms.
        """
        current_x = a_x
        current_y = a_y
        count = 0
        while current_y != b_y:
            while current_x != b_x:
                current_x = current_x + 1 if current_x < b_x else current_x - 1
                count += 1
            current_y = current_y + 1 if current_y < b_y else current_y - 1
            count += 1
        return count

    def __populate_map(self):
        """Responsible for populating a fresh map with an entrance, exit, pillar, et cetera."""
        essential_rooms = []  # Store the entrance, exit, and pillar here
        other_rooms = []  # Temporarily store other non-blocked rooms here

        # Place entrance
        entrance_x, entrance_y = (random.randint(0, self._length - 1), random.randint(0, self._width - 1))
        self._entrance_loc = (entrance_x, entrance_y)
        self._map[entrance_x][entrance_y] = Room('ENTRANCE')
        essential_rooms.append((entrance_x, entrance_y))

        # Place exit
        exit_x, exit_y = (random.randint(0, self._length - 1), random.randint(0, self._width - 1))
        distance = self.__distance(entrance_x, entrance_y, exit_x, exit_y)
        while distance <= self._length - 1:
            exit_x, exit_y = (random.randint(0, self._length - 1), random.randint(0, self._width - 1))
            distance = self.__distance(entrance_x, entrance_y, exit_x, exit_y)
        self._exit_loc = (exit_x, exit_y)
        self._map[exit_x][exit_y] = Room('EXIT')
        essential_rooms.append((exit_x, exit_y))

        # Generate path and offshoots
        path = self.__path_to_exit(entrance_x, entrance_y, exit_x, exit_y)
        offshoot_rooms = self.__generate_offshoots(path)
        populated_rooms = path + offshoot_rooms
        self._room_list = populated_rooms  # Initialize the room list

        # Add all other rooms to other_rooms list
        for a in populated_rooms:
            x, y = a
            self._map[x][y].define_valid_directions(self._length, self._width, self._map, x, y)
            other_rooms.append((x, y))

        # Place pillar
        self.__place_pillar(populated_rooms, exit_x, exit_y)
        pillar_coords = next(
            (x, y) for x, y in populated_rooms if self._map[x][y].get_type() == 'PILLAR'
        )
        essential_rooms.append(pillar_coords)  # Add pillar as the third room in the list

        # Finalize the room list
        self._room_list = essential_rooms + [room for room in other_rooms if room not in essential_rooms]

    def __generate_offshoots(self, path):
        """
        Responsible for generating offshoot paths on the map.

        :param path: The path from the entrance to exit, sequence of (row, column) tuples.
        :return: The locations of all offshoot rooms.
        """
        offshoot_length = self._length - 2
        starting_points = random.sample(path[1:-1], offshoot_length - 1)
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        room_locations = []
        for x, y in starting_points:
            direction = random.choice(directions)
            if not self.__valid_direction_for_offshoot(direction, x, y):
                direction = [-1 * direction[0], -1 * direction[1]]
            for i in range(offshoot_length):
                next_x, next_y = x + direction[0] * (i + 1), y + direction[1] * (i + 1)
                if (0 <= next_x < self._length and
                        0 <= next_y < self._width and
                        self._map[next_x][next_y].type == 'BLOCKED'):
                    self._map[next_x][next_y] = Room('RANDOM')
                    room_locations.append((next_x, next_y))
                else:
                    break
        return room_locations

    def __path_to_exit(self, entrance_x, entrance_y, exit_x, exit_y) -> list:
        """
        Responsible for creating and returning the path from the entrance to the exit of the dungeon.

        :param entrance_x: The row coordinate of the entrance.
        :param entrance_y: The column coordinate of the entrance.
        :param exit_x: The row coordinate of the exit.
        :param exit_y: The column coordinate of the exit.
        :return: A list of coordinates (row, column) that is the path from the entrance to the exit.
        """
        current_x = entrance_x
        current_y = entrance_y
        path = [(current_x, current_y)]
        while current_y != exit_y:
            while current_x != exit_x:
                current_x = current_x + 1 if current_x < exit_x else current_x - 1
                self._map[current_x][current_y] = Room('RANDOM')
                path.append((current_x, current_y))
            current_y = current_y + 1 if current_y < exit_y else current_y - 1
            if current_x != exit_x or current_y != exit_y:
                self._map[current_x][current_y] = Room('RANDOM')
            path.append((current_x, current_y))
        return path

    def __place_pillar(self, rooms, exit_x, exit_y):
        """
        Places one pillar somewhere on the map (excluding entrance/exit).

        :param rooms: A list of all traversable room coordinates.
        :param exit_x: The row coordinate of the exit.
        :param exit_y: The column coordinate of the exit.
        """
        x, y = random.choice(rooms[1:])  # excludes entrance room
        while x == exit_x and y == exit_y:
            x, y = random.choice(rooms[1:])
        self._map[x][y].set_type("PILLAR")
        self._pillar_loc = (x, y)
        if (x, y) not in self._room_list:
            self._room_list.append((x, y))  # Add to non-blocked list

    def __valid_direction_for_offshoot(self, direction, x, y) -> bool:
        """
        Whether a direction is a valid direction to place an offshoot on the map or not.

        :param direction: The direction.
        :param x: The row of the room.
        :param y: The column of the room.
        """
        new_x, new_y = x + direction[0], y + direction[1]
        return (0 <= new_x < self._length and 0 <= new_y < self._width and
                self._map[new_x][new_y].type == 'BLOCKED')

    def create_map(self, reveal_all=False):
        """
        Creates the minimap of the floor. By default, only returns visited rooms. Returns a Surface.

        :param reveal_all: Whether all rooms should be revealed on the map or not.
        :return A pygame Surface representing the current floor's map.
        """
        tile_size = MAP_SURFACE_TILE_SIZE
        map_surface = Surface((MAP_SURFACE_TILE_SIZE * 8, MAP_SURFACE_TILE_SIZE * 8))  # 8 is max floor width/height
        color = None
        for row in range(self._length):
            for col in range(self._width):
                room = self._map[row][col]
                x = col * tile_size
                y = row * tile_size
                if room.type == "MONSTER":
                    color = RED
                elif room.type == "ELITE":
                    color = DARK_RED
                elif room.type == "ITEM":
                    color = GOLD
                elif room.type == "PILLAR":
                    color = FADED_GRAY
                elif room.type == "TRAP":
                    color = BROWN
                elif room.type == "ENTRANCE":
                    color = VIOLET
                elif room.type == "EXIT":
                    color = DARK_VIOLET
                elif room.type == "EMPTY":
                    color = MEDIUM_GREY
                elif room.type == "BLOCKED":
                    color = BLACK
                if not reveal_all and room.visited:
                    pygame.draw.rect(map_surface, color, (x, y, tile_size, tile_size))
                elif reveal_all:
                    pygame.draw.rect(map_surface, color, (x, y, tile_size, tile_size))

        return map_surface

    def __getstate__(self):
        """Stores the object's state in a pickled dictionary."""
        return {'_length': self._length,
                '_width': self._width,
                '_map': self._map,
                '_entrance_loc': self._entrance_loc,
                '_exit_loc': self._exit_loc,
                '_pillar_loc': self._pillar_loc,
                '_room_list': self._room_list}

    def __setstate__(self, state):
        """Restores the object's state from the pickled dictionary."""
        self._length = state['_length']
        self._width = state['_width']
        self._map = state['_map']
        self._entrance_loc = state['_entrance_loc']
        self._exit_loc = state['_exit_loc']
        self._pillar_loc = state['_pillar_loc']
        self._room_list = state['_room_list']


if __name__ == "__main__":
    screen = pygame.display.set_mode((500, 500))
    # Testing code
    d = DungeonFloor(4)
    print(d.__str__())
    print(f"Non-blocked rooms ({len(d._room_list)}): {d._room_list}")
    running = True
    d_map = d.create_map(True)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill(BACKGROUND_COLOR)
        screen.blit(d_map, (0, 0))
        pygame.display.update()
