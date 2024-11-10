import random
from copy import deepcopy
from model.factories.item_factory import ItemFactory

class ItemManager:
    _instance = None  # Singleton instance

    @staticmethod
    def get_instance():
        if ItemManager._instance is None:
            ItemManager._instance = ItemManager()
        return ItemManager._instance

    def __init__(self):
        if ItemManager._instance is not None:
            raise Exception("This class is a singleton!")
        self.item_factory = ItemFactory()  # Initialize the factory
        self.unique_items_acquired = set()  # Track unique items acquired by the adventurer
        self.item_cache = self.item_factory.item_cache  # Cache for all items

    def get_unique_item(self, item_name):
        """Returns a unique item only if it hasn't been acquired before."""
        if item_name in self.unique_items_acquired:
            return None  # Item has already been acquired
        item = self.item_cache.get(item_name)
        if item and item.my_item_unique:
            self.unique_items_acquired.add(item_name)
            return deepcopy(item)  # Return a copy to avoid modifying the original
        return None

    def get_limited_item(self, item_name):
        """Returns a clone of a limited-instance item from the cache."""
        item = self.item_cache.get(item_name)
        return deepcopy(item) if item else None

    def get_random_non_unique_item(self):
        """Returns a random non-unique item from the cache."""
        non_unique_items = [item for item in self.item_cache.values() if not item.my_item_unique]
        if not non_unique_items:
            return None  # No non-unique items available
        return deepcopy(random.choice(non_unique_items))

    def reset_unique_items(self):
        """Resets tracking of unique items, useful for new games."""
        self.unique_items_acquired.clear()
