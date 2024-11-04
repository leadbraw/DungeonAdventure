

class Entity:
    # TODO getters/setters/attributes

    def __init__(self, the_name, the_position,
                 the_hp, the_attack_speed, the_chance_to_hit, the_damage_range):
        self.__my_life_status = True
        self.__my_name = the_name                       # str
        self.__my_position = the_position               # tuple

        # entity shared attributes (from database)
        self.__my_hp = the_hp                           # int
        self.__my_attack_speed = the_attack_speed       # int
        self.__my_chance_to_hit = the_chance_to_hit     # float
        self.__my_damage_range = the_damage_range       # tuple


    def attack(self, the_target):
        # attack roll
        # damage rolls
        # set health
        # print success/failure
        pass

    def _get_attack_speed(self):
        return self.__my_attack_speed

    def _update_hp(self, the_dmg):
        self.__my_hp = self.__my_hp - the_dmg

    def __str__(self):
        return f"Name: {self.__my_name}; Position: {self.__my_position}"
