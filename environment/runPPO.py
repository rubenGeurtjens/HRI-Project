import env_test_RJ
from agents.PPO import ActorCritic, ppo
from torch.optim import Adam
import torch 

if __name__ == '__main__':
    ############################
    #    Hyperparamaters       #
    ############################
    coeff_entropy = 0.0001
    lr = 0.0003
    batch_size = 100
    n_steps = 1500
    nupdates = 10
    max_epochs = 2000
    clip_value = 0.2

    env = env_test_RJ.env()
    policy = ActorCritic.MLP(4, 1).cuda()
    opt = Adam(policy.parameters(), lr=lr)

    PPO = ppo.PPO(policy,opt,batch_size,nupdates,coeff_entropy,clip_value)

    save_weights = True 
    load_policy = False

    path = 'environment/models/'
    agent_name = '2_goal_normalized_R_bigger_NN'

    if load_policy:
        print("loading policy")
        policy.load_state_dict(torch.load(path + agent_name+'.pth'))


    for epoch in range(1, max_epochs+1):

        should_render = True #epoch % 200 == 0

        observations, actions, logprobs, returns, values, rewards = PPO.generate_episode(env, n_steps, should_render=should_render)

        memory = (actions, observations, values, logprobs, returns)
        PPO.update(memory)
        print(f'Episode {epoch}, reward is {rewards.sum()}')
        if epoch % 30 == 0:
            print("saving policy")
            torch.save(policy.state_dict(), path + agent_name + '.pth')
