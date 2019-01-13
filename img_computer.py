"""
判断待测图片是否和模版图片相似
"""
import cv2
import numpy


def img_compare(image, target, value):
    """
    :param image: 待测图片
    :param target: 模板图片
    :param value: 相似度
    :return:
    """
    img_rgb = cv2.imread(image)
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    template = cv2.imread(target, 0)
    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    threshold = float(value)
    loc = numpy.where(res >= threshold)
    if len(loc[0]) > 0:
        return True
    else:
        return False
