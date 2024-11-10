import sqlite3

class HeroSeeder:
    def __init__(self, db_path='data/dungeon_game.db'):
        self.db_path = db_path

    def populate_heroes(self):
        """Inserts initial hero data into the heroes table."""
        heroes_data = [
            # TODO: Populate with hero data
            # Example data format:
            # ("HeroName", "Warrior", 75, 5, 0.75, 5, 15, 0.2, "Power Strike")
            # Columns: (name, type, max_HP, attack_speed, chance_to_hit,
            #           attack_damage_min, attack_damage_max, chance_to_block, special_attack)
        ]

        insert_query = """
            INSERT INTO heroes (name, type, max_HP, attack_speed, chance_to_hit,
                                attack_damage_min, attack_damage_max, chance_to_block, special_attack)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """

        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.executemany(insert_query, heroes_data)
                conn.commit()
            print("Heroes table populated.")
        except sqlite3.Error as e:
            print(f"Error populating heroes table: {e}")