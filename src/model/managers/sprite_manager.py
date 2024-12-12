import pygame


class SpriteManager:
    _instance = None  # Singleton instance

    @staticmethod
    def get_instance():
        """Static method to fetch the singleton instance."""
        if SpriteManager._instance is None:
            SpriteManager._instance = SpriteManager()
        return SpriteManager._instance

    def __init__(self):
        """Private constructor to prevent direct instantiation."""
        if SpriteManager._instance is not None:
            raise Exception("This class is a singleton! Use get_instance() to access it.")
        self.sprites = {}

    def preload_sprites(self, sprite_paths):
        """
        Preloads all sprites from the given dictionary.
        :param sprite_paths: Dictionary with {name: file_path}
        """
        for name, file_path in sprite_paths.items():
            self.load_sprite(name, file_path)

        loaded_count = len([s for s in self.sprites.values() if s is not None])

    def load_sprite(self, name, file_path):
        """
        Loads a sprite image if it has not been loaded already.
        :param name: Unique name for the sprite.
        :param file_path: Path to the sprite image file.
        """
        if name not in self.sprites:
            try:
                self.sprites[name] = pygame.image.load(file_path).convert_alpha()
            except Exception as e:
                print(f"[SpriteManager] Error loading sprite '{name}' from {file_path}: {e}")
                self.sprites[name] = None
        return self.sprites.get(name)

    def get_sprite(self, name):
        """
        Retrieves a sprite by name if it exists.
        :param name: Name of the sprite.
        :return: The original sprite or None if not found.
        """
        sprite = self.sprites.get(name)
        return sprite

    def get_transformed_sprite(self, name, flip_x=False, rotate=0):
        """
        Dynamically transforms a sprite without caching the result.
        :param name: Name of the sprite.
        :param flip_x: Flip horizontally if True.
        :param rotate: Rotation angle in degrees.
        :return: The transformed sprite or None if not found.
        """
        # Fetch the original sprite
        original_sprite = self.get_sprite(name)
        if not original_sprite:
            print(f"[SpriteManager] Sprite '{name}' not found for transformation.")
            return None

        transformed_sprite = original_sprite

        # Apply horizontal flip if needed
        if flip_x:
            transformed_sprite = pygame.transform.flip(transformed_sprite, True, False)

        # Apply rotation if needed
        if rotate != 0:
            transformed_sprite = pygame.transform.rotate(transformed_sprite, rotate)

        return transformed_sprite

    def clear_sprites(self):
        """Clears all loaded sprites and transformations."""
        self.sprites.clear()
