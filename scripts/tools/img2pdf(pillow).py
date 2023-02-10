# -*- coding: utf-8 -*-
# @Time    : 2022/8/17 11:38

from PIL import Image
import os


def convert_img_pdf(input_path, output_path):
    """
    转换图片为pdf格式
    Args:
        filepath (str): 文件路径
        output_path (str): 输出路径
    """
    file_list = os.listdir(input_path)
    for file in file_list:
        file_path = os.path.join(input_path, file)
        # print(file_path)
        output = Image.open(file_path)
        output.save(output_path, "pdf", save_all=True)
        output.close()
        print(f'{file}转换完成!')
    print('全部转换完成')


if __name__ == "__main__":
    input_path = r"D:\input"
    output_path = "D:output"

    convert_img_pdf(input_path, output_path)
