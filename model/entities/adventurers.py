import random
from abc import abstractmethod
from typing import final
from model.entities.entities import Entity


class Adventurer(Entity):
    def __init__(self, the_name, the_position, the_max_hp,
                 the_attack_speed, the_chance_to_hit, the_damage_range,
                 the_chance_to_block):
        super().__init__(the_name, the_position, the_max_hp,
                         the_attack_speed, the_chance_to_hit, the_damage_range)

        # adventurer specific attributes (from database)
        self.__my_chance_to_block = the_chance_to_block

    @final
    def _hit_response(self, the_dmg):
        message = ""

        # check block
        if self._block():
            message += self._block_msg()
        else:
            self._update_hp(the_dmg)

        return message

    @final
    def _block_msg(self):
        return f"\n{self.name} blocked the attack."

    @final
    def _block(self):
        blocked = False
        # chance to block (random float within block chance)
        if random.uniform(0,1) <= self.chance_to_block:
            blocked = True

        return blocked

    @property
    def chance_to_block(self):
        return self.__my_chance_to_block

    @chance_to_block.setter
    def chance_to_block(self, the_chance_to_block):
        if 1 >= the_chance_to_block >= 0:
            self.__my_chance_to_block = the_chance_to_block

    @final
    def move(self, the_new_position):
        self.pos = the_new_position

    @abstractmethod
    def special_action(self):
        # defined in adventurer subclasses
        pass


class Warrior(Adventurer):
    @abstractmethod
    def special_action(self):
        # defined in adventurer subclasses
        pass

class Priest(Adventurer):
    @abstractmethod
    def special_action(self):
        # defined in adventurer subclasses
        pass

class Thief(Adventurer):
    @abstractmethod
    def special_action(self):
        # defined in adventurer subclasses
        pass

class Bard(Adventurer):
    @abstractmethod
    def special_action(self):
        # defined in adventurer subclasses
        pass


# p = Bard("this guy", (0,0), 10,
#                  6, 0.7, (1,5), 0.3)
# print(p.attack(p))
# print(p.name, p.hp)