# item_factory.py

from model.entities.item import Item

class ItemFactory:
    _instance = None

    @staticmethod
    def get_instance():
        if ItemFactory._instance is None:
            ItemFactory._instance = ItemFactory()
        return ItemFactory._instance

    def __init__(self):
        if ItemFactory._instance is not None:
            raise Exception("This class is a singleton! Use get_instance() to access the instance.")

    @staticmethod
    def create_item_from_raw(raw_data):
        """
        Create an Item instance from raw database data (dictionary).
        :param raw_data: Dictionary containing item attributes.
        :return: An Item instance.
        """
        if not raw_data:
            raise ValueError("No raw data provided to create an item.")

        return Item(
            name=raw_data["name"],
            description=raw_data["description"],
            target=raw_data["target"],
            one_time_item=bool(raw_data["one_time_item"]),
            effect_min=raw_data.get("effect_min"),
            effect_max=raw_data.get("effect_max"),
            buff_type=raw_data.get("buff_type"),
        )

    @staticmethod
    def create_unique_item(raw_data):
        """
        Create a unique item from raw data.
        :param raw_data: Dictionary containing item attributes.
        :return: A unique Item instance.
        """
        item = ItemFactory.create_item_from_raw(raw_data)
        item.one_time_item = True  # Ensure the item is marked as unique
        return item

    @staticmethod
    def create_standard_item(raw_data):
        """
        Create a standard (non-unique) item from raw data.
        :param raw_data: Dictionary containing item attributes.
        :return: A standard Item instance.
        """
        item = ItemFactory.create_item_from_raw(raw_data)
        item.one_time_item = False
        return item