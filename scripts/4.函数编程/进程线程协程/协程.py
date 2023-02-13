import time

# def func():
#     print("123")
#     time.sleep(1)       # 让当前的线程处于阻塞状态,cpu是是不为我工作的
#     print("12345")
#
# if __name__ == '__main__':
#     func()

# input() 时程序也是处于阻塞状态, requests.get(),在网络请求返回数据之前,程序也是处于阻塞状态的
# 一般情况下,当程序处于IO操作的是时候,线程都会处于阻塞状态

"""
协程: 当程序遇见了IO操作的时候,可以选择性的切换到其他任务上.
在微观上是,一个任务一个任务的进行切换,切换条件一般是IO
在宏观上, 我们能看到的其实是多个任务在一起执行
多任务异步操作

上方所将的一切,都是在单线程的情况下
尽可能充分的利用单线程的资源
且协程的操作模型是由程序来实现的,而不是系统
"""

# python编写协程的程序
import asyncio

async def func1():
    # 异步协程函数
    print('你好,我是张三')
    # time.sleep(3)   # 当程序出现了同步操作的时候, 异步就中断了
    await asyncio.sleep(3)    # 异步操作的代码
    print('张三搞定')

async def func2():
    print('你好,我是潘周丹')
    # time.sleep(2)
    await asyncio.sleep(2)
    print('潘周丹搞定')

async def func3():
    print('你好,我是赵构')
    # time.sleep(4)
    await asyncio.sleep(4)
    print('赵构搞定')

# if __name__ == '__main__':
#     # g = func1()       # 异步协程函数,此时函数执行得到的是一个协程对象
#     # # print(g)
#     # asyncio.run(g)      # 协程程序运行需要asyncio模块的支持
#
#     f1 = func1()
#     f2 = func2()
#     f3 = func3()
#
#     tasks = [
#         f1, f2, f3
#     ]
#
#     t1 = time.time()
#     # 一次性启动多个任务(协程)
#     asyncio.run(asyncio.wait(tasks))
#     t2 = time.time()
#
#     print(t2 - t1)


# 推荐的写法,可以有效避免主线程过长
# 协程函数
async def main():
    # # 第一种写法
    # f1 = func1()        # 协程对象
    # # 一般await挂起操作都放在协程对象前面
    # await f1

    # 第二种写法(推荐), 便于套在爬虫上
    # 统一执行
    # tasks = [
    #     func1(),
    #     func2(),
    #     func3(),
    # ]

    # 为避免报错,可以手动的把协程对象包装成task对象
    tasks = [
        asyncio.create_task(func1()),     # 执行
        asyncio.create_task(func2()),     # 执行
        asyncio.create_task(func3()),     # 执行
    ]

    await asyncio.wait(tasks)


if __name__ == '__main__':
    t1 = time.time()
    # 一次性启动多个任务(协程)
    asyncio.run(main())
    t2 = time.time()
    print(t2 - t1)


# # 在爬虫领域的应用
# async def download(url):
#     print("准备开始下载")
#     await asyncio.sleep(2)      # 模拟网络请求, 在此处requests.get()不好使,因为requests.get()是同步操作,换成异步方式
#     print("下载完成")
#
#
# async def main():
#     urls = [
#         'http://www.baidu,com',
#         'http://www.bilibili.com',
#         'http://www.163.com',
#     ]
#
#     tasks = []
#     for url in urls:
#         d = asyncio.create_task(download(url))       # 不是函数执行,是得到了一个协程对象
#         tasks.append(d)
#
#     await asyncio.wait(tasks)
#
#
# if __name__ == '__main__':
#     asyncio.run(main())
