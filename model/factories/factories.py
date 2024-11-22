from model.entities.adventurers import Warrior, Priest, Thief, Bard
from model.entities.monsters import Monster
#importing the sqlite
import sqlite3

###############SQL Database##############################
# Connect to the SQLite database (it will create 'dungeon_game.db' if it doesn't exist)
conn = sqlite3.connect('../../data/dungeon_game.db')
# Create a cursor to execute SQL commands
cursor = conn.cursor()

# Drop the table if it exists to avoid conflicts
cursor.execute('DROP TABLE IF EXISTS monsters')

# Create the monsters table with the correct schema
cursor.execute('''
CREATE TABLE monsters (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    hit_points INTEGER,
    attack_speed INTEGER,
    chance_to_hit DOUBLE,
    min_damage INTEGER,
    max_damage INTEGER,
    chance_to_heal DOUBLE,
    min_heal_points INTEGER,
    max_heal_points INTEGER
)
''')

# Commit the changes
conn.commit()

# Insert some default monsters
def insert_monster(name, hit_points, attack_speed, chance_to_hit, min_damage, max_damage, chance_to_heal,
                   min_heal_points, max_heal_points):
    cursor.execute('''
    INSERT INTO monsters (name, hit_points, attack_speed, chance_to_hit, min_damage, max_damage, 
    chance_to_heal, min_heal_points, max_heal_points)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
    (name, hit_points, attack_speed, chance_to_hit, min_damage, max_damage, chance_to_heal, min_heal_points, max_heal_points))
    conn.commit()

# Monster entries
insert_monster("Corpsegrinder", 200, 2, 0.6, 30, 60, 0.1, 30, 60)
insert_monster("Nekrogoblikon", 70, 5, 0.8, 15, 30, 0.4, 20, 40)
insert_monster("Whitechapel", 100, 3, 0.8, 30, 50, 0.3, 30, 50)

# Retrieve monsters from the database
def fetch_monsters():
    cursor.execute("SELECT * FROM monsters")
    return cursor.fetchall()

# Fetch and display monsters
monsters = fetch_monsters()
for monster in monsters:
    print(monster)

# Close the connection when done
conn.close()

# utilizes singleton design pattern
class Factory:
    # will hold sql probing behaviors and create a lit
    # of sample monster objects at the beginning of each game

    #TODO random name

    __monster_list = []
    __hero = None

    @staticmethod
    def get_monsters_db():
        conn = sqlite3.connect('../../data/dungeon_game.db')
        cursor = conn.cursor()
        cursor.execute("SELECT name, hit_points, attack_speed, chance_to_hit, "
                       "min_damage, max_damage, chance_to_heal, "
                       "min_heal_points, max_heal_points")
        monsters = cursor.fetchall()
        conn.close()

        for (name, hit_points, attack_speed, chance_to_hit, min_damage, max_damage, chance_to_heal, min_heal_points,
             max_heal_points) in monsters:
            if name == "Corpsegrinder":
                Factory.__monster_list.append(Factory.make_ogre(name, (0,0), hit_points, attack_speed, chance_to_hit,
                         (min_damage, max_damage), chance_to_heal, (min_heal_points, max_heal_points)))
            elif name == "Nekrogoblikon":
                Factory.__monster_list.append(Factory.make_gremlin(name, (0, 0), hit_points, attack_speed, chance_to_hit, (min_damage, max_damage),
                            chance_to_heal, (min_heal_points, max_heal_points)))
            elif name == "Whitechapel":
                Factory.__monster_list.append(Factory.make_skeleton(name, (0, 0), hit_points, attack_speed, chance_to_hit, (min_damage, max_damage),
                             chance_to_heal, (min_heal_points, max_heal_points)))

    @staticmethod
    def get_monster_list():
        if len(Factory.__monster_list) == 0:
            # populate list
            Factory.get_monsters_db()

        return Factory.__monster_list

    @staticmethod
    def get_hero():
        return Factory.__hero

    @staticmethod
    def __set_hero(the_hero):
        Factory.__hero = the_hero

    ############# MONSTER CONSTRUCTORS #############

    ############# ADVENTURER CONSTRUCTORS #############
    @staticmethod
    def make_warrior(the_name="Mark", the_position=(0, 0)):
        warrior = Warrior(the_name, the_position,
                          125, 4, 0.8, (35, 60),
                          0.3)
        Factory.__set_hero(warrior)
        return warrior

    @staticmethod
    def make_priest(the_name="Noah", the_position=(0, 0)):
        priest = Priest(the_name, the_position,
                          75, 5, 0.7, (25, 45),
                          0.3)
        Factory.__set_hero(priest)
        return priest

    @staticmethod
    def make_thief(the_name="Jayne", the_position=(0, 0)):
        thief = Thief(the_name, the_position,
                          75, 6, 0.8, (20, 40),
                          0.4)
        Factory.__set_hero(thief)
        return thief

    @staticmethod
    def make_bard(the_name="Sean", the_position=(0, 0)):
        bard = Bard(the_name, the_position,
                     85, 5, 0.8, (30, 50),
                     0.4)
        Factory.__set_hero(bard)
        return bard


# m = Factory.get_monster_list()[0]
a = Factory.make_thief()
b = Factory.make_bard()
print(b.name, ":", b.hp)
print(a.name, ":", a.hp)
while(True):
    print(b.attack(a))
    print(a.attack(b))
    print(b)
    print(a)
    if not b.is_alive() or not a.is_alive():
        break
    print(b.special_action(a))
    print(a.special_action(b))
    print(b)
    print(a)
    if not b.is_alive() or not a.is_alive():
        break
