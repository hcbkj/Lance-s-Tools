# 通过页面源代码发现实际上是服务器段加载的数据，需要的数据在页面源代码中有所体现
'''
思路：
    拿到页面源代码 =>requests
    通过re来提取想要的有效信息
'''

import re
import requests
import csv      # csv文件以,作为分隔符,便于之后进行数据分析

url = "https://movie.douban.com/top250"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36"
}

params = {
        "start": 0,
    }

# 解析内容
obj = re.compile(r'<li>.*?<div class="item">.*?<span class="title">(?P<name>.*?)</span>.*?<p class="">'
                 '.*?<br>(?P<year>.*?)&nbsp.*?<span class="rating_num" property="v:average">(?P<score>.*?)</span>'
                 '.*?<span>(?P<num>.*?)人评价</span>', re.S)

f = open('豆瓣电影Top250MovieData.csv', mode='w', encoding='utf-8')
csvWriter = csv.writer(f)
flag = False
i = 0
# 开始匹配
while not flag:
    params['start'] = i
    resp = requests.get(url, headers=headers, params=params)
    page_content = resp.text

    result = obj.finditer(page_content)
    for it in result:
        print(f'{it.group("name")}:{it.group("year").strip()}年上映,{it.group("score")}分,{it.group("num")}人评价')
        dic = it.groupdict()
        dic['year'] = dic['year'].strip()
        csvWriter.writerow(dic.values())
    i += 25
    if i >= 250:
        flag = True

print('over!')

f.close()

