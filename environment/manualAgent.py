import agent 
from pygame.locals import (K_UP,K_DOWN,K_RIGHT,K_LEFT, KEYDOWN)
import pygame.event 

class manualAgent(agent.agent):
    """
    manually controlled agent
    """

    def __init__(self,pos,size):
        super().__init__(pos,size) 
    
    def step(self, move):
        keys = pygame.key.get_pressed()
        if(keys[pygame.K_DOWN]):
            print("HALLO")
            self.update_pos([0,-1])
        elif(keys[K_DOWN]):
            self.update_pos[0,1]
        elif(keys[K_LEFT]):
            self.update_pos[-1,0]
        elif(keys[K_RIGHT]):
            self.update_pos[1,0]