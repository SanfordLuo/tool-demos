"""
图片降维处理,获取RYG值
"""
import numpy
from PIL import Image

IMG_NUMPY = numpy.array(Image.open('../img/img_000.jpg'))


def height_width_pixel():
    """
    返回图片的基础信息
    :return: 高, 宽, 像素
    """
    height = IMG_NUMPY.shape[0]
    width = IMG_NUMPY.shape[1]
    pixel = height * width
    return height, width, pixel


def two_to_one(two_array, height, width):
    """
    将二维数组转换为一维数组
    :return: 一维数组
    """
    one_array = []
    for i in range(height):
        for j in range(width):
            one_array.append(two_array[i][j])
    return one_array


def sort_one_array(one_array, pixel):
    """
    将图片一维数组进行排序，并标记一维数组位置
    :return: 排序后的一维数组, 一维数组对应的索引值
    """
    one_array_index = [_ for _ in range(pixel)]
    for i in range(pixel):
        for j in range(i, pixel):
            if one_array[i] < one_array[j]:
                one_array[i], one_array[j] = one_array[j], one_array[i]
                one_array_index[i], one_array_index[j] = one_array_index[j], one_array_index[i]
    return one_array, one_array_index


if __name__ == '__main__':
    height, width, pixel = height_width_pixel()

    # 初始化数组
    green = numpy.zeros([height, width], numpy.int16)
    yellow = numpy.zeros([height, width], numpy.int16)
    red = numpy.zeros([height, width], numpy.int16)

    for i in range(height):
        for j in range(width):
            green[i][j] = IMG_NUMPY[i][j][1]
            yellow[i][j] = (int(IMG_NUMPY[i][j][0]) + int(IMG_NUMPY[i][j][1])) / 2
            red[i][j] = IMG_NUMPY[i][j][0]

    one_green = two_to_one(green, height, width)
    ret_green = sort_one_array(one_green, pixel)
    G = ret_green[0][0]

    one_yellow = two_to_one(yellow, height, width)
    ret_yellow = sort_one_array(one_yellow, pixel)
    Y = ret_yellow[0][0]

    one_red = two_to_one(red, height, width)
    ret_red = sort_one_array(one_red, pixel)
    R = ret_red[0][0]

    print(G, Y, R)
