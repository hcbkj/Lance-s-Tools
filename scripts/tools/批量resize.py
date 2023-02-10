# -*- coding: utf-8 -*-
# @Time    : 2022/10/21 11:16
import cv2
import os
import numpy as np
from paddle_serving_app.reader import *
from PIL import Image
from typing import Tuple


# def image_point(num: int) -> int:
#     """
#     处理图片分辨率，要求resize时是32的倍数
#     :param num: 分辨率
#     :return:处理后的分辨率
#     """
#     if not num % 32 == 0:
#         if num % 32 >= 16:
#             point = (int(num / 32) + 1) * 32
#         else:
#             point = int(num / 32) * 32
#     else:
#         point = num
#     return point

def image_point(x: int, y: int) -> Tuple[int]:
    """
    处理图片分辨率，要求resize时是32的倍数
    :param x, y: 分辨率的横坐标
    :return: 处理后的分辨率
    """

    if not (z := x % 32) == 0:
        x = (x // 32 + 1) * 32 if z >= 16 else x // 32 * 32

    if not (z := y % 32) == 0:
        y = (y // 32 + 1) * 32 if z >= 16 else y // 32 * 32
    tuples = (x, y)

    if max(x, y) > 640:
        proportion = y / x
        tuples = (640, int(640 * proportion)) if proportion > 0 else (640 // proportion, 640)
    return tuples


def bytes2cv2(img_bytes: str or bytes) -> str:
    """
    字节流图片转换为cv2格式
    :param img_bytes: 字节流图片
    :return: cv2格式的图片img_data
    """
    img_buffer_numpy = np.frombuffer(img_bytes, dtype=np.uint8)  # 将图片字节码bytes  转换成一维的numpy数组到缓存中
    img_data = cv2.imdecode(img_buffer_numpy, 1)  # 从指定的内存缓存中读取一维numpy数据，并把数据转换(解码)成图像矩阵格式

    return img_data


if __name__ == '__main__':
    path = r"D:\工作相关\需求\Image\国徽面"
    path_list = os.listdir(path)
    for file in path_list:
        print(file)
        img_path = os.path.join(path, file)

        img = open(img_path, 'rb').read()
        img = bytes2cv2(img)

        # 这个是图片分辨率，要求resize时是32的倍数，通过im.shape取出的元组中第一项是图片纵坐标，第二项是图片横坐标
        y, x = img.shape[0], img.shape[1]
        print(f"{x},{y}")

        x, y = image_point(x, y)
        # print('===========')
        # print(f"{x},{y}")
        preprocess = Resize((int(x), int(y)))
        img = preprocess(img)
        # img = cv2.imdecode(img, cv2.IMREAD_COLOR)

        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        bg_img1 = Image.fromarray(np.uint8(img))
        bg_img1.save(r'D:\工作相关\需求\Image\国徽面处理结果\{}'.format(file))
        # cv2.imwrite(r'D:\工作相关\需求\Image\国徽面处理结果\{}'.format(file), img)

        # break
