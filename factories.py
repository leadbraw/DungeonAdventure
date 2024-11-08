import random
from adventurers import Warrior, Priest, Thief
from monsters import Ogre, Gremlin, Skeleton

# utilizes singleton design pattern
class Factory:
    # will hold sql probing behaviors and create a lit
    # of sample monster objects at the beginning of each game

    #TODO SQL stats
    #TODO random name/position, random monster, random adventurer

    __monster_list = []

    @staticmethod
    def sql_something():
        pass

    @staticmethod
    def get_monster_list():
        if len(Factory.__monster_list) == 0:
            # populate list
            Factory.__monster_list.append(Factory.make_ogre())
            Factory.__monster_list.append(Factory.make_gremlin())
            Factory.__monster_list.append(Factory.make_skeleton())

        return Factory.__monster_list


    ############# MONSTER CONSTRUCTORS #############
    @staticmethod
    def make_ogre(the_name = "Corpsegrinder", the_position = (0,0)):
        return Ogre(the_name, the_position,
                       200, 2, 0.6, (30, 60),
                       0.1, (30, 60))

    @staticmethod
    def make_gremlin(the_name = "Nekrogoblikon", the_position = (0,0)):
        return Gremlin(the_name, the_position,
                       70, 5, 0.8, (15, 30),
                       0.4, (20, 40))

    @staticmethod
    def make_skeleton(the_name = "Whitechapel", the_position = (0,0)):
        return Skeleton(the_name, the_position,
                       100, 3, 0.8, (30, 50),
                       0.3, (30, 50))


    ############# ADVENTURER CONSTRUCTORS #############
    @staticmethod
    def make_warrior(the_name="Mark", the_position=(0, 0)):
        return Warrior(the_name, the_position,
                          125, 4, 0.8, (35, 60),
                          0.3)

    @staticmethod
    def make_priest(the_name="Noah", the_position=(0, 0)):
        return Priest(the_name, the_position,
                          75, 5, 0.7, (25, 45),
                          0.3)

    @staticmethod
    def make_thief(the_name="Jayne", the_position=(0, 0)):
        return Thief(the_name, the_position,
                          75, 6, 0.8, (20, 40),
                          0.4)

    @staticmethod
    def make_bard(the_name="Sean", the_position=(0, 0)):
        return Thief(the_name, the_position,
                     85, 5, 0.8, (30, 50),
                     0.4)

# m = Factory.make_ogre()
# a = Factory.make_thief()
# print(m.get_name(), ":", m.get_hp())
# print(a.get_name(), ":", a.get_hp())
# while(m.is_alive() and a.is_alive()):
#     print(m.attack(a))
#     print(a.attack(m))
#     print(m.get_name(), ":", m.get_hp(), ":", m.is_alive())
#     print(a.get_name(), ":", a.get_hp(), ":", a.is_alive())
