# -*- coding: utf-8 -*-
# @Time    : 2022/9/27 15:45

import numpy as np
import cv2


def image_rotate(img, cls):
    """
    根据box和image坐标信息，判断并旋转图片至正立
    box_xmin, box_ymin, box_xmax, box_ymax = box_point_list[2], box_point_list[3],box_point_list[4],box_point_list[
    5]
    image_xmin, image_ymin, image_xmax, image_ymax = image_point_list[2], image_point_list[3], image_point_list[
    4], image_point_list[5]
    """

    # 测试数据
    box_xmin, box_ymin, box_xmax, box_ymax = 100, 100, 500, 500
    image_xmin, image_ymin, image_xmax, image_ymax = 350, 150, 450, 400
    # 坐标原点
    x_mid = (box_xmax - box_xmin) / 2 + box_xmin
    y_mid = (box_ymax - box_ymin) / 2 + box_ymin

    # location是人像/国徽相对于图片中点的坐标系处于第几象限
    location = 1
    if image_xmin > x_mid and image_ymin < y_mid:
        location = 1
    elif image_xmin < x_mid and image_ymin < y_mid:
        location = 2
    elif image_xmin < x_mid and image_ymin > y_mid:
        location = 3
    elif image_xmin > x_mid and image_ymin > y_mid:
        location = 4

    if cls == "FACE":
        # 人像面
        if location:
            # 如果n>=4, 就取余数来确定旋转的度数
            # 正数代表逆时针旋转，负数代表顺时针旋转
            data = np.rot90(img, -(location - 1))
            return data
    else:
        # 国徽面
        if location:
            data = np.rot90(img, -(location - 2))
            return data


if __name__ == '__main__':
    # box_point = [(100, 100), (500, 500)]
    # img_point = [(350, 150), (450, 400)]
    # img_point(box_point[0][0])
    # 测试判断
    img_path = r"C:\Users\9000\Desktop\emblem.jpg"
    cls = "EMBLEM"
    im = cv2.imread(img_path)
    print(im.shape)
    data = image_rotate(im, cls)
    print(data.shape)

    cv2.imshow('data', data)
    cv2.waitKey()

    # 如果n>=4, 就取余数来确定旋转的度数
    # 正数代表逆时针旋转，负数代表顺时针旋转
# np.array(list(im.shape[1:])).reshape(-1),