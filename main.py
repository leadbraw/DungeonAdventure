import sys
import pygame
import controller.database_init
from model.managers.room_manager import RoomManager
from model.managers.monster_manager import MonsterManager
from model.managers.item_manager import ItemManager
import model.dungeon.Dungeon
class Button:
    """Self-explanatory. Used to represent clickable buttons on screen."""
    def __init__(self, color, x, y, width, height, font=None, text_color=None, text=''):
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
class CharacterScreen:
    """Represents the state of the character screen (not the character select screen)."""
    def __init__(self, window, chosen_font, hero_name, hero_stats, hero_abilities, hero_image):
        """Constructor. Instantiates fields"""
        self.screen = window
        self.font = chosen_font
        self.hero_name = hero_name
        self.hero_stats = hero_stats
        self.hero_abilities = hero_abilities
        self.hero_image = pygame.image.load(hero_image)
        self.hero_image = pygame.transform.scale(self.hero_image, (400, 400))
        #Buttons for 'Select' and 'Back'
        button_font = pygame.font.Font(None, 30)
        self.select_button = Button((60, 180, 75), 550, 500, 100, 40,
                                    button_font, (255, 255, 255), "Select")
        self.back_button = Button((180, 60, 60), 670, 500, 100, 40,
                                  button_font, (255, 255, 255), "Back")

    def draw(self):
        """Responsible for drawing the character screen, complete with name, image, stats."""
        # Clear screen with a darker background
        self.screen.fill(dark_grey)

        # Display hero image on the right
        image_rect = self.hero_image.get_rect(center=(550, 250))
        self.screen.blit(self.hero_image, image_rect)

        #Display hero name at the top left
        name_text = self.font.render(self.hero_name, True, (255, 255, 255))
        self.screen.blit(name_text, (50, 50))
        stats_text = self.font.render("Stats: " + self.hero_stats, True, (200, 200, 200))
        self.screen.blit(stats_text, (50, 100))
        abilities_text = self.font.render("Abilities: " + self.hero_abilities, True, (200, 200, 200))
        self.screen.blit(abilities_text, (50, 150))

        # Draw "Select" and "Back" buttons
        self.select_button.draw(self.screen)
        self.back_button.draw(self.screen)

    def handle_event(self, event):
        """Handles button clicks for select and back buttons"""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            if self.select_button.is_hovered(mouse_pos):
                print(f"{self.hero_name} selected")
                return "select"
            elif self.back_button.is_hovered(mouse_pos):
                print("Returning to character selection.")
                return "back"
        return None
def main():
    """Displays splash screen, calls main_menu()"""
    # Display splash screen
    splash_message = font.render("TEAM 5", True, pastel_red)
    screen.blit(splash_message, (screen.get_width()/2 - splash_message.get_width()/2,
                                      screen.get_height()/2 - splash_message.get_height()/2))
    pygame.display.update()
    pygame.time.delay(1000)
    main_menu()
