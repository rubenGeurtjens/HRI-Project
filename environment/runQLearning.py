import env_QLearning

if __name__ == '__main__':
    env = env_QLearning.env()
    obs = env.reset()
    while True:
        if env.skip_frame:
            action = env.prev_action
        else:
            action = env.agent.generateMove(obs)
        obs, _, done, _  = env.step(action)
        env.render()
        if done:
            env.reset()