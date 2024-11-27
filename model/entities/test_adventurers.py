import pytest
from unittest.mock import patch, Mock
from model.entities.adventurers import Adventurer, Warrior, Priest, Thief, Bard

# Utility function to set up mock for random
def mock_random_uniform(return_value):
    """ Mock random.uniform to return a fixed value for testing purposes. """
    return patch('random.uniform', return_value=return_value)


@pytest.fixture
def warrior():
    return Warrior("Warrior", "Mark", 100, 10, 0.75, (10, 20), 0.2)


@pytest.fixture
def priest():
    return Priest("Priest", "Noah", 100, 8, 0.6, (5, 15), 0.3)


@pytest.fixture
def thief():
    return Thief("Thief", "Jayne", 80, 12, 0.8, (8, 18), 0.5)


@pytest.fixture
def bard():
    return Bard("Bard", "Sean", 90, 9, 0.7, (12, 25), 0.4)


# Test Warrior's special action
def test_warrior_special_action(warrior):
    with mock_random_uniform(1):  # Simulating a successful attack
        target = Mock(spec=Adventurer)  # Mock target to simulate hit response
        target.is_alive.return_value = True
        result = warrior.special_action(target)

        assert "Warrior uses Crushing Blow" in result
        assert "Warrior hit" in result


# Test Priest's special action (healing)
def test_priest_special_action(priest):
    with mock_random_uniform(0.5):  # Simulating heal between 0.4 and 0.7 of max_hp
        target = Mock(spec=Adventurer)  # Mock target to simulate hit response
        target.is_alive.return_value = True
        result = priest.special_action(target)

        assert "Priest uses Divine Prayer" in result
        assert "heals for" in result


# Test Thief's special action (Surprise Attack)
def test_thief_special_action(thief):
    with mock_random_uniform(0.3):  # Simulating a successful surprise attack
        target = Mock(spec=Adventurer)  # Mock target to simulate hit response
        target.is_alive.return_value = True
        result = thief.special_action(target)

        assert "Thief uses Surprise Attack" in result
        assert "Thief gets an extra attack!" in result


# Test Bard's special action (Discombobulating Thought)
def test_bard_special_action(bard):
    with mock_random_uniform(0.6):  # Simulating a successful attack with a damage range of 30-70
        target = Mock(spec=Adventurer)  # Mock target to simulate hit response
        target.is_alive.return_value = True
        result = bard.special_action(target)

        assert "Bard uses Discombobulating Thought" in result
        assert "Bard hit" in result
        assert "Bard takes" in result


# Test blocking behavior (hit or block)
def test_blocking_behavior(warrior):
    with patch('random.uniform', return_value=0.1):  # Simulating a successful block (0.2 chance)
        warrior._block_chance = 0.2
        target = Mock(spec=Adventurer)
        target.is_alive.return_value = True
        result = warrior._hit_response(10)  # Simulating a damage of 10 points

        assert "blocked the attack" in result

    with patch('random.uniform', return_value=0.9):  # Simulating a failed block
        warrior._block_chance = 0.2
        result = warrior._hit_response(10)  # Simulating a damage of 10 points

        assert "hit" in result


# Test Adventurer's block chance setter and getter
def test_block_chance_setter_and_getter():
    adventurer = Adventurer("Adventurer", "warrior", 100, 10, 0.75, (5, 10), 0.4)

    # Test the getter
    assert adventurer.block_chance == 0.4

    # Test the setter with a valid value
    adventurer.block_chance = 0.5
    assert adventurer.block_chance == 0.5

    # Test the setter with an invalid value (should not update if outside range)
    adventurer.block_chance = 1.2
    assert adventurer.block_chance == 0.5  # No change due to invalid value

    adventurer.block_chance = -0.1
    assert adventurer.block_chance == 0.5  # No change due to invalid value


# Test Adventurer's _hit_response method for invalid actions
def test_hit_response_for_dead_adventurer():
    adventurer = Adventurer("Dead Adventurer", "dead", 0, 0, 0.5, (0, 0), 0.2)

    # Simulate a dead adventurer (hp = 0)
    result = adventurer._hit_response(10)

    # Should not perform any action and return empty response
    assert result == ""


# Test if attack works correctly when calling attack from Adventurer or subclass
def test_attack_behavior(warrior, priest):
    # Simulate random outcome of attack
    with mock_random_uniform(0.4):  # Simulate a hit chance of 0.75
        target = Mock(spec=Adventurer)
        target.is_alive.return_value = True
        result = warrior.attack(target)

        assert "hit" in result
        assert "for" in result

    with mock_random_uniform(0.8):  # Simulate a miss
        target = Mock(spec=Adventurer)
        target.is_alive.return_value = True
        result = warrior.attack(target)

        assert "missed" in result
