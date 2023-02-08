# Requests爬虫
import requests

url = "https://movie.douban.com/j/chart/top_list?"

# url参数过长,重新封装参数
param = {
    'type': '24',
    'interval_id': '100:90',
    'action': '',
    'start': 40,
    'limit': 20,
}

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36"
}

resp = requests.get(url=url, params=param, headers=headers)

# 什么也没用,反爬虫:第一时间考虑user-agent
print(resp.json())
resp.close()    # 关闭resp,避免请求过多

