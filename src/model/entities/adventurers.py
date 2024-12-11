import random
from abc import abstractmethod
from typing import final
from src.model.entities.entities import Entity
from src.model.entities.inventory import Inventory


# optional: move special action constants into database and add parameters to be updated with them


class Adventurer(Entity):
    def __init__(self, the_name, the_type, the_max_hp,
                 the_attack_speed, the_hit_chance, the_damage_range,
                 the_block_chance):
        """
        Represents an adventurer.
        :param the_name: The name of the adventurer.
        :param the_type: The class of the adventurer.
        :param the_max_hp: Maximum health points of the adventurer.
        :param the_attack_speed: Attack speed of the adventurer.
        :param the_hit_chance: Hit chance of the adventurer.
        :param the_damage_range: Damage range of the adventurer.
        :param the_block_chance: Block chance of the adventurer.
        """
        super().__init__(the_name, the_max_hp, the_attack_speed, the_hit_chance, the_damage_range)
        self.__my_type = the_type.strip() if the_type else "Invalid type"  # Validate type
        self.__my_block_chance = min(max(0, the_block_chance), 1)  # Clamp between 0 and 1
        self.__inventory = Inventory()

    """ PUBLIC METHODS """
    @abstractmethod
    def special_action(self, the_target):
        # implemented in subclasses
        pass

    """ INTERNAL METHODS """
    @final
    def _hit_response(self, the_dmg):
        """
        Checks for a successful block and negates received damage on success.
        Updates HP otherwise.
        :param the_dmg: received damage.
        :return: block message on success.
        """
        message = ""

        if not self.is_alive():
            return message

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
        return f"You blocked the attack."

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

    def apply_buff(self, buff_value, buff_type):
        """
        Applies a permanent buff to the adventurer.

        :param buff_value: The value of the buff to apply.
        :param buff_type: The type of the buff (e.g., 'max_hp', 'block_chance', 'attack_damage', 'attack_speed').
        """
        if buff_type == "max_hp":
            self.max_hp = self.max_hp + buff_value  # Uses the setter for max_hp
            self._update_hp(-buff_value)
            print(f"{self.name}'s maximum HP increased by {buff_value}. New max HP: {self.max_hp}.")
        elif buff_type == "block_chance":
            self.block_chance = min(self.block_chance + (buff_value / 10), 1.0)
            print(
                f"{self.name}'s block chance increased by {buff_value / 10:.2f}. "
                f"New block chance: {self.block_chance:.2f}.")
        elif buff_type == "attack_damage":
            min_damage, max_damage = self.damage_range
            self.damage_range = (min_damage + buff_value, max_damage + buff_value)  # Uses the setter for damage_range
            print(f"{self.name}'s attack damage increased by {buff_value}. New damage range: {self.damage_range}.")
        elif buff_type == "attack_speed":
            self.attack_speed = self.attack_speed + buff_value  # Uses the setter for attack_speed
            print(f"{self.name}'s attack speed increased by {buff_value}. New attack speed: {self.attack_speed}.")
        elif buff_type == "hit_chance":
            self.hit_chance = buff_value
        else:
            print(f"Buff type '{buff_type}' is not recognized.")

    def heal_from_item(self, heal_amount):
        """
        Heals the adventurer by a specific amount from an item.
        :param heal_amount: The amount of HP to restore.
        """
        if self.hp < self.max_hp:
            healed = min(self.max_hp - self.hp, heal_amount)
            self._update_hp(-healed)  # Negative value to heal
            print(f"{self.name} healed for {healed} HP from an item. Current HP: {self.hp}/{self.max_hp}.")
        else:
            print(f"{self.name} is already at full health.")

    """ PROPERTIES """
    @property
    def type(self):
        return self.__my_type

    @property
    def block_chance(self):
        return self.__my_block_chance

    @property
    def inventory(self):
        return self.__inventory

    @type.setter
    def type(self, the_type):
        self.__my_type = the_type

    @block_chance.setter
    def block_chance(self, the_block_chance):
        if 1 >= the_block_chance >= 0:
            self.__my_block_chance = the_block_chance

    @inventory.setter
    def inventory(self, the_inventory):
        self.__inventory = the_inventory

    # Method to define what gets pickled
    def __getstate__(self):
        # Return a dictionary of the object's state
        state = super().__getstate__()
        state['__my_type'] = self.__my_type
        state['__my_block_chance'] = self.__my_block_chance
        state['__inventory'] = self.__inventory
        # state.append({
        #         # '__my_name': self.__my_name,
        #         # '__my_max_hp': self.__my_max_hp,
        #         # '__my_attack_speed': self.__my_attack_speed,
        #         # '__my_hit_chance': self.__my_hit_chance,
        #         # '__my_damage_range': self.__my_damage_range,
        #         # '__my_hp': self.__my_hp,
        #         '__my_type': self.__my_type,
        #         '__my_block_chance': self.__my_block_chance,
        #         '__inventory': self.__inventory})
        return state

    # Method to define how the object is restored
    def __setstate__(self, state):
        # Restore the object's state from the dictionary
        # self.__my_name = state['__my_name']
        # self.__my_max_hp = state['__my_max_hp']
        # self.__my_attack_speed = state['__my_attack_speed']
        # self.__my_hit_chance = state['__my_hit_chance']
        # self.__my_damage_range = state['__my_damage_range']
        # self.__my_hp = state['__my_hp']
        super().__setstate__(state)
        self.__my_type = state['__my_type']
        self.__my_block_chance = state['__my_block_chance']
        self.__inventory = state['__inventory']


