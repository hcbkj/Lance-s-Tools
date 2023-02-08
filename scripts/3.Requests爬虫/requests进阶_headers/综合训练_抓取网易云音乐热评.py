'''
1. Form Data中 找到未加密的参数                      # window.asrsea(参数, xxx, xxx)
2. 想办法去把参数进行加密(必须参考网易的加密逻辑), params => encText, encSecKey => encSecKey
3. 请求到网页网易, 拿到评论信息
'''
import requests
from Crypto.Cipher import AES
from base64 import b64encode
import json

# 网易云登录之后 csrf_token=就有值了
url = "https://music.163.com/weapi/comment/resource/comments/get?csrf_token="

# 请求方式是post
data = {
    "rid": "R_SO_4_1325905146",
    "threadId": "R_SO_4_1325905146",
    "pageNo": "1",
    "pageSize": "20",
    "cursor": "-1",
    "offset": "0",
    "orderType": "1",
    "csrf_token": "",
}

# 处理加密过程
'''
    function a(a) {         # a = 16
        var d, e, b = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", c = "";
        for (d = 0; a > d; d += 1)      # 循环16次
            e = Math.random() * b.length,       # random 随机数 例:1.2345
            e = Math.floor(e),          # 取整 例:1
            c += b.charAt(e);           # 取字符串中的xxx位置 例:b
        return c        # 16个随机的字符串
    }
    function b(a, b) {      # a: 要加密的内容, 
        var c = CryptoJS.enc.Utf8.parse(b)      # b是密钥
          , d = CryptoJS.enc.Utf8.parse("0102030405060708")
          , e = CryptoJS.enc.Utf8.parse(a)      # e是数据
          , f = CryptoJS.AES.encrypt(e, c, {    # c: 加密的密钥
            iv: d,          # AES加密中的iv是偏移量
            mode: CryptoJS.mode.CBC     # 加密模式,CBC
        });
        return f.toString()         # 加密后把f变成了字符串
    }
    function c(a, b, c) {       # 算法,里面并不产生随机值
        var d, e;
        return setMaxDigits(131),
        d = new RSAKeyPair(b,"",c),
        e = encryptedString(d, a)
    }
    
    # d: 数据data, e: buV4Z(["流泪", "强"]) => Console => 010001, 
    f: buV4Z(Rg0x.md) => Console => "很长一串"    g: buV4Z(["爱心", "女孩", "惊恐", "大笑"]) => 0CoJUm6Qyw8W8jud
    
    function d(d, e, f, g) {        
            var h = {}      # 空对象
          , i = a(16);      # function a() => i是16位的随机值
        return h.encText = b(d, g),         # g就是密钥
        h.encText = b(h.encText, i),        # 返回的就是params, i也是密钥
        h.encSecKey = c(i, e, f),           # 返回的就是encSecKey  e和f是固定值, 在i身上做文章, 当此时的i固定, 则key一定能够固定
        h       # return h
    }
    
    # 两次加密
    # 数据 + g => b => 第一次加密 + i => params
'''

# 服务于d
e = '010001'
f = '00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7 '
g = '0CoJUm6Qyw8W8jud'
i = "7JyxU1YRf6S7xeDe"


def to_16(data):
    # 处理数据格式
    # 转化为16的倍数，为下方的加密算法服务
    pad = 16 - len(data) % 16
    data += chr(pad) * pad
    return data


def get_encSecKey():
    return "bb29f6a16261686c435f66869e4f619c8c7b16a757d656aab5196f1d8aa8a0ee06f280141e4f3b30719e297f87031cf7e33081985eb9451ef1528c8965e3154854c3d06937b3abdda1dca81a907ac900de447ba0589e6bbe6eba9300653724dcc950161baf7aa6d9bec8bb12da4c99c657f0bc510596099977b3aece64b10c47"


# 把参数进行加密
def get_params(data):
    # 默认这里收到的是字符串
    # 还原出原来代码中的function d(...)
    first = enc_params(data, g)     # 两次加密
    second = enc_params(first, i)
    return second  # 返回的就是params


def enc_params(data, key):  # 加密过程
    # 还原出原来代码中的function b(...)
    iv = "0102030405060708"
    data = to_16(data)
    aes = AES.new(key=key.encode('utf-8'), iv=iv.encode('utf-8'), mode=AES.MODE_CBC)  # 创建加密器对象
    bs = aes.encrypt(data.encode('utf-8'))  # 加密, 加密的内容的长度一定要是16的倍数
    return str(b64encode(bs), 'utf-8')  # 转化成字符串返回


resp = requests.post(url, data={
    'params': get_params(json.dumps(data)),
    'encSecKey': get_encSecKey(),
})

print(resp.text)
