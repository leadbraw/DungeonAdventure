import pygame

class SpriteManager:
    def __init__(self):
        self.sprites = {}  # Dictionary to store loaded sprites

    def load_sprite(self, name, file_path):
        """Loads a sprite image if it hasn’t been loaded already."""
        # TODO: Implement logic to load a sprite only once
        if name not in self.sprites:
            self.sprites[name] = pygame.image.load(file_path)
        return self.sprites[name]

    def get_sprite(self, name):
        """Retrieves a sprite by name if it exists."""
        # TODO: Implement retrieval logic or error handling if sprite not found
        return self.sprites.get(name)

    def clear_sprites(self):
        """Clears all loaded sprites, useful for transitions or reloading assets."""
        # TODO: Implement logic to clear loaded sprites
        self.sprites.clear()
