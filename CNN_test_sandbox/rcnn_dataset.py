import os
import pandas as pd
from os import listdir
from os.path import join, isfile
from torchvision.io import read_image
from torch.utils.data import Dataset
from PIL import Image


class RCNNDataset(Dataset):
    def __init__(self, annotations, img_dir, device='cpu', transform=None, target_transform=None):
        self.img_data = pd.read_csv(annotations)
        self.img_dir = img_dir
        self.transform = transform
        self.target_transform = target_transform
        self.device = device

        temp = [f for f in listdir(img_dir) if isfile(join(img_dir, f)) and f!='annotations.csv']
        self.file_list = temp
        
        box_list = []
        label_list = []
        images = []
        #load annotations and images
        for f in temp:
            boxes = []
            labels = []
            temp_df = self.img_data.loc[self.img_data['file_name'] == f]
            for index, row in temp_df.iterrows():
                box = [
                    float(row['x1']),
                    float(row['y1']),
                    float(row['x2']),
                    float(row['y2']),
                ]
                label = int(row['label'])
                boxes.append(box)
                labels.append(label)

            box_list.append(boxes)
            label_list.append(labels)

            temp_path = join(img_dir, f)
            #img = read_image(temp_path)
            #img = img.float()
            img = Image.open(temp_path)
            

            images.append(img)

        self.box_list = box_list
        self.label_list = label_list
        self.images = images
        print('Dataset Loaded')


    def __len__(self):
        return len(self.file_list)


    def __getitem__(self, idx):
        #get image
        img = self.images[idx]

        #target
        temp_target = {
                'boxes': self.box_list[idx], 
                'labels': self.label_list[idx]
            }

        #image transform
        if self.transform:
            img = self.transform(img)

        #target transform
        if self.target_transform:
            temp_target = self.target_transform(temp_target)

        #return 
        return (img, temp_target)

        


if __name__ == '__main__':
    ds = RCNNDataset(
        annotations='D:\\GitHub\\Hindi-Handwriting-Recognition\\CNN_test_sandbox\\Dataset\\Local (Training)\\annotations.csv',
        img_dir='D:\\GitHub\\Hindi-Handwriting-Recognition\\CNN_test_sandbox\\Dataset\\Local (Training)'
    )