import random
from math import *
import sys, os, time

import pandas as pd
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

earth = pygame.image.load('./img/planet-earth.png')
#! game music
# mixer.music.load('./music/background.wav')
# mixer.music.play(-1)

#! global variables
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
    new_enemy1 = Enemy.enemy(pygame.image.load('./img/enemy.png'), random.randint(350, 549 ), -20, 5, 40, mixer.Sound('./sound/explosion.wav'))
    new_enemy2 = Enemy.enemy(pygame.image.load('./img/enemy.png'), random.randint(251, 350), -80, 5, 40, mixer.Sound('./sound/explosion.wav'))
    enemies.append(new_enemy1)
    enemies.append(new_enemy2)
    
    
    #! enemyGuardian
    enemiesGuardians = []
    g1x = random.randint(1, 150)
    g1y = random.randint(1, 100)
    g2x = random.randint(600, 800) 
    g2y = random.randint(300, 400) 
    enemyG = Enemy.enemyGuardian(pygame.image.load('./img/enemyGuardian.png'), g1x, g1y, 5, 40, mixer.Sound('./sound/explosion.wav'))
    enemyG2 = Enemy.enemyGuardian(pygame.image.load('./img/enemyGuardian.png'), g2x, g2y, 5, 40, mixer.Sound('./sound/explosion.wav'))
    enemiesGuardians.append(enemyG)
    enemiesGuardians.append(enemyG2)

    # enemies += enemiesGuardians
    
    #! earth
    
    #! the loop game
    global runing
    global end
    while runing:
    
        #! red, green, blue 
        # screen.fill((0, 0, 0))

        screen.blit(background, (0, 0))
        screen.blit(earth, (350, 550))


        #! keydown and keyup listeners
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                runing = False
            if not end:
                human_player.initializePlaying(e)
    
        if not end:
            human_player.move()
            human_player.initializeFire(screen, enemies+enemiesGuardians)
            human_player.keepMeOnTheScreen()

        if human_player.getState() is "dead":
            game_over(False)
        else:
            human_player.play(screen)
        
        for b in human_player.getBulletsStock():
            if b.getState() is "gone":
                human_player.getBulletsStock().remove(b)
        
    
        if not end:
            enemiesGuardians = Enemy.enemyGuardian.keepProducingGuardians(enemiesGuardians, human_player.x, human_player.y)
            enemiesGuardians = Enemy.enemyGuardian.checkAndAddEnemies(enemiesGuardians, human_player.x, human_player.y)
            
            for en in enemiesGuardians:
                en.initializeFire(screen, human_player)
                en.initializePlaying(human_player.x, human_player.y)
                en.keepMeOnTheScreen()
                en.move()
                en.play(screen)
                if en.state is "killed":
                    enemiesGuardians.remove(en)
            
        
        if not end:
            enemies = Enemy.enemy.checkAndAddEnemies(enemies)
            for en in enemies:
                en.move()
                en.play(screen)
                if en.state is "killed":
                    enemies.remove(en)

        for en in enemies:
            if en.arriveToEarth(350, 550):
                game_over(False)
        
        if len(enemies+enemiesGuardians) == 0:
            game_over(True)
        pygame.display.update()
    
    save_data(human_player)
    
    
    data = {'x':human_player.dataMoves[0], 'y':human_player.dataMoves[1]}

    df2 = pd.DataFrame(data)
    df2.to_csv(index=False, path_or_buf='./data/dataXY.csv', mode='w')



def game_over(win):
    global end

    if win:
        screen.fill((255, 255, 255))
    elif not win:
        screen.fill((0, 0, 0))
    end = True


def save_data(human_player):
    '''
        it's a function to save player moves, number of bullets fired and shooting positions
        so you can check out the moves you have done and also the your shooting positions
        and the number of bullets you have fired
    '''
    try:
        k = pd.read_csv('./data/dataFirePosition.csv')
        df2 = pd.DataFrame(human_player.data)  
        k = k.append(df2)
        k.to_csv(index=False, path_or_buf='./data/dataFirePosition.csv', mode='w')
    except:
        df2 = pd.DataFrame(human_player.data)
        df2.to_csv(index=False, path_or_buf='./data/dataFirePosition.csv', mode='w')

    
        
if __name__ == '__main__': main()
