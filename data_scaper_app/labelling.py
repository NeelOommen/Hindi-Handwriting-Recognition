import tkinter as tk
import os
import sys

sys.path.insert(0,'../Hindi-Handwriting-Recognition/')

from functools import partial
from tkinter import Canvas
from tkinter import *
from PIL import ImageTk, Image
from utility.unicode_list import hindi_unicode_characters
from os import listdir
from os.path import isfile, join


thumbnail_width = 200
label_dict = {}
file_list = None
current_img = ''

canvas_ref = None

img_temp = None


def indexConvertor(i, j, keysPerRow):
    index = (i*keysPerRow) + j
    return index


def load_file_names(manager):
    global file_list

    cache_path = manager.getOutputPath()
    flist = [f for f in listdir(cache_path) if isfile(join(cache_path, f))]
    file_list = flist.copy()


def button_callback(manager, character):
    global current_img

    label_dict[current_img] = character

    print(label_dict)
    nextImage(manager)


def nextImage(manager):   
    global file_list
    global current_img

    cache_path = manager.getOutputPath()
    print(cache_path)

    current_picture = file_list.pop(0)
    current_img = current_picture

    img = Image.open(manager.getOutputPath() + current_picture)
    #resize for better viewing
    width, height = img.size
    wpercent = (thumbnail_width/float(width))
    new_height = int(float(wpercent) * float(height))
    img = img.resize((thumbnail_width, new_height), Image.Resampling.LANCZOS)
    img = ImageTk.PhotoImage(img)
    manager.setImgCache(img)
    img_temp = img
    canvas_ref.create_image(0, 0, anchor=NW, image=img)



def mappingPopulate(f, manager):
    global canvas_ref
    load_file_names(manager)

    #Image Preview
    canvas = Canvas(f, width=200, height=350)
    canvas.grid(row=1, column=0, padx=5, pady=10)
    canvas_ref = canvas

    nextImage(manager)

    #description label
    description_label = tk.Label(f, text='Please select the correct labels for each character')
    description_label.grid(row=0, column=0, padx=10, pady=10)

    #create the "keyboard"
    for i in range(0, 8, 1):
        for j in range(0, 10, 1):
            index = indexConvertor(i,j,10)
            if(index < len(hindi_unicode_characters)):
                temp_button = tk.Button(f, text=hindi_unicode_characters[index], height=2, width=3, command=partial(button_callback, manager, hindi_unicode_characters[index]))
                temp_button.grid(row=i+2, column=j+1, padx=5, pady=5)