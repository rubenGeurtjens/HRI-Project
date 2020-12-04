
import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
import math 

class MLP(nn.Module):
    """
    MLP ActorCritic class in PPO network i.e decides which actions to take and returns the critic value
    input should be: [Batch, Channels, Height, Width]
    n_input_channels: n_inputs channels of input (3 for rgb image)
    n_outputs: number of actions normal distribution should have. 
    returns: value scaler, matrix of mu,sigma
    """
    def __init__(self, obs_space, action_space):
        super(MLP, self).__init__()
        # action network
        self.act_fc1 = nn.Linear(obs_space, 24)
        #self.act_fc2 = nn.Linear(84, 168)
        self.mu = nn.Linear(24, action_space)
        self.mu.weight.data.mul_(0.1)

        #paramater so if MLP goes to GPU it joins
        self.logstd = nn.Parameter(torch.zeros(action_space))

        self.value_fc1 = nn.Linear(obs_space, 84)
        self.value_fc2 = nn.Linear(84, 168)
        self.value_fc3 = nn.Linear(168, 1)
        self.value_fc3.weight.data.mul(0.1)

    def forward(self, x):
        act = self.act_fc1(x)
        act = torch.relu(act)
        #act = self.act_fc2(act)
        #act = torch.relu(act)
        mean = self.mu(act) 
        logstd = self.logstd.expand_as(mean)
        std = torch.exp(logstd)
        action = torch.normal(mean, std)

        v = self.value_fc1(x)
        v = torch.relu(v)
        v = self.value_fc2(v)
        v = torch.relu(v)
        v = self.value_fc3(v)

        logprob = self.log_normal_density(action, mean, std=std, log_std=logstd)
        return v, action, logprob, mean
    
    def evaluate_actions(self, x, action):
        v, _, _, mean = self.forward(x)
        logstd = self.logstd.expand_as(mean)
        std = torch.exp(logstd)
        logprob = self.log_normal_density(action, mean, log_std=logstd, std=std)
        dist_entropy = 0.5 + 0.5 * math.log(2 * math.pi) + logstd
        dist_entropy = dist_entropy.sum(-1).mean()
        return v, logprob, dist_entropy
        
    def log_normal_density(self, x, mean, log_std, std):
        """returns guassian density given x on log scale"""
        variance = std.pow(2)
        log_density = -(x - mean).pow(2) / (2 * variance) - 0.5 * np.log(2 * np.pi) - log_std
        log_density = log_density.sum(dim=1, keepdim=True)
        return log_density