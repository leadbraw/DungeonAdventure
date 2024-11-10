import random
from copy import deepcopy
from .database_manager import DatabaseManager
from model.entities.monsters import Ogre, Gremlin, Skeleton # Import specific monster classes

class MonsterManager:
    _instance = None  # Singleton instance

    @staticmethod
    def get_instance():
        if MonsterManager._instance is None:
            MonsterManager._instance = MonsterManager()
        return MonsterManager._instance

    def __init__(self):
        if MonsterManager._instance is not None:
            raise Exception("This class is a singleton!")
        self.monsters = self.load_monsters()  # Load all monsters once on initialization

    def load_monsters(self):
        """Loads all monsters from the database and initializes them as objects."""
        query = "SELECT * FROM monsters"
        result = DatabaseManager.get_instance().execute_query(query)
        monster_objects = []

        for row in result:
            # Extract database values and set a temporary position outside the dungeon
            name = row[1]
            max_hp = row[3]
            attack_speed = row[4]
            chance_to_hit = row[5]
            damage_range = (row[6], row[7])
            chance_to_heal = row[8]
            heal_range = (row[9], row[10])
            initial_position = (-2, -2)

            # Initialize monster based on type
            monster_type = row[2]
            if monster_type == "Ogre":
                monster_objects.append(Ogre(name, initial_position, max_hp, attack_speed,
                                            chance_to_hit, damage_range, chance_to_heal, heal_range))
            elif monster_type == "Gremlin":
                monster_objects.append(Gremlin(name, initial_position, max_hp, attack_speed,
                                               chance_to_hit, damage_range, chance_to_heal, heal_range))
            elif monster_type == "Skeleton":
                monster_objects.append(Skeleton(name, initial_position, max_hp, attack_speed,
                                                chance_to_hit, damage_range, chance_to_heal, heal_range))

        return monster_objects

    def get_monster_clone(self, monster_name):
        """Returns a deep copy of a specified monster by name."""
        original = next((m for m in self.monsters if m.get_name() == monster_name), None)
        return deepcopy(original) if original else None

    def get_random_monster(self):
        """Returns a random monster instance from the available list."""
        base_monster = random.choice(self.monsters) if self.monsters else None
        return deepcopy(base_monster) if base_monster else None