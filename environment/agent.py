from abc import ABC, abstractmethod #needed to create abstract class 

class agent(ABC):
    """
    Abstract class for the agent.
    Is used in the human controlled agent and PPO-agent
    """
    def __init__(self, pos,size):
        self.pos = pos 
        self.size = size 

    @abstractmethod
    def step(self, action):
        pass 

    def update_pos(self, new_pos):
        self.pos[0] += new_pos[0]
        self.pos[1] += new_pos[1]
    
    def get_pos(self):
        return self.pos
    
    def get_size(self):
        return self.size
