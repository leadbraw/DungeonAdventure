import re
import pytest
from model.factories.item_factory import ItemFactory
from model.entities.item import Item


@pytest.fixture
def raw_item_data():
    return {
        "name": "Health Potion",
        "description": "Restores health",
        "target": "self",
        "one_time_item": 1,
        "effect_min": 10,
        "effect_max": 20,
        "buff_type": None,
    }


def test_singleton_behavior():
    instance1 = ItemFactory.get_instance()
    instance2 = ItemFactory.get_instance()
    assert instance1 is instance2

    # Attempting direct instantiation should raise an exception
    with pytest.raises(Exception, match=re.escape("This class is a singleton! Use get_instance() to access the instance.")):
        ItemFactory()


def test_create_item_from_raw(raw_item_data):
    item = ItemFactory.create_item_from_raw(raw_item_data)

    assert isinstance(item, Item)
    assert item.name == raw_item_data["name"]
    assert item.description == raw_item_data["description"]
    assert item.target == raw_item_data["target"]
    assert item.one_time_item is True
    assert item.effect_min == raw_item_data["effect_min"]
    assert item.effect_max == raw_item_data["effect_max"]
    assert item.buff_type == raw_item_data["buff_type"]


def test_create_item_from_raw_missing_data():
    # Missing required fields in raw data
    with pytest.raises(KeyError):
        ItemFactory.create_item_from_raw({"name": "Health Potion"})


def test_create_item_from_raw_no_data():
    # No raw data provided
    with pytest.raises(ValueError, match="No raw data provided to create an item."):
        ItemFactory.create_item_from_raw(None)


def test_create_unique_item(raw_item_data):
    item = ItemFactory.create_unique_item(raw_item_data)

    assert isinstance(item, Item)
    assert item.one_time_item is True


def test_create_standard_item(raw_item_data):
    item = ItemFactory.create_standard_item(raw_item_data)

    assert isinstance(item, Item)
    assert item.one_time_item is False


def test_create_item_from_minimal_raw_data():
    minimal_raw_data = {
        "name": "Basic Item",
        "description": "Just a basic item",
        "target": "self",
        "one_time_item": 0,
        "effect_min": 0,
        "effect_max": 0,
        "buff_type": None,
    }
    item = ItemFactory.create_item_from_raw(minimal_raw_data)
    assert item.name == minimal_raw_data["name"]
    assert item.description == minimal_raw_data["description"]
    assert item.target == minimal_raw_data["target"]
    assert item.one_time_item is False
    assert item.effect_min == minimal_raw_data["effect_min"]
    assert item.effect_max == minimal_raw_data["effect_max"]
    assert item.buff_type == minimal_raw_data["buff_type"]


def test_create_item_with_extreme_values():
    extreme_raw_data = {
        "name": "Overpowered Item",
        "description": "An item with extreme values",
        "target": "enemy",
        "one_time_item": 1,
        "effect_min": -1000,
        "effect_max": 1000000,
        "buff_type": "damage",
    }
    item = ItemFactory.create_item_from_raw(extreme_raw_data)
    assert item.effect_min == extreme_raw_data["effect_min"]
    assert item.effect_max == extreme_raw_data["effect_max"]


def test_create_item_with_invalid_data_types():
    invalid_raw_data = {
        "name": "Glitched Item",
        "description": "An item with invalid types",
        "target": "self",
        "one_time_item": "not_a_boolean",  # Invalid type
        "effect_min": 1,
        "effect_max": 2,
        "buff_type": None,
    }

    with pytest.raises(TypeError, match="Invalid type for 'one_time_item'"):
        ItemFactory.create_item_from_raw(invalid_raw_data)


def test_create_standard_vs_unique_item(raw_item_data):
    standard_item = ItemFactory.create_standard_item(raw_item_data)
    unique_item = ItemFactory.create_unique_item(raw_item_data)

    assert standard_item.one_time_item is False
    assert unique_item.one_time_item is True


def test_create_multiple_items():
    raw_item_data_1 = {
        "name": "Health Potion",
        "description": "Restores health",
        "target": "self",
        "one_time_item": 1,
        "effect_min": 10,
        "effect_max": 20,
        "buff_type": None,
    }
    raw_item_data_2 = {
        "name": "Mana Potion",
        "description": "Restores mana",
        "target": "self",
        "one_time_item": 0,
        "effect_min": 5,
        "effect_max": 10,
        "buff_type": None,
    }
    item1 = ItemFactory.create_item_from_raw(raw_item_data_1)
    item2 = ItemFactory.create_item_from_raw(raw_item_data_2)

    assert item1.name == "Health Potion"
    assert item2.name == "Mana Potion"
    assert item1 is not item2


def test_create_item_with_buff_type():
    raw_item_data = {
        "name": "Strength Potion",
        "description": "Increases strength",
        "target": "self",
        "one_time_item": 1,
        "effect_min": 10,
        "effect_max": 30,
        "buff_type": "strength",
    }
    item = ItemFactory.create_item_from_raw(raw_item_data)
    assert item.buff_type == "strength"


def test_create_item_with_empty_strings():
    raw_item_data = {
        "name": "",
        "description": "",
        "target": "self",
        "one_time_item": 0,
        "effect_min": 0,
        "effect_max": 0,
        "buff_type": None,
    }
    item = ItemFactory.create_item_from_raw(raw_item_data)
    assert item.name == ""
    assert item.description == ""


def test_bulk_item_creation():
    raw_item_data = {
        "name": "Generic Item",
        "description": "Used in bulk testing",
        "target": "self",
        "one_time_item": 0,
        "effect_min": 1,
        "effect_max": 5,
        "buff_type": None,
    }
    items = [ItemFactory.create_item_from_raw(raw_item_data) for _ in range(100)]
    assert len(items) == 100
    assert all(isinstance(item, Item) for item in items)