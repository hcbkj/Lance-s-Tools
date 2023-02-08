"""
匿名函数:
    lambda表达式   简化函数操作
    语法:
        变量 = lambda 参数1,参数2,参数3...: (函数体) 返回值

"""

# def func(a, b):
#     return a + b
#
# ret = func(12, 13)
# print(ret)

fn = lambda a, b: a + b
print(fn)       # <function <lambda> at 0x000002B8F472DCA0>
ret = fn(12, 13)
print(ret)
