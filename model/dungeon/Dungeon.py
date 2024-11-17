from enum import Enum
import random
from copy import deepcopy

'''
MONSTER: Room with monster, battle begins upon entry
BOSS: Room with boss enemy, battle begins upon entry
EXIT: Allows exiting the dungeon
ENTRANCE: Starting room
ITEM: Room containing an item, picked up upon entry
BLOCKED: Inaccessible room
'''

class Room:
    def __init__(self, room_type='BLOCKED'):
        self.type = (room_type if room_type != 'RANDOM'
                     else random.choices(population=['MONSTER', 'TRAP', 'ELITE', 'ITEM'],
                                         weights=[0.45, 0.2, 0.1, 0.25],
                                         k=1)[0])
        self.valid_directions = [False, False, False, False] # Up, Right, Down, Left
        '''
        45% chance for a random room to be a monster,
        20% for trap
        25% for item,
        10% for a boss/elite enemy
        '''

    def __str__(self):
        return self.type

    def set_type(self, new_type):
        self.type = new_type

    def get_type(self):
        return self.type

    def define_valid_directions(self, length, width, dungeon, x, y):
        directions = [(-1, 0), (0, 1), (1, 0), (0, -1)] # Up, Right, Down, Left
        count = 0
        for i in directions:
            if 0 <= x + i[0] < length and 0 <= y + i[1] < width and dungeon[x + i[0]][y + i[1]].type != 'BLOCKED':
                self.valid_directions[count] = True
            count += 1

class Dungeon:
    def __init__(self, floor_number):
        """Constructor for Dungeon. Instantiates it."""
        # 5x5, 6x6, 7x7, 8x8
        self.length = floor_number + 4
        self.width = floor_number + 4
        self.map = [[Room('BLOCKED') for _ in range(self.length)] for _ in range(self.width)] # Rooms by default are blocked
        # These three fields will be initialized in populate_map()
        self.entrance_loc = None
        self.exit_loc = None
        self.room_list = None
        '''Populates the map, in addition to instantiating the entrance_loc, exit_loc, and room_list fields'''
        self.__populate_map()

    def get_width(self) -> int:
        """Returns width"""
        return self.width

    def get_length(self) -> int:
        """Returns length"""
        return self.length

    def get_room_list(self) -> list[tuple[int, int]]:
        """Returns deep copy of room coordinate list"""
        return deepcopy(self.room_list)

    def get_entrance_coords(self) -> tuple[int, int]:
        """Returns coordinates of entrance room"""
        return self.entrance_loc

    def get_exit_coords(self) -> tuple[int, int]:
        """Returns coordinates of exit room"""
        return self.exit_loc

    def fetch_room(self, x, y) -> Room:
        """Fetches room at given coordinates"""
        return self.map[x][y]

    def __str__(self):
        result = ""
        for row in self.map:
            result += " ".join(str(item) for item in row) + "\n"
        return result

    @staticmethod
    def __distance(a_x, a_y, b_x, b_y):
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
        """Responsible for populating a fresh map with an entrance, exit, pillar, et cetera"""
        entrance_x, entrance_y = (random.randint(0, self.length - 1), random.randint(0, self.width - 1))
        self.entrance_loc = (entrance_x, entrance_y) # Initializing a field!
        exit_x, exit_y = (random.randint(0, self.length - 1), random.randint(0, self.width - 1))
        distance = self.__distance(entrance_x, entrance_y, exit_x, exit_y)
        while distance <= self.length - 2:
            exit_x, exit_y = (random.randint(0, self.length - 1), random.randint(0, self.width - 1))
            distance = self.__distance(entrance_x, entrance_y, exit_x, exit_y)
        self.exit_loc = (exit_x, exit_y) # Initializing a field!
        self.map[entrance_x][entrance_y] = Room('ENTRANCE')
        self.map[exit_x][exit_y] = Room('EXIT')
        # self.__str__()
        # print('~')
        path = self.__path_to_exit(entrance_x, entrance_y, exit_x, exit_y)
        # self.__str__()
        # print('~')
        offshoot_rooms = self.__generate_offshoots(path)
        populated_rooms = path + offshoot_rooms
        self.room_list = populated_rooms # Initializing a field!
        for a in populated_rooms:
            x, y = (a[0], a[1])
            self.map[x][y].define_valid_directions(self.length, self.width, self.map, x, y)
        self.__place_pillar(populated_rooms, exit_x, exit_y)
        # print(self.__str__())

    def __generate_offshoots(self, path):
        offshoot_length = self.length - 2
        starting_points = random.sample(path[1:-1], offshoot_length - 1)
        directions = [(1,0),(-1,0),(0,1),(0,-1)]
        room_locations = []
        for x, y in starting_points:
            direction = random.choice(directions)
            if not self.__valid_direction_for_offshoot(direction, x, y):
                # If we know the direction won't work, reverse it before trying again
                direction = [-1 * direction[0], -1 * direction[1]]
            for i in range(offshoot_length):
                next_x, next_y = x + direction[0] * (i + 1), y + direction[1] * (i + 1)
                '''Validate coordinates and avoid an offshoot 'wrapping around' and generating on the opposite side
                of the map after hitting an edge (due to negative indexing).'''
                if (0 <= next_x < self.length and
                    0 <= next_y < self.width and
                    self.map[next_x][next_y].type == 'BLOCKED'):
                    self.map[next_x][next_y] = Room('RANDOM')
                    room_locations.append((next_x, next_y))
                else:
                    break
        return room_locations

    def __path_to_exit(self, entrance_x, entrance_y, exit_x, exit_y) -> list:
        """Responsible for creating and returning the path from the entrance to the exit of the dungeon"""
        current_x = entrance_x
        current_y = entrance_y
        path = []
        path.append((current_x, current_y))
        '''Path from entrance to exit horizontally, then vertically, creating random rooms along the way.
        The path from entrance to exit is stored to generate offshoots later.'''
        while current_y != exit_y:
            while current_x != exit_x:
                current_x = current_x + 1 if current_x < exit_x else current_x - 1
                self.map[current_x][current_y] = Room('RANDOM')
                path.append((current_x, current_y))
            current_y = current_y + 1 if current_y < exit_y else current_y - 1
            if current_x != exit_x or current_y != exit_y:
                self.map[current_x][current_y] = Room('RANDOM')
            path.append((current_x, current_y))
        return path

    def __place_pillar(self, rooms, exit_x, exit_y):
        """Places one pillar somewhere on the map (excluding entrance/exit)"""
        x, y = random.choice(rooms[1:]) # excludes entrance room
        while x == exit_x and y == exit_y: # still need to check for exit room, as it is not in set place
            x, y = random.choice(rooms)
        self.map[x][y] = Room('PILLAR')

    def __valid_direction_for_offshoot(self, direction, x, y) -> bool:
        new_x, new_y = x * direction[0], y * direction[1]
        return (0 <= new_x < self.length and 0 <= new_y < self.width and
                self.map[new_x][new_y].type == 'BLOCKED')

# for testing...
# d = Dungeon(3)