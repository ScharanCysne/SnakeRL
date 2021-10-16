class RLState:
	def __init__(self, board_state):
		self.state = []
		for line in board_state:
			self.state.append(''.join(line))
		self.state = tuple(self.state)
