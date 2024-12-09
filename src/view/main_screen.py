import pygame
from constants import DARK_GREY, BACKGROUND_COLOR, MENU_BUTTON_WIDTH, MENU_BUTTON_HEIGHT, LIGHT_BLUE, OFF_WHITE
from src.view.gui_elements import Button


class MainScreen:
    def __init__(self, screen, fonts):
        self.screen = screen
        self.fonts = fonts  # Dictionary of fonts passed from main
        self.new_game_button = Button(
            DARK_GREY, screen.get_width() / 2 - 70, 2 * screen.get_height() / 3,
            MENU_BUTTON_WIDTH, MENU_BUTTON_HEIGHT, self.fonts["small"], OFF_WHITE, 'NEW GAME'
        )
        self.load_game_button = Button(
            DARK_GREY, screen.get_width() / 2 - 70 - 165, 2 * screen.get_height() / 3,
            MENU_BUTTON_WIDTH, MENU_BUTTON_HEIGHT, self.fonts["small"], OFF_WHITE, 'LOAD GAME'
        )
        self.manual_button = Button(
            DARK_GREY, screen.get_width() / 2 - 70 + 165, 2 * screen.get_height() / 3,
            MENU_BUTTON_WIDTH, MENU_BUTTON_HEIGHT, self.fonts["small"], OFF_WHITE, 'MANUAL'
        )
        self.manual_menu_button = Button(DARK_GREY, 75, 75, 625, 425)

    def run(self):
        """Handles the main menu loop."""
        running = True
        while running:
            clicked = False
            mouse_pos = pygame.mouse.get_pos()
            self.screen.fill(BACKGROUND_COLOR)

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # left click
                    clicked = True
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            self.draw_main_menu()

            if clicked:
                if self.new_game_button.is_hovered(mouse_pos):
                    print("New Game button clicked!")
                    return "new_game"
                elif self.load_game_button.is_hovered(mouse_pos):
                    print("Load Game button clicked!")
                    return "load_game"
                elif self.manual_button.is_hovered(mouse_pos):
                    print("Manual button clicked!")
                    self.show_manual()

            pygame.display.flip()

    def draw_main_menu(self):
        """Draws the main menu buttons and title."""
        title = self.fonts["large"].render("DUNGEON ADVENTURE", True, LIGHT_BLUE)
        self.screen.blit(title, (self.screen.get_width() / 2 - title.get_width() / 2,
                                 self.screen.get_height() / 3 - title.get_height() / 2))
        self.new_game_button.draw(self.screen)
        self.load_game_button.draw(self.screen)
        self.manual_button.draw(self.screen)

    def show_manual(self):
        """Handles the manual screen."""
        manual_running = True
        exit_button = pygame.Rect(655, 75, 45, 45)
        # There is a better way to do this, but I can't be bothered.
        manual_body = self.fonts["small"].render("Navigate through four floors of a dungeon and gather",
                                                 True, OFF_WHITE)
        manual_body2 = self.fonts["small"].render("all four pillars of O.O. to beat the game. Any room",
                                                  True, OFF_WHITE)
        manual_body3 = self.fonts["small"].render("could have a monster, a formidable elite monster, an",
                                                  True, OFF_WHITE)
        manual_body4 = self.fonts["small"].render("item to help you on your journey, a trap, or the pillar.",
                                                  True, OFF_WHITE)
        manual_body5 = self.fonts["small"].render("Only one pillar is present per floor. You must grab",
                                                  True, OFF_WHITE)
        manual_body6 = self.fonts["small"].render("the pillar before proceeding to the next floor.", True, OFF_WHITE)
        while manual_running:
            clicked = False
            mouse_pos = pygame.mouse.get_pos()

            self.manual_menu_button.draw(self.screen)
            pygame.draw.rect(self.screen, OFF_WHITE, exit_button)
            exit_text = self.fonts["medium"].render("X", True, DARK_GREY)
            exit_text_rect = exit_text.get_rect(center=exit_button.center)
            self.screen.blit(exit_text, exit_text_rect)

            manual_text = self.fonts["large"].render("MANUAL", True, OFF_WHITE)
            self.screen.blit(manual_text, (self.screen.get_width() / 2 - manual_text.get_width() / 2,
                                           self.screen.get_height() / 5 - manual_text.get_height() / 2))
            '''First line is drawn 50 pixels below 'MANUAL' title. Others are drawn 32 pixels below each
            preceding line. Hence the adding of 50, 82, 114, 146, 178, 210 to the heights each time'''
            self.screen.blit(manual_body, (self.screen.get_width() / 2 - manual_body.get_width() / 2,
                                           self.screen.get_height() / 5 - manual_body.get_height() / 2 + 50))
            self.screen.blit(manual_body2, (self.screen.get_width() / 2 - manual_body.get_width() / 2,
                                            self.screen.get_height() / 5 - manual_body.get_height() / 2 + 82))
            self.screen.blit(manual_body3, (self.screen.get_width() / 2 - manual_body.get_width() / 2,
                                            self.screen.get_height() / 5 - manual_body.get_height() / 2 + 114))
            self.screen.blit(manual_body4, (self.screen.get_width() / 2 - manual_body.get_width() / 2,
                                            self.screen.get_height() / 5 - manual_body.get_height() / 2 + 146))
            self.screen.blit(manual_body5, (self.screen.get_width() / 2 - manual_body.get_width() / 2,
                                            self.screen.get_height() / 5 - manual_body.get_height() / 2 + 178))
            self.screen.blit(manual_body6, (self.screen.get_width() / 2 - manual_body.get_width() / 2,
                                            self.screen.get_height() / 5 - manual_body.get_height() / 2 + 210))
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # left click
                    clicked = True
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            if clicked and exit_button.collidepoint(mouse_pos):
                manual_running = False

            pygame.display.flip()
