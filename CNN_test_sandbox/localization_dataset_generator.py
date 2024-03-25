import random
import os
import PIL
import sys
import uuid
import csv
import threading
sys.path.insert(0,'../Hindi-Handwriting-Recognition/')

from utility.unicode_list import test_set_labels_only
from utility.iou import area_of_intersection
from os import listdir
from os.path import isfile, join

from PIL import Image, ImageFilter

width = 500
height = 500

num_samples = 1000

base_path = 'CNN_test_sandbox\Dataset\Train'
output_path = 'D:\GitHub\Hindi-Handwriting-Recognition\CNN_test_sandbox\Dataset\Local (Testing)'

min_num_characters = 30
max_num_characters = 45

grid_size = 7
cell_size = 68

#variation limits
min_degrees = -10
max_degrees = 10

m_min = -0.2
m_max = 0.2

max_blur_radius = 1

min_noise_pixels = 25
max_noise_pixels = 300

lock = threading.Lock()


#sample generator function
def create_sample(a_list, idx):
    print(f'started {idx}')
    global height
    global width
    #file name
    new_file_name = uuid.uuid4().hex
    new_file_name += '.jpg'
    #create canvas
    img = Image.new('RGB', (height, width), (0,0,0))

    #get number of samples
    num_chars = random.randint(min_num_characters, max_num_characters)

    #create a list of random characters of num_chars length
    char_list = random.sample(test_set_labels_only, 40)

    #iterate over list
    img_num = 0
    for c in char_list:
        #get list of available samples for the character
        char_path = base_path + '\\' + c
        char_files = [f for f in listdir(char_path) if isfile(join(char_path, f))]

        chosen_file_path = char_path + '\\' + random.choice(char_files)
        #print(chosen_file_path)

        #open the chosen image
        current_img = Image.open(chosen_file_path)

        #calculate coordinates
        i = img_num % 7
        j = img_num // 7

        #filters
        t_width, t_height = current_img.size
        #rotate
        deg = random.randint(min_degrees, max_degrees)
        current_img = current_img.rotate(deg, PIL.Image.NEAREST, expand=1)

        #skew
        m = random.uniform(m_min, m_max)
        xshift = abs(m) * t_width
        new_width = t_width + int(round(xshift))
        current_img = current_img.transform((new_width, t_height), Image.AFFINE, (1, m, -xshift if m > 0 else 0, 0, 1, 0), Image.BICUBIC)

        #blur
        radius = random.randint(0, max_blur_radius)
        current_img = current_img.filter(ImageFilter.GaussianBlur(radius=radius))

        #resizing
        chance = random.randint(0, 100)
        if chance > 75:
            base_width = new_width + random.randint(0, cell_size - new_width)
            wpercent = (base_width / float(new_width))
            hsize = int((float(t_height) * float(wpercent)))
            current_img = current_img.resize((base_width, hsize), Image.Resampling.LANCZOS)

        #final location
        t_width, t_height = current_img.size
        x_range = cell_size - t_width
        y_range = cell_size - t_height

        x = (i * cell_size) + random.randint(0, x_range)
        y = (j * cell_size) + random.randint(0, y_range)

        #paste image
        img.paste(current_img, (x,y))
        img_num += 1

        temp_dict = {'file_name': new_file_name, 'label': c, 'x1': x, 'y1': y, 'x2': x + t_width, 'y2': y + t_height}
        
        a_list.append(temp_dict)
        

    #noise
    num_noise_pixels = random.randint(min_noise_pixels, max_noise_pixels)
    for i in range(num_noise_pixels):
        tx = random.randint(0, width-1)
        ty = random.randint(0, height-1)
        img.putpixel((tx, ty), (255, 255, 255))

    #save and annotate file
    new_file_path = output_path + '\\' + new_file_name
    img.save(new_file_path)
    print(f'Done with {idx}')



#create dataset
if __name__ == '__main__':
    field_names = ['file_name', 'label', 'x1', 'y1', 'x2','y2']
    annotation_list = []

    threading_list = []

    for i in range(1000):
        temp = threading.Thread(target=create_sample, args=(annotation_list, i))
        threading_list.append(temp)
        temp.start()
        
    for i in range(len(threading_list)):
        threading_list[i].join()

    with open('D:\\GitHub\\Hindi-Handwriting-Recognition\\CNN_test_sandbox\\Dataset\\Local (Testing)\\annotations.csv', 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=field_names)
        writer.writerows(annotation_list)