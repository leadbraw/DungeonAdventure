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
        self.__my_name = name
        self.__my_description = description
        self.__my_target = target
        self.__my_one_time_item = bool(one_time_item)
        self.__my_effect_min = effect_min
        self.__my_effect_max = effect_max
        self.__my_buff_type = buff_type

    # Read-only property for name
    @property
    def name(self):
        return self.__my_name

    # Read-only property for description
    @property
    def description(self):
        return self.__my_description

    # Read-only property for target
    @property
    def target(self):
        return self.__my_target

    # Read-only property for one_time_item
    @property
    def one_time_item(self):
        return self.__my_one_time_item

    # Read-only property for effect_min
    @property
    def effect_min(self):
        return self.__my_effect_min

    # Read-only property for effect_max
    @property
    def effect_max(self):
        return self.__my_effect_max

    # Read-only property for buff_type
    @property
    def buff_type(self):
        return self.__my_buff_type

    def __getstate__(self):
        """ Stores the object's state in a pickled dictionary.
        :return: dictionary of states to be stored.
        """
        return {'__my_name': self.__my_name,
                '__my_description': self.__my_description,
                '__my_target': self.__my_target,
                '__my_one_time_item': self.__my_one_time_item,
                '__my_effect_min': self.__my_effect_min,
                '__my_effect_max': self.__my_effect_max,
                '__my_buff_type': self.__my_buff_type}

    def __setstate__(self, state):
        """ Restores the object's state from the pickled dictionary.
        :param state: dictionary of restored states.
        """
        self.__my_name = state['__my_name']
        self.__my_description = state['__my_description']
        self.__my_target = state['__my_target']
        self.__my_one_time_item = state['__my_one_time_item']
        self.__my_effect_min = state['__my_effect_min']
        self.__my_effect_max = state['__my_effect_max']
        self.__my_buff_type = state['__my_buff_type']