import random

from adventurers import Adventurer
from entities import Entity


class Monster(Entity):
    def __init__(self, the_name, the_position, the_hp,
                 the_attack_speed, the_chance_to_hit, the_damage_range,
                 the_chance_to_heal, the_heal_range):
        super().__init__(the_name, the_position, the_hp,
                         the_attack_speed, the_chance_to_hit, the_damage_range)

        # monster specific attributes (from database)
        self.__my_chance_to_heal = the_chance_to_heal   # float
        self.__my_heal_range = the_heal_range           # tuple

    def _update_hp(self, the_diff):
        message = ""

        super()._update_hp(the_diff)
        if not self.is_alive():
            message += f"\n{self.get_name()} fainted."
        else:
            # check regen
            heal = self.regen()
            if heal > 0:
                message += f"\n{self.get_name()} healed for {heal} points!"

        return message

    def regen(self):
        heal = 0

        # chance to heal (random float within heal chance)
        if random.uniform(0,1) <= self.__my_chance_to_heal:
            # heal number (random int within heal range)
            heal = random.randint(self.__my_heal_range[0], self.__my_heal_range[1])
            # set health
            self._update_hp(-heal)

        return heal

    def get_heal_chance(self):
        return self.__my_chance_to_heal

    def get_heal_range(self):
        return self.__my_heal_range


class Ogre(Monster):
    pass


class Gremlin(Monster):
    pass


class Skeleton(Monster):
    pass
