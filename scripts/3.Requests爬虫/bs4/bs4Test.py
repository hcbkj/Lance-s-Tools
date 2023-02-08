# 电影天堂爬取2022新片精品
import requests
from bs4 import BeautifulSoup
import csv

url = "https://www.dytt89.com/"

resp = requests.get(url, verify=False)
resp.encoding = "gb2312"
# print(resp.text)
# data_list = []
file = open("2022新片精品.csv", mode="w", encoding='utf-8')

# 先生成对象
page = BeautifulSoup(resp.text, "html.parser")      # 指定为HTML的解释器
# find(标签, 属性=值)
# find_all(标签, 属性=值)
# table = page.find("table", class_="hq_table")  # class是python的关键字
# table = page.find("table", attrs={"class": "hq_table"})  # 和上一行是一个意思. 此时可以避免class
movie_new_div = page.find("div", class_="co_content222")
movie_new_li = movie_new_div.find_all("li")
movie_new_li.pop(0)
for data, i in movie_new_li:
    # data_list.append(data.text)
    # 记得csv.writer().writerow传参是迭代器
    csv.writer(file).writerow([data.text])

file.close()
print("over!")

