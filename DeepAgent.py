import tensorflow as tf
import numpy as np
import constants
import controller.snake_env as controller
import matplotlib.pyplot as plt

class DeepAgent(object):
    def __init__(self, params):
        self.reward
        self.gamma = 0.9
        self.epsilon = 1
        self.learning_rate = params['learning_rate']
        self.first_layer = params['first_layer_size']
        self.second_layer = params['second_layer_size']

        self.model = self.create_snake_model()



    # Input -> 11, Output -> 4
    def create_snake_model(self):
        model = tf.keras.models.Sequential([
            tf.keras.layers.Dense(output_dim=self.first_layer, activation='relu', input_dim=11),
            tf.keras.layers.Dense(output_dim=self.second_layer, activation='relu'),
            tf.keras.layers.Dense(output_dim=4, activation='softmax')
        ])

        # LEARN ME
        opt = tf.keras.optimizers.Adam(self.learning_rate)
        model.compile(loss='mse', optimizer=opt)

        return model