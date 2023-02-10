# -*- coding: utf-8 -*-
# @Time    : 2022/8/16 16:21

import pdfplumber

from openpyxl import Workbook
import os
import re
from flows.flow import ScriptDef, DirectoryItem, ListDataFlow
import time
from rpalib.log import logger
import pandas as pd
import requests
import ast
import numpy as np
from paddle.dataset.image import cv2
import paddlehub as hub


ocr = hub.Module(name="chinese_ocr_db_crnn_mobile")

class JSxj(ListDataFlow):
    def __init__(self, directory) -> None:
        super().__init__()
        self.path = directory  # 文件夹路径
        self.all_path_list = []
        self.all_pdf_list = []
        self.all_message_dict = []

    def obtain_file(self):
        """
        获取要提取的文件名
        """
        pdf_path = os.listdir(self.path)

        for path in pdf_path:
            # 拼接pdf路径
            new_pdf_path = os.path.join(self.path, path)
            self.all_pdf_list.append(new_pdf_path)
        return self.all_pdf_list

    def open_pdf(self):
        """
        打开pdf
        """
        for i in self.all_pdf_list:
            logger.info(f"开始执行{os.path.basename(i)}")
            if i.endswith('.pdf'):
                # 判断是否为pdf文件
                message = self.get_pdf_info(i)
                from_pdf = True
                self.handle_texts(message, i, from_pdf)
                logger.info(f'{os.path.basename(i)}提取完成')
            elif i.endswith('.png'):
                # 判断是否为png文件
                message = self.get_png_info(i)
                # self.get_png_info(i)

                from_pdf = False
                self.handle_texts(message, i, from_pdf)
                logger.info(f'{os.path.basename(i)}提取完成')
            else:
                logger.error(f"{os.path.basename(i)} 文件格式不匹配！")

    def handle_texts(self, text, file_path, from_pdf=True):
        """
        处理text
        """
        error_info = ''
        try:
            # 判断是从pdf读的字符还是从png中ocr识别的字符
            if from_pdf:
                # pdf中的数据提取

                # 两个正则分别对应两种不同样式下的户名提取
                ht_name = re.search('户名：\s*(.*)账号', text, re.S).group(1).replace('\n', '').replace(' ', '')
                if '交易结果' in ht_name:
                    ht_name = re.search('户名：\s*(.*)交易结果', text, re.S).group(1).replace('\n', '').replace(' ', '')
                else:
                    # 第2种样式下，部分凭证的交易结果在前，户名在后,且户名字体小
                    ht_name = re.search('渠道返回成功(.*?)户名：', text, re.S).group(1).replace('\n', '').replace(' ', '')
                if ht_name == '':
                    # 第2种样式下，部分凭证的交易结果在前，户名在后,且户名字体正常
                    ht_name = re.search('户名：(.*?)账号：', text, re.S).group(1).replace('\n', '').replace(' ', '')
                print(ht_name)
                if ht_name == '':
                    ht_name = None
                    error_info = '户名提取失败'

                # 目前的两种样式下的交易金额的提取方式相同
                ht_num = re.search('￥(.*)\s*订单编号', text, re.S).group(1).replace(',', '').split('.')[0]
                # print(ht_num)
                if ht_num == '':
                    ht_num = None
                    error_info = '交易金额提取失败'

            else:
                # png中的数据提取
                text = text.replace("['", '')
                text = text.replace("']", '')
                # print(text)

                ht_name = re.search('收款户名(.*?)收款', text, re.S).group(1).replace("'", '').replace(',', '').strip()
                # print(ht_name)
                if ht_name == '':
                    ht_name = None
                    error_info = '户名提取失败'

                ht_num = re.search('付款金额(.*?)元', text, re.S).group(1).replace("'", '').replace(',', '').strip()
                # print(ht_num)
                if ht_num == '':
                    ht_num = None
                    error_info = '交易金额提取失败'

            if error_info != '':
                logger.info(error_info)
            self.all_message_dict.append({
                '识别文件名称': file_path,
                '户名': ht_name,
                '交易金额': ht_num,
                '报错': error_info,
            })

        except:
            error_info = '数据提取失败'
            self.all_message_dict.append({
                '识别文件名称': file_path,
                '户名': None,
                '交易金额': None,
                '报错': error_info,
            })
            logger.info(error_info)

        return self.all_message_dict

    def get_pdf_info(self, file):
        """这个函数是为了少些变量，只需要写正则表达式就行了，将提取的信息存储到列表里，返回出来
        :param file: pdf文件路径，全路径
        """
        texts = ""
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                texts += page.extract_text() + "\n"
        # print(texts)
        return texts

    def get_png_info(self, file):
        """
        新样式中的放款协议存在png格式的文件,该方法处理并获取png文件中的信息
        """
        # 通过ocr识别
        # url = 'http://172.29.12.242:5000/rpa/ocr'
        url = 'http://47.97.112.170/rpa/ocr'
        files = {'file': (os.path.basename(file), open(file, mode='rb'))}
        # print(type(files))
        # print(files)
        data = requests.post(url, files=files)
        text = ast.literal_eval(data.text)
        # print(str(text['text']))

        return str(text['text'])


        # # file = r"D:\工作相关\需求\晋商消金-放款凭证信息提取\test\A1022020112507224669.png"
        # np_images = cv2.imread("A1022020112507224669.png")
        # print(np_images)
        # results = ocr.recognize_text(
        #     images=[np_images],  # 图片数据，ndarray.shape 为 [H, W, C]，BGR格式；
        #     use_gpu=False,  # 是否使用 GPU；若使用GPU，请先设置CUDA_VISIBLE_DEVICES环境变量
        #     # use_gpu=True,            # 是否使用 GPU；若使用GPU，请先设置CUDA_VISIBLE_DEVICES环境变量
        #     # output_dir='ocr_result',  # 图片的保存路径，默认设为 ocr_result；
        #     # visualization=True,  # 是否将识别结果保存为图片文件；
        #     box_thresh=0.5,  # 检测文本框置信度的阈值；
        #     text_thresh=0.5)  # 识别中文文本置信度的阈值；
        # print(type(results))
        # print(results)

    # def ocr(self):
    #     file = request.files.get('file')
    #
    #     if not file:
    #         return "文件不能为空"
    #
    #     # 判断上传文件类型
    #     file_name, file_type = file.filename.split(".")
    #
    #     if file_type.lower() == "pdf":
    #         save_path = os.path.join(upload_path, f"{file_name}-{str(uuid.uuid4()).split('-')[0]}.{file_type}")
    #         print(save_path)
    #         # 保存文件
    #         file.save(save_path)
    #         # 拆分pdf成图片
    #         imgs, out_dir = split_pdf(save_path)
    #         # 图片提取信息
    #         info = default_impl.ocr(imgs)
    #         if not info:
    #             return json.dumps({"code": 500, "msg": "获取信息失败"}, ensure_ascii=False)
    #         # 删除上传文件
    #         os.remove(save_path)
    #         shutil.rmtree(out_dir)
    #         return json.dumps({"code": 200, "msg": "success", "text": info}, ensure_ascii=False)
    #
    #     if file_type.lower() in ['png', 'jpg', 'jpeg']:
    #         save_path = os.path.join(upload_path, f"{file_name}-{str(uuid.uuid4()).split('-')[0]}.{file_type}")
    #         # 保存文件
    #         file.save(save_path)
    #         # 图片提取信息
    #         # default_impl.ocr 需要传入图片列表
    #         info = self.ocr_paddleMod([save_path])
    #         if not info:
    #             return json.dumps({"code": 500, "msg": "获取信息失败"}, ensure_ascii=False)
    #         # 删除上传文件
    #         os.remove(save_path)
    #         return json.dumps({"code": 200, "msg": "success", "text": info}, ensure_ascii=False)
    #
    #     return json.dumps({"code": 404, "msg": "Failed", "text": "请检查上传文件并重试"}, ensure_ascii=False)
    #
    # def ocr_paddleMod(self, images:str) -> str:
    #     """
    #     ocr识图
    #     :param images: 识别图片列表
    #     :return: ocr识别文字内容
    #     """
    #     try:
    #         img_nps = [np.fromfile(file, dtype=np.uint8) for file in images]  # 用numpy读取处理图片
    #         img = [cv2.imdecode(img_np, cv2.IMREAD_COLOR) for img_np in img_nps]
    #         ocr = hub.Module(name="chinese_ocr_db_crnn_mobile")
    #         results = ocr.recognize_text(images=img)
    #         a1 = []
    #         for result in results:
    #             data = result['data']
    #             for info in data:
    #                 a1.append([info["text"]])
    #         return a1
    #     except Exception as e:
    #         return "提取信息失败"


    def to_excel(self):
        """
        将数据写入excel表
        """
        df = pd.DataFrame(self.all_message_dict)
        beijing_time = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime(time.time()))
        df.to_excel(os.path.join(os.path.dirname(self.path), f"晋商消金-放款凭证-信息提取数据{beijing_time}.xlsx"), index=False)
        f = os.path.join(os.path.dirname(self.path), f"晋商消金-放款凭证-信息提取数据{beijing_time}.xlsx")

        logger.info(f"提取数据保存在 {f}")

    def run(self):
        """
        总控
        """
        self.obtain_file()
        self.open_pdf()
        self.to_excel()


export = ScriptDef(
    cls=JSxj,
    group='其他',
    title="晋商消金-放款凭证-提取信息",
    description="晋商消金-放款凭证-提取信息",
    arguments=[
        DirectoryItem(title="存储待提取文件的目录", name="directory"),
    ]
)

if __name__ == '__main__':
    gm = JSxj(
        r"D:\工作相关\需求\晋商消金-放款凭证信息提取\样例2"
    )
    gm.run()
