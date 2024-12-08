import pytest
from model.entities.item import Item


def test_item_initialization():
    # Test with all attributes provided
    item = Item(
        name="Health Potion",
        description="Restores health",
        target="adventurer",
        one_time_item=True,
        effect_min=10,
        effect_max=20,
        buff_type="health",
    )
    assert item.name == "Health Potion"
    assert item.description == "Restores health"
    assert item.target == "adventurer"
    assert item.one_time_item is True
    assert item.effect_min == 10
    assert item.effect_max == 20
    assert item.buff_type == "health"

    # Test with optional attributes not provided
    item = Item(
        name="Basic Potion",
        description="Just a basic item",
        target="adventurer",
        one_time_item=False,
    )
    assert item.name == "Basic Potion"
    assert item.description == "Just a basic item"
    assert item.target == "adventurer"
    assert item.one_time_item is False
    assert item.effect_min is None
    assert item.effect_max is None
    assert item.buff_type is None


def test_get_name():
    item = Item(
        name="Mana Potion",
        description="Restores mana",
        target="adventurer",
        one_time_item=True,
    )
    assert item.get_name() == "Mana Potion"