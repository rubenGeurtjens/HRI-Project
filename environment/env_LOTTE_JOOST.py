import pygame
import numpy as np
from agents import manualAgent, ppoAgent

'''
Deze file is waar jullie je crowd dingen in kunnen maken.
'''


class env():

    def __init__(self):
        self.size = [600, 400]
        self.agent = ppoAgent.ppoAgent([200,300],[20,20])
        self.setup = True
        self.goal1 = [100,50]
        self.goal2 = [100,150]
        self.goal3 = [100,250]
        self.crowd = [(100, 50), (100,60)]
        self.clock = pygame.time.Clock()

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
        
        # self.agent.step(action)
        #
        # done = False
        # reward = 0
        # dist = self.agent.dist_goal(self.goal1)
        # if dist < 10:
        #     print('finished!!!!')
        #     reward = 500
        #     done = True
        # obs=np.concatenate((self.agent.get_pos(), self.goal1))
        # return obs, -0.1*dist+reward, done, {}

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

        # self.clock.tick(60)
        # pass

    def reset(self):
        """
        Resets the enviornment to begin condition

        returns:
        initial observation
        """
        print("reset")
        self.agent.pos = [np.random.randint(0,600),np.random.randint(0,400)]

        return np.concatenate((self.agent.get_pos(), self.goal1))

    def _draw_agent(self):
        x,y = self.agent.get_pos()
        w,h = self.agent.get_size()
        rec = pygame.Rect(x,y,w,h)
        pygame.draw.rect(self.screen, (255,0,0), rec)

    def _draw_goal(self):
        x1,y1 = self.goal1
        x2,y2 = self.goal2
        x3,y3 = self.goal3
        rec1 = pygame.Rect(x1,y1,20,20)
        rec2 = pygame.Rect(x2,y2,20,20)
        rec3 = pygame.Rect(x3,y3,20,20)
        pygame.draw.rect(self.screen, (0,255,0), rec1)
        pygame.draw.rect(self.screen, (0,255,0), rec2)
        pygame.draw.rect(self.screen, (0,255,0), rec3)

    def _draw_crowd(self):
        # surface, color, center, radius
        for i in range(0,5):
            center = (x, y)
            pygame.draw.circle(self.screen, (0,0,255), center, 10)


if __name__ == "__main__":
    env = env()
    env.reset()
    while True:
        env.render()
        env.step([0,0])
