from enum import Enum
import random

'''
MONSTER: Room with monster, battle begins upon entry
BOSS: Room with boss enemy, battle begins upon entry
EXIT: Allows exiting the dungeon
ENTRANCE: Starting room
ITEM: Room containing an item, picked up upon entry
BLOCKED: Inaccessible room
'''
RoomType = Enum('MONSTER', 'BOSS', 'EXIT', 'ENTRANCE', 'ITEM', 'BLOCKED')

class Room:
    def __init__(self, room_type='BLOCKED'):
        self.type = room_type

    def set_type(self, new_type):
        self.type = new_type

class Dungeon:
    length=0
    width=0
    def __init__(self, map_length=5, map_width=5):
        self.length = map_length
        self.width = map_width
        self.map = [[Room('BLOCKED') for _ in range(map_length)] for _ in range(map_width)] # Rooms by default are blocked
        self.populate_map()

    def __populate_map(self):
        self.map[random.randint(0, self.length)][random.randint(0, self.width)] = Room('ENTRANCE')
        self.map[random.randint(0, self.length)][random.randint(0, self.width)] = Room('EXIT')
        # TODO: Enforce minimum distance between entrance and exit(?)
        # TODO: Generate path from entrance to exit, then generate offshoots, dead-ends, etc.
        # TODO: Ensure map is traversable, also enforce only one OO pillar being present on map.
