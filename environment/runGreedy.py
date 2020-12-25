import env_test_RJ
import torch 

if __name__ == '__main__':

    env = env_test_RJ.env()
    obs = env.reset()
    while True:
        action = env.agent.generateMove(obs)
        obs, _, done, _  = env.step(action)
        env.render()

        if done:
            env.reset()