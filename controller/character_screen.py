import pygame
from constants import DARK_GREY, LIGHT_BLUE, MENU_BUTTON_WIDTH, MENU_BUTTON_HEIGHT, OFF_WHITE
from controller.gui_elements import Button


class CharacterScreen:
    """Handles the character selection and confirmation screen."""
    def __init__(self, screen, fonts):
        self.screen = screen
        self.fonts = fonts

        # Create buttons for adventurer selection
        self.noah_button = Button(DARK_GREY, self.screen.get_width() / 4 - 100, self.screen.get_height() / 3,
                                  MENU_BUTTON_WIDTH, MENU_BUTTON_HEIGHT, self.fonts["small"], OFF_WHITE, 'NOAH')
        self.jayne_button = Button(DARK_GREY, 3 * self.screen.get_width() / 4 - 100, self.screen.get_height() / 3,
                                   MENU_BUTTON_WIDTH, MENU_BUTTON_HEIGHT, self.fonts["small"], OFF_WHITE, 'JAYNE')
        self.sean_button = Button(DARK_GREY, self.screen.get_width() / 4 - 100, 2 * self.screen.get_height() / 3,
                                  MENU_BUTTON_WIDTH, MENU_BUTTON_HEIGHT, self.fonts["small"], OFF_WHITE, 'SEAN')
        self.mark_button = Button(DARK_GREY, 3 * self.screen.get_width() / 4 - 100, 2 * self.screen.get_height() / 3,
                                  MENU_BUTTON_WIDTH, MENU_BUTTON_HEIGHT, self.fonts["small"], OFF_WHITE, 'MARK')

        # Back button for initial selection screen
        self.initial_back_button = Button(
            OFF_WHITE, self.screen.get_width() / 2 - 70, self.screen.get_height() - 100,
            MENU_BUTTON_WIDTH, MENU_BUTTON_HEIGHT, self.fonts["small"], DARK_GREY, 'BACK'
        )

        # State management for transitions
        self.on_confirmation_screen = False
        self.selected_character = None
        self.confirm_button = Button(LIGHT_BLUE, self.screen.get_width() / 2 - 70, 2 * self.screen.get_height() / 3,
                                      MENU_BUTTON_WIDTH, MENU_BUTTON_HEIGHT, self.fonts["small"], OFF_WHITE, 'CONFIRM')
        self.confirm_back_button = Button(OFF_WHITE, self.screen.get_width() / 2 - 70, self.screen.get_height() - 100,
                                          MENU_BUTTON_WIDTH, MENU_BUTTON_HEIGHT, self.fonts["small"], DARK_GREY, 'BACK')

    def draw(self):
        """Draw the character selection or confirmation screen."""
        self.screen.fill(DARK_GREY)

        if self.on_confirmation_screen and self.selected_character:
            # Draw confirmation screen
            char_name = self.fonts["large"].render(self.selected_character["name"], True, OFF_WHITE)
            char_stats = self.fonts["small"].render(self.selected_character["stats"], True, OFF_WHITE)
            char_ability = self.fonts["small"].render(f"Ability: {self.selected_character['ability']}", True, OFF_WHITE)

            # Load and display character image
            char_image = pygame.image.load(self.selected_character["image"])
            char_image = pygame.transform.scale(char_image, (200, 200))
            self.screen.blit(char_image, (self.screen.get_width() / 2 - 300, 200))

            # Draw character information
            self.screen.blit(char_name, (self.screen.get_width() / 2 + 100, 100))
            self.screen.blit(char_stats, (self.screen.get_width() / 2 + 100, 200))
            self.screen.blit(char_ability, (self.screen.get_width() / 2 + 100, 250))

            # Draw buttons
            self.confirm_button.draw(self.screen)
            self.confirm_back_button.draw(self.screen)
        else:
            # Draw selection screen
            title = self.fonts["large"].render("CHOOSE ADVENTURER", True, LIGHT_BLUE)
            self.screen.blit(title, (self.screen.get_width() / 2 - title.get_width() / 2,
                                     self.screen.get_height() / 6 - title.get_height() / 2))

            # Draw adventurer selection buttons
            self.noah_button.draw(self.screen)
            self.jayne_button.draw(self.screen)
            self.sean_button.draw(self.screen)
            self.mark_button.draw(self.screen)

            # Draw the back button for the initial selection screen
            self.initial_back_button.draw(self.screen)

    def handle_event(self, event):
        """Handle events for character selection or confirmation."""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left click
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if self.on_confirmation_screen:
                if self.confirm_button.is_hovered((mouse_x, mouse_y)):
                    print(f"{self.selected_character['name']} has been selected!")
                    return "select", self.selected_character["name"]
                elif self.confirm_back_button.is_hovered((mouse_x, mouse_y)):
                    self.on_confirmation_screen = False
            else:
                if self.noah_button.is_hovered((mouse_x, mouse_y)):
                    self.selected_character = {
                        "name": "Noah",
                        "stats": "HP: 75, MP: 50",
                        "ability": "Heal",
                        "image": "assets/images/noah.png"
                    }
                    self.on_confirmation_screen = True
                elif self.jayne_button.is_hovered((mouse_x, mouse_y)):
                    self.selected_character = {
                        "name": "Jayne",
                        "stats": "HP: 75, MP: 60",
                        "ability": "Surprise Attack",
                        "image": "assets/images/jayne.png"
                    }
                    self.on_confirmation_screen = True
                elif self.sean_button.is_hovered((mouse_x, mouse_y)):
                    self.selected_character = {
                        "name": "Sean",
                        "stats": "HP: 90, MP: 40",
                        "ability": "Music",
                        "image": "assets/images/sean.png"
                    }
                    self.on_confirmation_screen = True
                elif self.mark_button.is_hovered((mouse_x, mouse_y)):
                    self.selected_character = {
                        "name": "Mark",
                        "stats": "HP: 125, MP: 30",
                        "ability": "Crushing Blow",
                        "image": "assets/images/mark.png"
                    }
                    self.on_confirmation_screen = True
                elif self.initial_back_button.is_hovered((mouse_x, mouse_y)):
                    # Back out from the initial screen
                    return "back", None
        return None, None

    def run(self):
        """Main loop for character selection and confirmation."""
        import sys
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                action, data = self.handle_event(event)
                if action == "select":
                    # Return the selected hero name to main
                    return data
                elif action == "back":
                    # Return to main menu
                    return None

            self.draw()
            pygame.display.flip()