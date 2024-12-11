import random


class ItemManager:
    _instance = None  # Singleton instance

    @staticmethod
    def get_instance(items_data=None):
        """
        Retrieve the singleton instance of ItemManager, initializing it if necessary.
        :param items_data: List of tuples representing items from the database (used only on first initialization).
        :return: The singleton instance of ItemManager.
        """
        if ItemManager._instance is None:
            if items_data is None:
                raise ValueError("ItemManager requires 'items_data' for initialization.")
            ItemManager._instance = ItemManager(items_data)
        return ItemManager._instance

    def __init__(self, items_data):
        if ItemManager._instance is not None:
            raise Exception("This class is a singleton! Use get_instance() to access the instance.")

        # Separate raw item data into two dictionaries
        self.one_time_items = {}  # Items that can only be acquired once
        self.other_items = {}  # Items that can be acquired multiple times

        for item_name, data in self.one_time_items.items():
            if not data["name"]:
                raise ValueError(f"Missing name for one-time item: {data}")
        for item_name, data in self.other_items.items():
            if not data["name"]:
                raise ValueError(f"Missing name for limited item: {data}")

        # Populate dictionaries from items_data
        for row in items_data:
            item_name = row[1]

            item_data = {
                "name": row[1],
                "description": row[2],
                "target": row[3],
                "one_time_item": row[4],
                "effect_min": row[5],
                "effect_max": row[6],
                "buff_type": row[7]
            }

            if row[4]:  # If one_time_item is True
                self.one_time_items[item_name] = item_data
            else:
                self.other_items[item_name] = item_data

        # Track unique items acquired by the adventurer
        self.unique_items_acquired = set()

    def get_unique_item_data(self, floor_index):
        """
        Retrieve and remove a random unique item from the one_time_items dictionary.
        Ensures each unique item is used only once.

        :return: Raw data for a random unique item, or None if no items remain.
        """
        if not self.one_time_items:
            return None  # No more unique items to retrieve

        item_name = list(self.one_time_items.keys())[floor_index]
        return self.one_time_items[item_name]

    def mark_item_acquired(self, item_name):
        """
        Mark a unique item as acquired.
        :param item_name: The name of the item.
        """
        self.unique_items_acquired.add(item_name)

    def get_limited_item_data(self, item_name):
        """
        Retrieve data for a non-unique item.
        :param item_name: The name of the item.
        :return: Raw data for the item or None if not found.
        """
        return self.other_items.get(item_name)

    def get_random_consumable_item_data(self):
        """
        Retrieve data for a random consumable item.
        :return: Raw data for the item or None if no items are available.
        """
        if not self.other_items:
            print("Warning: No consumable items available.")
            return None

        return random.choice(list(self.other_items.values()))

    def reset_unique_items(self):
        """
        Clear the set of unique items acquired, allowing them to be acquired again.
        """
        self.unique_items_acquired.clear()

    def list_all_items(self):
        """
        Lists all items managed by the ItemManager for debugging purposes.
        """
        print("Unique Items:")
        for item_name, item_data in self.one_time_items.items():
            print(f"- {item_name}: {item_data}")

        print("\nLimited Items:")
        for item_name, item_data in self.other_items.items():
            print(f"- {item_name}: {item_data}")

    def initialize_pillar_order(self):
        """
        Randomizes the order of one_time_items for unique item placement (pillars).
        """
        randomized_items = list(self.one_time_items.items())  # Convert to a list of (key, value) pairs
        random.shuffle(randomized_items)  # Shuffle the items
        self.one_time_items = dict(randomized_items)  # Reassign as a randomized dictionary
        print(f"[ItemManager] Randomized one_time_items: {list(self.one_time_items.keys())}")
