import cv2
import numpy as np

class Screen:
	def __init__(self, name, height, width, channels = 3):
		self.height = height
		self.width = width
		self.channels = channels
		self.image = np.zeros((self.height, self.width, self.channels))
		self.createWindow(name)

	def createWindow(self, name):
		cv2.namedWindow(name)
		self.name = name

	def updateWindow(self):
		cv2.imshow(self.name, self.image)

	def destroyWindow(self):
		cv2.destroyAllWindows()

	def waitKey(self, delay):
		return (cv2.waitKey(delay) & 0xFF)
