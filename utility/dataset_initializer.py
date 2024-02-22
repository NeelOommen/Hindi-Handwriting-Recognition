import os 
from os import listdir
from os.path import isfile, join
import csv

def createCSV(dir_path):
    #get name of directories for labels
    dir_list = listdir(dir_path)

    #output a index to label translation
    label_list = []
    label_dict = {}
    for i in range(len(dir_list)):
        label_dict[dir_list[i]] = i
        temp_dict = {'label': dir_list[i], 'int_representation': i}
        label_list.append(temp_dict)

    label_file_name = 'label_list.csv'

    label_fields = ['label', 'int_representation']

    with open(dir_path + '\\' + label_file_name, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=label_fields)
        writer.writerows(label_list)


    #construct dict of image and labels
    data_list = []

    for p in dir_list:
        if p == 'label_list.csv':
            continue
        temp_path = dir_path + '\\' + p + '\\'
        filelist = [f for f in listdir(temp_path) if isfile(join(temp_path, f))]

        for f in filelist:
            temp_dict = {'filename': f, 'label': p}
            data_list.append(temp_dict)

    data_file_name = 'annotations.csv'

    data_fields = ['filename', 'label']

    with open(dir_path + '\\' + data_file_name, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=data_fields)
        writer.writerows(data_list)

    