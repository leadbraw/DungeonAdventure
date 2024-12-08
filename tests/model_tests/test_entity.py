import pytest
from model.entities.entities import Entity


# Mock subclass for testing
class MockEntity(Entity):
    def __init__(self, the_name, the_max_hp, the_attack_speed, the_hit_chance, the_damage_range):
        super().__init__(the_name, the_max_hp, the_attack_speed, the_hit_chance, the_damage_range)

    def _hit_response(self, the_dmg):
        # simulates behavior implemented in subclasses
        message = ""
        message += self._update_hp(the_dmg)

        return message


@pytest.fixture
def entity():
    return MockEntity("Test Entity", 100, 10,
                      0.8, (5, 10))
@pytest.fixture
def attacker():
    return MockEntity("Attacker", 100, 10,
                      0.8, (5, 10))

@pytest.fixture
def target():
    return MockEntity("Target", 100, 10,
                      0.8, (5, 10))


# Test initialization
def test_entity_initialization():
    # Test valid initialization
    entity = MockEntity("Test Entity", 100, 10,
                        0.8, (5, 10))
    assert entity.name == "Test Entity"
    assert entity.max_hp == 100
    assert entity.attack_speed == 10
    assert entity.hit_chance == 0.8
    assert entity.damage_range == (5, 10)
    assert entity.hp == 100


def test_invalid_name(entity):
    # Test invalid name input
    entity.name = ""
    assert entity.name == "Unnamed Entity"


def test_invalid_max_hp(entity):
    # Test invalid max_hp input (must be at least 1)
    entity.max_hp = -5
    assert entity.max_hp == 1
    assert entity.hp == 1


def test_invalid_attack_speed(entity):
    # Test invalid attack speed (must be at least 1)
    entity.attack_speed = -10
    assert entity.attack_speed == 1


@pytest.mark.parametrize("chance_in, chance_out", [(-0.2, 0.1),
                                                   (1.2, 1)])
def test_invalid_hit_chance(chance_in, chance_out, entity):
    # Test invalid hit chance (must be between 0 and 1)
    entity.hit_chance = chance_in
    assert entity.hit_chance == chance_out


@pytest.mark.parametrize("range_in, range_out", [((-5, 10), (1, 10)),
                                                 ((5, -10), (5, 5)),
                                                 ((5, ), (1, 1))])
def test_invalid_damage_range(range_in, range_out, entity):
    # Test invalid damage range (must be non-negative and a tuple of length 2)
    entity.damage_range = range_in
    assert entity.damage_range == range_out


# Test is_alive
@pytest.mark.parametrize("hp_val, status", [(100, True),
                                            (0, False)])
def test_is_alive(hp_val, status, entity):
    entity.hp = hp_val
    assert entity.is_alive() is status


# Test attack method
@pytest.mark.parametrize("force_roll, attack_outcome", [(0, "Attacker hit Target"),
                                                        (1, "Attacker missed the attack")])
def test_attack(force_roll, attack_outcome, attacker, target, mocker):
    mocker.patch('random.uniform', return_value=force_roll)
    message = attacker.attack(target)
    assert attack_outcome in message


def test_attack_kills_target(attacker, target, mocker):
    target.hp = 5
    mocker.patch('random.uniform', return_value=0)  # Force hit
    message = attacker.attack(target)
    assert "Target has fainted" in message


def test_attack_no_action_if_dead(attacker, target):
    target._update_hp(target.max_hp)

    message = attacker.attack(target)
    assert message == ""  # No actions should happen if target is dead


# Test _update_hp method
@pytest.mark.parametrize("hp_in, hp_should", [(20, 60),
                                              (100, 0),
                                              (-50, 100),
                                              (-10, 90)])
def test_update_hp(hp_in, hp_should, entity):
    # increase max for healing testing
    entity.hp = 80
    # Subtract in value
    entity._update_hp(hp_in)
    assert entity.hp == hp_should


# Test faint message
def test_faint_message(entity):
    faint_message = entity._has_fainted_msg()
    assert faint_message == "Test Entity has fainted."
