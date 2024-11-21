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
        """
        Returns a string representation of the Entity.
        :return: string containing name, HP, and position.
        """
        return f"{self.name} {self.hp} {self.pos}"

    ### PUBLIC METHODS ###
    @final
    def is_alive(self):
        """
        Returns entity's life status.
        :return: True if the entity is alive; False otherwise.
        """
        return self.hp > 0

    @final
    def attack(self, the_target):
        """
        Performs an appropriate number of attacks based on own and the target's
        attack speeds. Randomly determines if an attack is successful (within attack
        chance) and triggers the target's hit response on success.
        Tracks the battle sequence and represents it as a string of performed
        attacks, missed attacks, successful hit responses, and faint messages.
        Does nothing if self or target is dead.
        :param the_target: attack target.
        :return: string of battle actions performed by entity and target.
        """
        message = ""

        for i in range(self.__calculate_attack_num(the_target)):
            if not self.is_alive() or not the_target.is_alive():
                break

            if random.uniform(0, 1) <= self.hit_chance:
                damage = random.randint(*self.damage_range)
                message += the_target._hit_response(damage)
            else:
                message += f"{self.name} missed the attack.\n"

        return message[:len(message) - 1]

    ### INTERNAL METHODS ###
    @final
    def __calculate_attack_num(self, the_target):
        """
        Returns the number of attacks based on the integer quotient of the entity's
        and target's attack speeds (min 1).
        :param the_target: attack target.
        :return: number of attacks.
        """
        # determine number of attacks
        attacks_per_turn = int(self.attack_speed / the_target.attack_speed)
        if attacks_per_turn == 0:
            attacks_per_turn = 1

        return attacks_per_turn

    @final
    def _update_hp(self, the_diff):
        """
        Subtracts the passed in difference from the entity's HP and updates the HP.
        Does not update HP to below 0 or above the HP max.
        :param the_diff: the HP difference.
        :return: faint message if HP reaches 0.
        """
        message = ""
        if self.hp - the_diff < 0:
            self.hp = 0
            message += self._has_fainted_msg()
        elif self.hp - the_diff > self.max_hp:
            self.hp = self.max_hp
        else:
            self.hp = self.hp - the_diff

        return message

    def _has_fainted_msg(self):
        """
        Returns the faint message for the entity.
        :return: faint message.
        """
        return f"{self.name} has fainted.\n"

    @abstractmethod
    def _hit_response(self, the_dmg):
        # implemented in subclasses
        pass

    ### PROPERTIES ###
    @property
    def name(self):
        return self.__my_name

    @property
    def pos(self):
        return self.__my_position

    @pos.setter
    def pos(self, the_position):
        if isinstance(the_position, tuple) and len(the_position) == 2:
            self.__my_position = the_position

    @property
    def max_hp(self):
        return self.__my_max_hp

    @property
    def hp(self):
        return self.__my_hp

    @hp.setter
    def hp(self, the_hp):
        if self.__my_max_hp >= the_hp >= 0:
            self.__my_hp = the_hp

    @property
    def hit_chance(self):
        return self.__my_hit_chance

    @property
    def damage_range(self):
        return self.__my_damage_range

    @property
    def attack_speed(self):
        return self.__my_attack_speed

    ### PUBLIC METHODS ###
    '''
    is_alive:
        Returns the entity's life status.

    attack:
        Performs attacks on the target based on attack speed, chance, and other attributes. '''

    ### INTERNAL METHODS ###
    '''
    __calculate_attack_num:
        Calculates the number of attacks based on the entity's and target's attack speeds.

    _update_hp:
        Updates the entity's HP based on the difference passed. Ensures HP stays within valid bounds.

    _has_fainted_msg:
        Generates a message when the entity's HP reaches 0. '''

    ### PROPERTIES ###
    '''
    name:
        Returns the entity's name.

    pos:
        Gets or sets the entity's position.

    max_hp:
        Returns the entity's maximum HP.

    hp:
        Gets or sets the entity's current HP, ensuring valid bounds. '''

    ### JAYNE ORIGINAL CODE ###

    # import random
    # from abc import abstractmethod
    # from typing import final
    #
    #
    # class Entity:
    #     def __init__(self, the_name, the_position, the_max_hp, the_attack_speed, the_hit_chance, the_damage_range):
    #         # Private fields
    #         self.__my_name = the_name.strip() if the_name else "Unnamed Entity"  # Validate name
    #         self.__my_position = the_position if isinstance(the_position, tuple) else (0, 0)
    #
    #         # Entity attributes with validation
    #         self.__my_max_hp = max(1, the_max_hp)  # Ensure at least 1 HP
    #         self.__my_attack_speed = max(1, the_attack_speed)  # Ensure non-zero attack speed
    #         self.__my_hit_chance = min(max(0, the_hit_chance), 1)  # Clamp between 0 and 1
    #         self.__my_damage_range = (
    #             max(0, the_damage_range[0]),
    #             max(0, the_damage_range[1])
    #         ) if the_damage_range and len(the_damage_range) == 2 else (0, 1)
    #
    #         self.__my_hp = self.__my_max_hp  # Initialize HP to max HP
    #
    #     def __str__(self):
    #         """
    #         Returns a string representation of the Entity.
    #         :return: string containing name, HP, and position.
    #         """
    #         return f"{self.name} {self.hp} {self.pos}"
    #
    #     ### PUBLIC METHODS ###
    #     @final
    #     def is_alive(self):
    #         """
    #         Returns entity's life status.
    #         :return: True if the entity is alive; False otherwise.
    #         """
    #         return self.hp > 0
    #
    #     @final
    #     def attack(self, the_target):
    #         """
    #         Performs an appropriate number of attacks based on own and the target's
    #         attack speeds. Randomly determines if an attack is successful (within attack
    #         chance) and triggers the target's hit response on success.
    #         Tracks the battle sequence and represents it as a string of performed
    #         attacks, missed attacks, successful hit responses, and faint messages.
    #         Does nothing if self or target is dead.
    #         param the_target: attack target.
    #         :return: string of battle actions performed by entity and target.
    #         """
    #         message = ""
    #
    #         for i in range(self.__calculate_attack_num(the_target)):
    #             if not self.is_alive() or not the_target.is_alive():
    #                 break
    #
    #             if random.uniform(0, 1) <= self.hit_chance:
    #                 damage = random.randint(*self.damage_range)
    #                 message += the_target._hit_response(damage)
    #             else:
    #                 message += f"{self.name} missed the attack.\n"
    #
    #         return message[:len(message) - 1]
    #
    #     ### INTERNAL METHODS ###
    #     @final
    #     def __calculate_attack_num(self, the_target):
    #         """
    #         Returns the number of attacks based on the integer quotient of the entity's
    #         and target's attack speeds (min 1).
    #         param the_target: attack target.
    #         :return: number of attacks.
    #         """
    #         # determine number of attacks
    #         attacks_per_turn = int(self.attack_speed / the_target.attack_speed)
    #         if attacks_per_turn == 0:
    #             attacks_per_turn = 1
    #
    #         return attacks_per_turn
    #
    #     @final
    #     def _update_hp(self, the_diff):
    #         """
    #         Subtracts the passed in difference from the entity's HP and updates the HP.
    #         Does not update HP to below 0 or above the HP max.
    #         :param the_diff: the HP difference.
    #         :return: faint message if HP reaches 0.
    #         """
    #         message = ""
    #         if self.hp - the_diff < 0:
    #             self.hp = 0
    #             message += self._has_fainted_msg()
    #         elif self.hp - the_diff > self.max_hp:
    #             self.hp = self.max_hp
    #         else:
    #             self.hp = self.hp - the_diff
    #
    #         return message
    #
    #     def _has_fainted_msg(self):
    #         """
    #         Returns the faint message for the entity.
    #         :return: faint message.
    #         """
    #         return f"{self.name} has fainted.\n"
    #
    #     @abstractmethod
    #     def _hit_response(self, the_dmg):
    #         # implemented in subclasses
    #         pass
    #
    #     ### PROPERTIES ###
    #     @property
    #     def name(self):
    #         return self.__my_name
    #
    #     @property
    #     def pos(self):
    #         return self.__my_position
    #
    #     @pos.setter
    #     def pos(self, the_position):
    #         if isinstance(the_position, tuple) and len(the_position) == 2:
    #             self.__my_position = the_position
    #
    #     @property
    #     def max_hp(self):
    #         return self.__my_max_hp
    #
    #     @property
    #     def hp(self):
    #         return self.__my_hp
    #
    #     @hp.setter
    #     def hp(self, the_hp):
    #         if self.__my_max_hp >= the_hp >= 0:
    #             self.__my_hp = the_hp
    #
    #     ### PUBLIC METHODS ###
    #     '''
    #     is_alive:
    #         Returns the entity's life status.
    #
    #     attack:
    #         Performs attacks on the target based on attack speed, chance, and other attributes. '''
    #
    #     ### INTERNAL METHODS ###
    #     '''
    #     __calculate_attack_num:
    #         Calculates the number of attacks based on the entity's and target's attack speeds.
    #
    #     _update_hp:
    #         Updates the entity's HP based on the difference passed. Ensures HP stays within valid bounds.
    #
    #     _has_fainted_msg:
    #         Generates a message when the entity's HP reaches 0. '''
    #
    #     ### PROPERTIES ###
    #     '''
    #     name:
    #         Returns the entity's name.
    #
    #     pos:
    #         Gets or sets the entity's position.
    #
    #     max_hp:
    #         Returns the entity's maximum HP.
    #
    #     hp:
    #         Gets or sets the entity's current HP, ensuring valid bounds.