from entities import Entity


class Adventurer(Entity):
    def __init__(self, the_name, the_position, the_hp,
                 the_attack_speed, the_chance_to_hit, the_damage_range,
                 the_chance_to_block):
        super().__init__(the_name, the_position, the_hp,
                         the_attack_speed, the_chance_to_hit, the_damage_range)

        # adventurer specific attributes (from database)
        self.__my_chance_to_block = the_chance_to_block

    def __calculate_attacks_per_turn(self, the_target):
        # compare attack speeds
        # return number of attacks
        pass

    def move(self, the_new_position):
        self.__my_position = the_new_position


class Warrior(Adventurer):
    pass


class Priest(Adventurer):
    pass


class Thief(Adventurer):
    pass