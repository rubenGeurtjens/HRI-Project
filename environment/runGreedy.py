from environments import env_forces
import torch 
import csv

if __name__ == '__main__':
    filename = 'forces_agent_10_crowds.csv'
    with open(filename, 'a') as f:
               writer = csv.writer(f)
               writer.writerow(['run', 'steps', 'collisions', 'intimate', 'close intimate', 'person', 'social', 'public'])

    nr_steps = 0
    nr_finishes = 0
    max_finishes = 499
    env = env_forces.env()
    obs = env.reset()
    while nr_finishes < max_finishes:
        nr_steps += 1
        action = env.agent.generateMove(obs)
        obs, _, done, _  = env.step(action)
        env.render()

        if done:
            with open(filename, 'a') as f:
                writer = csv.writer(f)
                writer.writerow([nr_finishes, nr_steps, env.nr_collisions, env.nr_intimate_zone, \
                    env.nr_close_intimate_zone, env.nr_personal_zone, env.nr_social_zone, env.nr_public_zone])
            nr_finishes += 1
            nr_steps = 0
            env.reset()