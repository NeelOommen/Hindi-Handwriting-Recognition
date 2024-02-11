import tkinter as tk
import shutil

from functools import partial
from tkinter import filedialog
from tkinter import Canvas
from tkinter import *
from PIL import ImageTk, Image

max_img_width = 1000
max_thumbnail_width = 400

def browse_files(file_name_var, image_canvas, manager):

    global img

    filepath = filedialog.askopenfilename(initialdir='/',
                                          title='Select Image to Process',
                                          filetypes=(
                                              ("JPG Images", "*.jpg"),
                                          ))
    
    file_name_var.set(filepath)
    
    if type(filepath) == str and len(filepath) > 0:
        #create a temporary copy for manipulative processing
        temp = filepath.split('/')
        filename = temp[-1]
        copyPath = '..\Hindi-Handwriting-Recognition\processing_cache\\' + filename
        thumbnailPath = '..\Hindi-Handwriting-Recognition\processing_cache\\thumbnail.jpg'
        shutil.copy(filepath, copyPath)
        shutil.copy(filepath, thumbnailPath)

        #resize the copied image for processing and thumbnail
        temp_img = Image.open(copyPath)
        thumb_img = Image.open(thumbnailPath)

        width, height = temp_img.size
        tWidth, tHeight = thumb_img.size

        wpercent = (max_img_width/float(width))
        tWpercent = (max_thumbnail_width/float(tWidth))
        
        new_height = int(float(wpercent) * float(height))
        t_new_height = int(float(tWpercent) * float(tHeight))
        
        temp_img = temp_img.resize((max_img_width, new_height), Image.Resampling.LANCZOS)
        thumb_img = thumb_img.resize((max_thumbnail_width, t_new_height), Image.Resampling.LANCZOS)
        
        temp_img.save(copyPath)
        thumb_img.save(thumbnailPath)

        img = ImageTk.PhotoImage(Image.open(thumbnailPath))
        image_canvas.create_image(0,0, anchor=NW, image=img)

        manager.setPaths(copyPath, thumbnailPath)
    else:
        file_name_var.set('No File Selected')
        manager.setPaths(None, None)



def fileSelectorPopulate(f, manager):

    file_descriptor_label = tk.Label(f, text='Select File to Process')
    file_descriptor_label.grid(row=0, column=0, padx=10, pady=5)

    file_name = tk.StringVar()
    file_name.set("No file currently selected")
    file_name_label = tk.Label(f, textvariable=file_name)
    file_name_label.grid(row=1, column=0, padx=10, pady=10)

    canvas = Canvas(f, width=600, height=700)
    canvas.grid(row=3, column=0, padx=10, pady=10)

    file_browse_button = tk.Button(f, text="Browse for image", command=partial(browse_files, file_name, canvas, manager))
    file_browse_button.grid(row=2, column=0, padx=10, pady=10)

    go_to_processing_button = tk.Button(f, text="Continue to Processing", command=manager.returnProcessingSwitchFunction())
    go_to_processing_button.grid(row=4, column=0, padx=10, pady=10)