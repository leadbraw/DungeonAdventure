class Item:
    def __init__(self, name, description, target, one_time_item,
                 effect_min=None, effect_max=None, buff_type=None):
        """
        Represents an item in the game.

        :param name: Name of the item.
        :param description: Description of the item's effect.
        :param target: The entity or object affected by the item (e.g., "adventurer", "monster", "room").
        :param one_time_item: Boolean indicating if the item is a one-time unique item.
        :param effect_min: The minimum value of the item's effect (optional, for numeric effects).
        :param effect_max: The maximum value of the item's effect (optional, for numeric effects).
        :param buff_type: The type of buff applied by the item (e.g., "max_hp", "attack_speed") (optional).
        """
        self.name = name
        self.description = description
        self.target = target
        self.one_time_item = bool(one_time_item)
        self.effect_min = effect_min
        self.effect_max = effect_max
        self.buff_type = buff_type

    def get_name(self):
        """Returns the name of the item."""
        return self.name