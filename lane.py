import cv2
import numpy as np

def canny(img):
    gray_img = cv2.cvtColor(lane_img, cv2.COLOR_RGB2GRAY) #converts image to grayscale
    blur = cv2.GaussianBlur(gray_img, (5,5), 0) #GaussianBlur to reduce noise
    canny = cv2.Canny(blur, 50, 150) #outlines strongest gradients in image
    return canny

def display_lines(img, lines): #displays detected lines
    line_img = np.zeros_like(img)
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line.reshape(4)
            cv2.line(line_img, (x1, y1), (x2, y2), (255, 0, 0), 10)

    return line_img

def region(img): #fills in region of street
    height = img.shape[0]
    polygons = np.array([[(200,height), (1100, height), (550, 250)]])
    mask = np.zeros_like(img)
    cv2.fillPoly(mask, polygons, 255)
    masked_image = cv2.bitwise_and(img, mask) #highlights only road lines by checking for similarities between triangle mask and original image with all lines
    return masked_image

img = cv2.imread("test_image.jpg")
lane_img = np.copy(img)
canny = canny(lane_img)

cropped_img = region(canny)
lines = cv2.HoughLinesP(cropped_img, 2, np.pi/180, 100, np.array([]), minLineLength= 40, maxLineGap=5) #detects straight lines in image
lines_img = display_lines(lane_img, lines)
cv2.imshow("result", lines_img)
cv2.waitKey(0)
