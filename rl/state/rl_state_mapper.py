from rl.state.utils.utils import state_to_numpy

class RLStateMapper:
	def __init__(self):
		self.index = 0
		self.state_to_index = {}
		self.index_to_state = {}

	def get_index(self, rl_state):
		if rl_state.state in self.state_to_index:
			return self.state_to_index[rl_state.state]

		self.state_to_index[rl_state.state] = self.index
		self.index_to_state[self.index] = rl_state
		self.index += 1

		return self.index-1

	def get_state(self, index):
		if index in self.index_to_state:
			return state_to_numpy(self.index_to_state[index].state)
		return None
