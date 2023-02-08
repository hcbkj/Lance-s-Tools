'''
1. 拿到主页面的源代码，然后提取到子页面的链接地址，href
2. 通过href拿到子页面的内容，从子页面中找到图片的下载地址 img -> src
3. 下载图片
'''

import requests
from bs4 import BeautifulSoup
import time

url = 'https://www.umei.cc/bizhitupian/weimeibizhi/'
resp = requests.get(url)
resp.encoding = 'utf-8'

# print(resp.text)
# 把源代码交给bs
main_page = BeautifulSoup(resp.text, 'html.parser')
alist = main_page.find('div', class_='pic-box').find_all('a')
alist.pop(0)
alist.pop(0)
# print(alist)
for a in alist:
    # 如何在bs中拿到标签的属性？直接通过get就可以拿到属性的值
    picture_url = url + a.get('href').split('/', 3)[-1]
    # print(picture_url)

    # 拿到子页面的源代码
    child_page_resp = requests.get(picture_url)
    child_page_resp.encoding = 'utf-8'
    # 从子页面中拿到图片的下载路径
    child_page = BeautifulSoup(child_page_resp.text, 'html.parser')
    img_download = child_page.find('div', class_="content-box").find('img')
    # img_download = child_page.find('div', class_="content-box")
    src = img_download.get('src')

    # 下载图片
    img_resp = requests.get(src)
    # img_resp.content    # 这里拿到的是字节
    img_name = src.split('/')[-1]   # 起名
    with open('img/'+img_name, mode='wb') as f:
        f.write(img_resp.content)       # 写入图片，把该页面下拿到的所有字节保存在文件中，就是一张图片了
    print('over!', img_name)
    time.sleep(1)

print('all over!!')
