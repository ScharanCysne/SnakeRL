from gui.gui_info      import GUIInfo
from gui.gui_manager   import GUIManager
from logic.game_board  import GameBoard

from rl.agent.epsilon     import EpsilonInfo
from rl.agent.agent       import Agent
from rl.state.utils.utils import state_to_numpy

from constants import *

import random
import cv2
import numpy             as np
import matplotlib.pyplot as plt

rows = 7
cols = 7

guiInfo = GUIInfo(rows = rows,
	              cols = cols,
	              side = 35,
	              space = 3,
	              offset = (3, 3),
	              name = ':: Manga Snake ::')


def runStep(game_board, action):
	if actions_map[action] == 'LEFT':
		game_board.goLeft()
	elif actions_map[action] == 'RIGHT':
		game_board.goRight()
	else: # action == 'S', straight
		pass

	game_state = game_board.update()
	next_state = game_board.getState()

	return (game_state, next_state)


name = '255_train.h5'

actions_map = {0:'LEFT',
               1:'STRAIGHT',
               2:'RIGHT'}

guiManager = GUIManager(guiInfo)
game_board = GameBoard(rows, cols)

episodes = 1000
steps = 200
eps_info = EpsilonInfo(0.00, 0.00, 0.00)

agent = Agent(rows + 2,
	          cols + 2,
	          actions_map, 0.0, 0.0, 0, eps_info)

agent.load('save/' + name)

# Main Loop
done = False

for w in range(episodes):
	if done:
		break

	game_board.reset()

	foodEaten = 0
	wallHitten = 0
	bodyHitten = 0

	for v in range(steps):
		if done:
			break

		curr_state = state_to_numpy(game_board.getState())
		action = agent.act(curr_state)

		result, next_state = runStep(game_board, action)

		guiManager.update(next_state)
		guiManager.show()
		key = guiManager.waitKey(100)

		if key == K_ESC:
			done = True

		if result.hitWall or result.hitSelf:
			if result.hitWall:
				wallHitten += 1
			if result.hitSelf:
				bodyHitten += 1
			game_board.reset()
			continue

		if result.gotFood:
			foodEaten += 1

	print('episode', w + 1)
	print('food:', foodEaten)
	print('wall:', wallHitten)
	print('body:', bodyHitten)
	print()

guiManager.finish()
