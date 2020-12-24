import agents.agent 
from pygame.locals import (K_UP,K_DOWN,K_RIGHT,K_LEFT, KEYDOWN)
import pygame.event 
import numpy as np

class greedyAgent(agents.agent.agent):
    """
    manually controlled agent
    """


    def __init__(self,pos,size):
        super().__init__(pos,size) 
        self.moves = [[-1,0], [0,-1], [1,0], [0,1]] 
        self.name = "greedy"
    
    def step(self, move):
        self.update_pos(move)

    def generateMove(self, obs):
        goal, obstacles = obs
        obj_dist = 50


        goal_x, goal_y = goal
        pos_x, pos_y = self.pos

        a = np.arctan((goal_y -pos_y)/(goal_x-pos_x))
        x = np.cos(a)
        y = np.sin(a)

        if goal_x<pos_x:
            v1 = [-x,-y]
        else:
            v1 = [x,y]


        for obstacle in obstacles:
            if self.dist_goal(obstacle, self.pos) < 50:
                obstacle_x, obstacle_y = obstacle
                a = np.arctan((obstacle_y -pos_y)/(obstacle_x-pos_x))
                x = np.cos(a)
                y = np.sin(a)

                if obstacle_x < pos_x:
                    v2 = [-x*0.8,-y*0.8] 
                else:
                    v2 = [x*0.8,y*0.8] 
                
                v1 =[v1[0]-v2[0], v1[1]-v2[1]]

            
        
        v_x, v_y = v1

        magnitude = np.sqrt(v_x*v_x + v_y*v_y)

        norm_v1 = v1/magnitude


        return norm_v1

        # best_move = [0,0]
        # min_dist = inf
        
        #----Greedy tactic no obstacles---

        # for move in self.moves:
        #     dist = self.dist_goal(goal, [self.pos[0]+move[0], self.pos[1]+move[1]])
        #     if dist < min_dist:
        #         best_move = move
        #         min_dist = dist


        # for move in self.moves:
        #     dist = self.dist_goal(goal, [self.pos[0]+move[0], self.pos[1]+move[1]])
        #     dist_ok = self.distanceCheck(obstacles,  [self.pos[0]+move[0], self.pos[1]+move[1]], obj_dist)
        #     if dist < min_dist and dist_ok:
        #         best_move = move
        #         min_dist = dist

        # return best_move
    
    def distanceCheck(self, obstacles, pos, min_dist):
        for obstacle in obstacles:
            print(obstacle)
            if self.dist_goal(obstacle,pos) <= min_dist:
                return False          
        return True