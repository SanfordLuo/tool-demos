"""
判断图片是否为全黑或者全白
"""
import numpy as np
import cv2

image_path = r"D:\fff\01571.jpg"

def judge_color(image_path):
    # 获得图片的像素点总数
    img = cv2.imread(image_path)
    pixels = img.shape[0] * img.shape[1]

    if (np.sum(cv2.imread(image_path, 0)) / pixels) == 0:
        return "Is Black"
    elif (np.sum(cv2.imread(image_path, 0)) / pixels) > 239:
        return "Is White"
    else:
        return "Other Color"

if __name__ == '__main__':
    color = judge_color(image_path)
    print(color)
