"""
根据像素点建立图片中的数字模板
"""
from numpy import *
import numpy as np
from pylab import *
import PIL.Image
import cv2

def M_size():

    """
    :return: 返回图片的详细信息
    """
    im = PIL.Image.open(READ_PATH_M)
    ima = im.convert("L")  # 转化为灰度图
    x = np.array(ima)
    hang = x.shape[0]  # 图片行数
    lie = x.shape[1]  # 图片列数
    tol = hang * lie  # 图片像素数目
    return x, hang, lie, tol

if __name__ == '__main__':
    READ_PATH_M = "./1.jpg"
    x, hang, lie, tol = M_size()

