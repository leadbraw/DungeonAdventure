from src.model.entities.adventurers import Warrior, Priest, Thief, Bard


class AdventurerFactory:
    _instance = None

    @staticmethod
    def get_instance():
        """
        Retrieve the singleton instance of AdventurerFactory.
        :return: The singleton instance.
        """
        if AdventurerFactory._instance is None:
            AdventurerFactory._instance = AdventurerFactory()
        return AdventurerFactory._instance

    def __init__(self):
        if AdventurerFactory._instance is not None:
            raise Exception("This class is a singleton! Use get_instance() to access the instance.")

    def make_adventurer(self, raw_data):
        """
        Create an Adventurer instance based on the type field in raw data.
        :param raw_data: Tuple containing adventurer attributes.
        :return: An Adventurer instance of the appropriate type.

        Fields in raw_data (by position):
        0: name (str)
        1: type (str) - The adventurer's class type (e.g., 'Warrior', 'Priest').
        2: max_HP (int)
        3: attack_speed (int)
        4: chance_to_hit (float)
        5: attack_damage_min (int)
        6: attack_damage_max (int)
        7: chance_to_block (float)
        """
        adventurer_type = raw_data[1]
        if adventurer_type == "Warrior":
            return self.make_warrior(raw_data)
        elif adventurer_type == "Priest":
            return self.make_priest(raw_data)
        elif adventurer_type == "Thief":
            return self.make_thief(raw_data)
        elif adventurer_type == "Bard":
            return self.make_bard(raw_data)
        else:
            raise ValueError(f"Unknown adventurer type: {adventurer_type}")

    @staticmethod
    def make_warrior(raw_data):
        """
        Create a Warrior instance.
        :param raw_data: Tuple containing adventurer attributes.
        :return: A Warrior instance.
        """
        return Warrior(raw_data[0], raw_data[1], raw_data[2], raw_data[3],
                       raw_data[4], (raw_data[5], raw_data[6]), raw_data[7])

    @staticmethod
    def make_priest(raw_data):
        """
        Create a Priest instance.
        :param raw_data: Tuple containing adventurer attributes.
        :return: A Priest instance.
        """
        return Priest(raw_data[0], raw_data[1], raw_data[2], raw_data[3],
                      raw_data[4], (raw_data[5], raw_data[6]), raw_data[7])

    @staticmethod
    def make_thief(raw_data):
        """
        Create a Thief instance.
        :param raw_data: Tuple containing adventurer attributes.
        :return: A Thief instance.
        """
        return Thief(raw_data[0], raw_data[1], raw_data[2], raw_data[3],
                     raw_data[4], (raw_data[5], raw_data[6]), raw_data[7])

    @staticmethod
    def make_bard(raw_data):
        """
        Create a Bard instance.
        :param raw_data: Tuple containing adventurer attributes.
        :return: A Bard instance.
        """
        return Bard(raw_data[0], raw_data[1], raw_data[2], raw_data[3],
                    raw_data[4], (raw_data[5], raw_data[6]), raw_data[7])
