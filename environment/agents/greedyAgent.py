import agents.agent 
from pygame.locals import (K_UP,K_DOWN,K_RIGHT,K_LEFT, KEYDOWN)
import pygame.event 

class manualAgent(agents.agent.agent):
    """
    manually controlled agent
    """

    def __init__(self,pos,size):
        super().__init__(pos,size) 
    
    def step(self, move):
        self.update_pos(move)

    def generateMove(self, obs):
        
        return move