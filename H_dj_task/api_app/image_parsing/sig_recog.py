import cv2
import numpy as np
from skimage import measure
from skimage.measure import label, regionprops
from skimage.color import label2rgb
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from scipy import ndimage
from skimage import morphology
import os


def get_singnature_advanced(img):
	"""
	Сonnected component analysis method to find signatures
	"""
	img = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)[1]  # ensure binary

	# connected component analysis by scikit-learn framework
	blobs = img > img.mean()
	blobs_labels = measure.label(blobs, background=1)

	the_biggest_component = 0
	total_area = 0
	counter = 0
	average = 0.0
	signs = 0

	for region in regionprops(blobs_labels):
		if region.area > 10:
			total_area = total_area + region.area
			counter = counter + 1
		# print region.area # (for debugging)
		# take regions with large enough areas
		if region.area >= 250:
			signs = signs + 1
			if (region.area > the_biggest_component):
				the_biggest_component = region.area

	average = (total_area / counter)

	# Modify depending on the size of image for better accuracy
	a4_constant = (((average / 84.0) * 250.0) + 100) * 1.5

	# remove the connected pixels are smaller than a4_constant
	b = morphology.remove_small_objects(blobs_labels, a4_constant)
	# save the the pre-version image
	filename = "pre_version{}.png".format(os.getpid())
	cv2.imwrite(filename, b)

	# read the pre-version
	img = cv2.imread(filename, 0)
	# ensure binary
	img = cv2.threshold(
		img, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
	img = cv2.bitwise_not(img)
	os.remove(filename)
	return img


def get_singnature_standart(img):
	"""
	Extract signature made by blue pencil in standart document
	"""
	# 
	image = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
	lower = np.array([90, 38, 0])
	upper = np.array([145, 255, 255])
	mask = cv2.inRange(image, lower, upper)

	return mask


def count_signature(img):
	ROI_number = 0
	# Make found signatures better visible
	mask = cv2.blur(img, (50, 50))
	mask = cv2.erode(mask, None, iterations=4)
	mask = cv2.dilate(mask, None, iterations=8)
	mask = cv2.addWeighted(mask, 64, mask, 0, 64)
	# Make sure there only 2 colors black and white
	_, blackAndWhiteImage = cv2.threshold(mask, 127, 255, cv2.THRESH_BINARY)

	# Count contours we found in that range
	cnts = cv2.findContours(
		blackAndWhiteImage, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	cnts = cnts[0] if len(cnts) == 2 else cnts[1]
	ROI_number = len(cnts)

	return ROI_number
