import sqlite3

class ItemSeeder:
    def __init__(self, db_path='data/dungeon_game.db'):
        self.db_path = db_path

    def populate_items(self):
        """Inserts initial item data into the items table."""
        items_data = [
            # Pillars of OO (Permanent buffs targeting the adventurer)
            ("Pillar of Abstraction", "One of the four Pillars of OO. Grants +25 to max HP.",
             "adventurer", 1, 25, 25, "max_hp"),
            ("Pillar of Encapsulation", "One of the four Pillars of OO. Grants +0.1 to block chance.",
             "adventurer", 1, 1, 1, "block_chance"),
            ("Pillar of Inheritance", "One of the four Pillars of OO. Grants +5 to min and max attack damage.",
             "adventurer", 1, 5, 5, "attack_damage"),
            ("Pillar of Polymorphism", "One of the four Pillars of OO. Grants +1 to attack speed.",
             "adventurer", 1, 1, 1, "attack_speed"),

            # Potions (temporary items)
            ("Code Spike", "Deals 20-25 damage to a Monster.",
             "monster", 0, 20, 25, None),
            ("Energy Drink", "Heals the adventurer by 5-15 hit points.",
             "adventurer", 0, 5, 15, None),
            ("White Box", "Reveals surrounding rooms in the dungeon.",
             "room", 0, None, None, None)
        ]

        insert_query = """
            INSERT INTO items (name, description, target, one_time_item, effect_min, effect_max, buff_type)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """

        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.executemany(insert_query, items_data)
                conn.commit()
            #print("Items table populated.")
        except sqlite3.Error as e:
            print(f"Error populating items table: {e}")
