# -*- encoding:utf-8 -*-
"""rpa接口使用样例"""
import time
from copy import deepcopy
import hashlib
import json
import os.path
import base64
from dataclasses import dataclass

import requests

IS_INTRANET = True

url = "http://172.29.9.116:10001" if IS_INTRANET else "http://120.26.77.174:8000"
# url = "http://127.0.0.1:8000"


def get_img(data: bytes) -> str:
    """
    base64读图片
    :param data: 字节流图片
    :return: encodestr的图片
    """
    try:
        encodestr = str(base64.b64encode(data), 'utf-8')
    except TypeError:
        encodestr = base64.b64encode(data)
    return encodestr


class OcrUrl(object):
    Text: str = "/api/ocr/text"  # 文字识别
    Table: str = "/api/ocr/table"  # 表格识别
    HandWrite: str = "/api/ocr/handwrite"  # 手写体识别
    IdClassify: str = "/api/idcard/classify"  # 身份证正反面识别
    IdCrop: str = "/api/idcard/crop"  # 身份证图片分割处理
    IdExtract: str = "/api/idcard/extract"  # 身份证按部分识别
    IdProcess: str = "/api/idcard/process"  # 流水线，对身份证图片的从分类到识别全过程，包含与阿里云结果的比对
    Nlp: str = "/api/nlp/extract"  # NLP识别


class RpaAPI(object):
    """计算请求头密钥"""

    @staticmethod
    def check_json_format(raw_msg):
        """
        用于判断一个字符串是否符合Json格式
        """
        if isinstance(raw_msg, str):  # 首先判断变量是否为字符串
            try:
                json.loads(raw_msg, encoding='utf-8')
            except ValueError:
                return False
            return True
        else:
            return False

    def signutil(self, post_body, secret: str) -> str:
        strs = ''
        # print(post_body)
        # 若post_body是json字符串则直接计算
        if self.check_json_format(post_body):
            strs = post_body
        else:
            # 先删除参数中的复杂数据类型，只使用简单数据类型来计算签名
            complex_data_key = []
            for item in post_body.values():
                if type(item) in [list, dict, tuple]:
                    complex_data_key.append(list(post_body.keys())[list(post_body.values()).index(item)])
            for key in complex_data_key:
                post_body.pop(key)
            # 按照参数名的字典排序
            postBody_data = sorted(post_body.keys(), reverse=True)
            # 拼接参数，按照a=1&b=2的规则拼接
            for i in postBody_data:
                strs += f"{i}={post_body[i]}&"
        # 拼接字符串的尾部拼接上 secret=xxx
        strs += f"secret={secret}"
        # 计算MD5值，小写
        return hashlib.md5(strs.encode(encoding='utf-8')).hexdigest()

    def __headers__(self, data) -> dict:
        """生成请求头"""
        KEY = "123"  # key
        SECRET = "12sass"  # 密钥
        h_data = deepcopy(data)
        sign = self.signutil(post_body=h_data, secret=SECRET)
        # print(sign)
        return {'key': KEY, 'sign': sign}

    def __ocr_upload__(self, url_api, file_path, engine, **kwargs):
        """该方法只用于ocr"""
        files = [
            ('file', (os.path.basename(file_path), open(file_path, 'rb'), 'image/jpeg'))
        ]
        data = {"file_path": file_path, "engine": engine}
        data.update(kwargs)

        response = requests.post(url + url_api, headers=self.__headers__(data), data=data, files=files)
        return response.json()

    def ocr(self, file_path: str, ocr_type=OcrUrl.Text, engine="default", **kwargs):
        """
        ocr识别
        :param file_path: 图片文件地址 只支持 "png","jpg","jpeg","tif"
        :param ocr_type: 请求接口
        :param engine: 引擎
        """
        return self.__ocr_upload__(url_api=ocr_type, file_path=file_path, engine=engine, **kwargs)

    def nlp(self, schema: list, text: str):
        """
        nlp识别
        :param schema: 需要识别的关键字，接收列表
        :param text: 需要被识别的文本
        :return:
        """
        api = OcrUrl.Nlp
        data = {'keys': schema, 'text': text}
        # data = json.dumps(data)
        h = self.__headers__(data)
        # h.update({"content-type": "application/json"})
        # print(h)
        response = requests.post(url + api, headers=h, data=data)
        return response.json()

    def get_address(self, address: str, cleanTown="true", multimode="false"):
        r"""
        将包含地址信息的文本，识别为结构化的地址信息，返回省、市、区、乡镇、详细地址等分段信息，能够智能补全缺失的行政区域
        :param address: 包含地址信息的文本，批量模式下多条地址用回车或换行符（\r或\n）分隔
        :param cleanTown: 是否从地址中清洗乡镇、街道级别行政区域信息，默认值为false。若为true，返回结果中会包含town，town_id字段，address字段中将不再包含乡镇级别行政区域信息。
        :param multimode: 是否为批量模式，false为非批量，此时整个text参数认为是一条地址；true为批量，此时根据text参数中的换行符区隔多条地址。默认为true
        """
        api = "/api/address/kstructureaddress"
        data = {"cleanTown": cleanTown, "multimode": multimode, "text": address}
        response = requests.post(url + api, headers=self.__headers__(data), data=data)
        return response.json()

    # def company(self, company: str):
    def company(self, name: str, idcard_no: str, **kwargs):
        r"""
        企业工商信息查询
        """
        # api = "/api/company/info"
        # data = {"company": company}
        # response = requests.post(url + api, headers=self.__headers__(data), data=data)
        # return response.json()
        api = "/api/executed/info"
        data = {
            "name": name,
            "idcard_no": idcard_no
        }
        headers = RpaAPI().__headers__(data)
        response = requests.post(url=url + api, headers=headers, data=data, **kwargs)
        return response.json()

    # def verification_ddddocr(self, image: str):
    #     api = "/api/verification"
    #     data = {"img_base64": image}
    #     response = requests.post(url + api, headers=self.__headers__(data), data=data)
    #     return response.json()


if __name__ == '__main__':
    rpa = RpaAPI()
    # print(rpa.nlp(schema=['时间', '选手', '赛事名称'], text='2月8日上午北京冬奥会自由式滑雪女子大跳台决赛中中国选手谷爱凌以188.25分获得金牌！'))
    result = rpa.ocr(r"C:\Users\9000\Desktop\01.jpg", ocr_type=OcrUrl.IdCrop, raw_mode=True)
    print(result['result']['image'])
    # print(rpa.company(name='彭申平', idcard_no='420982197012087216'))

    # with open(r"C:\Users\9000\Desktop\验证.png", 'rb') as f:
    #     img = get_img(f.read())
    # print(rpa.verification_ddddocr(img))
