import numpy as np
import keyboard
from mss import mss
import time
import imutils
import cv2

from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.keys import Keys

options = ChromeOptions()
options.add_argument("--start-maximized")

# session_id = "06410b0753cdbfc7ce2a9763bf357e2d"
# executor_url = "http://127.0.0.1:51249"


driver = webdriver.Chrome('/home/home/chrome_driver/chromedriver', chrome_options=options)

# driver = webdriver.Remote(command_executor=executor_url, desired_capabilities={})
# driver.session_id = session_id
driver.set_network_conditions(offline=True, latency=5, throughput=500 * 1024)

driver.get('https://www.google.com')
# driver.set_page_load_timeout(0)

# print(f'driver.command_executor._url: {driver.command_executor._url}')
# print(f'driver.session_id: {driver.session_id}')

driver.implicitly_wait(300)

# runner = driver.find_element_by_tag_name('body')

# print(runner.is_enabled())
# print(runner.is_displayed())



BOUNDING_BOX = {'top': 195, 'left': 720, 'width': 350, 'height': 100}


LOOKUP_POINT = (75, 0)

X_LIMIT = 0
sct = mss()

while True:
	image = np.array(sct.grab(BOUNDING_BOX))
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

	gray = cv2.GaussianBlur(gray, (5, 5), 0)
	edge = cv2.Canny(gray, 170, 225)
		
	edge = cv2.dilate(edge, None, iterations=2)

	cv2.imshow("edge", edge)

	cnts, _ = cv2.findContours(edge.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

	if len(cnts) > 0:

		for c in cnts:

			x, y, w, h = cv2.boundingRect(c)

			front_cx, front_cy = x, y + h // 2

			xdist_to_lookup = front_cx - LOOKUP_POINT[1]
			ydist_to_lookup = LOOKUP_POINT[0] - front_cy

			if xdist_to_lookup <= X_LIMIT and ydist_to_lookup <= 10:
				#driver.find_element_by_tag_name('body').send_keys(Keys.UP)
				keyboard.press_and_release("up")
				time.sleep(.1)
				# break

			elif xdist_to_lookup < 70 and ydist_to_lookup < 10:
				keyboard.press_and_release("down")
				time.sleep(.1)

			else:
				pass

	# cv2.imshow("screen", image)

	if cv2.waitKey(1) & 0xFF == ord('q'):
		break