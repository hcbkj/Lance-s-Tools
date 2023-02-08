'''
多态 不同的子类对象调用相同的父类方法，产生不同的执行结果
    1.多态可以增加代码的灵活度
    2.多态是以 继承 和 重写父类方法 为前提
    3.多态是调用方法的技巧，不会影响到类的内部设计
'''


class A:
    # 人类
    def work(self):
        print('人类需要工作')


class B(A):
    # 程序员
    def work(self):
        print('程序员在工作 --- 代码')


class C(A):
    # 设计师
    def work(self):
        print('设计师在工作 --- 图纸')


b = B()
c = C()
b.work()
c.work()
