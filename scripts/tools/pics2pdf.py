# -*- coding: utf-8 -*-
# @Time    : 2022/11/3 14:00
from PIL import Image
import os


def combine_imgs_pdf(folder_path, pdf_file_path):
    """
    合成文件夹下的所有图片为pdf
    Args:
        folder_path (str): 源文件夹
        pdf_file_path (str): 输出路径
    """
    files = os.listdir(folder_path)
    png_files = []
    sources = []
    for file in files:
        if 'png' in file or 'jpg' in file:
            png_files.append(folder_path + file)
    png_files.sort()
    output = Image.open(png_files[0])
    png_files.pop(0)
    for file in png_files:
        png_file = Image.open(file)
        if png_file.mode == "RGB":
            png_file = png_file.convert("RGB")
        sources.append(png_file)
    output.save(pdf_file_path, "pdf", save_all=True, append_images=sources)


if __name__ == "__main__":
    folder = r"D:\工作相关\需求\阳光保险材料整理\test\img\\"
    pdfFile = r"D:\工作相关\需求\阳光保险材料整理\test\代偿债务与权益转让确认书.pdf"
    combine_imgs_pdf(folder, pdfFile)
