import random
from abc import abstractmethod
from typing import final


# utilizes template design pattern
class Entity:
    # TODO update method visibility

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

    @final
    def is_alive(self):
        return self.hp > 0

    @final
    def attack(self, the_target):
        message = ""

        for i in range(self.__calculate_attack_num(the_target)):

            if not the_target.is_alive() or not self.is_alive():
                break

            # attack roll (random float within the hit chance)
            if random.uniform(0,1) <= self.hit_chance:
                # damage roll (random int within damage_range)
                damage = random.randint(self.damage_range[0], self.damage_range[1])
                # set health
                message += f"{self.name} hit {the_target.name} for {damage} points!\n"
                message += the_target._hit_response(damage)

            else:
                message += f"{self.name}'s attack missed {the_target.name}.\n"

        return message[:len(message) - 1]

    @final
    def __calculate_attack_num(self, the_target):
        # determine number of attacks
        attacks_per_turn = int(self.attack_speed / the_target.attack_speed)
        if attacks_per_turn == 0:
            attacks_per_turn = 1

        return attacks_per_turn

    @final
    def _update_hp(self, the_diff):
        if self.hp - the_diff < 0:
            self.hp = 0
        elif self.hp - the_diff > self.max_hp:
            self.hp = self.max_hp
        else:
            self.hp = self.hp - the_diff

    @final
    def has_fainted_msg(self):
        return f"{self.name} fainted."

    @abstractmethod
    def __hit_response(self, the_dmg):
        # implemented in subclasses
        pass

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

    def __str__(self):
        return f"Name: {self.name}; HP: {self.hp}; Pos: {self.pos}"

