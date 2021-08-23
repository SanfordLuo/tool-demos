"""
根据像素点获取图片中的数字模板
"""
from numpy import *
import numpy as np
from pylab import *
import PIL.Image
import cv2
import matplotlib.pyplot as pyplot

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

def Two_One(a, hang, lie):
    """
    :return: 将二维数组转换为一维数组 
    """
    k = 0
    temp = []
    for i in range(hang):
        for j in range(lie):
            temp.append(a[i][j])
            k += 1
    return temp

def Sign(tol):
    """
    :return: 序列的一维数组
    """
    temp = []
    for i in range(tol):
        temp.append(i)
    return temp

def Sort(aa, bb, tol):
    """
    :return: 将图片一维数组进行排序，并标记位置
    """
    for i in range(tol):
        for j in range(i, tol):
            if aa[i] < aa[j]:
                aa[i], aa[j] = aa[j], aa[i]
                bb[i], bb[j] = bb[j], bb[i]
    return aa, bb

def Mark_Two(num, B_sign_S):
    """
    :return: 标记图片二维数组像素位置
    """
    h = zeros(tol, int16)
    l = zeros(tol, int16)
    for i in range(num):
        h[i] = B_sign_S[i] // lie
        l[i] = B_sign_S[i] % lie
    return h, l

def Assignment(num, x, h, l):
    """
    :return: 图像二值化
    """
    for i in range(num):
        x[h[i]][l[i]] = 1
    for j in range(num, tol):
        x[h[j]][l[j]] = 255
    return x

def Creat_Model(num, n, nn):
    for k in range(n):
        Num_path = "{}/{:0>1d}/{:0>1d}.jpg".format(PATH_M, num, k+1)
        im = PIL.Image.open(Num_path)
        ima = im.convert('L')  # 转化灰度图

        # 取灰度值
        b = np.array(ima)  # 转化为二维数组
        Ima_one = Two_One(b, hang, lie)  # 二维数组转化为一维数组
        B_sign_n = Sign(tol)  # 构建标号一维数组
        _, B_sign_S = Sort(Ima_one, B_sign_n, tol)  # 将图片和标号一维数组进行排序，对应
        h, l = Mark_Two(tol, B_sign_S)  # 返回二维数组坐标，按顺序排列
        a = Assignment(nn, x, h, l)

        M_path = "{}/{:0>1d}/{:0>3d}.jpg".format(PATH_M, num, k+1)
        cv2.imwrite(M_path, a)
        k += 1

def  Confirm_Model(num, n):
    """
    :return: 
    """
    nn = 0
    for k in range(n):
        model_path1 = "{}/{:0>1d}/{:0>3d}.jpg".format(PATH_M, num, 1)
        im1 = PIL.Image.open(model_path1)
        x0 = np.array(im1)
        x1 = np.array(im1)

        model_path2 = "{}/{:0>1d}/{:0>3d}.jpg".format(PATH_M, num, k+1)
        im2 = PIL.Image.open(model_path2)
        x2 = np.array(im2)

        for i in range(x1.shape[0]):
            for j in range(x1.shape[1]):
                if x1[i][j] <= 10 and x2[i][j] <= 6:
                    x0[i][j] = 0
                    x1[i][j] = 1
                else:
                    x0[i][j] = 255
                    x1[i][j] = 0
        k += 1
    for i in range(x1.shape[0]):
        for j in range(x1.shape[1]):
            if x1[i][j] == 1:
                nn += 1
    model_view = "{}/{:0>1d}/{}.jpg".format(PATH_M, num, 'Model')
    cv2.imwrite(model_view, x0)

    # print(x0)
    imshow(x0)
    pyplot.show()
    return x1, nn

def main(num, n, nn):
    Creat_Model(num, n, nn)
    MODEL, nn = Confirm_Model(num, n)
    return MODEL, nn




if __name__ == '__main__':
    READ_PATH_M = "./Model/3/1.jpg"
    PATH_M = "./Model"
    x, hang, lie, tol = M_size()
    MODEL, nn = main(3, 1, 60)
    MODEL = MODEL.tolist()
    print(MODEL)

