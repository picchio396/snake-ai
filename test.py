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

MAX_EPOCHS = 5000

## TODO
# figure out how to stop
# figure out how to save

# q_table = np.zeros([])

# All 0 < x < 1 
# alpha: learning rate (the extent to which our Q-values are being updated in every iteration)
# gamma: discount factor (how much importance we want to give to future rewards)
# epsilon: exploration faction (exploration (choosing alpha random action) vs exploitation (choosing actions based on already learned Q-values))
alpha = 0.1 #0.1
gamma = 0.6 #0.6
epsilon = 0.1 #0.1

env = gym.make('snake-v0')

try:
    print('Loading...')
    q_table = np.load('q_table.npy')
except:
    print("Initializing...")
    q_table = np.zeros([int(constants.MAX_WIDTH*2), int(constants.SCREEN_HEIGHT*2), int(constants.MAX_WIDTH*2), int(constants.MAX_HEIGHT*2), 4])

# For plotting metrics
all_epochs = []
all_penalties = []

max_score = 0

for i in range(0, MAX_EPOCHS):
    state = env.reset()

    epochs, penalties, reward, = 0, 0, 0
    done = False
    
    while not done:
        if random.uniform(0, 1) < epsilon:
            action = env.action_space.sample() # Explore action space
        else:
            action = np.argmax(q_table[state[0]][state[1]][state[2]][state[3]]) # Exploit learned values

        next_state, reward, done, score = env.step(action) 
        # print( next_state, reward, done, score)
        
        old_value = q_table[state[0]][state[1]][state[2]][state[3]][action]
        next_max = np.max(q_table[next_state[0]][next_state[1]][next_state[2]][next_state[3]])
        
        new_value = (1 - alpha) * old_value + alpha * (reward + gamma * next_max)
        q_table[state[0]][state[1]][state[2]][state[3]][action] = new_value

        if reward == -10:
            penalties += 1

        state = next_state
        epochs += 1

    
    if score > max_score:
        max_score = score
        print('New max score: ' + str(max_score))
    if i % 100 == 0:
        print(f"Episode: {i}")

print('Saving...')
np.save('q_table.npy', q_table)

print("Max score: " + str(max_score))
print("Training finished.\n")
