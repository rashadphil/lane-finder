import cv2
import numpy as np

img = cv2.imread("test_image.jpg")
lane_img = np.copy(img)
gray_img = cv2.cvtColor(lane_img, cv2.COLOR_RGB2GRAY)
cv2.imshow("result", gray_img)
cv2.waitKey(0)
