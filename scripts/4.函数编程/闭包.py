'''
闭包函数：本质，内层函数对外层函数的局部变量的使用，此时内层函数被称为闭包函数
    1.可以让变量常驻与内存
    2.可以避免全局变量被修改（局部变量不易被修改，闭包可以在外部修改局部变量）
'''

def func():
    a = 10
    def inner():        # 闭包函数
        nonlocal a
        a += 1
        return a
    return inner

ret = func()
# ret ==>inner * 不确定inner()什么时候会被执行 所以inner()内部用到的变量a需要一直都能被访问到，所以a在内存中常驻

r1 = ret()      # ret()等价于inner()
print(r1)
r2 = ret()
print(r2)

