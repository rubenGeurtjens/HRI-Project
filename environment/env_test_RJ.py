import pygame
from agents import manualAgent, ppoAgent, greedyAgent
import numpy as np

class env():

    def __init__(self):
        self.size = [600, 400]
        self.agent = ppoAgent.ppoAgent([200,300],[20,20])
        self.setup = True
        self.goal = [290,50]
        self.clock = pygame.time.Clock()
        self.objects = [[200,100], [250,150], [340,250], [400,100],[100,280]]


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
            
        if dist < 25:
            print('finished!!!!')
            done = True
            reward = 0

        #punishment = -1* dist / 634.113554  #normalizing
        punishment = self._calculate_punishment2(action)

        obs=np.concatenate((self.agent.get_pos(), self.goal))

        #print('punishment: ', punishment)
        # print('goal pos: ', self.goal)
        # print('agent pos: ', self.agent.get_pos())
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
        
        #self.clock.tick(2)

    def reset(self):
        """
        Resets the enviornment to begin condition

        returns:
        initial observation
        """
        self.agent.pos = [300,200]

        x = np.random.randint(4)

        if x == 0:
            self.goal = [100,30]

        elif x == 1:
            self.goal = [500,10]

        elif x == 2:
            self.goal = [100,370]  

        elif x == 3:
            self.goal = [500,370]
        
        #self.agent.pos = [np.random.randint(0,600),np.random.randint(0,400)]
        return np.concatenate((self.agent.get_pos(), self.goal))

    def _calculate_punishment(self, dist):
        if dist<50:
            return 20
        if dist<100:
            return 10
        if dist < 200:
            return 1
        else:
            return -1

    def _calculate_punishment2(self, action):
        reward = 0
        #if the current position is closed to the goal than the previous one give a reward
        curr_dist = self.agent.dist_goal(self.goal)
        self.agent.step([-action[0], -action[1]]) #move agent to previous location
        previous_dist = self.agent.dist_goal(self.goal)
        if curr_dist < previous_dist: 
            reward = 1
        self.agent.step(action) #move the agent back
        return reward 

    def _draw_agent(self):
        x,y = self.agent.get_pos()
        w,h = self.agent.get_size()
        rec = pygame.Rect(x-w/2,y-h/2,w,h)
        pygame.draw.rect(self.screen, (255,0,0), rec)

    def _draw_goal(self):
        x,y = self.goal
        rec = pygame.Rect(x-10,y-10,20,20)
        pygame.draw.rect(self.screen, (0,255,0), rec)

    def _draw_objects(self):
        for person in self.objects:
            x,y = person
            w,h = self.agent.get_size()
            rec = pygame.Rect(x-w/2,y-h/2,w,h)
            pygame.draw.rect(self.screen, (0,0,255), rec)
