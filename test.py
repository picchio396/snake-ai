'''
    Initialize the Q-table by all zeros.
    Start exploring actions: For each state, select any one among all possible actions for the current state (S).
    Travel to the next state (S') as alpha result of that action (alpha).
    For all possible actions from the state (S') select the one with the highest Q-value.
    Update Q-table values using the equation.
    Set the next state as the current state.
    If goal state is reached, then end and repeat the process.
'''
import gym 
import gym_snake
import random
import numpy as np
import constants

MAX_EPOCHS = 100

# q_table = np.zeros([])

# All 0 < x < 1 
# alpha: learning rate (the extent to which our Q-values are being updated in every iteration)
# gamma: discount factor (how much importance we want to give to future rewards)
# epsilon: exploration faction (exploration (choosing alpha random action) vs exploitation (choosing actions based on already learned Q-values))
alpha = 0.1
gamma = 0.6
epsilon = 0.1

env = gym.make('snake-v0')

q_table = np.zeros([int(constants.MAX_WIDTH), int(constants.SCREEN_HEIGHT), int(constants.MAX_WIDTH), int(constants.MAX_HEIGHT)])

# For plotting metrics
all_epochs = []
all_penalties = []

for i in range(1, MAX_EPOCHS):
    state = env.reset()

    epochs, penalties, reward, = 0, 0, 0
    done = False
    
    while not done:
        if random.uniform(0, 1) < epsilon:
            action = env.action_space.sample() # Explore action space
        else:
            action = np.argmax(q_table[state]) # Exploit learned values

        next_state, reward, done = env.step(action) 
        
        old_value = q_table[state][action]
        next_max = np.max(q_table[next_state])
        
        new_value = (1 - alpha) * old_value + alpha * (reward + gamma * next_max)
        q_table[state][action] = new_value

        if reward == -10:
            penalties += 1

        state = next_state
        epochs += 1
        
    if i % 100 == 0:
        print(f"Episode: {i}")

print("Training finished.\n")
