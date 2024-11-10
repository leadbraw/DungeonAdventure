import sqlite3

class ItemSeeder:
    def __init__(self, db_path='data/dungeon_game.db'):
        self.db_path = db_path

    def populate_items(self):
        """Inserts initial item data into the items table."""
        items_data = [
            # TODO: Populate with item data
            # Example data format for unique items:
            # ("Pillar of Composition", "Randomly raises 3 attributes.", "hp:10, min_dmg:10, attack_speed:3", False, True)
            # ("Pillar of Encapsulation", "Raises HP by 25.", "hp:25", False, True)
            # ("Pillar of Abstraction", "Reveals all visited rooms on map.", "effect handled externally", False, True)
            # Example data format for limited items:
            # ("Agile Potion", "Removes walls in the current room to adjacent rooms.", "effect handled externally", True, False)
            # ("Energy Drink", "Heals 5-10 health points per turn.", "hp:5", True, False)
            # Columns: (name, description, ability, temporary, unique)
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
