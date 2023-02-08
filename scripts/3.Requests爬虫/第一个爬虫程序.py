# Requests爬虫:通过编写程序来获取到互联网上的资源
# 百度
# 需求: 用程序模拟浏览器,输入网址并从中获取到资源或内容

from urllib.request import urlopen

url = "http://www.baidu.com"
resp = urlopen(url)
# print(resp.read().decode("utf-8"))
# 保存到文件中
with open("mybaidu.html", mode="w", encoding="utf-8") as f:
    f.write(resp.read().decode("utf-8"))        # 读取到网页的页面内容,源代码
print("over!")


