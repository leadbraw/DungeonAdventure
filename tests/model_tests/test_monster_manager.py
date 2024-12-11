import pytest
from unittest.mock import patch
from src.model.managers.monster_manager import MonsterManager

@pytest.fixture
def sample_monsters_data():
    return [
        (1, "Goblin", "Normal", 30, 5, 0.75, (3, 7), 0.1, (2, 4)),
        (2, "Orc", "Normal", 50, 4, 0.6, (5, 10), 0.2, (3, 6)),
        (3, "Dragon", "Elite", 300, 3, 0.9, (20, 50), 0.3, (10, 30))
    ]

@pytest.fixture
def manager(sample_monsters_data):
    # Reset the singleton
    MonsterManager._instance = None
    return MonsterManager.get_instance(sample_monsters_data)

def test_singleton_behavior(sample_monsters_data):
    instance1 = MonsterManager.get_instance(sample_monsters_data)
    instance2 = MonsterManager.get_instance()
    assert instance1 is instance2

def test_data_loading(manager):
    data = manager.monster_data
    assert "Normal" in data
    assert "Elite" in data
    assert len(data["Normal"]) == 2
    assert len(data["Elite"]) == 1

def test_get_monster_data_by_name(manager):
    goblin = manager.get_monster_data(monster_name="Goblin", monster_type="Normal")
    assert goblin[1] == "Goblin"

    dragon = manager.get_monster_data(monster_name="Dragon", monster_type="Elite")
    assert dragon[1] == "Dragon"

    non_existent = manager.get_monster_data(monster_name="Troll", monster_type="Normal")
    assert non_existent is None

def test_get_random_monster(manager):
    with patch("random.choice", return_value=(1, "Goblin", "Normal", 30, 5, 0.75, (3, 7), 0.1, (2, 4))):
        random_monster = manager.get_monster_data(monster_type="Normal")
        assert random_monster[1] == "Goblin"

def test_duplicate_monster_names(manager):
    duplicate_data = [
        (1, "Goblin", "Normal", 30, 5, 0.75, (3, 7), 0.1, (2, 4)),
        (2, "Goblin", "Normal", 40, 5, 0.75, (5, 9), 0.2, (4, 6))
    ]
    MonsterManager._instance = None  # Reset singleton
    manager = MonsterManager.get_instance(duplicate_data)

    goblin = manager.get_monster_data(monster_name="Goblin", monster_type="Normal")
    assert goblin[0] == 2  # Latest entry is returned


def test_random_monster_with_no_data(manager):
    MonsterManager._instance = None  # Reset singleton
    manager = MonsterManager.get_instance([(3, "Dragon", "Elite", 300, 3, 0.9, (20, 50), 0.3, (10, 30))])
    assert manager.get_monster_data(monster_type="Normal") is None

def test_mixed_valid_and_invalid_types(manager):
    mixed_data = [
        (1, "Goblin", "Normal", 30, 5, 0.75, (3, 7), 0.1, (2, 4)),
        (2, "Unknown", "Invalid", 0, 0, 0, (0, 0), 0, (0, 0))
    ]
    MonsterManager._instance = None  # Reset singleton
    manager = MonsterManager.get_instance(mixed_data)

    assert len(manager.monster_data["Normal"]) == 1
    assert "Invalid" not in manager.monster_data

def test_get_random_elite_monster(manager):
    with patch("random.choice", return_value=(3, "Dragon", "Elite", 300, 3, 0.9, (20, 50), 0.3, (10, 30))):
        elite_monster = manager.get_monster_data(monster_type="Elite")
        assert elite_monster[1] == "Dragon"

def test_empty_monster_data(manager):
    MonsterManager._instance = None  # Reset singleton
    manager = MonsterManager.get_instance([])
    assert manager.get_monster_data(monster_type="Normal") is None
    assert manager.get_monster_data(monster_type="Elite") is None