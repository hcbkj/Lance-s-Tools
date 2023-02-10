# -*- coding: utf-8 -*-
# @Time    : 2023/1/30 16:26

import requests
import base64


def request(url: str, headers: dict, data: dict):
    r = requests.post(url=url, json=data, headers=headers)
    return r


def get_img(img_file):
    if img_file.startswith("http"):
        return img_file
    else:
        with open(img_file, 'rb') as f:  # 以二进制读取本地图片
            data = f.read()
    try:
        encodestr = str(base64.b64encode(data), 'utf-8')
    except TypeError:
        encodestr = base64.b64encode(data)

    return encodestr

def parse_jpg(file_path):
    r = requests.post("https://tysbgpu.market.alicloudapi.com/api/predict/ocr_general", json={
        "image": get_img(file_path),
        "configure": {"min_size": 16, "output_prob": True, "output_keypoints": False, "skip_detection": False,
                      "without_predicting_direction": False}
    }, headers={
        'Authorization': 'APPCODE %s' % 'c529065b0e41400bb6cc12e427b646c3',
        'Content-Type': 'application/json; charset=UTF-8'
    })
    print(r.text)
    return r


if __name__ == '__main__':
    url = 'https://tysbgpu.market.alicloudapi.com/api/predict/ocr_general'
    print(parse_jpg(r'D:\工作相关\需求\宁波银行信用卡流水清单信息提取-对账单\兼容\0.png'))
    # headers = {
    #     'Authorization': 'APPCODE %s' % 'c529065b0e41400bb6cc12e427b646c3',
    # }
    # data = {
    #     "image": get_img(r'D:\工作相关\需求\宁波银行信用卡流水清单信息提取-对账单\兼容\0.png'),
    #     "configure": {"min_size": 16, "output_prob": True, "output_keypoints": False, "skip_detection": False,
    #                   "without_predicting_direction": False}
    # }
    #
    # response = request(url, headers, data)
    #
    # print(response.json())
    # print(response.status_code)
