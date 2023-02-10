import hashlib
import requests
import time


def genearteMD5(strs: str) -> str:
    # 创建md5对象
    hl = hashlib.md5()
    # Tips
    # 此处必须声明encode
    # 否则报错为：hl.update(str)    Unicode-objects must be encoded before hashing
    hl.update(strs.encode(encoding='utf-8'))
    return hl.hexdigest()


def signutil(postBody: dict, secret: str) -> str:
    # 进行签名验证

    # 按照参数名的字典排序
    postBody_data = sorted(postBody.keys(), reverse=True)
    # print(postBody_data)

    # 拼接参数，按照a=1&b=2的规则拼接
    strs = ''
    for i in postBody_data:
        strs += f"{i}={postBody[i]}&"

    # 拼接字符串的尾部拼接上 secret=xxx
    strs += f"secret={secret}"
    # print(strs)

    # 计算MD5值，小写
    return genearteMD5(strs)


def httputil(url, payload, key, secret):
    file_name = payload['file_path'].split('\\')[-1]
    files = [
        ('file', (file_name, open(payload['file_path'], 'rb'), 'image/jpeg'))
    ]
    headers = {
        # 下面的key从/admin界面查询或由管理员下发， sign为签名，通过签名工具类进行计算
        'key': key,
        'sign': signutil(payload, secret)
    }

    response = requests.request("POST", url, headers=headers, data=payload, files=files)
    print(response.ok)
    print(response.content)
    return response.json()


if __name__ == '__main__':
    start_time = time.time()
    # api 为请求的接口
    api = '/api/idcard/process'
    # key 和 secret 从管理界面（"http://172.29.9.115:8000/admin"）查看 或由管理员下发
    key = '123'
    secret = '12sass'
    # payload为当前请求的全部参数
    payload = {
        'file_path': r"D:\工作相关\需求\阳光保险材料整理\test\北京中关村银行股份有限公司\C833620200714814026\IDnumber1594372128979.jpg"
    }

    # url = "http://172.29.9.115:8000" + api      # 内网请求
    url = "http://120.26.77.174:8000" + api  # 外网请求
    # url = "http://127.0.0.1:8000" + api
    text = httputil(url, payload, key, secret)
    end_time = time.time() - start_time
    print(text)
    print(end_time)
