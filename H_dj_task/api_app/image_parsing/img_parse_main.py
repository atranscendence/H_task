from rest_framework.response import Response
from api_app import serializers
from rest_framework import status
from PIL import Image
from django.conf import settings
import os
import cv2
from imutils import contours
from skimage import measure
import numpy as np
import argparse
import imutils
import pytesseract
from api_app.image_parsing import sig_recog
from pdf2image import convert_from_path
import re

# from cStringIO import StringIO
# from django.core.files.base import ContentFile


def preprocess_img(img, mode):
    # sharpen iamge
    if mode == "thresh":
        gray = cv2.threshold(img, 100, 255,
                             cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    # use blure if we need to remove noice
    elif mode == "blur":
        gray = cv2.medianBlur(gray, 3)


def text_recognition(image):
    # style to mnipulate image if its bad qulity

    # Make sure there only 2 colors black and white
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # save tmp image in png for OCR
    filename = "{}.png".format(os.getpid())
    cv2.imwrite(filename, gray)

    # load image Pillow, use OCR, then delete tmp file.png
    text = pytesseract.image_to_string(Image.open(filename), lang='rus')
    os.remove(filename)
    return text


def get_sights(obj, doc_type, doc_format, inner_serializer):
    sigh_number = 0
    image = None

    # Convert if format is pdf
    if (doc_format == 'pdf'):
        pil_image = convert_from_path(obj.image.path, 500)[0]
        image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
    else:
        image = cv2.imread(obj.image.path)

    # Recongnise any text on document then look for words in it
    doc_text = text_recognition(image)
    words_num = len(re.findall(r'[а-яА-Я]+', doc_text))
    if (words_num < 5):
        # simple check documents by looking if there any words on image
        obj.delete()
        response = {"Message": 'Неправильный формат документа', }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    # Scan depend on type of document
    if (doc_type == 'Advanced'):
        # Use connected component analysis
        sig_mask = sig_recog.get_singnature_advanced(image)
        sigh_number = sig_recog.count_signature(sig_mask)
    elif (doc_type == 'Standart'):
        # Use color masking
        sig_mask = sig_recog.get_singnature_standart(image)
        sigh_number = sig_recog.count_signature(sig_mask)
    else:
        """only text recognition"""
        pass

    # save png for signature
    filename = "Sinatures_file_{}.png".format(
        obj.image.name.split('/')[-1].split('.')[0])
    filepath = os.path.join('uploads/docs', filename)
    cv2.imwrite(filepath, sig_mask)

    # get detail information from img and save them in model
    obj.sigh_number = sigh_number
    obj.parse_text = doc_text
    obj.sig_in_image = filepath

    obj.save()

    # build response
    response = {"Подписи": obj.sigh_number,
                "Изображение подписи": inner_serializer(obj).data['sig_in_image'],
                "Распознанный текст": obj.parse_text,
                }
    return Response(response, status=status.HTTP_200_OK)
