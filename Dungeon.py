from enum import Enum
import random
from math import floor, ceil

'''
MONSTER: Room with monster, battle begins upon entry
BOSS: Room with boss enemy, battle begins upon entry
EXIT: Allows exiting the dungeon
ENTRANCE: Starting room
ITEM: Room containing an item, picked up upon entry
BLOCKED: Inaccessible room
'''
RoomType = Enum('MONSTER', 'BOSS', 'EXIT', 'TRAP', 'ENTRANCE', 'ITEM', 'BLOCKED', 'RANDOM')

class Room:
    def __init__(self, room_type='BLOCKED'):
        self.type = (room_type if room_type != 'RANDOM'
                     else random.choices(population=['MONSTER', 'TRAP', 'BOSS', 'ITEM'],
                                         weights=[0.5, 0.2, 0.1, 0.2],
                                         k=1))
        '''
        50% chance for a random room to be a monster,
        20% for trap or item,
        10% for a boss/elite enemy
        '''

    def set_type(self, new_type):
        self.type = new_type

class Dungeon:
    length=0
    width=0

    def __init__(self, map_length=5, map_width=5):
        """Constructor for Dungeon. Instantiates it."""
        self.length = map_length
        self.width = map_width
        self.map = [[Room('BLOCKED') for _ in range(map_length)] for _ in range(map_width)] # Rooms by default are blocked
        self.__populate_map()

    def __populate_map(self):
        """Responsible for populating a fresh map with an entrance, exit, pillar, et cetera"""
        entrance_x, entrance_y = {random.randint(0, self.length), random.randint(0, self.width)}
        exit_x, exit_y = {random.randint(0, self.length), random.randint(0, self.width)}
        self.map[entrance_x][entrance_y] = Room('ENTRANCE')
        self.map[exit_x][exit_y] = Room('EXIT')
        path = self.__path_to_exit(entrance_x, entrance_y, exit_x, exit_y)
        self.__generate_offshoots(path)
        # TODO: Enforce minimum distance between entrance and exit(?)
        # TODO: Ensure map is traversable, also enforce only one OO pillar being present on map.

    def __path_to_exit(self, entrance_x, entrance_y, exit_x, exit_y) -> list:
        """Responsible for creating and returning the path from the entrance to the exit of the dungeon"""
        current_x = entrance_x
        current_y = entrance_y
        path = []
        '''Path from entrance to exit horizontally, then vertically, creating random rooms along the way.
        the path from entrance to exit is stored to generate offshoots later.'''
        while current_y != exit_y:
            while current_x != exit_x:
                current_x = current_x + 1 if current_x < exit_x else current_x - 1
                self.map[current_x][current_y] = Room('RANDOM')
                path.append((current_x, current_y))
            current_y = current_y + 1 if current_y < exit_y else current_y - 1
            self.map[current_x][current_y] = Room('RANDOM')
            path.append((current_x, current_y))

        return path

   # def __generate_offshoots(self, path):
        # max_offshoot_length = ceil((self.length + self.width) / 3))
        # min_offshoot_length = floor((self.length + self.width) / 4))
        # TODO: Implement creating offshoots, and making things reliant on floor # instead of map size.


