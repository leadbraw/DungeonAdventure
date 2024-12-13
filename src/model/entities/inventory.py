import random
from src.model.managers.item_manager import ItemManager


class Inventory:
    """
    A class to manage an inventory system for an adventurer or other entities.
    """

    def __init__(self, capacity=10):
        """
        Initializes the inventory with a maximum size and an empty list of items.

        :param capacity: The maximum number of items the inventory can hold.
        """
        self.capacity = capacity
        # List of dictionaries: {"item": dict, "quantity": int}
        self.items = []

    def add_item(self, item, quantity=1):
        """
        Adds an item to the inventory.

        :param item: The `Item` object to be added.
        :param quantity: The quantity of the item to add.
        :return: True if the item was added successfully, False if there was no space.
        """
        if self.is_full():
            return False

        # Check if the item already exists in the inventory
        for entry in self.items:
            if entry["item"].name == item.name:
                entry["quantity"] += quantity
                return True

        # If the item doesn't already exist, add it as a new entry
        self.items.append({"item": item, "quantity": quantity})
        return True

    def remove_item(self, item_name, quantity=1):
        """
        Removes a specified quantity of an item from the inventory.

        :param item_name: The name of the item to remove.
        :param quantity: The quantity of the item to remove.
        :return: True if the item was removed successfully, False otherwise.
        """
        for entry in self.items:
            if entry["item"].name == item_name:
                if entry["quantity"] >= quantity:
                    entry["quantity"] -= quantity
                    if entry["quantity"] == 0:
                        self.items.remove(entry)
                    return True
                else:
                    return False
        return False

    def use_item(self, item_name, target):
        """
        Uses an item from the inventory, triggering its effect.

        :param item_name: The name of the item to use.
        :param target: The target entity or object for the item's effect.
        :return: The used item, or None if the item is not found.
        """

        # Check inventory structure
        if not self.items:
            return None

        for entry in self.items:
            item = entry["item"]

            # Check if the current inventory item matches the requested item
            if item.name == item_name:
                effect_min = item.effect_min
                effect_max = item.effect_max
                # Attempt to apply the item's effect to the target
                if self.apply_effect(item, target, effect_min, effect_max):
                    self.remove_item(item_name, 1)
                    return item
                else:
                    pass
        return None

    def apply_effect(self, item_data, target, effect_min, effect_max):
        """
        Applies the item's effect to the target.

        :param item_data: The Item object containing item data.
        :param target: The target entity or object.
        :param effect_min: The minimum effect value.
        :param effect_max: The maximum effect value.
        :return: True if the effect was applied successfully, False otherwise.
        """

        # Check if the item_data is valid
        if not item_data:
            return False

        # Determine the correct target type for the item
        if item_data.target == "adventurer":
            return self._apply_effect_to_adventurer(item_data, target, effect_min, effect_max)

        elif item_data.target == "monster":
            return self._apply_effect_to_monster(item_data, target, effect_min, effect_max)

        elif item_data.target == "room":
            # Ensure target contains both position and dungeon
            if isinstance(target, tuple) and len(target) == 2:
                position, dungeon = target
                return self._apply_effect_to_room(item_data, position, dungeon)
            else:
                return False

        else:
            return False

    @staticmethod
    def _apply_effect_to_adventurer(item_data, adventurer, effect_min, effect_max):
        """
        Applies the item's effect to an adventurer.

        :param item_data: The Item object containing item data.
        :param adventurer: The adventurer object.
        :param effect_min: The minimum effect value.
        :param effect_max: The maximum effect value.
        :return: True if the effect was applied successfully, False otherwise.
        """
        # Handle Pillar buffs
        if item_data.name.startswith("Pillar"):
            buff_type = item_data.buff_type
            if not buff_type:
                raise ValueError(f"Item '{item_data.name}' is missing a 'buff_type'.")

            buff_value = random.randint(effect_min, effect_max)
            adventurer.apply_buff(buff_value, buff_type)
            return True

        # Handle Energy Drink
        elif item_data.name == "Energy Drink":
            heal_amount = random.randint(effect_min, effect_max)
            adventurer.heal_from_item(heal_amount)
            return True
        return False

    @staticmethod
    def _apply_effect_to_monster(item_data, monster, effect_min, effect_max):
        """
        Applies the item's effect to a monster.

        :param item_data: The Item object containing item data.
        :param monster: The monster object.
        :param effect_min: The minimum effect value.
        :param effect_max: The maximum effect value.
        :return: True if the effect was applied successfully, False otherwise.
        """
        if not monster or not item_data:
            return False

        # Check for Code Spike and calculate damage
        if effect_min is not None and effect_max is not None and item_data.name == "Code Spike":
            try:
                damage = random.randint(effect_min, effect_max)

                # Apply damage and log monster health
                monster.take_item_damage(damage)
                return True

            except Exception as e:
                print(f"[ERROR] Failed to apply effect to monster. Error: {e}")
                return False

        return False

    @staticmethod
    def _apply_effect_to_room(item_data, position, dungeon):
        """
        Applies the White Box's effect to reveal adjacent rooms on the current floor.
        :param item_data: The Item object containing item data.
        :param position: A tuple (x, y) representing the current position on the current floor.
        :param dungeon: The dungeon object for the current floor.
        :return: True if the effect was applied successfully, False otherwise.
        """

        if item_data.name == "White Box":
            if not position or not dungeon:
                return False

            # All 8 adjacent rooms
            directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)]
            current_x, current_y = position

            # Validate dungeon type
            if not hasattr(dungeon, "get_length") or not hasattr(dungeon, "get_width"):
                return False

            # Check adjacent rooms and mark them as visited
            for dx, dy in directions:
                adj_x, adj_y = current_x + dx, current_y + dy
                if 0 <= adj_x < dungeon.get_length() and 0 <= adj_y < dungeon.get_width():
                    adjacent_room = dungeon.fetch_room(adj_x, adj_y)
                    if not adjacent_room.get_visited():
                        adjacent_room.set_visited(True)
            return True
        return False

    def is_full(self):
        """
        Checks if the inventory is full.

        :return: True if the inventory is full, False otherwise.
        """
        return len(self.items) >= self.capacity

    def find_item(self, item_name):
        """
        Finds an item in the inventory by its name.

        :param item_name: The name of the item to find.
        :return: The item if found, or None.
        """
        for entry in self.items:
            if entry["item"]["name"] == item_name:
                return entry["item"]
        return None

    def clear_inventory(self):
        """
        Clears all items from the inventory.
        """
        self.items = []

    def save_inventory(self):
        """
        Saves the inventory state to a serializable format.
        :return: A list of item dictionaries with their names and quantities.
        """
        return [{"name": entry["item"]["name"], "quantity": entry["quantity"]} for entry in self.items]

    def load_inventory(self, saved_data):
        """
        Loads the inventory state from a saved format.

        :param saved_data: A list of dictionaries with item names and quantities.
        """
        for entry in saved_data:
            item = ItemManager.get_instance().get_limited_item_data(entry["name"])
            if item:
                self.add_item(item, entry["quantity"])

    def __getstate__(self):
        """ Stores the object's state in a pickled dictionary.
        :return: dictionary of states to be stored.
        """
        return {'capacity': self.capacity,
                'items': self.items}

    def __setstate__(self, state):
        """ Restores the object's state from the pickled dictionary.
        :param state: dictionary of restored states.
        """
        self.capacity = state['capacity']
        self.items = state['items']