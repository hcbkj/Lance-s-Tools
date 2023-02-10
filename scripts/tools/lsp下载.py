# -*- coding: utf-8 -*-
# @Time    : 2022/8/9 11:05
# @File    : lsp下载.py

import requests
from lxml import etree
import time
import os


def download_pic(src):
    root = "D://LSP//"
    path = root + src.split('/')[-1]
    if not os.path.exists(root):
        os.mkdir(root)
    if not os.path.exists(path):
        r = requests.get(src)
        r.raise_for_status()
        with open(path, 'wb') as f:
            f.write(r.content)
            print('爬取成功')


def get_html(url):
    response = requests.get(url)
    response.encoding = 'gbk'
    html = etree.HTML(response.text)
    print(html.xpath('//ul[@class="clearfix"]/li/a/img'))
    img_src = html.xpath('//ul[@class="clearfix"]/li/a/img/@src')
    for src in img_src:
        print(src)
        download_pic(src)


indexa = 1
for i in range(1, 30):
    url = 'https://www.99tu.com/mz/siwameitui/29_{}.html'.format(i)
    print('这是第' + str(indexa) + "页数据")
    indexa = indexa + 1
    get_html(url)
    time.sleep(2)
print('下载完成')
