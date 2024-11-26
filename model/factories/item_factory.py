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
        Create an Item instance from raw database data.
        :param raw_data: Tuple containing item attributes.
        :return: An Item instance.
        """
        if not raw_data:
            raise ValueError("No raw data provided to create an item.")

        name, description, ability, one_time_item = raw_data

        return Item(
            name=name,
            description=description,
            ability=ability,
            one_time_item=bool(one_time_item),
        )

    @staticmethod
    def create_unique_item(raw_data):
        """
        Create a unique item from raw data.
        :param raw_data: Tuple containing item attributes.
        :return: A unique Item instance.
        """
        item = ItemFactory.create_item_from_raw(raw_data)
        item.one_time_item = True  # Ensure the item is marked as unique
        return item

    @staticmethod
    def create_standard_item(raw_data):
        """
        Create a standard (non-unique) item from raw data.
        :param raw_data: Tuple containing item attributes.
        :return: A standard Item instance.
        """
        item = ItemFactory.create_item_from_raw(raw_data)
        item.one_time_item = False
        return item