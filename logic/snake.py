from logic.utils.vec2 import Vec2

class Snake:
	def __init__(self, initDir):
		self.body = [Vec2(0, 0),                               # head
		             Vec2((-1) * initDir.r, (-1) * initDir.c)] # tail
		self.size = len(self.body)
		self.direction = initDir

	def goRight(self): # turns direction 90 degrees clockwise
		r = self.direction.r
		c = self.direction.c
		self.direction.r = c
		self.direction.c = (-1) * r

	def goLeft(self): # turns direction 90 degrees counter clockwise
		r = self.direction.r
		c = self.direction.c
		self.direction.r = (-1) * c
		self.direction.c = r

	def update(self, grow = False):
		self.growBody(grow) # increases size, if grow is True
		self.moveBody() # take a step forward
		return self.shiftAndCheckIfSelfHit() # check if self hit

	def isInsideBody(self, pos):
		for k in range(self.size):
			if self.body[k].c == pos.c and \
			   self.body[k].r == pos.r:
				return True
		return False

	# private method
	def growBody(self, grow = False):
		if grow:
			self.body.append(Vec2(0, 0)) # adds a dummy at the tail
			self.size += 1               # increases size			

	# private method
	def moveBody(self):
		for k in range(self.size - 1):
			p = self.size - k - 1
			self.body[p].r = self.body[p-1].r
			self.body[p].c = self.body[p-1].c
		self.body[0].update(self.direction)

	# private method
	def shiftAndCheckIfSelfHit(self):
		hitSelf = False
		shift = Vec2((-1) * self.direction.r,
			         (-1) * self.direction.c)
		for k in range(self.size):
			self.body[k].update(shift)
			if k != 0 and self.isAtHead(k):
				hitSelf = True
		return hitSelf

	# private method
	def isAtHead(self, k):
		return (self.body[k].r == 0 and \
			    self.body[k].c == 0)
