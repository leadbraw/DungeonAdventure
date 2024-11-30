import pygame
from constants import LIGHT_BLUE, FADED_BLUE, FADED_GRAY
from controller.gui_elements import Button


class InventoryOverlay:
    def __init__(self, screen, fonts, inventory):
        """
        Initializes the inventory overlay.

        :param screen: The main game screen surface.
        :param fonts: A dictionary of fonts used in the game.
        :param inventory: The inventory object to display.
        """
        self.screen = screen
        self.fonts = fonts
        self.inventory = inventory
        self.selected_item = None

    def display(self):
        """Displays the inventory overlay and handles item selection."""
        running = True
        self.selected_item = None
        overlay_opacity = 150  # Transparency level (0-255)

        while running:
            # Draw transparent overlay background
            overlay_surface = pygame.Surface((300, 600))
            overlay_surface.set_alpha(overlay_opacity)
            overlay_surface.fill((30, 30, 30))  # Dark gray transparent background
            self.screen.blit(overlay_surface, (500, 0))

            # Pillar items (left column)
            pillar_names = ["Pillar of Abstraction", "Pillar of Encapsulation", "Pillar of Inheritance",
                            "Pillar of Polymorphism"]
            for i, name in enumerate(pillar_names):
                item_in_inventory = any(entry["item"].name == name for entry in self.inventory.items)
                color = LIGHT_BLUE if item_in_inventory else FADED_GRAY
                item_button = Button(
                    color=color,
                    x=510,  # Left column position
                    y=20 + i * 140,  # Vertical spacing
                    width=128,
                    height=128,
                    font=self.fonts["small"],
                    text_color=(255, 255, 255),
                    text=name.split()[-1],  # Display only the pillar type (e.g., "Abstraction")
                )
                item_button.draw(self.screen)

            # Usable items (right column)
            usable_items = ["Code Spike", "Energy Drink", "White Box"]
            item_buttons = []  # Store buttons to process events later
            for i, name in enumerate(usable_items):
                quantity = next((entry["quantity"] for entry in self.inventory.items if entry["item"].name == name), 0)
                color = LIGHT_BLUE if quantity > 0 else FADED_BLUE
                item_button = Button(
                    color=color,
                    x=650,  # Right column position
                    y=20 + i * 140,  # Match vertical spacing with the left column
                    width=128,
                    height=128,
                    font=self.fonts["small"],
                    text_color=(255, 255, 255),
                    text=name.split()[0],  # Display only the first word (e.g., "Code")
                )
                item_button.draw(self.screen)
                item_buttons.append((item_button, name, quantity))  # Add to list for event handling

            # Draw a close button at the bottom-right corner
            close_button = Button(
                color=LIGHT_BLUE,
                x=650,  # Positioned in the open space
                y=450,  # Bottom-right corner
                width=128,
                height=128,
                font=self.fonts["small"],
                text_color=(255, 255, 255),
                text="Close",
            )
            close_button.draw(self.screen)
            pygame.display.flip()

            # Consolidate event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()

                    # Check item buttons for usable items
                    for item_button, name, quantity in item_buttons:
                        if item_button.is_hovered(mouse_pos) and quantity > 0:
                            if self.inventory.use_item(name):
                                print(f"You used {name}.")
                                running = False
                            else:
                                print(f"Failed to use {name}.")

                    # Check close button
                    if close_button.is_hovered(mouse_pos):
                        running = False

            # Reset selected item after display loop
            if not self.selected_item:
                print("No item selected. Resetting selection.")
            return self.selected_item