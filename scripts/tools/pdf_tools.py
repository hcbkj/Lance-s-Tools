# -*- coding: utf-8 -*-
# @Time    : 2022/11/7 14:22
# pdf读取的一些工具方法

import os
import re
import glob
import fitz
import PyPDF2
import pdfplumber
from PIL import Image
from PyPDF2 import PdfFileReader, PdfFileWriter


def pdf_page_img(pdf_path: str, save_path: str):
    """
    获取pdf中单独指定页的图片
    :param pdf_path: pdf路径
    :param save_path: 图片保存路径
    """
    doc = fitz.open(pdf_path)
    reader = PyPDF2.PdfFileReader(pdf_path)
    # 获取单个文件页数
    pageNum = reader.getNumPages()
    for pg in range(0, pageNum):
        page = doc.load_page(pg)
        pix = page.get_pixmap(matrix=fitz.Matrix(4, 4))
        img_name = str(pg) + ".png"
        pix.save(rf'{save_path}\{img_name}')


def pdf2pic(pdf_path: str, pic_path: str):
    """
    使用正则表达式查找并获取PDF中所有的图片
    :param pdf_path: pdf的路径
    :param pic_path: 图片保存文件夹的路径
    :return pic_path:图片保存文件夹的路径
    """
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
    return pic_path


def pdf_read(pdf_path: str):
    """
    该函数是读取含有正常可识别文字的pdf,并提取信息进行判断
    :param pdf_path: pdf文件路径
    :return texts: 识别结果字符串
    """
    texts = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            texts += page.extract_text() + "\n"
    texts = texts.replace(' ', '')
    # print(texts)
    return texts


def merge_PDF(pdf_lst: list, outfile: str):
    """
    多个pdf合并为一个
    :param pdf_lst: 列表，每一个元素为一个需要合并的pdf路径
    :param outfile: 多个pdf合并之后的新文件路径
    """
    output = PdfFileWriter()
    outputPages = 0
    pdf_fileName = pdf_lst
    i = 0
    for each in pdf_fileName:
        i = i + 1
        print(i, each)
        # 读取源pdf文件
        input = PdfFileReader(open(each, "rb"))

        # 如果pdf文件已经加密，必须首先解密才能使用pyPdf
        if input.isEncrypted == True:
            input.decrypt("map")

        # 获得源pdf文件中页面总数
        pageCount = input.getNumPages()
        outputPages += pageCount
        print("PageCount: ", pageCount)

        # 分别将page添加到输出output中
        for iPage in range(0, pageCount):
            output.addPage(input.getPage(iPage))

    print("All Pages Number:" + str(outputPages))
    # 最后写pdf文件
    outputStream = open(outfile, "wb")
    output.write(outputStream)
    outputStream.close()
    print("finished")


def img2pdf_all2all(img_path: str, img_type, pdf_path: str):
    """
    fitz库：文件夹中指定img类型图片转换为相同名称的PDF文件，保存至指定文件夹
    :param img_path: 输入图片文件夹路径
    :param img_type: 图片类型，如jpg、png等
    :param pdf_path: 指定PDF输出路径
    """
    for img in sorted(glob.glob(img_path + "\*.%s" % img_type)):
        # 先修改好文件名
        # os.path.basename  返回path最后的文件名。如果path以 / 或 \ 结尾，就会返回空值
        filename = os.path.basename(img).replace(img_type, 'pdf')
        doc = fitz.open()

        imgdoc = fitz.open(img)
        pdfbytes = imgdoc.convert_to_pdf()
        imgpdf = fitz.open('pdf', pdfbytes)
        doc.insert_pdf(imgpdf)
        doc.savefig(pdf_path + '\\' + filename, dpi=300)
        # doc.save(pdf_path + '\\' + filename)

        doc.close()
        print('1张图片已转换')
    print('全部转换完成')


def img2pdf_all2one(img_path: str, img_type, pdf_path: str, pdf_name: str):
    """
    fitz库：文件夹中指定img类型图片转换为一个指定名称的PDF文件，保存至指定文件夹
    :param img_path: 输入图片文件夹路径
    :param img_type: 图片类型，如jpg、png等
    :param pdf_path: 指定PDF输出路径
    :param pdf_name: 指定PDF输出文件名
    """
    doc = fitz.open()

    for img in sorted(glob.glob(img_path + '\*.%s' % img_type)):
        imgdoc = fitz.open(img)
        pdfbytes = imgdoc.convert_to_pdf()
        imgpdf = fitz.open('pdf', pdfbytes)
        doc.insert_pdf(imgpdf)

    doc.save(pdf_path + pdf_name)
    doc.close()
    print('转换完成')


def convert_img_pdf(input_path: str, output_path: str):
    """
    pillow库：转换图片为pdf格式
    :param input_path: 文件路径
    :param output_path: 输出路径
    """
    file_list = os.listdir(input_path)
    for file in file_list:
        file_path = os.path.join(input_path, file)
        output = Image.open(file_path)
        output.save(output_path, "pdf", save_all=True)
        output.close()
        print(f'{file}转换完成!')
    print('全部转换完成')


def combine_imgs_pdf(folder_path: str, pdf_file_path: str):
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

# def shengshiqu_re():
#     import re
#     a = ['河南省', '郑州市', '二七区', '宁夏回族自治区', '新疆维吾尔自治区', '香港特别行政区']
#     for i in a:
#         print(re.search('.[^(省市壮族回维吾尔自治区特别行政区)]*', i).group())
#         print(re.search('.*[^省]|.*[^市]|.*[^自治区]', i).group())
