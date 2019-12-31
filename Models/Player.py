import random

from pygame import mixer

from . import Bullet, Enemy
import pygame

UP = "UP"
DOWN = "DOWN"
LEFT = "LEFT"
RIGHT = "RIGHT" 

class player:
    def __init__(self, img, x, y, dx, dy):
        self.img = img
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self._position = UP
        self._bulletStock = []
        self._state = "alive"
        self.data = {LEFT: [0],RIGHT: [0], UP: [0], DOWN: [0]}
        self.dataMoves = [[], []]
    def getBulletsStock(self):
        return self._bulletStock
    def getState(self):
        return self._state
    def setState(self, state):
        self._state = state
    def play(self, screen):
        screen.blit(self.img, (self.x, self.y))
                  
    def initializePlaying(self, e):
        #! keydown listener
        if e.type == pygame.KEYDOWN:
                #! movements listener
                if e.key == pygame.K_LEFT:
                    self.moveLeft()
                elif e.key == pygame.K_RIGHT:
                    self.moveRight()
                if e.key == pygame.K_UP:
                    self.moveUp()
                elif e.key == pygame.K_DOWN:
                    self.moveDown()
                #! fires listener
                if e.key == pygame.K_SPACE:
                    self.fire()
            #! keydup listener
        elif e.type == pygame.KEYUP:
            self.stopMoving()


    def initializeFire(self, screen, enemies):
        for blt in self._bulletStock:
            if blt.getState() is "fire":
                self.launchBullet(blt, screen) # blt.fire_bullet(screen)
            for e in enemies:
                if blt.isCollision(e.x , e.y):
                    if blt in self._bulletStock:
                        self._bulletStock.remove(blt)
                    Bullet.bullet.kill = True
                    if e in enemies:
                        e.death_sound.play()
                        e.state = "killed"
                
                    
    def launchBullet(self, blt, screen):
        blt.fire_bullet(self._position, screen)

    def fire(self):
        self.data[self._position][0] += 1 
        new_bullet = Bullet.bullet(pygame.image.load('./img/bullet.png'), self.x, self.y, 8, 8, mixer.Sound('./sound/laser.wav'))
        new_bullet.fire_sound.play()
        new_bullet.setState("fire")


        self.getBulletsStock().append(new_bullet)
    def stopMoving(self):
        self.dx = 0
        self.dy = 0
    def move(self):
        self.x += self.dx
        self.y += self.dy
        self.dataMoves[0].append(self.x)
        self.dataMoves[1].append(600 - self.y)
    def keepMeOnTheScreen(self):
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
        self.dx = -4
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
        self.dx = 4
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
        self.dy = -4
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
        self.dy = 4
        self.dx = 0
    
    