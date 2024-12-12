import random


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
        self.monster_data = {"Normal": [], "Elite": []}  # Store monster data categorized by type
        self.load_monsters(monsters_data)

    def load_monsters(self, monsters_data):
        """
        Load monster data into the manager, categorized by type ('Normal' or 'Elite').
        If a monster with the same name already exists, it is replaced with the latest entry.

        :param monsters_data: List of tuples containing monster attributes.
        """
        if not monsters_data:
            print("[ERROR] No monster data provided!")
            return

        for row in monsters_data:
            monster_type = row[2]
            if monster_type not in self.monster_data:
                print(f"[ERROR] MonsterManager: Unknown monster type '{monster_type}'! Skipping.")
                continue

            # Remove existing monster with the same name
            self.monster_data[monster_type] = [
                monster for monster in self.monster_data[monster_type] if monster[1] != row[1]
            ]

            # Add the new monster data
            self.monster_data[monster_type].append(row)

    def get_monster_data(self, monster_name=None, monster_type="normal"):
        """
        Retrieve monster data by name or randomly.
        :param monster_name: The name of the monster to retrieve, or None for random.
        :param monster_type: The type of monster to retrieve ('normal' or 'elite').
        :return: A tuple of monster data or None if not found.
        """
        if monster_type not in self.monster_data:
            raise ValueError(f"Unknown monster type: {monster_type}")
        data = self.monster_data[monster_type]
        if monster_name:
            # Return specific monster data by name
            monster = next((m for m in data if m[1] == monster_name), None)
            if monster:
                pass
            else:
                print(f"[WARNING] MonsterManager: Monster '{monster_name}' not found!")
            return monster
        else:
            # Return random monster data
            if data:
                random_monster = random.choice(data)
                return random_monster
            else:
                print("[ERROR] MonsterManager: No monsters available!")
                return None
