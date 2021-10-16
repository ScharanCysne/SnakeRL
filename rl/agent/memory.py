import random

class Memory:
	def __init__(self, max_size):
		self.queue = []
		self.max_size = max_size

	def add_experience(self, init_state, action, reward, next_state):
		self.queue.append((init_state, action, reward, next_state))
		if self.size() > self.max_size:
			self.queue.pop(0)

	def get_sample(self, size):
		return random.sample(self.queue, size)

	def size(self):
		return len(self.queue)
