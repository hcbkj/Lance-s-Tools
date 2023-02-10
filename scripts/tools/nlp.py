# -*- coding: utf-8 -*-
# @Time    : 2023/1/9 16:29

import requests

data = {'schema': ['时间', '选手', '赛事名称'],
        'text': '2月8日上午北京冬奥会自由式滑雪女子大跳台决赛中中国选手谷爱凌以188.25分获得金牌！'}
url = r"http://172.29.9.116:9290/rpa/info_extract"
resp = requests.post(url, json=data)
print(resp)
print(resp.json())
