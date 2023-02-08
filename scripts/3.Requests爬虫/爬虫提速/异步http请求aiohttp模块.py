# requests.get() 同步的代码 -> 异步操作aiohttp
# pip install aiohttp

import asyncio
import aiohttp

urls = [
    "http://kr.shanghai-jiuxin.com/file/2020/1031/191468637cab2f0206f7d1d9b175ac81.jpg",
    "http://kr.shanghai-jiuxin.com/file/2020/1031/563337d07af599a9ea64e620729f367e.jpg",
    "http://kr.shanghai-jiuxin.com/file/2020/1031/774218be86d832f359637ab120eba52d.jpg"
]


async def aioDownload(url):
    # 发送请求，得到图片内容，保存到图片
    # s = aiohttp.ClientSession()  <==> requests
    # s.get()   s.post()    <==>    requests.get()  requests.post()
    name = url.rsplit("/", 1)[1]
    async with aiohttp.ClientSession() as session:      # requests
        async with session.get(url) as resp:        # resp = requests.get()
            # 请求回来了,写入文件
            # 可以学一下aiofiles
            with open(name, mode="wb") as f:         # 创建文件
                f.write(await resp.content.read())      # 需要加上一个await来挂起


async def main():
    tasks = []
    for url in urls:
        tasks.append(aioDownload(url))

    await asyncio.wait(tasks)


if __name__ == '__main__':
    asyncio.run(main())
