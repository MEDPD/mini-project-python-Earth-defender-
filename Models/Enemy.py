import random

import pygame
from pygame import mixer 

from . import Bullet
from EarthDefenderError import EarthDefenderError

UP = "UP"
DOWN = "DOWN"
LEFT = "LEFT"
RIGHT = "RIGHT" 

class enemy:
    def __init__(self, img, x, y, dx, dy, death_sound):
        self.img = img
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.state = "alive"
        self.death_sound = death_sound
        self._position = UP
        self._classTime = 2*1000 # 2sec
    def getBulletsStock(self):
        return self._bulletStock
    def play(self, screen):
        screen.blit(self.img, (self.x,self.y))
    def move(self):
        self._weakMove()

    def _weakMove(self):
        self.x += self.dx 
        if self.x  >= 736:
            self.dx  = -5
            self.y += self.dy
        elif self.x  <= 0:
            self.dx = 5
            self.y += self.dy

class enemyGuardian(enemy):
    '''
     blt : bullet
    '''
    def __init__(self, img, x, y, dx, dy, death_sound):
        super(enemyGuardian, self).__init__(img, x, y, dx, dy, death_sound)
        self._bulletStock = []
        self._hasShootingPosition = False
        # self._movement = "standing"

    def stopMoving(self):
        # print('calling stopMoving')
        self.dx = 0
        self.dy = 0
    def play(self, screen):
        screen.blit(self.img, (self.x,self.y))
    def move(self):
        self.x += self.dx
        self.y += self.dy
    def initializeFire(self, screen, HumanPlayer):
        for blt in self._bulletStock:
            if blt.getState() is "fire":
                self.launchBullet(blt, screen) # blt.fire_bullet(screen)
            #! code the player death here
            if blt.isCollision(HumanPlayer.x, HumanPlayer.y):
                if blt in self._bulletStock:
                    self._bulletStock.remove(blt)
                    HumanPlayer.setState("dead")
    def locateShootingPlace(self, px, py): 
        if (px >= self.x +2 or px <= self.x -2) and (py >= self.y +2 or py <= self.y -2):
            
            # print("mov", self.x, self.y)
            
            if abs(px - self.x) < abs(py - self.y):
                # print("mova<b", abs(px - self.x), abs(py - self.y))
                if px > self.x:         
                    self.moveRight()
                elif px < self.x:
                    self.moveLeft()   
            elif abs(px - self.x) > abs(py - self.y):
                # print("mova>b", abs(px - self.x), abs(py - self.y))
                if py > self.y:
                    self.moveDown()
                elif py < self.y:
                    self.moveUp()
            self._hasShootingPosition = False
        elif (px <= self.x +2 and px >= self.x -2) or (py <= self.y +2 and py >= self.y -2):
            # print("stop")
            self.stopMoving()
            if not self._hasShootingPosition:
                # print('tkShoot')
                self.takeShootingPosition(px=px, py=py)
                self._hasShootingPosition = True

            self.fire()
    def initializePlaying(self, px, py):
        self.locateShootingPlace(px, py)

    def takeShootingPosition(self, px, py):
        if (px <= self.x +2 and px >= self.x -2):
            if self.y > py:
                if self._position is LEFT:
                    self.img = pygame.transform.rotate(self.img, -90)
                    self._position = UP
                elif self._position is RIGHT:
                    self.img = pygame.transform.rotate(self.img, 90)
                    self._position = UP
            elif self.y < py:
                if self._position is LEFT:
                    self.img = pygame.transform.rotate(self.img, 90)
                    self._position = DOWN
                elif self._position is RIGHT:
                    self.img = pygame.transform.rotate(self.img, -90)
                    self._position = DOWN
        elif (py <= self.y +2 and py >= self.y -2):
            if self.x > px:
                if self._position is DOWN:
                    self.img = pygame.transform.rotate(self.img, -90)
                    self._position = LEFT
                elif self._position is UP:
                    self.img = pygame.transform.rotate(self.img, 90)
                    self._position = LEFT
            elif self.x < px:
                if self._position is DOWN:
                    self.img = pygame.transform.rotate(self.img, 90)
                    self._position = RIGHT
                elif self._position is UP:
                    self.img = pygame.transform.rotate(self.img, -90)
                    self._position = RIGHT

    def launchBullet(self, blt, screen):
        blt.fire_bullet(self._position, screen)

    def fire(self):
        if self.state is not "killed" and pygame.time.get_ticks() % 30 == 0:
            new_bullet = Bullet.bullet(pygame.image.load('./img/alienBullet.png'), self.x, self.y, 8, 8, mixer.Sound('./sound/laser.wav'))
            new_bullet.fire_sound.play()
            new_bullet.x = new_bullet.x -17
            new_bullet.setState("fire")
            self.getBulletsStock().append(new_bullet)
    def keepMeOnTheScreen(self):
        # print('calling keepMeOnTheScreen')
        if self.x >= 700:
            self.x = 700
        if self.x < 0:
            self.x = 0
        if self.y >= 520:
            self.y = 520
        if self.y < 0:
            self.y = 0
    def moveLeft(self):
        if self._position is not LEFT:
            if self._position is DOWN:
                self.img = pygame.transform.rotate(self.img, -90)
            elif self._position is UP:
                self.img = pygame.transform.rotate(self.img, 90)
            elif self._position is RIGHT:
                self.img = pygame.transform.rotate(self.img, 180)
            self._position = LEFT
            # print('pos : left')
        self.dx = -2
        self.dy = 0
    def moveRight(self):
        if self._position is not RIGHT:
            if self._position is LEFT:
                self.img = pygame.transform.rotate(self.img, 180)
            elif self._position is UP:
                self.img = pygame.transform.rotate(self.img, -90)
            elif self._position is DOWN:
                self.img = pygame.transform.rotate(self.img, 90)
            self._position = RIGHT
        self.dx = 2
        self.dy = 0
    def moveUp(self):
        if self._position is not UP:
             if self._position is DOWN:
                self.img = pygame.transform.rotate(self.img, 180)
             elif self._position is LEFT:
                self.img = pygame.transform.rotate(self.img, -90)
             elif self._position is RIGHT:
                self.img = pygame.transform.rotate(self.img, 90)
             self._position = UP
        self.dy = -2
        self.dx = 0
    def moveDown(self):
        if self._position is not DOWN:
            if self._position is UP:
                self.img = pygame.transform.rotate(self.img, 180)
            elif self._position is LEFT:
                self.img = pygame.transform.rotate(self.img, 90)
            elif self._position is RIGHT:
                self.img = pygame.transform.rotate(self.img, -90)
            self._position = DOWN
        self.dy = 2
        self.dx = 0