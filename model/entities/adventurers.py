import random
from abc import abstractmethod
from typing import final
from model.entities.entities import Entity

""" Provides the default behavior shared by all adventurers.

    Attributes:

    Entity shared:
    name (string): entity's name.
    pos (tuple): entity's position.
    max_hp (int): entity's max hp.
    hit_chance (float): entity's attack hit chance percentage (0 and 1).
    damage_range (tuple): entity's attack min and max damage.

    Adventurer specific:
    block_chance (float): adventurer's block chance percentage (0 to 1).

    Methods:
    move_to(the_new_position): updates the adventurer's position.
    special_action(the_target): performs a special action on the target (or self).
"""


class Adventurer(Entity):
    def __init__(self, the_name, the_position, the_max_hp,
                 the_attack_speed, the_hit_chance, the_damage_range,
                 the_block_chance):
        super().__init__(the_name, the_position, the_max_hp, the_attack_speed, the_hit_chance, the_damage_range)
        # adventurer specific attributes (from database)
        self.__my_block_chance = the_block_chance

    ### PUBLIC METHODS ###
    @final
    def move_to(self, the_new_position):
        """
        Updates the adventurer's position to the passed in position as long as
        they are within 1 unit of each other (adventurer's movement is continuous).
        :param the_new_position: new position.
        """
        if (abs(the_new_position[0] - self.pos[0]) <= 1
                and abs(the_new_position[1] - self.pos[1]) <= 1):
            self.pos = the_new_position

    @abstractmethod
    def special_action(self, the_target):
        # implemented in subclasses
        pass

    ### INTERNAL METHODS ###
    @final
    def _hit_response(self, the_dmg):
        """
        Checks for a successful block and negates received damage on success.
        Updates HP otherwise.
        :param the_dmg: received damage.
        :return: block message on success.
        """
        message = ""

        # check block
        if self._block():
            message += self._block_msg()
        else:
            message += self._update_hp(the_dmg)

        return message

    @final
    def _block_msg(self):
        """
        Returns a successful block message.
        :return: block message.
        """
        return f"{self.name} blocked the attack.\n"

    @final
    def _block(self):
        """
        Randomly determines if a block is successful (within block chance).
        :return: True on success; False on failure.
        """
        blocked = False
        # chance to block (random float within block chance)
        if random.uniform(0, 1) <= self.block_chance:
            blocked = True

        return blocked

    ### PROPERTIES ###
    @property
    def block_chance(self):
        return self.__my_block_chance

    @block_chance.setter
    def block_chance(self, the_block_chance):
        if 1 >= the_block_chance >= 0:
            self.__my_block_chance = the_block_chance


### ADVENTURER CLASSES ###
""" Provides Warrior specific behavior.
    Attributes:
    __my_special_hit_chance (float): special attack hit chance.
    __my_special_dmg_range (tuple): special attack damage min and max.
    Methods:
    special_action(the_target): performs Crushing Blow.
"""
class Warrior(Adventurer):
    __my_special_hit_chance = 0.4
    __my_special_dmg_range = (75, 175)

    def special_action(self, the_target):
        """
        Performs Crushing Blow: chance of hit 40%, damage range 75 to 175.
        Tracks the attack and outputs the appropriate message.
        Does nothing if self is dead.
        :param the_target: attack target.
        :return: Crushing Blow outcome message.
        """
        message = ""
        if not self.is_alive():
            return message

        message += self.__special_action_msg(the_target)
        # crushing blow 75 to 175 dmg 0.4 chance to hit
        # attack roll (random float within the hit chance)
        if random.uniform(0, 1) <= self.__my_special_hit_chance:
            # damage roll (random int within damage_range)
            damage = random.randint(*self.__my_special_dmg_range)
            # set health
            message += f"{self.name} hit {the_target.name} for {damage} points.\n"
            message += the_target._hit_response(damage)

        else:
            message += f"{self.name} missed the attack.\n"

        return message[:len(message) - 1]

    def __special_action_msg(self, the_target):
        """
        Returns the Crushing Blow action message.
        :param the_target: attack target.
        :return: Crushing Blow message.
        """
        return f"{self.name} uses Crushing Blow on {the_target.name}.\n"


