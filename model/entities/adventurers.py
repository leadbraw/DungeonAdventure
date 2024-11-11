import random
from abc import abstractmethod
from typing import final
from model.entities.entities import Entity


class Adventurer(Entity):
    def __init__(self, the_name, the_position, the_max_hp,
                 the_attack_speed, the_hit_chance, the_damage_range,
                 the_block_chance):
        super().__init__(the_name, the_position, the_max_hp,
                         the_attack_speed, the_hit_chance, the_damage_range)

        # adventurer specific attributes (from database)
        self.__my_block_chance = the_block_chance

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
        return f"{self.name} blocked the attack.\n"

    @final
    def _block(self):
        blocked = False
        # chance to block (random float within block chance)
        if random.uniform(0,1) <= self.block_chance:
            blocked = True

        return blocked

    @property
    def block_chance(self):
        return self.__my_block_chance

    @block_chance.setter
    def block_chance(self, the_block_chance):
        if 1 >= the_block_chance >= 0:
            self.__my_block_chance = the_block_chance

    @final
    def move(self, the_new_position):
        self.pos = the_new_position

    @abstractmethod
    def special_action(self, the_target):
        # defined in subclasses
        pass


class Warrior(Adventurer):
    __my_special_hit_chance = 0.4
    __my_special_dmg_range = (75, 175)
    __my_special_attack_speed = 1

    def special_action(self, the_target):
        message = ""
        if not self.is_alive():
            return message

        # crushing blow 75 to 175 dmg 0.4 chance to hit
        # save current stats
        old_hit_chance = self.hit_chance
        old_dmg_range = self.damage_range
        old_attack_speed = self.attack_speed

        # use action specific stats
        self.hit_chance = self.__my_special_hit_chance
        self.damage_range = self.__my_special_dmg_range
        self.attack_speed = self.__my_special_attack_speed

        message += self.__special_action_msg(the_target)
        message += self.attack(the_target)

        # restore original stats
        self.hit_chance = old_hit_chance
        self.damage_range = old_dmg_range
        self.attack_speed = old_attack_speed

        return message[:len(message)] # utilizes Entity attack method trimming

    def __special_action_msg(self, the_target):
        return f"{self.name} uses Crushing Blow on {the_target.name}!\n"


class Priest(Adventurer):
    __my_special_heal_range_percentage = (0.4, 0.7)

    def special_action(self, the_target):
        message = ""
        if not self.is_alive():
            return message

        # heal number (random percentage of max hp within the specified range)
        heal = random.randint(int(self.__my_special_heal_range_percentage[0] * self.max_hp),
                              int(self.__my_special_heal_range_percentage[1] * self.max_hp))
        # set health
        self._update_hp(-heal)
        message += self.__special_action_msg(heal)

        return message[:len(message) - 1]

    def __special_action_msg(self, the_heal):
        return f"{self.name} uses Divine Prayer and heals for {the_heal}!\n"

class Thief(Adventurer):
    def special_action(self, the_target):
        if not self.is_alive():
            return ""
        pass

    def __special_action_msg(self, the_target):
        return f"{self.name} uses Sneak Attack on {the_target.name}!\n"

class Bard(Adventurer):
    def special_action(self, the_target):
        if not self.is_alive():
            return
        pass

    def __special_action_msg(self, the_target):
        return f"{self.name} uses Discombobulating Thought on {the_target.name}!"


# p = Warrior("war guy", (0,0), 10,
#                  6, 0.7, (1,5), 0.3)
#
# q = Priest("heal guy", (0,0), 10,
#                  3, 0.7, (1,5), 0.3)
# # q.hp = 0
# print(q.special_action(p))
# print(p, q)