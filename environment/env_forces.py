import pygame
from agents import manualAgent, ppoAgent, greedyAgent
import numpy as np
from boids import Boid
import math

class env():

    def __init__(self):
        self.screen  = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

        info = pygame.display.Info()
        screen_width,screen_height = info.current_w,info.current_h
        self.size = [screen_width, screen_height]
        self.agent = greedyAgent.greedyAgent([200,300],[3,3], 50,20)
        self.setup = False
        self.clock = pygame.time.Clock()
        self.objects = [[100,100], [self.size[0]-100,100], [self.size[0]-100,self.size[1]-100], [100,self.size[1]-100],[100,280]]

        self.nr_crowds = 50
        self.goals = [[100,100], [self.size[0]-100,100], [self.size[0]-100,self.size[1]-100], [100,self.size[1]-100]]

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

        # step all crowds
        for crowd in self.crowds:
            self.boid(crowd)

        #step agent
        self.agent.step(action)
            
        
        #check if episode is over finished/crashed
        done = False

        dist = self.agent.dist_goal(self.goal)

        if dist < 20:
            print('finished!!!!')
            done = True
    
        persons = [boid.position for crowd in self.crowds for boid in crowd]

        min_dist = np.inf
        for person in persons:
            if self.agent.dist_goal(person, self.agent.pos) < min_dist:
                min_dist = self.agent.dist_goal(person, self.agent.pos)

        if min_dist < 2:
            print("collision!!!")
            done = True

        #create observations
        obs = [self.goal, persons]

        return obs, 0, done, {}



    def render(self, mode='human'):
        """
        Used to render the screen
        """
        if self.setup:
            self.screen  = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            #self.screen = pygame.display.set_mode((self.size[0], self.size[1]))
            self.setup = False

        self.screen.fill((0,0,0))
        self._draw_agent()
        self._draw_goal()
        #self._draw_objects()
        self._draw_crowd()
        pygame.display.update()

        self.clock.tick(120)

    def reset(self):
        """
        Resets the enviornment to begin condition

        returns:
        initial observation
        """
        self.agent.pos = [self.size[0]/2, self.size[1]/2]

        x = np.random.randint(4)

        self.goal = self.goals[x]
        
        self.make_crowd()
        
        persons = [boid.position for crowd in self.crowds for boid in crowd]

        return [self.goal, persons]
    
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
        self.crowds = []

        variance_from_line = 300
        for _ in range(self.nr_crowds):
            r = np.random.randint(4)
            x, y = self.goals[r]

            if r == 0:
                x = np.random.randint(self.size[0])
                y = np.random.randint(y-variance_from_line, y+variance_from_line)
            
            if r == 1:
                x = np.random.randint(x-variance_from_line, x+variance_from_line)
                y = np.random.randint(self.size[1])
        
            if r == 2:
                x = np.random.randint(self.size[0])
                y = np.random.randint(y-variance_from_line, y+variance_from_line)

            if r == 3:
                x = np.random.randint(x-variance_from_line, x+variance_from_line)
                y = np.random.randint(self.size[1])


            goal = np.random.randint(4)
            new_crowd = [Boid(np.random.randint(x, x+100), np.random.randint(y,y+100), self.size[0], self.size[1], goal) for _ in range(10)]
            self.crowds.append(new_crowd)

    def _draw_agent(self):
        pygame.draw.circle(self.screen, (100,0,0), self.agent.pos, self.agent.start_push_dist)
        pygame.draw.circle(self.screen, (150,0,0), self.agent.pos, self.agent.close_push_dist)
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

    def _draw_crowd(self):
        for crowd in self.crowds:
            for boid in crowd:
                person = boid.position
                pygame.draw.circle(self.screen, (0,0,255), person, 3)
