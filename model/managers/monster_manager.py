import random
from copy import deepcopy
from model.entities.monsters import Monster


class MonsterManager:
    _instance = None  # Singleton instance

    @staticmethod
    def get_instance(monsters_data=None):
        """
        Retrieve the singleton instance of MonsterManager, initializing it if necessary.
        :param monsters_data: List of tuples representing monster data from the database.
        :return: The singleton instance of MonsterManager.
        """
        if MonsterManager._instance is None:
            if monsters_data is None:
                raise ValueError("MonsterManager requires 'monsters_data' for initialization.")
            MonsterManager._instance = MonsterManager(monsters_data)
        return MonsterManager._instance

    def __init__(self, monsters_data):
        if MonsterManager._instance is not None:
            raise Exception("This class is a singleton! Use get_instance() to access the instance.")
        self.monster_options = []  # Store all loaded monsters

        # Dynamically load monsters from the provided data
        self.load_monsters(monsters_data)

    def load_monsters(self, monsters_data):
        if not monsters_data:
            print("MonsterManager: No monster data provided!")
        for row in monsters_data:
            print(f"MonsterManager: Loading monster {row[1]} of type {row[2]}")
            name = row[1]
            monster_type = row[2]
            max_hp = row[3]
            attack_speed = row[4]
            chance_to_hit = row[5]
            damage_range = (row[6], row[7])
            chance_to_heal = row[8]
            heal_range = (row[9], row[10])
            initial_position = (-2, -2)

            # Create and append a generic Monster
            self.monster_options.append(
                Monster(
                    name,
                    initial_position,
                    max_hp,
                    attack_speed,
                    chance_to_hit,
                    damage_range,
                    chance_to_heal,
                    heal_range,
                    monster_type,
                )
            )
        print(f"MonsterManager: Loaded {len(self.monster_options)} monsters.")

    def get_monster_clone(self, monster_name):
        """
        Returns a deep copy of a specified monster by name.
        :param monster_name: The name of the monster to clone.
        :return: A deep copy of the specified monster or None if not found.
        """
        original = next((m for m in self.monster_options if m.name == monster_name), None)
        return deepcopy(original) if original else None

    def get_random_monster(self):
        if not self.monster_options:
            print("MonsterManager: No monsters available!")
            return None
        base_monster = random.choice(self.monster_options)
        print(f"MonsterManager: Selected monster: {base_monster}")
        return deepcopy(base_monster)
