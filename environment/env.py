import pygame
import humanAgent

class env():
    
    def __init__(self):
        self.size = [600, 400]
        self.agent = humanAgent.humanAgent([0,0],[400,400])

    def step(self, action):
        """
        Performs one update step 
        and contains the main logic

        returns:
        obs,reward,done,info
        """
        pass

    def render(self, mode='human'):
        """
        Used to render the screen 
        """
        pass 

    def reset(self):
        """
        Resets the enviornment. For instance:
        reset agent and objects 
        """
        pass 

env = env()
