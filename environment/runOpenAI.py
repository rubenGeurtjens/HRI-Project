import env_OPENAI

import gym
import math
from stable_baselines.common.policies import MlpPolicy
from stable_baselines.common import make_vec_env
from stable_baselines import PPO2
from stable_baselines.common.env_checker import check_env

if __name__ == '__main__':
    env = env_OPENAI.env()
    check_env(env)

    model = PPO2(MlpPolicy, env, n_steps=512, verbose=1)
    model.learn(total_timesteps=250000)

    obs = env.reset()
    while True:
        action, _states = model.predict(obs)
        obs, _, done, _  = env.step(action)
        env.render()
        if done:
            env.reset()