""" ADVENTURER CLASSES """
""" Provides Warrior specific behavior.
    Attributes:
    __my_special_hit_chance (float): special attack hit chance.
    __my_special_dmg_range (tuple): special attack damage min and max.
    Methods:
    special_action(the_target): performs Crushing Blow.
"""


class Warrior(Adventurer):
    __my_special_hit_chance = 0.6
    __my_special_dmg_range = (85, 175)

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
        # crushing blow 85 to 175 dmg 60% chance to hit
        # attack roll (random float within the hit chance)
        if random.uniform(0, 1) <= self.__my_special_hit_chance:
            # damage roll (random int within damage_range)
            damage = random.randint(*self.__my_special_dmg_range)
            # set health
            message += f"{self.name} hit {the_target.name} for {damage} points."
            message += the_target._hit_response(damage)

        else:
            message += f"{self.name} missed the attack."

        return message[:len(message) - 1]

    def __special_action_msg(self, the_target):
        """
        Returns the Crushing Blow action message.
        :param the_target: attack target.
        :return: Crushing Blow message.
        """
        return f"{self.name} uses Crushing Blow on {the_target.name}."


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
        :param the_heal: heal points.
        :return: Divine Prayer message.
        """
        return f"{self.name} uses Divine Prayer and heals for {the_heal}."


""" Provides Thief specific behavior.
    Attributes:
    __my_normal_attack_chance (float): chance of a normal attack.
    __my_detection_chance (float): chance of being detected.
    Methods:
    special_action(the_target): performs Surprise Attack.
"""


class Thief(Adventurer):
    # __my_special hit chance = 0.4
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
        # miss: [0, 0.2)
        # hit: [0.2, 0.6)
        # extra hit: [0.6, 1]
        # attack roll (random float within the hit chance)
        attack_roll = random.uniform(0, 1)

        if attack_roll >= self.__my_detection_chance:
            # not detected: succeeds
            if attack_roll >= self.__my_detection_chance + self.__my_normal_attack_chance:
                # extra attack
                message += f"{self.name} gets an extra attack."
                message += self.attack(the_target)

            # normal attack
            message += "." + self.attack(the_target)

        else:
            message += f"{self.name} was detected."  # end statement

        return message  # utilizes Entity attack method trimming

    def __special_action_msg(self, the_target):
        """
        Returns the Surprise Attack action message.
        :param the_target: attack target.
        :return: Surprise Attack message.
        """
        return f"{self.name} uses Surprise Attack on {the_target.name}."


""" Provides Bard specific behavior.
    Attributes:
    __my_special_dmg_range (tuple): special action damage min and max.
    Methods:
    special_action(the_target): performs Discombobulating Tune.
"""


class Bard(Adventurer):
    __my_special_dmg_range = (30, 70)

    def special_action(self, the_target):
        """
        Performs Discombobulating Tune: hits the target for 30 to 70 points
        of damage. Bard takes half of the dealt damage.
        Tracks the attack and outputs the appropriate message.
        Does nothing if self is dead.
        :param the_target: attack target.
        :return: Discombobulating Tune outcome message.
        """
        message = ""
        if not self.is_alive():
            return message

        message += self.__special_action_msg(the_target)
        damage = random.randint(*self.__my_special_dmg_range)
        message += f"{self.name} hit {the_target.name} for {damage} points."
        message += the_target._hit_response(damage)
        message += f"{self.name} takes {int(damage / 2)} points of damage."
        self._update_hp(int(damage / 2))

        return message[:len(message) - 1]

    def __special_action_msg(self, the_target):
        """
        Returns the Discombobulating Tune action message.
        :param the_target: attack target.
        :return: Discombobulating Tune message.
        """
        return f"{self.name} uses Discombobulating Tune on {the_target.name}."
