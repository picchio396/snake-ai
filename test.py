'''
    Initialize the Q-table by all zeros.
    Start exploring actions: For each state, select any one among all possible actions for the current state (S).
    Travel to the next state (S') as alpha result of that action (alpha).
    For all possible actions from the state (S') select the one with the highest Q-value.
    Update Q-table values using the equation.
    Set the next state as the current state.
    If goal state is reached, then end and repeat the process.
'''
import random
import numpy as np
import constants
import controller.snake_env as controller

MAX_EPOCHS = 200

env = controller.SnakeEnv()

# All 0 < x < 1 
# alpha: learning rate (the extent to which our Q-values are being updated in every iteration)
# gamma: discount factor (how much importance we want to give to future rewards)
# epsilon: exploration faction (exploration (choosing alpha random action) vs exploitation (choosing actions based on already learned Q-values))
alpha = 0.17#0.1
gamma = 0.65#0.6
epsilon =  0.2 #0.1

# epsilon = 1
# epsilon_rate = 0.8
# min_epsilon = 0.1

# gamma = 0.2
# gamma_rate = 0.99
# min_gamma = 0.3

# try:
#     print('Loading...')
#     q_table = np.load('q_table.npy')
# except:
print("Initializing...")
q_table = np.zeros([2048, 3])

# For plotting metrics
all_epochs = []
all_penalties = []

max_score = 0

for i in range(0, MAX_EPOCHS):
    state = env.reset()

    epochs, reward, = 0, 0
    done = False
    
    while not done:
        if random.uniform(0, 1) < epsilon:
            action = random.randint(0,2) # Explore action space
        else:
            action = np.argmax(q_table[state]) # Exploit learned values

        next_state, reward, done, score = env.step(action) 
        # print( next_state, reward, done, score)
        
        old_value = q_table[state][action]
        next_max = np.max(q_table[next_state])
        
        new_value = (1 - alpha) * old_value + alpha * (reward + gamma * next_max)
        q_table[state][action] = new_value

        state = next_state
        epochs += 1

        # Updating epsilon value
        # epsilon = epsilon * epsilon_rate if epsilon > min_epsilon else min_epsilon

    
    if score > max_score:
        max_score = score
        print('New max score: ' + str(max_score))
    if i % 100 == 0:
        print(f"Episode: {i}")

# print('Saving...')
# np.save('q_table.npy', q_table)

print("Max score: " + str(max_score))
print("Training finished.\n")
