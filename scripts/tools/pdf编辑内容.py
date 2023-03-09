# -*- coding: utf-8 -*-
# @Time    : 2023/3/6 10:50

import io
import re
from pdfminer.high_level import extract_text_to_fp
import docx

# # 解析PDF文件并获取其文本内容
# def extract_text_from_pdf(pdf_path):
#     output = io.StringIO()
#     with open(pdf_path, 'rb') as pdf_file, io.BytesIO() as output_buffer:
#         extract_text_to_fp(pdf_file, output_buffer)
#         output.write(output_buffer.getvalue().decode())
#     return output.getvalue()
#
#
# # 创建一个新的Word文档对象并将PDF文本内容写入其中
# def convert_pdf_to_word(pdf_path, word_path):
#     # 解析PDF文本
#     pdf_text = extract_text_from_pdf(pdf_path)
#
#     # 清理PDF文本内容
#     pdf_text = re.sub('[^\x00-\x7F]+', ' ', pdf_text)
#     pdf_text = pdf_text.encode('utf-8').decode('utf-8')
#
#     # 创建一个新的Word文档对象
#     doc = docx.Document()
#
#     # 将PDF文本内容写入Word文档对象中
#     doc.add_paragraph(pdf_text)
#
#     # 保存Word文档
#     doc.save(word_path)
#     print('ok')
#
#
# convert_pdf_to_word(pdf_path=r'D:\\工作相关\\需求\\苏宁要素表pdf批量删除信息\\test\\鲍江波-411282198201127016-要素表.pdf',
#                     word_path=r'D:\\工作相关\\需求\\苏宁要素表pdf批量删除信息\\test\\鲍江波-411282198201127016-要素表.docx')

import sys
import fitz


def mark_word(page, text):
    """Underline each word that contains 'text'.
    """
    found = 0
    for block in page.get_text_blocks():  # 获取页面中的所有文本块
        if text in block[4]:  # w[4] is the word's string
            found += 1  # count
            rect = fitz.Rect(block[:4])  # make rect from word bbox
            page.draw_rect(rect, color=(1, 1, 1), fill=(1, 1, 1))  # draw a white rectangle over the text block
    return found


if __name__ == '__main__':
    pdf_path = r"D:\工作相关\需求\苏宁要素表pdf批量删除信息\test\鲍江波-411282198201127016-要素表.pdf"
    # fname = sys.argv[1]  # filename
    text = '代理人：封游川'
    document = fitz.open(pdf_path)

    print("修改部分 '%s' 文件名： '%s'" % (text, document.name))

    new_doc = False  # indicator if anything found at all

    for page in document:  # scan through the pages
        found = mark_word(page, text)  # mark the page's words
        if found:  # if anything found ...
            new_doc = True
            print("found '%s' %i times on page %i" % (text, found, page.number + 1))
    document.save(r"D:\工作相关\需求\苏宁要素表pdf批量删除信息\test\new-要素表.pdf")

    if new_doc:
        # doc.saveIncr()
        document.save(r"D:\工作相关\需求\苏宁要素表pdf批量删除信息\test\new-要素表.pdf")
