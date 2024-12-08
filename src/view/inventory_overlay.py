import sys

import pygame
from constants import LIGHT_BLUE, FADED_BLUE, FADED_GRAY, PASTEL_RED
from src.view.gui_elements import Button


class InventoryOverlay:
    def __init__(self, screen, fonts, inventory, current_monster=None, current_room=None, dungeon=None):
        """Initializes the inventory overlay."""
        self._previous_frame = None
        self.screen = screen
        self.fonts = fonts
        self.inventory = inventory
        self.selected_item = None
        self.current_monster = current_monster
        self.current_room = current_room
        self.dungeon = dungeon

    def draw_overlay(self, overlay_x, overlay_y, overlay_width, overlay_height, opacity=200):
        """Draws the inventory overlay background."""
        overlay_surface = pygame.Surface((overlay_width, overlay_height))
        overlay_surface.set_alpha(opacity)
        overlay_surface.fill((30, 30, 30))  # Dark gray transparent background
        self.screen.blit(overlay_surface, (overlay_x, overlay_y))

    def draw_pillar_buttons(self, button_size, spacing):
        """Draws the pillar buttons on the top row."""
        pillar_names = ["Pillar of Abstraction", "Pillar of Encapsulation",
                        "Pillar of Inheritance", "Pillar of Polymorphism"]
        total_width = len(pillar_names) * button_size + (len(pillar_names) - 1) * spacing
        row_start_x = (650 - total_width) // 2  # Center row horizontally
        row_y = 6  # Fixed vertical position for the first row (6px from the top)
        buttons = []
        for i, name in enumerate(pillar_names):
            item_in_inventory = any(entry["item"].name == name for entry in self.inventory.items)
            color = LIGHT_BLUE if item_in_inventory else FADED_GRAY
            item_button = Button(
                color=color,
                x=row_start_x + i * (button_size + spacing),
                y=row_y,
                width=button_size,
                height=button_size,
                font=self.fonts["extra_small"],
                text_color=(255, 255, 255),
                text=name.split()[-1],  # Display only the pillar type (e.g., "Abstraction")
            )
            item_button.draw(self.screen)
            buttons.append(item_button)
        return buttons

    def draw_usable_item_buttons(self, button_size, spacing):
        """Draws the usable item buttons on the second row."""
        usable_items = ["Code Spike", "Energy Drink", "White Box"]
        total_width = len(usable_items) * button_size + (len(usable_items) - 1) * spacing
        row_start_x = (650 - total_width) // 2  # Center row horizontally
        row_y = 6 + button_size + 6  # Fixed vertical position: 6px top + 128px button + 6px spacing

        buttons = []
        for i, name in enumerate(usable_items):
            # Fetch item quantity from inventory
            quantity = next((entry["quantity"] for entry in self.inventory.items if entry["item"].name == name), 0)

            color = LIGHT_BLUE if quantity > 0 else FADED_BLUE

            # Create and draw the button
            item_button = Button(
                color=color,
                x=row_start_x + i * (button_size + spacing),
                y=row_y,
                width=button_size,
                height=button_size,
                font=self.fonts["small"],
                text_color=(255, 255, 255),
                # text=name.split()[0],  Display only the first word (e.g., "Code")
                text=f"{name.split()[0]} ({quantity})"
            )
            item_button.draw(self.screen)
            buttons.append((item_button, name, quantity))

        return buttons

    def draw_close_button(self, close_size, button_size, spacing):
        """Draws the close button at the specified position."""
        close_x = 650 - 40  # Align to the far right of the overlay
        # Align vertically with the center of the second row
        row_y = 6 + button_size + 6  # Second row's y position
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

    def handle_events(self, pillar_buttons, usable_item_buttons, close_button, target, current_monster, position,
                      dungeon):
        """Handles events for inventory overlay."""
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
        """Displays the inventory overlay and handles item selection."""
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
            self.draw_overlay(overlay_x, overlay_y, overlay_width, overlay_height)

            # Draw buttons
            pillar_buttons = self.draw_pillar_buttons(button_size, spacing)
            usable_item_buttons = self.draw_usable_item_buttons(button_size, spacing)
            close_button = self.draw_close_button(close_size, button_size, spacing)

            # Update display
            pygame.display.flip()

            # Handle events
            event_result = self.handle_events(
                pillar_buttons,
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