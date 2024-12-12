import math
import time

import pygame
from constants import DARK_GREY, BACKGROUND_COLOR, MENU_BUTTON_WIDTH, MENU_BUTTON_HEIGHT, LIGHT_BLUE, OFF_WHITE, \
    SCREEN_WIDTH, SCREEN_HEIGHT, DARK_RED, RED, BROWN, GOLD, VIOLET, DARK_VIOLET, MEDIUM_GREY, FADED_GRAY
from src.view.gui_elements import Button


class MainScreen:
    """Represents the main menu and manual."""

    def __init__(self, screen, fonts):
        """
        Constructor, instantiates fields.

        :param screen: The pygame Surface on which to draw things.
        :param fonts: The fonts.
        """
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
        self.manual_menu_button = Button(DARK_GREY, 75, 75, 650, 450)

    def run(self):
        """
        Handles the main menu loop/state transitions from it.

        :return: A string representing the new state.
        """
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
                                 self.screen.get_height() / 3 - title.get_height() / 2 + math.sin(time.time() * 6)*7))
        self.new_game_button.draw(self.screen, True)
        self.load_game_button.draw(self.screen, True)
        self.manual_button.draw(self.screen, True)

    def show_manual(self):
        """Handles the manual screen."""
        manual_running = True
        exit_button = pygame.Rect(680, 75, 45, 45)

        # There is a better way to do this, but I can't be bothered.
        # Manual text
        manual_body = self.fonts["small"].render("Navigate through four floors of a dungeon and gather all",
                                                 True, OFF_WHITE)
        manual_body2 = self.fonts["small"].render("four pillars of O.O. to beat the game. Any room may",
                                                  True, OFF_WHITE)
        manual_body3 = self.fonts["small"].render("have a monster, a formidable elite monster, an item to",
                                                  True, OFF_WHITE)
        manual_body4 = self.fonts["small"].render("help you on your journey, a trap, or one of the pillars.",
                                                  True, OFF_WHITE)
        manual_body5 = self.fonts["small"].render("Only one pillar is present per floor. You must grab the",
                                                  True, OFF_WHITE)
        manual_body6 = self.fonts["small"].render("pillar before proceeding to the next floor.", True, OFF_WHITE)
        manual_text = self.fonts["large"].render("MANUAL", True, LIGHT_BLUE)
        key_text = self.fonts["medium"].render("Map Color Key:", True, LIGHT_BLUE)

        # Minimap key rects
        monster_rect = pygame.Rect(125, 400, 35, 35)
        elite_rect = pygame.Rect(270, 400, 35, 35)
        item_rect = pygame.Rect(415, 400, 35, 35)
        trap_rect = pygame.Rect(560, 400, 35, 35)
        pillar_rect = pygame.Rect(125, 450, 35, 35)
        empty_rect = pygame.Rect(270, 450, 35, 35)
        entrance_rect = pygame.Rect(415, 450, 35, 35)
        exit_rect = pygame.Rect(560, 450, 35, 35)

        # Minimap key texts
        monster_text = self.fonts["small"].render("Monster", True, OFF_WHITE)
        elite_text = self.fonts["small"].render("Elite", True, OFF_WHITE)
        item_text = self.fonts["small"].render("Item", True, OFF_WHITE)
        trap_text = self.fonts["small"].render("Trap", True, OFF_WHITE)
        pillar_text = self.fonts["small"].render("Pillar", True, OFF_WHITE)
        empty_text = self.fonts["small"].render("Empty", True, OFF_WHITE)
        entrance_text = self.fonts["small"].render("Entrance", True, OFF_WHITE)
        exit_text = self.fonts["small"].render("Exit", True, OFF_WHITE)

        # Manual loop
        while manual_running:
            clicked = False
            mouse_pos = pygame.mouse.get_pos()

            self.manual_menu_button.draw(self.screen, True)
            pygame.draw.rect(self.screen, OFF_WHITE, exit_button)
            exit_button_text = self.fonts["medium"].render("X", True, DARK_GREY)
            exit_text_rect = exit_button_text.get_rect(center=exit_button.center)
            self.screen.blit(exit_button_text, exit_text_rect)

            pygame.draw.rect(self.screen, DARK_RED, elite_rect)
            pygame.draw.rect(self.screen, RED, monster_rect)
            pygame.draw.rect(self.screen, BROWN, trap_rect)
            pygame.draw.rect(self.screen, GOLD, item_rect)
            pygame.draw.rect(self.screen, FADED_GRAY, pillar_rect)
            pygame.draw.rect(self.screen, MEDIUM_GREY, empty_rect)
            pygame.draw.rect(self.screen, VIOLET, entrance_rect)
            pygame.draw.rect(self.screen, DARK_VIOLET, exit_rect)

            '''Each text drawn 145 pixels to the right of the previous.
            Second row drawn 50 pixels below first'''
            self.screen.blit(monster_text, (165, 400 + elite_text.get_height() / 2 - 3))
            self.screen.blit(elite_text, (310, 400 + elite_text.get_height() / 2 - 3))
            self.screen.blit(item_text, (455, 400 + elite_text.get_height() / 2 - 3))
            self.screen.blit(trap_text, (600, 400 + elite_text.get_height() / 2 - 3))
            self.screen.blit(pillar_text, (165, 450 + elite_text.get_height() / 2 - 3))
            self.screen.blit(empty_text, (310, 450 + elite_text.get_height() / 2 - 3))
            self.screen.blit(entrance_text, (455, 450 + elite_text.get_height() / 2 - 3))
            self.screen.blit(exit_text, (600, 450 + elite_text.get_height() / 2 - 3))

            self.screen.blit(manual_text, (SCREEN_WIDTH / 2 - manual_text.get_width() / 2,
                                           SCREEN_HEIGHT / 5 - manual_text.get_height() / 2))
            self.screen.blit(key_text, (SCREEN_WIDTH / 2 - manual_text.get_width() / 2,
                                           SCREEN_HEIGHT * 9 / 15 - 10))

            '''First line is drawn 50 pixels below 'MANUAL' title. Others are drawn 32 pixels below each
            preceding line. Hence the adding of 50, 82, 114, 146, 178, 210 to the heights each time'''
            self.screen.blit(manual_body, (SCREEN_WIDTH / 2 - manual_body.get_width() / 2,
                                           SCREEN_HEIGHT / 5 - manual_body.get_height() / 2 + 50))
            self.screen.blit(manual_body2, (SCREEN_WIDTH / 2 - manual_body.get_width() / 2,
                                            SCREEN_HEIGHT / 5 - manual_body.get_height() / 2 + 82))
            self.screen.blit(manual_body3, (SCREEN_WIDTH / 2 - manual_body.get_width() / 2,
                                            SCREEN_HEIGHT / 5 - manual_body.get_height() / 2 + 114))
            self.screen.blit(manual_body4, (SCREEN_WIDTH / 2 - manual_body.get_width() / 2,
                                            SCREEN_HEIGHT / 5 - manual_body.get_height() / 2 + 146))
            self.screen.blit(manual_body5, (SCREEN_WIDTH / 2 - manual_body.get_width() / 2,
                                            SCREEN_HEIGHT / 5 - manual_body.get_height() / 2 + 178))
            self.screen.blit(manual_body6, (SCREEN_WIDTH / 2 - manual_body.get_width() / 2,
                                            SCREEN_HEIGHT / 5 - manual_body.get_height() / 2 + 210))
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # left click
                    clicked = True
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            if clicked and exit_button.collidepoint(mouse_pos):
                manual_running = False

            pygame.display.flip()
