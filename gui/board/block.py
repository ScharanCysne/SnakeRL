from gui.utils.utils import drawRectangle

class Block:
	def __init__(self, side, center, color):
		self.side = side
		self.center = center
		self.topLeft = (self.center[1] - self.side//2,
			            self.center[0] - self.side//2)
		self.botRight = (self.center[1] + self.side//2,
			             self.center[0] + self.side//2)
		self.setColor(color)

	def stamp(self, img):
		drawRectangle(img, self.topLeft, self.botRight, self.color)

	def setColor(self, color):
		self.color = color
