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
        observation,reward,done and info
        """
        pass

    def render(self, mode='human'):
        """
        Used to render the screen 
        """
        pass 

    def reset(self):
        """
        Resets the enviornment to begin condition
        
        returns:
        initial observation
        """
        pass 

env = env()
obs = env.reset()
done = False
while True:
    env.render()
    env.step(0)
    if done:
        env.reset()
