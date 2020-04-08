import gym
from gym import error, spaces, utils
from gym.utils import seeding
import numpy as np

from gym_snake.envs.snake import Snake, Food
import pygame
from pygame.locals import (
  KEYDOWN,
  K_ESCAPE,
  QUIT
)
import gym_snake.envs.constants as constants

class SnakeEnv(gym.Env):
  metadata = {'render.modes': ['human']}

  def __init__(self):
    # gym variables
    self.action_space = spaces.Discrete(4)

    # Initialize pygame
    pygame.init()
    self.screen = pygame.display.set_mode((constants.SCREEN_WIDTH + 1, constants.SCREEN_HEIGHT + 1))
    # self.clock = pygame.time.Clock() 
    self.state = self.reset()

  def step(self, action):
    state = self.getState()

    for event in pygame.event.get():
        if event.type == KEYDOWN:
          if event.key == K_ESCAPE:
            self.done = True
        elif event.type == QUIT:
            self.done = True
    
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

    if (len(self.snake.body) >= constants.MAX_SIZE ):
      # print('You won! No more space')
      self.done = True

    lost, reward = self.snake.collision(self.food)

    if (lost):
      # print("gg")
      # print("Score: " + str(self.snake.score))
      self.done = True

    # self.clock.tick(10)
    return [ state , reward, self.done, self.snake.score ]

  def reset(self):
    self.done = False
    self.reward = 0.1
    self.snake = Snake()
    self.food = Food()
    state = self.getState()
    
    return state

  def render(self, mode='human', close=False):
    self.screen.fill((0,0,0))
    self.snake.draw(self.screen)
    self.food.draw(self.screen)
    pygame.display.flip()

  def close(self):
    self.done = True

  # State is given by relative fruit position and relative tail position
  def getState(self):
    rel_food = [self.snake.body[0][0] - self.food.position[0], self.snake.body[0][1] - self.food.position[1]]
    rel_tail = [self.snake.body[0][0] - self.snake.body[-1][0], self.snake.body[0][1] - self.snake.body[-1][1]]

    return [rel_food[0],rel_food[1], rel_tail[0], rel_tail[1]]

