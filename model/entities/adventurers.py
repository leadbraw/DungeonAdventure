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

    def special_action(self, the_target):
        message = ""
        if not self.is_alive():
            return message

        message += self.__special_action_msg(the_target)
        # crushing blow 75 to 175 dmg 0.4 chance to hit
        # attack roll (random float within the hit chance)
        if random.uniform(0, 1) <= self.__my_special_hit_chance:
            # damage roll (random int within damage_range)
            damage = random.randint(self.__my_special_dmg_range[0], self.__my_special_dmg_range[1])
            # set health
            message += f"{self.name} hit {the_target.name} for {damage} points.\n"
            message += the_target._hit_response(damage)

        else:
            message += f"{self.name}'s attack missed {the_target.name}.\n"

        return message[:len(message)-1]

    def __special_action_msg(self, the_target):
        return f"{self.name} uses Crushing Blow on {the_target.name}.\n"


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
        return f"{self.name} uses Divine Prayer and heals for {the_heal}.\n"

class Thief(Adventurer):
    # special hit chance = 0.4
    __my_normal_attack_chance = 0.4
    __my_detection_chance = 0.2

    def special_action(self, the_target):
        message = ""
        if not self.is_alive():
            return message

        message += self.__special_action_msg(the_target)
        # surprise attack 0.4 to hit, 0.4 to normal, 0.2 to skip
        # attack roll (random float within the hit chance)
        attack_roll = random.uniform(0, 1)

        if attack_roll >= self.__my_detection_chance:
            # not detected: succeeds
            if attack_roll >= self.__my_detection_chance + self.__my_normal_attack_chance:
                # extra attack
                message += f"{self.name} gets an extra attack!\n"
                message += self.attack(the_target) + "\n"

            # normal attack
            message += self.attack(the_target)

        else:
            message += f"{self.name} was detected." # end statement

        return message  # utilizes Entity attack method trimming

    def __special_action_msg(self, the_target):
        return f"{self.name} uses Surprise Attack on {the_target.name}.\n"

class Bard(Adventurer):
    __my_special_dmg_range = (30, 70)

    def special_action(self, the_target):
        message = ""
        if not self.is_alive():
            return message

        message += self.__special_action_msg(the_target)
        # discombobulating thought always hits but deals half the damage to attacker
        # damage roll (random int within damage_range)
        damage = random.randint(self.__my_special_dmg_range[0], self.__my_special_dmg_range[1])
        # set health
        message += f"{self.name} hit {the_target.name} for {damage} points.\n"
        message += the_target._hit_response(damage)
        message += f"{self.name} takes {int(damage/2)} points of damage.\n"
        self._update_hp(damage/2)

        return message[:len(message) - 1]

    def __special_action_msg(self, the_target):
        return f"{self.name} uses Discombobulating Thought on {the_target.name}.\n"


# p = Warrior("war guy", (0,0), 10,
#                  6, 0.7, (1,5), 0.3)
#
# q = Priest("heal guy", (0,0), 10,
#                  3, 0.7, (1,5), 0.3)
# # q.hp = 0
# print(q.special_action(p))
# print(p, q)