class Item:
    def __init__(self, the_item_id, the_item_name, the_item_description, the_item_attributes, the_item_temporary, the_item_unique):
        """Initializer for Item with static attributes."""
        self.my_item_id = the_item_id
        self.my_item_name = the_item_name
        self.my_item_description = the_item_description
        self.my_item_attributes = the_item_attributes  # e.g., {"hp": 10}
        self.my_item_temporary = the_item_temporary
        self.my_item_unique = the_item_unique
        self.my_item_remaining_turns = 5 if the_item_temporary else None

    # def __repr__(self):
    #     """item debugging"""
    #     return (f"Item(id={self.my_item_id}, name='{self.my_item_name}', "
    #             f"description='{self.my_item_description}', attributes={self.my_item_attributes}, "
    #             f"temporary={self.my_item_temporary})")