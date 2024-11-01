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

def player():
    screen.blit(playerImg, (playerX, playerY))

#Game loop
running = True
while running:

    #background color for the Gui
    screen.fill((255, 255, 255))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    player()
    pygame.display.update()