def main_menu():
    """Handles the main menu (and manual)"""
    new_game_button = Button(dark_grey, screen.get_width() / 2 - 70, 2 * screen.get_height() / 3,
                             menu_button_width, menu_button_height, font_small, off_white, 'NEW GAME')
    load_game_button = Button(dark_grey, screen.get_width() / 2 - 70 - 165, 2 * screen.get_height() / 3,
                              menu_button_width, menu_button_height, font_small, off_white, 'LOAD GAME')
    manual_button = Button(dark_grey, screen.get_width() / 2 - 70 + 165, 2 * screen.get_height() / 3,
                           menu_button_width, menu_button_height, font_small, off_white, 'MANUAL')

    manual_menu = Button(dark_grey, 75, 75, 625, 425)
    manual_large_text = font.render("MANUAL", True, off_white)
    title = font.render("DUNGEON ADVENTURE", True, light_blue)
    exit_submenu = font_medium.render("X", True, dark_grey)
    exit_submenu_rect = exit_submenu.get_rect()
    while True:
        clicked = False
        mouse_pos = pygame.mouse.get_pos()
        screen.fill(background_grey)
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # left click
                clicked = True
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        screen.blit(title, (screen.get_width() / 2 - title.get_width() / 2,
                            screen.get_height() / 3 - title.get_height() / 2))
        new_game_button.draw(screen)
        load_game_button.draw(screen)
        manual_button.draw(screen)
        if clicked:
            if new_game_button.is_hovered(mouse_pos):
                print('new game button pushed')
                character_select()
            elif load_game_button.is_hovered(mouse_pos):
                print('load game button pushed')
                # TODO: Load game functionality.
            elif manual_button.is_hovered(mouse_pos):
                print('manual button pushed')
                in_manual = True
                while in_manual:
                    clicked = False
                    # TODO: Move logic out into methods to avoid duplicated stuff like this
                    mouse_pos = pygame.mouse.get_pos()
                    manual_menu.draw(screen)
                    # TODO: Make some constants to reduce function calls
                    # TODO: Make exit button a Button proper
                    manual_exit = pygame.Rect(655, 75, 45, 45)
                    pygame.draw.rect(screen, off_white, manual_exit)
                    exit_submenu_rect.center = manual_exit.center
                    exit_submenu_button_area = screen.blit(exit_submenu, exit_submenu_rect)
                    screen.blit(manual_large_text, (screen.get_width() / 2 - manual_large_text.get_width() / 2,
                                                    screen.get_height() / 5 - manual_large_text.get_height() / 2))
                    for event in pygame.event.get():
                        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # left click
                            clicked = True
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                        if clicked and exit_submenu_button_area.collidepoint(mouse_pos):
                            in_manual = False
                    pygame.display.flip()
        pygame.display.flip()
def character_select():
    """Handles the character select logic. User chooses a character, then must confirm their choice."""
    noah_button = Button(dark_grey, screen.get_width() / 4 - 70, screen.get_height() / 3, menu_button_width,
                         menu_button_height, font_small, off_white, 'NOAH')
    jayne_button = Button(dark_grey, 3 * screen.get_width() / 4 - 70, screen.get_height() / 3, menu_button_width,
                          menu_button_height, font_small, off_white, 'JAYNE')
    sean_button = Button(dark_grey, screen.get_width() / 4 - 70, 2 * screen.get_height() / 3, menu_button_width,
                         menu_button_height, font_small, off_white, 'SEAN')
    mark_button = Button(dark_grey, 3 * screen.get_width() / 4 - 70, 2 * screen.get_height() / 3, menu_button_width,
                         menu_button_height, font_small, off_white, 'MARK')

    # Store the character screen instance if a hero is selected
    on_character_screen = False
    character_screen = None
    while True:
        clicked = False
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # left click
                clicked = True
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # Handle character screen events
            if on_character_screen and character_screen:
                action = character_screen.handle_event(event)
                if action == "back":
                    on_character_screen = False
                elif action == "select":
                    print(f"{character_screen.hero_name} has been selected!")
                    gameplay(character_screen.hero_name)
        # Clear the screen and display "CHOOSE ADVENTURER"
        screen.fill(dark_grey)
        # Display the appropriate screen
        if on_character_screen and character_screen:
            character_screen.draw()
        else:
            char_select = font.render("CHOOSE ADVENTURER", True, light_blue)
            screen.blit(char_select, (screen.get_width() / 2 - char_select.get_width() / 2,
                                      screen.get_height() / 6 - char_select.get_height() / 2))
            # Draw adventurer selection buttons
            noah_button.draw(screen)
            jayne_button.draw(screen)
            sean_button.draw(screen)
            mark_button.draw(screen)
            # Handle button clicks for each character
            if clicked:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if noah_button.is_hovered((mouse_x, mouse_y)):
                    character_screen = CharacterScreen(screen, font_small, "Noah",
                                                       "HP: 75, MP: 50", "Heal",
                                                       "assets/images/noah.png")
                    on_character_screen = True
                elif jayne_button.is_hovered((mouse_x, mouse_y)):
                    character_screen = CharacterScreen(screen, font_small, "Jayne",
                                                       "HP: 75, MP: 60", "Surprise Attack",
                                                       "assets/images/jayne.png")
                    on_character_screen = True
                elif sean_button.is_hovered((mouse_x, mouse_y)):
                    character_screen = CharacterScreen(screen, font_small, "Sean",
                                                       "HP: 90, MP: 40", "Music",
                                                       "assets/images/sean.png")
                    on_character_screen = True
                elif mark_button.is_hovered((mouse_x, mouse_y)):
                    character_screen = CharacterScreen(screen, font_small, "Mark",
                                                       "HP: 125, MP: 30", "Crushing Blow",
                                                       "assets/images/mark.png")
                    on_character_screen = True
        pygame.display.flip()
