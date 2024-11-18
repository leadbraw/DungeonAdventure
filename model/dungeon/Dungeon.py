import random
from colorama import Fore, Style
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
        if room_type == 'RANDOM':
            # First roll: Decide the major category
            main_category = random.choices(
                population=['ENTITY', 'EVENT', 'EMPTY'],
                weights=[0.4, 0.4, 0.2],  # 40% entity, 40% event, 20% empty
                k=1
            )[0]

            if main_category == 'ENTITY':
                # 80% chance for 'MONSTER', 20% for 'ELITE'
                self.type = random.choices(
                    population=['MONSTER', 'ELITE'],
                    weights=[0.8, 0.2],
                    k=1
                )[0]

            elif main_category == 'EVENT':
                # 50% chance for 'TRAP', 50% for 'ITEM'
                self.type = random.choices(
                    population=['TRAP', 'ITEM'],
                    weights=[0.5, 0.5],
                    k=1
                )[0]

            elif main_category == 'EMPTY':
                # Directly assign 'EMPTY'
                self.type = 'EMPTY'
        else:
            # Assign fixed room type for non-random cases
            self.type = room_type

        self.valid_directions = [False, False, False, False]  # Up, Right, Down, Left

    def __str__(self):
        # Assign colors to specific room types
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
        self.entrance_loc = None
        self.exit_loc = None
        self.room_list = None
        self.non_blocked_rooms = []  # List to store non-blocked room coordinates
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

    def get_non_blocked_rooms(self) -> list[tuple[int, int]]:
        """Returns a deep copy of the list of non-blocked room coordinates."""
        return deepcopy(self.non_blocked_rooms)

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
        essential_rooms = []  # Store the entrance, exit, and pillar here
        other_rooms = []  # Temporarily store other non-blocked rooms here

        # Place entrance
        entrance_x, entrance_y = (random.randint(0, self.length - 1), random.randint(0, self.width - 1))
        self.entrance_loc = (entrance_x, entrance_y)
        self.map[entrance_x][entrance_y] = Room('ENTRANCE')
        essential_rooms.append((entrance_x, entrance_y))

        # Place exit
        exit_x, exit_y = (random.randint(0, self.length - 1), random.randint(0, self.width - 1))
        distance = self.__distance(entrance_x, entrance_y, exit_x, exit_y)
        while distance <= self.length - 2:
            exit_x, exit_y = (random.randint(0, self.length - 1), random.randint(0, self.width - 1))
            distance = self.__distance(entrance_x, entrance_y, exit_x, exit_y)
        self.exit_loc = (exit_x, exit_y)
        self.map[exit_x][exit_y] = Room('EXIT')
        essential_rooms.append((exit_x, exit_y))

        # Generate path and offshoots
        path = self.__path_to_exit(entrance_x, entrance_y, exit_x, exit_y)
        offshoot_rooms = self.__generate_offshoots(path)
        populated_rooms = path + offshoot_rooms
        self.room_list = populated_rooms  # Initialize the room list

        # Add all other rooms to other_rooms list
        for a in populated_rooms:
            x, y = a
            self.map[x][y].define_valid_directions(self.length, self.width, self.map, x, y)
            other_rooms.append((x, y))

        # Place pillar
        self.__place_pillar(populated_rooms, exit_x, exit_y)
        pillar_coords = next(
            (x, y) for x, y in populated_rooms if self.map[x][y].get_type() == 'PILLAR'
        )
        essential_rooms.append(pillar_coords)  # Add pillar as the third room in the list

        # Finalize the non_blocked_rooms list
        self.non_blocked_rooms = essential_rooms + [room for room in other_rooms if room not in essential_rooms]

    def __generate_offshoots(self, path):
        offshoot_length = self.length - 2
        starting_points = random.sample(path[1:-1], offshoot_length - 1)
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        room_locations = []
        for x, y in starting_points:
            direction = random.choice(directions)
            if not self.__valid_direction_for_offshoot(direction, x, y):
                direction = [-1 * direction[0], -1 * direction[1]]
            for i in range(offshoot_length):
                next_x, next_y = x + direction[0] * (i + 1), y + direction[1] * (i + 1)
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
        path = [(current_x, current_y)]
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
        x, y = random.choice(rooms[1:])  # excludes entrance room
        while x == exit_x and y == exit_y:
            x, y = random.choice(rooms)
        self.map[x][y] = Room('PILLAR')
        if (x, y) not in self.non_blocked_rooms:
            self.non_blocked_rooms.append((x, y))  # Add to non-blocked list

    def __valid_direction_for_offshoot(self, direction, x, y) -> bool:
        new_x, new_y = x + direction[0], y + direction[1]
        return (0 <= new_x < self.length and 0 <= new_y < self.width and
                self.map[new_x][new_y].type == 'BLOCKED')

# for testing...
d = Dungeon(1)
print(d.__str__())
print(f"Non-blocked rooms ({len(d.non_blocked_rooms)}): {d.non_blocked_rooms}")