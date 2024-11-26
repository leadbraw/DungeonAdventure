import pytest
from unittest.mock import patch
from model.entities.entities import Entity


# Mock subclass for testing
class TestEntity(Entity):
    def __init__(self, the_name, the_max_hp, the_attack_speed, the_hit_chance, the_damage_range):
        super().__init__(the_name, the_max_hp, the_attack_speed, the_hit_chance, the_damage_range)

    def _hit_response(self, the_dmg):
        # simulates behavior implemented in subclasses
        message = ""
        message += self._update_hp(the_dmg)

        return message


# Test initialization
def test_entity_initialization():
    # Test valid initialization
    entity = TestEntity("Test Entity", 100, 10,
                        0.8, (5, 10))
    assert entity.name == "Test Entity"
    assert entity.max_hp == 100
    assert entity.attack_speed == 10
    assert entity.hit_chance == 0.8
    assert entity.damage_range == (5, 10)
    assert entity.hp == 100


def test_invalid_name():
    # Test invalid name input
    entity = TestEntity("", 100, 10, 0.8, (5, 10))
    assert entity.name == "Unnamed Entity"


def test_invalid_max_hp():
    # Test invalid max_hp input (must be at least 1)
    entity = TestEntity("Test Entity", -5, 10, 0.8, (5, 10))
    assert entity.max_hp == 1
    assert entity.hp == 1


def test_invalid_attack_speed():
    # Test invalid attack speed (must be at least 1)
    entity = TestEntity("Test Entity", 100, -10, 0.8, (5, 10))
    assert entity.attack_speed == 1


def test_invalid_hit_chance():
    # Test invalid hit chance (must be between 0 and 1)
    entity = TestEntity("Test Entity", 100, 10, -0.2, (5, 10))
    assert entity.hit_chance == 0

    entity = TestEntity("Test Entity", 100, 10, 1.2, (5, 10))
    assert entity.hit_chance == 1


def test_invalid_damage_range():
    # Test invalid damage range (must be non-negative and a tuple of length 2)
    entity = TestEntity("Test Entity", 100, 10, 0.8, (-5, 10))
    assert entity.damage_range == (1, 10)

    entity = TestEntity("Test Entity", 100, 10, 0.8, (5, -10))
    assert entity.damage_range == (5, 5)

    entity = TestEntity("Test Entity", 100, 10, 0.8, (5,))
    assert entity.damage_range == (1, 1)


# Test is_alive
def test_is_alive():
    # Test when alive
    entity = TestEntity("Test Entity", 100, 10, 0.8, (5, 10))
    assert entity.is_alive() is True

    # Test when fainted (hp == 0)
    entity.hp = 0
    assert entity.is_alive() is False


# Test attack method
def test_attack():
    attacker = TestEntity("Attacker", 100, 10, 0.8, (5, 10))
    target = TestEntity("Target", 100, 10, 0.8, (5, 10))

    with patch('random.uniform', return_value=0.7):  # Force a hit
        message = attacker.attack(target)
        assert "Attacker hit Target" in message

    with patch('random.uniform', return_value=0.9):  # Force a miss
        message = attacker.attack(target)
        assert "Attacker missed the attack." in message


def test_attack_faints_target():
    attacker = TestEntity("Attacker", 100, 10, 0.8, (5, 10))
    target = TestEntity("Target", 5, 10, 0.8, (5, 10))

    # Target will faint after one attack
    with patch('random.uniform', return_value=0.7):  # Force a hit
        message = attacker.attack(target)
        print(message)
        assert "Target has fainted." in message


def test_attack_no_action_if_dead():
    attacker = TestEntity("Attacker", 100, 10, 0.8, (5, 10))
    target = TestEntity("Target", 10, 10, 0.8, (5, 10))
    target._update_hp(target.max_hp)

    message = attacker.attack(target)
    assert message == ""  # No actions should happen if target is dead


# Test _update_hp method
def test_update_hp():
    entity = TestEntity("Test Entity", 100, 10, 0.8, (5, 10))

    # Subtract 20 HP (but not below 0)
    entity._update_hp(20)
    assert entity.hp == 80

    # Subtract 100 HP (should be set to 0, faint)
    entity._update_hp(100)
    assert entity.hp == 0
    assert "Test Entity has fainted." in entity._update_hp(100)

    # Add 50 HP (but not above max HP)
    entity._update_hp(-50)
    assert entity.hp == 50

    # Try to go above max HP
    entity._update_hp(-200)
    assert entity.hp == entity.max_hp  # No more than max_hp


# Test faint message
def test_faint_message():
    entity = TestEntity("Test Entity", 100, 10, 0.8, (5, 10))
    faint_message = entity._has_fainted_msg()
    assert faint_message == "Test Entity has fainted.\n"
