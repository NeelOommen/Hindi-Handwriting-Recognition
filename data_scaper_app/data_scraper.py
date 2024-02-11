import cv2
import numpy as np
import uuid
from areaCollector import collectArea

def segmentCharacters(manager):
    #load image
    img = cv2.imread(manager.getFileName())
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = cv2.bitwise_not(img)
    img = cv2.threshold(img , manager.lower_threshold, manager.upper_threshold, cv2.THRESH_BINARY)[1]

    #create a copy for final segmentation
    unprocessed_img_copy = img

    height, width = img.shape

    #apply blur
    blur_factor = manager.getBlurFactor()
    _kernel = np.ones((blur_factor, blur_factor), np.float32)/(blur_factor*blur_factor)
    img = cv2.filter2D(img, -1, kernel=_kernel)

    #get output path
    output_path = manager.getOutputPath()

    print(output_path)

    #carry out segmentation
    for i in range(0 , width, 1):
       for j in range(0 , height, 1):
            if img[j][i] > 0:
               left,top,right,bottom = collectArea(img, i, j)
               roi = unprocessed_img_copy[left:right, top:bottom]
               roi_name = uuid.uuid4().hex
               cv2.imwrite((output_path+roi_name+'.jpg'), roi)

