inf = float('inf')

class GameState:
	def __init__(self, gotFood = False, hitWall = False, hitSelf = False, distance = inf):
		self.gotFood  = gotFood
		self.hitWall  = hitWall
		self.hitSelf  = hitSelf
		self.distance = distance
