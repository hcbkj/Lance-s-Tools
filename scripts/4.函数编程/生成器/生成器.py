"""
生成器 generator ：
    生成器的本质就是迭代器

    创建生成器的常用方法：
        1.生成器函数
        2.生成器表达式

    生成器函数特性
        1. 生成器函数中有一个关键字yield
        2. 生成器函数执行的时候，得到的是生成器，并不会执行函数

        yield：只要函数中出现了yield，它就是一个生成器函数
            作用：
                1.可以返回数据
                2.可以分段的执行函数中的内容，通过__next__()可以执行到下一个yield的位置

        优势：用好了，特别节省内存

        
"""

# def func():
#     print(123456)
#     yield 999       # yield 也有返回的意思。
#
# ret = func()
# # print(ret)      # <generator object func at 0x0000019F7ED94890> 生成器对象
# print(ret.__next__())   # yield只有执行到next的时候才会返回数据 （迭代器的惰性机制）
# print(ret.__next__())   # StopIteration


# # 分段执行示例
# def func():
#     print(123)
#     yield 666
#     print(456)
#     yield 999
#
# ret = func()
# print(ret.__next__())
# print("------")
# print(ret.__next__())       # 接着上次执行的位置继续执行


# # 应用场景
# # 例：去工厂定制一批衣服
# def order():
#     lst = []
#     for i in range(10000):
#         lst.append(f'衣服{i}')
#     return  lst
#
# lst = order()
# print(lst)
# 内存就是这样消耗的，可以改用生成器去节省内存

def order():
    lst = []
    for i in range(10000):
        lst.append(f'衣服{i}')
        if len(lst) == 50:
            yield lst
            # 下一次拿数据，清空数据列表
            lst = []


gen = order()
# print(gen)
# 生成器函数实质上是迭代器
print(gen.__next__())
print(gen.__next__())

