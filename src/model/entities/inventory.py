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
        self.items = []  # List of dictionaries: {"item": dict, "quantity": int}

    def add_item(self, item, quantity=1):
        """
        Adds an item to the inventory.

        :param item: The `Item` object to be added.
        :param quantity: The quantity of the item to add.
        :return: True if the item was added successfully, False if there was no space.
        """
        if self.is_full():
            print("Inventory is full!")
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
                    print("Not enough quantity to remove.")
                    return False
        print(f"Item '{item_name}' not found in inventory.")
        return False

    def use_item(self, item_name, target):
        """
        Uses an item from the inventory, triggering its effect.

        :param item_name: The name of the item to use.
        :param target: The target entity or object for the item's effect.
        :return: The used item, or None if the item is not found.
        """
        print(f"[DEBUG] use_item called with item_name='{item_name}' and target='{target}'.")

        # Check inventory structure
        if not self.items:
            print("[DEBUG] Inventory is empty. Cannot use any item.")
            return None

        for entry in self.items:
            item = entry["item"]
            quantity = entry["quantity"]

            # Debug information about the current item in inventory
            print(f"[DEBUG] Checking inventory item: {item.name} with quantity={quantity}")

            # Check if the current inventory item matches the requested item
            if item.name == item_name:
                print(f"[DEBUG] Found matching item '{item_name}' in inventory.")
                effect_min = item.effect_min
                effect_max = item.effect_max
                print(f"[DEBUG] Attempting to apply effect: min={effect_min}, max={effect_max} to target '{target}'.")

                # Attempt to apply the item's effect to the target
                if self.apply_effect(item, target, effect_min, effect_max):
                    print(f"[DEBUG] Item '{item_name}' successfully applied to target '{target}'.")
                    self.remove_item(item_name, 1)
                    print(f"[DEBUG] Item '{item_name}' removed from inventory. Remaining quantity: {quantity - 1}")
                    return item
                else:
                    print(f"[DEBUG] Failed to apply item '{item_name}' to target '{target}'.")

        # If the item was not found or could not be used
        print(f"[DEBUG] Item '{item_name}' is not usable or not found in inventory.")
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
        print(f"[DEBUG] apply_effect called with item='{item_data.name}', target='{target}', "
              f"effect_min={effect_min}, effect_max={effect_max}.")

        # Check if the item_data is valid
        if not item_data:
            print("[DEBUG] Invalid item_data provided to apply_effect.")
            return False

        # Determine the correct target type for the item
        if item_data.target == "adventurer":
            print(f"[DEBUG] Target is 'adventurer'. Applying effect to '{target}'.")
            return self._apply_effect_to_adventurer(item_data, target, effect_min, effect_max)

        elif item_data.target == "monster":
            print(f"[DEBUG] Target is 'monster'. Applying effect to '{target}'.")
            return self._apply_effect_to_monster(item_data, target, effect_min, effect_max)

        elif item_data.target == "room":
            print(f"[DEBUG] Target is 'room'. Attempting to apply room effect.")
            # Ensure target contains both position and dungeon
            if isinstance(target, tuple) and len(target) == 2:
                position, dungeon = target
                print(f"[DEBUG] Room target identified: position={position}, dungeon={dungeon}.")
                return self._apply_effect_to_room(item_data, position, dungeon)
            else:
                print(f"[DEBUG] Invalid room target format: {target}. Expected (position, dungeon).")
                return False

        else:
            # Log unhandled target types
            print(f"[DEBUG] No valid effect for item '{item_data.name}' with target type '{item_data.target}'.")
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
            print(f"{adventurer.name} gains {buff_value} to {buff_type} from {item_data.name}.")
            return True

        # Handle Energy Drink
        elif item_data.name == "Energy Drink":
            heal_amount = random.randint(effect_min, effect_max)
            adventurer.heal_from_item(heal_amount)
            print(f"{adventurer.name} heals {heal_amount} HP from {item_data.name}.")
            return True

        # Fallback for unhandled cases
        print(f"Item '{item_data.name}' could not be applied to {adventurer.name}.")
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
        if not monster:
            print("[DEBUG] No valid monster target provided.")
            return False

        if not item_data:
            print("[DEBUG] No valid item data provided.")
            return False

        print(f"[DEBUG] Attempting to apply effect from item '{item_data.name}' to monster '{monster.name}'.")

        # Check for Code Spike and calculate damage
        if effect_min is not None and effect_max is not None and item_data.name == "Code Spike":
            try:
                damage = random.randint(effect_min, effect_max)
                print(f"[DEBUG] Calculated damage: {damage} (min={effect_min}, max={effect_max}).")

                # Apply damage and log monster health
                result_message = monster.take_item_damage(damage)  # Assuming this method exists and logs health changes
                print(f"[DEBUG] Monster '{monster.name}' damage result: {result_message}")
                return True

            except Exception as e:
                print(f"[ERROR] Failed to apply effect to monster. Error: {e}")
                return False

        # Log unhandled item effect cases
        print(f"[DEBUG] No valid effect for item '{item_data.name}' on monster '{monster.name}'.")
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
        print(f"[DEBUG] Room effect called for item: {item_data.name}. Position: {position}, Dungeon: {dungeon}")

        if item_data.name == "White Box":
            if not position or not dungeon:
                print("[DEBUG] Position or dungeon is None. Cannot apply room effect.")
                return False

            # All 8 adjacent rooms
            directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)]
            current_x, current_y = position  # Unpack current position

            # Validate dungeon type
            if not hasattr(dungeon, "get_length") or not hasattr(dungeon, "get_width"):
                print("[DEBUG] Dungeon is not a valid dungeon object.")
                return False

            # Check adjacent rooms and mark them as visited
            for dx, dy in directions:
                adj_x, adj_y = current_x + dx, current_y + dy
                if 0 <= adj_x < dungeon.get_length() and 0 <= adj_y < dungeon.get_width():
                    adjacent_room = dungeon.fetch_room(adj_x, adj_y)
                    if not adjacent_room.get_visited():
                        adjacent_room.set_visited(True)
                        print(
                            f"The White Box reveals an adjacent room: {adjacent_room.get_type()} at ({adj_x}, {adj_y}).")

            return True

        print(f"[DEBUG] No valid room effect for item: {item_data.name}.")
        return False

    def list_items(self):
        """
        Lists all items in the inventory with their quantities.
        """
        if not self.items:
            print("The inventory is empty.")
        for entry in self.items:
            print(f"{entry['item']['name']} (x{entry['quantity']})")

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
        print("Inventory cleared.")

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