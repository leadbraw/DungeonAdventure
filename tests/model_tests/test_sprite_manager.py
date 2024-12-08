import pytest
from unittest.mock import patch, MagicMock
from src.model.managers.sprite_manager import SpriteManager


@pytest.fixture
def mock_pygame():
    """Mock the pygame module."""
    with patch("model.managers.sprite_manager.pygame") as mock_pygame:
        # Mock image loading and transformation methods
        mock_image = MagicMock()
        mock_pygame.image.load.return_value = mock_image
        mock_image.convert_alpha.return_value = mock_image

        mock_transform = mock_pygame.transform
        mock_transform.flip.return_value = mock_image
        mock_transform.rotate.return_value = mock_image

        yield mock_pygame


@pytest.fixture
def sprite_manager():
    """Reset the singleton and return a fresh instance."""
    SpriteManager._instance = None
    return SpriteManager.get_instance()


def test_singleton_behavior(sprite_manager):
    instance1 = sprite_manager
    instance2 = SpriteManager.get_instance()
    assert instance1 is instance2


def test_preload_sprites(sprite_manager, mock_pygame):
    sprite_paths = {
        "sprite1": "path/to/sprite1.png",
        "sprite2": "path/to/sprite2.png"
    }
    sprite_manager.preload_sprites(sprite_paths)
    assert len(sprite_manager.sprites) == 2
    mock_pygame.image.load.assert_any_call("path/to/sprite1.png")
    mock_pygame.image.load.assert_any_call("path/to/sprite2.png")


def test_load_sprite(sprite_manager, mock_pygame):
    sprite = sprite_manager.load_sprite("sprite1", "path/to/sprite1.png")
    assert sprite is not None
    mock_pygame.image.load.assert_called_once_with("path/to/sprite1.png")


def test_load_sprite_error_handling(sprite_manager, mock_pygame):
    mock_pygame.image.load.side_effect = Exception("Error loading image")
    sprite = sprite_manager.load_sprite("sprite1", "path/to/invalid.png")
    assert sprite is None


def test_get_sprite(sprite_manager, mock_pygame):
    sprite_manager.load_sprite("sprite1", "path/to/sprite1.png")
    sprite = sprite_manager.get_sprite("sprite1")
    assert sprite is not None
    assert sprite_manager.get_sprite("nonexistent") is None


def test_get_transformed_sprite(sprite_manager, mock_pygame):
    sprite_manager.load_sprite("sprite1", "path/to/sprite1.png")
    transformed_sprite = sprite_manager.get_transformed_sprite("sprite1", flip_x=True, rotate=90)
    assert transformed_sprite is not None
    mock_pygame.transform.flip.assert_called_once_with(mock_pygame.image.load(), True, False)
    mock_pygame.transform.rotate.assert_called_once_with(mock_pygame.image.load(), 90)


def test_clear_sprites(sprite_manager):
    sprite_manager.sprites = {"sprite1": MagicMock(), "sprite2": MagicMock()}
    sprite_manager.clear_sprites()
    assert len(sprite_manager.sprites) == 0


def test_duplicate_sprite_name(sprite_manager, mock_pygame):
    sprite_manager.load_sprite("sprite1", "path/to/sprite1.png")
    sprite1_first = sprite_manager.get_sprite("sprite1")
    sprite_manager.load_sprite("sprite1", "path/to/sprite1.png")
    sprite1_second = sprite_manager.get_sprite("sprite1")
    assert sprite1_first == sprite1_second
    mock_pygame.image.load.assert_called_once_with("path/to/sprite1.png")


def test_preload_empty_sprites(sprite_manager):
    sprite_manager.preload_sprites({})
    assert len(sprite_manager.sprites) == 0


def test_transform_nonexistent_sprite(sprite_manager):
    transformed_sprite = sprite_manager.get_transformed_sprite("nonexistent", flip_x=True, rotate=90)
    assert transformed_sprite is None


def test_clear_empty_sprites(sprite_manager):
    sprite_manager.clear_sprites()
    assert len(sprite_manager.sprites) == 0


def test_load_invalid_sprite_path(sprite_manager, mock_pygame):
    mock_pygame.image.load.side_effect = FileNotFoundError("File not found")
    sprite = sprite_manager.load_sprite("sprite1", "invalid/path/to/sprite1.png")
    assert sprite is None
    mock_pygame.image.load.assert_called_once_with("invalid/path/to/sprite1.png")