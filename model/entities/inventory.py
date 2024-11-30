import random

from model.entities import item
from model.managers.item_manager import ItemManager

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
        for entry in self.items:
            if entry["item"].name == item_name:
                effect_min = entry["item"].effect_min
                effect_max = entry["item"].effect_max
                if self.apply_effect(entry["item"], target, effect_min, effect_max, dungeon):
                    self.remove_item(item_name, 1)
                    return entry["item"]
        print(f"Item '{item_name}' is not usable or not found.")
        return None

    def apply_effect(self, item_data, target, effect_min, effect_max):
        """
        Applies the item's effect to the target.

        :param item_data: The dictionary containing item data.
        :param target: The target entity or object.
        :param effect_min: The minimum effect value.
        :param effect_max: The maximum effect value.
        :return: True if the effect was applied successfully, False otherwise.
        """
        if item_data["target"] == "adventurer":
            return self._apply_effect_to_adventurer(item_data, target, effect_min, effect_max)
        elif item_data["target"] == "monster":
            return self._apply_effect_to_monster(item_data, target, effect_min, effect_max)
        elif item_data["target"] == "room":
            return self._apply_effect_to_room(item_data, target)
        else:
            print(f"No valid effect applied for item '{item_data['name']}'.")
            return False

    def _apply_effect_to_adventurer(self, item_data, adventurer, effect_min, effect_max):
        """
        Applies the item's effect to an adventurer.
        :param item_data: The dictionary containing item data.
        :param adventurer: The adventurer object.
        :param effect_min: The minimum effect value.
        :param effect_max: The maximum effect value.
        :return: True if the effect was applied successfully, False otherwise.
        """
        # Handle Pillar buffs
        if item.name.startswith("Pillar"):
            buff_type = item.buff_type
            if not buff_type:
                raise ValueError(f"Item '{item.name}' is missing a 'buff_type'.")

            buff_value = random.randint(effect_min, effect_max)
            adventurer.apply_buff(buff_value, buff_type)
            print(f"{adventurer.name} gains {buff_value} to {buff_type} from {item.name}.")
            return True

        elif item.name == "Energy Drink":
            heal_amount = random.randint(effect_min, effect_max)
            adventurer.heal_from_item(heal_amount)
            print(f"{adventurer.name} heals {heal_amount} HP from {item.name}.")
            return True

        print(f"Item '{item.name}' could not be applied to {adventurer.name}.")
        return False

    def _apply_effect_to_monster(self, item_data, monster, effect_min, effect_max):
        """
        Applies the item's effect to a monster.
        :param item_data: The dictionary containing item data.
        :param monster: The monster object.
        :param effect_min: The minimum effect value.
        :param effect_max: The maximum effect value.
        :return: True if the effect was applied successfully, False otherwise.
        """
        if effect_min is not None and effect_max is not None and item_data.get("name") == "Code Spike":
            damage = random.randint(effect_min, effect_max)
            print(monster.take_item_damage(damage))  # Bypasses regen
            return True
        return False

    def _apply_effect_to_room(self, item_data, position, dungeon):
        """
        Applies the White Box's effect to reveal adjacent rooms on the current floor.
        :param item_data: The dictionary containing item data.
        :param position: A tuple (x, y) representing the current position on the current floor.
        :param dungeon: The dungeon object for the current floor.
        :return: True if the effect was applied successfully, False otherwise.
        """
        if item_data["name"] == "White Box":
            directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]  # Up, Right, Down, Left
            current_x, current_y = position  # Unpack current position

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

if __name__ == "__main__":
    import random
    from model.managers.item_manager import ItemManager
    from model.entities.adventurers import Adventurer
    from model.entities.monsters import Monster
    from model.dungeon.dungeon import Dungeon

    # Create test adventurer
    adventurer = Adventurer("Hero", "Warrior", 50, 1.0, 0.9, (5, 10), 0.2)
    print(f"Created adventurer: {adventurer.name} with HP {adventurer.hp}/{adventurer.max_hp}")

    # Create test monster
    monster = Monster("Goblin", "Beast", 30, 1.0, 0.8, (3, 6), 0.1, (5, 10))
    print(f"Created monster: {monster.name} with HP {monster.hp}/{monster.max_hp}")

    # Create test dungeon
    dungeon = Dungeon(1)  # 5x5 dungeon
    adventurer_position = (2, 2)
    dungeon.fetch_room(*adventurer_position).set_visited(True)  # Set starting room as visited

    # Create test items
    white_box = {"name": "White Box"}
    energy_drink = {"name": "Energy Drink", "effect_min": 5, "effect_max": 15}
    code_spike = {"name": "Code Spike", "effect_min": 10, "effect_max": 20}
    pillar_abstraction = {"name": "Pillar of Abstraction", "buff_type": "max_hp", "effect_min": 25, "effect_max": 25}

    # Create inventory instance
    inventory = Inventory()

    # Add items to inventory
    inventory.add_item(white_box)
    inventory.add_item(energy_drink)
    inventory.add_item(code_spike)
    inventory.add_item(pillar_abstraction)

    # Test _apply_effect_to_adventurer
    print("\n=== Testing Adventurer Effects ===")
    inventory._apply_effect_to_adventurer(pillar_abstraction, adventurer, 25, 25)
    inventory._apply_effect_to_adventurer(energy_drink, adventurer, 5, 15)

    # Test _apply_effect_to_monster
    print("\n=== Testing Monster Effects ===")
    inventory._apply_effect_to_monster(code_spike, monster, 10, 20)

    # Test _apply_effect_to_room
    print("\n=== Testing Room Effects ===")
    inventory._apply_effect_to_room(white_box, adventurer_position, dungeon)

    # Verify results
    print("\n=== Verifying Results ===")
    print(f"Adventurer HP: {adventurer.hp}/{adventurer.max_hp}")
    print(f"Monster HP: {monster.hp}/{monster.max_hp}")
    adjacent_positions = [(1, 2), (3, 2), (2, 1), (2, 3)]
    for pos in adjacent_positions:
        room = dungeon.fetch_room(*pos)
        if room:
            print(f"Room at {pos}: Visited = {room.get_visited()}")