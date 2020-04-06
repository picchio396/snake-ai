import gym 
import gym_snake

env = gym.make('snake-v0')

timestep = 0
penalties, reward = 0, 0

done = False

while not done:
    action = env.action_space.sample()
    state, reward, done = env.step(action)

    if reward == -10:
        penalties += 1

    timestep += 1
    
    
print("Timesteps taken: {}".format(timestep))
print("Penalties incurred: {}".format(penalties))