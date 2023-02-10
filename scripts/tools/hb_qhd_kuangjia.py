# -*- coding: utf-8 -*-
# @Time    : 2022/11/10 10:24
# 框架
import numpy as np
import pandas as pd
import os
import re
import time
import win32gui
from rpalib.helens import AutoWinBrowser
from rpalib.log import logger
from flows.flow import ScriptDef, FileItem, SelectItem, ListDataFlow, StringItem, DirectoryItem
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait


# 河北秦皇岛昌黎县执保立案
class QHD_CL_ZX_LA(ListDataFlow):
    # 这里声明全局变量
    def __init__(self, spv, excel) -> None:
        super().__init__()
        self.spv = spv  # 公司名称
        self.excel = excel  # 读取的excel表格
        self.b = AutoWinBrowser(browser_type=3)  # 3代表启动ie浏览器
        self.url = 'http://131.104.3.40/sym/'

    # 1-登录
    def login(self):
        pass

    # 2-查询
    def search(self, row):
        pass

    # 3-编辑页面
    def edit(self):
        pass

    # 读取身份证信息提取的表格，得到DataFrame
    def get_df(self, excel_path):
        df = pd.read_excel(excel_path, sheet_name=0, header=0, dtype='string')  # 读取表格
        df.dropna(axis='index', how='all', inplace=True)  # 过滤所有值为空的行
        df["状态"] = np.nan  # 运行程序时候，将状态列，初始化为空
        df = df.fillna('')  # 填充NaN值
        return df

    # 将数据转存为excel
    def save_excel(self, save_excel_df):
        beijing_time = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime(time.time()))  # 生成时间格式
        save_excel_path = os.path.join(os.getcwd(), f"河北秦皇岛-昌黎{beijing_time}.xlsx")  # 存储路径
        save_excel_df.to_excel(save_excel_path)  # 输出excel路径
        logger.info(f"程序运行结果： {save_excel_path}")  # 输出程序运行结果保存路径，空格为了方便复制路径

    def run(self):
        df = self.get_df(self.excel)  # 获取df，循环用
        min_handdle = self.login()  # 获取主窗口句柄，关闭其他窗口用
        # 多次尝试，如果挂掉，运行完毕再次运行错误的
        for retry_index in range(3):
            for index, row in df.iterrows():
                try:
                    row = dict(row)
                    if row["状态"] == "ok":
                        continue
                    flag = self.search(row)
                    if flag == None:
                        continue  # 没有搜索到该案号
                except:
                    pass


