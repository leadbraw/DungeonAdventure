import pytest
from unittest.mock import patch
from model.entities.monsters import Monster

# Fixtures for standard monster types
@pytest.fixture
def monster():
    return Monster("Goblin", "Normal", 50, 5, 0.75, (5, 10), 0.5, (5, 15))

@pytest.fixture
def ogre():
    return Monster("Ogre", "Normal", 200, 2, 0.6, (30, 60), 0.1, (30, 60))

@pytest.fixture
def gremlin():
    return Monster("Gremlin", "Normal", 70, 5, 0.8, (15, 30), 0.4, (20, 40))

@pytest.fixture
def skeleton():
    return Monster("Skeleton", "Normal", 100, 3, 0.8, (30, 50), 0.3, (30, 50))

@pytest.fixture
def elite():
    return Monster("Tom", "Elite", 250, 8, 0.85, (35, 55), 0.4, (38, 50))

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


def test_take_item_damage_already_defeated(skeleton):
    skeleton.hp = 0
    message = skeleton.take_item_damage(10)
    assert "is already defeated!" in message