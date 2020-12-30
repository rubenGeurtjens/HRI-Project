import agents.agent 
from pygame.locals import (K_UP,K_DOWN,K_RIGHT,K_LEFT, KEYDOWN)
import pygame.event 
import numpy as np

class greedyAgent(agents.agent.agent):
    """
    manually controlled agent
    """


    def __init__(self,pos,size,start_push=100, close_push_dist=50):
        super().__init__(pos,size) 
        self.name = "greedy"
        self.start_push_dist = start_push
        self.close_push_dist = close_push_dist
    
    def step(self, move):
        self.update_pos(move)

    def generateMove(self, obs):
        """
        Generates the next move of the agent.
        The move returned is a vector of length 1 in the desired direction
        """
        #unpack observation
        goal, obstacles = obs

        v1 = self.vector_to_goal(goal)

        closest_obstacle = self.get_closest_obstacle(obstacles)
        

        x,y = self.vector_from_obstacle(closest_obstacle)
        
        push_strength = self.get_push_strength(closest_obstacle)
        

        pos_x, _ = self.pos
        obstacle_x, _ = closest_obstacle

        if obstacle_x < pos_x:
            v2 = [-x*push_strength,-y*push_strength] 
        else:
            v2 = [x*push_strength,y*push_strength] 
        
        #construct final vector and normalize
        v =[v1[0]-v2[0], v1[1]-v2[1]]
        v_x, v_y = v
        magnitude = np.sqrt(v_x*v_x + v_y*v_y)
        norm_v = v/magnitude

        return norm_v
    
    def vector_to_goal(self, goal):
        """
        calculates vector of maginitude one towards goal from agent pos
        """
        goal_x, goal_y = goal
        pos_x, pos_y = self.pos

        a = np.arctan((goal_y -pos_y)/(goal_x-pos_x))
        x = np.cos(a)
        y = np.sin(a)

        if goal_x<pos_x:
            return [-x,-y]
        else:
            return [x,y]
    
    def get_closest_obstacle(self, obstacles):
        min_dist = np.inf
        for obstacle in obstacles:
            if self.dist_goal(obstacle, self.pos) < min_dist:
                min_dist = self.dist_goal(obstacle, self.pos)
                closest_obstacle = obstacle
        
        return closest_obstacle
    
    def vector_from_obstacle(self, closest_obstacle):
        pos_x, pos_y = self.pos
        obstacle_x, obstacle_y = closest_obstacle
        a = np.arctan((obstacle_y -pos_y)/(obstacle_x-pos_x))
        x = np.cos(a)
        y = np.sin(a)
        return(x,y)
    
    def get_push_strength(self, closest_obstacle):
        """
        Calculates the amount of required push strength based on the distance to the closest obstacle
        """
        #strength of inner cirlce
        if self.close_push_dist > self.dist_goal(closest_obstacle, self.pos):
            return 10*(1 - 1/self.close_push_dist * self.dist_goal(closest_obstacle, self.pos))


        # strength of outer circle
        elif self.start_push_dist > self.dist_goal(closest_obstacle, self.pos):
            return 3*(1 - 1/self.start_push_dist * self.dist_goal(closest_obstacle, self.pos)) 
        
        else:
            return 0
