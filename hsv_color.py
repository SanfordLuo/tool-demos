import cv2
import numpy as np

def Distinguish_Colour():
    """
    :param nnn:
    :return:  返回最大的下标索引，和列表，例如：0, [89, 17, 0]
    """

    read_path = r"D:\lwx596588\V2.3\CUT_V\715.jpg"
    img = cv2.imread(read_path, cv2.IMREAD_COLOR)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # 绿
    lower_green = np.array([40, 43, 46])
    upper_green = np.array([77, 255, 255])

    mask = cv2.inRange(hsv, lower_green, upper_green)
    res = cv2.bitwise_and(img, img, mask=mask)
    img_green = cv2.cvtColor(res, cv2.THRESH_BINARY)
    cv2.imwrite("hsv_green.jpg", img_green)
    green_sum = 0
    image_shape = img_green.shape
    result_green = img_green[:, :, :3].reshape(image_shape[0] * image_shape[1], 3)
    for num in result_green:
        if sum(num) != 0:
            green_sum += 1

    # 黄
    lower_yellow = np.array([20, 43, 46])
    upper_yellow = np.array([34, 255, 255])

    mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
    res = cv2.bitwise_and(img, img, mask=mask)
    img_yellow = cv2.cvtColor(res, cv2.THRESH_BINARY)
    cv2.imwrite("hsv_yellow.jpg", img_yellow)
    yellow_sum = 0
    result_yellow = img_yellow[:, :, :3].reshape(image_shape[0] * image_shape[1], 3)
    for num in result_yellow:
        if sum(num) != 0:
            yellow_sum += 1

    # 红
    lower_red = np.array([0, 43, 46])
    upper_red = np.array([10, 255, 255])
    # lower_red = np.array([156, 43, 46])
    # upper_red = np.array([180, 255, 255])

    mask = cv2.inRange(hsv, lower_red, upper_red)
    res = cv2.bitwise_and(img, img, mask=mask)
    img_red = cv2.cvtColor(res, cv2.THRESH_BINARY)
    cv2.imwrite("hsv_red.jpg", img_red)
    red_sum = 0
    result_red = img_red[:, :, :3].reshape(image_shape[0] * image_shape[1], 3)
    for num in result_red:
        if sum(num) != 0:
            red_sum += 1

    lv_huang_hong = [green_sum, yellow_sum, red_sum]
    if sum(lv_huang_hong) == 0:
        return "hei", lv_huang_hong
    else:
        return lv_huang_hong.index(max(lv_huang_hong)), lv_huang_hong


if __name__ == '__main__':
    print(Distinguish_Colour())
