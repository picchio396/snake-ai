import numpy as np
import pygame
from pygame.locals import (
  KEYDOWN,
  K_ESCAPE,
  QUIT
)

from controller.snake import Snake, Food
import constants as constants

class SnakeEnv():

  def __init__(self):
    # Initialize pygame
    pygame.init()
    self.screen = pygame.display.set_mode((constants.SCREEN_WIDTH + 1, constants.SCREEN_HEIGHT + 1))
    self.clock = pygame.time.Clock() 

    self.isSnakeRight = False
    self.isSnakeLeft = False
    self.isSnakeUp = False
    self.isSnakeDown = False

    self.isSnakeRight = False
    self.isSnakeLeft = False
    self.isSnakeUp = False
    self.isSnakeDown = False
    self.isDanger = False

    self.state = self.reset()

  def step(self, action):
    state = self.getState()

    for event in pygame.event.get():
        if event.type == KEYDOWN:
          if event.key == K_ESCAPE:
            self.done = True
        elif event.type == QUIT:
            self.done = True
    
    # Go straigth (do nothing)
    # if(action == 0):
    #     self.snake.moveUp()
    if(action == 1):
        self.snake.turnRight()
    elif(action == 2):
        self.snake.turnLeft()

    self.render()
    self.snake.update()
    # input('\n')

    if (len(self.snake.body) >= constants.MAX_SIZE ):
      # print('You won! No more space')
      self.done = True

    lost, reward = self.snake.collision(self.food)

    if (lost):
      # print("gg")
      # print("Score: " + str(self.snake.score))
      self.done = True

    self.clock.tick(60)
    return [ state , reward, self.done, self.snake.score ]

  def reset(self):
    self.done = False
    self.reward = -0.1
    self.snake = Snake()
    self.food = Food()
    state = self.getState()
    
    return state

  def render(self):
    self.screen.fill((0,0,0))
    self.snake.draw(self.screen)
    self.food.draw(self.screen)
    pygame.display.flip()

  def close(self):
    self.done = True

  # State is given by relative fruit position and relative tail position
  def getState(self):
    # Reset
    self.isSnakeRight = False
    self.isSnakeLeft = False
    self.isSnakeUp = False
    self.isSnakeDown = False

    self.isFoodRight = False
    self.isFoodLeft = False
    self.isFoodUp = False
    self.isFoodDown = False

    self.isDangerFront = False
    self.isDangerLeft = False
    self.isDangerRight = False

    # rel_food = [self.snake.body[0][0] - self.food.position[0], self.snake.body[0][1] - self.food.position[1]]
    # rel_tail = [self.snake.body[0][0] - self.snake.body[-1][0], self.snake.body[0][1] - self.snake.body[-1][1]]

    # going rigth
    if self.snake.direction == [1, 0]:
      self.isSnakeRight =  True
      # food left or right
      if self.snake.body[0][1] - self.food.position[1] > 0:
        self.isFoodLeft = True
      elif self.snake.body[0][1] - self.food.position[1] < 0:
        self.isFoodRight = True
      #food up or down
      if self.snake.body[0][0] - self.food.position[0] > 0:
        self.isFoodDown = True
      elif self.snake.body[0][0] - self.food.position[0] < 0:
        self.isFoodUp = True

    # going left
    if self.snake.direction == [-1, 0]:
      self.isSnakeLeft = True
      # food left or right
      if self.snake.body[0][1] - self.food.position[1] < 0:
        self.isFoodLeft = True
      elif self.snake.body[0][1] - self.food.position[1] > 0:
        self.isFoodRight = True
      #food up or down
      if self.snake.body[0][0] - self.food.position[0] < 0:
        self.isFoodDown = True
      elif self.snake.body[0][0] - self.food.position[0] > 0:
        self.isFoodUp = True

    # going up
    if self.snake.direction == [0,-1]:
      self.isSnakeUp = True
      # food left or right
      if self.snake.body[0][0] - self.food.position[0] > 0:
        self.isFoodLeft = True
      elif self.snake.body[0][0] - self.food.position[0] < 0:
        self.isFoodRight = True
      #food up or down
      if self.snake.body[0][1] - self.food.position[1] < 0:
        self.isFoodDown = True
      elif self.snake.body[0][1] - self.food.position[1] > 0:
        self.isFoodUp = True

    # going down
    if self.snake.direction == [0,1]:
      self.isSnakeDown = True
      # food left or right
      if self.snake.body[0][0] - self.food.position[0] < 0:
        self.isFoodLeft = True
      elif self.snake.body[0][0] - self.food.position[0] > 0:
        self.isFoodRight = True
      #food up or down
      if self.snake.body[0][1] - self.food.position[1] > 0:
        self.isFoodDown = True
      elif self.snake.body[0][1] - self.food.position[1] < 0:
        self.isFoodUp = True


    self.isDangerFront = self.snake.danger('front')
    self.isDangerLeft = self.snake.danger('left')
    self.isDangerRight = self.snake.danger('rights')

    # self.printState()

    bin_string = str(int(self.isSnakeRight == True)) + str(int(self.isSnakeLeft == True)) + str(int(self.isSnakeUp == True)) + str(int(self.isSnakeDown == True)) + str(int(self.isFoodRight == True)) + str(int(self.isFoodLeft == True)) + str(int(self.isFoodUp == True)) + str(int(self.isFoodDown == True)) + str(int(self.isDangerFront == True)) + str(int(self.isDangerLeft == True)) + str(int(self.isDangerRight == True))

    print(int(bin_string, 2))

    return int(bin_string, 2) 

  def printState(self):
    print("\
      isSnakeRight: {0}\n\
      isSnakeLeft: {1}\n\
      isSnakeUp: {2}\n\
      isSnakeDown: {3}\n\n\
      isFoodRight: {4}\n\
      isFoodLeft: {5}\n\
      isFoodUp: {6}\n\
      isFoodDown: {7}\n\n\
      isDangerFront: {8}\n\
      isDangerLeft:{9}\n\
      isDangerRight: {10}\n\n\
    ".format(self.isSnakeRight, self.isSnakeLeft, self.isSnakeUp, self.isSnakeDown, self.isFoodRight, self.isFoodLeft, self.isFoodUp, self.isFoodDown, self.isDangerFront, self.isDangerLeft, self.isDangerRight),
      end="\r"
    )

