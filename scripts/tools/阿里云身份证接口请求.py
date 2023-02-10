# # -*- coding: utf-8 -*-
#
# import requests
# import os
# import base64
#
#
# def get_img(data: bytes) -> str:
#     """
#     base64读图片
#     :param data: 字节流图片
#     :return: encodestr的图片
#     """
#     try:
#         encodestr = str(base64.b64encode(data), 'utf-8')
#     except TypeError:
#         encodestr = base64.b64encode(data)
#
#     return encodestr
#
#
# def extract():
#     url = 'https://dm-51.data.aliyun.com/rest/160601/ocr/ocr_idcard.json'
#     result = {}
#     headers = {
#         'Authorization': 'APPCODE %s' % 'c529065b0e41400bb6cc12e427b646c3',
#     }
#     # face身份证正面，back身份证反面
#     with open(r"C:\Users\9000\Desktop\被告身份证-反面-马岩-410782198811049621.jpg", 'rb') as f:
#         img = f.read()
#     img = get_img(img)
#     r = requests.post(url=url, json={
#         "configure": {"side": "back"}, "image": img
#     }, headers=headers)
#
#     if str(r.status_code) == "403":
#         return RuntimeError("阿里云剩余次数不足")
#
#     # 待测试
#     print(r.status_code)
#     result = r.json()
#     print(result)
#     return result
#
#
# if __name__ == '__main__':
#     extract()


import base64

import requests


def extract(blocks):
    """
        aliyun识别
        :param blocks: crop中完整身份证图片
        :param cls:传入人像面或国徽面的分类结果
        :return: OCR结果
        """
    url = 'https://dm-51.data.aliyun.com/rest/160601/ocr/ocr_idcard.json'
    result = {}
    headers = {
        # 'Authorization': API_AUTH_TOKEN,
        'Authorization': 'APPCODE %s' % 'c529065b0e41400bb6cc12e427b646c3',
    }

    r = requests.post(url=url, json={
        "configure": {"side": 'face'}, "image": blocks
    }, headers=headers)
    print(r.json())

    if str(r.status_code) != "200":
        if str(r.status_code) == "403":
            raise Exception("阿里云：403 剩余次数不足!")
        if str(r.status_code) == "463":
            raise Exception("阿里云：463 用户受限，请稍后重试")
        raise Exception("阿里云：接口调用失败，" + "当前请求状态码为：" + str(r.status_code))

    return result


if __name__ == '__main__':
    with open(r"C:\Users\9000\Desktop\陈凯-370826198901096415-被告身份证.JPG", 'rb') as f:
        file = str(base64.b64encode(f.read()), 'utf-8')
    print(extract(file))

