import sqlite3

class ItemSeeder:
    def __init__(self, db_path='data/dungeon_game.db'):
        self.db_path = db_path

    def populate_items(self):
        """Inserts initial item data into the items table."""
        items_data = [
            # Pillars of OO
            ("Pillar of Abstraction", "One of the four Pillars of OO required to win the game.", "effect handled externally", False, True),
            ("Pillar of Encapsulation", "One of the four Pillars of OO required to win the game.", "effect handled externally", False, True),
            ("Pillar of Inheritance", "One of the four Pillars of OO required to win the game.", "effect handled externally", False, True),
            ("Pillar of Polymorphism", "One of the four Pillars of OO required to win the game.", "effect handled externally", False, True),

            #Potions (temporary items)
            ("Healing Potion", "Heals he adventurer by 5-15 hit points.", "hp:5-15", True, False),
            ("Vision Potion", "Reveals surrounding rooms in the dungeon.", "effect handles externally", True, False)
        ]

        insert_query = """
            INSERT INTO items (name, description, ability, temporary, unique)
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
