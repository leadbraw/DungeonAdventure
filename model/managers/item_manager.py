import random
from copy import deepcopy
from model.factories.item_factory import ItemFactory

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

        # Separate data into two dictionaries
        self.one_time_items = {}
        self.other_items = {}

        for row in items_data:
            item_name = row[1]  # Assuming the name is at index 1
            if row[5]:  # Assuming the one_time_item flag is at index 5
                self.one_time_items[item_name] = row
            else:
                self.other_items[item_name] = row

        self.unique_items_acquired = set()  # Track unique items acquired by the adventurer

    def get_unique_item(self, item_name):
        if item_name in self.unique_items_acquired:
            return None  # Item has already been acquired

        raw_data = self.one_time_items.get(item_name)
        if not raw_data:
            return None

        self.unique_items_acquired.add(item_name)
        return ItemFactory.create_item_from_raw(raw_data)

    def get_limited_item(self, item_name):
        raw_data = self.other_items.get(item_name)
        return ItemFactory.create_item_from_raw(raw_data) if raw_data else None

    def get_random_non_temporary_item(self):
        non_temporary_data = [
            raw_data for raw_data in self.other_items.values() if not raw_data[4]  # Assuming index 4 is 'temporary'
        ]
        if not non_temporary_data:
            return None  # No non-temporary items available

        raw_data = random.choice(non_temporary_data)
        return ItemFactory.create_item_from_raw(raw_data)

    def reset_unique_items(self):
        self.unique_items_acquired.clear()