'''
装饰器：*结论
    装饰器本质上是一个闭包
    作用：
        在不改变原有函数调用的情况下，给函数增加新的功能。
        直白：可以在函数的前后添加新功能，但是不改变原来的代码

    应用场景：
        在用户登录、日志

    雏形：
        def wrapper(fn):        # wrapper:装饰器, fn:目标函数
            def inner(*args, **kwargs):
                # 在目标函数执行之前。。。
                fn(*args, **kwargs)
                # 在目标函数执行之后。。。
            return inner        # 返回inner是返回函数，返回inner()是返回函数执行结果

'''

# 装饰器：

def guanjia(game):
    def inner(*args, **kwargs):     # inner添加了参数，且不限制参数的数量，args 一定是一个元组 kwargs 一定是一个字典 args('admin', '123456')
        print("开启外挂")
        # *，** 表示把args元组和kwargs字典打散成 位置参数 以及 关键字参数传递进去
        game(*args, **kwargs)   # game('admin', '123456')
        print("关闭外挂")
    return inner


@guanjia        # 相当于play_dnf = guanjia(play_dnf)
def play_dnf(username, password):
    print('我要开始玩dnf了', username, password)
    print('你好啊，我叫赛琳娜，今天又是美好的一天！')


@guanjia        # 相当于play_lol = guanjia(play_lol)
def play_lol(username, password, hero):
    print('我要开始玩lol了', username, password, hero)
    print('德玛西亚！！')


play_dnf('admin', '123456')      # inner
play_lol('admin', '456789', '盖伦')
