import pytest
from unittest.mock import patch
from model.entities.monsters import Monster

# Fixtures for standard monster types
@pytest.fixture
def monster():
    return Monster("Goblin", "Normal", 50, 5, 0.75, (5, 10), 0.5, (5, 15))

@pytest.fixture
def elite():
    return Monster("Tom", "Elite", 250, 8, 0.85, (35, 55), 0.4, (38, 50))

# Test regen behavior
@pytest.mark.parametrize("force_roll, heal, message", [(0, 5, "healed"),
                                                       (1, 0, "")])
def test_regen_behavior(monster, mocker, force_roll, heal, message):
    mocker.patch('random.uniform', return_value=force_roll) # forcing a regen
    mocker.patch('random.randint', return_value=heal)  # forcing a regen
    result = monster._hit_response(10)  # Simulating a damage of 10 points

    assert message in result
    assert monster.max_hp - monster.hp == 10 - heal


# Test regen chance setter
@pytest.mark.parametrize("chance_in, chance_out", [(1.2, 0.5),
                                                   (-0.1, 0.5),
                                                   (0.8, 0.8),
                                                   (0, 0)])
def test_regen_chance_setter(monster, chance_in, chance_out):
    monster.heal_chance = chance_in
    print(monster.heal_chance)
    assert monster.heal_chance == chance_out


# Test heal range setter
@pytest.mark.parametrize("range_in, range_out", [((-5, 10), (1, 10)),
                                                 ((5, -10), (5, 5)),
                                                 ((5, ), (1, 1)),
                                                 ((5, 10), (5, 10))])
def test_heal_range_setter(monster, range_in, range_out):
    monster.damage_range = range_in
    assert monster.damage_range == range_out


# Test Adventurer's _hit_response method for invalid actions
def test_hit_response_for_dead_monster(monster):
    # Simulate a dead adventurer (hp = 0)
    monster.hp = 0
    result = monster._hit_response(10)

    # Should not perform any action and return empty response
    assert result == ""

#Item interactions
def test_take_item_damage(elite):
    elite.hp = 20
    message = elite.take_item_damage(15)
    assert elite.hp == 5
    assert "takes 15 item damage." in message


def test_take_item_damage_kill(monster):
    monster.hp = 10
    message = monster.take_item_damage(15)
    assert monster.hp == 0
    assert "takes 15 item damage." in message
    assert "has been defeated!" in message


def test_take_item_damage_already_defeated(monster):
    monster.hp = 0
    message = monster.take_item_damage(10)
    assert "is already defeated!" in message