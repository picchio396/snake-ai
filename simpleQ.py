# https://lilianweng.github.io/lil-log/2018/05/05/implementing-deep-reinforcement-learning-models.html
# https://github.com/lilianweng/deep-reinforcement-learning-gym/blob/master/playground/policies/qlearning.py
'''
    Initialize the Q-table by all zeros.
    Start exploring actions: For each state, select any one among all possible actions for the current state (S).
    Travel to the next state (S') as alpha result of that action (alpha).
    For all possible actions from the state (S') select the one with the highest Q-value.
    Update Q-table values using the equation.
    Set the next state as the current state.
    If goal state is reached, then end and repeat the process.
'''

""" NOT USED GOOD FOR REFERENCE
import sys
import random
import numpy as np
import constants
import controller.snake_env as controller


def run_experiment(argv):
    print(argv)
    MAX_EPOCHS = 1
    
    # env = controller.SnakeEnv(hasView=True, speed=constants.SPEED)
    env = controller.SnakeEnv()

    # All 0 < x < 1 
    # alpha: learning rate (the extent to which our Q-values are being updated in every iteration)
    # gamma: discount factor (how much importance we want to give to future rewards)
    # epsilon: exploration faction (exploration (choosing alpha random action) vs exploitation (choosing actions based on already learned Q-values))
    alpha = 0.1 #0.1
    gamma = 0.6#0.6
    epsilon =  0 #0.1

    # epsilon_rate = 0.99
    # min_epsilon = 0.2

    # gamma_rate = 0.99
    # min_gamma = 0.3

    try:
        print('Loading...')
        q_table = np.load('q_table.npy')
    except:
        print("Initializing...")
        q_table = np.zeros([2048, 4])

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
                action = random.randint(0,3) # Explore action space
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

        # # Updating values
        # epsilon = epsilon * epsilon_rate if epsilon > min_epsilon else min_epsilon

        if score > max_score:
            max_score = score
            print('New max score: ' + str(max_score))
        if i % 100 == 0:
            print(f"Episode: {i}")

    print('Saving...')
    np.save('q_table.npy', q_table)

    print("Max score: " + str(max_score))
    print("Training finished.\n")
    return int(max_score)

if __name__ == "__main__":
    run_experiment(sys.argv[1:])
"""