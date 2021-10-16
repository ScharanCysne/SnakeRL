from logic.gameinfo   import GameInfo
from logic.gameboard  import GameBoard
from gui.guiinfo      import GUIInfo
from gui.guimanager   import GUIManager
from constants        import *

# Environment Settings
rows = 11
cols = 15

gameInfo = GameInfo(rows = rows,
	                cols = cols,
	                startPos = (rows//2, cols//4),
	                startDir = RIGHT)

guiInfo = GUIInfo(rows = rows,
	              cols = cols,
	              side = 35,
	              space = 3,
	              offset = (3, 3),
	              name = ':: Manga Snake ::')
# - - - - -


guiManager = GUIManager(guiInfo)
gameBoard  = GameBoard(gameInfo)


# Main Loop
done = False
while (not done):
	curr  = gameBoard.update()
	state = gameBoard.getState()

	if curr.hitWall or curr.hitSelf:
		gameBoard.reset()

	guiManager.update(state)
	guiManager.show()
	key = guiManager.waitKey(100)

	if key == K_ESC:
		done = True
	elif key == K_A:
		gameBoard.goLeft()
	elif key == K_D:
		gameBoard.goRight()
# - - - - -


guiManager.finish()

# Q-learning | SARS	 | Off-policy | Q-value
# SARSA	     | SARSA | On-policy  | Q-value
