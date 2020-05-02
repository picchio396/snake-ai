import tensorflow as tf
import numpy as np
import random

import collections

class DeepAgent(object):
    def __init__(self, params):
        self.reward = 0
        self.gamma = 0.9
        self.epsilon = 1
        self.learning_rate = params['learning_rate']
        self.first_layer = params['first_layer_size']
        self.second_layer = params['second_layer_size']
        self.third_layer = params['third_layer_size']

        self.short_memory = np.array([])
        self.memory = collections.deque(maxlen=params['memory_size'])
        self.load_weights = params['load_weights']

        self.model = self.create_snake_model()


    # Input -> 11, Output -> 4
    def create_snake_model(self):
        model = tf.keras.models.Sequential([
            tf.keras.layers.Dense(units=self.first_layer, activation='relu', input_dim=11),
            tf.keras.layers.Dense(units=self.second_layer, activation='relu'),
            tf.keras.layers.Dense(units=4, activation='softmax')
        ])

        # LEARN ME
        opt = tf.keras.optimizers.Adam(self.learning_rate)
        model.compile(loss='mse', optimizer=opt)

        return model

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    # LEARN ME
    def replay_new(self, memory, batch_size):
        if len(memory) > batch_size:
            minibatch = random.sample(memory, batch_size)
        else:
            minibatch = memory
        for state, action, reward, next_state, done in minibatch:
            target = reward
            if not done:
                target = reward + self.gamma * np.amax(self.model.predict(np.array([next_state]))[0])
            target_f = self.model.predict(np.array([state]))
            target_f[0][np.argmax(action)] = target
            self.model.fit(np.array([state]), target_f, epochs=1, verbose=0)

    # LEARN ME
    def train_short_memory(self, state, action, reward, next_state, done):
        target = reward
        if not done:
            target = reward + self.gamma * np.amax(self.model.predict(next_state.reshape((1, 11)))[0])
        target_f = self.model.predict(state.reshape((1, 11)))
        target_f[0][np.argmax(action)] = target
        self.model.fit(state.reshape((1, 11)), target_f, epochs=1, verbose=0)