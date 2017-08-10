from tools.transform import four_point_transform
from tools import imutils
import numpy as np
import argparse
import cv2

refPts = []
clickCounts = 0
def click_callback(event, x, y, flag, param):
	global refPts, clickCounts
	if event == cv2.EVENT_LBUTTONUP:
		print(clickCounts)
		if clickCounts == 0:
			refPts = [(x, y)]
		elif clickCounts >= 4:
			return
		else:
			refPts.append((x, y))
		print("click on:"+str(x)+", "+str(y)+", refPts.type="+str(type(refPts)))
		cv2.circle(param, (x, y), 2, (0,255,0), 5)
		clickCounts += 1

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required = True)
args = vars(ap.parse_args())

image = cv2.imread(args["image"])
ratio = image.shape[0] / 500.0
orig = image.copy()
image = imutils.resize(image, height = 500)
cv2.namedWindow("image")
cv2.setMouseCallback("image", click_callback, image)

while True:
	cv2.imshow("image", image)
	key = cv2.waitKey(1) & 0xFF
	if key == ord("r"):
		clickCounts = 0
		cv2.setMouseCallback("image", click_callback, image)
	elif key == ord("s"):
		break
print(refPts)
print(type(refPts))
pts = np.array(refPts)
print(pts)
if len(refPts) == 4:
	warp = four_point_transform(orig, pts*ratio)
	#cv2.imshow("Original", image)
	cv2.imshow("Warped", warp)
	cv2.waitKey(0)
cv2.destroyAllWindows()