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

        self.goal = [200,200]
        self.close_view = 3
        self.block_size = 20 #pixels per block
        self.nr_blocks = 3 #number of blocks on each side of the agent 
        self.agent = QLearningAgent.QLearningAgent([114,35],[3,3], 2*self.close_view+1)
        #boids
        self.nr_crowds = 5
        self.goals = [[100,100], [self.size[0]-100,100], [self.size[0]-100,self.size[1]-100], [100,self.size[1]-100]]

        self.skip_frame = False #only true when count % modulo 2 == 0
        self.prev_action = 0 #used to store previous action
        self.count = 0 #used to determine when to skip a frame(speed up q-learning)


        #checking social distance
        self.nr_collisions = 0
        self.nr_intimate_zone = 0
        self.nr_close_intimate_zone = 0
        self.nr_personal_zone = 0
        self.nr_social_zone = 0
        self.nr_public_zone = 0


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

        for crowd in self.crowds:
            self.boid(crowd)

        self.agent.step(action) 

        done =  self.agent.pos == self.goal 

        x,y = self.agent.pos 
        x2,y2 = self.goal

        close_x,close_y = self._get_closest_pos()
        
        #agent checks if its need the small or big view depending on closeness of other persons and goal
        #use small if goal or person is within blocksize
        use_small = (abs(x-x2) <= self.block_size and abs(y-y2) <= self.block_size) or (abs(x-close_x) <= self.block_size and abs(y-close_y) <= self.block_size)
        use_small = True
        if use_small:
            self.skip_frame =  False #no skipping frames when in small mode
            self.agent.iterations = 800 #change the amount of iterations to ensure that the agent does not crash

            self.agent.set_q_table(2*self.close_view+1) #change the size of the q-table depending on the view mode
            obs = np.zeros((2*self.close_view+1,2*self.close_view+1)) #look at every dicrection close_view pixels
            obs = self._add_persons_small(obs)#add all persons to the observation
            obs = self._add_goal_small(obs)#add the goal to the observation, if goal is outside of the view we map it to observation so that the agent still knowns in which direciton to travel
        else:
            self.skip_frame =  self.count % 2 == 0 #agent can skip frame if in big frame to speed up computations 
            self.agent.iterations = 200

            self.agent.set_q_table(self.nr_blocks*2+1)
            obs = np.zeros((2*self.nr_blocks+1, 2*self.nr_blocks+1))
            obs = self._add_persons_large(obs)
            obs = self._add_goal_large(obs)

        persons = [boid.position for crowd in self.crowds for boid in crowd]

        #checks for closeness in persons space  
        for person in persons:
            dist = self.agent.dist_goal(person,self.agent.pos)
            if dist == 0:
                self.nr_collisions+=1
            elif dist <= 3:
                self.nr_intimate_zone += 1
            elif dist <= 9:
                self.nr_close_intimate_zone += 1
            elif dist <= 24:
                self.nr_personal_zone += 1
            elif dist <= 72:
                self.nr_social_zone += 1
            elif dist < 2000:
                self.nr_public_zone += 1

        self.count += 1
        self.prev_action = action #storing previous action so that the agent can repeat it when skipping a frame 
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
        self._draw_crowd()
        self._draw_goal()

        pygame.display.update()

       # self.clock.tick(20) #used to controll FPS 

    def reset(self):
        """
        Resets the enviornment to begin condition

        returns:
        initial observation
        """
        #resetting all counts 
        self.nr_collisions = 0
        self.nr_intimate_zone = 0
        self.nr_close_intimate_zone = 0
        self.nr_personal_zone = 0
        self.nr_social_zone = 0
        self.nr_public_zone = 0


        self.make_crowd()
        self.count = 0
        
        x,y = self.size[0]/2, self.size[1]/2 #reset agent to the middle 
        self.agent.pos = [x, y]
        self.goal = self.goals[np.random.randint(4)]
        x2,y2 = self.goal

        #again checking if the agent should use close or big view
        close_x,close_y = self._get_closest_pos()
        use_small = (abs(x-x2) and abs(y-y2) <= self.block_size) or (abs(x-close_x) < self.block_size and abs(y-close_y) < self.block_size)
        if use_small: 
            self.agent.set_q_table(2*self.close_view+1)
            obs = np.zeros((2*self.close_view+1,2*self.close_view+1)) #look at every dicrection 
            obs = self._add_persons_small(obs) 
            obs = self._add_goal_small(obs) 
        else:
            self.agent.set_q_table(self.nr_blocks*2+1) 
            obs = np.zeros((2*self.nr_blocks+1, 2*self.nr_blocks+1))
            obs = self._add_persons_large(obs)
            obs = self._add_goal_large(obs)
        
        return obs

    def _get_closest_pos(self):
        """
        Gets the position of the closest boid(person) 
        """
        boids_pos = [boid.position for crowd in self.crowds for boid in crowd]
        min_dist = np.inf
        closest = boids_pos[0]
        for pos in boids_pos:
            if self.agent.dist_goal(pos, self.agent.pos) < min_dist:
                min_dist = self.agent.dist_goal(pos, self.agent.pos)
                closest = pos 
        return np.asarray(closest,dtype='int32')


    def _add_goal_small(self, obs):
        """
        Adds the goal to the observation of the agent if in small view mode
        """
        x,y = self.agent.get_pos()       
        x2,y2=self.goal 
        
        #middle punt of the grid is the agent
        obs[self.close_view,self.close_view] = 0
        #if goal in reach
        if abs(x-x2) <= self.close_view and abs(y-y2) <= self.close_view: #f the goal is within close view add it directly 
            obs[int(y2-y+self.close_view), int(x2-x+self.close_view)] = 1
        else: #if the agent can't see the goal add it to the outside. If we don't do this the agent doesn't know where to go since there is no goal
            a,b=self._get_small_goal_pos() 
            obs[b,a] = 1
        return obs


    def _add_goal_large(self, obs):
        """
        Adds the coordinates of the goal to the observation. 
        Maps the goalcoordinates to the correct observation cell depending on the blocksize etc. 
        """
        x,y = self._get_large_goal_pos()
        obs[y,x] = 1

        obs[self.nr_blocks, self.nr_blocks] = 0
        return obs

    def _get_small_goal_pos(self):
        """
        Returns the goal position mapped to coordinates of the observation matrix if the small-view agent can't see the goal. 
        """
        x,y = self.agent.pos 
        x2,y2 = self.goal 

        dx = x-x2
        dy = y-y2 

        x_inrange = abs(x-x2) < (self.close_view + 1) 
        y_inrange = abs(y-y2) < (self.close_view + 1)
                    
        if not x_inrange:
            if x2 < x: 
                dx = (self.close_view + 1)
                dx -= 1
            else:
                dx = (self.close_view + 1) * -1
                dx += 1
        
        if not y_inrange:
            if y2 < y: 
                dy = (self.close_view + 1)
                dy -= 1
            else:
                dy = (self.close_view + 1)  * -1
                dy += 1        

        our_x =self.close_view #agent is always in the middle of the observation 
        our_y =self.close_view 
        return int(our_x-dx), int(our_y-dy) 

    
    def _get_large_goal_pos(self):
        """
        Returns the goal position mapped to coordinates of the observation matrix if the big-view agent can't see the goal. 
        """

        x,y = self.agent.pos 
        x2,y2 = self.goal 

        dx = x-x2
        dy = y-y2 

        #check if agent can see the goal 
        x_inrange = abs(x-x2) < (self.nr_blocks + 1)* self.block_size 
        y_inrange = abs(y-y2) < (self.nr_blocks + 1)* self.block_size 
        
        #if the agent can't see the goal in its x-coordinate we map it so that it still appears in the observation matrix
        if not x_inrange:
            if x2 < x: 
                dx = (self.nr_blocks + 1)* self.block_size 
                dx -= 1
            else:
                dx = (self.nr_blocks + 1)* self.block_size * -1
                dx += 1
        #Same for the y-coordinate 
        if not y_inrange:
            if y2 < y: 
                dy = (self.nr_blocks + 1)* self.block_size 
                dy -= 1
            else:
                dy = (self.nr_blocks + 1)* self.block_size * -1
                dy += 1        


        our_x =self.nr_blocks #agent is always in the middle of the observation 
        our_y =self.nr_blocks

        #map the coordinates to the correct cell. Each cell is has a length of block_size 
        dx = dx / self.block_size
        dy = dy / self.block_size
        if dx>0:
            dx = math.floor(dx)
        else:
            dx = math.ceil(dx) 
        if dy>0:
            dy = math.floor(dy)
        else:
            dy = math.ceil(dy)
        return our_x-dx, our_y-dy
    
    def _add_persons_small(self, obs):
        """
        Adds all persons to the corresponding cell in the observation matrix for the small-view agent.
        Only does this if the agent can see the person
        """
        persons = [boid.position for crowd in self.crowds for boid in crowd] #get all coordinates of the persons
        for p in persons: 
            x,y = self.agent.pos 
            x2,y2 = p

            dx = x-x2
            dy = y-y2 

            #check if the agent can see the person
            x_inrange = abs(x-x2) < (self.close_view + 1) 
            y_inrange = abs(y-y2) < (self.close_view + 1)
                        
            #if not continue 
            if not x_inrange or not y_inrange:
                continue 
            #otherwise we can simply add it 
            our_x =self.close_view
            our_y =self.close_view
            
            obs[int(our_y-dy),int(our_x-dx)] = -1
        return obs

    def _add_persons_large(self, obs):
        """
        Adds all persons to the corresponding cell in the observation matrix for the big-view agent.
        Only does this if the agent can see the person
        """
        persons = [boid.position for crowd in self.crowds for boid in crowd]
        for p in persons: 
            x,y = self.agent.pos 
            x2,y2 = p

            dx = x-x2
            dy = y-y2 

            #again check if agent can see the person
            x_inrange = abs(x-x2) < (self.nr_blocks + 1)* self.block_size 
            y_inrange = abs(y-y2) < (self.nr_blocks + 1)* self.block_size 
                        
            if not x_inrange or not y_inrange:
                continue        

            #map the persons coordinates to the coordinates of the agent
            #where each cell in the observation matrix has a length of block_size 
            our_x =self.nr_blocks #agent is always in the middle of the observation 
            our_y =self.nr_blocks

            dx = dx / self.block_size
            dy = dy / self.block_size
            if dx>0:
                dx = math.floor(dx)
            else:
                dx = math.ceil(dx) 
            if dy>0:
                dy = math.floor(dy)
            else:
                dy = math.ceil(dy)
            
            obs[our_y-dy,our_x-dx] = -1
        return obs


    def boid(self, crowd):
        for boid in crowd:

            # Vector from me to cursor
            goalX, goalY = self.goals[boid.goalNr]
            x, y = boid.position

            if (goalX + 10  >= x >= goalX - 10) and (goalY + 10  >= y >= goalY - 10):
                boid.reached_goal(goalX + 10, goalY + 10)
                boid.position = Vector2(-100000, -100000)

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
        """
        Creates all the persons
        The groups of persons spawn at 4 random location with some variance 
        Each group also gets a goal to which they have to move towards. 
        """
        self.crowds = []

        variance_from_line = 50
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
        """
        draws the agent to the screen 
        """
        x,y = self.agent.pos
        rec_big = pygame.Rect(x - (self.nr_blocks*2+1)*self.block_size/2, y- (self.nr_blocks*2+1)*self.block_size/2, (self.nr_blocks*2+1)*self.block_size, (self.nr_blocks*2+1)*self.block_size)
        rec_small = pygame.Rect(x - (self.close_view*2+1)/2, y-(self.close_view*2+1)/2, (self.close_view*2+1), (self.close_view*2+1))
        pygame.draw.rect(self.screen, (100,0,0), rec_big)
        pygame.draw.rect(self.screen, (170,0,0), rec_small)
        pygame.draw.circle(self.screen, (255,0,0), self.agent.pos, 1)
    
    def _draw_goal(self):
        for goal in self.goals:
            x,y = goal
            rec = pygame.Rect(x-10,y-10,20,20)
            pygame.draw.rect(self.screen, (0,100,0), rec)

        x,y = self.goal
        rec = pygame.Rect(x-10,y-10,20,20)
        pygame.draw.rect(self.screen, (0,255,0), rec)


    def _draw_crowd(self):
        for crowd in self.crowds:
            for boid in crowd:
                person = boid.position
                pygame.draw.circle(self.screen, (0,0,255), person, 1)
