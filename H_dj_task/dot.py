
import numpy as np
import cv2
from imutils import contours
from skimage import measure
import numpy as np
import argparse
import imutils
# reading the image in grayscale mode
gray = cv2.imread('afsdffdsds.jpg', 0)

# threshold
th, threshed = cv2.threshold(gray, 100, 255,
                             cv2.THRESH_BINARY | cv2.THRESH_OTSU)

# findcontours
cnts = cv2.findContours(threshed, cv2.RETR_LIST,
                        cv2.CHAIN_APPROX_SIMPLE)[-2]
# filter by area
s1 = 3
s2 = 20
xcnts = []
df = 0
for cnt in cnts:
    if s1 < cv2.contourArea(cnt):
        df = df+1
        xcnts.append(cnt)
print("Images found ->",df)
