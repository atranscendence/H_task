import numpy as np
import cv2
from imutils import contours
from skimage import measure
import numpy as np
import argparse
import imutils

image = cv2.imread('qwe.jpg')
image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
lower = np.array([90, 38, 0])
upper = np.array([145, 255, 255])
mask = cv2.inRange(image, lower, upper)
mask = cv2.blur(mask,(50,50))

# mask = cv2.bitwise_not(mask)
thresh = cv2.erode(mask, None, iterations=2)
thresh = cv2.dilate(thresh, None, iterations=4)
mask = cv2.addWeighted( mask, 64, mask, 0, 64)


cv2.imwrite('afsdffdsds.jpg', mask)