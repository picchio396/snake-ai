import numpy as np
import pygame
from pygame.locals import (
KEYDOWN,
K_ESCAPE,
QUIT
)

from controller.snake import Snake, Food
import constants

class SnakeEnv():

	def __init__(self):
		# Initialize pygame
		pygame.init()
		self.screen = pygame.display.set_mode((constants.SCREEN_WIDTH + 61, constants.SCREEN_HEIGHT + 1))
		self.clock = pygame.time.Clock() 

		self.state = self.reset()

	'''
	# must go off danger function in snake
	# might have to decrease state (remove danger bins)

	def look_ahead(self, action):
		if (action == 0):
			# compute reward
		elif (action == 1):
			# compute reward
		elif (action == 2):
			# compute reward
	'''

	def step(self, action):
		for event in pygame.event.get():
			if event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					self.done = True
				elif event.type == QUIT:
					self.done = True
		
		if(action == 0):
			self.snake.moveUp()
		if(action == 1):
			self.snake.moveDown()
		if(action == 2):
			self.snake.moveRight()
		if(action == 3):
			self.snake.moveLeft()

		self.render()
		self.snake.update()
		# input('\n')
		state = self.getState()

		lost, reward = self.snake.collision(self.food)

		if (lost):
			# print("gg")
			# print("Score: " + str(self.snake.score))
			self.done = True

		self.clock.tick(constants.CLOCK)
		return [ state , reward, self.done, self.snake.score ]

	def reset(self):
		self.done = False
		self.reward = constants.REWARD_NULL
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

	def display_ui(self, score, record):
		myfont = pygame.font.SysFont('Segoe UI', 20)
		myfont_bold = pygame.font.SysFont('Segoe UI', 20, True)
		text_score = myfont.render('SCORE: ', True, (0, 0, 0))
		text_score_number = myfont.render(str(score), True, (0, 0, 0))
		text_highest = myfont.render('HIGHEST SCORE: ', True, (0, 0, 0))
		text_highest_number = myfont_bold.render(str(record), True, (0, 0, 0))

		self.screen.blit(text_score, (45, 440))
		self.screen.blit(text_score_number, (120, 440))
		self.screen.blit(text_highest, (190, 440))
		self.screen.blit(text_highest_number, (350, 440))

	# State is given by relative fruit position and relative tail position
	def getState(self):
		# Reset
		isSnakeRight = False
		isSnakeLeft = False
		isSnakeUp = False
		isSnakeDown = False

		isFoodRight = False
		isFoodLeft = False
		isFoodUp = False
		isFoodDown = False

		isDangerFront = False
		isDangerLeft = False
		isDangerRight = False

		# rel_food = [self.snake.body[0][0] - self.food.position[0], self.snake.body[0][1] - self.food.position[1]]
		# rel_tail = [self.snake.body[0][0] - self.snake.body[-1][0], self.snake.body[0][1] - self.snake.body[-1][1]]

		# going rigth
		if self.snake.direction == [1, 0]:
			isSnakeRight =  True
			# food left or right
			if self.snake.body[0][1] - self.food.position[1] > 0:
				isFoodLeft = True
			elif self.snake.body[0][1] - self.food.position[1] < 0:
				isFoodRight = True
			#food up or down
			if self.snake.body[0][0] - self.food.position[0] > 0:
				isFoodDown = True
			elif self.snake.body[0][0] - self.food.position[0] < 0:
				isFoodUp = True

		# going left
		if self.snake.direction == [-1, 0]:
			isSnakeLeft = True
			# food left or right
			if self.snake.body[0][1] - self.food.position[1] < 0:
				isFoodLeft = True
			elif self.snake.body[0][1] - self.food.position[1] > 0:
				isFoodRight = True
			#food up or down
			if self.snake.body[0][0] - self.food.position[0] < 0:
				isFoodDown = True
			elif self.snake.body[0][0] - self.food.position[0] > 0:
				isFoodUp = True

		# going up
		if self.snake.direction == [0,-1]:
			isSnakeUp = True
			# food left or right
			if self.snake.body[0][0] - self.food.position[0] > 0:
				isFoodLeft = True
			elif self.snake.body[0][0] - self.food.position[0] < 0:
				isFoodRight = True
			#food up or down
			if self.snake.body[0][1] - self.food.position[1] < 0:
				isFoodDown = True
			elif self.snake.body[0][1] - self.food.position[1] > 0:
				isFoodUp = True

		# going down
		if self.snake.direction == [0,1]:
			isSnakeDown = True
			# food left or right
			if self.snake.body[0][0] - self.food.position[0] < 0:
				isFoodLeft = True
			elif self.snake.body[0][0] - self.food.position[0] > 0:
				isFoodRight = True
			#food up or down
			if self.snake.body[0][1] - self.food.position[1] > 0:
				isFoodDown = True
			elif self.snake.body[0][1] - self.food.position[1] < 0:
				isFoodUp = True


		isDangerFront = self.snake.danger('front')
		isDangerLeft = self.snake.danger('left')
		isDangerRight = self.snake.danger('right')

		# self.printState([
		# 	isSnakeRight,
		# 	isSnakeLeft,
		# 	isSnakeUp,
		# 	isSnakeDown,
		# 	isFoodRight,
		# 	isFoodLeft,
		# 	isFoodUp,
		# 	isFoodDown,
		# 	isDangerFront,
		# 	isDangerLeft,
		# 	isDangerRight
		# ])

		bin_string = str(int(isSnakeRight == True)) + str(int(isSnakeLeft == True)) + str(int(isSnakeUp == True)) + str(int(isSnakeDown == True)) + str(int(isFoodRight == True)) + str(int(isFoodLeft == True)) + str(int(isFoodUp == True)) + str(int(isFoodDown == True)) + str(int(isDangerFront == True)) + str(int(isDangerLeft == True)) + str(int(isDangerRight == True))

		return int(bin_string, 2) 

	def printState(self, state):
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
		".format(state[0], state[1], state[2], state[3], state[4], state[5], state[6], state[7], state[8], state[9], state[10]),
		end="\r"
		)
