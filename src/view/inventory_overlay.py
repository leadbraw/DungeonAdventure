import sys
import pygame
from constants import LIGHT_BLUE, FADED_BLUE, FADED_GRAY, PASTEL_RED, SPRITE_PATHS
from src.view.gui_elements import Button


class InventoryOverlay:
    """Class representing the overlay drawn on screen reflecting the adventurer's inventory."""

    def __init__(self, screen, fonts, inventory, pillar_status=None, current_monster=None, current_room=None,
                 dungeon=None):
        """Initializes the inventory overlay."""
        self._previous_frame = None
        self.previous_frame = None
        self.screen = screen
        self.fonts = fonts
        self.inventory = inventory
        self.pillar_status = pillar_status
        self.selected_item = None
        self.current_monster = current_monster
        self.current_room = current_room
        self.dungeon = dungeon
        self.current_floor = 1  # Initialize with a default value

    def draw_pillar_buttons(self, button_size, spacing):
        """
        Constructs/draws the pillar buttons with images centered at the top and text below indicating buffs.

        :param button_size: Size of each button.
        :param spacing: Space between each button.
        :return: All pillar buttons.
        """
        total_width = len(self.pillar_status) * button_size + (len(self.pillar_status) - 1) * spacing
        row_start_x = (650 - total_width) // 2  # Center row horizontally
        row_y = 6  # Fixed vertical position for the first row
        buttons = []

        # Buff descriptions for each pillar
        pillar_buffs = {
            "Pillar of Abstraction": "Max HP +25",
            "Pillar of Encapsulation": "Block +10%",
            "Pillar of Inheritance": "Attack +5",
            "Pillar of Polymorphism": "Speed +1"
        }

        for i, (name, acquired) in enumerate(self.pillar_status.items()):
            color = LIGHT_BLUE if acquired else FADED_GRAY

            # Draw button background
            item_button = Button(
                color=color,
                x=row_start_x + i * (button_size + spacing),
                y=row_y,
                width=button_size,
                height=button_size,
                font=self.fonts["extra_small"],
                text_color=(255, 255, 255),
                text=""  # Remove text if relying solely on the image
            )
            item_button.draw(self.screen)

            # Determine the image to display (shrink to 100x100)
            sprite_key = name.split()[-1].lower() + "_pillar"
            image_path = SPRITE_PATHS.get(
                sprite_key if acquired else "placeholder")  # Use a placeholder for blocked-out
            if image_path:
                image = pygame.image.load(image_path)
                image = pygame.transform.scale(image, (100, 100))  # Resize image to 100x100
                image_x = row_start_x + i * (button_size + spacing) + button_size // 2 - image.get_width() // 2
                image_y = row_y + 5  # Center image at the top with padding
                self.screen.blit(image, (image_x, image_y))

                # Display the buff text only if the pillar is acquired
                if acquired:
                    buff_text = pillar_buffs.get(name, "")
                    text_surface = self.fonts["extra_small"].render(buff_text, True, (255, 255, 255))
                    text_x = row_start_x + i * (
                                button_size + spacing) + button_size // 2 - text_surface.get_width() // 2
                    text_y = row_y + button_size - 20  # Position the text below the button
                    self.screen.blit(text_surface, (text_x, text_y))

            buttons.append(item_button)

        return buttons

    def draw_usable_item_buttons(self, button_size, spacing):
        """
        Constructs/draws usable item buttons with item name above, image centered, and quantity below.

        :param button_size: The size of each button.
        :param spacing: The spacing between each button.
        :return: All usable item buttons.
        """
        usable_items = ["Code Spike", "Energy Drink", "White Box"]
        total_width = len(usable_items) * button_size + (len(usable_items) - 1) * spacing
        row_start_x = (650 - total_width) // 2  # Center row horizontally
        row_y = 6 + button_size + 6  # Fixed vertical position: 6px top + button_size + 6px spacing

        buttons = []
        for i, name in enumerate(usable_items):
            # Fetch item quantity from inventory
            quantity = next((entry["quantity"] for entry in self.inventory.items if entry["item"].name == name), 0)

            color = LIGHT_BLUE if quantity > 0 else FADED_BLUE

            # Draw button background
            item_button = Button(
                color=color,
                x=row_start_x + i * (button_size + spacing),
                y=row_y,
                width=button_size,
                height=button_size,
                font=self.fonts["small"],
                text_color=(255, 255, 255),
                text="",  # No text on the button itself
            )
            item_button.draw(self.screen)

            # Render the item name above the image
            name_surface = self.fonts["extra_small"].render(name, True, (255, 255, 255))
            name_x = row_start_x + i * (button_size + spacing) + button_size // 2 - name_surface.get_width() // 2
            name_y = row_y + 8  # Adjusted padding above the image
            self.screen.blit(name_surface, (name_x, name_y))

            # Load and center usable item image within the button
            sprite_key = name.lower().replace(" ", "_")
            image_path = SPRITE_PATHS.get(sprite_key)
            if image_path:
                image = pygame.image.load(image_path)
                image = pygame.transform.scale(image, (64, 64))
                image_x = row_start_x + i * (button_size + spacing) + button_size // 2 - image.get_width() // 2
                image_y = name_y + name_surface.get_height() + 8  # Adjusted padding between name and image
                self.screen.blit(image, (image_x, image_y))

            # Display quantity text below the image
            quantity_text = f"x({quantity})"
            text_surface = self.fonts["extra_small"].render(quantity_text, True, (255, 255, 255))
            text_x = row_start_x + i * (button_size + spacing) + button_size // 2 - text_surface.get_width() // 2
            text_y = image_y + image.get_height() + 8  # Adjusted padding below the image
            self.screen.blit(text_surface, (text_x, text_y))

            buttons.append((item_button, name, quantity))
        return buttons

    def draw_close_button(self, close_size, button_size, spacing):
        """
        Draws the close button at the specified position on the overlay.

        :param close_size: The width/height of the close button.
        :param button_size: The size of each button. Used for positioning.
        :param spacing: The spacing between each button.
        :return: All usable item buttons.
        """
        close_x = 650 - 40  # Align to the far right of the overlay
        # Align vertically with the center of the second row
        row_y = 6 + button_size + spacing  # Second row's y position
        close_y = row_y + (button_size // 2) - (close_size // 2)
        close_button = Button(
            color=PASTEL_RED,
            x=close_x,
            y=close_y,
            width=close_size,
            height=close_size,
            font=self.fonts["small"],
            text_color=(255, 255, 255),
            text="X",
        )
        close_button.draw(self.screen)
        return close_button

    def handle_events(self, usable_item_buttons, close_button, target, current_monster, position, dungeon):
        """
        Handles events for inventory overlay.

        :param usable_item_buttons: List of consumable item buttons.
        :param close_button: The close button.
        :param target: The target for the item to be used.
        :param current_monster: The current monster being fought, if any.
        :param position: The position within the floor of the dungeon (or the current room as a fallback).
        :param dungeon: The current floor the adventurer is on (or the whole dungeon as a fallback).
        """

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("[DEBUG] Quit event detected. Exiting game.")
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                print(f"[DEBUG] Mouse clicked at {mouse_pos}")

                # Check usable item buttons
                for item_button, name, quantity in usable_item_buttons:
                    if item_button.is_hovered(mouse_pos) and quantity > 0:
                        print(f"[DEBUG] {name} button clicked, quantity available: {quantity}")

                        # Determine the actual target based on item type
                        if name == "White Box":
                            if isinstance(dungeon, list):  # Ensure dungeon is a list of floors
                                current_dungeon = dungeon[self.current_floor - 1]  # Get the current floor
                            else:
                                current_dungeon = dungeon  # Single floor passed directly
                            print(f"[DEBUG] Current dungeon for White Box: {current_dungeon}")

                            actual_target = (position, current_dungeon)
                        else:
                            actual_target = (
                                current_monster if name == "Code Spike" else
                                target if name == "Energy Drink" else
                                None
                            )

                        print(f"[DEBUG] Resolved target for '{name}': {actual_target}")

                        # Attempt to use the item
                        if actual_target and self.inventory.use_item(name, actual_target):
                            print(f"[DEBUG] Successfully used '{name}' on target: {actual_target}.")
                            return "item_used"
                        else:
                            print(f"[DEBUG] Failed to use '{name}' on target: {actual_target}.")
                            return "close_overlay"

                # Check close button
                if close_button.is_hovered(mouse_pos):
                    print("[DEBUG] Close button clicked.")
                    return "close_overlay"

        return "continue"  # Keep overlay open if no exit condition is met

    def display(self, target, position=None, dungeon=None):
        """
        Displays the inventory overlay and handles item selection.

        :param target: The target on which an item will be used.
        :param position: The position of the adventurer.
        :param dungeon: The dungeon.
        :return: The selected item.
        """
        running = True
        self.selected_item = None

        # Overlay dimensions
        overlay_width = 650
        overlay_height = 275
        overlay_x = 0
        overlay_y = 0

        # Button layout
        button_size = 128
        spacing = 6
        close_size = 32

        # Save the current screen before displaying the overlay
        self.previous_frame = self.screen.copy()

        print("[DEBUG] Displaying inventory overlay...")

        while running:
            # Draw overlay background
            pygame.draw.rect(self.screen, (30, 30, 30), (overlay_x, overlay_y, overlay_width, overlay_height))

            # Draw buttons
            self.draw_pillar_buttons(button_size, spacing) # buttons discarded
            usable_item_buttons = self.draw_usable_item_buttons(button_size, spacing)
            close_button = self.draw_close_button(close_size, button_size, spacing)

            # Update display
            pygame.display.flip()

            # Handle events
            event_result = self.handle_events(
                usable_item_buttons,
                close_button,
                target,
                self.current_monster,
                position or self.current_room,  # Fallback to current_room if position is None
                dungeon or self.dungeon  # Fallback to self.dungeon if dungeon is None
            )

            # Process the event result
            if event_result in {"item_used", "close_overlay"}:
                print("[DEBUG] Closing inventory overlay due to event.")
                self.screen.blit(self.previous_frame, (0, 0))  # Restore previous frame
                pygame.display.flip()
                running = False

        return self.selected_item
