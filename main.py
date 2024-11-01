import pygame

#initialize the pygame
pygame.init()

#create the screen
screen = pygame.display.set_mode((800, 600))

#Title and Icon
pygame.display.set_caption("Dungeon Adventure")
dungeon_icon = pygame.image.load('dice.png')
pygame.display.set_icon(dungeon_icon)

#Player
playerImg = pygame.image.load('hero.png')
playerImg = pygame.transform.scale(playerImg, (50, 50))
playerX = 370
playerY = 480
playerX_change = 0
playerY_change = 0

#method for displaying the player/hero
def player(theX, theY):
    screen.blit(playerImg, (theX, theY))

#Game loop
running = True
while running:

    #background color for the Gui
    screen.fill((255, 255, 255))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if keystroke is pressed check whether its right or left
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_LEFT:
                playerX_change = -0.2
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.2
            if event.key == pygame.K_UP:
                print("Up key is pressed")
                playerY_change = -0.2
            if event.key == pygame.K_DOWN:
                print("Down arrow is pressed")
                playerY_change = 0.2

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                playerX_change = 0
                playerY_change = 0

    playerX += playerX_change
    playerY += playerY_change
    player(playerX, playerY)
    pygame.display.update()