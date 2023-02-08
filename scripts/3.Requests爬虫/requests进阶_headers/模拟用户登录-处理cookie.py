'''
1. 登录 -> 得到cookie
2. 带着cookie 去请求到书架的url -> 书架上的内容
# 上述操作需连起来
3. 可以使用session进行请求 -> session 可以认为是一连串的请求, 在这个过程中的cookie不会丢失
'''
import requests

# 会话
session = requests.session()
data = {
    "username": "19817578769",
    "password": "2dadd1c1c49b05ab3bb6689ab1c542be2682b3f1b72f9befa3459077b90b3d244743cd9a55b9db154cf709e0395ea77b"
                "51b3eb8429226e3922ac8b6b0992669c6fe68184c4b9ddf9379c0e3d22d77aa0812f6be2dc3ee212a3a1876dba8c4ed56"
                "4a8937a1ebe7b51195bc48332ec39172b70f64955048d3e896c836a52f03b6e "
}

# 1. 登录
url = "https://ptlogin.yuewen.com/login/login?callback=jQuery19108126529430716407_1658991401246&appId=10&areaId=1" \
      "&source=&returnurl=https%3A%2F%2Fwww.qidian.com%2FloginSuccess%3Fsurl%3Dhttps%253A%252F%252Fwww.qidian.com" \
      "%252F&version=&imei=&qimei=&target=iframe&ticket=1&autotime=30&jumpdm=yuewen&ajaxdm=yuewen&auto=1&sdkversion" \
      "=&ywtoken=AhzCYs%2FsnVbXoLsBIUMCvdtUL4hNdPCGhyVRR8EZL%2BA%3D&username=19817578769&password" \
      "=2dadd1c1c49b05ab3bb6689ab1c542be2682b3f1b72f9befa3459077b90b3d244743cd9a55b9db154cf709e0395ea77b51b3eb8429226e3922ac8b6b0992669c6fe68184c4b9ddf9379c0e3d22d77aa0812f6be2dc3ee212a3a1876dba8c4ed564a8937a1ebe7b51195bc48332ec39172b70f64955048d3e896c836a52f03b6e&code=&method=LoginV1.loginCallback&sessionkey=&format=jsonp&_=1658991401248 "
resp = session.get(url, data=data)
print(resp.text)
print(resp.cookies)  # 看cookie

# # 2. 拿书架上的数据
# # 刚才的那个session中是有cookie的
# resp = session.get('https://user.17k.com/ck/author/shelf?page=1&appKey=2406394919')
# # 直接json
# print(resp.json())

# resp = requests.get("https://user.17k.com/ck/author/shelf?page=1&appKey=2406394919", headers={
#     "Cookie": ""
# })
# print(resp.text)
