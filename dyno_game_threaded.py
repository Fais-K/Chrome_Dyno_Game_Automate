import numpy as np
import pyautogui as pg
from threading import Thread
from mss import mss
import time
import imutils
import cv2
from queue import Queue

FIXED_DISTANCE = 75

def grab_screen(BOUNDING_BOX, sct, q):
	while True:
		image = np.array(sct.grab(BOUNDING_BOX))
		gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

		blur = cv2.GaussianBlur(gray, (9, 9), 0)

		edge = cv2.Canny(blur, 170, 225)
		edge = cv2.dilate(edge, None, iterations=5)

		cnts, _ = cv2.findContours(edge.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

		q.put(cnts)

def find_delay_and_action(DISTANCE, LOOKUP_POINT, is_once, delay_and_action, q):
	while True:
		cnts = q.get()
		if len(cnts) > 0:
			x, y, w, h = cv2.boundingRect(cnts[0])

			if x > 175 and is_once == True:
				initial_time = time.time()
				dist = x 
				is_once = False

			if x == 0 and is_once == False:
				time_taken = time.time()-initial_time

				front_cy = int(y + h / 2)

				ydist_to_lookup = LOOKUP_POINT[0] - front_cy

				if ydist_to_lookup < 10:
					action = "UP"

				if ydist_to_lookup > 10 and ydist_to_lookup < 18:
					action = "DOWN"

				is_once = True
				speed = dist/time_taken

				time_delay = FIXED_DISTANCE/speed
				time_delay = round(time_delay, 3)

				delay_and_action.put((time_delay, action))
				# break

	# cv2.imshow("screen", edge)

	# if cv2.waitKey(1) & 0xFF == ord('q'):
	# 	break

def perform_action(delay_and_action):
	while True:
		if delay_and_action.qsize() > 0:
			delay, button = delay_and_action.get()
			print("count", delay_and_action.qsize())

			if button == "UP":
				time.sleep(delay)
				pg.press("up")
				# break

			if button == "DOWN":
				time.sleep(delay)
				pg.keyDown("down")
				time.sleep(0.1)
				pg.keyUp("down")
				# break


if __name__ == '__main__':

	BOUNDING_BOX = {'top': 205, 'left': 1026, 'width': 200, 'height': 55}

	sct = mss()

	DISTANCE = 600
	LOOKUP_POINT = (30, 0)
	is_once = True

	delay_and_action = Queue()
	q = Queue()

	# lock = threading.Lock()

	t1 = Thread(target=grab_screen, args=(BOUNDING_BOX, sct, q))
	t2 = Thread(target=find_delay_and_action, args=(DISTANCE, LOOKUP_POINT, is_once, delay_and_action, q))
	t3 = Thread(target=perform_action, args=(delay_and_action,))

	t1.start()
	t2.start()
	t3.start()

	# t1.join()
	# t2.join()
	# t3.join()


	# cv2.imshow("screen", image)
	
	# if cv2.waitKey(1) & 0xFF == ord('q'):
	# 	break

