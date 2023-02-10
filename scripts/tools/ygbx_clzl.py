# -*- coding: utf-8 -*-
# @Time    : 2022/11/3 10:39
# 阳光保险材料整理需求

import os
import re
import shutil
import pdfplumber
from rpalib.log import logger
from rpalib.rpa_ocr import RpaOcr
from flows.flow import FileItem, ScriptDef, ListDataFlow, DirectoryItem
import fitz
from PIL import Image
import pandas as pd


class Ygbx_clzl(ListDataFlow):
    def __init__(self, directory, new_directory, excel_path):
        super().__init__()
        # 选择存放文件的目录
        self.directory = directory
        self.new_directory = new_directory
        self.excel_path = excel_path
        self.all_beigao_info = []
        self.all_beigao_info_new = []
        self.son_file_list = []

    def create_dirs(self):
        df = pd.read_excel(self.excel_path, usecols=["客户名称", "保单号", "身份证号", "合作银行"])
        bank_list = ['北京中关村银行股份有限公司', '渤海银行股份有限公司广州分行', '东亚银行（中国）有限公司', '福建海峡银行股份有限公司',
                     '光大银行股份有限公司', '河北银行股份有限公司', '徽商银行股份有限公司合肥云谷路支行', '廊坊银行股份有限公司营业部', '龙江银行股份有限公司',
                     '盛京银行股份有限公司沈阳分行', '烟台银行股份有限公司', '长春农村商业银行股份有限公司', '中国对外经济贸易信托有限公司', '重庆农村商业银行股份有限公司']
        # 创建合作银行对应文件夹
        for bank in bank_list:
            if not os.path.exists(os.path.join(self.new_directory, bank)):
                os.mkdir(os.path.join(self.new_directory, bank))
        for _, data in df.iterrows():
            data = dict(data)
            # 创建客户名称+身份证号文件夹
            personal_folder = os.path.join(os.path.join(self.new_directory, data['合作银行']), data['客户名称'] + data['身份证号'])
            if not os.path.exists(personal_folder):
                os.mkdir(personal_folder)
            data['被告文件夹'] = personal_folder
            self.all_beigao_info.append(data)

    def pdf2pic(self, pdf_path, pic_path):
        """
        使用正则表达式查找PDF中的图片
        :param pdf_path: pdf的路径
        :param pic_path:图片保存文件夹的路径
        """
        # pic_path:图片保存文件夹的路径
        # pic_path = pdf_path.strip(pdf_path.split("\\")[-1]) + 'img'
        # 创建图片存放路径
        if not os.path.exists(pic_path):
            os.mkdir(pic_path)
        # 使用正则表达式来查找图片
        checkXO = r"/Type(?= */XObject)"
        checkIM = r"/Subtype(?= */Image)"
        # 打开pdf
        doc = fitz.open(pdf_path)
        # 图片计数
        imgCount = 0
        lenXREF = doc.xref_length()

        # # 打印pdf的信息
        # print("文件名:{},页数:{},对象:{}".format(pdf_path, len(doc), lenXREF - 1))

        # 遍历每一个对象
        for i in range(1, lenXREF):
            # 定义对象字符串
            text = doc.xref_object(i)
            isXObject = re.search(checkXO, text)
            # 使用正则表达式查看是否是图片
            isImage = re.search(checkIM, text)
            # 如果不是对象也不是图片，则continue
            if not isXObject or not isImage:
                continue
            imgCount += 1
            # 根据索引生成图像
            pix = fitz.Pixmap(doc, i)
            # 根据pdf的路径生成图片的名称
            new_name = "img_{}.png".format(imgCount)

            # 如果pix.n<5，可以直接存为png
            if pix.n < 5:
                pix.writePNG(os.path.join(pic_path, new_name))
            # 否则先转换CMYK
            else:
                pix0 = fitz.Pixmap(fitz.csRGB, pix)
                pix0.writePNG(os.path.join(pic_path, new_name))
                pix0 = None
        # 释放资源
        pix = None
        # print("提取了{}张图片".format(imgCount))

    def combine_imgs_pdf(self, folder_path, pdf_file_path):
        """
        合成文件夹下的所有图片为pdf
        :param folder_path: 源文件夹
        :param pdf_file_path: 输出文件完整路径
        """
        files = os.listdir(folder_path)
        png_files = []
        sources = []
        for file in files:
            if 'png' in file or 'jpg' in file:
                png_files.append(os.path.join(folder_path, file))
        png_files.sort(key=lambda x: int(x.split('.')[0].split('_')[1]))
        output = Image.open(png_files[0])
        png_files.pop(0)
        for file in png_files:
            png_file = Image.open(file)
            if png_file.mode == "RGB":
                png_file = png_file.convert("RGB")
            sources.append(png_file)
        output.save(pdf_file_path, "pdf", save_all=True, append_images=sources)

    def pdf_read(self, pdf_path):
        """
        该函数是读取含有正常可识别文字的pdf,并提取信息进行判断
        :param pdf_path:pdf文件路径
        """
        texts = ""
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                texts += page.extract_text() + "\n"
        texts = texts.replace(' ', '').replace(' ', '')
        # print(texts)
        return texts

    def ocr_img_info(self, file_path):
        """
        提取pdf中的信息，判断是否为需要的文书,返回值为文书类型,不是需要的文书类型则返回空值
        :param file_path: 文件地址
        """
        try:
            # ocr识别图片内容
            result = RpaOcr().ocr(api='/api/ocr/text', is_intranet=False, key='123', secret='12sass',
                                  payload={'file_path': file_path})
            context = result['result']['value'].replace(' ', '')
            # print(context)
        except:
            raise RuntimeError('"ocr文字识别"未识别出结果')

        return context

    def ocr_idcard_info(self, file_path):
        """
        身份证信息ocr,返回值isface为当前识别身份证图片是否为正面,并返回客户名称和身份证号
        :param file_path: 文件地址
        """
        isface = False
        try:
            ocr = RpaOcr().ocr(api='/api/idcard/classify', is_intranet=False, key='123', secret='12sass',
                               payload={'file_path': file_path})
            # print(ocr['result']['value'].keys())
            # 判断是否为人像面
            if 'FACE' in ocr:
                isface = True

        except:
            raise RuntimeError('"ocr身份证识别"未识别出结果')

        return isface

    def document_type_judged(self, context) -> str:
        """
        :param context: 文书内容
        """
        # 确认文书类型
        # document_type_list的元素是正则表达式
        document_type_list = ['代偿债务与权益转让确认书', '个人贷款保证保险电子保单\n', '借款合同\n', '阳光个人贷款保证保险保险单',
                              '个人无抵押消费贷款申请表', '放款记录\n', '\n借款借据\n', '个人贷款合同.无担保条款.', '支行贷款借据\n',
                              '放款情况说明\n', '个人借款合同\n', '借款凭证（借据）', '个人借款凭证\n', '电子借款借据\n', '\n账户明细\n',
                              '^贷款合同', '^个人信托贷款合同', '放款的情况说明\n', '保险理赔与权益转让确认书']
        document_type = None
        for item in document_type_list:
            if types := re.search(item, context):
                document_type = types.group().replace('\n', '').replace('^', '')
                # print(document_type)

        # 特殊处理
        if document_type:
            if document_type == '贷款合同' or document_type == '个人信托贷款合同':
                document_type = '贷款合同'
            if '个人贷款合同' in document_type:
                document_type = '个人贷款合同'

        return document_type

    def pdf_pic_documemt_pages(self, doc_type, context, img, bank):
        """
        判断图片格式的pdf中,对应文书的部分的起始页
        :param doc_type: 需要判断的文书类型
        :param context: 用于判断的pdf内容
        :param img: 当前正在判断的图片名称
        :param bank: 合作银行 (对于部分文书,银行不同样式也不相同)
        """
        start_num, end_num, no_operate_flag = 0, 0, False

        if doc_type == '借款合同':
            objects = re.search("借款合同\n", context)
            if type(objects) == re.Match:
                start_num = int(img.split('.')[0].split('_')[1])
            if bank == '渤海银行股份有限公司广州分行':
                objects = re.search("借款人不得利用贷款人提供的各类金融产品和服务从事违法活动。", context.replace('\n', ''))
            elif bank == '福建海峡银行股份有限公司':
                objects = re.search("争议解决方式", context.replace('\n', ''))
            elif bank == '烟台银行股份有限公司' or bank == '长春农村商业银行股份有限公司':
                objects = re.search("借款合同签字页", context.replace('\n', ''))
            elif bank == '重庆农村商业银行股份有限公司':
                objects = re.search("法定代表人/负责人", context.replace('\n', ''))
            if type(objects) == re.Match:
                end_num = int(img.split('.')[0].split('_')[1])
        elif doc_type == '代偿债务与权益转让确认书':
            objects = re.search("代偿债务与权益转让确认书[(（]第一联：业务联[）)]", context.replace('\n', ''))
            if type(objects) == re.Match:
                start_num = int(img.split('.')[0].split('_')[1])
            objects = re.search("代偿债务与权益转让确认书[(（]第二联：财务联[）)]", context.replace('\n', ''))
            if type(objects) == re.Match:
                end_num = int(img.split('.')[0].split('_')[1])
        elif doc_type == '个人贷款保证保险电子保单':
            start_num = end_num = int(img.split('.')[0].split('_')[1])
        elif doc_type == '阳光个人贷款保证保险保险单':
            start_num = end_num = int(img.split('.')[0].split('_')[1])
        elif doc_type == '个人无抵押消费贷款申请表':
            objects = re.search("个人无抵押消费贷款申请表", context)
            if type(objects) == re.Match:
                start_num = int(img.split('.')[0].split('_')[1])
            objects = re.search("银行工作人员填写", context.replace('\n', ''))
            if type(objects) == re.Match:
                end_num = int(img.split('.')[0].split('_')[1])
        elif doc_type == '放款记录':
            start_num = end_num = int(img.split('.')[0].split('_')[1])
        elif doc_type == '借款借据':
            start_num = end_num = int(img.split('.')[0].split('_')[1])
        elif doc_type == '个人贷款合同':
            objects = re.search("个人贷款合同.无担保条款.", context)
            if type(objects) == re.Match:
                start_num = int(img.split('.')[0].split('_')[1])
            objects = re.search("关于贷款细节的约定|法定代表人/负责人", context.replace('\n', ''))
            if type(objects) == re.Match:
                end_num = int(img.split('.')[0].split('_')[1])
        elif doc_type == '支行贷款借据':
            start_num = end_num = int(img.split('.')[0].split('_')[1])
        elif doc_type == '放款情况说明':
            start_num = end_num = int(img.split('.')[0].split('_')[1])
        elif doc_type == '个人借款合同':
            objects = re.search("个人借款合同\n", context)
            if type(objects) == re.Match:
                start_num = int(img.split('.')[0].split('_')[1])
            if bank == '河北银行股份有限公司':
                objects = re.search("第十三条合同生效本合同自甲方电子签名、乙方电子签章后生效。", context.replace('\n', ''))
            elif bank == '徽商银行股份有限公司合肥云谷路支行':
                objects = re.search("第二十二条争议解决", context.replace('\n', ''))
            elif bank == '龙江银行股份有限公司':
                objects = re.search("（三）甲方用于本条所述通知与送达用途的联系方式以甲方在阳光财险网络平台上预留的信息为准。",
                                    context.replace('\n', ''))
            if type(objects) == re.Match:
                end_num = int(img.split('.')[0].split('_')[1])
        elif doc_type == '借款凭证（借据）':
            start_num = end_num = int(img.split('.')[0].split('_')[1])
        elif doc_type == '个人借款凭证':
            if bank == '徽商银行股份有限公司合肥云谷路支行':
                start_num = end_num = int(img.split('.')[0].split('_')[1])
        elif doc_type == '电子借款借据':
            start_num = end_num = int(img.split('.')[0].split('_')[1])
        elif doc_type == '账户明细' and bank == '长春农村商业银行股份有限公司':
            # pdf内只含有这一个文书且不好判断文书的结束页
            no_operate_flag = True
        elif doc_type == '贷款合同' and bank == '中国对外经济贸易信托有限公司':
            objects = re.search("^贷款合同", context)
            if type(objects) == re.Match:
                start_num = int(img.split('.')[0].split('_')[1])
            else:
                objects = re.search("^个人信托贷款合同", context)
                if type(objects) == re.Match:
                    start_num = int(img.split('.')[0].split('_')[1])
            objects = re.search("本合同一式叁份", context.replace('\n', ''))
            if type(objects) == re.Match:
                end_num = int(img.split('.')[0].split('_')[1])
        elif doc_type == '放款的情况说明' and bank == '中国对外经济贸易信托有限公司':
            start_num = end_num = int(img.split('.')[0].split('_')[1])
        elif doc_type == '保险理赔与权益转让确认书':
            objects = re.search('保险理赔与权益转让确认书[(（]第一联：业务联[）)]', context.replace('\n', ''))
            if type(objects) == re.Match:
                start_num = int(img.split('.')[0].split('_')[1])
            objects = re.search('保险理赔与权益转让确认书[(（]第二联：财务联[）)]', context.replace('\n', ''))
            if type(objects) == re.Match:
                end_num = int(img.split('.')[0].split('_')[1])

        return start_num, end_num, no_operate_flag

    def dispose_pdf_doc(self, file_path, beigao_info):
        """
        pdf文书处理
        :param file_path: 需要处理的pdf文件路径
        :param beigao_info: 需要处理的文书对应的被告信息
        """
        pdf_inner = self.pdf_read(file_path)
        # 先判断pdf内容类型
        if len(pdf_inner.replace('\n', '')) != 0:
            # 有文本内容
            document_type = self.document_type_judged(pdf_inner)
            if document_type:
                # 龙江银行的代偿确认书为分页的格式,待解决
                hetong_name = f'{beigao_info["客户名称"]}{beigao_info["身份证号"]}{str(document_type)}.pdf'
                shutil.copy(file_path, os.path.join(beigao_info['被告文件夹'], hetong_name))
        else:
            # 图片类型，ocr处理
            img_path = os.path.join(beigao_info['被告文件夹'], 'img')
            self.pdf2pic(file_path, img_path)
            img_path_list = os.listdir(img_path)

            # 处理img文件名按照字符串排序问题
            img_path_list.sort(key=lambda x: int(x.split('.')[0].split('_')[1]))

            text_ocr, document_type, last_page_doc = '', '', ''
            doc_info = []
            for img in img_path_list:
                # 依次对分割出来的图片进行ocr
                try:
                    context = self.ocr_img_info(os.path.join(img_path, img))
                except Exception as e:
                    logger.error(f"报错为{e}, 报错位置为：{e.__traceback__.tb_lineno}")
                    raise RuntimeError(e)

                # 一次循环img文件夹应该获得所有文书类型,存成字典,并循环操作各个文书
                document_type = self.document_type_judged(context)
                # 特殊处理多页文书
                if document_type:
                    last_page_doc = document_type
                elif last_page_doc and not document_type:
                    document_type = last_page_doc

                try:
                    start_num, end_num, no_operate_flag = self.pdf_pic_documemt_pages(document_type, context, img,
                                                                                      beigao_info["合作银行"])
                    if start_num != 0 or end_num != 0:
                        # 同一文书获得了第二个首页信息，跳过
                        if end_num == 0 and [item for item in doc_info if item["文书类型"] == document_type]:
                            pass
                        else:
                            # 筛选并记录文书的结束页
                            doc_info.append(
                                {"文书类型": document_type, "文书开始页": start_num, "文书结束页": end_num,
                                 "无需操作标识符": no_operate_flag})
                            if document_type and end_num != 0:
                                [item for item in doc_info if item["文书类型"] == document_type and item['文书开始页'] != 0][0][
                                    "文书结束页"] = end_num
                                # 删除识别后存在0页的部分
                                for i in doc_info:
                                    if [i] == [item for item in doc_info if
                                               item["文书类型"] == document_type and item['文书开始页'] == 0]:
                                        doc_info.remove(i)
                except:
                    e = RuntimeError(f"文书判断失败，当前文件为{file_path}")
                    logger.error(f"报错文件为{file_path}, 报错位置为：{e.__traceback__.tb_lineno}")
                    raise e

                text_ocr += context

            if len(doc_info) == 1 and doc_info[0]["无需操作标识符"]:
                shutil.copy(file_path, os.path.join(beigao_info['被告文件夹'],
                                                    f'{beigao_info["客户名称"]}{beigao_info["身份证号"]}{doc_info[0]["文书类型"]}.pdf'))
            else:
                for doc in doc_info:
                    # 每个doc为一个字典,包含3个信息,(文书类型,文书开始页,文书结束页),doc_info的长度即为当前pdf中所含需要文书的数量
                    doc_file_path = os.path.join(beigao_info['被告文件夹'], doc["文书类型"])
                    # 删除可能已经存在的文书文件夹
                    if os.path.exists(doc_file_path):
                        shutil.rmtree(doc_file_path)
                    os.mkdir(doc_file_path)

                    if not doc["文书开始页"] and not doc["文书结束页"]:
                        # 不是需要获取的文书,直接跳过
                        continue
                    elif not doc["文书开始页"] or not doc["文书结束页"]:
                        # 文书未成功获取起始页,直接跳过
                        logger.error(f'文书-{doc["文书类型"]}-未成功获取起始页,直接跳过')
                        continue
                    for i in range(doc["文书开始页"], doc["文书结束页"] + 1):
                        doc_img_path = os.path.join(doc_file_path, f'img_{i}.png')
                        # 每次生成文书后，文书对应的img图片都会被移出img文件夹
                        os.rename(os.path.join(img_path, f'img_{i}.png'), doc_img_path)
                    # 将文书合并为新的pdf
                    doc_name = f'{beigao_info["客户名称"]}{beigao_info["身份证号"]}{doc["文书类型"]}.pdf'
                    doc_path = os.path.join(beigao_info['被告文件夹'], doc_name)
                    # 若已存在该文书则删除，并生成新文书
                    if os.path.exists(doc_path):
                        os.remove(doc_path)
                    try:
                        self.combine_imgs_pdf(doc_file_path, doc_path)
                    except Exception as e:
                        logger.error(f'文书{doc["文书类型"]},合并失败')
                        raise e
                    # 合并img为pdf后删除临时文件夹
                    if os.path.exists(doc_file_path):
                        shutil.rmtree(doc_file_path)
            # 删除存放临时文书图片的文件夹
            if os.path.exists(img_path):
                shutil.rmtree(img_path)

    def pdf_doc_set(self, text, file_path, beigao_info):
        """
        对pdf内容可能出现的两种情况：图片格式或者文字格式进行处理
        """
        if len(text.replace('\n', '')) == 0:
            # pdf文件为图片格式时, ocr获取pdf内容
            img_path = os.path.join(self.new_directory, f"{beigao_info['保单号']}-img")
            self.pdf2pic(file_path, img_path)
            for img in os.listdir(img_path):
                context = self.ocr_img_info(os.path.join(img_path, img))
                text += context
            if os.path.exists(img_path):
                shutil.rmtree(img_path)

        # 对子文件夹内pdf文书类型进行判断
        try:
            self.dispose_pdf_doc(file_path, beigao_info)
        except Exception as e:
            beigao_info['报错'] = str(e) + f' 报错位置为：{e.__traceback__.tb_lineno}'
            logger.error(f"报错为{e}, 报错位置为：{e.__traceback__.tb_lineno}")
            return beigao_info

        return beigao_info

    def dispose_son_dir(self, son_dir):
        """
        处理子文件夹
        """
        beigao_info = {}
        # 以保单号为名的子文件夹,该类文件夹名为19位保全号,里面是同一个人的信息(不全,外层文件夹下可能还有该人信息的pdf)
        if os.path.isdir(os.path.join(self.directory, son_dir)):
            beigao_info = [item for item in self.all_beigao_info if son_dir in item.values()][0]
            logger.info(f"子文件夹：{son_dir}")

            # 子文件夹完整路径
            son_dirs_path = os.path.join(self.directory, son_dir)
            son_dir_list = os.listdir(son_dirs_path)
            # 将son_dir_list中的元素进行类型转换
            son_dir_list = list(map(str, son_dir_list))

            # 优先对身份证图片进行处理以获得客户名称和身份证号
            for file in son_dir_list:
                # 文件完整路径
                file_path = os.path.join(son_dirs_path, file)
                if file.endswith('.jpg') or file.endswith('.png'):
                    # 判断是否为身份证图片
                    if 'IDnumber' in file:
                        try:
                            isface = self.ocr_idcard_info(file_path)
                        except Exception as e:
                            beigao_info['报错'] = f'文件"{file_path}"ocr识别出错, 报错信息为{e}, 报错位置为{e.__traceback__.tb_lineno}'
                            beigao_info['身份证图片'] = file_path
                            logger.error(f"报错为{e}, 报错位置为：{e.__traceback__.tb_lineno}")
                            # 身份证识别的精度问题或有时图片模糊，此时若正面已识别到信息，后续操作可继续进行，故continue
                            continue

                        if isface and '身份证正面' not in beigao_info.keys():
                            # 判断身份证正反面
                            beigao_info['身份证正面'] = file_path
                        else:
                            beigao_info['身份证反面'] = file_path

            # 处理pdf
            # 判断子文件夹下的pdf文件数量
            pdf_file_num = 0
            # 处理子文件夹下的pdf
            for file in son_dir_list:
                # 文件完整路径
                file_path = os.path.join(son_dirs_path, file)
                if file.endswith('.pdf'):
                    pdf_file_num += 1
                    text = self.pdf_read(file_path)
                    try:
                        self.pdf_doc_set(text, file_path, beigao_info)
                    except:
                        return beigao_info

            # 将全部图片文件输出
            for file in son_dir_list:
                # 文件完整路径
                file_path = os.path.join(son_dirs_path, file)
                # 图片处理
                if file.endswith('.jpg') or file.endswith('.png'):
                    # 身份证图片
                    if 'IDnumber' in file:
                        try:
                            if file in beigao_info['身份证正面']:
                                # 判断身份证正反面
                                shutil.copy(beigao_info['身份证正面'],
                                            os.path.join(beigao_info['被告文件夹'], beigao_info['客户名称'] + beigao_info[
                                                '身份证号'] + '被告身份证正面.jpg'))
                            elif file in beigao_info['身份证反面']:
                                shutil.copy(beigao_info['身份证反面'],
                                            os.path.join(beigao_info['被告文件夹'], beigao_info['客户名称'] + beigao_info[
                                                '身份证号'] + '被告身份证反面.jpg'))
                            elif file in beigao_info['身份证图片']:
                                shutil.copy(beigao_info['身份证图片'],
                                            os.path.join(beigao_info['被告文件夹'], beigao_info['客户名称'] + beigao_info[
                                                '身份证号'] + '被告身份证.jpg'))
                        except:
                            # 未识别到身份证正面或反面图片，跳过
                            pass
                    elif beigao_info['保单号'] in file:
                        # 文书类图片，且只有一张
                        try:
                            text = self.ocr_img_info(file_path)
                        except Exception as e:
                            beigao_info['报错'] = str(e) + f' 报错位置为：{e.__traceback__.tb_lineno}'
                            logger.error(f"报错为{e}, 报错位置为：{e.__traceback__.tb_lineno}")
                            return beigao_info

                        doc_type = self.document_type_judged(text)
                        if doc_type:
                            shutil.copy(file_path, os.path.join(beigao_info['被告文件夹'], beigao_info['客户名称'] + beigao_info[
                                '身份证号'] + doc_type + '.jpg'))
                    else:
                        # 其他不需要的文书全部跳过
                        pass

        return beigao_info

    def dispose_son_file(self, son_file):
        # 文件完整路径
        error_message = {}
        file_path = os.path.join(self.directory, son_file)
        if os.path.isfile(file_path) and son_file.endswith('pdf'):
            logger.info(f"子文件：{son_file}")
            # 通过保单号查询已取得的全部被告信息
            baodanhao = son_file.split('-')[0]
            beigao_info = [dicts for dicts in self.all_beigao_info_new if dicts['保单号'] == baodanhao][0]
            # 对各类别文书进行处理
            try:
                self.dispose_pdf_doc(file_path, beigao_info)
            except Exception as e:
                error_message['报错'] = str(e)
                return error_message

    def to_excel(self):
        """
        将数据写入excel表
        """
        df = pd.DataFrame(self.all_beigao_info_new, columns=['客户名称', '保单号', '身份证号', '合作银行', '成功整理记录', '报错'])
        df.to_excel(os.path.join(self.new_directory, '阳光保险结果输出.xlsx'), index=False)

    def run(self):
        # 先创建所需的各类文件夹
        self.create_dirs()

        dirs = os.listdir(self.directory)
        for son_files in dirs:
            # 筛选出所有的子文件,存入子文件列表
            if os.path.isfile(son_file_path := os.path.join(self.directory, son_files)):
                self.son_file_list.append(son_file_path)

        # 处理子文件夹
        for son_dir in dirs:
            try:
                outcome = self.dispose_son_dir(son_dir)
                if outcome != {}:
                    self.all_beigao_info_new.append(outcome)
                    if '报错' in outcome.keys():
                        raise RuntimeError(outcome['报错'])
            except Exception as e:
                logger.error(
                    f'"{os.path.join(self.directory, son_dir)}"处理失败,报错为{e},已跳过当前文件夹')
                continue

        # 处理子文件
        for son_file in dirs:
            try:
                error_message = self.dispose_son_file(son_file)
                if error_message:
                    raise RuntimeError(error_message['报错'])
            except Exception as e:
                logger.error(
                    f'"{os.path.join(self.directory, son_file)}"处理失败,报错为{e},已跳过当前文件')
                continue

        # 添加数据记录， need_data为正常获取时各银行所需文书列表
        need_data = {'北京中关村银行股份有限公司': ['被告身份证', '被告身份证正面', '被告身份证反面', '代偿债务与权益转让确认书', '个人贷款保证保险电子保单'],
                     '渤海银行股份有限公司广州分行': ['被告身份证', '被告身份证正面', '被告身份证反面', '个人贷款保证保险电子保单', '借款合同', '代偿债务与权益转让确认书'],
                     '东亚银行（中国）有限公司': ['被告身份证', '被告身份证正面', '被告身份证反面', '个人无抵押消费贷款申请表', '阳光个人贷款保证保险保险单'],
                     '福建海峡银行股份有限公司': ['被告身份证', '被告身份证正面', '被告身份证反面', '个人贷款保证保险电子保单', '代偿债务与权益转让确认书', '借款合同', '放款记录',
                                      '借款借据'],
                     '光大银行股份有限公司': ['被告身份证', '被告身份证正面', '被告身份证反面', '阳光个人贷款保证保险保险单', '个人贷款合同', '支行贷款借据', '放款情况说明',
                                    '代偿债务与权益转让确认书'],
                     '河北银行股份有限公司': ['被告身份证', '被告身份证正面', '被告身份证反面', '个人贷款保证保险电子保单', '代偿债务与权益转让确认书', '个人借款合同',
                                    '借款凭证（借据）'],
                     '徽商银行股份有限公司合肥云谷路支行': ['被告身份证', '被告身份证正面', '被告身份证反面', '个人贷款保证保险电子保单', '个人借款合同', '个人借款凭证',
                                           '代偿债务与权益转让确认书'],
                     '廊坊银行股份有限公司营业部': ['被告身份证', '被告身份证正面', '被告身份证反面', '个人贷款保证保险电子保单'],
                     '龙江银行股份有限公司': ['被告身份证', '被告身份证正面', '被告身份证反面', '个人贷款保证保险电子保单', '代偿债务与权益转让确认书', '电子借款借据', '个人借款合同'],
                     '盛京银行股份有限公司沈阳分行': ['被告身份证', '被告身份证正面', '被告身份证反面', '个人贷款保证保险电子保单'],
                     '烟台银行股份有限公司': ['被告身份证', '被告身份证正面', '被告身份证反面', '个人贷款保证保险电子保单', '代偿债务与权益转让确认书', '放款记录', '借款合同'],
                     '长春农村商业银行股份有限公司': ['被告身份证', '被告身份证正面', '被告身份证反面', '个人贷款保证保险电子保单', '借款合同', '代偿债务与权益转让确认书', '账户明细'],
                     '中国对外经济贸易信托有限公司': ['被告身份证', '被告身份证正面', '被告身份证反面', '个人贷款保证保险电子保单', '阳光个人贷款保证保险保险单', '贷款合同',
                                        '代偿债务与权益转让确认书',
                                        '放款的情况说明'],
                     '重庆农村商业银行股份有限公司': ['被告身份证', '被告身份证正面', '被告身份证反面', '个人贷款保证保险电子保单', '借款合同', '电子借款借据', '保险理赔与权益转让确认书']
                     }
        for beigaoinfo in self.all_beigao_info_new:
            # 成功整理记录
            if '被告文件夹' in beigaoinfo.keys():
                beigaos = os.listdir(beigaoinfo['被告文件夹'])
                zljl_success = ''
                for beigao in beigaos:
                    # 只记录输出的被告文件夹下子文件为成功整理记录
                    if os.path.isfile(os.path.join(beigaoinfo['被告文件夹'], beigao)):
                        zljl_success += beigao.split('.')[-2].lstrip(beigaoinfo['被告文件夹'].split('\\')[-1]) + ';'
                beigaoinfo['成功整理记录'] = zljl_success.rstrip(';')
            else:
                beigaoinfo['成功整理记录'] = ''

            # 报错
            if beigaoinfo['合作银行'] in need_data.keys():
                all_doc = need_data[beigaoinfo['合作银行']]
                success = beigaoinfo['成功整理记录'].split(';')
                fail = set(all_doc).difference(success)
                if '被告身份证' in fail and ('被告身份证正面' not in fail and '被告身份证反面' not in fail):
                    fail.remove('被告身份证')
                error = '缺失;'.join(list(fail))
                if not error:
                    beigaoinfo['报错'] = error
                else:
                    beigaoinfo['报错'] = error + '缺失'

        # print(self.all_beigao_info_new)

        # 将信息写入excel
        logger.info('全部数据处理完毕，开始写入excel')
        self.to_excel()
        logger.info('OK!')


export = ScriptDef(
    cls=Ygbx_clzl,
    group="Nas资料整理",
    title="阳光保险材料整理",
    description="阳光保险材料整理",
    arguments=[
        DirectoryItem(title="材料目录", name="directory"),
        DirectoryItem(title="整理后的目录", name="new_directory"),
        FileItem(title="提取信息的excel表头", name="excel_path")
    ]
)

if __name__ == '__main__':
    Ygbx_clzl(directory=r"D:\工作相关\需求\阳光保险材料整理\test\all_test",
              new_directory=r"D:\工作相关\需求\阳光保险材料整理\test\output",
              excel_path=r"D:\工作相关\需求\阳光保险材料整理\test\阳光保险各资方样例表头(1).xlsx"
              ).run()
