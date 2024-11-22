import sqlite3

class AdventurerSeeder:
    def __init__(self, db_path='data/dungeon_game.db'):
        self.db_path = db_path

    def populate_adventurers(self):
        """Inserts initial hero data into the adventurers table."""
        adventurers_data = [
            ("Mark", "Warrior", 125, 4, 0.8, 35, 60, 0.3, "Crushing Blow"),
            ("Noah", "Priest", 75, 5, 0.7, 25, 45, 0.2, "Divine Prayer"),
            ("Jayne", "Thief", 80, 6, 0.8, 20, 40, 0.4, "Surprise Attack"),
            ("Sean", "Bard", 85, 5, 0.8, 30, 50, 0.4, "Discombobulating Thought")
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
            print("Adventurers table populated.")
        except sqlite3.Error as e:
            print(f"Error populating adventurers table: {e}")