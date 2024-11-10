import sys
import pygame

class Button:
    def __init__(self, color, x, y, width, height, font, text_color, text=''):
        """Constructor, instantiates fields"""
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.font = font
        self.text_color = text_color
        self.text = text

    def draw(self, window, outline=None):
        """Draws button on screen"""
        if outline:
            pygame.draw.rect(window, outline, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)

        pygame.draw.rect(window, self.color, (self.x, self.y, self.width, self.height), 0)
        if self.text != '': # If button has text, draw it!
            text = self.font.render(self.text, True, self.text_color)
            window.blit(text, (self.x + (self.width / 2 - text.get_width() / 2),
                               self.y + (self.height / 2 - text.get_height() / 2)))

    def is_hovered(self, mouse_pos):
        """Returns true if cursor is currently over button, false otherwise."""
        if self.x < mouse_pos[0] < self.x + self.width:
            if self.y < mouse_pos[1] < self.y + self.height:
                return True
        return False

def main():
    # initialize the pygame
    pygame.init()

    # some constants:
    dark_grey = (60, 60, 60)
    pastel_red = (250, 145, 147)
    light_blue = (85, 176, 230)
    off_white = (226, 226, 226)
    background_grey = (24, 24, 24)
    menu_button_width = 140
    menu_button_height = 40

    # create the screen
    screen = pygame.display.set_mode((800, 600))

    # Title and Icon
    pygame.display.set_caption("Dungeon Adventure")
    dungeon_icon = pygame.image.load('assets/images/dice.png')
    pygame.display.set_icon(dungeon_icon)

    # Loading default pygame font, display splash screen
    font = pygame.font.Font(None, size=85)
    font_small = pygame.font.Font(None, size=30)
    font_medium = pygame.font.Font(None, size=50)
    splash_message = font.render("TEAM 5", True, pastel_red)
    screen.blit(splash_message, (screen.get_width()/2 - splash_message.get_width()/2,
                                      screen.get_height()/2 - splash_message.get_height()/2))
    pygame.display.update()
    pygame.time.delay(1000)
    new_game_button = Button(dark_grey, screen.get_width() / 2 - 70, 2 * screen.get_height() / 3,
                             menu_button_width, menu_button_height, font_small, off_white, 'NEW GAME')
    load_game_button = Button(dark_grey, screen.get_width() / 2 - 70 - 165, 2 * screen.get_height() / 3,
                              menu_button_width, menu_button_height, font_small, off_white, 'LOAD GAME')
    manual_button = Button(dark_grey, screen.get_width() / 2 - 70 + 165, 2 * screen.get_height() / 3,
                              menu_button_width, menu_button_height, font_small, off_white, 'MANUAL')
    manual_large_text = font.render("MANUAL", True, off_white)
    title = font.render("DUNGEON ADVENTURE", True, light_blue)
    char_select = font.render("CHOOSE ADVENTURER", True, light_blue)
    exit_submenu = font_medium.render("X", True, dark_grey)
    # Text for adventurer select
    noah_text = font_small.render("NOAH", True, off_white)
    jayne_text = font_small.render("JAYNE", True, off_white)
    sean_text = font_small.render("SEAN", True, off_white)
    mark_text = font_small.render("MARK", True, off_white)
    exit_submenu_rect = exit_submenu.get_rect()
    main_menu = True

    while main_menu:
        clicked = False
        mouse_pos = pygame.mouse.get_pos()
        screen.fill(background_grey)
        # display title
        screen.blit(title, (screen.get_width() / 2 - title.get_width() / 2,
                            screen.get_height() / 3 - title.get_height() / 2))
        new_game_button.draw(screen)
        load_game_button.draw(screen)
        manual_button.draw(screen)
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: # left click
                clicked = True
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if clicked:
                if new_game_button.is_hovered(mouse_pos):
                    print('new game button pushed')
                    main_menu = False
                    clicked = False
                elif load_game_button.is_hovered(mouse_pos):
                    print('load game button pushed')
                elif manual_button.is_hovered(mouse_pos):
                    print('manual button pushed')
                    in_manual = True
                    while in_manual:
                        clicked = False
                        # TODO: Move logic out into methods to avoid duplicated stuff like this
                        mouse_x2, mouse_y2 = pygame.mouse.get_pos()
                        manual_menu = pygame.Rect(75, 75, 625, 425)
                        # TODO: make some constants to reduce function calls
                        manual_menu.center = (screen.get_width() / 2, screen.get_height() / 2)
                        manual_exit = pygame.Rect(668, 88, 45, 45)
                        pygame.draw.rect(screen, dark_grey, manual_menu)
                        pygame.draw.rect(screen, off_white, manual_exit)
                        exit_submenu_rect.center = manual_exit.center
                        exit_submenu_button_area = screen.blit(exit_submenu, exit_submenu_rect)
                        screen.blit(manual_large_text, (screen.get_width() / 2 - manual_large_text.get_width() / 2,
                                            screen.get_height() / 5 - manual_large_text.get_height() / 2))
                        for event2 in pygame.event.get():
                            if event2.type == pygame.MOUSEBUTTONDOWN and event2.button == 1:  # left click
                                clicked = True
                            if event2.type == pygame.QUIT:
                                pygame.quit()
                                sys.exit()
                            if clicked and exit_submenu_button_area.collidepoint(mouse_x2, mouse_y2):
                                in_manual = False
                        pygame.display.flip()
        pygame.display.flip()

    # New game button pressed: enter main loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: # left click
                clicked = True
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Clear the screen and display "CHOOSE ADVENTURER"
        screen.fill(dark_grey)
        screen.blit(char_select, (screen.get_width() / 2 - char_select.get_width() / 2,
                            screen.get_height() / 6 - char_select.get_height() / 2))
        # TODO: Add buttons/portraits for each adventurer.
        noah_button = pygame.Rect(screen.get_width() / 4 - 70, screen.get_height() / 3, menu_button_width, menu_button_height)
        jayne_button = pygame.Rect(3 * screen.get_width() / 4 - 70, screen.get_height() / 3, menu_button_width, menu_button_height)
        sean_button = pygame.Rect(screen.get_width() / 4 - 70, 2 * screen.get_height() / 3, menu_button_width, menu_button_height)
        mark_button = pygame.Rect(3 * screen.get_width() / 4 - 70, 2 * screen.get_height() / 3, menu_button_width, menu_button_height)

        pygame.draw.rect(screen, dark_grey, noah_button)
        pygame.draw.rect(screen, dark_grey, jayne_button)
        pygame.draw.rect(screen, dark_grey, sean_button)
        pygame.draw.rect(screen, dark_grey, mark_button)

        noah_rect = noah_text.get_rect(center=noah_button.center)
        jayne_rect = jayne_text.get_rect(center=jayne_button.center)
        sean_rect = sean_text.get_rect(center=sean_button.center)
        mark_rect = sean_text.get_rect(center=mark_button.center)

        screen.blit(noah_text, noah_rect)
        screen.blit(jayne_text, jayne_rect)
        screen.blit(sean_text, sean_rect)
        screen.blit(mark_text, mark_rect)

        if clicked:
            mouse_x, mouse_y = pygame.mouse.get_pos()

            if noah_button.collidepoint(mouse_x, mouse_y):
                print("Noah selected")
                #TODO Implement character selection logic
            elif jayne_button.collidepoint(mouse_x, mouse_y):
                print("Jayne selected")
                #TODO Implement character selection logic
            elif sean_button.collidepoint(mouse_x, mouse_y):
                print("Sean selected")
                # TODO Implement character selection logic
            else:
                print("Mark selected")
                #TODO Implement character selection logic
            clicked = False

        pygame.display.flip()
# TODO: Make separate button class to make things easier.

if __name__ == '__main__':
    main()