from gui.board.block     import Block
from gui.utils.constants import BLACK, BROWN, RED, DARKGREEN, GREEN, GREY

class GUIBoard:
	def __init__(self, info):
		self.side = info.side
		self.space = info.space
		self.offset = info.offset
		self.rows = info.rows + 2
		self.cols = info.cols + 2
		self.mapping = {}
		self.initialiseMapping()
		self.createBoard()

	def updateBoard(self, state):
		for i in range(self.rows):
			for j in range(self.cols):
				self.board[i][j].setColor(self.mapping[state[i][j]])

	def drawBoard(self, img):
		for i in range(self.rows):
			for j in range(self.cols):
				self.board[i][j].stamp(img)

	# private method
	def initialiseMapping(self):
		self.mapping['e'] = GREY
		self.mapping['w'] = BROWN
		self.mapping['f'] = RED
		self.mapping['s'] = DARKGREEN
		self.mapping['h'] = GREEN

	# private method
	def createBoard(self):
		hSide = self.side // 2
		delta = self.side + self.space
		topLeft = (self.offset[0] + hSide, self.offset[1] + hSide)
		self.board = []
		
		for i in range(self.rows):
			currLine = []
			for j in range(self.cols):
				currLine.append(Block(self.side,
					                  (topLeft[0] + i * delta,
   				                  	   topLeft[1] + j * delta),
					                  self.mapping['e']))
			self.board.append(currLine)
