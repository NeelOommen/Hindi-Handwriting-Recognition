import tkinter as tk
import cv2
import sys

sys.path.insert(0,'../Hindi-Handwriting-Recognition/')

from functools import partial
from tkinter import Canvas
from tkinter import *
from PIL import ImageTk, Image
from utility.data_scraper import segmentCharacters

lower_limit_setter = None
upper_limit_setter = None
canvas_ref = None
manager_ref = None

def update_lower(limit):
    lower_limit_setter(int(limit))
    updateImage(canvas_ref, manager_ref)

def update_upper(limit):
    upper_limit_setter(int(limit))
    updateImage(canvas_ref, manager_ref)
    

def finalPreprocess(manager):
    segmentCharacters(manager)

    switcher = manager.returnLabellingSwitchFunction()
    switcher()

def updateImage(image_canvas, manager):
    img = manager.getImageCache()
    img = cv2.threshold(img, manager.lower_threshold, manager.upper_threshold, cv2.THRESH_BINARY)[1]
    imgtk = ImageTk.PhotoImage(image=Image.fromarray(img))

    #Only caching image to prevent the garabge collector from culling it from memory immediately
    manager.setPreservedImage(imgtk)

    #display preview
    image_canvas.create_image(0,0, anchor=NW, image=imgtk)


def calculatePreview(image_canvas, lower_slider, upper_slider, manager):
    manager.setLowerThreshold(int(lower_slider.get()))
    manager.setUpperThreshold(int(upper_slider.get()))
    
    updateImage(image_canvas, manager)


def preprocessorPopulate(f, manager):
    global lower_limit_setter 
    lower_limit_setter = manager.setLowerThreshold
    global upper_limit_setter 
    upper_limit_setter = manager.setUpperThreshold
    global manager_ref 
    manager_ref = manager
    global canvas_ref

    file_name = tk.StringVar()
    file_name.set(manager.getFileName())
    file_name_label = tk.Label(f, textvariable=file_name)
    file_name_label.grid(row=0, column=0, padx=10, pady=10)

    canvas = Canvas(f, width=600, height=500)
    canvas_ref = canvas
    canvas.grid(row=1, column=0, padx=10, pady=10)

    #load
    img = cv2.imread(manager.getThumbnail())
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = cv2.bitwise_not(img)

    manager.setImgCache(img)

    if manager.arePathsValid:
        updateImage(canvas, manager)

    lower_bound_label = tk.Label(f, text='Lower Threshold Limit')
    lower_bound_label.grid(row=2, column=0, padx=10, pady=10)
    lower_bound_slider = tk.Scale(f, from_=0, to=255, orient=HORIZONTAL, resolution=1, length=400, command=update_lower)
    lower_bound_slider.grid(row=3, column=0, padx=10, pady=10)

    upper_bound_label = tk.Label(f, text='Upper Threshold Limit')
    upper_bound_label.grid(row=4, column=0, padx=10, pady=10)
    upper_bound_slider = tk.Scale(f, from_=0, to=255, orient=HORIZONTAL, resolution=1, length=400, command=update_upper)
    upper_bound_slider.grid(row=5, column=0, padx=10, pady=10)

    go_to_labelling__button = tk.Button(f, text='Continue to Labelling', command=partial(finalPreprocess, manager))
    go_to_labelling__button.grid(row=6, column=0, padx=10, pady=10)

