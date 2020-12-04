import pygame
import numpy as np
from agents import manualAgent, ppoAgent, greedyAgent

'''
Deze file is waar jullie je crowd dingen in kunnen maken.
'''

class env():

    def __init__(self):
        self.size = [600, 400]
        self.agent = manualAgent.manualAgent([200,300],[20,20])
        self.setup = True
        self.goal1 = [100,50]
        # self.goal2 = [100,150]
        # self.goal3 = [100,250]
        self.crowd = [(np.random.randint(0,600),np.random.randint(0,400)),
                        (np.random.randint(0,600),np.random.randint(0,400))]
        self.clock = pygame.time.Clock()
        self.done = False

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

        ## Hier moeten we die euclidean shit maken

        for i, person in enumerate(self.crowd):
            x, y = person
            y = 1 * x + 11
            if x > 600:
                print("out of screen")
                self.done = True
            new_center = (x + 1, y)
            self.crowd[i] = new_center

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
        for person in self.crowd:
            pygame.draw.circle(self.screen, (0,0,255), person, 3)


if __name__ == "__main__":
    env = env()
    env.reset()
    while env.done != True:
        env.render()
        env.step()
