import pygame
from agents import manualAgent, ppoAgent, greedyAgent
import numpy as np
from boids import Boid
import random
import math

class env():

    def __init__(self):
        self.size = [600, 400]
        self.agent = greedyAgent.greedyAgent([200,300],[20,20])
        self.setup = True
        self.goal = [290,50]
        self.clock = pygame.time.Clock()
        self.objects = [[200,100], [250,150], [340,250], [400,100],[100,280]]


        self.width = 600
        self.height = 400
        self.crowd1 = [Boid(random.randint(500, 600), random.randint(300, 400), self.width, self.height, 0) for _ in range(10)]
        self.goals = [(100, 50), (100, 200), (100, 350)]

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

        self.boid(self.crowd1)

        self.agent.step(action)
        

        x,y = self.agent.get_pos()

        dist = self.agent.dist_goal(self.goal)
            
        if dist < 10:
            print('finished!!!!')
            done = True

        
        objects = [boid.pos for boid in self.crowd1]

        obs = [self.goal, objects]



        return obs, 0, done, {}

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
        #self._draw_objects()
        self._draw_crowd(self.crowd1)
        pygame.display.update()

        self.clock.tick(120)

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
        
        
        return [self.goal, self.objects]
    
    def boid(self, crowd):
        for boid in crowd:
            random_int = random.randint(0, 5)

            if random_int > 4:
                random_int = random.randint(0, 5)
                if random_int > 4:
                    for i in range (1, 500):
                        goalX, goalY = self.goals[boid.goalNr]
                        x, y = boid.position

                        if (goalX + 10  >= x >= goalX - 10) and (goalY + 10  >= y >= goalY - 10):
                            boid.reached_goal(goalX + 10, goalY + 10)

                        dx = random.randint(0, self.width) - x
                        dy = random.randint(0, self.height) - y

                        # Unit vector in the same direction
                        distance = math.sqrt(dx * dx + dy * dy)
                        dx /= distance
                        dy /= distance

                        # And now we move:
                        x += dx
                        y += dy

                        boid.set_goal(dx, dy)

                        boid.position += boid.velocity


            else:
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

    def _draw_crowd(self, crowd):
        # surface, color, center, radius
        # hier worden de locaties van de mensjes geupdate
        for boid in crowd:
            person = boid.position
            pygame.draw.circle(self.screen, (0,0,255), person, 3)
