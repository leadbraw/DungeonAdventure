import pytest
from unittest.mock import patch, Mock
from model.entities.adventurers import Adventurer, Warrior, Priest, Thief, Bard

# TODO special_attack edge cases and specific damage number testing

@pytest.fixture
def warrior():
    return Warrior("Mark", "Warrior", 100,
                   10, 0.75, (10, 20), 0.2)


@pytest.fixture
def priest():
    return Priest("Noah", "Priest", 100,
                  8, 0.6, (5, 15), 0.3)


@pytest.fixture
def thief():
    return Thief("Jayne", "Thief", 80,
                 12, 0.8, (8, 18), 0.5)


@pytest.fixture
def bard():
    return Bard("Sean", "Bard", 90, 9,
                0.7, (12, 25), 0.4)

@pytest.fixture
def adventurer():
    return Adventurer("Randy", "Adventurer", 100, 5,
                0.5, (10, 20), 0.5)


# Test Warrior's special action
def test_warrior_special_action(warrior, adventurer, mocker):
    mocker.patch('random.uniform', return_value=0)  # Force hit
    result = warrior.special_action(adventurer)

    assert "Mark uses Crushing Blow" in result
    assert "Mark hit" in result


# Test Priest's special action (healing)
def test_priest_special_action(priest):
    old_hp = 80 # create a measurable difference
    priest.hp = old_hp
    result = priest.special_action(priest)

    assert "Noah uses Divine Prayer and heals for " in result
    assert priest.hp > old_hp


# Test Thief's special action (Surprise Attack)
def test_thief_special_action(thief, mocker, adventurer):
    mocker.patch('random.uniform', return_value=1)  # Simulating a successful surprise attack
    result = thief.special_action(adventurer)

    assert "Jayne uses Surprise Attack" in result
    assert "Jayne gets an extra attack!" in result


# Test Bard's special action (Discombobulating Thought)
def test_bard_special_action(bard, adventurer):
    result = bard.special_action(adventurer)

    assert "Sean uses Discombobulating Thought" in result
    assert "Sean hit" in result
    assert "Sean takes" in result


# Test blocking behavior (hit or block)
@pytest.mark.parametrize("force_roll, hp_diff, message", [(0, 0, "blocked the attack"),
                                                          (1, 10, "")])
def test_blocking_behavior(adventurer, mocker, force_roll, hp_diff, message):
    mocker.patch('random.uniform', return_value=force_roll) # forcing a block (0.2 chance)
    old_hp = adventurer.hp
    result = adventurer._hit_response(10)  # Simulating a damage of 10 points

    assert message in result
    assert old_hp - adventurer.hp == hp_diff


# Test Adventurer's block chance setter
@pytest.mark.parametrize("chance_in, chance_out", [(1.2, 0.5),
                                                   (-0.1, 0.5),
                                                   (0.8, 0.8),
                                                   (0, 0)])
def test_block_chance_setter(adventurer, chance_in, chance_out):
    adventurer.block_chance = chance_in
    assert adventurer.block_chance == chance_out  # No change due to invalid value


# Test Adventurer's _hit_response method for invalid actions
def test_hit_response_for_dead_adventurer(adventurer):
    # Simulate a dead adventurer (hp = 0)
    adventurer.hp = 0
    result = adventurer._hit_response(10)

    # Should not perform any action and return empty response
    assert result == ""


# Test Adventurer's apply_buff method
def test_apply_buff_max_hp(adventurer):
    adventurer.apply_buff(20, "max_hp")
    assert adventurer.max_hp == 120  # Maximum HP should increase
    assert adventurer.hp == 120  # Current HP should also increase by the same amount


def test_apply_buff_block_chance(adventurer):
    assert adventurer.block_chance == 0.5  # Verify initial value
    adventurer.apply_buff(0.1, "block_chance")
    assert adventurer.block_chance == 0.6

    adventurer.apply_buff(0.5, "block_chance")  # Test cap at 1.0
    assert adventurer.block_chance == 1.0


def test_apply_buff_attack_damage(adventurer):
    assert adventurer.damage_range == (10, 20)  # Verify initial value
    adventurer.apply_buff(5, "attack_damage")
    assert adventurer.damage_range == (15, 25)


def test_apply_buff_attack_speed(adventurer):
    assert adventurer.attack_speed == 5  # Verify initial value
    adventurer.apply_buff(2, "attack_speed")
    assert adventurer.attack_speed == 7


def test_apply_buff_invalid_type(adventurer):
    adventurer.apply_buff(10, "invalid_type")
    # Ensure no changes are made
    assert adventurer.max_hp == 100
    assert adventurer.block_chance == 0.5
    assert adventurer.damage_range == (10, 20)
    assert adventurer.attack_speed == 5


# Test Adventurer's heal_from_item method
def test_heal_from_item(adventurer):
    adventurer.hp = 50  # Simulate damage
    adventurer.heal_from_item(30)
    assert adventurer.hp == 80  # Healed by 30


def test_heal_from_item_full_health(adventurer):
    adventurer.hp = 100  # Already at full health
    adventurer.heal_from_item(30)
    assert adventurer.hp == 100  # No change


def test_heal_from_item_overheal(adventurer):
    adventurer.hp = 90  # Almost full health
    adventurer.heal_from_item(20)
    assert adventurer.hp == 100  # Capped at max HP