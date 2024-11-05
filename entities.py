import random


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

    def is_alive(self):
        return self.get_hp() > 0

    def attack(self, the_target):
        message = ""

        for i in range(self._calculate_attack_num(the_target)):

            if not the_target.is_alive():
                break

            # attack roll (random float within the hit chance)
            if random.uniform(0,1) <= self.get_hit_chance():
                # damage roll (random int within damage_range)
                damage = random.randint(self.__my_damage_range[0], self.__my_damage_range[1])
                # set health
                message += f"\n{self.get_name()} hit {the_target.get_name()} for {damage} points!"
                message += the_target._update_hp(damage)

            else:
                message += f"\n{self.get_name()}'s attack missed {the_target.get_name()}."

        return message[1:] # skips the first /n character

    def _calculate_attack_num(self, the_target):
        # determine number of attacks
        attacks_per_turn = int(self.get_attack_speed() / the_target.get_attack_speed())
        if attacks_per_turn == 0:
            attacks_per_turn = 1

        return attacks_per_turn

    def _update_hp(self, the_diff):
        if self.__my_hp - the_diff < 0:
            self.set_hp(0)
        elif self.__my_hp - the_diff > self.__my_max_hp:
            self.set_hp(self.__my_max_hp)
        else:
            self.set_hp(self.__my_hp - the_diff)

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

    #TODO implement value check
    def set_pos(self, the_pos):
        self.__my_position = the_pos

    def set_hp(self, the_hp):
        if self.__my_max_hp >= the_hp >= 0:
            self.__my_hp = the_hp

    def __str__(self):
        return f"Name: {self.__my_name}; HP: {self.__my_hp}"

