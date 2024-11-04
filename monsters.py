from entities import Entity


class Monster(Entity):
    def __init__(self, the_name, the_position, the_hp,
                 the_attack_speed, the_chance_to_hit, the_damage_range,
                 the_chance_to_heal, the_heal_range):
        super().__init__(the_name, the_position, the_hp,
                         the_attack_speed, the_chance_to_hit, the_damage_range)

        # monster specific attributes (from database)
        self.__my_chance_to_heal = the_chance_to_heal   # float
        self.__my_heal_range = the_heal_range           # tuple

    def regen(self):
        pass


class Ogre(Monster):
    pass


class Goblin(Monster):
    pass


class Skeleton(Monster):
    pass
