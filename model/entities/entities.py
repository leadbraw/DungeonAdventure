import random
from abc import abstractmethod
from typing import final


# utilizes template design pattern
class Entity:
    # TODO look into attributes

    def __init__(self, the_name, the_position,
                 the_max_hp, the_attack_speed, the_chance_to_hit, the_damage_range):
        self.__my_name = the_name                       # str
        self.__my_position = the_position               # tuple

        # entity shared attributes (from database)
        self.__my_max_hp = the_max_hp                   # int
        self.__my_attack_speed = the_attack_speed       # int
        self.__my_chance_to_hit = the_chance_to_hit     # float
        self.__my_damage_range = the_damage_range       # tuple

        self.__my_hp = self.__my_max_hp                 # int

    @final
    def is_alive(self):
        return self.get_hp() > 0

    @final
    def attack(self, the_target):
        message = ""

        for i in range(self._calculate_attack_num(the_target)):

            if not self.is_alive():
                message += self._has_fainted_msg()
                break

            if not the_target.is_alive():
                message += the_target._has_fainted_msg()
                break

            # attack roll (random float within the hit chance)
            if random.uniform(0,1) <= self.get_hit_chance():
                # damage roll (random int within damage_range)
                damage = random.randint(self.__my_damage_range[0], self.__my_damage_range[1])
                # set health
                message += f"\n{self.get_name()} hit {the_target.get_name()} for {damage} points!"
                message += the_target._hit_response(damage)

            else:
                message += f"\n{self.get_name()}'s attack missed {the_target.get_name()}."

        return message[1:] # skips the first /n character

    @final
    def _calculate_attack_num(self, the_target):
        # determine number of attacks
        attacks_per_turn = int(self.get_attack_speed() / the_target.get_attack_speed())
        if attacks_per_turn == 0:
            attacks_per_turn = 1

        return attacks_per_turn

    @final
    def _update_hp(self, the_diff):
        if self.__my_hp - the_diff < 0:
            self.set_hp(0)
        elif self.__my_hp - the_diff > self.__my_max_hp:
            self.set_hp(self.__my_max_hp)
        else:
            self.set_hp(self.__my_hp - the_diff)

    def _has_fainted_msg(self):
        return f"\n{self.get_name()} fainted."

    @abstractmethod
    def _hit_response(self, the_dmg):
        # implemented in subclasses
        pass

    def get_name(self):
        return self.__my_name

    def get_pos(self):
        return self.__my_position

    def get_attack_speed(self):
        return self.__my_attack_speed

    def get_hit_chance(self):
        return self.__my_chance_to_hit

    def get_damage_range(self):
        return self.__my_damage_range

    def get_hp(self):
        return self.__my_hp

    def set_name(self, the_name):
        self.__my_name = the_name

    def set_pos(self, the_position):
        self.__my_position = the_position

    def set_attack_speed(self, the_attack_speed):
        self.__my_attack_speed = the_attack_speed

    def set_hit_chance(self, the_chance_to_hit):
        if 1 >= the_chance_to_hit >= 0:
            self.__my_chance_to_hit = the_chance_to_hit

    def set_damage_range(self, the_damage_range):
        self.__my_damage_range = the_damage_range

    def set_hp(self, the_hp):
        if self.__my_max_hp >= the_hp >= 0:
            self.__my_hp = the_hp

    def __str__(self):
        return f"Name: {self.get_name()}; HP: {self.get_hp()}; Pos: {self.get_pos()}"

