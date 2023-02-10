# -*- coding: utf-8 -*-
# @Time    : 2022/11/17 15:35

import sys
import importlib
import os
import os.path
from PyPDF2 import PdfFileReader, PdfFileWriter

importlib.reload(sys)


def MergePDF(pdf_lst, outfile):
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


if __name__ == '__main__':
    pdf_lst = [r"D:\工作相关\需求\阳光保险材料整理\test\龙江银行股份有限公司\C832520201218902496\assign_debt.pdf",
               r"D:\工作相关\需求\阳光保险材料整理\test\龙江银行股份有限公司\C832520201218902496\assign_debt_duplicate.pdf"]

    out = r"D:\工作相关\需求\阳光保险材料整理\test\龙江银行股份有限公司\C832520201218902496\合并文件.pdf"  # 合并后文件名称
    MergePDF(pdf_lst, out)

# import os
# from PyPDF2 import PdfFileMerger
# import warnings
#
# # target_path = r'pdf'  ## pdf目录文件
# # pdf_lst = [f for f in os.listdir(target_path) if f.endswith('.pdf')]
# pdf_lst = [r"D:\工作相关\需求\阳光保险材料整理\test\龙江银行股份有限公司\C832520201218902496\assign_debt.pdf",
#            r"D:\工作相关\需求\阳光保险材料整理\test\龙江银行股份有限公司\C832520201218902496\assign_debt_duplicate.pdf"]
#
# file_merger = PdfFileMerger()
# for pdf in pdf_lst:
#     file_merger.append(pdf, import_bookmarks=False)  # 合并pdf文件
#
# file_merger.write(r"D:\工作相关\需求\阳光保险材料整理\test\龙江银行股份有限公司\C832520201218902496\合并文件.pdf")
