# -*- coding: utf-8 -*-
# @Time    : 2022/11/3 10:05
import hashlib
import requests
import warnings


class RpaOcr(object):
    def __init__(self):
        warnings.warn("rpa_ocr的方法已不被支持，新的接口调用方式请查看rpa_api.py", DeprecationWarning, stacklevel=2)

    def genearteMD5(self, strs: str) -> str:
        hl = hashlib.md5()
        # Tips
        # 此处必须声明encode
        # 否则报错为：hl.update(str)    Unicode-objects must be encoded before hashing
        hl.update(strs.encode(encoding='utf-8'))
        return hl.hexdigest()

    def signutil(self, postBody: dict, secret: str) -> str:
        """
        进行签名验证
        :param postBody: 请求的全部参数
        :param secret: 密钥
        """
        # 进行签名验证
        # 按照参数名的字典排序
        postBody_data = sorted(postBody.keys(), reverse=True)
        # print(postBody_data)

        # 拼接参数，按照a=1&b=2的规则拼接
        strs = ''
        for i in postBody_data:
            strs += f"{i}={postBody[i]}&"

        # 拼接字符串的尾部拼接上 secret=xxx
        strs += f"secret={secret}"
        # print(strs)

        # 计算MD5值，小写
        return self.genearteMD5(strs)

    def httputil(self, url: str, payload: dict, key: str, secret: str):
        """
        请求工具方法
        :param url:str 请求url
        :param payload:dict 当前请求的全部参数
        :param key:str 请求所需的key值
        :param secret:str 请求所需的密钥
        """
        file_name = payload['file_path'].split('\\')[-1]
        files = [
            ('file', (file_name, open(payload['file_path'], 'rb'), 'image/jpeg'))
        ]
        headers = {
            # 下面的key从/admin界面查询或由管理员下发， sign为签名，通过签名工具类进行计算
            'key': key,
            'sign': self.signutil(payload, secret)
        }

        response = requests.request("POST", url, headers=headers, data=payload, files=files)

        return response.json()

    def ocr(self, api: str, key: str, secret: str, payload: dict, is_intranet: bool = True):
        """
        进行ocr识别
        :param api:str 要请求的接口
        :param key:str 请求所需的key值
        :param secret:str 请求所需的密钥
        :param payload:dict 当前请求的全部参数,{'file_path': ...},'file_path'为必填参数,具体不同接口所需的参数不同,可查看Rpa_ocr接口文档
        :param is_intranet:bool 可选值,默认为True(内网请求),True为内网请求,False为外网请求
        :return: ocr识别结果
        """
        warnings.warn("rpa_ocr的方法已不被支持，新的接口调用方式请查看rpa_api.py", DeprecationWarning, stacklevel=2)

        if is_intranet:
            url = "http://172.29.9.116:10001" + api
        else:
            url = "http://120.26.77.174:8000" + api
        text = self.httputil(url, payload, key, secret)
        return text

    def __call__(self, filename, is_intranet: bool = True):
        warnings.warn("rpa_ocr的方法已不被支持，新的接口调用方式请查看rpa_api.py", DeprecationWarning, stacklevel=2)

        api = '/api/ocr/text'
        # key 和 secret 从管理界面（"http://172.29.9.116:10001/admin"）查看 或由管理员下发
        key = "123"
        secret = "12sass"
        if is_intranet:
            url = "http://172.29.9.116:10001" + api
        else:
            url = "http://120.26.77.174:8000" + api
        text = self.httputil(url, {"file_path": filename}, key, secret)
        return text

    def get_address(self, text: str, is_intranet: bool = True):
        warnings.warn("rpa_ocr的方法已不被支持，新的接口调用方式请查看rpa_api.py", DeprecationWarning, stacklevel=2)

        api = '/api/address/structureaddress'
        # key 和 secret 从管理界面（"http://172.29.9.116:10001/admin"）查看 或由管理员下发
        key = "123"
        secret = "12sass"
        data = {"address": text}
        if is_intranet:
            url = "http://172.29.9.116:10001" + api
        else:
            url = "http://120.26.77.174:8000" + api
        headers = {
            # 下面的key从/admin界面查询或由管理员下发， sign为签名，通过签名工具类进行计算
            'key': key,
            'sign': self.signutil(data, secret)
        }

        response = requests.request("POST", url, headers=headers, data=text)

        return response.json()


if __name__ == '__main__':
    Ocr = RpaOcr()

    # __call__使用方法,text识别
    ocr_result = Ocr(filename=r"C:\Users\9000\Desktop\emblem.jpg")
    print(ocr_result)

    # ocr_result = Ocr.get_address('安徽省太和县', is_intranet=False)
    # print(ocr_result)
