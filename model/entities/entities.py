import random
from abc import abstractmethod
from typing import final


class Entity:
    def __init__(self, the_name, the_position, the_max_hp, the_attack_speed, the_hit_chance, the_damage_range):
        # Private fields
        self.__my_name = the_name.strip() if the_name else "Unnamed Entity"  # Validate name
        self.__my_position = the_position if isinstance(the_position, tuple) else (0, 0)

        # Entity attributes with validation
        self.__my_max_hp = max(1, the_max_hp)  # Ensure at least 1 HP
        self.__my_attack_speed = max(1, the_attack_speed)  # Ensure non-zero attack speed
        self.__my_hit_chance = min(max(0, the_hit_chance), 1)  # Clamp between 0 and 1
        self.__my_damage_range = (
            max(0, the_damage_range[0]),
            max(0, the_damage_range[1])
        ) if the_damage_range and len(the_damage_range) == 2 else (0, 1)

        self.__my_hp = self.__my_max_hp  # Initialize HP to max HP

    def __str__(self):
        """Returns a string representation of the Entity."""
        return f"{self.name} {self.hp}/{self.max_hp} at {self.pos}"

    ### PUBLIC METHODS ###
    @final
    def is_alive(self):
        """Returns entity's life status."""
        return self.hp > 0

    @final
    def attack(self, the_target):
        """Performs an attack on the target, respecting attack speed and hit chance."""
        if not self.is_alive():
            return f"{self.name} cannot attack because it is not alive."

        if not the_target.is_alive():
            return f"{the_target.name} is already defeated."

        message = ""

        # Perform attacks based on attack speeds
        for _ in range(self.__calculate_attack_num(the_target)):
            if random.uniform(0, 1) <= self.hit_chance:  # Attack hit
                damage = random.randint(self.damage_range[0], self.damage_range[1])
                message += f"{self.name} hit {the_target.name} for {damage} points.\n"
                message += the_target._hit_response(damage)
            else:  # Attack missed
                message += f"{self.name}'s attack missed {the_target.name}.\n"

        return message.strip()

    ### INTERNAL METHODS ###
    @final
    def __calculate_attack_num(self, the_target):
        """Calculates the number of attacks based on attack speed."""
        return max(1, self.attack_speed // the_target.attack_speed)

    @final
    def _update_hp(self, the_diff):
        """
        Adjusts HP based on the given difference.
        Does not allow HP to exceed max HP or drop below 0.
        """
        new_hp = max(0, min(self.hp - the_diff, self.max_hp))
        if new_hp == 0 and self.hp > 0:
            return self._has_fainted_msg()
        self.hp = new_hp
        return ""

    @final
    def _has_fainted_msg(self):
        """Returns the faint message for the entity."""
        return f"{self.name} has fainted.\n"

    @abstractmethod
    def _hit_response(self, the_dmg):
        """Abstract method to be implemented in subclasses."""
        pass

    ### PROPERTIES ###
    @property
    def name(self):
        """Getter for the name."""
        return self.__my_name

    @property
    def pos(self):
        """Getter for the position."""
        return self.__my_position

    @property
    def max_hp(self):
        """Getter for max HP."""
        return self.__my_max_hp

    @property
    def attack_speed(self):
        """Getter for attack speed."""
        return self.__my_attack_speed

    @property
    def hit_chance(self):
        """Getter for hit chance."""
        return self.__my_hit_chance

    @property
    def damage_range(self):
        """Getter for damage range."""
        return self.__my_damage_range

    @property
    def hp(self):
        """Getter for current HP."""
        return self.__my_hp

    @hp.setter
    def hp(self, value):
        """Setter for HP with validation."""
        if 0 <= value <= self.__my_max_hp:
            self.__my_hp = value
        else:
            raise ValueError("HP must be between 0 and max HP.")

    @pos.setter
    def pos(self, value):
        """Setter for position with validation."""
        if isinstance(value, tuple) and len(value) == 2 and all(isinstance(x, int) for x in value):
            self.__my_position = value
        else:
            raise ValueError("Position must be a tuple of two integers.")