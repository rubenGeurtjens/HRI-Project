import env_QLearning

if __name__ == '__main__':
    env = env_QLearning.env()
    obs = env.reset()
    while True:
        action = env.agent.generateMove(obs)
        obs, _, done, _  = env.step([0,0])
        env.render()
        if done:
            env.reset()