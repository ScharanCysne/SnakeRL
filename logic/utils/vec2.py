from logic.utils.utils import genRandInt

class Vec2:
	# represents a tuple (row, col) where
	# r is the row and c is the col
	def __init__(self, r, c):
		self.r = r
		self.c = c

	# @delta is a Vec2 object
	# updates r and c as
	#     r = r + dr
	#     c = c + dc
	# and returns a reference to itself
	def update(self, delta):
		self.r += delta.r
		self.c += delta.c
		return self

	# creates a copy of itself
	def copy(self):
		return Vec2(self.r, self.c)

def genRandVec2(MAX_R, MAX_C):
	return Vec2(genRandInt(MAX_R), genRandInt(MAX_C))
