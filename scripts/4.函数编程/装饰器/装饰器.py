'''
内容回顾：
    1.函数可以当作参数来进行传递
    2.函数可以当作返回值来返回
    3.函数名称可以当作变量进行赋值操作

装饰器：*结论
    装饰器本质上是一个闭包
    作用：
        在不改变原有函数调用的情况下，给函数增加新的功能。
        直白：可以在函数的前后添加新功能，但是不改变原来的代码

    应用场景：
        在用户登录、日志

    雏形：
        def wrapper(fn):        # wrapper:装饰器, fn:目标函数
            def inner():
                # 在目标函数执行之前。。。
                fn()
                # 在目标函数执行之后。。。
            return inner        # 返回inner是返回函数，返回inner()是返回函数执行结果

'''

# 1
# def func():
#     print('我是函数')
#
#
# def gggg(fn):  # fn要求是个函数
#     fn()  # 等价于func()
#
#
# gggg(func)


# # 2
# def func():
#     def inner():
#         print('123')
#     return inner
#
# ret = func()
# ret()


# # 3
# def func1():
#     print('我是函数1')
#
#
# def func2():
#     print('我是函数2')
#
#
# func1 = func2
# func1()     # 实际上func1已经被赋值为func2，等于func2()


# 装饰器：

def guanjia(game):
    def inner():
        print("开启外挂")
        game()      # 直接玩起来了
        print("关闭外挂")
    return inner


@guanjia        # 相当于play_dnf = guanjia(play_dnf)
def play_dnf():
    print('你好啊，我叫赛琳娜，今天又是美好的一天！')


@guanjia        # 相当于play_lol = guanjia(play_lol)
def play_lol():
    print('德玛西亚！！')


# print("开启外挂")
# play_dnf()
# print("关闭外挂")

# play_dnf = guanjia(play_dnf)        # 此时已经让管家把游戏重新封装了一边，我这边把原来的游戏替换了
# play_lol = guanjia(play_lol)        # 让管家把lol也重新封装了一下。

play_dnf()      # 此时运行的是管家给的内层函数inner
play_lol()

