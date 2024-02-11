import tkinter as tk

from tkinter import messagebox
from file_selector import fileSelectorPopulate
from preprocessor import preprocessorPopulate
from labelling import mappingPopulate
from data_manager import data_manager

img=None  

manager = data_manager()

window = tk.Tk()

#frames
file_selector_frame = tk.Frame(window)
preprocessor_frame = tk.Frame(window)
char_mapping_frame = tk.Frame(window)

def goToProcessing():
    global file_selector_frame
    global preprocessor_frame

    if manager.arePathsValid:
        preprocessorPopulate(preprocessor_frame, manager)
        preprocessor_frame.pack(fill='both', expand=1)
        file_selector_frame.forget()
    else:
        messagebox.showerror('Invalid Paths', 'Invalid file or no file chosen')


def goToLabelling():
    global preprocessor_frame
    global char_mapping_frame

    mappingPopulate(char_mapping_frame, manager)
    char_mapping_frame.pack(fill='both', expand=1)
    preprocessor_frame.forget()


manager.setProcessingSwitchFunction(goToProcessing)
manager.setLabellingSwitchFunction(goToLabelling)
manager.setBlurFactor(7)
manager.setOutputPath('..\\Hindi-Handwriting-Recognition\\processing_cache\\temp_output\\')

window.title('Handwriting Sample Processor')
window.geometry('700x900')

#construct the UI for each frame
fileSelectorPopulate(file_selector_frame, manager)


file_selector_frame.pack(fill='both', expand=1)
#char_mapping_frame.pack(fill='both', expand=1)

window.mainloop()