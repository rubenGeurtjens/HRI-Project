import pygame
import manualAgent

class env():
    
    def __init__(self):
        self.size = [600, 400]
        self.agent = manualAgent.manualAgent([0,0],[400,400])

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
