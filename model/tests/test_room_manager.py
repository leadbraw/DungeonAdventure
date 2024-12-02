import pytest
import json
from model.managers.room_manager import RoomManager

@pytest.fixture
def sample_rooms_data():
    return [
        (json.dumps([True, False, True, False]), "path/to/image1.png", 90),
        (json.dumps([False, True, False, True]), "path/to/image2.png", 180),
        (json.dumps([True, True, False, False]), "path/to/image3.png", 0)
    ]

@pytest.fixture
def manager(sample_rooms_data):
    RoomManager._instance = None  # Reset singleton
    return RoomManager.get_instance(sample_rooms_data)

def test_singleton_behavior(sample_rooms_data):
    instance1 = RoomManager.get_instance(sample_rooms_data)
    instance2 = RoomManager.get_instance()
    assert instance1 is instance2

def test_initialization(manager):
    assert len(manager.get_all_rooms()) == 3  # Three rooms loaded

def test_initialization_empty_data(manager):
    RoomManager._instance = None  # Reset singleton
    manager = RoomManager.get_instance([])
    assert len(manager.get_all_rooms()) == 0

def test_get_room_by_doors(manager):
    room = manager.get_room_by_doors([True, False, True, False])
    assert room["sprite_name"] == "image1"  # File name without path
    assert room["rotation"] == 90

    non_existent_room = manager.get_room_by_doors([False, False, False, False])
    assert non_existent_room is None

def test_get_all_rooms(manager):
    rooms = manager.get_all_rooms()
    assert len(rooms) == 3
    assert tuple([True, False, True, False]) in rooms

def test_duplicate_door_configurations(manager):
    duplicate_data = [
        (json.dumps([True, False, True, False]), "path/to/image1.png", 90),
        (json.dumps([True, False, True, False]), "path/to/image2.png", 180)  # Duplicate
    ]
    RoomManager._instance = None  # Reset singleton
    manager = RoomManager.get_instance(duplicate_data)

    room = manager.get_room_by_doors([True, False, True, False])
    assert room["sprite_name"] == "image2"  # File name without path
    assert room["rotation"] == 180  # Latest entry is retained

def test_invalid_door_configuration():
    invalid_data = [
        ("not a json", "path/to/image1.png", 90)  # Invalid JSON
    ]
    RoomManager._instance = None  # Reset singleton

    with pytest.raises(json.JSONDecodeError):
        RoomManager.get_instance(invalid_data)