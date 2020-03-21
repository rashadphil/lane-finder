import cv2
import numpy as np

def make_coords(img, line_parameters):
    slope, intercept = line_parameters
    y1 = img.shape[0]
    y2 = int(y1 * (3/5))
    x1 = int((y1 - intercept)/slope)
    x2 = int((y2 - intercept)/slope)
    return np.array([x1, y1, x2, y2])



def avg_slope_int(img, lines): #used to fill in unfilled lines
    left_fit = []
    right_fit = []
    for line in lines:
        x1, y1, x2, y2 = line.reshape(4)
        parameters = np.polyfit((x1, x2), (y1, y2), 1)
        slope = parameters[0]
        intercept = parameters[1]
        if slope <0:
            left_fit.append((slope,intercept))
        else:
            right_fit.append((slope,intercept))
    left_fit_avg = np.average(left_fit, axis = 0)
    right_fit_avg = np.average(right_fit, axis =0)

    left_line = make_coords(img, left_fit_avg)
    right_line = make_coords(img, right_fit_avg)
    return np.array([left_line, right_line])



def canny(img):
    gray_img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY) #converts image to grayscale
    blur = cv2.GaussianBlur(gray_img, (5,5), 0) #GaussianBlur to reduce noise
    canny = cv2.Canny(blur, 50, 150) #outlines strongest gradients in image
    return canny

def display_lines(img, lines): #displays detected lines
    line_img = np.zeros_like(img)
    if lines is not None:
        for x1, y1, x2, y2 in lines:
            cv2.line(line_img, (x1, y1), (x2, y2), (255, 0, 0), 10)

    return line_img

def region(img): #fills in region of street
    height = img.shape[0]
    polygons = np.array([[(200,height), (1100, height), (550, 250)]])
    mask = np.zeros_like(img)
    cv2.fillPoly(mask, polygons, 255)
    masked_image = cv2.bitwise_and(img, mask) #highlights only road lines by checking for similarities between triangle mask and original image with all lines
    return masked_image

# img = cv2.imread("test_image.jpg")
# lane_img = np.copy(img)
# canny = canny(lane_img)
#
# cropped_img = region(canny)
# lines = cv2.HoughLinesP(cropped_img, 2, np.pi/180, 100, np.array([]), minLineLength= 40, maxLineGap=5) #detects straight lines in image
# avg_lines = avg_slope_int(lane_img, lines)
#
# lines_img = display_lines(lane_img, avg_lines)
#
# combo_img = cv2.addWeighted(lane_img, 0.8, lines_img, 1, 1) #combines line img and original img
# cv2.imshow("result", combo_img)
# cv2.waitKey(0)

cap = cv2.VideoCapture("test2.mp4")
while cap.isOpened(): #detects lines in a video
    _, frame = cap.read()
    canny_img = canny(frame)
    cropped_img = region(canny_img)
    lines = cv2.HoughLinesP(cropped_img, 2, np.pi/180, 100, np.array([]), minLineLength= 40, maxLineGap=5) #detects straight lines in image
    avg_lines = avg_slope_int(frame, lines)
    lines_img = display_lines(frame, avg_lines)
    combo_img = cv2.addWeighted(frame, 0.8, lines_img, 1, 1) #combines line img and original img
    cv2.imshow("result", combo_img)
    if cv2.waitKey(1) == ord('q'): break
cap.release()
cv2.destroyAllWindows()
