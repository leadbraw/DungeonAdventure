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
        self.one_time_items = {}
        self.other_items = {}

        for row in items_data:
            item_name = row[1]  # Assuming the name is at index 1 TODO: fix?
            if row[4]:  # Assuming the one_time_item/unique_item flag is at index 4 TODO: fix?
                self.one_time_items[item_name] = row
            else:
                self.other_items[item_name] = row

        self.unique_items_acquired = set()  # Track unique items acquired by the adventurer

    def get_unique_item_data(self, item_name):
        """
        Retrieve raw data for a unique item, ensuring it hasn't already been acquired.
        :param item_name: The name of the unique item.
        :return: Raw data for the item or None if already acquired or not found.
        """
        if item_name in self.unique_items_acquired:
            return None  # Item has already been acquired

        return self.one_time_items.get(item_name)

    def mark_item_acquired(self, item_name):
        """
        Mark a unique item as acquired.
        :param item_name: The name of the item.
        """
        self.unique_items_acquired.add(item_name)

    def get_limited_item_data(self, item_name):
        """
        Retrieve raw data for a limited-instance item.
        :param item_name: The name of the item.
        :return: Raw data for the item or None if not found.
        """
        return self.other_items.get(item_name)

    def get_random_consumable_item_data(self):
        """
        Retrieve raw data for a random consumable item.
        :return: Raw data for the item or None if no items are available.
        """
        consumable_data = [
            raw_data for raw_data in self.other_items.values() if not raw_data[4]  # Assuming index 4 is 'unique'
        ]
        return random.choice(consumable_data) if consumable_data else None

    def reset_unique_items(self):
        """
        Clear the set of unique items acquired, allowing them to be acquired again.
        """
        self.unique_items_acquired.clear()