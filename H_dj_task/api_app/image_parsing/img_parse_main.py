from rest_framework.response import Response
from api_app import serializers
from rest_framework import status
from PIL import Image
from django.conf import settings
import os
import numpy as np
import cv2
from imutils import contours
from skimage import measure
import numpy as np
import argparse
import imutils
import pytesseract


def count_signature(img):
    # threshold
    signatures = 0
    th, threshed = cv2.threshold(img, 100, 255,
                                cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    # findcontours
    cnts = cv2.findContours(threshed, cv2.RETR_LIST,
                            cv2.CHAIN_APPROX_SIMPLE)[-2]
    # filter by area
    s1 = 3
    #s2 = 20
    xcnts = []
    
    for cnt in cnts:
        if s1 < cv2.contourArea(cnt):
            signatures = signatures+1
            xcnts.append(cnt)
    return signatures

def text_recognition(image):
    preprocess = "thresh"

    # загрузить образ и преобразовать его в оттенки серого
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # проверьте, следует ли применять пороговое значение для предварительной обработки изображения
    # if preprocess == "thresh":
    #     gray = cv2.threshold(gray, 100, 255,
    #         cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    # если нужно медианное размытие, чтобы удалить шум
    # elif preprocess == "blur":
    #     gray = cv2.medianBlur(gray, 3)

    # сохраним временную картинку в оттенках серого, чтобы можно было применить к ней OCR

    filename = "{}.png".format(os.getpid())
    cv2.imwrite(filename, gray)

    # загрузка изображения в виде объекта image Pillow, применение OCR, а затем удаление временного файла
    text = pytesseract.image_to_string(Image.open(filename),lang='rus')
    os.remove(filename)
    return text
    

def get_sights(obj):
    #img = Image.open(obj.image)

    image = cv2.imread(obj.image.path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    lower = np.array([90, 38, 0])
    upper = np.array([145, 255, 255])
    mask = cv2.inRange(image, lower, upper)
    mask = cv2.blur(mask,(50,50))

    # mask = cv2.bitwise_not(mask)
    thresh = cv2.erode(mask, None, iterations=2)
    thresh = cv2.dilate(thresh, None, iterations=4)
    mask = cv2.addWeighted( mask, 64, mask, 0, 64)

    signatures_num=(count_signature(mask))
   
    obj.sigh_number = signatures_num
    obj.parse_text = text_recognition(image)
    obj.save()
    response = {"status_code": status.HTTP_200_OK,
                     "Подписи":  obj.sigh_number,
                     "Created" : obj.req_time,
                    } 

    return Response(response)








