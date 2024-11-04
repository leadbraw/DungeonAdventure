from adventurers import Warrior, Priest, Thief
from monsters import Ogre, Goblin, Skeleton


class Factory:
    # will hold sql probing behaviors and pass
    # relevant info to constructors when entities are made

    #TODO SQL stats
    #TODO random name/position, random monster, random adventurer

    @staticmethod
    def sql_something():
        pass


    ############# MONSTERS #############
    @staticmethod
    def make_ogre(the_name = "Corpsegrinder", the_position = (0,0)):
        return Ogre(the_name, the_position,
                       200, 2, 0.6, (30, 60),
                       0.1, (30, 60))

    @staticmethod
    def make_gremlin(the_name = "Nekrogoblikon", the_position = (0,0)):
        return Goblin(the_name, the_position,
                       70, 5, 0.8, (15, 30),
                       0.4, (20, 40))

    @staticmethod
    def make_skeleton(the_name = "Whitechapel", the_position = (0,0)):
        return Thief(the_name, the_position,
                       100, 3, 0.8, (30, 50),
                       0.3)


    ############# ADVENTURERS #############
    @staticmethod
    def make_warrior(the_name="Memoriam", the_position=(0, 0)):
        return Warrior(the_name, the_position,
                          125, 4, 0.8, (35, 60),
                          0.3)

    @staticmethod
    def make_priest(the_name="Belzebub", the_position=(0, 0)):
        return Priest(the_name, the_position,
                          75, 5, 0.7, (25, 45),
                          0.3)

    @staticmethod
    def make_thief(the_name="Obscura", the_position=(0, 0)):
        return Thief(the_name, the_position,
                          75, 6, 0.8, (20, 40),
                          0.4)