""" Provides Priest specific behavior.
    Attributes:
    __my_special_heal_range_percentage (float): heal percentage range.
    Methods:
    special_action(the_target): performs Divine Prayer.
"""
class Priest(Adventurer):
    __my_special_heal_range_percentage = (0.4, 0.7)

    def special_action(self, the_target):
        """
        Performs Divine Prayer: heals between 40% to 70% of max HP.
        Tracks the heal and outputs the appropriate message.
        Does nothing if self is dead.
        :param the_target: attack target.
        :return: Divine Prayer outcome message.
        """
        message = ""
        if not self.is_alive():
            return message

        heal = int(random.uniform(*self.__my_special_heal_range_percentage) * self.max_hp)
        self._update_hp(-heal)
        message += self.__special_action_msg(heal)

        return message[:len(message) - 1]

    def __special_action_msg(self, the_heal):
        """
        Returns the Divine Prayer action message.
        :param the_target: attack target.
        :return: Divine Prayer message.
        """
        return f"{self.name} uses Divine Prayer and heals for {the_heal}.\n"


""" Provides Thief specific behavior.
    Attributes:
    __my_normal_attack_chance (float): chance of a normal attack.
    __my_detection_chance (float): chance of being detected.
    Methods:
    special_action(the_target): performs Surprise Attack.
"""
class Thief(Adventurer):
    # special hit chance = 0.4
    __my_normal_attack_chance = 0.4
    __my_detection_chance = 0.2

    def special_action(self, the_target):
        """
        Performs Surprise Attack: 40% chance of an extra attack, 40% chance
        of normal attack, 20% chance of being detected (no attack).
        Tracks the attack and outputs the appropriate message.
        Does nothing if self is dead.
        :param the_target: attack target.
        :return: Surprise Attack outcome message.
        """
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
            message += f"{self.name} was detected."  # end statement

        return message  # utilizes Entity attack method trimming

    def __special_action_msg(self, the_target):
        """
        Returns the Surprise Attack action message.
        :param the_target: attack target.
        :return: Surprise Attack message.
        """
        return f"{self.name} uses Surprise Attack on {the_target.name}.\n"


""" Provides Bard specific behavior.
    Attributes:
    __my_special_dmg_range (tuple): special action damage min and max.
    Methods:
    special_action(the_target): performs Discombobulating Thought.
"""


class Bard(Adventurer):
    __my_special_dmg_range = (30, 70)

    def special_action(self, the_target):
        """
        Performs Discombobulating Thought: hits the target for 30 to 70 points
        of damage. Bard takes half of the dealt damage.
        Tracks the attack and outputs the appropriate message.
        Does nothing if self is dead.
        :param the_target: attack target.
        :return: Discombobulating Thought outcome message.
        """
        message = ""
        if not self.is_alive():
            return message

        message += self.__special_action_msg(the_target)
        damage = random.randint(*self.__my_special_dmg_range)
        message += f"{self.name} hit {the_target.name} for {damage} points.\n"
        message += the_target._hit_response(damage)
        message += f"{self.name} takes {int(damage / 2)} points of damage.\n"
        self._update_hp(int(damage / 2))

        return message[:len(message) - 1]

    def __special_action_msg(self, the_target):
        """
        Returns the Discombobulating Thought action message.
        :param the_target: attack target.
        :return: Discombobulating Thought message.
        """
        return f"{self.name} uses Discombobulating Thought on {the_target.name}.\n"


if __name__ == "__main__":
    p = Warrior("war guy", (0, 0), 10, 6, 0.7, (1, 5), 0.3)
    q = Priest("heal guy", (0, 0), 10, 3, 0.7, (1, 5), 0.3)

    # Simulating a scenario
    # q.hp = 0  # Uncomment to simulate Priest being dead
    print(q.special_action(p))  # Priest performs a special action on Warrior
    print(p, q)  # Prints the state of both Warrior and Priest

### PUBLIC METHODS ###
'''
move_to:
Updates
the
adventurer
's position to the passed-in position if they are within 1 unit.

special_action:
Performs a special action on the target( or self).Must be implemented by subclasses. '''

### INTERNAL METHODS ###
'''
_hit_response:
Handles
the
adventurer
's response to being hit. Checks for a successful block.

_block_msg:
Generates a message indicating a successful block. 

_block:
Determines whether a block is successful based on block chance. '''

### PROPERTIES ###
'''
block_chance:
    Get or set the adventurer's block chance, ensuring the value is between 0 and 1. '''

### REMOVED METHODS ###
'''
# Below methods were removed from the earlier version.

# def move(self, the_new_position):
#     """
#     Directly updates the adventurer's position without any checks.
#     """
#     self.pos = the_new_position '''