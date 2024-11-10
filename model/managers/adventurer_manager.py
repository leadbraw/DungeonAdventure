from .database_manager import DatabaseManager
from model.entities.adventurers import Warrior, Priest, Thief, Bard  # Import specific adventurer classes as needed


class AdventurerManager:
    _instance = None  # Singleton instance

    @staticmethod
    def get_instance():
        if AdventurerManager._instance is None:
            AdventurerManager._instance = AdventurerManager()
        return AdventurerManager._instance

    def __init__(self):
        if AdventurerManager._instance is not None:
            raise Exception("This class is a singleton!")
        self.adventurer = None  # Placeholder for the single selected adventurer
        self.adventurer_options = {}  # Dictionary to hold all adventurer options for display

    def load_adventurer_options(self):
        """Loads all adventurer options from the database for the menu display."""
        query = "SELECT * FROM heroes"
        results = DatabaseManager.get_instance().execute_query(query)

        for row in results:
            name = row[1]
            max_hp = row[3]
            attack_speed = row[4]
            chance_to_hit = row[5]
            damage_range = (row[6], row[7])
            chance_to_block = row[8]
            initial_position = (-3, -3)  # Temporary position outside the dungeon

            # Determine the adventurer class type and add to the options dictionary
            adventurer_type = row[2]
            if adventurer_type == "Warrior":
                self.adventurer_options["Warrior"] = Warrior(name, initial_position, max_hp, attack_speed,
                                                             chance_to_hit, damage_range, chance_to_block)
            elif adventurer_type == "Priest":
                self.adventurer_options["Priest"] = Priest(name, initial_position, max_hp, attack_speed, chance_to_hit,
                                                           damage_range, chance_to_block)
            elif adventurer_type == "Thief":
                self.adventurer_options["Thief"] = Thief(name, initial_position, max_hp, attack_speed, chance_to_hit,
                                                         damage_range, chance_to_block)
            elif adventurer_type == "Bard":
                self.adventurer_options["Bard"] = Bard(name, initial_position, max_hp, attack_speed, chance_to_hit,
                                                       damage_range, chance_to_block)

    def get_adventurer_options(self):
        """Returns a dictionary of all adventurer options for the menu."""
        return self.adventurer_options

    def load_adventurer(self, adventurer_type):
        """Sets the selected adventurer as the player's choice."""
        self.adventurer = self.adventurer_options.get(adventurer_type)

    def get_adventurer(self):
        """Returns the currently selected adventurer instance."""
        return self.adventurer

    def reset_adventurer(self):
        """Resets the adventurer instance (useful for new games or class changes)."""
        self.adventurer = None
