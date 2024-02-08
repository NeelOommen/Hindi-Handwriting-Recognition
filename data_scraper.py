import cv2
import numpy as np
from utility import collectArea

file_name = 's1.jpg'

img = cv2.imread('src_images\\' + file_name)
img_demo = cv2.imread('src_images\\' + file_name)
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#img_demo = cv2.cvtColor(img_demo, cv2.COLOR_BGR2GRAY)
img = cv2.bitwise_not(img)
img = cv2.threshold(img, 85, 255, cv2.THRESH_BINARY)[1]

height, width = img.shape

print(f'{width} {height}')

#apply blur
blur_factor = 7
kernel = np.ones((blur_factor, blur_factor), np.float32)/(blur_factor*blur_factor)
img = cv2.filter2D(img, -1, kernel=kernel)
#img = cv2.blur(img, (blur_factor, blur_factor))

#crush white
# for i in range(0, width, 1):
#     for j in range(0, height, 1):
#          if img[j][i] != 0:
#             img[j][i] = 255

for i in range(0 , width, 1):
    for j in range(0 , height, 1):
         if img[j][i] > 0:
            left,top,right,bottom = collectArea(img, i, j)
            cv2.rectangle(img_demo, (top,left), (bottom,right), (0,0,255), 1)
            
#debug
f = open('dump.txt', 'w')
for i in range(0 , width, 1):
    for j in range(0 , height, 1):
        f.write(str(img[j][i]) + '\t')
    f.write('\n')
f.close()


cv2.imshow('test', img_demo)
#cv2.imshow('test2', img)
cv2.waitKey(0)