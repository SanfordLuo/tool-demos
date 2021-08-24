import glob
import os
import cv2
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import ProcessPoolExecutor
from PIL import Image


# for imagePath in glob.glob("../img01/*.jpg"):
#     cropImg = Image.open(imagePath).convert('L')
#     cropImg.save(imagePath)



def func(imagePath):
    cropImg = Image.open(imagePath).convert('L')
    cropImg.save(imagePath)

if __name__ == '__main__':
    imagePath = glob.glob("../img02/*.jpg")
    ProcessPoolExecutor().map(func, imagePath)
