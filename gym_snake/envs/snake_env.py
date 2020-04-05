import gym
from gym import error, spaces, utils
from gym.utils import seeding

from gym_snake.envs.snake import Snake, Food
import pygame

BLOCK_SIZE = 25
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
MAX_SIZE = (SCREEN_HEIGHT/BLOCK_SIZE) * (SCREEN_WIDTH/BLOCK_SIZE)

class FooEnv(gym.Env):
  metadata = {'render.modes': ['human']}

  def __init__(self):
    # Initialize pygame
    pygame.init()
    self.screen = pygame.display.set_mode((SCREEN_WIDTH + 1, SCREEN_HEIGHT + 1))
    self.clock = pygame.time.Clock() 
    self.reset()

  def step(self, action):
    if(self.done):
        print("Game over")
        return [ self.snake.x, self.snake.y, self.food.x, self.food.y, self.score, self.done]

    if(action == 0):
        self.snake.moveUp()
    elif(action == 1):
        self.snake.moveDown()
    elif(action == 2):
        self.snake.moveLeft()
    elif(action == 3):
        self.snake.moveRight()

    self.render()
    self.snake.update()

    if (len(self.snake.x) >= MAX_SIZE ):
        print('You won! No more space')
        self.done = True

    lost, score = self.snake.collision(self.food)
    self.score = score
    if (lost):
        print("You lost")
        self.done = True

    self.clock.tick(10)
    return [ self.snake.x, self.snake.y, self.food.x, self.food.y, self.score, self.done]

  def reset(self):
    self.done = False
    self.score = 0
    self.snake = Snake()
    self.food = Food()

  def render(self, mode='human', close=False):
    ...