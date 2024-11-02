class Entity:

    def __init__(self, the_name, the_position,
                 the_hp, the_min_dmg, the_max_dmg, the_attack_speed, the_chance_to_hit):
        self.__my_life_status = True
        self.__my_name = the_name                   # str
        self.__my_position = the_position           # tuple

        # stats updated from database
        self.__my_hp = the_hp                       # int
        self.__my_min_dmg = the_min_dmg             # int
        self.__my_max_dmg = the_max_dmg             # int
        self.__my_attack_speed = the_attack_speed   # int
        self.__my_chance_to_hit = the_chance_to_hit # float

    def attack(self, the_target):
        # determine attack rolls
        # determine damage rolls
        # set health
        # print success/failure
        pass

    def _get_attack_speed(self):
        # TODO check with Tom's code
        return self.__my_attack_speed

    def _update_hp(self, the_dmg):
        # TODO implement checks, add setters
        self.__my_hp = self.__my_hp - the_dmg

    def __str__(self):
        return f"Name: {self.__my_name}; Position: {self.__my_position}"


class Adventurer(Entity):

    def __calculate_attacks_per_turn(self, the_target):
        # compare attack speeds
        # return number of attacks
        pass

    def move(self, the_new_position):
        self.__my_position = the_new_position


class Monster(Entity):
    # add regens
    pass
