import sqlite3
import json
import random
from copy import deepcopy
from .item import Item


class ItemFactory:
    def __init__(self, db_path='data/dungeon_game.db'):
        self.db_path = db_path
        self.item_cache = self.load_items()  # Cache items for quick access

    def load_items(self):
        """Loads all items from the database into a cache."""
        item_cache = {}
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        query = "SELECT id, name, description, attributes, temporary, unique FROM items"
        cursor.execute(query)

        for row in cursor.fetchall():
            item_id, name, description, attributes_json, temporary, unique = row
            attributes = json.loads(attributes_json)  # Parse JSON string into dictionary
            item_cache[name] = Item(item_id, name, description, attributes, bool(temporary), bool(unique))

        conn.close()
        return item_cache

    def get_item(self, item_name):
        """Returns a deep copy of an item by name."""
        item = self.item_cache.get(item_name)
        return deepcopy(item) if item else None

    def get_random_non_unique_item(self):
        """Returns a random non-unique item from the cache."""
        non_unique_items = [item for item in self.item_cache.values() if not item.my_item_unique]
        if not non_unique_items:
            return None  # No non-unique items available
        return deepcopy(random.choice(non_unique_items))
