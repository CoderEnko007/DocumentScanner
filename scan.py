from tools import imutils
from tools.transform import four_point_transform
import numpy as np
import argparse
import cv2

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required = True)
args = vars(ap.parse_args())

#1.图片加载和裁剪
image = cv2.imread(args["image"])
orig = image.copy()
ratio = image.shape[0] / 500.0
print(image.shape[0])
image = imutils.resize(image, height = 500)
cv2.imshow("image", image)

#2.边缘识别
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#cv2.imshow("gray", gray)
gray = cv2.GaussianBlur(gray, (5, 5), 0)
#cv2.imshow("blur", gray)
edged = cv2.Canny(gray, 75, 100)
cv2.imshow("edged", edged)
cv2.waitKey(0)
cv2.destroyAllWindows()

(_, cnts, _) = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
'''
key：用列表元素的某个属性或函数进行作为关键字，有默认值，迭代集合中的一项,cv2.contoursArea计算轮廓面积;
reverse：排序规则. reverse = True  降序 或者 reverse = False 升序，有默认值。
返回值：是一个经过排序的可迭代类型，与iterable一样。
'''
cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:5]
print(type(cnts))

for c in cnts:
	#计算轮廓周长,True表示轮廓封闭
	peri = cv2.arcLength(c, True)
	#对轮廓进行多边形拟合, True表示拟合的轮廓封闭
	approx = cv2.approxPolyDP(c, 0.02 * peri, True)
	print("peri = %s" % peri)
	print("approx = %s" % approx)

	if len(approx) == 4:
		screenCnt = approx
		print("screenCnt = %s" % screenCnt)
		print(type(screenCnt))
		break

cv2.drawContours(image, [screenCnt], -1, (0, 255, 0), 2)
cv2.imshow("Outline", image)
cv2.waitKey(0)
cv2.destroyAllWindows()

warped = four_point_transform(orig, screenCnt.reshape(4, 2) * ratio)
#cv2.imshow("warped", warped)
cv2.imshow("orig", imutils.resize(orig, height = 500))
cv2.imshow("Scaned", imutils.resize(warped, height = 500))
cv2.waitKey(0)










