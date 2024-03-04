import os
import pandas as pd
import torch
from torchvision.io import read_image
from torch.utils.data import Dataset

class CustomImageDataset(Dataset):
    def __init__(self, annotations_file_path, img_dir, transform = None, target_transform = None):
        self.img_labels = pd.read_csv(annotations_file_path)
        self.img_dir = img_dir
        self.transform = transform
        self.target_transform = target_transform


    def __len__(self):
        return len(self.img_labels)
    

    def __getitem__(self, idx):
        #load image
        img_path = os.path.join(self.img_dir, self.img_labels.iloc[idx, 0])
        image = read_image(img_path)
        image = image.float()

        #get label
        label = int(self.img_labels.iloc[idx, 1])

        #create tensor
        if self.transform:
            image = self.transform(image)

        #label transform
        if self.target_transform:
            label = self.target_transform(label)
        else:
            label = torch.tensor(float(label))

        #return tensor
        return (image, label)