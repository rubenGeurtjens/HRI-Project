import pygame
import random
import math
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
        self.goals = [(100, 50), (100, 200), (100, 350)]
        self.crowd1 = [Boid(random.randint(500, 600), random.randint(300, 400), self.width, self.height, 0) for _ in range(10)]
        self.crowd2 = [Boid(random.randint(300, 400), random.randint(250, 350), self.width, self.height, 1) for _ in range(10)]
        self.crowd3 = [Boid(random.randint(200, 300), random.randint(150, 250), self.width, self.height, 2) for _ in range(10)]
        self.clock = pygame.time.Clock()
        self.done = False

    def step(self, crowd):
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

        for boid in crowd:
            random_int = random.randint(0, 5)

            # if random_int > 4:
            #     random_int = random.randint(0, 5)
            #     if random_int > 4:
            #         for i in range (1, 500):
            #             goalX, goalY = self.goals[boid.goalNr]
            #             x, y = boid.position

            #             if (goalX + 10  >= x >= goalX - 10) and (goalY + 10  >= y >= goalY - 10):
            #                 boid.reached_goal(goalX + 10, goalY + 10)

            #             dx = random.randint(0, self.width) - x
            #             dy = random.randint(0, self.height) - y

            #             # Unit vector in the same direction
            #             distance = math.sqrt(dx * dx + dy * dy)
            #             dx /= distance
            #             dy /= distance

            #             # And now we move:
            #             x += dx
            #             y += dy

            #             boid.set_goal(dx, dy)

            #             boid.position += boid.velocity
            #else:
            #           boid.position += boid.velocity
            
            # Vector from me to cursor


            goalX, goalY = self.goals[boid.goalNr]
            x, y = boid.position

            if (goalX + 10  >= x >= goalX - 10) and (goalY + 10  >= y >= goalY - 10):
                boid.reached_goal(goalX + 10, goalY + 10)

            else:
                dx = goalX - x
                dy = goalY - y

                # Unit vector in the same direction
                # distance = np.linalg.norm(dx * dx + dy * dy)
                distance = math.sqrt(dx * dx + dy * dy)
                dx /= distance
                dy /= distance

                # And now we move:
                x += dx
                y += dy

                boid.set_goal(dx, dy)

                boid.position += boid.velocity

    def render(self, mode='human'):
        """
        Used to render the screen
        """
        if self.setup:
            self.screen = pygame.display.set_mode((self.size[0], self.size[1]))
            self.setup = False

        self.screen.fill((0,0,0))
        self._draw_agent()
        self._draw_crowd(self.crowd1)
        self._draw_crowd(self.crowd2)
        self._draw_crowd(self.crowd3)
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

        return np.concatenate((self.agent.get_pos(), [100, 200]))

    def _draw_agent(self):
        x,y = self.agent.get_pos()
        w,h = self.agent.get_size()
        rec = pygame.Rect(x,y,w,h)
        pygame.draw.rect(self.screen, (255,0,0), rec)

    def _draw_goal(self):
        for goal in self.goals:
            x, y = goal
            rec = pygame.Rect(x, y, 20, 20)
            pygame.draw.rect(self.screen, (0,255,0), rec)

    def _draw_crowd(self, crowd):
        # surface, color, center, radius
        # hier worden de locaties van de mensjes geupdate
        for boid in crowd:
            person = boid.position
            pygame.draw.circle(self.screen, (0,0,255), person, 3)


if __name__ == "__main__":
    env = env()
    env.reset()
    while env.done != True:
        env.render()
        env.step(env.crowd1)
        env.step(env.crowd2)
        env.step(env.crowd3)
