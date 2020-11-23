import pygame
import humanAgent

class env():
    
    def __init__(self):
        self.size = [600, 400]
        self.agent = humanAgent.humanAgent([400,300],[20,20])
        self.setup = True 
        self.goal = [290,50]
        

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
        if self.setup:
            self.screen = pygame.display.set_mode((self.size[0], self.size[1]))
            self.setup = False 
        
        self._draw_agent()
        self._draw_goal()
        pygame.display.update()


    def reset(self):
        """
        Resets the enviornment to begin condition
        
        returns:
        initial observation
        """
        pass 

    def _draw_agent(self):
        x,y = self.agent.get_pos()
        w,h = self.agent.get_size()
        rec = pygame.Rect(x,y,w,h)
        pygame.draw.rect(self.screen, (255,0,0), rec)
    
    def _draw_goal(self):
        x,y = self.goal 
        rec = pygame.Rect(x,y,20,20)
        pygame.draw.rect(self.screen, (0,255,0), rec)

env = env()
obs = env.reset()
done = False
while True:
    env.render()
    env.step(0)
    if done:
        env.reset()
