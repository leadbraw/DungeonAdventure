import pytest
from unittest.mock import patch
from src.model.managers.item_manager import ItemManager

@pytest.fixture
def sample_items_data():
    return [
        (1, "Pillar of OOP", "Grants encapsulation", "self", True, 0, 0, "stat_boost"),
        (2, "Energy Drink", "Restores energy", "self", False, 10, 50, "heal"),
        (3, "Magic Potion", "Restores health", "self", False, 5, 30, "heal"),
        (4, "Pillar of Inheritance", "Grants polymorphism", "self", True, 0, 0, "stat_boost")
    ]

@pytest.fixture
def manager(sample_items_data):
    # Reset the singleton
    ItemManager._instance = None
    return ItemManager.get_instance(sample_items_data)

def test_singleton_behavior(sample_items_data):
    instance1 = ItemManager.get_instance(sample_items_data)
    instance2 = ItemManager.get_instance()
    assert instance1 is instance2

def test_initialization_categorization(manager):
    assert len(manager.one_time_items) == 2  # Two unique items
    assert len(manager.other_items) == 2  # Two non-unique items

def test_initialization_empty_data(manager):
    ItemManager._instance = None  # Reset singleton
    manager = ItemManager.get_instance([])
    assert len(manager.one_time_items) == 0
    assert len(manager.other_items) == 0

def test_get_unique_item_data(manager):
    unique_item = manager.get_unique_item_data(1)
    assert unique_item["name"] in ["Pillar of OOP", "Pillar of Inheritance"]  # Unique items

def test_get_limited_item_data(manager):
    energy_drink = manager.get_limited_item_data("Energy Drink")
    assert energy_drink["name"] == "Energy Drink"

    non_existent = manager.get_limited_item_data("Non Existent Item")
    assert non_existent is None

def test_get_random_consumable_item_data(manager):
    with patch("random.choice", return_value={
        "name": "Energy Drink", "description": "Restores energy", "target": "self",
        "one_time_item": False, "effect_min": 10, "effect_max": 50, "buff_type": "heal"
    }):
        consumable = manager.get_random_consumable_item_data()
        assert consumable["name"] == "Energy Drink"

def test_reset_unique_items(manager):
    # Acquire a unique item
    unique_item = manager.get_unique_item_data(1)
    # Mark it acquired
    manager.mark_item_acquired(unique_item["name"])
    # Reset unique items
    manager.reset_unique_items()
    assert len(manager.unique_items_acquired) == 0

def test_duplicate_item_names(manager):
    duplicate_data = [
        (1, "Energy Drink", "Restores energy", "self", False, 10, 50, "heal"),
        (2, "Energy Drink", "Boosts speed", "self", False, 5, 10, "speed_boost")
    ]
    ItemManager._instance = None  # Reset singleton
    manager = ItemManager.get_instance(duplicate_data)

    energy_drink = manager.get_limited_item_data("Energy Drink")
    assert energy_drink["effect_max"] == 10  # Latest entry is returned

def test_boundary_effect_values(manager):
    boundary_data = [
        (1, "Weak Potion", "Does nothing", "self", False, 0, 0, "heal"),
        (2, "Overpowered Potion", "Restores everything", "self", False, 0, 9999, "heal")
    ]
    ItemManager._instance = None  # Reset singleton
    manager = ItemManager.get_instance(boundary_data)

    weak_potion = manager.get_limited_item_data("Weak Potion")
    assert weak_potion["effect_max"] == 0

    overpowered_potion = manager.get_limited_item_data("Overpowered Potion")
    assert overpowered_potion["effect_max"] == 9999