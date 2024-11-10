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

    @final
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
        return f"\n{self.name} healed for {the_heal} points!"

    def _regen(self):
        heal = 0

        # chance to heal (random float within heal chance)
        if random.uniform(0,1) <= self.chance_to_heal:
            # heal number (random int within heal range)
            heal = random.randint(self.heal_range[0], self.heal_range[1])
            # set health
            self._update_hp(-heal)

        return heal

    @property
    def chance_to_heal(self):
        return self.__my_chance_to_heal

    @property
    def heal_range(self):
        return self.__my_heal_range

    @chance_to_heal.setter
    def chance_to_heal(self, the_chance_to_heal):
        if 1 >= the_chance_to_heal >= 0:
            self.__my_chance_to_heal = the_chance_to_heal

    @heal_range.setter
    def heal_range(self, the_heal_range):
        self.__my_heal_range = the_heal_range

class Ogre(Monster):
    pass


class Gremlin(Monster):
    pass


class Skeleton(Monster):
    pass

# m = Ogre("that guy", (0,0), 10,
#          6, 0.7, (1,5), 1, (1, 5))
# print (m.attack(m))
# print(m.hp)