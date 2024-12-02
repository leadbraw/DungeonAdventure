import pygame
from constants import LIGHT_BLUE, FADED_BLUE, FADED_GRAY, PASTEL_RED
from controller.gui_elements import Button


class InventoryOverlay:
    def __init__(self, screen, fonts, inventory):
        """
        Initializes the inventory overlay.

        :param screen: The main game screen surface.
        :param fonts: A dictionary of fonts used in the game.
        :param inventory: The inventory object to display.
        """
        self._previous_frame = None
        self.screen = screen
        self.fonts = fonts
        self.inventory = inventory
        self.selected_item = None

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
                font=self.fonts["small"],
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
            quantity = next((entry["quantity"] for entry in self.inventory.items if entry["item"].name == name), 0)
            color = LIGHT_BLUE if quantity > 0 else FADED_BLUE
            item_button = Button(
                color=color,
                x=row_start_x + i * (button_size + spacing),
                y=row_y,
                width=button_size,
                height=button_size,
                font=self.fonts["small"],
                text_color=(255, 255, 255),
                text=name.split()[0],  # Display only the first word (e.g., "Code")
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

    def handle_events(self, pillar_buttons, usable_item_buttons, close_button):
        """
        Handles events for inventory overlay.
        :param pillar_buttons: List of pillar buttons on the top row.
        :param usable_item_buttons: List of usable item buttons on the second row.
        :param close_button: The close button for the overlay.
        :return: True if the overlay should remain open, False otherwise.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("[DEBUG] Quit event detected.")
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                print(f"[DEBUG] Mouse clicked at {mouse_pos}")

                # Check pillar buttons
                for button in pillar_buttons:
                    if button.is_hovered(mouse_pos):
                        print(f"[DEBUG] {button.text} button clicked (no action).")

                # Check usable item buttons
                for item_button, name, quantity in usable_item_buttons:
                    if item_button.is_hovered(mouse_pos) and quantity > 0:
                        print(f"[DEBUG] {name} button clicked, attempting to use...")
                        return True  # Keep overlay open (logic for issue 2 to be addressed later)

                # Check close button
                if close_button.is_hovered(mouse_pos):
                    print("[DEBUG] Close button clicked.")
                    self.screen.blit(self.previous_frame, (0, 0))  # Restore the previous UI frame
                    pygame.display.flip()  # Refresh the screen
                    return False  # Close overlay

        return True  # Keep overlay open

    def display(self):
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
        spacing = 6  # Consistent spacing
        close_size = 32

        # Save the current screen before displaying the overlay
        self.previous_frame = self.screen.copy()

        print("[DEBUG] Displaying inventory overlay...")

        while running:
            # Draw overlay
            self.draw_overlay(overlay_x, overlay_y, overlay_width, overlay_height)

            # Draw buttons
            pillar_buttons = self.draw_pillar_buttons(button_size, spacing)
            usable_item_buttons = self.draw_usable_item_buttons(button_size, spacing)
            close_button = self.draw_close_button(close_size, button_size, spacing)

            pygame.display.flip()

            # Handle events
            running = self.handle_events(pillar_buttons, usable_item_buttons, close_button)

        return self.selected_item