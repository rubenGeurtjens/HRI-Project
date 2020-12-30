import pygame
from agents import manualAgent, ppoAgent, greedyAgent
import numpy as np
from boids import Boid
import random
import math

class env():

    def __init__(self):
        self.size = [600, 400]
        self.agent = greedyAgent.greedyAgent([200,300],[3,3])
        self.setup = True
        self.goal = [290,50]
        self.clock = pygame.time.Clock()
        self.objects = [[200,100], [250,150], [340,250], [400,100],[100,280]]


        self.width = 600
        self.height = 400

        self.nr_crowds = 3
        self.goals = [(100, 30), (500, 30), (100, 370), (500, 370)]

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

        for crowd in self.crowd:
            self.boid(crowd)

        self.agent.step(action)
        

        x,y = self.agent.get_pos()

        dist = self.agent.dist_goal(self.goal)
            
        if dist < 10:
            print('finished!!!!')
            done = True


        
    
        objects = [boid.position for crowd in self.crowd for boid in crowd]

        min_dist = np.inf
        for obstacle in objects:
            if self.agent.dist_goal(obstacle, self.agent.pos) < min_dist:
                min_dist = self.agent.dist_goal(obstacle, self.agent.pos)
                closest_obstacle = obstacle

        if min_dist < 2:
            print("collision!!!")
            done = True

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
        self._draw_crowd(self.crowd)
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
            self.goal = [500,30]

        elif x == 2:
            self.goal = [100,370]  

        elif x == 3:
            self.goal = [500,370]
        
        self.make_crowd()
        
        objects = [boid.position for crowd in self.crowd for boid in crowd]

        return [self.goal, objects]
    
    def boid(self, crowd):
        for boid in crowd:
            
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
    
    def make_crowd(self):
        self.crowd = []
        for c in range(self.nr_crowds):
            x = np.random.randint(100,500)
            y = np.random.randint(100,300)
            goal = np.random.randint(4)
            new_crowd = [Boid(np.random.randint(x, x+100), random.randint(y,y+100), self.width, self.height, goal) for _ in range(10)]
            self.crowd.append(new_crowd)

    def _draw_agent(self):
        x,y = self.agent.get_pos()
        w,h = self.agent.get_size()
        rec = pygame.Rect(x-w/2,y-h/2,w,h)
        pygame.draw.circle(self.screen, (255,0,0), self.agent.pos, 3)

    def _draw_goal(self):
        for goal in self.goals:
            x,y = goal
            rec = pygame.Rect(x-10,y-10,20,20)
            pygame.draw.rect(self.screen, (0,100,0), rec)


        x,y = self.goal
        rec = pygame.Rect(x-10,y-10,20,20)
        pygame.draw.rect(self.screen, (0,255,0), rec)

    def _draw_objects(self):
        for person in self.objects:
            x,y = person
            w,h = self.agent.get_size()
            rec = pygame.Rect(x-w/2,y-h/2,w,h)
            pygame.draw.rect(self.screen, (0,0,255), rec)

    def _draw_crowd(self, crowds):
        # surface, color, center, radius
        # hier worden de locaties van de mensjes geupdate
        for crowd in crowds:
            for boid in crowd:
                person = boid.position
                pygame.draw.circle(self.screen, (0,0,255), person, 3)