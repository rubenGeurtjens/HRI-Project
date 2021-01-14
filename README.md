# Human Robot Interaction(HRI) -Project

## Goal
The agent should walk towards one of the 4 goals while keeping a person's social zones in mind. 

The final project contains 3 agents: 

1. Proximal Policy Optimization (PPO) agent
2. Q-Learning agent
3. Vector agent

## PPO
Runs in actor critic mode. Both the actor and critic have a small MLP (4 layers). The critic returns a value to give feedback on the actor. The actor returns a mu and sigma to construct the policy. The input tensor for both networks consists of the goal position and agent position. The policy is a Gaussian distribution from which actions are sampled. Training is very slow, and hyperparameters and a reward function need to be tuned in order for it to work properly. 

## Q-Learning agent
We have 2 different modes of q-learning
1. Big, general view: if there are no persons within a predifined distance
2. Small, precize view: if there is a person or goal within a predifined distance 

When in big view the agent is able to see more, since each cell in the observation spans multiple pixels. In small view, the agent is able to see less far, but every cell is one pixel, meaning it can make very precise movement to avoid people. 

Because the environment is dynamic it is slow, since we need to recompute the q-table every step. There are a variety of ways we can speed it up. We tried to skip frames when the agent is in "big view mode". This means the agent will repeat the same action as it previously did if no persons are within its big view. Some other thing we haven't done, but could help are to carefully construct the observations, which can help with making the q-table converge faster.

## Vector agent
Constant vector which pushes the agent towards the goal. The person that is closest to the agent gives a repelling force, which causes it to change its movement. 

## Environments 
Each agent has its own environment. Each environment consists of 3 "main" functions, created in a similar way OpenAI does it. 

1. step 
2. reset
3. render

The *step* function contains the main logic and is responsible to do all calculations and move the agent and persons. 
The *reset* function resets the agent,persons and all other things that need to be reset. This function is called every time the agent "dies" or reseaches the goal.
The *render* function renders everything using PyGame so that visible inspection is possible. Not rendering does make learning faster 





