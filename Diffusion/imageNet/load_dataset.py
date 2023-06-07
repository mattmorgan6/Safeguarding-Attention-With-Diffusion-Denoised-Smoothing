'''
PyTorch Dataset Handling. The dataset folder should comprise of two subfolders namely "train" and "test" where both folders has subfolders that named
according to their class names.
'''

import cv2
import glob
import numpy as np
import os
import torch
from PIL import Image
from torch.utils import data
from torch.utils.data import Dataset, dataset
from torch.utils.data.sampler import SubsetRandomSampler


def get_subset_random_sampler(dataset, dataset_size):
    random_seed = 42    # We always get the same subset and randomization unless you change this seed.
    np.random.seed(random_seed)
    torch.manual_seed(random_seed)

    print("Total dataset size:", len(dataset))

    indices = list(range(len(dataset)))    
    np.random.shuffle(indices)
    subset_len = int(len(dataset) * dataset_size)
    # print(indices[:subset_len])

    print("Total Subset size:", subset_len)

    # Use this to randomize the random subset (needed for accurate training)
    sampler = SubsetRandomSampler(indices[:subset_len])

    return sampler


class LoadDataset(Dataset):
    '''Loads the dataset from the given path.
    '''

    def __init__(self, dataset_folder_path, image_size=224, image_depth=3, train=True, transform=None, validate=False):
        '''Parameter Init.
        '''

        assert not dataset_folder_path is None, "Path to the dataset folder must be provided!"

        self.dataset_folder_path = dataset_folder_path
        self.transform = transform
        self.image_size = image_size
        self.image_depth = image_depth
        self.train = train
        self.validate = validate
        self.classes = sorted(self.get_classnames())
        self.image_path_label = self.read_folder()

    def get_classnames(self):
        '''Returns the name of the classes in the dataset.
        '''
        if self.validate:
            return os.listdir(f"{self.dataset_folder_path.rstrip('/')}/" )
        else:
            return os.listdir(f"{self.dataset_folder_path.rstrip('/')}/train/" )


    def read_folder(self):
        '''Reads the folder for the images with their corresponding label (foldername).
        '''

        image_path_label = []

        if self.validate:
            folder_path = f"{self.dataset_folder_path.rstrip('/')}/"
        elif self.train:
            folder_path = f"{self.dataset_folder_path.rstrip('/')}/train/"
        else:
            folder_path = f"{self.dataset_folder_path.rstrip('/')}/test/"

        for x in glob.glob(folder_path + "**", recursive=True):

            if not x.endswith('jpg') and not x.endswith('JPEG') and not x.endswith('png'):
                continue

            class_idx = self.classes.index(x.split('/')[-2])
            image_path_label.append((x, int(class_idx)))

        return image_path_label


    def __len__(self):
        '''Returns the total size of the data.
        '''
        return len(self.image_path_label)


    def __getitem__(self, idx):
        '''Returns a single image array.
        '''

        if torch.is_tensor(idx):
            idx = idx.tolist()

        if idx >= len(self.image_path_label):
            print("Idx", idx, "Len", len(self.image_path_label))

        image, label = self.image_path_label[idx]
        
        image = Image.open(image)
        image = image.convert('RGB')
        image = self.transform(image)

        return {
            'image': image,
            'label': label
        }