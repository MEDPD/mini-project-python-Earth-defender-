import random
from math import *
import sys, os, time

import pygame
from pygame import mixer

from Models import Player, Enemy, Bullet

#! initialize the game

pygame.init()

#! create the game screen

screen = pygame.display.set_mode((800, 600))

#! title and icon

pygame.display.set_caption('Earth defender')
icon = pygame.image.load('./img/spaceship.png')
pygame.display.set_icon(icon)

#! game background

background = pygame.image.load('./img/background.png')

#! game music
# mixer.music.load('./music/background.wav')
# mixer.music.play(-1)

# global variables
runing = True
end = False



# the main
def main():
    
    #! player
    playerX = 400
    playerY = 480
    human_player = Player.player(pygame.image.load('./img/spaceship.png'), playerX, playerY, 0, 0) 
    
    #! enemies
    enemies = []
    new_enemy1 = Enemy.enemy(pygame.image.load('./img/enemy.png'), random.randint(1, 736), random.randint(1, 50), 5, 40, mixer.Sound('./sound/explosion.wav'))
    new_enemy2 = Enemy.enemy(pygame.image.load('./img/enemy.png'), random.randint(1, 736), random.randint(1, 50), 5, 40, mixer.Sound('./sound/explosion.wav'))
    enemies.append(new_enemy1)
    enemies.append(new_enemy2)
    
    
    #! enemyGuardian
    g1x = random.randint(1, 150)
    g1y = random.randint(1, 100)
    g2x = random.randint(600, 800) # g1x + 150
    g2y = random.randint(300, 400) # g1x + 200
    enemyG = Enemy.enemyGuardian(pygame.image.load('./img/enemyGuardian.png'), g1x, g1y, 5, 40, mixer.Sound('./sound/explosion.wav'))
    enemyG2 = Enemy.enemyGuardian(pygame.image.load('./img/enemyGuardian.png'), g2x, g2y, 5, 40, mixer.Sound('./sound/explosion.wav'))
    enemies.append(enemyG)
    enemies.append(enemyG2)
    
    
    
    
    #! the loop game
    global runing
    global end
    while runing:
    
        #! red, green, blue 
        screen.fill((0, 0, 0))
        screen.blit(background, (0, 0))
        
        #! keydown and keyup listeners
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                runing = False
            if not end:
                human_player.initializePlaying(e)
    
        if not end:
            human_player.move()
            human_player.initializeFire(screen, enemies)
            human_player.keepMeOnTheScreen()

        if human_player.getState() is "dead":
            game_over(enemies, False)
        else:
            human_player.play(screen)
        
        for b in human_player.getBulletsStock():
            if b.getState() is "gone":
                human_player.getBulletsStock().remove(b)
        
    
        if not end:
            enemyG.initializeFire(screen, human_player)
            # enemyG.locateShootingPlace(human_player.x, human_player.y)  
            enemyG.initializePlaying(human_player.x, human_player.y)
            enemyG.keepMeOnTheScreen()
            
        
            # enemyG2.move()
            enemyG2.initializeFire(screen, human_player)
            # enemyG2.locateShootingPlace(human_player.x, human_player.y)  
            enemyG2.initializePlaying(human_player.x, human_player.y)
            enemyG2.keepMeOnTheScreen()
                      
        
        
        
        if not end:
            for e in enemies:
               e.move()
            for en in enemies:
                en.play(screen) 
                if en.state is "killed":
                    # print(type(en))
                    enemies.remove(en)
        
        if len(enemies) == 0:
            game_over(enemies, True)
        pygame.display.update()
    
    print(human_player.getBulletsStock())
    print(enemies)

def game_over(enemies, win):
    global end
    for en in enemies:
        en.state = "killed"
    
    if win:
        screen.fill((255, 255, 255))
    elif not win:
        screen.fill((0, 0, 0))
    end = True
        



if __name__ == '__main__': main()