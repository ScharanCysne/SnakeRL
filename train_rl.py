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


def rewardFunc(gameState):
	if gameState.hitSelf:
		return -1.0
		# return -50.0

	if gameState.hitWall:
		return -1.0
		# return -50.0

	if gameState.gotFood:
		return 1.0
		# return 500.0

	# if gameState.distance < 6:
	# 	return (-1.0) * gameState.distance

	# return -6.0
	return -0.1


def runStep(game_board, reward_function, action):
	if actions_map[action] == 'LEFT':
		game_board.goLeft()
	elif actions_map[action] == 'RIGHT':
		game_board.goRight()
	else: # action == 'S', straight
		pass

	game_state = game_board.update()
	reward = reward_function(game_state)
	check_board = game_board.getState()

	return (game_state, reward, check_board)


show_gui = True

gamma = 0.98
max_replay = 5000
update_rate = 5

batch_size = 75
episodes = 3000000
steps = 50
name = 'train.h5'

actions_map = {0:'LEFT',
               1:'STRAIGHT',
               2:'RIGHT'}

guiManager = GUIManager(guiInfo)
game_board = GameBoard(rows, cols)

learning_rate = 0.0005
eps_info = EpsilonInfo(0.90, 0.90, 0.20)

agent = Agent(rows + 2,
	          cols + 2,
	          actions_map,
	          learning_rate,
	          gamma,
	          max_replay,
	          eps_info)

# agent.load('save/' + name)

history = []

# Main Loop
done = False
mean_acc_reward = 0.0

for w in range(episodes):
	if done:
		break

	game_board.reset()

	foodEaten = 0
	wallHitten = 0
	bodyHitten = 0
	acc_reward = 0.0

	for v in range(steps):
		if done:
			break

		curr_state = state_to_numpy(game_board.getState())
		action = agent.act(curr_state)

		result, reward, next_state = runStep(game_board, rewardFunc, action)

		acc_reward += reward

		if show_gui:
			guiManager.update(next_state)
			guiManager.show()
			key = guiManager.waitKey(1)
		else:
			key = (cv2.waitKey(1) & 0xFF)

		if key == K_ESC:
			done = True
		elif key == K_P:
			show_gui = not show_gui

		agent.add_experience(action, reward, next_state)

		if result.hitWall or result.hitSelf:
			if result.hitWall:
				wallHitten += 1
			if result.hitSelf:
				bodyHitten += 1
			game_board.reset()
			agent.curr_state = None
			agent.prev_state = None
			continue

		if result.gotFood:
			foodEaten += 1

		if agent.memory_size() > 2 * batch_size:
			agent.experience_replay(batch_size)

	agent.update_epsilon()
	history.append(acc_reward)
	mean_acc_reward += acc_reward

	print('episode', w + 1)
	print('food:', foodEaten)
	print('wall:', wallHitten)
	# print('body:', bodyHitten)
	print('eps:', round(agent.epsilon, 2))
	print('reward:', round(acc_reward, 2))
	print()

	if (w + 1) % update_rate == 0:
		plt.plot(history, 'b')
		plt.ylabel('Return')
		plt.savefig('save/' + 'dqn_training_' + str(w+1) + '.png', fig_format='png')
		agent.save('save/' + str(w+1) + '_' + name)

# - - - - -

guiManager.finish()
