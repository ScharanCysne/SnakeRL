class GUIInfo:
	def __init__(self, rows, cols, side, space, offset, name):
		self.rows = rows
		self.cols = cols
		self.side = side
		self.space = space
		self.offset = offset
		self.windowName = name

	def computeWindowDimensions(self):
		HEIGHT = 2*self.offset[0] + (self.rows + 2)*(self.side + self.space) - self.space
		WIDTH  = 2*self.offset[1] + (self.cols + 2)*(self.side + self.space) - self.space
		return (HEIGHT, WIDTH)
