# -*- coding: utf-8 -*-
# @Time    : 2022/8/4 15:05
# @Author  : SYH
# @File    : 彩票数据分析.py
# @Software: PyCharm

import requests
from bs4 import BeautifulSoup as bs
import csv

import pandas as pd
import matplotlib.pyplot as plt

# # 先爬取数据
# url = 'http://datachart.500.com/ssq/history/history.shtml'
#
# resp = requests.get(url)
# resp.encoding = 'gb2312'
# # 先生成bs对象
# page = bs(resp.text, "html.parser")
#
# # 从中查找数据
# div = page.find("div", attrs={'class': 'chart'})
# table = div.find('table')
# trs = table.find_all('tr')[2:]
# f = open("data.csv", mode="w", newline='')
# csvwriter = csv.writer(f)
#
# for tr in trs:
#     tds = tr.find_all('td')
#     result_temp = []
#     for td in tds:
#         td.text.strip(',')
#         result_temp.append("".join(td.text.replace(',', '').split()))
#
#     csvwriter.writerow(result_temp)
#     # print(result_temp)
#
# f.close()
# print('over!')


# 开始处理数据
# 先引入数据
df = pd.read_csv('data.csv', header=None, index_col=0)
# print(df)

# 把所有的红球号码拿出来
# 从1-6
red_ball = df.loc[:, 1:6]
# print(red_ball)

# 把所有的蓝球号码拿出来
blue_ball = df.loc[:, 7]
# print(blue_ball)

# 做数据统计
red_ball_count = pd.value_counts(red_ball.values.flatten())
# print(red_ball_count)
blue_ball_count = pd.value_counts(blue_ball)
# print(blue_ball_count)

# 可视化展示     --> 图表
# fig, ax = plt.subplots(2, 1)  # 一次创建多个图表

# 用饼图来展示
plt.pie(red_ball_count, labels=red_ball_count.index, radius=1, wedgeprops={"width": 0.3})  # wedgeprops设计每个扇形的长度 楔子
plt.pie(blue_ball_count, labels=blue_ball_count.index, radius=0.5, wedgeprops={"width": 0.2})
plt.show()  # 展示图表
