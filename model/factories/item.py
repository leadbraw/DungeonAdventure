class Item:
    def __init__(self, item_id, name, description, ability, temporary, one_time_item):
        """
        Represents an item in the game.
        :param item_id: Unique identifier for the item.
        :param name: Name of the item.
        :param description: Description of the item's effect.
        :param ability: Effect or ability provided by the item.
        :param temporary: Boolean indicating if the item is temporary.
        :param one_time_item: Boolean indicating if the item is a one-time unique item.
        """
        self.item_id = item_id
        self.name = name
        self.description = description
        self.ability = ability
        self.temporary = bool(temporary)
        self.one_time_item = bool(one_time_item)

    def get_name(self):
        """Returns the name of the item."""
        return self.name