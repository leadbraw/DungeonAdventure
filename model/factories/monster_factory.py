from model.entities.monsters import Monster


class MonsterFactory:
    _instance = None

    @staticmethod
    def get_instance():
        if MonsterFactory._instance is None:
            MonsterFactory._instance = MonsterFactory()
        return MonsterFactory._instance

    def __init__(self):
        if MonsterFactory._instance is not None:
            raise Exception("This class is a singleton! Use get_instance() to access the instance.")

    @staticmethod
    def make_monster(raw_data):
        """
        Create a Monster instance from raw database data based on the type field.
        :param raw_data: Tuple containing monster attributes.
        :return: A Monster instance of the appropriate type.

        Fields in raw_data (by position):
        0: name (str)
        1: type (str)
        2: max_HP (int)
        3: attack_speed (int)
        4: chance_to_hit (float)
        5: attack_damage_min (int)
        6: attack_damage_max (int)
        7: chance_to_heal (float)
        8: heal_range_min (int)
        9: heal_range_max (int)
        """
        print(raw_data)
        monster_type = raw_data[1]
        if monster_type == "Normal":
            return MonsterFactory.make_normal_monster(raw_data)
        elif monster_type == "Elite":
            return MonsterFactory.make_elite_monster(raw_data)
        else:
            raise ValueError(f"Unknown monster type: {monster_type}")

    @staticmethod
    def make_normal_monster(raw_data):
        """
        Create a normal Monster instance.
        :param raw_data: Tuple containing monster attributes.
        :return: A normal Monster instance.
        """
        print(raw_data)
        return Monster(raw_data[0], raw_data[1], raw_data[2],
                       raw_data[3], raw_data[4], (raw_data[5], raw_data[6]),
                       raw_data[7], (raw_data[8], raw_data[9]))

    @staticmethod
    def make_elite_monster(raw_data):
        """
        Create an elite Monster instance.
        :param raw_data: Tuple containing monster attributes.
        :return: An elite Monster instance.
        """
        return Monster(raw_data[0], raw_data[1], raw_data[2], raw_data[3],
                       raw_data[4], (raw_data[5], raw_data[6]),
                       raw_data[7], (raw_data[8], raw_data[9]))