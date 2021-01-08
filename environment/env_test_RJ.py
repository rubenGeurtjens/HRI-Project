import pygame
from agents import manualAgent, ppoAgent, greedyAgent
import numpy as np
from boids import Boid
import math

class env():

    def __init__(self):
        self.size = [600, 400]
        self.agent = ppoAgent.ppoAgent([200,300],[20,20])
        self.setup = True
        self.clock = pygame.time.Clock()

        self.nr_crowds = 3
        self.goals = [(100, 30), (500, 30), (100, 370), (500, 370)]
        self.objects = [[110,40], [80,30]]

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

        #for crowd in self.crowds:
        #    self.boid(crowd)

        self.agent.step(action)

        x,y = self.agent.get_pos()
       
        done = x < 0 or x > self.size[0] or y < 0 or y > self.size[1]

        dist = self.agent.dist_goal(self.goal)
            
        if dist < 25:
            print('finished')
            done = True
            reward = 200
        
        punishment = self._get_punish_boids(action)

        if self._get_closest_boid() <= 10:
            print('collision')
            reward = -1000 
            done = True  

        boids_pos = np.asarray([boid.position for crowd in self.crowds for boid in crowd])
        obs = np.concatenate((self.agent.get_pos(), self.goal))
        obs=np.concatenate((obs, self._get_closest_pos()))
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
        self._draw_crowd()

        pygame.display.update()
        
        #self.clock.tick(60)

    def reset(self):
        """
        Resets the enviornment to begin condition

        returns:
        initial observation
        """
        self.agent.pos = [300,200]

        x = np.random.randint(1)
        self.goal = self.goals[x]
        
        self._make_crowd()
        
        boids_pos = np.asarray([boid.position for crowd in self.crowds for boid in crowd])
        obs = np.concatenate((self.agent.get_pos(), self.goal))
        obs = np.concatenate((obs, self._get_closest_pos()))
        return obs

    def _get_punish_no_boids(self, action):
        reward = 0
        #if the current position is closed to the goal than the previous one give a reward
        curr_dist = self.agent.dist_goal(self.goal)
        self.agent.step([-action[0], -action[1]]) #move agent to previous location
        previous_dist = self.agent.dist_goal(self.goal)
        if curr_dist < previous_dist: 
            reward = 1
        self.agent.step(action) #move the agent back
        return reward 

    def _get_punish_boids(self, action):
        reward = self._get_punish_no_boids(action)
        dist = self._get_closest_boid()
        if dist <= 10:
            reward -= 50
        return reward 

    def _get_closest_boid(self):
        boids_pos = [boid.position for crowd in self.crowds for boid in crowd]
        min_dist = np.inf
        for pos in boids_pos:
            if self.agent.dist_goal(pos, self.agent.pos) < min_dist:
                min_dist = self.agent.dist_goal(pos, self.agent.pos)
        
        return min_dist

    def _get_closest_pos(self):
        boids_pos = [boid.position for crowd in self.crowds for boid in crowd]
        min_dist = np.inf
        closest = boids_pos[0]
        for pos in boids_pos:
            if self.agent.dist_goal(pos, self.agent.pos) < min_dist:
                min_dist = self.agent.dist_goal(pos, self.agent.pos)
                closest = pos 
        return np.asarray(closest,dtype='int32')

    # def _make_crowd(self):
    #     self.crowds = []

    #     variance_from_line = 300
    #     for _ in range(self.nr_crowds):
    #         r = np.random.randint(4)
    #         x, y = self.goals[r]

    #         if r == 0:
    #             x = np.random.randint(self.size[0])
    #             y = np.random.randint(y-variance_from_line, y+variance_from_line)
            
    #         if r == 1:
    #             x = np.random.randint(x-variance_from_line, x+variance_from_line)
    #             y = np.random.randint(self.size[1])
        
    #         if r == 2:
    #             x = np.random.randint(self.size[0])
    #             y = np.random.randint(y-variance_from_line, y+variance_from_line)

    #         if r == 3:
    #             x = np.random.randint(x-variance_from_line, x+variance_from_line)
    #             y = np.random.randint(self.size[1])


    #         goal = np.random.randint(4)
    #         new_crowd = [Boid(np.random.randint(x, x+100), np.random.randint(y,y+100), self.size[0], self.size[1], goal) for _ in range(10)]
    #         self.crowds.append(new_crowd)
    
    def _make_crowd(self):
        self.crowds = []
        x = np.random.randint(-25,25)
        y = np.random.randint(-10,10)
        b = Boid(130+x,70+y,10,10,1)
        self.crowds.append([b])

        x = np.random.randint(-50,50)
        y = np.random.randint(-50,50)
        b = Boid(200+x, 60+y,10,10,1)
        self.crowds.append([b])

        x = np.random.randint(-50,50)
        y = np.random.randint(-50,50)
        b = Boid(40+x, 90+y,10,10,1)
        self.crowds.append([b])


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

                distance = math.sqrt(dx * dx + dy * dy)
                dx /= distance
                dy /= distance

                x += dx
                y += dy

                boid.set_goal(dx, dy)
                boid.position += boid.velocity

    def _draw_agent(self):
        pygame.draw.circle(self.screen, (255,0,0), self.agent.pos, 3)

    def _draw_goal(self):
        x,y = self.goal
        rec = pygame.Rect(x-10,y-10,20,20)
        pygame.draw.rect(self.screen, (0,255,0), rec)

    
    def _draw_crowd(self):
        for crowd in self.crowds:
            for boid in crowd:
                person = boid.position
                pygame.draw.circle(self.screen, (0,0,255), person, 10)