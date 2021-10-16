# https://stackoverflow.com/questions/10443295/combine-3-separate-numpy-arrays-to-an-rgb-image-in-python
# https://www.kaggle.com/vlasoff/beginner-s-guide-nn-with-multichannel-input
# https://towardsdatascience.com/build-your-own-convolution-neural-network-in-5-mins-4217c2cf964f
# https://jhui.github.io/2017/03/16/CNN-Convolutional-neural-network/
# https://towardsdatascience.com/building-a-convolutional-neural-network-cnn-in-keras-329fbbadc5f5

from rl.agent.memory          import Memory
from rl.state.rl_state        import RLState
from rl.state.rl_state_mapper import RLStateMapper

import random
import numpy as np

class Agent:
	def __init__(self, rows, cols, actions, learning_rate, gamma, max_replay, eps_info):
		self.lr = learning_rate
		self.max_replay = max_replay
		self.g = gamma
		self.actions_map = actions

		self.epsilon  = eps_info.start
		self.eps_rate = eps_info.rate
		self.eps_min  = eps_info.minimum

		self.state_mapper = RLStateMapper()
		self.brain = self.create_brain(rows, cols)
		self.memory = Memory(max_replay)

		self.curr_state = None
		self.prev_state = None

	def update_epsilon(self):
		self.epsilon *= self.eps_rate
		if self.epsilon < self.eps_min:
			self.epsilon = self.eps_min

	def epsilon_greedy(self):
		chance = random.uniform(0.0, 1.0)
		if chance >= self.epsilon:
			return -1
		return int(len(self.actions_map) * (chance/self.epsilon))

	def act(self, state):
		rd_action = self.epsilon_greedy()
		if rd_action >= 0:
			return rd_action
		return np.argmax(self.brain.predict(state))

	def add_experience(self, action, reward, next_state):
		self.curr_state = self.state_mapper.get_index(RLState(next_state))
		if self.prev_state != None:
			# n = 1
			# if reward > 0.0:
			# 	n = 100
			# while n > 0:
			# 	self.memory.add_experience(self.prev_state, action, reward, self.curr_state)
			# 	n -= 1
			self.memory.add_experience(self.prev_state, action, reward, self.curr_state)
		self.prev_state = self.curr_state

	def memory_size(self):
		return self.memory.size()

	def experience_replay(self, batch_size):
		minibatch = self.memory.get_sample(batch_size)
		states, targets = [], []
		for transition in minibatch:
			state = self.state_mapper.get_state(transition[0])
			action = transition[1]
			reward = transition[2]
			next_state = self.state_mapper.get_state(transition[3])
			
			target = self.brain.predict(state)
			target[0][action] = reward + self.g * np.max(self.brain.predict(next_state)[0])

			states.append(state[0])
			targets.append(target[0])

		history = self.brain.fit(np.array(states), np.array(targets), epochs=10, verbose=0)
		return history.history['loss'][0]		

	def create_brain(self, rows, cols):
	    from keras import layers, activations
	    from keras import optimizers, losses
	    from keras.models import Sequential
	    from keras.layers.normalization import BatchNormalization

	    model = Sequential()
	    model.add(layers.Conv2D(filters = 8,                   \
	                            kernel_size = (3, 3),          \
	                            strides = (2, 2),              \
	                            padding = 'same',              \
	                            activation = activations.relu, \
	                            bias = False,                  \
	                            input_shape = (rows, cols, 3)))
	                            # input_shape = (rows, cols, 1)))
	    model.add(BatchNormalization())

	    # model.add(layers.AveragePooling2D(pool_size = (2, 2), \
	    #                                   strides = (2, 2)))

	    model.add(layers.Conv2D(filters = 8,          \
	                            kernel_size = (3, 3), \
	                            strides = (2, 2),     \
	                            padding = 'same',              \
	                            bias = True,
	                            activation = activations.relu))

	    # model.add(layers.AveragePooling2D(pool_size = (2, 2), \
	    #                                   strides = (2, 2)))

	    # model.add(layers.Conv2D(filters = 8,          \
	    #                         kernel_size = (3, 3), \
	    #                         strides = (2, 2),     \
	    #                         activation = activations.relu))

	    model.add(layers.Flatten())

	    model.add(layers.Dense(units = 64, \
	                           activation = activations.relu))

	    model.add(layers.Dense(units =  3, \
	                           activation = activations.softmax))

	    model.compile(loss=losses.mse, optimizer=optimizers.Adam(lr=self.lr))
	    # model.summary()

	    return model

	def save(self, name):
		self.brain.model.save_weights(name)

	def load(self, name):
		self.brain.load_weights(name)
