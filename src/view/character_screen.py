import pygame
from constants import DARK_GREY, LIGHT_BLUE, MENU_BUTTON_WIDTH, MENU_BUTTON_HEIGHT, OFF_WHITE, FADED_BLUE, FADED_GRAY, \
    MEDIUM_GREY, BACKGROUND_COLOR, PASTEL_RED
from src.view.gui_elements import Button
from src.model.managers.adventurer_manager import AdventurerManager


class CharacterScreen:
    """Handles the character selection and confirmation screen."""

    def __init__(self, screen, fonts):
        self.screen = screen
        self.fonts = fonts

        self.adventurer_manager = AdventurerManager.get_instance()

        self.adventurer_buttons = {}
        self._initialize_adventurer_buttons()

        self.initial_back_button = Button(
            PASTEL_RED, self.screen.get_width() / 2 - 70, self.screen.get_height() - 100,
            MENU_BUTTON_WIDTH, MENU_BUTTON_HEIGHT,
            self.fonts["small"], DARK_GREY, 'BACK'
        )

        # State management for transitions
        self.on_confirmation_screen = False
        self.selected_character = None
        self.confirm_button = Button(
            FADED_BLUE, self.screen.get_width() / 2 - MENU_BUTTON_WIDTH / 2, self.screen.get_height() - 150,
            MENU_BUTTON_WIDTH, MENU_BUTTON_HEIGHT,
            self.fonts["small"], DARK_GREY, 'CONFIRM'
        )
        self.confirm_back_button = Button(
            PASTEL_RED, self.screen.get_width() / 2 - MENU_BUTTON_WIDTH / 2, self.screen.get_height() - 100,
            MENU_BUTTON_WIDTH, MENU_BUTTON_HEIGHT,
            self.fonts["small"], DARK_GREY, 'BACK'
        )

    def _initialize_adventurer_buttons(self):
        """Dynamically create buttons for all adventurers."""
        adventurer_data = self.adventurer_manager.get_adventurer_data()
        positions = [
            (self.screen.get_width() / 4 - 75, self.screen.get_height() / 3),
            (535, self.screen.get_height() / 3),
            (self.screen.get_width() / 4 - 75, 2 * self.screen.get_height() / 3),
            (535, 2 * self.screen.get_height() / 3)
        ]

        for idx, (name, data) in enumerate(adventurer_data.items()):
            x, y = positions[idx % len(positions)]
            self.adventurer_buttons[name] = Button(
                OFF_WHITE, x, y, MENU_BUTTON_WIDTH, MENU_BUTTON_HEIGHT,
                self.fonts["small"], DARK_GREY, name.upper()
            )

    @staticmethod
    def _wrap_text(text, font, max_width):
        """Wrap text to fit within the max width."""
        words = text.split(' ')
        lines = []
        current_line = ""
        for word in words:
            test_line = f"{current_line} {word}".strip()
            if font.size(test_line)[0] <= max_width:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word
        lines.append(current_line)
        return lines

    def draw(self):
        """Draw the character selection or confirmation screen."""
        self.screen.fill(DARK_GREY)

        if self.on_confirmation_screen and self.selected_character:
            char_name = self.fonts["large"].render(
                self.selected_character["name"], True, OFF_WHITE
            )
            details = [
                f"Class: {self.selected_character['type']}",
                f"HP: {self.selected_character['max_HP']}",
                f"Attack Speed: {self.selected_character['attack_speed']}",
                f"Hit Chance: {self.selected_character['chance_to_hit'] * 100:.1f}%",
                f"Attack Damage: {self.selected_character['attack_damage_min']} - "
                f"{self.selected_character['attack_damage_max']}",
                f"Block Chance: {self.selected_character['chance_to_block'] * 100:.1f}%"
            ]

            label_width = self.fonts["small"].size("Ability: ")[0]
            space_width = self.fonts["small"].size(" ")[0]
            indent_spaces = label_width // space_width
            raw_ability_text = f"Ability: {self.selected_character['special_attack']}"
            wrapped_lines = self._wrap_text(
                raw_ability_text, self.fonts["small"], max_width=300
            )

            if len(wrapped_lines) > 1:
                for i in range(1, len(wrapped_lines)):
                    wrapped_lines[i] = " " * indent_spaces + wrapped_lines[i]

            details.extend(wrapped_lines)

            char_image = pygame.image.load(self.selected_character["image"])
            char_image = pygame.transform.scale(char_image, (256, 256))
            self.screen.blit(char_image, (self.screen.get_width() / 4 - 128, 100))

            self.screen.blit(char_name, (self.screen.get_width() / 2 + 100, 20))
            spacing = 50
            start_y = 100
            for idx, detail in enumerate(details):
                text_surface = self.fonts["small"].render(detail, True, OFF_WHITE)
                self.screen.blit(
                    text_surface, (self.screen.get_width() / 2 + 100, start_y + idx * spacing)
                )

            self.confirm_button.draw(self.screen, True)
            self.confirm_back_button.draw(self.screen, True)
        else:
            title = self.fonts["large"].render("CHOOSE ADVENTURER", True, LIGHT_BLUE)
            self.screen.blit(
                title,
                (
                    self.screen.get_width() / 2 - title.get_width() / 2,
                    self.screen.get_height() / 6 - title.get_height() / 2,
                )
            )

            for button in self.adventurer_buttons.values():
                button.draw(self.screen, True)

            self.initial_back_button.draw(self.screen, True)

    def handle_event(self, event):
        """Handle events for character selection or confirmation."""
        if event.type == pygame.MOUSEBUTTONDOWN and (event.button == 1 or event.button == 3):
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if self.on_confirmation_screen:
                if self.confirm_button.is_hovered((mouse_x, mouse_y)):
                    if event.button == 1:
                        print(f"{self.selected_character['name']} has been selected!")
                        return "select", self.selected_character["name"]
                    elif event.button == 3:
                        print(f"{self.selected_character['name']} has been selected in DEBUG mode!")
                        return "debug", self.selected_character["name"]
                elif self.confirm_back_button.is_hovered((mouse_x, mouse_y)):
                    self.on_confirmation_screen = False
            else:
                for name, button in self.adventurer_buttons.items():
                    if button.is_hovered((mouse_x, mouse_y)):
                        raw_data = self.adventurer_manager.get_adventurer_data(name)
                        self.selected_character = {
                            "name": name,
                            "type": raw_data[2],
                            "max_HP": raw_data[3],
                            "attack_speed": raw_data[4],
                            "chance_to_hit": raw_data[5],
                            "attack_damage_min": raw_data[6],
                            "attack_damage_max": raw_data[7],
                            "chance_to_block": raw_data[8],
                            "special_attack": raw_data[9],
                            "image": f"assets/images/{name.lower()}.png"
                        }
                        self.on_confirmation_screen = True
                        break
                if self.initial_back_button.is_hovered((mouse_x, mouse_y)):
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
                    return data, "select"
                elif action == "back":
                    return None
                elif action == "debug":
                    return data, "debug"

            self.draw()
            pygame.display.flip()
