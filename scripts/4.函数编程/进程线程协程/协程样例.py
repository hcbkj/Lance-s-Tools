# -*- coding: utf-8 -*-
# @Time    : 2023/2/13 10:33

"""
asyncio.get_event_loop() 函数是 asyncio 中的一个函数，它用于获取事件循环（event loop）。事件循环是一个主要组件，它用于管理 asyncio 应用程序中的协程和其他任务。
run_until_complete(future) 函数用于在事件循环中执行协程。它的参数是一个 future 对象，它代表一个未来的操作。最终，当 future 完成时，run_until_complete 函数会终止事件循环。
结合使用，这两个函数可以帮助您在 asyncio 中管理并执行协程。
"""

import asyncio


async def my_coroutine():
    # Some async code here
    pass


loop = asyncio.get_event_loop()
task = loop.create_task(my_coroutine())
loop.run_until_complete(task)
loop.close()

"""
在这个例子中，我们首先调用 asyncio.get_event_loop() 获取事件循环。
然后我们使用该事件循环的 create_task 方法将我们的协程包装在任务中，以便在事件循环中执行。
最后，我们调用 run_until_complete 函数，它会在事件循环中运行协程，直到它完成。
"""

"""
asyncio.gather(*coroutines, loop=None, return_exceptions=False) 是 asyncio 中的一个函数，它用于在协程中同时运行多个任务，并等待它们完成。
这是一种非常有用的方法，因为它允许您在不阻塞主程序的情况下并行执行多个任务。
"""
import asyncio


async def task_1():
    # Some async code here
    pass


async def task_2():
    # Some async code here
    pass


async def main():
    # Use asyncio.gather to run tasks concurrently
    await asyncio.gather(task_1(), task_2())


# Run the main coroutine
asyncio.run(main())

"""
在这个例子中，我们定义了两个协程 task_1 和 task_2。然后我们在 main 协程中调用 asyncio.gather 函数，同时运行两个任务。asyncio.gather 函数等待两个任务完成，然后继续执行主协程。
通过使用 asyncio.gather，您可以极大地提高程序的并行性，提高程序的执行速度。
"""

"""
aiohttp.ClientSession() 是 aiohttp 库中的一个函数，它用于创建一个客户端 HTTP 会话。
这个会话可以在多个请求之间共享一些资源，如身份验证凭证，代理服务器，连接池等。这可以帮助您更有效地处理请求，并避免重复创建连接等操作。
"""
import aiohttp


async def fetch_data(session, url):
    async with session.get(url) as response:
        data = await response.text()
        return data


async def main():
    async with aiohttp.ClientSession() as session:
        data = await fetch_data(session, 'https://www.example.com/data')
        print(data)


# Run the main coroutine
asyncio.run(main())
"""
在这个例子中，我们使用 aiohttp.ClientSession() 创建了一个客户端会话，并使用上下文管理器在 main 协程的作用域内管理它。
然后我们调用了 fetch_data 函数，使用会话对象从给定 URL 获取数据。这样，我们可以在多个请求中共享一个会话，从而更有效地处理请求。
"""

"""
asyncio.ensure_future() 函数是在 Python 的 asyncio 库中的一个函数，用于将协程（coroutine）封装为一个未来（Future）对象。
未来（Future）是 asyncio 中的一个类，表示一个异步操作的最终结果。它的作用类似于线程中的Future，但是针对协程而设计。
使用 asyncio.ensure_future() 函数可以很方便地将协程放入事件循环，并在后台异步地运行。这样可以提高程序的并发性和效率。
下面是一个使用 asyncio.ensure_future() 函数的例子：
"""
import asyncio


async def my_coroutine():
    # 模拟一个异步操作，如网络请求
    await asyncio.sleep(1)
    return "Hello, World!"


async def main():
    # 将协程封装为未来
    future = asyncio.ensure_future(my_coroutine())
    # 等待未来完成
    result = await future
    print(result)


# 启动事件循环
asyncio.run(main())
