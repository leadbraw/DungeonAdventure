import sys
import pygame

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
dungeon_icon = pygame.image.load('dice.png')
pygame.display.set_icon(dungeon_icon)

# Loading default pygame font, display splash screen
font = pygame.font.Font(None, size=85)
font_small = pygame.font.Font(None, size=30)
splash_message = font.render("TEAM 5", True, pastel_red)
screen.blit(splash_message, (screen.get_width()/2 - splash_message.get_width()/2,
                                  screen.get_height()/2 - splash_message.get_height()/2))
pygame.display.update()
pygame.time.delay(1000)
new_game_text = font_small.render("NEW GAME", True, off_white)
load_game_text = font_small.render("LOAD GAME", True, off_white)
manual_text = font_small.render("MANUAL", True, off_white)
title = font.render("DUNGEON ADVENTURE", True, light_blue)
main_menu = True
while main_menu:
    clicked = False
    mouse_x, mouse_y = pygame.mouse.get_pos()
    screen.fill(background_grey)
    # display title
    screen.blit(title, (screen.get_width() / 2 - title.get_width() / 2,
                        screen.get_height() / 3 - title.get_height() / 2))
    # draw buttons, center text within them
    new_game_rect = new_game_text.get_rect()
    load_game_rect = load_game_text.get_rect()
    manual_rect = manual_text.get_rect()
    new_game_button = pygame.Rect(screen.get_width() / 2 - 70, 2 * screen.get_height() / 3,
                                  menu_button_width, menu_button_height)
    load_game_button = pygame.Rect(screen.get_width() / 2 - 70 - 165, 2 * screen.get_height() / 3,
                                  menu_button_width, menu_button_height)
    manual_button = pygame.Rect(screen.get_width() / 2 - 70 + 165, 2 * screen.get_height() / 3,
                                  menu_button_width, menu_button_height)
    pygame.draw.rect(screen, dark_grey, new_game_button)
    pygame.draw.rect(screen, dark_grey, load_game_button)
    pygame.draw.rect(screen, dark_grey, manual_button)
    new_game_rect.center = new_game_button.center
    new_game_button_area = screen.blit(new_game_text, new_game_rect)
    load_game_rect.center = load_game_button.center
    load_game_button_area = screen.blit(load_game_text, load_game_rect)
    manual_rect.center = manual_button.center
    manual_button_area = screen.blit(manual_text, manual_rect)
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: # left click
            clicked = True
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if clicked:
            if new_game_button_area.collidepoint(mouse_x, mouse_y):
                print('new game button pushed')
            elif load_game_button_area.collidepoint(mouse_x, mouse_y):
                print('load game button pushed')
            elif manual_button_area.collidepoint(mouse_x, mouse_y):
                print('manual button pushed')
    pygame.display.update()
    # TODO: Start on the main game loop.

# #Player
# playerImg = pygame.image.load('hero.png')
# playerImg = pygame.transform.scale(playerImg, (50, 50))
# playerX = 370
# playerY = 480
# playerX_change = 0
# playerY_change = 0
#
# #method for displaying the player/hero
# def player(theX, theY):
#     screen.blit(playerImg, (theX, theY))
#
# #Game loop
# running = True
# while running:
#
#     #background color for the Gui
#     screen.fill((255, 255, 255))
#
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False
#
#         # if keystroke is pressed check whether its right or left
#         if event.type == pygame.KEYDOWN:
#
#             if event.key == pygame.K_LEFT:
#                 playerX_change = -0.2
#             if event.key == pygame.K_RIGHT:
#                 playerX_change = 0.2
#             if event.key == pygame.K_UP:
#                 print("Up key is pressed")
#                 playerY_change = -0.2
#             if event.key == pygame.K_DOWN:
#                 print("Down arrow is pressed")
#                 playerY_change = 0.2
#
#         if event.type == pygame.KEYUP:
#             if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_UP or event.key == pygame.K_DOWN:
#                 playerX_change = 0
#                 playerY_change = 0
#
#     playerX += playerX_change
#     playerY += playerY_change
#     player(playerX, playerY)
#     pygame.display.update()