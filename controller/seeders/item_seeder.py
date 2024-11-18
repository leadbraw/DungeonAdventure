import sqlite3

class ItemSeeder:
    def __init__(self, db_path='data/dungeon_game.db'):
        self.db_path = db_path

    def populate_items(self):
        """Inserts initial item data into the items table."""
        items_data = [
            # Pillars of OO
            ("Pillar of Abstraction", "One of the four Pillars of OO required to win the game.",
             "effect handled externally", 0, 1),  # Use 0/1 for False/True
            ("Pillar of Encapsulation", "One of the four Pillars of OO required to win the game.",
             "effect handled externally", 0, 1),
            ("Pillar of Inheritance", "One of the four Pillars of OO required to win the game.",
             "effect handled externally", 0, 1),
            ("Pillar of Polymorphism", "One of the four Pillars of OO required to win the game.",
             "effect handled externally", 0, 1),

            # Potions (temporary items)
            ("Data Spike", "Deals 20-25 Damage to a Monster.", "effect handles externally", 0, 0),
            ("Healing Potion", "Heals the adventurer by 5-15 hit points.", "hp:5-15", 1, 0),
            ("Vision Potion", "Reveals surrounding rooms in the dungeon.", "effect handles externally", 1, 0)
        ]

        insert_query = """
            INSERT INTO items (name, description, ability, temporary, one_time_item)
            VALUES (?, ?, ?, ?, ?)
        """

        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.executemany(insert_query, items_data)
                conn.commit()
            print("Items table populated.")
        except sqlite3.Error as e:
            print(f"Error populating items table: {e}")
