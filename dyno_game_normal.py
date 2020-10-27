import numpy as np
import pyautogui as pg
import keyboard
from mss import mss
import time
import imutils
import cv2

BOUNDING_BOX = {'top': 205, 'left': 1026, 'width': 200, 'height': 55}

LOOKUP_POINT = (30, 0)

X_LIMIT = 0

sct = mss()

is_once = True

time.sleep(0.1)

while True:
	image = np.array(sct.grab(BOUNDING_BOX))
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

	gray = cv2.GaussianBlur(gray, (9, 9), 0)
	edge = cv2.Canny(gray, 170, 225)
		
	edge = cv2.dilate(edge, None, iterations=5)

	cnts, _ = cv2.findContours(edge.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

	if len(cnts) > 0:
		for c in cnts:
			x, y, w, h = cv2.boundingRect(c)

			if x > 150 and is_once == True:
				dist = x 
				is_once = False
			if x == 0 and is_once == False:
				is_once = True

			# cv2.rectangle(image, (x, y), (x+w, y+h), (0, 0, 255), 2)

			front_cx, front_cy = x, y + (h // 2)

			xdist_to_lookup = front_cx - LOOKUP_POINT[1]
			ydist_to_lookup = LOOKUP_POINT[0] - front_cy

			if xdist_to_lookup <= X_LIMIT and ydist_to_lookup < 10:
				pg.press("up")

			elif xdist_to_lookup <= X_LIMIT and ydist_to_lookup > 10 and ydist_to_lookup < 18:
				pg.keyDown("down")
				time.sleep(delay)
				pg.keyUp("down")

			else:
				pass

	# cv2.imshow("screen", image)
	
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

