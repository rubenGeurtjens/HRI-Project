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
        pygame.event.get()
        keys = pygame.key.get_pressed()
        if(keys[K_UP]):
            self.update_pos([0,-1])
        if(keys[K_DOWN]):
            self.update_pos([0,1])
        if(keys[K_LEFT]):
            self.update_pos([-1,0])
        if(keys[K_RIGHT]):
            self.update_pos([1,0])