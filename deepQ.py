# Reference https://github.com/maurock/snake-ga

import sys
from random import randint, uniform
import numpy as np
import argparse

import controller.snake_env as controller
from ml_agent.DeepAgent import DeepAgent

import os
import matplotlib.pyplot as plt
import seaborn as sns

def define_parameters():
    params = dict()
    params['display_option'] = True
    params['speed'] = 60
    params['epsilon_decay_linear'] = 1/75
    params['learning_rate'] = 0.0005
    params['first_layer_size'] = 12 #150   # neurons in the first layer
    params['second_layer_size'] = 8 #150   # neurons in the second layer
    params['third_layer_size'] = 0 #150    # neurons in the third layer
    params['episodes'] = 1          
    params['memory_size'] = 2500
    params['batch_size'] = 500
    params['weights_path'] = 'ml_agent/weights/weights.hdf5'
    params['load_weights'] = False
    params['train'] = False
    return params

def plot_seaborn(x_array, y_array):
    sns.set(color_codes=True)
    ax = sns.regplot(
        np.array([x_array])[0],
        np.array([y_array])[0],
        color="b",
        x_jitter=.1,
        line_kws={'color': 'green'}
    )
    ax.set(xlabel='games', ylabel='score')
    plt.show()

def run_experiment(params):
    # Start environment
    env = controller.SnakeEnv('deep', params['display_option'], params['speed'])
    agent = DeepAgent(params)

    episode_num = 0
    max_score = 0

    score_plot = []
    episode_plot = []

    while episode_num < params['episodes']:
        state = env.reset()

        game_steps, reward = 0, 0
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

            # Perform action and get new state
            next_state, reward, done, score = env.step(action) 
            
            if params['train']:
                # train short memory base on the new action and state
                agent.train_short_memory(state, action, reward, next_state, done)
                # store the new data into a long term memory
                agent.remember(state, action, reward, next_state, done)

            if score > max_score:
                max_score = score
                print(f"New max: {max_score}")

            state = next_state
            game_steps += 1

        if params['train']:
            agent.replay_new(agent.memory, params['batch_size'])
        episode_num += 1
        print(f'Game {episode_num}      Score: {score}')
        score_plot.append(score)
        episode_plot.append(episode_num)

    if params['train']:
        agent.model.save_weights(params['weights_path'])

    print("Training finished.\n")
    plot_seaborn(episode_plot, score_plot)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run simple Q learning algorithm')
    parser.add_argument('--display',
                        metavar='bool',  
                        type=bool, 
                        default=False,
                        help='If you want a ui or not',
                        )
    parser.add_argument('--wait', 
                        metavar='int',
                        type=int, 
                        default=50,
                        help='how long to wait till next action (bigger the number slower the speed)')
    args = parser.parse_args()
    params = define_parameters()

    run_experiment(args.display, args.wait, params)
