import random
import pytest
from model.dungeon.dungeon import Dungeon

@pytest.fixture
def dungeon_1():
    return Dungeon(1)

@pytest.fixture
def dungeon_2():
    return Dungeon(2)

@pytest.fixture
def dungeon_3():
    return Dungeon(3)

@pytest.fixture
def dungeon_4():
    return Dungeon(4)

def test_proper_width_1(dungeon_1):
    assert dungeon_1.get_width() == 5

def test_proper_length_1(dungeon_1):
    assert dungeon_1.get_length() == 5

def test_proper_width_2(dungeon_2):
    assert dungeon_2.get_width() == 6

def test_proper_length_2(dungeon_2):
    assert dungeon_2.get_length() == 6

def test_proper_width_3(dungeon_3):
    assert dungeon_3.get_width() == 7

def test_proper_length_3(dungeon_3):
    assert dungeon_3.get_length() == 7

def test_proper_width_4(dungeon_4):
    assert dungeon_4.get_width() == 8

def test_proper_length_4(dungeon_4):
    assert dungeon_4.get_length() == 8

def test_room_list(dungeon_1, dungeon_2, dungeon_3, dungeon_4):
    dungeons = [dungeon_1, dungeon_2, dungeon_3, dungeon_4]
    for dungeon in dungeons:
        for x, y in dungeon.get_room_list():
            assert dungeon.fetch_room(x, y).type != "BLOCKED"

def test_reveal_adjacent_rooms(dungeon_1, dungeon_2, dungeon_3, dungeon_4):
    dungeons = [dungeon_1, dungeon_2, dungeon_3, dungeon_4]
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)]
    for dungeon in dungeons:
        x, y = random.randint(0, dungeon.get_length() - 1), random.randint(0, dungeon.get_width() - 1)
        dungeon.reveal_adjacent_rooms(x, y)
        for pair in directions:
            new_x, new_y = x + pair[0], y + pair[1]
            assert dungeon.fetch_room(new_x, new_y).get_visited


def test_traversable(dungeon_1, dungeon_2, dungeon_3, dungeon_4):
    dungeons = [dungeon_1, dungeon_2, dungeon_3, dungeon_4]
    for dungeon in dungeons: # DFS
        coords = dungeon.get_entrance_coords()
        visited = set()
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        neighbors = []
        stack = [coords]
        while len(stack):
            coords = stack[-1]
            stack.pop()
            if coords not in visited:
                visited.add(coords)
            for x, y in directions:
                new_coords = (coords[0] + x, coords[1] + y)
                new_room = None
                if 0 <= new_coords[0] < dungeon.get_length() and 0 <= new_coords[1] < dungeon.get_width():
                    new_room = dungeon.fetch_room(*new_coords)
                if new_room is not None and new_room.get_type() != "BLOCKED":
                    neighbors.append(new_coords)
            for pair in neighbors:
                if pair not in visited:
                    stack.append(pair)
        assert dungeon.get_entrance_coords() in visited
        assert dungeon.get_exit_coords() in visited
        assert dungeon.get_pillar_coords() in visited
