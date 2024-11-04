from item import Item
from entities import Adventurer  # Import the Adventurer class
import sqlite3

class ItemManager:
    def __init__(self, the_db_path: str):
        self.my_db_path = the_db_path
        self.my_cache = {}  # Cache for items
        self.my_limited_instances = {}  # Track instances of limited items
        self.load_items()  # Populate the cache initially

    def load_items(self):
        """Load items from the database or test items into the cache."""
        try:
            # Attempt to load items from the database
            self.my_cache["Pillar of Encapsulation"] = Item.create_from_database(1, self.my_db_path)
            self.my_cache["Pillar of Polymorphism"] = Item.create_from_database(2, self.my_db_path)
            self.my_cache["Energy Drink"] = Item.create_from_database(3, self.my_db_path)
            self.my_cache["Code Spike"] = Item.create_from_database(4, self.my_db_path)

            # Initialize limited item counters with a max of 3 instances
            self.my_limited_instances = {
                "Energy Drink": 0,
                "Code Spike": 0
            }
        except sqlite3.Error as e:
            print(f"Database error: {e}. Loading test items instead.")
            self._load_test_items()

    def _load_test_items(self):
        """Load predefined test items into the cache if the database is unavailable."""
        test_items = Item.create_test_items()
        for item in test_items:
            self.my_cache[item.my_item_name] = item
            # Initialize each limited item in the counter if it's part of the test set
            if item.my_item_name in ["Energy Drink", "Code Spike"]:
                self.my_limited_instances[item.my_item_name] = 0

    def get_unique_item(self, the_item_name: str, the_adventurer: Adventurer):
        """Returns the unique item from the cache to place in the world
            if not already acquired by the adventurer."""

        # Dictionary mapping unique item names to the adventurer's bitfield check
        item_bitfield_checks = {
            # Need to implement constants in Adventurer
            "Pillar of Encapsulation": Adventurer.PILLAR_OF_ENCAPSULATION,
            "Pillar of Polymorphism": Adventurer.PILLAR_OF_POLYMORPHISM,
        }

        # Check if item is in cache and has a valid bitfield check
        if the_item_name in self.my_cache and the_item_name in item_bitfield_checks:
            # Need getter in Adventurer
            if not the_adventurer.has_acquired_pillar(item_bitfield_checks[the_item_name]):
                return self.my_cache[the_item_name].clone()
            else:
                raise ValueError(f"Unique item '{the_item_name}' has already been acquired.")
        raise ValueError(f"Unique item '{the_item_name}' not found in the cache.")

    def get_limited_item(self, the_item_name: str, max_limit=3):
        """Returns a clone of a limited-instance item if within the allowed instance limit."""
        if the_item_name in self.my_cache:
            # Check if the current count of the item is within the limit
            if self.my_limited_instances.get(the_item_name, 0) < max_limit:
                self.my_limited_instances[the_item_name] += 1
                return self.my_cache[the_item_name].clone()
            else:
                raise ValueError(f"Instance limit of {max_limit} reached for item '{the_item_name}'.")
        raise ValueError(f"Limited item '{the_item_name}' not found in the cache.")

    def return_limited_item(self, the_item_name: str):
        """Decreases the count of a limited-instance item when it is removed from the game world."""
        if the_item_name in self.my_limited_instances and self.my_limited_instances[the_item_name] > 0:
            self.my_limited_instances[the_item_name] -= 1
        else:
            raise ValueError(f"No active instances of '{the_item_name}' to return.")