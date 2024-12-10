import sqlite3

class MonsterSeeder:
    def __init__(self, db_path='data/dungeon_game.db'):
        self.db_path = db_path

    def populate_monsters(self):
        """Inserts initial monster data into the monsters table."""
        monsters_data = [
            ("Ogre", "Normal", 200, 2, 0.65, 30, 45, 0.2, 20, 30),
            ("Gremlin", "Normal", 70, 5, 0.85, 10, 20, 0.3, 15, 20),
            ("Skeleton", "Normal", 100, 3, 0.8, 20, 30, 0.1, 60, 100),
            ("Tom", "Elite", 250, 6, .85, 15, 35, .25, 25, 40)
        ]

        insert_query = """
            INSERT INTO monsters (name, type, max_HP, attack_speed, chance_to_hit,
                                  attack_damage_min, attack_damage_max, chance_to_heal, heal_range_min, heal_range_max)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM monsters")
                cursor.executemany(insert_query, monsters_data)
                conn.commit()
            #print(f"{len(monsters_data)} monsters added to the table.")
        except sqlite3.Error as e:
            print(f"Error populating monsters table: {e}")
