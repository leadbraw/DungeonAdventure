import pygame
from constants import DARK_GREY, LIGHT_BLUE, MENU_BUTTON_WIDTH, MENU_BUTTON_HEIGHT, OFF_WHITE
from controller.gui_elements import Button
from model.managers.adventurer_manager import AdventurerManager

class CharacterScreen:
    """Handles the character selection and confirmation screen."""
    def __init__(self, screen, fonts):
        self.screen = screen
        self.fonts = fonts

        self.adventurer_manager = AdventurerManager.get_instance()

        self.adventurer_buttons = {}
        self._initialize_adventurer_buttons()

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

    def _initialize_adventurer_buttons(self):
        """Dynamically create buttons for all adventurers."""
        adventurer_data = self.adventurer_manager.get_adventurer_data()
        positions = [
            (self.screen.get_width() / 4 - 100, self.screen.get_height() / 3),
            (3 * self.screen.get_width() / 4 - 100, self.screen.get_height() / 3),
            (self.screen.get_width() / 4 - 100, 2 * self.screen.get_height() / 3),
            (3 * self.screen.get_width() / 4 - 100, 2 * self.screen.get_height() / 3)
        ]

        for idx, (name, data) in enumerate(adventurer_data.items()):
            x, y = positions[idx % len(positions)]
            self.adventurer_buttons[name] = Button(
                DARK_GREY, x, y, MENU_BUTTON_WIDTH, MENU_BUTTON_HEIGHT, self.fonts["small"], OFF_WHITE, name.upper()
            )

    def draw(self):
        """Draw the character selection or confirmation screen."""
        self.screen.fill(DARK_GREY)

        if self.on_confirmation_screen and self.selected_character:
            char_name = self.fonts["large"].render(self.selected_character["name"], True, OFF_WHITE)
            char_type = self.fonts["small"].render(f"Class: {self.selected_character['type']}", True, OFF_WHITE)
            char_hp = self.fonts["small"].render(f"HP: {self.selected_character['max_HP']}", True, OFF_WHITE)
            char_attack_speed = self.fonts["small"].render(f"Attack Speed: {self.selected_character['attack_speed']}", True, OFF_WHITE)
            char_chance_to_hit = self.fonts["small"].render(f"Hit Chance: {self.selected_character['chance_to_hit'] * 100:.1f}%", True, OFF_WHITE)
            char_attack_damage = self.fonts["small"].render(
                f"Attack Damage: {self.selected_character['attack_damage_min']} - {self.selected_character['attack_damage_max']}",
                True, OFF_WHITE
            )
            char_chance_to_block = self.fonts["small"].render(f"Block Chance: {self.selected_character['chance_to_block'] * 100:.1f}%", True, OFF_WHITE)
            # char_special_attack = self.fonts["small"].render(f"Ability: {self.selected_character['special_attack']}", True, OFF_WHITE)

            char_image = pygame.image.load(self.selected_character["image"])
            char_image = pygame.transform.scale(char_image, (200, 200))
            self.screen.blit(char_image, (self.screen.get_width() / 2 - 300, 200))

            self.screen.blit(char_name, (self.screen.get_width() / 2 + 100, 50))
            self.screen.blit(char_type, (self.screen.get_width() / 2 + 100, 100))
            self.screen.blit(char_hp, (self.screen.get_width() / 2 + 100, 150))
            self.screen.blit(char_attack_speed, (self.screen.get_width() / 2 + 100, 200))
            self.screen.blit(char_chance_to_hit, (self.screen.get_width() / 2 + 100, 250))
            self.screen.blit(char_attack_damage, (self.screen.get_width() / 2 + 100, 300))
            self.screen.blit(char_chance_to_block, (self.screen.get_width() / 2 + 100, 350))
            # self.screen.blit(char_special_attack, (self.screen.get_width() / 2 + 100, 400))

            self.confirm_button.draw(self.screen)
            self.confirm_back_button.draw(self.screen)
        else:
            title = self.fonts["large"].render("CHOOSE ADVENTURER", True, LIGHT_BLUE)
            self.screen.blit(title, (self.screen.get_width() / 2 - title.get_width() / 2,
                                     self.screen.get_height() / 6 - title.get_height() / 2))

            for button in self.adventurer_buttons.values():
                button.draw(self.screen)

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
                for name, button in self.adventurer_buttons.items():
                    if button.is_hovered((mouse_x, mouse_y)):
                        raw_data = self.adventurer_manager.get_adventurer_data(name)
                        print(f"raw_data for {name}: {raw_data}")
                        self.selected_character = {
                            "name": name,
                            "type": raw_data[2],
                            "max_HP": raw_data[3],
                            "attack_speed": raw_data[4],
                            "chance_to_hit": raw_data[5],
                            "attack_damage_min": raw_data[6],
                            "attack_damage_max": raw_data[7],
                            "chance_to_block": raw_data[8],
                            # "special_attack": raw_data[9],
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
                    return data
                elif action == "back":
                    return None

            self.draw()
            pygame.display.flip()