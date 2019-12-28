from math import *
from EarthDefenderError import EarthDefenderError
from . import Enemy, Player

import pygame

class bullet:
    kill = False
    def __init__(self, img, x, y, dx, dy, fire_sound):
        self.img = img
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self._state = "ready"
        self.fire_sound = fire_sound
        self._havePosition = False
        self._first_position = ''
         
    def fire_bullet(self, pos, screen):
        if self._havePosition is False:
            self._first_position = str(pos)
            # print(first_position)
            if self._first_position  is Player.DOWN:
                self.img = pygame.transform.rotate(self.img, 180)
            elif self._first_position is Player.RIGHT:
                self.img = pygame.transform.rotate(self.img, -90)
            elif self._first_position  is Player.LEFT:
                self.img = pygame.transform.rotate(self.img, 90)
            self._havePosition = True

        screen.blit(self.img, (self.x + 42, self.y + 42 ))
        if self._first_position  is Player.UP:
            self.y -= self.dy
        elif self._first_position  is Player.DOWN:
            self.y += self.dy
        elif self._first_position  is Player.RIGHT:
            self.x += self.dx
        elif self._first_position  is Player.LEFT:
            self.x -= self.dx
        if self.y < 0 or self.y > 600 or self.x < 0 or self.x > 800:
            self.setState("gone")
    def isCollision(self, target_x, target_y):
        distance = sqrt(pow(target_x - self.x, 2) + pow(target_y - self.y, 2))
        if distance < 30:
            return True
        else:
            return False 
    def getState(self):
        return self._state
    def setState(self, state):
        if state in ("ready", "fire", "fired", "gone"):
            self._state = state
        else:
            raise EarthDefenderError("we couldn't set bullet satate to " + str(state) + " \n the acceptable values are : \nready, fire, fired, gone")


