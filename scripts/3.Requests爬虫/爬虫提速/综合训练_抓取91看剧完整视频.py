"""
思路:
    1. 拿到主页面的页面源代码, 找到iframe
    2. 从iframe的页面源代码中拿到m3u8文件的地址
    3. 下载第一层m3u8文件 -> 下载第二层m3u8文件(视频存放路径)
    4. 下载视频
    5. 下载秘钥, 进行解密操作
    6. 合并所有ts文件为一个mp4文件
"""
import requests
from bs4 import BeautifulSoup as bs  # 在这种页面源代码中只有一个iframe，且该iframe正好是需要的iframe的时候，使用bs比较简单
import re
import asyncio
import aiohttp
import aiofiles
from Crypto.Cipher import AES
import os


def get_iframe_url(resp):
    main_page = bs(resp.text, 'html.parser')
    src = main_page.find('iframe').get('src')
    return src


def get_m3u8_from_iframe(url):
    resp = requests.get(url)
    m3u8_url = re.search(r'var main = "(?P<m3u8_url>.*?)"', resp.text, re.S).group('m3u8_url')
    return m3u8_url


def download_m3u8_file(url, name):
    resp = requests.get(url)
    with open(name, mode='wb') as f:
        f.write(resp.content)


async def aio_download_task(url, name, session):
    # async with aiohttp.ClientSession() as session
    # 本来在异步任务的第一步是创建会话来进行异步aiohttp请求,但是在异步任务的内部写会导致每次异步(ts下载)都创建一个新的Session,所有在上一层的异步函数内创建Session
    async with session.get(url) as resp:
        # 下载ts切片文件
        async with aiofiles.open(f'video{name}', mode='wb') as f:
            await f.write(await resp.content.read())  # 把下载到的内容写入到文件中
    print(f"{name}下载完毕")


async def aio_download_video(up_url):
    # https://boba.52kuyun.com/20170906/Moh2l9zV/hls/
    tasks = []  # 创建任务列表
    async with aiohttp.ClientSession() as session:  # 提前准备好session
        async with aiofiles.open('second_m3u8.txt', mode='r', encoding='utf-8') as f:
            async for line in f:
                if line.startswith("#"):
                    continue
                # line --> xxxxx.ts
                line = line.strip()  # 格式化
                # 拼接真正的ts文件路径
                ts_url = up_url + line
                # 有了url就开始创建异步任务
                task = asyncio.create_task(aio_download_task(ts_url, line, session))  # 创建任务
                tasks.append(task)  # 把任务加入任务列表
            await asyncio.wait(tasks)  # 当第一个ts进入io操作(下载)时,await,进入下一个ts


def get_key(url):
    resp = requests.get(url)
    return resp.text


async def dec_ts(name, key):
    aes = AES.new(key=key, IV=b'0000000000000000', mode=AES.MODE_CBC)  # 偏移量IV是字节流16位(密钥是几位就是几位)  解码模式默认CBC
    async with aiofiles.open(f'video/{name}', mode='rb') as f1, aiofiles.open(f'video/temp_{name}', mode='wb') as f2:
        # 一个切片打开两个对象,一个读一个写,写的生成temp_新文件
        bs = await f1.read()  # 从源文件读取内容
        await f2.write(aes.decrypt(bs))  # 把解密好的内容写入文件
    print(f"{name}处理完毕")


async def aio_dec(key):
    tasks = []  # 同样是先创建任务列表
    async with aiofiles.open('second_m3u8.txt', mode='r', encoding='utf-8') as f:
        async for line in f:
            if line.startswith("#"):
                continue
            line = line.strip()
            # 开始创建异步任务
            task = asyncio.create_task(dec_ts(line, key))
            tasks.append(task)
        await asyncio.wait(tasks)


def merge_ts():
    # 不同电脑写法格式不同
    # mac: cat 1.ts 2.ts 3.ts > xxx.mp4
    # windows: copy /b 1.ts+2.ts+3.ts xxx.mp4
    lst = []
    with open('second_m3u8.txt', mode='r', encoding='utf-8') as f:
        for line in f:
            if line.startswith('#'):
                continue
            line = line.strip()
            lst.append(f'video/temp_{line}')

    s = '+'.join(lst)
    os.system(f'copy /b {s} movie.mp4')
    print('搞定!')


def main():
    url = 'https://www.91kanju.com/vod-play/541-2-1.html'
    resp = requests.get(url)
    # 1. 拿到主页面的页面源代码, 找到iframe
    src = get_iframe_url(resp)
    # 拿到iframe的域名
    # "https://boba.52kuyun.com/share/xfPs9NPHvYGhNzFp"
    iframe_url = src.split('/share')[0]

    # 2. 从iframe的页面源代码中拿到m3u8文件的地址
    m3u8_url = get_m3u8_from_iframe(src)
    # 拼接出完整的的m3u8文件下载地址
    first_m3u8_url = iframe_url + m3u8_url
    # https://boba.52kuyun.com/20170906/Moh2l9zV/index.m3u8?sign=548ae366a075f0f9e7c76af215aa18e1

    # 3. 下载第一层m3u8文件 -> 下载第二层m3u8文件(视频存放路径)
    # 先下载第一层m3u8
    download_m3u8_file(first_m3u8_url, 'first_m3u8.txt')
    # 读取m3u8文件,获得第二层m3u8
    with open('first_m3u8.txt', mode='r', encoding='utf-8') as first_m3u8_file:
        for line in first_m3u8_file:
            if line.startswith('#'):
                # m3u8文件中#开头的部分并不是我所需要的
                continue
            else:
                line = line.strip()  # 格式化处理     hls/index.m3u8
                # 拼接出第二层m3u8的路径
                # https://boba.52kuyun.com/20170906/Moh2l9zV/ + hls/index.m3u8
                # https://boba.52kuyun.com/20170906/Moh2l9zV/hls/index.m3u8
                # https://boba.52kuyun.com/20170906/Moh2l9zV/hls/cFN8o3436000.ts
                second_m3u8_url = iframe_url + line
                # 再下载第二层m3u8的内容
                download_m3u8_file(second_m3u8_url, 'second_m3u8.txt')
                print("second_m3u8.txt文件下载完毕")

    # 4. 下载视频
    # 这地方显然是需要异步操作了
    # second_m3u8.txt的解析不能在外面做,需要放在异步函数里面去执行,因为读取.txt文件的操作已经需要异步的处理了
    second_m3u8_url_up = second_m3u8_url.replace("index.m3u8", "")  # 用于拼接
    asyncio.run(aio_download_video(second_m3u8_url_up))

    # 5. 下载秘钥, 进行解密操作
    # 解密的数据很多,且也是多为io操作,显然是异步
    # 首先是要下载密钥
    with open('second_m3u8.txt', mode='r', encoding='utf-8') as second_m3u8_file:
        m3u8_text = ''
        for line in second_m3u8_file:
            m3u8_text += line
        key_url_part = re.search(r'URI="(?P<key_url>.*?)"', m3u8_text, re.S).group('key_url')

    key_url = second_m3u8_url_up + key_url_part
    # 获取密钥的内容
    key_text = get_key(key_url)

    # 解密
    # 需要使用密钥给每一个ts切片文件解密,因此需要异步操作
    asyncio.run(aio_dec(key_text))

    # 6. 合并所有ts文件为一个mp4文件,直接同步操作就行
    # 合并切片的操作,可以由软件来完成,或者是通过程序os.system()来完成合并
    merge_ts()


if __name__ == '__main__':
    main()
