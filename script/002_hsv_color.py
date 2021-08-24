"""
hsv区分颜色应用
h: 色调, s: 饱和度, v: 明度
"""
import os
import cv2
import numpy

PROJECT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG_NAME_COLOR = "img_001.jpg"
IMG_NAME_RAINBOW = "img_001.jpg"


class HsvBaseSpace:
    """
    hsv色彩空间表
    黑 灰 白 红 橙 黄 绿 青 蓝 紫
    """
    lower_black = numpy.array([0, 0, 0])
    upper_black = numpy.array([180, 255, 46])

    lower_gray = numpy.array([0, 0, 46])
    upper_gray = numpy.array([180, 43, 220])

    lower_white = numpy.array([0, 0, 221])
    upper_white = numpy.array([180, 30, 255])

    lower_red_0 = numpy.array([0, 43, 46])
    upper_red_0 = numpy.array([10, 255, 255])

    lower_red_1 = numpy.array([156, 43, 46])
    upper_red_1 = numpy.array([180, 255, 255])

    lower_orange = numpy.array([11, 43, 46])
    upper_orange = numpy.array([25, 255, 255])

    lower_yellow = numpy.array([26, 43, 46])
    upper_yellow = numpy.array([34, 255, 255])

    lower_green = numpy.array([35, 43, 46])
    upper_green = numpy.array([77, 255, 255])

    lower_cyan = numpy.array([78, 43, 46])
    upper_cyan = numpy.array([99, 255, 255])

    lower_blue = numpy.array([100, 43, 46])
    upper_blue = numpy.array([124, 255, 255])

    lower_purple = numpy.array([125, 43, 46])
    upper_purple = numpy.array([155, 255, 255])


def turn_img(img_name, lower, upper, color_name, imwrite=False):
    """
    图片转换
    """
    img_path = "{0}/img/{1}".format(PROJECT_PATH, img_name)
    img = cv2.imread(img_path, cv2.IMREAD_COLOR)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # 将位于两个区域间的值置为白(255)，位于区间外的值置为黑(0)
    mask = cv2.inRange(hsv, lower, upper)

    # 对像素值进行二进制与操作, 白色区域原像素保留，黑色区域像素剔除
    _img = cv2.bitwise_and(img, img, mask=mask)

    # 除选定颜色外其他都值黑
    ret_img = cv2.cvtColor(_img, cv2.THRESH_BINARY)

    if imwrite:
        cv2.imwrite("{0}/img/rainbow/{1}.jpg".format(PROJECT_PATH, color_name), ret_img)
    # cv2.imshow('hsv', ret_img)
    # cv2.waitKey()
    # cv2.destroyAllWindows()

    return ret_img


def total_not_zero(turn_img):
    """
    返回不全为0的个数
    """
    total = 0
    ret_img = turn_img[:, :, :3].reshape(turn_img.shape[0] * turn_img.shape[1], 3)
    for _ in ret_img:
        if sum(_) != 0:
            total += 1
    return total


def distinguish_color():
    """
    识别图片颜色
    """
    black = turn_img(IMG_NAME_COLOR, HsvBaseSpace.lower_black, HsvBaseSpace.upper_black, "black")
    black_total = total_not_zero(black)

    gray = turn_img(IMG_NAME_COLOR, HsvBaseSpace.lower_gray, HsvBaseSpace.upper_gray, "gray")
    gray_total = total_not_zero(gray)

    white = turn_img(IMG_NAME_COLOR, HsvBaseSpace.lower_white, HsvBaseSpace.upper_white, "white")
    white_total = total_not_zero(white)

    red_0 = turn_img(IMG_NAME_COLOR, HsvBaseSpace.lower_red_0, HsvBaseSpace.upper_red_0, "red_0")
    red_0_total = total_not_zero(red_0)

    red_1 = turn_img(IMG_NAME_COLOR, HsvBaseSpace.lower_red_1, HsvBaseSpace.upper_red_1, "red_1")
    red_1_total = total_not_zero(red_1)

    orange = turn_img(IMG_NAME_COLOR, HsvBaseSpace.lower_orange, HsvBaseSpace.upper_orange, "orange")
    orange_total = total_not_zero(orange)

    yellow = turn_img(IMG_NAME_COLOR, HsvBaseSpace.lower_yellow, HsvBaseSpace.upper_yellow, "yellow")
    yellow_total = total_not_zero(yellow)

    green = turn_img(IMG_NAME_COLOR, HsvBaseSpace.lower_green, HsvBaseSpace.upper_green, "green")
    green_total = total_not_zero(green)

    cyan = turn_img(IMG_NAME_COLOR, HsvBaseSpace.lower_cyan, HsvBaseSpace.upper_cyan, "cyan")
    cyan_total = total_not_zero(cyan)

    blue = turn_img(IMG_NAME_COLOR, HsvBaseSpace.lower_blue, HsvBaseSpace.upper_blue, "blue")
    blue_total = total_not_zero(blue)

    purple = turn_img(IMG_NAME_COLOR, HsvBaseSpace.lower_purple, HsvBaseSpace.upper_purple, "purple")
    purple_total = total_not_zero(purple)

    total_list = [black_total, gray_total, white_total, red_0_total, red_1_total, orange_total,
                  yellow_total, green_total, cyan_total, blue_total, purple_total]
    return total_list.index(max(total_list)), total_list


def split_rainbow():
    """
    拆分图片
    """
    black = turn_img(IMG_NAME_RAINBOW, HsvBaseSpace.lower_black, HsvBaseSpace.upper_black, "black", imwrite=True)

    gray = turn_img(IMG_NAME_RAINBOW, HsvBaseSpace.lower_gray, HsvBaseSpace.upper_gray, "gray", imwrite=True)

    white = turn_img(IMG_NAME_RAINBOW, HsvBaseSpace.lower_white, HsvBaseSpace.upper_white, "white", imwrite=True)

    red_0 = turn_img(IMG_NAME_RAINBOW, HsvBaseSpace.lower_red_0, HsvBaseSpace.upper_red_0, "red_0", imwrite=True)

    red_1 = turn_img(IMG_NAME_RAINBOW, HsvBaseSpace.lower_red_1, HsvBaseSpace.upper_red_1, "red_1", imwrite=True)

    orange = turn_img(IMG_NAME_RAINBOW, HsvBaseSpace.lower_orange, HsvBaseSpace.upper_orange, "orange", imwrite=True)

    yellow = turn_img(IMG_NAME_RAINBOW, HsvBaseSpace.lower_yellow, HsvBaseSpace.upper_yellow, "yellow", imwrite=True)

    green = turn_img(IMG_NAME_RAINBOW, HsvBaseSpace.lower_green, HsvBaseSpace.upper_green, "green", imwrite=True)

    cyan = turn_img(IMG_NAME_RAINBOW, HsvBaseSpace.lower_cyan, HsvBaseSpace.upper_cyan, "cyan", imwrite=True)

    blue = turn_img(IMG_NAME_RAINBOW, HsvBaseSpace.lower_blue, HsvBaseSpace.upper_blue, "blue", imwrite=True)

    purple = turn_img(IMG_NAME_RAINBOW, HsvBaseSpace.lower_purple, HsvBaseSpace.upper_purple, "purple", imwrite=True)


if __name__ == '__main__':
    print(distinguish_color())
    # split_rainbow()
