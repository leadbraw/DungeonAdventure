class Entity:
    def __init__(self, the_entity_id, the_name, the_health, the_position):
        self.__my_entityID = the_entity_id  # int
        self.__my_name = the_name           # str
        self.__my_health = the_health       # int
        self.__my_position = the_position   # tuple

    def attack(self, the_target):
        pass

    def __str__(self):
        return f"ID: {self.__my_entityID}; Name: {self.__my_name}; Health: {self.__my_health}; Position: {self.__my_position}"


class Adventurer:
    def __init__(self):
        pass


e1 = Entity(1, "thing", 10, (0,0))
print(e1)

