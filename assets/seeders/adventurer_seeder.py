import sqlite3

class AdventurerSeeder:
    def __init__(self, db_path='data/dungeon_game.db'):
        self.db_path = db_path

    def populate_adventurers(self):
        """Inserts initial hero data into the adventurers table."""
        adventurers_data = [
            ("Mark", "Warrior", 135, 4, 0.75, 40, 75, 0.35, "Crushing Blow"),
            ("Noah", "Priest", 75, 3, 0.7, 35, 50, 0.38, "Divine Prayer"),
            ("Jayne", "Thief", 80, 6, 0.8, 25, 40, 0.33, "Surprise Attack"),
            ("Sean", "Bard", 85, 20, 0.8, 30, 80, 0.4, "Discombobulating Tune")
        ]

        insert_query = """
            INSERT INTO adventurers (name, type, max_HP, attack_speed, chance_to_hit,
                                attack_damage_min, attack_damage_max, chance_to_block, special_attack)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """

        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.executemany(insert_query, adventurers_data)
                conn.commit()
            #print("Adventurers table populated.")
        except sqlite3.Error as e:
            print(f"Error populating adventurers table: {e}")