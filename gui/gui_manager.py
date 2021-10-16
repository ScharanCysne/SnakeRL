from gui.board.gui_board import GUIBoard
from gui.screen          import Screen

class GUIManager:
	def __init__(self, info):
		self.board = GUIBoard(info)

		HEIGHT, WIDTH = info.computeWindowDimensions()
		self.screen = Screen(info.windowName, HEIGHT, WIDTH)

	def update(self, state):
		self.board.updateBoard(state)
		self.board.drawBoard(self.screen.image)

	def show(self):
		self.screen.updateWindow()

	def waitKey(self, delay):
		return self.screen.waitKey(delay)

	def finish(self):
		self.screen.destroyWindow()
