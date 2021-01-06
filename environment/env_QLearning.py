import pygame
from agents import manualAgent, ppoAgent, greedyAgent, QLearningAgent
import numpy as np
from boids import Boid
import math
from pygame.math import Vector2

class env():

    def __init__(self):
        
        self.size = [500, 500]
        self.setup = True
        self.clock = pygame.time.Clock()

        self.goal = [115,35]
        self.agent = QLearningAgent.QLearningAgent([105,25],[3,3])

    def step(self, action):
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
        self.agent.step(action) 

        obs = np.zeros((21,21)) 

        x,y = self.agent.get_pos()       
        x2,y2=self.goal 
        
        obs[10,10] = 2

        #if goal in reach
        if abs(x-x2) <= 10 and abs(y-y2) <= 10:
            obs[y2-y+10, x2-x+10] = 1
            
        return obs, 0, False, {}



    def render(self, mode='human'):
        """
        Used to render the screen
        """
        if self.setup:
            #self.screen  = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            self.screen = pygame.display.set_mode((self.size[0], self.size[1]))
            self.setup = False

        self.screen.fill((0,0,0))
        self._draw_goal()
        self._draw_agent()
        pygame.display.update()

       # self.clock.tick(20)

    def reset(self):
        """
        Resets the enviornment to begin condition

        returns:
        initial observation
        """

        self.agent.pos = [105,25]

        grid = np.zeros((21,21)) 
        x,y = self.agent.get_pos()       
        x2,y2=self.goal 
        
        grid[10,10] = 2

        #if goal in reach
        if abs(x-x2) <= 10 and abs(y-y2) <= 10:
            grid[y2-y+10, x2-x+10] = 1

        return grid 
    


    def _draw_agent(self):
        pygame.draw.circle(self.screen, (255,0,0), self.agent.pos, 3)

    def _draw_goal(self):
        x,y = self.goal
        rec = pygame.Rect(x-10,y-10,20,20)
        pygame.draw.rect(self.screen, (0,255,0), rec)