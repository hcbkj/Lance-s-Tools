# 安装 pip install requests

import requests

# # 01 get
# query = input('输入你喜欢的明星:')
# url = f'https://www.sogou.com/web?query={query}'  # 地址栏中复制的url都是get方式,get可以直接拼接url
# headers = {
#         "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36"
# }
#
# resp = requests.get(url, headers=headers)   # 处理一个小小的反爬
#
# print(resp)  # <Response [200]> 200成功
# print(resp.text)  # 拿到页面源代码
# resp.close()    # 关闭resp,避免请求过多

# 02 Post
url = "https://fanyi.baidu.com/sug"

s = input("请输入你要翻译的英文单词:")
data = {
    "kw": s
}
resp = requests.post(url, data=data)
print(resp.json())      # 将服务器返回直接处理成json() =>dict
resp.close()    # 关闭resp,避免请求过多

