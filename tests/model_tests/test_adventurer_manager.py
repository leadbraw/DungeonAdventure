import pytest
from src.model.managers.adventurer_manager import AdventurerManager

@pytest.fixture
def sample_adventurers_data():
    return [
        (1, "Warrior", "Melee", 100, 10, 0.75, (10, 20), 0.2),
        (2, "Priest", "Healer", 80, 8, 0.6, (5, 15), 0.3),
        (3, "Thief", "Rogue", 90, 12, 0.8, (8, 18), 0.5)
    ]

@pytest.fixture
def manager(sample_adventurers_data):
    # Create a fresh instance for each test
    AdventurerManager._instance = None  # Reset singleton
    return AdventurerManager.get_instance(sample_adventurers_data)

def test_singleton_behavior(sample_adventurers_data):
    instance1 = AdventurerManager.get_instance(sample_adventurers_data)
    instance2 = AdventurerManager.get_instance()
    assert instance1 is instance2  # Both instances should be the same

def test_data_loading(manager):
    data = manager.get_adventurer_data()
    assert "Warrior" in data
    assert "Priest" in data
    assert "Thief" in data

def test_get_adventurer_data(manager):
    # Test retrieving all data
    all_data = manager.get_adventurer_data()
    assert len(all_data) == 3

    # Test retrieving specific data
    warrior_data = manager.get_adventurer_data("Warrior")
    assert warrior_data[1] == "Warrior"

    non_existent_data = manager.get_adventurer_data("Mage")
    assert non_existent_data is None

def test_load_active_adventurer(manager):
    # Load an existing adventurer
    manager.load_active_adventurer("Warrior")
    assert manager.active_adventurer[1] == "Warrior"

    # Try loading a non-existent adventurer
    manager.load_active_adventurer("Mage")
    assert manager.active_adventurer is None

def test_reset_active_adventurer(manager):
    # Load an adventurer and reset
    manager.load_active_adventurer("Warrior")
    assert manager.active_adventurer[1] == "Warrior"

    manager.reset_active_adventurer()
    assert manager.active_adventurer is None

def test_initialization_without_data():
    AdventurerManager._instance = None  # Reset singleton
    with pytest.raises(ValueError, match="AdventurerManager requires 'adventurers_data' for initialization."):
        AdventurerManager.get_instance()

def test_duplicate_adventurer_names(manager):
    duplicate_data = [
        (1, "Warrior", "Melee", 100, 10, 0.75, (10, 20), 0.2),
        (2, "Warrior", "Tank", 120, 8, 0.8, (15, 25), 0.3)
    ]
    AdventurerManager._instance = None  # Reset singleton
    manager = AdventurerManager.get_instance(duplicate_data)
    warrior_data = manager.get_adventurer_data("Warrior")
    assert warrior_data[0] == 2  # Ensure the latest entry is stored