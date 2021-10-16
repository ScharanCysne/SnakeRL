import cv2

def RGBToBGR(color):
	return (color[2], color[1], color[0])

def drawRectangle(img, topLeft, botRight, color, thick = -1):
	cv2.rectangle(img, topLeft, botRight, RGBToBGR(color), thick)

def drawCircle(img, center, radius, color, thick = -1):
	cv2.circle(img, center, radius, RGBToBGR(color), thick)
