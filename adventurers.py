import random
from entities import Entity


class Adventurer(Entity):
    def __init__(self, the_name, the_position, the_max_hp,
                 the_attack_speed, the_chance_to_hit, the_damage_range,
                 the_chance_to_block):
        super().__init__(the_name, the_position, the_max_hp,
                         the_attack_speed, the_chance_to_hit, the_damage_range)

        # adventurer specific attributes (from database)
        self.__my_chance_to_block = the_chance_to_block

    def _hit_response(self, the_dmg):
        message = ""

        # check block
        if self._block():
            message += self._block_msg()
        else:
            self._update_hp(the_dmg)

        return message

    def _block_msg(self):
        return f"\n{self.get_name()} blocked the attack."

    def _block(self):
        blocked = False
        # chance to block (random float within block chance)
        if random.uniform(0,1) <= self.__my_chance_to_block:
            blocked = True

        return blocked

    def get_block_chance(self):
        return self.__my_chance_to_block

    def set_block_chance(self, the_chance_to_block):
        if 1 >= the_chance_to_block >= 0:
            self.__my_chance_to_block = the_chance_to_block

    def move(self, the_new_position):
        self.set_pos(the_new_position)


class Warrior(Adventurer):
    pass

class Priest(Adventurer):
    pass

class Thief(Adventurer):
    pass

class Bard(Adventurer):
    pass