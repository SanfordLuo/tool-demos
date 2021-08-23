import numpy
import PIL.Image

im = PIL.Image.open('../CUT1/001.jpg')
x = numpy.array(im)
print(x)

# 图片大小
hang = x.shape[0]  # 图片行数
lie = x.shape[1]  # 图片列数
tol = hang * lie  # 图片像素数目


# 将二维数组变为一维数组
def Two_One(a, hang, lie):
    k = 0
    temp = []
    for i in range(hang):
        for j in range(lie):
            temp.append(a[i][j])
            k += 1
    return temp


# 序列的一维数组
def Sign(tol):
    temp = []
    for i in range(tol):
        temp.append(i)
    return temp


# 将图片一维数组进行排序，并标记一维数组位置
def Sort(aa, bb, tol):
    for k in range(tol):
        for i in range(k, tol):
            if aa[k] < aa[i]:
                temp1 = aa[i]
                aa[i] = aa[k]
                aa[k] = temp1

                temp2 = bb[i]
                bb[i] = bb[k]
                bb[k] = temp2
    return aa, bb


B_sign = numpy.zeros(tol, numpy.int16)
h = numpy.zeros(tol, numpy.int16)
l = numpy.zeros(tol, numpy.int16)
g = numpy.zeros([hang, lie], numpy.int16)
y = numpy.zeros([hang, lie], numpy.int16)
r = numpy.zeros([hang, lie], numpy.int16)

for i in range(hang):  # 转化为二值矩阵
    for j in range(lie):
        g[i][j] = x[i][j][1]  # 绿色
        y[i][j] = (int(x[i][j][0]) + int(x[i][j][1])) / 2  # 黄色
        r[i][j] = x[i][j][0]  # 红色

Ima_one_g = Two_One(g, hang, lie)  # 将图片二维数组转化为一维数组
B_sign_n_g = Sign(tol)  # 构建标号一维数组
Ima_one_G, _ = Sort(Ima_one_g, B_sign_n_g, tol)  # 将图片和标号一维数组进行排序、对应

Ima_one_y = Two_One(y, hang, lie)  # 将图片二维数组转化为一维数组
B_sign_n_y = Sign(tol)  # 构建标号一维数组
Ima_one_Y, _ = Sort(Ima_one_y, B_sign_n_y, tol)  # 将图片和标号一维数组进行排序、对应

Ima_one_r = Two_One(r, hang, lie)  # 将图片二维数组转化为一维数组
B_sign_n_r = Sign(tol)  # 构建标号一维数组
Ima_one_R, _ = Sort(Ima_one_r, B_sign_n_r, tol)  # 将图片和标号一维数组进行排序、对应

LV = Ima_one_G[0]
HUANG = Ima_one_Y[0]
HONG = Ima_one_R[0]

print(LV)
print(HUANG)
print(HONG)
