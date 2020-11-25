import time
import numpy as np
import torch
import torch.nn as nn
from torch.optim import Adam
from torch.nn import functional as F
import numpy as np
from torch.utils.data.sampler import BatchSampler, SubsetRandomSampler
import math
import os

class PPO():
    """
    Class that contains the logic behind the proximal policy algorithm that was developed by openAI
    """

    def __init__(self, policy, optimizer, batch_size, nupdates, coeff_entropy=0.02, clip_value=0.2):
        """
        Constructur of the PPO class

        #Parameters:
            policy: A neural network that represents the policy
            optimizer: Optimizer that optimizes the policy
            bach_size(int): The batch_size used when updating the policy
            nupdates(int): Number of epochs that the algorithm should perform
            clip_value(int): The clip value that clips the surrogate loss function
        
        #Returns
            nothing
        """

        self.policy = policy
        self.optimizer = optimizer
        self.batch_size = batch_size
        self.nupdates = nupdates
        self.coeff_entropy = coeff_entropy
        self.clip_value = clip_value

    def update(self, memory):
        """
        Performs nupdates on the policy using the memory that was collected during the episode

        #Parameters
            memory(tuple): A tuple contain all actions, observation,values and log probablities of these actions that were collected during an episode
        #Return
            value_loss(float): the value loss 
            policy_loss(float): the policy loss
            entropy_loss(float): the entropy bonus
        """
        #unpacking memory
        actions, obs, values, logprobs, returns = memory

        #normalizing the advantages
        advantages = returns - values
        advantages = (advantages - advantages.mean()) / advantages.std() 
        
        for update in range(self.nupdates):
            #creating minibatches from the trajectory
            batch_sampler = BatchSampler(SubsetRandomSampler(list(range(len(advantages)))), batch_size=self.batch_size, drop_last=False)
            for _, indexes in enumerate(batch_sampler):
                sampled_obs = torch.from_numpy(obs[indexes]).float().cuda()
                sampled_actions = torch.from_numpy(actions[indexes]).float().cuda()
                sampled_logprobs = torch.from_numpy(logprobs[indexes]).float().cuda()
                sampled_returns = torch.from_numpy(returns[indexes]).float().cuda()
                sampled_advs = torch.from_numpy(advantages[indexes]).float().cuda()

                new_value, new_logprob, dist_entropy = self.policy.evaluate_actions(sampled_obs, sampled_actions)

                sampled_logprobs = sampled_logprobs.view(-1, 1)
                ratio = torch.exp(new_logprob - sampled_logprobs)

                sampled_advs = sampled_advs.view(-1, 1)

                #####################################################
                # performing the updates according to the PPO paper #
                #####################################################

                #getting the actors loss
                loss1 = ratio * sampled_advs
                loss2 = torch.clamp(ratio, 1 - self.clip_value, 1 + self.clip_value) * sampled_advs
                policy_loss = torch.min(loss1, loss2)
                policy_loss = -policy_loss.mean()

                #getting the critics loss
                sampled_returns = sampled_returns.view(-1, 1)
                l1_loss = torch.nn.SmoothL1Loss()
                value_loss = l1_loss(new_value, sampled_returns)
                
                #adding a small entropy bonus to encourage exploration
                loss = policy_loss + value_loss - self.coeff_entropy * dist_entropy
                self.optimizer.zero_grad()
                loss.backward()
                self.optimizer.step()

        return value_loss.data.item(), policy_loss.data.item(), dist_entropy.data.item()

    def generate_episode(self, env, max_step, should_render=False):
        """
        Generates an episode using the current policy 

        #Parameters 
            env: The env in which the agent should perform the actions
            max_step(int): The number of steps the agent should perform
            should_render(bool): Wether the environment should be rendered
        
        #Returns
            observations(numpy array): all observations the agent encoutered
            actions(numpy array): all actions the agent took
            logprobs(numpy array): all the log probabilities of these action
            returns(numpy array): the n_step estimate 
            values(numpy array): all the values the critic gave
            rewards(numpy array): all the rewards the agent collected
        """

        obs = env.reset()
        done = False

        observations = []
        values = []
        logprobs = []
        rewards = []
        actions = []
        dones = []

        for i in range(max_step):
            if done:
                obs = env.reset()
            if should_render:
                env.render()

            obs = torch.from_numpy(obs).float().cuda() 
            obs = obs.unsqueeze(0) #adding batch dimension
            value, action, logprob, mu = self.policy(obs) 
            value = value.item() 
            logprob = logprob.data.cpu().numpy()[0] #can't use .item() since there can be multiple values in the tensor
            action = action.data.cpu().numpy()[0]

            x = math.cos(action) 
            y = math.sin(action)

            next_obs, reward, done, info = env.step([x,y])

            observations.append(obs.data.cpu().numpy()[0])
                       
            dones.append(done)
            rewards.append(reward)
            logprobs.append(logprob)
            actions.append(action)
            values.append(value)

            obs = next_obs

        if done:
            last_value = 0.0
        else:
            obs = torch.from_numpy(obs).float().cuda()
            obs = obs.unsqueeze(0)
            value, action, logprob, mu = self.policy(obs)
            last_value = value.data[0][0]

        observations = np.asarray(observations)
        rewards = np.asarray(rewards)
        logprobs = np.asarray(logprobs)
        actions = np.asarray(actions)
        dones = np.asarray(dones)
        dones = 1 - dones
        values = np.asarray(values)

        returns = self.n_step_return(dones, rewards, last_value, 0.99)
        return observations, actions, logprobs, returns, values, rewards

    def n_step_return(self, dones, rewards, last_value, gamma):
        returns = np.zeros(rewards.shape[0] + 1)
        returns[-1] = last_value
        for i in reversed(range(len(rewards))):
            returns[i] = gamma * returns[i+1] * dones[i] + rewards[i]
        return returns[:-1]