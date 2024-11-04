import sqlite3
import json
from copy import deepcopy

class Item:
    def __init__(self,
                 the_item_id: int,
                 the_item_name: str,
                 the_item_description: str,
                 the_item_attributes: dict,
                 the_item_temporary: bool
                 ):
        """ Initializer, take note of order of params"""
        self.my_item_id = the_item_id
        self.my_item_name = the_item_name
        self.my_item_description = the_item_description
        self.my_item_attributes = the_item_attributes
        self.my_item_temporary = the_item_temporary
        self.my_item_remaining_turns = 5 if the_item_temporary else None

    def clone(self):
        """Creates a deep copy of this item. Used for limited use items. """
        return deepcopy(self)

    @staticmethod
    def create_from_database(the_item_id: int, db_path: str):
        """Loads an item from the database by its ID and returns an Item instance."""
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        query = """
        SELECT id, name, description, attributes, temporary
        FROM items
        WHERE id = ?
        """
        cursor.execute(query, (the_item_id,))
        item_data = cursor.fetchone()

        if item_data:
            item_id, name, description, attributes_json, temporary = item_data
            attributes = json.loads(attributes_json)
            item_instance = Item(item_id,
                                 name,
                                 description,
                                 attributes,
                                 bool(temporary)
                                 )

            conn.close()
            return item_instance
        else:
            conn.close()
            raise ValueError(f"Item with ID {the_item_id} not found in the database.")

    @staticmethod
    def create_test_items():
        """Creates a predefined list of items for testing purposes, without a database."""
        return [
            # Unique Pillars
            Item(1,
                 "Pillar of Encapsulation",
                 "Raises HP by 25.",
                 {"hp": 25},
                 False
                 ),

            Item(2,
                 "Pillar of Polymorphism",
                 "Randomly raises 2 attributes.",
                 {"max_dmg": 10, "chance_to_hit": 0.05},  # Random simulated
                 False
                 ),

            # Limited Potions and Code Spike
            Item(3,
                 "Energy Drink",
                 "Heals 5-10 health points per turn.",
                 {"hp": 7},
                 True  # Fixed value for simplicity; random can be simulated
                 ),

            Item(4,
                 "Code Spike",
                 "Deals 20-25 damage to an enemy.",
                 {},
                 False  # Damage handled externally
                 )
        ]