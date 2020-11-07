from abc import ABC, abstractmethod #need to create abstract class 

class agent(ABC):
    """
    Abstract class for the agent.
    Is used the human controlled agent and PPO-agent
    """
    def __init__(self, pos,size):
        self.pos = pos 
        self.size = size 

    @abstractmethod
    def step(self, *args):
        pass 

    def update_pos(self, new_pos):
        self.pos[0] += new_pos[0]
        self.pos[1] += new_pos[1]
    
