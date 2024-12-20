class AdventurerManager:
    # Singleton instance
    _instance = None

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
        # Dictionary to hold all raw adventurer data
        self.adventurer_data = {}
        # Placeholder for the single selected adventurer
        self.active_adventurer = None

        # Load adventurers from the provided data
        self.load_adventurer_data(adventurers_data)

    def load_adventurer_data(self, adventurers_data):
        """
        Loads all raw adventurer data.
        :param adventurers_data: List of tuples representing adventurer data.
        """
        for row in adventurers_data:
            name = row[1]
            self.adventurer_data[name] = row  # Store raw data directly

    def get_adventurer_data(self, name=None):
        """
        Retrieve raw adventurer data.
        :param name: Name of the adventurer to retrieve, or None for all data.
        :return: Raw adventurer data.
        """
        if name:
            return self.adventurer_data.get(name)
        return self.adventurer_data

    def load_active_adventurer(self, name):
        """
        Sets the selected adventurer as the active choice.
        :param name: Name of the adventurer.
        """
        self.active_adventurer = self.adventurer_data.get(name)
        if self.active_adventurer:
            pass
        else:
            print(f"Adventurer {name} not found in data: {self.adventurer_data.keys()}")

    def reset_active_adventurer(self):
        """Resets the active adventurer instance."""
        self.active_adventurer = None