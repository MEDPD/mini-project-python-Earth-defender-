import pygame
import random
# initialize the game

pygame.init()

# create the game screen

screen = pygame.display.set_mode((800, 600))

#! title and icon

pygame.display.set_caption('Earth defender')
icon = pygame.image.load('./img/spaceship.png')

pygame.display.set_icon(icon)

#! game background

background = pygame.image.load('./img/background.png')

#! player
playerImage = pygame.image.load('./img/spaceship.png')
playerX = 370
playerY = 480

playerX_change = 0
playerY_change = 0
def player(x , y):
    screen.blit(playerImage, (x, y))

#! enemy
enemyImage = pygame.image.load('./img/enemy.png')
enemyX = random.randint(0, 800)
enemyY = 50

enemyX_change = 5
enemyY_change = 15
def enemy(x , y):
    screen.blit(enemyImage, (x, y))

#! bullet
bulletImage = pygame.image.load('./img/bullet.png')
bulletX = playerX
bulletY = playerY

bulletX_change = 5
bulletY_change = 5
bullet_state = "ready"
def fire_bullet(x , y):
    global bullet_state 
    bullet_state = "fire"
    screen.blit(bulletImage, (x + 24, y + 10))

#! the loop game
runing = True

while runing:

    #! red, green, blue 
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    # playerX = (playerX + 5) % 800
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            runing = False
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_LEFT:
                playerX_change = -5
            elif e.key == pygame.K_RIGHT:
                playerX_change = 5
            if e.key == pygame.K_UP:
                playerY_change = -5
            elif e.key == pygame.K_DOWN:
                playerY_change = 5
            if e.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bulletY = playerY
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        elif e.type == pygame.KEYUP:
            # if e.key == pygame.K_LEFT or e.key == pygame.K_RIGHT:
            playerX_change = 0
            playerY_change = 0
    playerX += playerX_change
    playerY += playerY_change
    if playerX >= 736 or playerX < 0:
        playerX = 736
    if playerY >= 536 or playerY < 0:
        playerY = 536

    enemyX += enemyX_change
    # enemyY += enemyY_change

    if enemyX >= 736:
        enemyX_change = -5
        enemyY += enemyY_change
    elif enemyX <= 0:
        enemyX_change = 5
        enemyY += enemyY_change
    

    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change
    if bulletY < 0:
        bullet_state = "ready"
        bulletY = playerY

    
    player(playerX, playerY)
    enemy(enemyX, enemyY)

    pygame.display.update()