def gameplay(hero_name):
    """Handles the main gameplay loop."""
    controller.database_init.main() # Make database.

    room_manager = RoomManager.get_instance()
    monster_manager = MonsterManager.get_instance()
    item_manager = ItemManager.get_instance()

    #create dungeon
    dungeon = model.Dungeon(floor_number=1)
    print(dungeon)

    #populate monsters and items
    all_rooms = []
    for row in dungeon.map:
        for room in row:
            all_rooms.append(room)

    #filter monster rooms
    monster_rooms = []
    for room in all_rooms:
        if room.type == 'MONSTER':
            monster_rooms.append(room)

    #filter item rooms
    item_rooms = []
    for room in all_rooms:
        if room.type == 'ITEM':
            item_rooms.append(room)

    # place monsters in rooms
    for room in monster_rooms:
        monster = monster_manager.get_random_monster()
        print(f"Placed {monster.get_name()} in a MONSTER room.")
    for room in item_rooms:
        item = item_manager.get_random_non_unique_item()
        print(f"Placed {item.get_name()} in a ITEM room.")

    # the adventurer's intial position
    position = None
    for row_index, row in enumerate(dungeon.map):
        for column_index, room in enumerate(row):
            if room.type == 'ENTRANCE':
                position = (row_index, column_index)
                break
        if position:
            break

    while True:
        '''The space not drawn over by the two dark rectangles along the bottom/right is where the dungeon images
        and prompts to move from room to room will be shown.'''
        screen.fill(dark_grey)
        bottom_rect = pygame.Rect(0, 450, 800, 150)
        right_rect = pygame.Rect(650, 0, 150, 450)
        pygame.draw.rect(screen, background_grey, bottom_rect)
        pygame.draw.rect(screen, background_grey, right_rect)
        match hero_name: # Grab the proper portrait for the selected hero
            case "Noah":
                portrait = pygame.image.load("assets/images/noah_portrait.png").convert_alpha()
            case "Sean":
                portrait = pygame.image.load("assets/images/sean_portrait.png").convert_alpha()
            case "Jayne":
                portrait = pygame.image.load("assets/images/jayne_portrait.png").convert_alpha()
            case "Mark":
                portrait = pygame.image.load("assets/images/mark_portrait.png").convert_alpha()
            case _: # fallback
                portrait = pygame.image.load("assets/images/hero.png").convert_alpha()
        portrait = pygame.transform.scale(portrait, (150, 150)) # Scale to fit in bottom right
        screen.blit(portrait, (650, 450))
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # left click
                clicked = True
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.flip()

# ENTRY POINT IS HERE.
# initialize the pygame
pygame.init()

# constants
dark_grey = (60, 60, 60)
pastel_red = (250, 145, 147)
light_blue = (85, 176, 230)
off_white = (226, 226, 226)
background_grey = (24, 24, 24)
menu_button_width = 140
menu_button_height = 40
font = pygame.font.Font(None, size=85)
font_small = pygame.font.Font(None, size=30)
font_medium = pygame.font.Font(None, size=50)

# create the screen
screen = pygame.display.set_mode((800, 600))

# Title and Icon
pygame.display.set_caption("Dungeon Adventure")
dungeon_icon = pygame.image.load('assets/images/dice.png')
pygame.display.set_icon(dungeon_icon)
main()