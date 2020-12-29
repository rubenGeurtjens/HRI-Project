import env_forces
import torch 

if __name__ == '__main__':

    env = env_forces.env()
    obs = env.reset()
    while True:
        action = env.agent.generateMove(obs)
        obs, _, done, _  = env.step(action)
        env.render()

        if done:
            env.reset()