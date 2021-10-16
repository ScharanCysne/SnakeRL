from rl.state.utils.constants import *

import numpy as np

def state_to_numpy(state):
	rows = len(state)
	cols = len(state[0])

	red   = np.zeros((rows, cols))
	green = np.zeros((rows, cols))
	blue  = np.zeros((rows, cols))

	# ret = np.zeros((rows, cols))

	for row in range(rows):
		for col in range(cols):
			s = state[row][col]
			if s == 'h':
				red[row][col] = 1.0
			elif s == 's':
				green[row][col] = 1.0
			elif s == 'w':
				blue[row][col] = 1.0
			elif s == 'f':
				blue[row][col] = 1.0
			# if s == 'h':
			# 	ret[row][col] = 0.25
			# elif s == 's':
			# 	ret[row][col] = 0.50
			# elif s == 'w':
			# 	ret[row][col] = 0.75
			# elif s == 'f':
			# 	ret[row][col] = 1.00

	# should multiply by 256?
	return np.dstack((red, green, blue)).reshape(-1, rows, cols, 3)
	# return ret.reshape(-1, rows, cols, 1)
