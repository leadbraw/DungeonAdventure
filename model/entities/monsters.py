import random
from typing import final

from model.entities.entities import Entity


class Monster(Entity):
    def __init__(self, the_name, the_position, the_max_hp,
                 the_attack_speed, the_chance_to_hit, the_damage_range,
                 the_chance_to_heal, the_heal_range):
        super().__init__(the_name, the_position, the_max_hp,
                         the_attack_speed, the_chance_to_hit, the_damage_range)

        # monster specific attributes (from database)
        self.__my_chance_to_heal = the_chance_to_heal   # float
        self.__my_heal_range = the_heal_range           # tuple

    def _hit_response(self, the_dmg):
        message = ""

        self._update_hp(the_dmg)

        if self.is_alive():
            # check regen
            heal = self._regen()
            if heal > 0:
                message += self._regen_msg(heal)

        return message

    def _regen_msg(self, the_heal):
        return f"\n{self.get_name()} healed for {the_heal} points!"

    def _regen(self):
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

    def set_heal_chance(self, the_chance_to_heal):
        if 1 >= the_chance_to_heal >= 0:
            self.my_chance_to_heal = the_chance_to_heal

    def set_heal_range(self, the_heal_range):
        self.my_heal_range = the_heal_range

class Ogre(Monster):
    pass


class Gremlin(Monster):
    pass


class Skeleton(Monster):
    pass
