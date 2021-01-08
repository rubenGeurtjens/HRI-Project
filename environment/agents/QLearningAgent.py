import agents.agent 
import pygame.event 
import numpy as np
import random 

class QLearningAgent(agents.agent.agent):
    """
    Q-learning agent
    """
    def __init__(self,pos,size,dim):
        super().__init__(pos,size) 
        self.name = "Q-learning agent"
        self.q_table = np.zeros((dim*dim, 4)) #20x20 pixels and 4 actions 
        self.dim = dim

        #hyperparamaters
        self.alpha = 0.1
        self.gamma = 0.6
        self.epsilon = 0.3

        self.iterations = 1000


    def step(self, move):
        self.update_pos(move)

    def generateMove(self, obs):
        #obs = matrix van nullen en +1 als het goal is en -1 als het vijand is
        self.q_table = np.zeros([21*21, 4]) #20x20 pixels and 4 actions 
        for i in range(self.iterations): #training cycles 
            startX, startY = int((self.dim-1)/2), int((self.dim-1)/2)
            x,y= int((self.dim-1)/2), int((self.dim-1)/2)
            done = False 
            max_steps = 250
            nr_steps = 0
            while not done:
                state = x*(self.dim-1) + y
                if random.uniform(0,1) < self.epsilon:
                    action = np.random.randint(4)
                else:
                    is_all_zero = np.all((self.q_table[state] == 0))
                    if is_all_zero:
                        action = np.random.randint(4)
                    else:
                        action = np.argmax(self.q_table[state])


                #0=left, 1=up, 2=right, 3=down
                if action == 0 and y>0 and obs[x,y-1] != -10: #no move outside the grid(y>0) and -10 means no outside grid in the "real" world
                    y -= 1 
                elif action == 1 and x>0 and obs[x,y-1] != -10:
                    x -= 1 
                elif action == 2 and y<self.dim-1 and obs[x,y-1] != -10:
                    y += 1
                elif action == 3 and x<self.dim-1 and obs[x,y-1] != -10:
                    x += 1

                reward = obs[x,y] 
                old_value = self.q_table[state, action]
                next_state = x*(self.dim-1) + y
                next_max = np.max(self.q_table[next_state])
                
                new_value = (1 - self.alpha) * old_value + self.alpha * (reward + self.gamma * next_max) #q-table update 
                self.q_table[state, action] = new_value
                state = next_state
                nr_steps += 1

                #if obs[x,y] == 1:
                #    print('goal found')

                done = obs[x,y] == 1 or nr_steps >= max_steps

        action = np.argmax(self.q_table[startX*(self.dim-1) + startY])  
        #print(f'action: {action} {np.random.randint(1000)}')      
        if action == 0:
            return [-1,0]
        elif action == 1:
            return [0,-1]
        elif action == 2:
            return [1,0]
        elif action == 3:
            return [0,1]

    def set_q_table(self, dim):
        self.q_table = np.zeros((dim,dim))
        self.dim = dim