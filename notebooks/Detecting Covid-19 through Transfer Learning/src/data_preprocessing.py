"""
filename: data_preprocessing.py
author: Supriya Sudarshan
version: 15.04.2021
description: Using N-Clahe as a part of preprocessing pipeline to enhance the
quality of original images (X-rays, CT and Ultrasound)  
"""

import cv2
import os
import numpy as np
from matplotlib import pyplot as plt

def apply_nclahe(dir_path, file_name):
    """
    Histogram equilization and Clahe
    """
    path = dir_path + '/' + file_name
    
    # read image
    img = cv2.imread(path, 0)

    # histogram equilization
    equ = cv2.equalizeHist(img)

    # Clahe
    processed_img = clahe.apply(equ)

    # save back
    cv2.imwrite(path, processed_img)


if __name__ == "__main__":
    
    # change the d_path to folder containing your image dataset
    d_path = '/content/drive/MyDrive/Colab Notebooks/Data'
    
    clahe = cv2.createCLAHE(clipLimit= 2.0, tileGridSize = (8,8))
    
    for root, dirs, files in os.walk(d_path):
    #print(root,dirs,files)
    for file in files:
        #print(root+'/'+file)
        apply_nclahe(root,file)

    print('Preprocessing completed...')

