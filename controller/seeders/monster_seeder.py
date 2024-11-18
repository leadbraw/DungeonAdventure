import sqlite3

class MonsterSeeder:
    def __init__(self, db_path='data/dungeon_game.db'):
        self.db_path = db_path

    def populate_monsters(self):
        """Inserts initial monster data into the monsters table."""
        monsters_data = [
            ("Ogre", "Normal", 200, 2, 0.6, 30, 60, 0.1, 30, 60),
            ("Gremlin", "Normal", 70, 5, 0.8, 15, 30, 0.4, 20, 40),
            ("Skeleton", "Normal", 100, 3, 0.8, 30, 50, 0.3, 30, 50),
            ("Tom", "Elite", 250, 8, .85, 35, 55, .4, 38, 50)
        ]

        insert_query = """
            INSERT INTO monsters (name, type, HP, attack_speed, chance_to_hit,
                                  attack_min, attack_max, chance_to_heal, heal_range_min, heal_range_max)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """

        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM monsters")
                cursor.executemany(insert_query, monsters_data)
                conn.commit()
            print(f"{len(monsters_data)} monsters added to the table.")
        except sqlite3.Error as e:
            print(f"Error populating monsters table: {e}")
