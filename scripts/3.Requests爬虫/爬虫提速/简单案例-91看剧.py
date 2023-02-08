"""
流程:
    1. 拿到548121-1-1.html的页面源代码
    2. 从源代码中提取到m3u8的url
    3. 下载m3u8
    4. 读取m3u8文件, 下载视频
    5. 合并视频(上述下载部分为切片)
"""
import requests
import re

# headers = {
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36"
# }
#
# obj = re.compile(r'"url":"(?P<url>.*?)",', re.S)        # 用来提取m3u8的url地址
# url = "https://91kju.com/vod-play-id-62944-sid-1-pid-1.html"
#
# resp = requests.get(url, headers=headers)
# m3u8_url = obj.search(resp.text).group('url').replace('\\', '')
# # print(m3u8_url)
# resp.close()
#
# """
# <script>var cms_player = {"yun":true,"url":"https:\/\/m3api.awenhao.com\/index.php?note=kkRsgytw4hnar2b5kjcd9&raw=1&n.m3u8",
# "copyright":0,"name":"pdplayer","jiexi":"https:\/\/www.1717yun.com\/jx\/ty.php?url=","time":3,
# "buffer":"\/\/91kju.com\/Public\/loading\/buffer.html","pause":"\/\/91kju.com\/Public\/loading\/pause.html",
# "next_path":null,"next_url":null,"url_path":"kk_91kju_com_bianyuanxingzhe_62944_8_1_1"};</script>
# """
#
# # 下载m3u8文件
# resp2 = requests.get(m3u8_url, headers=headers)
#
# with open('测试视频.m3u8', mode='wb') as f:
#     f.write(resp2.content)
#
# print(resp2.status_code)
# resp2.close()
# print("下载完成！")

# 解析m3u8文件
n = 1

with open("测试视频.m3u8", mode='r', encoding='utf-8') as f:
    for line in f:
        line = line.strip()
        if line.startswith('#'):
            # 如果以#开头,我不需要
            continue

        # print(line)
        # 下载ts片段
        resp3 = requests.get(line)
        f = open(f"video/{n}.ts", mode="wb")
        f.write(resp3.content)
        f.close()
        resp3.close()
        n += 1
        print("完成了1个")

