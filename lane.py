import cv2

img = cv2.imread("test_image.jpg")

cv2.imshow("result", img)
cv2.waitKey(0)
