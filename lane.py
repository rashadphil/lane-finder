import cv2
import numpy as np

img = cv2.imread("test_image.jpg")
lane_img = np.copy(img)

gray_img = cv2.cvtColor(lane_img, cv2.COLOR_RGB2GRAY) #converts image to grayscale

blur = cv2.GaussianBlur(gray_img, (5,5), 0) #GaussianBlur to reduce noise
cv2.imshow("result", blur)
cv2.waitKey(0)
