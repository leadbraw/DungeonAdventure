from model.entities.adventurers import Warrior, Priest, Thief, Bard

class AdventurerManager:
    _instance = None  # Singleton instance

    @staticmethod
    def get_instance(adventurers_data=None):
        """
        Retrieve the singleton instance of AdventurerManager, initializing it if necessary.
        :param adventurers_data: List of tuples representing adventurer data from the database.
        :return: The singleton instance of AdventurerManager.
        """
        if AdventurerManager._instance is None:
            if adventurers_data is None:
                raise ValueError("AdventurerManager requires 'adventurers_data' for initialization.")
            AdventurerManager._instance = AdventurerManager(adventurers_data)
        return AdventurerManager._instance

    def __init__(self, adventurers_data):
        if AdventurerManager._instance is not None:
            raise Exception("This class is a singleton! Use get_instance() to access the instance.")

        print(f"Initializing AdventurerManager with data: {adventurers_data}")
        self.adventurer = None  # Placeholder for the single selected adventurer
        self.adventurer_options = {}  # Dictionary to hold all adventurer options

        # Map adventurer types to their classes
        self.adventurer_classes = {
            "Warrior": Warrior,
            "Priest": Priest,
            "Thief": Thief,
            "Bard": Bard,
        }

        # Load adventurers from the provided data
        self.load_adventurer_options(adventurers_data)

    def load_adventurer_options(self, adventurers_data):
        """
        Loads all adventurer options from preloaded data.
        :param adventurers_data: List of tuples representing adventurer data.
        """
        print(f"Loading adventurer options with data: {adventurers_data}")
        for row in adventurers_data:
            print(f"Processing row: {row}")
            name = row[1]
            max_hp = row[3]
            attack_speed = row[4]
            chance_to_hit = row[5]
            damage_range = (row[6], row[7])
            chance_to_block = row[8]
            initial_position = (-3, -3)  # Temporary position outside the dungeon

            # Dynamically create the adventurer instance based on its type
            adventurer_type = row[2]
            print(f"Loading adventurer: {name} ({adventurer_type})")
            self.adventurer_options[name] = ...

            adventurer_class = self.adventurer_classes.get(adventurer_type)
            if adventurer_class:
                self.adventurer_options[name] = adventurer_class(
                    name, initial_position, max_hp, attack_speed, chance_to_hit, damage_range, chance_to_block
                )
                print(f"Added {name} to adventurer options")
            else:
                print(f"Adventurer class for type {adventurer_type} not found")

        print("Adventurer options loaded:", self.adventurer_options.keys())
    def get_adventurer_options(self):
        """Returns a dictionary of all adventurer options for the menu."""
        return self.adventurer_options

    def load_adventurer(self, adventurer_name):
        """Sets the selected adventurer as the player's choice."""
        print(f"Attempting to load adventurer: {adventurer_name}")
        self.adventurer = self.adventurer_options.get(adventurer_name)
        if self.adventurer:
            print(f"Adventurer {adventurer_name} loaded successfully.")
        else:
            print(f"Adventurer {adventurer_name} not found in options: {self.adventurer_options.keys()}")

    def get_adventurer(self):
        """Returns the currently selected adventurer instance."""
        return self.adventurer

    def reset_adventurer(self):
        """Resets the adventurer instance (useful for new games or class changes)."""
        self.adventurer = None