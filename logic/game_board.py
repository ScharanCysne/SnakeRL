from constants         import *
from logic.snake       import Snake
from logic.game_state  import GameState
from logic.utils.vec2  import Vec2, genRandVec2
from logic.utils.utils import genRandInt

class GameBoard:
	def __init__(self, rows, cols):
		self.rows = rows
		self.cols = cols
		self.snake = None
		self.snkHead = None
		self.snkInitDir = None
		self.snkInitPos = None
		self.food = None
		self.state = None
		self.directions = [LEFT, UP, RIGHT, DOWN]

	def set_init(self, startPos, startDir):
		self.snkInitPos = Vec2(startPos[0], startPos[1])
		self.snkInitDir = Vec2(startDir[0], startDir[1])

	def reset(self):
		self.set_init((1 + genRandInt(self.rows - 1), 
			           1 + genRandInt(self.cols - 1)),
		              self.directions[genRandInt(len(self.directions))])

		self.snake = Snake(self.snkInitDir.copy())
		self.snkHead = self.snkInitPos.copy()
		self.food = self.genFood()
		self.state = [['e' for j in range(self.cols + 2)] for i in range(self.rows + 2)]

	def goRight(self):
		self.snake.goRight()

	def goLeft(self):
		self.snake.goLeft()

	def update(self):
		direction = self.snake.direction
		self.snkHead.update(direction) # update head

		gotFood = self.byteFood() # check if got food
		hitSelf = self.snake.update(gotFood) # check if self hit
		hitWall = self.hitWall() # check if hit wall
		isDead = hitSelf or hitWall

		if (not isDead) and gotFood: # generate food, if possible
			self.food = self.genFood()

		dist = self.computeDistance()

		gameState = GameState(gotFood, \
			                  hitWall, \
			                  hitSelf, \
			                  dist)

		return gameState

	def getState(self):
		for i in range(self.rows + 2): 
			for j in range(self.cols + 2): 
				if i == 0 or i == self.rows + 1 or \
				   j == 0 or j == self.cols + 1:
					self.state[i][j] = 'w'
				else:
					self.state[i][j] = 'e'
				
		self.state[self.food.r + 1][self.food.c + 1] = 'f' # food

		hR = self.snkHead.r + 1
		hC = self.snkHead.c + 1

		snkBody = self.snake.body
		for k in snkBody: # snake
			self.state[hR + k.r][hC + k.c] = 's'
		self.state[hR][hC] = 'h'

		return self.state

	# private method
	def genFood(self):
		delta = Vec2((-1) * self.snkHead.r, 
			         (-1) * self.snkHead.c)

		def genCandidate(delta):
			candidate = genRandVec2(self.rows, self.cols)
			relativeCand = candidate.copy().update(delta)
			return (candidate, relativeCand)

		candidate, relativeCand = genCandidate(delta)
		while self.snake.isInsideBody(relativeCand):
			candidate, relativeCand = genCandidate(delta)

		return candidate

	# private method
	def byteFood(self):
		return (self.snkHead.r == self.food.r and 
			    self.snkHead.c == self.food.c)

	# private method
	def hitWall(self):
		return (self.snkHead.r < 0 or self.snkHead.r >= self.rows or
			    self.snkHead.c < 0 or self.snkHead.c >= self.cols)

	def computeDistance(self):
		return abs(self.snkHead.r - self.food.r) + abs(self.snkHead.c - self.food.c)
