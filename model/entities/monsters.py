import random
from typing import final
from model.entities.entities import Entity


class Monster(Entity):
    def __init__(self, the_name, the_position, the_max_hp,
                 the_attack_speed, the_hit_chance, the_damage_range,
                 the_heal_chance, the_heal_range):
        super().__init__(the_name, the_position, the_max_hp,
                         the_attack_speed, the_hit_chance, the_damage_range)

        # monster specific attributes (from database)
        self.__my_heal_chance = the_heal_chance         # float
        self.__my_heal_range = the_heal_range           # tuple

    ### INTERNAL METHODS ###

    @final
    def _hit_response(self, the_dmg):
        """
        Updates HP and heals on a successful regen.
        Does nothing if self is dead.

        :param the_dmg: received damage.
        :return: regen message on success.
        """
        message = ""

        self._update_hp(the_dmg)

        if self.is_alive():
            # check regen
            heal = self._regen()
            if heal > 0:
                message += self._regen_msg(heal)

        return message

    def _regen_msg(self, the_heal):
        """
        Returns a successful regen message.

        :param the_heal: the number of points healed.
        :return: regen message.
        """
        return f"{self.name} healed for {the_heal} points!\n"

    def _regen(self):
        """
        Randomly determines if a regen is successful (within regen chance).
        Randomly generates the number of points healed within the heal range.

        :return: number of points healed.
        """
        heal = 0

        # chance to heal (random float within heal chance)
        if random.uniform(0,1) <= self.heal_chance:
            # heal number (random int within heal range)
            heal = random.randint(self.heal_range[0], self.heal_range[1])
            # set health
            self._update_hp(-heal)

        return heal

    ### PROPERTIES ###

    @property
    def heal_chance(self):
        return self.__my_heal_chance

    @property
    def heal_range(self):
        return self.__my_heal_range

    @heal_chance.setter
    def heal_chance(self, the_heal_chance):
        if 1 >= the_heal_chance >= 0:
            self.__my_heal_chance = the_heal_chance

    @heal_range.setter
    def heal_range(self, the_heal_range):
        self.__my_heal_range = the_heal_range


### MONSTER CLASSES ###

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