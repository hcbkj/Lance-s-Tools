# -*- coding: utf-8 -*-
# @Time    : 2023/2/13 10:24
# @Author  : chat gpt

import asyncio
import aiohttp


async def download_file(session, url, filename, size):
    async with session.get(url) as resp:
        if resp.status == 200:
            if size < 5 * 1024 * 1024:
                print(f"Downloading small file {filename}")
            else:
                print(f"Downloading large file {filename}")
            with open(filename, "wb") as f:
                while True:
                    chunk = await resp.content.read(1024)
                    if not chunk:
                        break
                    f.write(chunk)
        else:
            print(f"Error downloading file {filename}: {resp.status}")


async def download_files(files: list):
    """
    异步下载函数
    :param files: url, filename, size in list
    :return: None
    """
    # 先创建一个客户端 HTTP 会话, 这个会话的作用是在会话中的多个请求可以共享资源,避免重复链接
    async with aiohttp.ClientSession() as session:
        # 任务列表
        # asyncio.ensure_future()用于将协程封装为future对象,这是为了将协程放入事件循环，并在后台异步地运行。
        tasks = [asyncio.ensure_future(download_file(session, url, filename, size))
                 for url, filename, size in files]
        await asyncio.gather(*tasks)


if __name__ == "__main__":
    files = [("http://example.com/file1.txt", "file1.txt", 1024),
             ("http://example.com/file2.txt", "file2.txt", 10 * 1024 * 1024)]

    # 下面两个函数可以帮助用户在 asyncio 中管理并执行协程。
    # get_event_loop()
    # 获取事件循环，可以简化理解为对协程的事件进行了实例化，后续操作对象都为事件循环对象loop
    loop = asyncio.get_event_loop()
    # run_until_complete(future)
    # 在事件循环中运行协程, run函数,future参数应该是一个未来的操作,为函数对象. 最终，当 future 完成时，run_until_complete 函数会终止事件循环。
    loop.run_until_complete(download_files(files))
    # 关闭事件循环
    loop.close()
