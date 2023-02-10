# # -*- coding: utf-8 -*-
# # @Time    : 2022/10/17 9:56
import base64
from io import BytesIO

from PIL import Image
import os
import numpy as np

from paddle_serving_app.reader import *
import cv2

file_name = r"C:\Users\9000\Desktop\被告身份证-正面-陶敏-340823198811162920.jpg"

# def PIL_to_bytes(im):
#     """
#     PIL转二进制
#     :param im: PIL图像，PIL.Image
#     :return: bytes图像
#     """
#     bytesIO = BytesIO()
#     try:
#         im.save(bytesIO, format='JPEG')
#     except:
#         im.save(bytesIO, format='PNG')
#     return bytesIO.getvalue()  # 转二进制
#
# img = Image.open(file_name)
#
# cropped = img.crop((int(63.38628387451172), int(107.40235137939453), int(207.3997802734375), int(141.41079711914062))) # (left, upper, right, lower)
#
# part_img = base64.b64encode(PIL_to_bytes(cropped)).decode('utf8')
# # print(part_img)
#
# # cropped.show()
# # print(PIL_to_bytes(cropped))
# # cropped.save(r"D:\工作相关\需求\Image\crop\name.jpg")
# with open(r"D:\工作相关\需求\Image\crop\name.jpg", 'wb') as f:
#     f.write(PIL_to_bytes(cropped))

im = cv2.imread(r"C:\Users\9000\Desktop\emblem.jpg")

preprocess = Sequential([
    # 按照顺序对图片进行预处理
    # resize中输入参数为第一项图片横坐标，第二项图片纵坐标
    # BGR2RGB(),
    Resize(
        (200, 150), interpolation=cv2.INTER_LINEAR),
    Div(255.0),
    Transpose((2, 0, 1))
])
re_tran = Sequential([
    Div(1/255),
    Transpose((1, 2, 0))
])

# print(im)
print(im.shape)
im = preprocess(im)
print(im.shape)

im = re_tran(im)
print(111111111111)
print(im.shape)
cv2.imwrite("img.jpg", im)
# def bytes2cv2(img_bytes: str or bytes):
#     """
#     字节流图片转换为cv2格式
#     :param img_bytes: 字节流图片
#     :return: cv2格式的图片img_data
#     """
#     img_buffer_numpy = np.frombuffer(img_bytes, dtype=np.uint8)  # 将图片字节码bytes  转换成一维的numpy数组到缓存中
#     img_data = cv2.imdecode(img_buffer_numpy, 1)  # 从指定的内存缓存中读取一维numpy数据，并把数据转换(解码)成图像矩阵格式
#
#     return img_data
#
# with open(r"C:\Users\9000\Desktop\被告身份证-正面-陶敏-340823198811162920.jpg", 'rb') as f:
#     file = f.read()
#     print(type(file))
#     im = bytes2cv2(file)
#     cv2.imwrite("im1.jpg", im)


print('OK')
