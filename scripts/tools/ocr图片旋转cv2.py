# -*- coding: utf-8 -*-
# @Time    : 2022/9/22 17:48
import numpy as np
import cv2
import math


# 根据box和image坐标信息，判断并旋转图片至正立
# def image_rotate(box_point_list: list, image_point_list: list) -> int:
def image_rotate() -> int:
    # box_xmin, box_ymin, box_xmax, box_ymax = box_point_list[2], box_point_list[3],box_point_list[4],box_point_list[5]
    # image_xmin, image_ymin, image_xmax, image_ymax = image_point_list[2], image_point_list[3], image_point_list[4], image_point_list[5]

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

    return location


# rotate_img
def rotate_image(src, angle, scale=1.):
    """
    旋转图片
    :param src: 图片路径
    :param angle: 旋转角度
    :param scale:
    :return:
    """
    img = cv2.imread(src)
    w = img.shape[1]
    h = img.shape[0]
    # convet angle into rad
    rangle = np.deg2rad(angle)  # angle in radians
    # calculate new image width and height
    nw = (abs(np.sin(rangle) * h) + abs(np.cos(rangle) * w)) * scale
    nh = (abs(np.cos(rangle) * h) + abs(np.sin(rangle) * w)) * scale
    # ask OpenCV for the rotation matrix
    rot_mat = cv2.getRotationMatrix2D((nw * 0.5, nh * 0.5), angle, scale)
    # calculate the move from the old center to the new center combined
    # with the rotation
    rot_move = np.dot(rot_mat, np.array([(nw - w) * 0.5, (nh - h) * 0.5, 0]))
    # the move only affects the translation, so update the translation
    # part of the transform
    rot_mat[0, 2] += rot_move[0]
    rot_mat[1, 2] += rot_move[1]
    # map
    return cv2.warpAffine(
        img, rot_mat, (int(math.ceil(nw)), int(math.ceil(nh))),
        flags=cv2.INTER_LANCZOS4)


if __name__ == '__main__':
    # box_point = [(100, 100), (500, 500)]
    # img_point = [(350, 150), (450, 400)]
    # img_point(box_point[0][0])
    # 测试判断
    location = image_rotate()

    img = r"C:\Users\9000\Desktop\emblem.jpg"

    # # 人像面
    # location = 4
    # if location:
    #     angle = (location-1)*90
    #     # 逆时针角度
    #     data = rotate_image(img, -angle)
    #     cv2.imshow('data',data)
    #     cv2.waitKey(100000)

    # 国徽面
    location = 4
    if location:
        angle = (location-2)*90
        # 逆时针角度
        data = rotate_image(img, -angle)
        print(type(data))
        print(data.shape)
        cv2.imshow('data', data)
        cv2.waitKey(100000)
