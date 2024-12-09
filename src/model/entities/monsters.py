import random
from typing import final
from src.model.entities.entities import Entity


class Monster(Entity):
    def __init__(self, the_name, the_type, the_max_hp,
                 the_attack_speed, the_hit_chance, the_damage_range,
                 the_heal_chance, the_heal_range):
        """
        Represents a generic monster in the game.
        :param the_name: The name of the monster.
        :param the_type: The type of the monster (for display or behavior differentiation).
        :param the_max_hp: Maximum health points of the monster.
        :param the_attack_speed: Attack speed of the monster.
        :param the_hit_chance: Hit chance of the monster.
        :param the_damage_range: Damage range of the monster.
        :param the_heal_chance: Heal chance of the monster.
        :param the_heal_range: Heal range of the monster.
        """
        super().__init__(the_name, the_max_hp,
                         the_attack_speed, the_hit_chance, the_damage_range)

        # Monster-specific attributes
        self.__my_type = the_type.strip() if the_type else "Invalid type"  # Validate type
        self.__my_heal_chance = min(max(0, the_heal_chance), 1)  # Clamp between 0 and 1
        self.__my_heal_range = (
            max(1, the_heal_range[0]),
            max(1, the_heal_range[0], the_heal_range[1])
            # if heal range is incomplete defaults to 1
        ) if the_damage_range and len(the_damage_range) == 2 else (1, 1)

    """ INTERNAL METHODS """
    @final
    def _hit_response(self, the_dmg):
        """
        Updates HP and heals on a successful regen.
        Does nothing if self is dead.
        :param the_dmg: received damage.
        :return: regen message on success.
        """
        message = ""

        self._update_hp(the_dmg)
        if self.is_alive():
            heal = self._regen()
            if heal > 0:
                message += self._regen_msg(heal)
                self._update_hp(-heal)

        return message

    def _regen_msg(self, the_heal):
        """
        Returns a successful regen message.
        :param the_heal: the number of points healed.
        :return: regen message.
        """
        return f"{self.name} healed for {the_heal} points."

    def _regen(self):
        """
        Randomly determines if a regen is successful (within regen chance).
        Randomly generates the number of points healed within the heal range.
        :return: number of points healed.
        """
        heal = 0

        # Chance to heal (random float within heal chance)
        if random.uniform(0, 1) <= self.heal_chance:
            heal = random.randint(*self.heal_range)

        return heal

    def take_item_damage(self, damage):
        """
        Applies item-induced damage to the monster, bypassing regeneration.
        :param damage: The amount of damage to apply.
        :return: A string message describing the result.
        """
        if not self.is_alive():
            return f"{self.name} is already defeated!"

        # Directly update HP, bypassing regeneration logic
        self._update_hp(damage)
        message = f"{self.name} takes {damage} item damage."
        if not self.is_alive():
            message += f"{self.name} has been defeated!"

        return message

    """ PROPERTIES """
    @property
    def heal_chance(self):
        return self.__my_heal_chance

    @heal_chance.setter
    def heal_chance(self, the_heal_chance):
        if 1 >= the_heal_chance >= 0:
            self.__my_heal_chance = the_heal_chance

    @property
    def heal_range(self):
        return self.__my_heal_range

    @heal_range.setter
    def heal_range(self, the_heal_range):
        self.__my_heal_range = the_heal_range

    @property
    def type(self):
        """
        :return: The type of the monster.
        """
        return self.__my_type

    @type.setter
    def type(self, the_type):
        self.type = the_type

    # Method to define what gets pickled
    def __getstate__(self):
        # Return a dictionary of the object's state
        state = super().__getstate__()
        state['__my_type'] = self.__my_type
        state['__my_heal_chance'] = self.__my_heal_chance
        state['__my_heal_range'] = self.__my_heal_range
        # state.append({
        #         # 'name': self.name,
        #         # '__my_max_hp': self.__my_max_hp,
        #         # '__my_attack_speed': self.__my_attack_speed,
        #         # '__my_hit_chance': self.__my_hit_chance,
        #         # '__my_damage_range': self.__my_damage_range,
        #         # '__my_hp': self.__my_hp,
        #         '__my_type': self.__my_type,
        #         '__my_heal_chance': self.__my_heal_chance,
        #         '__my_heal_range': self.__my_heal_range})
        return state

    # Method to define how the object is restored
    def __setstate__(self, state):
        # Restore the object's state from the dictionary
        # self.name = state['name']
        # self.max_hp = state['__my_max_hp']
        # self.attack_speed = state['__my_attack_speed']
        # self.hit_chance = state['__my_hit_chance']
        # self.damage_range = state['__my_damage_range']
        # self.my_hp = state['hp']
        super().__setstate__(state)
        self.__my_type = state['__my_type']
        self.__my_heal_chance = state['__my_heal_chance']
        self.__my_heal_range = state['__my_heal_range']
