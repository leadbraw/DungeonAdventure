import random
from typing import final
from model.entities.entities import Entity


class Monster(Entity):
    def __init__(self, the_name, the_type, the_position, the_max_hp,
                 the_attack_speed, the_hit_chance, the_damage_range,
                 the_heal_chance, the_heal_range):
        """
        Represents a generic monster in the game.
        :param the_name: The name of the monster.
        :param the_type: The type of the monster (for display or behavior differentiation).
        :param the_position: Initial position of the monster.
        :param the_max_hp: Maximum health points of the monster.
        :param the_attack_speed: Attack speed of the monster.
        :param the_hit_chance: Hit chance of the monster.
        :param the_damage_range: Damage range of the monster.
        :param the_heal_chance: Heal chance of the monster.
        :param the_heal_range: Heal range of the monster.
        """
        super().__init__(the_name, the_position, the_max_hp,
                         the_attack_speed, the_hit_chance, the_damage_range)

        # Monster-specific attributes
        self.__my_type = the_type                  # str
        self.__my_heal_chance = the_heal_chance    # float
        self.__my_heal_range = the_heal_range      # tuple

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

        # Chance to heal (random float within heal chance)
        if random.uniform(0, 1) <= self.heal_chance:
            heal = random.randint(*self.heal_range)

        return heal

    ### PROPERTIES ###
    @property
    def heal_chance(self):
        return self.__my_heal_chance

    @heal_chance.setter
    def heal_chance(self, the_heal_chance):
        if 1 >= the_heal_chance >= 0:
            self.__my_heal_chance = the_heal_chance

    @property
    def heal_range(self):
        return self.__my_heal_range

    @heal_range.setter
    def heal_range(self, the_heal_range):
        self.__my_heal_range = the_heal_range

    @property
    def type(self):
        """
        :return: The type of the monster.
        """
        return self.__my_type

    @type.setter
    def type(self, the_type):
        """
        Sets the type of the monster.
        :param the_type: The new type of the monster.
        """
        self.__my_type = the_type