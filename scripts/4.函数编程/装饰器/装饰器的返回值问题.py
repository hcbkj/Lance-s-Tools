'''
装饰器：*结论
    装饰器本质上是一个闭包
    作用：
        在不改变原有函数调用的情况下，给函数增加新的功能。
        直白：可以在函数的前后添加新功能，但是不改变原来的代码

    应用场景：
        在用户登录、日志


    通用装饰器的写法：
        def wrapper(fn):        # wrapper:装饰器, fn:目标函数
            def inner(*args, **kwargs):
                # 在目标函数执行之前。。。
                ret = fn(*args, **kwargs)
                # 在目标函数执行之后。。。
                return ret
            return inner        # 返回inner是返回函数，返回inner()是返回函数执行结果

        @wrapper
        def target():
            pass

        target()        # target() ==> inner()


    一个函数可以被多个装饰器装饰:
    规则：
        wrapper1 wrapper2 target wrapper1 wrapper2
'''

# 装饰器：
# def guanjia(game):
#     def inner(*args, **kwargs):
#         print("开启外挂")
#         ret = game(*args, **kwargs)     # 这里是目标函数的执行，从这里是可以拿到目标函数的返回值的。
#         print("关闭外挂")
#         return ret
#     return inner
#
#
# @guanjia        # 相当于play_dnf = guanjia(play_dnf)
# def play_dnf(username, password):
#     print('我要开始玩dnf了', username, password)
#     print('你好啊，我叫赛琳娜，今天又是美好的一天！')
#     return "一把屠龙刀"
#
#
# @guanjia        # 相当于play_lol = guanjia(play_lol)
# def play_lol(username, password, hero):
#     print('我要开始玩lol了', username, password, hero)
#     print('德玛西亚！！')
#
#
# ret = play_dnf('admin', '123456')      # inner
# print(ret)


# 一个函数可以被多个装饰器装饰

def wrapper1(fn):
    def inner(*args, **kwargs):
        print("wrapper1 in")    # 1
        ret = fn(*args, **kwargs)
        print("wrapper1 out")   # 5
        return ret
    return inner


def wrapper2(fn):
    def inner(*args, **kwargs):
        print("wrapper2 in")    # 2
        ret = fn(*args, **kwargs)
        print("wrapper2 out")   # 4
        return ret
    return inner


@wrapper1       # target = wrapper1(wrapper2.inner) ==> target: wrapper1.inner
@wrapper2       # target = wrapper2(target) ==> target: wrapper2.inner
def target():
    print('我是目标函数')     # 3
    return 1


print(target())
# wrapper1 wrapper2 target wrapper1 wrapper2
"""
wrapper1 in
wrapper2 in
我是目标函数
wrapper2 out
wrapper1 out
"""


