from model.factories.item import Item

class ItemFactory:
    @staticmethod
    def create_item_from_raw(raw_data):
        """
        Create an Item instance from raw database data.
        :param raw_data: Tuple containing item attributes.
        :return: An Item instance.
        """
        item_id, name, description, ability, temporary, one_time_item = raw_data
        return Item(item_id, name, description, ability, temporary, one_time_item)
