import random
from abc import abstractmethod
from typing import final


""" Provides the default behavior shared by all entities.
    
    Attributes:
    
    Passed in:
    name (string): entity's name.
    pos (tuple): entity's position.
    max_hp (int): entity's max hp.
    hit_chance (float): entity's attack hit chance percentage (0 and 1).
    damage_range (tuple): entity's attack min and max damage.
    
    Self-initialized:
    hp (int): entity's hp tracker. Initialized to max_hp.
    
    Methods:
    is_alive(): returns the entity's life status.
    attack(the_target): performs attacks on the target.    
"""
class Entity:

    def __init__(self, the_name, the_position,
                 the_max_hp, the_attack_speed, the_hit_chance, the_damage_range):
        self.__my_name = the_name                       # str
        self.__my_position = the_position               # tuple

        # entity shared attributes (from database)
        self.__my_max_hp = the_max_hp                   # int
        self.__my_attack_speed = the_attack_speed       # int
        self.__my_hit_chance = the_hit_chance           # float
        self.__my_damage_range = the_damage_range       # tuple

        self.__my_hp = self.__my_max_hp                 # int

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

            if not the_target.is_alive() or not self.is_alive():
                break

            # attack roll (random float within the hit chance)
            if random.uniform(0,1) <= self.hit_chance:
                # damage roll (random int within damage_range)
                damage = random.randint(self.damage_range[0], self.damage_range[1])
                # set health
                message += f"{self.name} hit {the_target.name} for {damage} points.\n"
                message += the_target._hit_response(damage)

            else:
                message += f"{self.name}'s attack missed {the_target.name}.\n"

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

    @final
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

    @property
    def max_hp(self):
        return self.__my_max_hp

    @property
    def attack_speed(self):
        return self.__my_attack_speed

    @property
    def hit_chance(self):
        return self.__my_hit_chance

    @property
    def damage_range(self):
        return self.__my_damage_range

    @property
    def hp(self):
        return self.__my_hp

    @name.setter
    def name(self, the_name):
        self.__my_name = the_name

    @pos.setter
    def pos(self, the_position):
        self.__my_position = the_position

    @max_hp.setter
    def max_hp(self, the_hp):
        if self.__my_max_hp >= the_hp >= 0:
            self.__my_hp = the_hp

    @attack_speed.setter
    def attack_speed(self, the_attack_speed):
        self.__my_attack_speed = the_attack_speed

    @hit_chance.setter
    def hit_chance(self, the_hit_chance):
        if 1 >= the_hit_chance >= 0:
            self.__my_hit_chance = the_hit_chance

    @damage_range.setter
    def damage_range(self, the_damage_range):
        self.__my_damage_range = the_damage_range

    @hp.setter
    def hp(self, the_hp):
        if self.__my_max_hp >= the_hp >= 0:
            self.__my_hp = the_hp

