import pygame
import numpy as np
from pygame.math import Vector2

class Boid():

    def __init__(self, x, y, width, height):
        self.position = Vector2(x, y)
        vec = (np.random.rand(2) - 0.5)*10
        self.velocity = Vector2(*vec)

        vec = (np.random.rand(2) - 0.5)/2
        self.acceleration = Vector2(*vec)
