#!/usr/bin/python3
import pygame
from random import randint

BLOCK_SIZE = 25
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

class Snake:
  x = [400, 375, 350]
  y = [300, 300, 300]
  direction = [1,0]
  score = 0

  def __init__(self):
    super().__init__()
    self.surf = pygame.Surface((24, 24))
    self.surf.fill((53, 181, 87)) # Darker (34, 117, 56)
    # self.rect = self.surf.get_rect()

  def draw(self, screen):
    for i in range(len(self.x)):
      screen.blit(self.surf, (self.x[i], self.y[i]))

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
    self.x[-1] = self.x[0]
    self.y[-1] = self.y[0]
    self.x.insert(1, self.x.pop(-1))
    self.y.insert(1, self.y.pop(-1))

    # Move head
    self.x[0] = self.x[0] + (self.direction[0] * BLOCK_SIZE)
    self.y[0] = self.y[0] + (self.direction[1] * BLOCK_SIZE)

    # Keep snake on the screen
    if self.x[0] < 0:
      self.x[0] = SCREEN_WIDTH - BLOCK_SIZE
    if self.x[0] >= SCREEN_WIDTH:
      self.x[0] = 0
    if self.y[0] < 0:
      self.y[0] = SCREEN_HEIGHT - BLOCK_SIZE
    if self.y[0] >= SCREEN_HEIGHT:
      self.y[0] = 0

  def collision(self, food):
    # Check if collides with itself
    for i in range(1, len(self.x)):
      if(self.x[0] == self.x[i] and self.y[0] == self.y[i]):
        return True

    # Check if food was eaten
    if(self.x[0] == food.x and self.y[0] == food.y):
      # Add snake length
      self.x.append(food.x)
      self.y.append(food.y)
      food.eaten(self.x, self.y)

      self.score = self.score + 1

    return (False, self.score)

class Food:
  def __init__(self):
    super().__init__()

    self.surf = pygame.Surface((24, 24))
    self.surf.fill((181, 53, 53))
    # self.rect = self.surf.get_rect()

    self.x = randint(0, (SCREEN_WIDTH-BLOCK_SIZE)/BLOCK_SIZE) * BLOCK_SIZE
    self.y = randint(0, (SCREEN_HEIGHT-BLOCK_SIZE)/BLOCK_SIZE) * BLOCK_SIZE

  def draw(self, screen):
    screen.blit(self.surf, (self.x, self.y))

  def eaten(self, snake_x, snake_y):
    temp_x = randint(0, (SCREEN_WIDTH-BLOCK_SIZE)/BLOCK_SIZE) * BLOCK_SIZE
    temp_y = randint(0, (SCREEN_HEIGHT-BLOCK_SIZE)/BLOCK_SIZE) * BLOCK_SIZE

    # Checking that new food is not in snake
    while (temp_x in snake_x) and (temp_y in snake_y):
      temp_x = randint(0, (SCREEN_WIDTH-BLOCK_SIZE)/BLOCK_SIZE) * BLOCK_SIZE
      temp_y = randint(0, (SCREEN_HEIGHT-BLOCK_SIZE)/BLOCK_SIZE) * BLOCK_SIZE

    self.x = temp_x
    self.y = temp_y