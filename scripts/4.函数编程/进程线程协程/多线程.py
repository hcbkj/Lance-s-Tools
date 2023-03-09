# 线程, 进程
# 进程是资源单位, 每一个进程至少要有一个线程
# 线程是执行单位

# 启动每一个程序默认都会有一个主线程

# def func():
#     for i in range(100):
#         print("func", i)
#
#
# if __name__ == '__main__':
#     func()
#     for i in range(100):
#         print("main", i)


# 多线程
from threading import Thread  # 线程类


# 实现多线程的第一种方法
def func(name):
    for i in range(100):
        print(name, i)


if __name__ == '__main__':
    # t = Thread(target=func)     # 创建线程并给线程安排任务
    # t.start()       # 开始执行该线程，实际上，只是给线路赋予了一个状态，表示可以开始了，具体的执行时间由cpu决定

    t1 = Thread(target=func, args=("周杰伦",))  # 传参 args(,)必须是元组,因此,当args()里面只有一个参数的时候,要加上逗号,
    t1.start()
    t2 = Thread(target=func, args=("王力宏",))  # 传参 args(,)必须是元组,因此,当args()里面只有一个参数的时候,要加上逗号,
    t2.start()

    for i in range(100):
        print("main", i)

# # 实现多线程的第二种方法
# class MyThread(Thread):
#     def run(self):
#         # 固定的, --> 当线程可以被执行的时候,被执行的就是run()
#         for i in range(100):
#             print("子线程", i)
#
# if __name__ == '__main__':
#     t = MyThread()
#     # t.run()       # 方法的调用 -> 单线程??
#     t.start()       # 开启线程
#
#     for i in range(100):
#         print("主线程", i)
