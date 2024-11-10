import sqlite3

class MonsterSeeder:
    def __init__(self, db_path='data/dungeon_game.db'):
        self.db_path = db_path

    def populate_monsters(self):
        """Inserts initial monster data into the monsters table."""
        monsters_data = [
            # TODO: Populate with monster data
            # Example data format:
            # ("Goblin", "Common", 30, 5, 0.7, 2, 5, 0.1, 1, 3)
            # Columns: (name, type, HP, attack_speed, chance_to_hit,
            #           attack_min, attack_max, chance_to_heal, heal_range_min, heal_range_max)
        ]

        insert_query = """
            INSERT INTO monsters (name, type, HP, attack_speed, chance_to_hit,
                                  attack_min, attack_max, chance_to_heal, heal_range_min, heal_range_max)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """

        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.executemany(insert_query, monsters_data)
                conn.commit()
            print("Monsters table populated.")
        except sqlite3.Error as e:
            print(f"Error populating monsters table: {e}")
