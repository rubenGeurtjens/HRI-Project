import pygame
from agents import manualAgent 


class env():
    
    def __init__(self):
        self.size = [600, 400]
        self.agent = manualAgent.manualAgent([400,300],[20,20])
        self.setup = True 
        self.goal = [290,50]
        self.clock = pygame.time.Clock()


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
        self.agent.step(1)
        return self.goal, 10, False, {}

    def render(self, mode='human'):
        """
        Used to render the screen 
        """
        if self.setup:
            self.screen = pygame.display.set_mode((self.size[0], self.size[1]))
            self.setup = False 
        
        self.screen.fill((0,0,0))
        self._draw_agent()
        self._draw_goal()
        pygame.display.update()

        print(self.agent.dist_goal(self.goal))

        self.clock.tick(60)

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
while True:
    env.render()
    obs, r, done, info = env.step(0)
    if done:
        env.reset()
