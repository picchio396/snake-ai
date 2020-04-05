#!/usr/bin/python3
import pygame
from random import randint

BLOCK_SIZE = 25
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

class Snake:
  body = [[400,300], [375,300], [350, 300]]
  direction = [1,0]
  score = 0

  def __init__(self):
    super().__init__()
    self.surf = pygame.Surface((24, 24))
    self.surf.fill((53, 181, 87)) # Darker (34, 117, 56)
    # self.rect = self.surf.get_rect()

  def draw(self, screen):
    for i in range(len(self.body)):
      screen.blit(self.surf, (self.body[i][0], self.body[i][1]))

  def moveRight(self):
    if (self.direction != [-1, 0]):
      self.direction = [1, 0]
  def moveLeft(self):
    if (self.direction != [1, 0]):
      self.direction = [-1, 0]
  def moveUp(self):
    if (self.direction != [0, 1]):
      self.direction = [0, -1]
  def moveDown(self):
    if (self.direction != [0, -1]):
      self.direction = [0, 1]
    
  def update(self):
    # Move last element to head spot
    self.body[-1] = self.body[0]
    self.body.insert(1, self.body.pop(-1))

    # Move head
    self.body[0] = [self.body[0][0] + (self.direction[0] * BLOCK_SIZE), self.body[0][1] + (self.direction[1] * BLOCK_SIZE)]
    # self.x[0] = self.x[0] + (self.direction[0] * BLOCK_SIZE)
    # self.y[0] = self.y[0] + (self.direction[1] * BLOCK_SIZE)

    # Keep snake on the screen
    if self.body[0][0] < 0:
      self.body[0][0] = SCREEN_WIDTH - BLOCK_SIZE
    if self.body[0][0] >= SCREEN_WIDTH:
      self.body[0][0] = 0
    if self.body[0][1] < 0:
      self.body[0][1] = SCREEN_HEIGHT - BLOCK_SIZE
    if self.body[0][1] >= SCREEN_HEIGHT:
      self.body[0][1] = 0

  def collision(self, food):
    # Check if collides with itself
    for i in range(1, len(self.body)):
      if(self.body[0] == self.body[i]):
        return True

    # Check if food was eaten
    if(self.body[0] == food.position):
      # Add snake length
      self.body.append(food.position)
      food.eaten(self.body)

      self.score = self.score + 1

    return [False, self.score]

class Food:
  def __init__(self):
    super().__init__()

    self.surf = pygame.Surface((24, 24))
    self.surf.fill((181, 53, 53))
    # self.rect = self.surf.get_rect()

    x = randint(0, (SCREEN_WIDTH-BLOCK_SIZE)/BLOCK_SIZE) * BLOCK_SIZE
    y = randint(0, (SCREEN_HEIGHT-BLOCK_SIZE)/BLOCK_SIZE) * BLOCK_SIZE
    self.position = [x, y]

  def draw(self, screen):
    screen.blit(self.surf, (self.position[0], self.position[1]))
    
  def eaten(self, snake_body):
    temp_x = randint(0, (SCREEN_WIDTH-BLOCK_SIZE)/BLOCK_SIZE) * BLOCK_SIZE
    temp_y = randint(0, (SCREEN_HEIGHT-BLOCK_SIZE)/BLOCK_SIZE) * BLOCK_SIZE
    temp_pos = [temp_x, temp_y]

    # Checking that new food is not in snake
    while temp_pos in snake_body:
      temp_x = randint(0, (SCREEN_WIDTH-BLOCK_SIZE)/BLOCK_SIZE) * BLOCK_SIZE
      temp_y = randint(0, (SCREEN_HEIGHT-BLOCK_SIZE)/BLOCK_SIZE) * BLOCK_SIZE
      temp_pos = [temp_x, temp_y]

    self.position = temp_pos