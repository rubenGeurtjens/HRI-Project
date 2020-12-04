import pygame
import random
from pygame.math import Vector2
import numpy as np
from boids import Boid
from agents import manualAgent, ppoAgent, greedyAgent

'''
Deze file is waar jullie je crowd dingen in kunnen maken.
'''

class env():

    def __init__(self):
        self.width = 600
        self.height = 400
        self.size = [self.width, self.height]
        self.agent = manualAgent.manualAgent([200,300],[20,20])
        self.setup = True
        self.goal1 = [100,50]
        # self.goal2 = [100,150]
        # self.goal3 = [100,250]
        self.crowd = [Boid(random.randint(0, 600), random.randint(0, 400), self.width, self.height) for _ in range(3)]
        self.clock = pygame.time.Clock()
        self.done = False

    def edges(self):
        if self.position.x > self.width:
            self.position.x = 0
        elif self.position.x < 0:
            self.position.x = self.width

        if self.position.y > self.height:
            self.position.y = 0
        elif self.position.y < 0:
            self.position.y = self.height

    def step(self):
        """
        Performs one update step
        and contains the main logic

        returns:
        observation: contains all info that the agent needs, so positions etc
        reward: reward that the agent gets for performing the action
        done: Boolean that indicates if episode is over, for instance if the agent
            "dies" or finishes the tasks
        info: dictionary of extra info that can be used to debug
        """


        # self.position += self.velocity
        # self.velocity += self.acceleration
        # #limit
        # if np.linalg.norm(self.velocity) > self.max_speed:
        #     self.velocity = self.velocity / np.linalg.norm(self.velocity) * self.max_speed
        #
        # self.acceleration = Vector2(*np.zeros(2))

        ## Hier moeten we die boid shit maken
        # print(self.crowd)
        # for i, person in enumerate(self.crowd):
        #     x, y = person
        #     # y = 1 * x + 11
        #     # if y > 600 or y < 0 or x > 400 or x < 0:
        #     #     print("out of screen")
        #     #     self.done = True
        #     new_center = (x + 1, y)
        #     self.crowd[i] = new_center

    def render(self, mode='human'):
        """
        Used to render the screen
        """
        if self.setup:
            self.screen = pygame.display.set_mode((self.size[0], self.size[1]))
            self.setup = False

        self.screen.fill((0,0,0))
        self._draw_agent()
        self._draw_crowd()
        self._draw_goal()
        pygame.display.update()

        self.clock.tick(60)
        # pass

    def reset(self):
        """
        Resets the enviornment to begin condition

        returns:
        initial observation
        """
        self.agent.pos = [np.random.randint(0,600),np.random.randint(0,400)]

        return np.concatenate((self.agent.get_pos(), self.goal1))

    def _draw_agent(self):
        x,y = self.agent.get_pos()
        w,h = self.agent.get_size()
        rec = pygame.Rect(x,y,w,h)
        pygame.draw.rect(self.screen, (255,0,0), rec)

    def _draw_goal(self):
        x1,y1 = self.goal1
        rec1 = pygame.Rect(x1,y1,20,20)
        pygame.draw.rect(self.screen, (0,255,0), rec1)

    def _draw_crowd(self):
        # surface, color, center, radius
        # hier worden de locaties van de mensjes geupdate
        for boid in self.crowd:
            person = boid.position
            pygame.draw.circle(self.screen, (0,0,255), person, 3)


if __name__ == "__main__":
    env = env()
    env.reset()
    while env.done != True:
        env.render()
        env.step()
