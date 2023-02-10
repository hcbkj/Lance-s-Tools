# -*- coding: utf-8 -*-
# @Time    : 2022/11/7 14:22
# pdf读取的一些工具方法

import os
import re
import pdfplumber
import fitz
import PyPDF2
from PIL import Image
from rpa_ocr import RpaOcr


class PdfReadTools(object):

    @staticmethod
    def pdf_page_img(pdf_path, save_path):
        doc = fitz.open(pdf_path)
        reader = PyPDF2.PdfFileReader(pdf_path)
        # 获取单个文件页数
        pageNum = reader.getNumPages()
        for pg in range(0, pageNum):
            page = doc.load_page(pg)
            pix = page.get_pixmap(matrix=fitz.Matrix(4, 4))
            img_name = str(pg) + ".png"
            pix.save(rf'{save_path}\{img_name}')

    def pdf2pic(self, pdf_path, pic_path):
        """
        使用正则表达式查找PDF中的图片
        :param pdf_path: pdf的路径
        返回pic_path:图片保存文件夹的路径
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

        # 打印pdf的信息
        print("文件名:{},页数:{},对象:{}".format(pdf_path, len(doc), lenXREF - 1))

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
        print("提取了{}张图片".format(imgCount))
        # return pic_path

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
        texts = texts.replace(' ', '')
        # print(texts)
        return texts

    def ocr_img_info(self, file_path):
        """
        提取pdf中的信息，判断是否为需要的文书,返回值为文书类型,不是需要的文书类型则返回空值
        :param file_path: 文件地址
        """
        # ocr识别图片内容
        result = RpaOcr().ocr(api='/api/ocr/text', is_intranet=False, key='123', secret='12sass',
                              payload={'file_path': file_path})
        # print(result)
        context = result['result']['value']
        return context

    def shengshiqu_re(self):
        import re
        a = ['河南省', '郑州市', '二七区', '宁夏回族自治区', '新疆维吾尔自治区', '香港特别行政区']
        for i in a:
            print(re.search('.[^(省市壮族回维吾尔自治区特别行政区)]*', i).group())
            print(re.search('.*[^省]|.*[^市]|.*[^自治区]', i).group())


if __name__ == '__main__':
    pdf_tool = PdfReadTools()
    file = r"C:\Users\9000\Desktop\445322199111091016莫嘉豪.pdf"
    dir = r'C:\Users\9000\Desktop\0208'
    pdf_tool.pdf2pic(file, dir)

    # img_path = r"D:\工作相关\测试文件夹\img"
    # pdf_tool.pdf2pic(file, img_path)
    #
    # text = ''
    # for img in os.listdir(img_path):
    #     context = pdf_tool.ocr_img_info(os.path.join(img_path, img))
    #     text += context

    # text = pdf_tool.ocr_img_info(file)
    # text = text.replace('\n', '').replace(' ', '')


