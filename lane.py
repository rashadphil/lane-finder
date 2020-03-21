import cv2
import numpy as np

def canny(img):
    gray_img = cv2.cvtColor(lane_img, cv2.COLOR_RGB2GRAY) #converts image to grayscale
    blur = cv2.GaussianBlur(gray_img, (5,5), 0) #GaussianBlur to reduce noise
    canny = cv2.Canny(blur, 50, 150) #outlines strongest gradients in image
    return canny

def region(img): #fills in region of street
    height = img.shape[0]
    polygons = np.array([[(200,height), (1100, height), (550, 250)]])
    mask = np.zeros_like(img)
    cv2.fillPoly(mask, polygons, 255)
    return mask

img = cv2.imread("test_image.jpg")
lane_img = np.copy(img)
canny = canny(lane_img)

cv2.imshow("result", region(canny))
cv2.waitKey(0)
