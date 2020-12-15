import pygame
from agents import manualAgent, ppoAgent, greedyAgent
import numpy as np

class env():

    def __init__(self):
        self.size = [600, 400]
        #self.agent = ppoAgent.ppoAgent([200,300],[20,20])
        self.agent = greedyAgent.greedyAgent([200,300],[20,20])
        self.setup = True
        self.goal = [290,50]
        self.clock = pygame.time.Clock()
        self.objects = [[0,0],[200,100]]


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
        done = False
        reward = 0
        self.agent.step(action)
        

        x,y = self.agent.get_pos()

        done = x < 0 or x > self.size[0] or y < 0 or y > self.size[1]

        dist = self.agent.dist_goal(self.goal)
            
        if dist < 10:
            print('finished!!!!')
            done = True
            reward = 50

        punishment = -1* dist / 634.113554 

        if self.agent.name == "ppo":
            obs=np.concatenate((self.agent.get_pos(), self.goal))
        
        if self.agent.name == "greedy":
            obs = [self.goal, self.objects]



        return obs, punishment + reward, done, {}

    def render(self, mode='human'):
        """
        Used to render the screen
        """
        if self.setup:
            self.screen = pygame.display.set_mode((self.size[0], self.size[1]))
            self.setup = False

        self.screen.fill((0,0,0))
        self._draw_agent()
        self._draw_goal()
        self._draw_objects()
        pygame.display.update()

        #self.clock.tick(60)

    def reset(self):
        """
        Resets the enviornment to begin condition

        returns:
        initial observation
        """
        self.agent.pos = [300,200]

        x = np.random.randint(2)

        if x == 0:
            self.goal = [100,10]

        elif x == 1:
            self.goal = [500,10]
        
        #self.agent.pos = [np.random.randint(0,600),np.random.randint(0,400)]
        if self.agent.name == "ppo":
            return np.concatenate((self.agent.get_pos(), self.goal))

        if self.agent.name == "greedy":
            return [self.goal, self.objects]

    def _draw_agent(self):
        x,y = self.agent.get_pos()
        w,h = self.agent.get_size()
        rec = pygame.Rect(x,y,w,h)
        pygame.draw.rect(self.screen, (255,0,0), rec)

    def _draw_goal(self):
        x,y = self.goal
        rec = pygame.Rect(x,y,20,20)
        pygame.draw.rect(self.screen, (0,255,0), rec)

    def _draw_objects(self):
        for person in self.objects:
            x,y = person
            w,h = self.agent.get_size()
            rec = pygame.Rect(x,y,w,h)
            pygame.draw.rect(self.screen, (0,0,255), rec)
