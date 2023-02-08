# 1. 如何提取单个页面的数据
# 2. 上线程池,多个页面同时抓取

import requests
from lxml import etree
from concurrent.futures import ThreadPoolExecutor

url = "http://www.xinfadi.com.cn/getPriceData.html"
resp = requests.post(url)
# print(resp.json())
current = resp.json()['current']
print(current)

# html = etree.HTML(resp.text)
# html.xpath()
# print()
