import sys
from random import randint, uniform
import numpy as np
import constants
import controller.snake_env as controller
import DeepAgent

import os
import argparse
import matplotlib.pyplot as plt

from tensorflow.keras.utils import to_categorical

def define_parameters():
    params = dict()
    params['epsilon_decay_linear'] = 1/75
    params['learning_rate'] = 0.0005
    params['first_layer_size'] = 150   # neurons in the first layer
    params['second_layer_size'] = 150   # neurons in the second layer
    params['third_layer_size'] = 150    # neurons in the third layer
    params['episodes'] = 150            
    params['memory_size'] = 2500
    # params['batch_size'] = 500
    params['weights_path'] = 'weights/weights.hdf5'
    params['load_weights'] = True
    params['train'] = False
    return params

def run_experiment(display_option, speed, params):
    # Start environment
    env = controller.SnakeEnv(display_option, speed)
    agent = DeepAgent(params)

    for episode_num in range(0, params['episodes']):
        state = env.reset()

        epochs, reward, = 0, 0
        done = False
        
        while not done:
            if not params['train']:
                agent.epsilon = 0
            else:
                agent.epsilon = 1 - (episode_num * params['epsilon_decay_linear'])

            if uniform(0, 1) < agent.epsilon:
                action = randint(0,3) # Explore action space
            else:
                prediction = agent.model.predict(state.reshape((1,11)))
                action = np.argmax(prediction) # Exploit learned values
                ## Come back here

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

    print("Max score: " + str(max_score))
    print("Training finished.\n")
    return int(max_score)

if __name__ == '__main__':
    # Set options to activate or deactivate the game view, and its speed
    parser = argparse.ArgumentParser()
    params = define_parameters()
    parser.add_argument("--display", type=bool, default=True)
    parser.add_argument("--speed", type=int, default=50)
    args = parser.parse_args()
    # params['bayesian_optimization'] = False    # Use bayesOpt.py for Bayesian Optimization
    
    run_experiment(args.display, args.speed, params)
