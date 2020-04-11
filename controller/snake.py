#!/usr/bin/python3
import pygame
from random import randint
import constants

class Snake:
  def __init__(self):
    super().__init__()
    self.surf = pygame.Surface((24, 24))
    self.surf.fill((53, 181, 87)) # Darker (34, 117, 56)
    # self.rect = self.surf.get_rect()
    self.body =  [[16,12], [15,12], [14, 12]]
    self.direction = [1,0]
    self.score = 0

  def draw(self, screen):
    for i in range(len(self.body)):
      screen.blit(self.surf, (self.body[i][0] * constants.BLOCK_SIZE, self.body[i][1] * constants.BLOCK_SIZE))

  def moveRight(self):
    if(self.direction != [-1, 0]):
      self.direction = [1, 0]
  def moveLeft(self):
    if(self.direction != [1, 0]):
      self.direction = [-1, 0]
  def moveUp(self):
    if(self.direction != [0, 1]):
      self.direction = [0, -1]
  def moveDown(self):
    if(self.direction != [0, -1]):
      self.direction = [0, 1]

  # def turnLeft(self):
  #   # going right -> move up
  #   if(self.direction == [1,0]):
  #     self.direction = [0, -1]
  #   # going left -> move down
  #   elif(self.direction == [-1,0]):
  #     self.direction = [0, 1]
  #   # going up -> move left
  #   elif(self.direction == [0,-1]):
  #     self.direction = [-1, 0]
  #   # going down -> move right
  #   elif(self.direction == [0,-1]):
  #     self.direction = [1, 0]

  # def turnRight(self):
  #   # going right -> move down
  #   if(self.direction == [1,0]):
  #     self.direction = [0, 1]
  #   # going left -> move up
  #   elif(self.direction == [-1,0]):
  #     self.direction = [0, -1]
  #   # going up -> move rigth
  #   elif(self.direction == [0,-1]):
  #     self.direction = [1, 0]
  #   # going down -> move left
  #   elif(self.direction == [0,-1]):
  #     self.direction = [-1, 0]
    
  def update(self):
    # Move last element to head spot
    self.body[-1] = self.body[0]
    self.body.insert(1, self.body.pop(-1))

    # Move head
    self.body[0] = [self.body[0][0] + self.direction[0], self.body[0][1] + self.direction[1]]
    # self.x[0] = self.x[0] + (self.direction[0])
    # self.y[0] = self.y[0] + (self.direction[1])

    # Keep snake on the screen
    # if self.body[0][0] < 0:
    #   self.body[0][0] = int(constants.MAX_WIDTH - 1)
    # if self.body[0][0] >= constants.MAX_WIDTH:
    #   self.body[0][0] = 0
    # if self.body[0][1] < 0:
    #   self.body[0][1] = int(constants.MAX_HEIGHT - 1)
    # if self.body[0][1] >= constants.MAX_HEIGHT:
    #   self.body[0][1] = 0

  def danger (self, look):  
    next_block = self.body[0]

    if look == 'front':
      next_block = [next_block[0] + self.direction[0], next_block[1] + self.direction[1]]

    if look == 'left':
        # going right -> check up
      if(self.direction == [1,0]):
        next_block = [next_block[0], next_block[1] - 1]
      # going left -> check down
      elif(self.direction == [-1,0]):
        next_block = [next_block[0], next_block[1] + 1]
      # going up -> check left
      elif(self.direction == [0,-1]):
        next_block = [next_block[0] - 1, next_block[1]]
      # going down -> check right
      elif(self.direction == [0,-1]):
        next_block = [next_block[0] + 1, next_block[1]]

    if look == 'right':
      # going right -> check down
      if(self.direction == [1,0]):
        next_block = [next_block[0], next_block[1] + 1]
      # going left -> check up
      elif(self.direction == [-1,0]):
        next_block = [next_block[0], next_block[1] - 1]
      # going up -> check rigth
      elif(self.direction == [0,-1]):
        next_block = [next_block[0] + 1, next_block[1]]
      # going down -> check left
      elif(self.direction == [0,-1]):
        next_block = [next_block[0] - 1, next_block[1]]

    # Check if collides with itself
    for i in range(1, len(self.body)):
      if(next_block == self.body[i]):
        return True

    # Check if hits walls
    if next_block[0] < 0 or next_block[0] >= constants.MAX_WIDTH or next_block[1] < 0 or next_block[1] >= constants.MAX_HEIGHT:
      return True

    return False


  def collision(self, food):
    # Check if collides with itself
    for i in range(1, len(self.body)):
      if(self.body[0] == self.body[i]):
        # print('me')
        return [True, -1]

    # Check if hits walls
    if self.body[0][0] < 0 or self.body[0][0] >= constants.MAX_WIDTH or self.body[0][1] < 0 or self.body[0][1] >= constants.MAX_HEIGHT:
      # print('wall')
      return [True, -1]

    # Check if food was eaten
    if(self.body[0] == food.position):
      # Add snake length
      self.body.append(food.position)
      food.eaten(self.body)

      self.score = self.score + 1
      return [False, 1]

    return [False, -0.1]

class Food:
  def __init__(self):
    super().__init__()

    self.surf = pygame.Surface((24, 24))
    self.surf.fill((181, 53, 53))
    # self.rect = self.surf.get_rect()

    x = randint(0, (constants.MAX_WIDTH - 1))
    y = randint(0, (constants.MAX_HEIGHT -1))
    self.position = [x, y]

  def draw(self, screen):
    screen.blit(self.surf, (self.position[0] * constants.BLOCK_SIZE , self.position[1] * constants.BLOCK_SIZE))
    
  def eaten(self, snake_body):
    temp_x = randint(0, (constants.MAX_WIDTH - 1))
    temp_y = randint(0, (constants.MAX_HEIGHT -1))
    temp_pos = [temp_x, temp_y]

    # Checking that new food is not in snake
    while temp_pos in snake_body:
      temp_x = randint(0, (constants.MAX_WIDTH - 1))
      temp_y = randint(0, (constants.MAX_HEIGHT -1))
      temp_pos = [temp_x, temp_y]

    self.position = temp_pos