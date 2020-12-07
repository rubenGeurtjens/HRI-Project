import pygame
import random
import numpy as np
from pygame.math import Vector2

class Boid():

    def __init__(self, x, y, width, height):
        self.position = Vector2(x, y)
        vec = (np.random.rand(2) - 0.5)*10

        self.velocityX = 0
        self.velocityY = 0
        self.velocity = (self.velocityX, self.velocityY)

    def set_goal(self, velX, velY):
        self.velocityX = velX
        self.velocityY = velY
        self.velocity = Vector2(velX, velY)

    def reached_goal(self, goalX, goalY):
        self.position = Vector2(goalX, goalY)
