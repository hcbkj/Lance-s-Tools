# Python 的 functools 模块提供了一些常用的高阶函数，也就是用于处理其它函数的特殊函数。换言之，就是能使用该模块对 所有可调用对象( 即 参数 或(和) 返回值 为其他函数的函数 ) 进行处理。
# Python 的 functools 模块的作用： 为 可调用对象(callable objects) 和 函数 定义高阶函数或操作。简单地说，就是基于已有的函数定义新的函数。所谓高阶函数，就是以函数作为输入参数，返回也是函数。
# 原文链接：https://blog.csdn.net/lyshark_lyshark/article/details/125848112

from functools import *

@cache(...)
def xxx():
    ...