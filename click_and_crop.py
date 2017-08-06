import argparse
import cv2

refPtr = []
def click_and_drop(event, x, y, flag, param):
	global refPtr
	if event == cv2.EVENT_LBUTTONDOWN:
		refPtr = [(x, y)]
		print("start:("+str(x)+", "+str(y)+")")
	elif event == cv2.EVENT_LBUTTONUP:
		refPtr.append((x, y))
		print("end:("+str(x)+", "+str(y)+")")
		#第五个参数为thickness为边框的粗细
		cv2.rectangle(image, refPtr[0], refPtr[1], (255, 0, 0), 2)
		cv2.imshow("image", image)

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required = True)
args = vars(ap.parse_args())
print(type(args))

image = cv2.imread(args["image"])
clone = image.copy()
cv2.namedWindow("image")
cv2.setMouseCallback("image", click_and_drop)

while True:
	cv2.imshow("image", image)
	key = cv2.waitKey(1) & 0xFF
	if key == ord("r"):
		image = clone.copy()
	elif key == ord("c"):
		break
if len(refPtr) == 2:
	#这里提取ROI先指定y轴再指定x轴
	image = clone[refPtr[0][1]:refPtr[1][1], refPtr[0][0]:refPtr[1][0]]
	print("refPtr[0][1]="+str(refPtr[0][1])+", refPtr[1][1]="+str(refPtr[1][1])+", refPtr[0][0]="+str(refPtr[0][0])+", refPtr[1][0]="+str(refPtr[1][0]))
	cv2.imshow("ROI", image)
	cv2.waitKey(0)
cv2.destroyAllWindows()