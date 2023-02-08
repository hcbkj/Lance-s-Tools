"""
for 变量 in 可迭代:
    pass

iterable: 可迭代的
iterator: 迭代器
    str, list, tuple, dict, open()

可迭代的数据类型都会提供一个叫做迭代器的东西，这个迭代器可以帮助我们把数据类型中的所有数据逐一的拿到

获取迭代器的两种方案：
    1. iter() 内置函数可以直接拿到迭代器
    2. __iter__ 特殊方法 用的少

从迭代器中获取数据：
    1. next() 内置函数
    2. __next__ 特殊方法

for里面一定要拿迭代器的，所以出现所有不可迭代东西都不可以用for循环
for循环一定有__next__出现

总结：
    迭代器统一了所有不同数据类型的遍历工作
    让不同数据类型有了相同的遍历方式
    迭代器本身也是可迭代的内容

迭代器的特性：
    1. 只能向前不能反复
    2. 特别节省内存，可以遍历庞大的数据集
    3. 惰性机制

"""

# it = iter("你叫什么名字")
# print(it)
#
# print(next(it))
# print(next(it))
# print(next(it))
# print(next(it))
# print(next(it))
# print(next(it))
#
# print(next(it))     # StopIteration: 迭代已经停止了，不可以再次从迭代器中拿数据了


# it = "呵呵哒".__iter__()
#
# print(it.__next__())
# print(it.__next__())
# print(it.__next__())


# # 模拟for循环工作原理
# s = '我是数据'
# it = s.__iter__()   # 拿到迭代器
# while 1:
#     try:
#         data = it.__next__()
#         print(data)     # for循环的循环体
#     except StopIteration:
#         break
# print(123456)

# 迭代器本身也是可迭代的内容
ss = "你好啊，我叫柯南"
it = ss.__iter__()
for i in it:
    print(i)
