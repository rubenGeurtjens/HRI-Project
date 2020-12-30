import env_OPENAI

import gym
import math
from stable_baselines.common.policies import MlpPolicy
from stable_baselines.common import make_vec_env
from stable_baselines import PPO2

if __name__ == '__main__':
    env = env_OPENAI.env()

    model = PPO2(MlpPolicy, env, n_steps=512, verbose=1)
    model.learn(total_timesteps=1000000)

    obs = env.reset()
    while True:
        action, _states = model.predict(obs)
        obs, _, done, _  = env.step(action)
        env.render()
        if done:
            env.reset()