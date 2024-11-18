import random
from typing import final
from model.entities.entities import Entity


class Monster(Entity):
    def __init__(self, the_name, the_position, the_max_hp,
                 the_attack_speed, the_hit_chance, the_damage_range,
                 the_heal_chance, the_heal_range, the_type=None):
        """
        Represents a generic monster in the game.
        :param the_name: The name of the monster.
        :param the_position: Initial position of the monster.
        :param the_max_hp: Maximum health points of the monster.
        :param the_attack_speed: Attack speed of the monster.
        :param the_hit_chance: Hit chance of the monster.
        :param the_damage_range: Damage range of the monster.
        :param the_heal_chance: Heal chance of the monster.
        :param the_heal_range: Heal range of the monster.
        :param the_type: The type of the monster (optional, for display or behavior differentiation).
        """
        super().__init__(the_name, the_position, the_max_hp,
                         the_attack_speed, the_hit_chance, the_damage_range)

        # Encapsulated attributes with validation
        self.__my_heal_chance = min(max(0, the_heal_chance), 1) if the_heal_chance else 0.0  # Clamp between 0 and 1
        self.__my_heal_range = (
            max(0, the_heal_range[0]),
            max(0, the_heal_range[1])
        ) if the_heal_range and len(the_heal_range) == 2 else (0, 0)
        self.__type = the_type.strip() if the_type else "Unknown"

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
            # Check for regen
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
            # Heal number (random int within heal range)
            heal = random.randint(self.heal_range[0], self.heal_range[1])
            # Set health
            self._update_hp(-heal)

        return heal

    ### PROPERTIES ###

    @property
    def heal_chance(self):
        """Getter for heal chance."""
        return self.__my_heal_chance

    @heal_chance.setter
    def heal_chance(self, value):
        """Setter for heal chance with validation."""
        if 0 <= value <= 1:
            self.__my_heal_chance = value
        else:
            raise ValueError("Heal chance must be between 0 and 1.")

    @property
    def heal_range(self):
        """Getter for heal range."""
        return self.__my_heal_range

    @heal_range.setter
    def heal_range(self, value):
        """Setter for heal range with validation."""
        if isinstance(value, tuple) and len(value) == 2 and all(isinstance(x, int) for x in value) and value[0] >= 0 and value[1] >= 0:
            self.__my_heal_range = value
        else:
            raise ValueError("Heal range must be a tuple of two non-negative integers.")

    @property
    def type(self):
        """Getter for monster type."""
        return self.__type

    @type.setter
    def type(self, value):
        """Setter for monster type with validation."""
        if value and isinstance(value, str):
            self.__type = value.strip()
        else:
            raise ValueError("Type must be a non-empty string.")