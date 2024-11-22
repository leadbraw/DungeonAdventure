from model.entities.adventurers import Warrior, Priest, Thief, Bard
from model.entities.monsters import Monster

# utilizes singleton design pattern
class Factory:

    # TODO implement constructors for monster, elite, adventurers getting info from managers

    @staticmethod
    def make_monster():
        pass

    @staticmethod
    def make_elite():
        pass

    @staticmethod
    def make_warrior(the_name="Mark", the_position=(0, 0)):
        warrior = Warrior(the_name, the_position,
                          125, 4, 0.8, (35, 60),
                          0.3)
        return warrior

    @staticmethod
    def make_priest(the_name="Noah", the_position=(0, 0)):
        priest = Priest(the_name, the_position,
                          75, 5, 0.7, (25, 45),
                          0.3)
        return priest

    @staticmethod
    def make_thief(the_name="Jayne", the_position=(0, 0)):
        thief = Thief(the_name, the_position,
                          75, 6, 0.8, (20, 40),
                          0.4)
        return thief

    @staticmethod
    def make_bard(the_name="Sean", the_position=(0, 0)):
        bard = Bard(the_name, the_position,
                     85, 5, 0.8, (30, 50),
                     0.4)
        return bard


# a = Factory.make_warrior()
# b = Factory.make_priest()
# print(b.name, ":", b.hp)
# print(a.name, ":", a.hp)
# while(True):
#     print(b.attack(a))
#     print(a.attack(b))
#     print(b)
#     print(a)
#     if not b.is_alive() or not a.is_alive():
#         break
#     print(b.special_action(a))
#     print(a.special_action(b))
#     print(b)
#     print(a)
#     if not b.is_alive() or not a.is_alive():
#         break
