# -*- coding: utf-8 -*-
# @Time    : 2022/8/17 11:16

import glob
import os
import fitz


def img2pdf_all2all(img_path, img_type, pdf_path):
    """
    文件夹中指定img类型图片转换为相同名称的PDF文件，保存至指定文件夹
    :param img_path: 输入图片文件夹路径
    :param img_type: 图片类型，如jpg、png等
    :param pdf_path: 指定PDF输出路径
    :return:
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


def img2pdf_all2one(img_path, img_type, pdf_path, pdf_name):
    """
    文件夹中指定img类型图片转换为一个指定名称的PDF文件，保存至指定文件夹
    :param img_path: 输入图片文件夹路径
    :param img_type: 图片类型，如jpg、png等
    :param pdf_path: 指定PDF输出路径
    :param pdf_name: 指定PDF输出文件名
    :return:
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


def data_read(pdf_path):
    print('开始')
    pdf_file_list = os.listdir(pdf_path)
    for pdf_file in pdf_file_list:
        if pdf_file.endswith('.pdf'):
            content = ""
            doc = fitz.open(os.path.join(pdf_path, pdf_file))
            for item in doc:
                content += item.get_text()
            print(f'文本内容:{content}')
            break
        else:
            print('文件类型不对')


if __name__ == '__main__':
    # 图片文件夹路径
    img_path = r"D:\工作相关\需求\img2pdf\input"
    # 图片输出文件夹路径
    pdf_path = r"D:\工作相关\需求\img2pdf\output"

    # 指定png格式转换对应 同名的PDF文件
    img2pdf_all2all(img_path, 'png', pdf_path)
    data_read(pdf_path)

    # # 指定png格式图片 转换为 1个指定的PDF文件
    # img2pdf_all2one(img_path, 'png', pdf_path, 'allpng.pdf')
